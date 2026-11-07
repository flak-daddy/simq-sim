"""SimQ v2 play commands. Claude runs these and relays the output.

  python3 cli.py new --cash 10000 [--seed S] [--replay RUN]
  python3 cli.py show [--all]          current decision point (--all: full chain)
  python3 cli.py sell P|C STRIKE [N] [--lot L]
  python3 cli.py btc ID|CONTRACT [N]
  python3 cli.py buy N                 buy N shares (round lots)
  python3 cli.py sellsh LOT [N]        sell shares from a lot
  python3 cli.py relot ID LOT          move a covered call to another lot
  python3 cli.py pass | hold            explicit "no (more) orders" here (pass = Monday, hold = Wed/Fri)
  python3 cli.py undo                  remove the last order/pass at this decision point (advances can't be undone)
  python3 cli.py note "text"           add a note to the run's log
  python3 cli.py go                    advance (auto-advance rules, SPEC §5.2); refuses without orders or pass/hold
  python3 cli.py status
  python3 cli.py close|abandon "note"   (writes the run-close one-pager and workbook)
  python3 cli.py report [label]        one-pager PDF on demand
  python3 cli.py compare RUN RUN ...   cross-run table with ruleset differences
"""
import argparse
import json
import os
import secrets
import sys

from simq import display, report, ruleset
from simq.play import ROOT, ActionError, Run

RULESET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rulesets", "ruleset-v2.0.json")
ACTIVE = os.path.join(ROOT, "active.txt")


def active():
    if not os.path.exists(ACTIVE):
        sys.exit("No active run. Start one with: python3 cli.py new --cash N")
    return Run.load(int(open(ACTIVE).read().strip()))


def next_id():
    os.makedirs(ROOT, exist_ok=True)
    ids = [int(d[4:]) for d in os.listdir(ROOT) if d.startswith("run-")]
    return max(ids, default=0) + 1


def out(lines):
    print("\n".join(lines))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("args", nargs="*")
    ap.add_argument("--cash", type=float)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--replay", type=int)
    ap.add_argument("--lot", type=int)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "new":
        if os.path.exists(ACTIVE):
            r = Run.load(int(open(ACTIVE).read().strip()))
            if r.save["run"]["status"] == "active":
                sys.exit(f"Run {r.save['run']['id']} is still active; close or abandon it first.")
        if a.cash is None:
            sys.exit("Starting cash is required: --cash N")
        rs = ruleset.load(RULESET)
        if not rs.get("calibration", {}).get("passed"):
            sys.exit("Ruleset has not passed calibration (hard gate).")
        seed, replay_of = a.seed, None
        if a.replay:
            old = Run.load(a.replay)
            if old.save["run"]["status"] == "active":
                sys.exit("A seed is revealed only after its run closes.")
            seed, replay_of, rs = old.seed, a.replay, old.save["ruleset"]
        seed = seed if seed is not None else secrets.randbits(48)
        r = Run.new(next_id(), rs, seed, a.cash, replay_of)
        open(ACTIVE, "w").write(str(r.save["run"]["id"]))
        print(f"Run {r.save['run']['id']} started · ruleset {rs['ruleset_id']} · starting cash "
              f"{display.money(a.cash)} · SimQ start {r.save['run']['start_price']:.2f}"
              + (f" · REPLAY of Run {replay_of}" if replay_of else "") + " · seed hidden")
        out(display.package(r, 1, "mon"))
        print("\nWAITING for your Week 1 Monday orders (or `pass`).")
        return

    if a.cmd == "compare":
        print("\n".join(report.compare([Run.load(int(x)) for x in a.args])))
        return
    r = active()
    try:
        if a.cmd == "show":
            out(display.package(r, r.week, r.phase, a.all))
        elif a.cmd == "status":
            b = r.book()
            print(f"Run {r.save['run']['id']} · {r.path.label(r.week, r.phase)} · status {r.save['run']['status']} · "
                  f"cash {display.money(b.cash)} · shares {b.shares()}")
        elif a.cmd == "sell":
            side, K = a.args[0].upper(), float(a.args[1])
            n = int(a.args[2]) if len(a.args) > 2 else 1
            e = r.sell(side, K, n, a.lot)
            r.write()
            print(f"SOLD {e['cid']} ×{n} at {e['price']:.2f} = {display.money(e['price'] * 100 * n)}"
                  + (f" (covers Lot {e['lot']})" if side == "C" else
                     f" · collateral {display.money(K * 100 * n)}"))
        elif a.cmd == "btc":
            n = int(a.args[1]) if len(a.args) > 1 else None
            e = r.btc(a.args[0], n)
            r.write()
            print(f"BOUGHT TO CLOSE {e['cid']} ×{e['n']} at {e['price']:.2f} = {display.money(e['price'] * 100 * e['n'])}")
        elif a.cmd == "buy":
            e = r.buy_shares(int(a.args[0]))
            r.write()
            print(f"BOUGHT {e['n']} sh at {e['price']:.2f} = {display.money(e['price'] * e['n'])} → Lot {e['lot']}")
        elif a.cmd == "sellsh":
            n = int(a.args[1]) if len(a.args) > 1 else None
            e = r.sell_shares(int(a.args[0]), n)
            r.write()
            print(f"SOLD {e['n']} sh of Lot {e['lot']} at {e['price']:.2f} = {display.money(e['price'] * e['n'])}")
        elif a.cmd == "relot":
            r.relot(a.args[0], int(a.args[1]))
            r.write()
            print(f"Call {a.args[0]} now covered by Lot {a.args[1]}")
        elif a.cmd in ("pass", "hold"):
            r.pass_()
            r.write()
            print(f"{a.cmd.upper()} recorded for {r.path.label(r.week, r.phase)}.")
        elif a.cmd == "undo":
            e = r.undo()
            r.write()
            print(f"UNDONE: {e['type']} " + json.dumps({k: v for k, v in e.items() if k not in ('week', 'phase')}))
        elif a.cmd == "note":
            r.note(" ".join(a.args))
            r.write()
            print("Note added.")
        elif a.cmd == "go":
            shown = r.go()
            parts = [display.package(r, w, p) for w, p in shown]
            print(("\n" + display.BREAK + "\n").join("\n".join(x) for x in parts))
            for w, p in shown:
                if p == "fri" and w in (26, 52):
                    print(f"CHECKPOINT Week {w}: mentor one-pager → {report.one_pager(r, f'week-{w}-checkpoint')}")
            nxt = {"mon": "Monday orders (or `pass`)", "wed": "Wednesday orders (or `hold`)",
                   "fri": "Friday share orders (or `hold`)"}[r.phase]
            print(f"\nWAITING for your {nxt}.")
            if any(p == "fri" for w, p in shown):
                print(f"PUSH DUE: Friday close of Week {max(w for w, p in shown if p == 'fri')}")
        elif a.cmd in ("close", "abandon"):
            note = " ".join(a.args)
            r.close_run("closed" if a.cmd == "close" else "abandoned", note)
            print(f"Run {r.save['run']['id']} {r.save['run']['status']}. Seed revealed: {r.seed}")
            print(f"Run-close one-pager → {report.one_pager(r, 'run-close')}")
            print(f"Week-by-week workbook → {report.workbook(r)}")
        elif a.cmd == "report":
            print(f"One-pager → {report.one_pager(r, a.args[0] if a.args else f'week-{report.completed_weeks(r)}')}")
        elif a.cmd == "compare":
            runs = [Run.load(int(x)) for x in a.args]
            print("\n".join(report.compare(runs)))
        else:
            sys.exit(f"Unknown command {a.cmd}")
    except ActionError as ex:
        print(f"NOT DONE: {ex}")


if __name__ == "__main__":
    main(sys.argv[1:])
