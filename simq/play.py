"""Run logic (SPEC §4, §5, §8): actions at decision points, auto-advance, settlement.

Every change is an appended event; the save file holds the run's full ruleset (Rule 0).
"""
import copy
import datetime
import hashlib
import json
import os

from simq import book as bk
from simq import chain as ch
from simq.game import Path

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs")
CONTRACT = 100


class ActionError(Exception):
    pass


def _h(*parts):
    h = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


class Run:
    def __init__(self, save, path_obj=None):
        self.save = save
        self.rs = save["ruleset"]
        self.seed = save["run"]["seed"]
        self.path = path_obj or Path(self.rs, self.seed)
        self._book = None
        self._chains = {}

    # ---- persistence ----
    @property
    def dir(self):
        return os.path.join(ROOT, f"run-{self.save['run']['id']:03d}")

    def write(self):
        os.makedirs(self.dir, exist_ok=True)
        with open(os.path.join(self.dir, "save.json"), "w") as f:
            json.dump(self.save, f, indent=1)

    @classmethod
    def load(cls, run_id):
        with open(os.path.join(ROOT, f"run-{run_id:03d}", "save.json")) as f:
            return cls(json.load(f))

    @classmethod
    def new(cls, run_id, rs, seed, start_cash, replay_of=None):
        rs = copy.deepcopy(rs)
        p = Path(rs, seed)
        save = {"run": {"id": run_id, "seed": seed, "start_cash": float(start_cash),
                        "start_price": p.start_price, "start_rate": rs["rates"]["start"],
                        "ruleset_id": rs["ruleset_id"], "status": "active", "status_note": "",
                        "created": datetime.date.today().isoformat(), "replay_of": replay_of},
                "ruleset": rs, "clock": {"week": 1, "phase": "mon"}, "events": [], "next_tid": 1, "next_lot": 1}
        r = cls(save, p)
        r.write()
        return r

    # ---- derived state ----
    @property
    def week(self):
        return self.save["clock"]["week"]

    @property
    def phase(self):
        return self.save["clock"]["phase"]

    def book(self):
        if self._book is None:
            self._book = bk.replay(self.save)
        return self._book

    def state(self, week=None, phase=None):
        return self.path.state(week or self.week, phase or self.phase)

    def chain(self, week=None, phase=None):
        key = (week or self.week, phase or self.phase)
        if key not in self._chains:
            self._chains[key] = ch.build(self.rs, self.seed, self.path.state(*key))
        return self._chains[key]

    def _add(self, e):
        e.setdefault("week", self.week)
        e.setdefault("phase", self.phase)
        self.save["events"].append(e)
        self.book().apply(e)

    def phase_events(self, week, phase, types=None):
        return [e for e in self.save["events"] if e.get("week") == week and e.get("phase") == phase
                and (types is None or e["type"] in types)]

    def share_price(self, side):
        st = self.state()
        spread = 0.01 if _h(self.seed, self.week, self.phase, side) < 0.5 else 0.02
        return round(st["spot"] + spread if side == "buy" else st["spot"] - spread, 2)

    # ---- actions ----
    def _need_active(self):
        if self.save["run"]["status"] != "active":
            raise ActionError(f"Run {self.save['run']['id']} is {self.save['run']['status']}.")

    def sell(self, side, K, n=1, lot=None):
        self._need_active()
        if self.phase == "fri":
            raise ActionError("Friday close allows share trades only; options settle automatically.")
        side = side.upper()
        row = ch.find(self.chain(), K)
        if row is None:
            raise ActionError(f"{K:g} is not a listed strike this week.")
        bid = row["pb"] if side == "P" else row["cb"]
        if bid <= 0:
            raise ActionError(f"The {K:g} {'put' if side == 'P' else 'call'} has no bid.")
        b = self.book()
        st = self.state()
        if side == "P":
            need = K * CONTRACT * n
            if need > b.free_cash() + 1e-9:
                fits = int(b.free_cash() // (K * CONTRACT))
                raise ActionError(f"Collateral ${need:,.2f} needed; free cash is ${b.free_cash():,.2f} "
                                  f"({fits} contract(s) at the {K:g} strike fit).")
        else:
            lots = [l for l in b.open_lots() if b.free_contracts(l["id"]) > 0]
            if not lots:
                raise ActionError("No held shares are free to cover a call. (Did you mean a put?)")
            if lot is None:
                lots.sort(key=lambda l: (abs(b.eff_basis(l) - K), l["week"], l["id"]))
                lot = lots[0]["id"]
            if lot not in b.lots or b.lots[lot]["shares"] == 0:
                raise ActionError(f"Lot {lot} is not held.")
            if b.free_contracts(lot) < n:
                raise ActionError(f"Lot {lot} covers {b.free_contracts(lot)} more call contract(s).")
        tid = self.save["next_tid"]
        self.save["next_tid"] += 1
        e = {"type": "sell", "tid": tid, "cid": ch.contract_id(self.week, side, K), "side": side, "K": K,
             "n": n, "price": bid, "spot": st["spot"]}
        if side == "C":
            e["lot"] = lot
        self._add(e)
        return e

    def btc(self, ref, n=None):
        self._need_active()
        if self.phase != "wed":
            raise ActionError("Buy to close is available at Wednesday close.")
        t = self._find_trade(ref)
        n = n or t["open_n"]
        if n > t["open_n"]:
            raise ActionError(f"Only {t['open_n']} contract(s) of {t['cid']} are open.")
        row = ch.find(self.chain(), t["K"])
        ask = row["pa"] if t["side"] == "P" else row["ca"]
        if ask * CONTRACT * n > self.book().cash + 1e-9:
            raise ActionError("Not enough cash to buy back.")
        e = {"type": "btc", "tid": t["tid"], "cid": t["cid"], "n": n, "price": ask}
        self._add(e)
        return e

    def _find_trade(self, ref):
        b = self.book()
        for t in b.open_trades():
            if str(t["tid"]) == str(ref) or t["cid"].upper() == str(ref).upper():
                return t
        raise ActionError(f"No open position {ref}.")

    def buy_shares(self, n):
        self._need_active()
        if n <= 0 or n % CONTRACT:
            raise ActionError("Shares trade in round lots of 100.")
        if self.phase == "fri" and not self._fri_paused():
            raise ActionError("Friday share trades are open only while shares are held.")
        px = self.share_price("buy")
        if px * n > self.book().free_cash() + 1e-9:
            raise ActionError(f"${px * n:,.2f} needed; free cash is ${self.book().free_cash():,.2f}.")
        lot = self.save["next_lot"]
        self.save["next_lot"] += 1
        e = {"type": "buy_shares", "lot": lot, "n": n, "price": px}
        self._add(e)
        return e

    def sell_shares(self, lot, n=None):
        self._need_active()
        b = self.book()
        if lot not in b.lots or b.lots[lot]["shares"] == 0:
            raise ActionError(f"Lot {lot} is not held.")
        L = b.lots[lot]
        free = L["shares"] - b.covered(lot) * CONTRACT
        n = n or free
        odd = L["shares"] % CONTRACT
        if n <= 0 or n > free:
            raise ActionError(f"Lot {lot} has {free} share(s) not covered by open calls.")
        if n % CONTRACT and n != odd and n != free:
            raise ActionError("Shares trade in round lots of 100 (odd lots after a reverse split sell whole).")
        e = {"type": "sell_shares", "lot": lot, "n": n, "price": self.share_price("sell")}
        self._add(e)
        return e

    def relot(self, ref, lot):
        self._need_active()
        t = self._find_trade(ref)
        b = self.book()
        if t["side"] != "C":
            raise ActionError("Only calls are tied to lots.")
        if lot not in b.lots or b.free_contracts(lot) < t["open_n"]:
            raise ActionError(f"Lot {lot} can't cover {t['open_n']} contract(s).")
        self._add({"type": "relot", "tid": t["tid"], "lot": lot})

    def close_run(self, status, note=""):
        self.save["run"]["status"] = status
        self.save["run"]["status_note"] = note
        self.save["run"]["closed"] = datetime.date.today().isoformat()
        self.save["run"]["closed_at"] = {"week": self.week, "phase": self.phase}
        self.write()

    # ---- clock ----
    def _fri_paused(self):
        return self.phase == "fri" and self.book().shares() > 0

    def _record_cash(self, key):
        self.save.setdefault("cash_marks", {}).setdefault(str(self.week), {})[key] = round(self.book().cash, 6)

    def _settle_friday(self):
        w = self.week
        t = self.path.day(w, 4)
        close = float(self.path.m["close"][t])
        b = self.book()
        for tr in list(b.open_trades()):
            if tr["side"] == "P":
                if close < tr["K"]:
                    lot = self.save["next_lot"]
                    self.save["next_lot"] += 1
                    self._add({"type": "assign", "tid": tr["tid"], "lot": lot, "close": round(close, 2)})
                else:
                    self._add({"type": "expire", "tid": tr["tid"], "close": round(close, 2)})
            else:
                if close > tr["K"]:
                    self._add({"type": "called", "tid": tr["tid"], "close": round(close, 2)})
                else:
                    self._add({"type": "expire", "tid": tr["tid"], "close": round(close, 2)})
        # interest: Mon-Wed on the Monday balance, Thu on the Wednesday balance, Fri-Sun after settlement
        marks = self.save.get("cash_marks", {}).get(str(w), {})
        rate = float(self.path.m["rate"][max(self.path.day(w, 0) - 1, self.path.day(1, 0))])
        bal_m = marks.get("mon", b.cash)
        bal_w = marks.get("wed", b.cash)
        amt = round((bal_m * 3 + bal_w * 1 + b.cash * 3) * rate / 365.0, 2)
        self._add({"type": "interest", "amount": amt, "rate": rate})
        mt = self.path.meeting(w)
        if mt:
            self._add({"type": "rate", "decision": mt["decision"], "rate": mt["rate"]})

    def _enter_monday(self):
        st = self.state(self.week, "mon")
        if st["split"]:
            self._add({"type": "split", "ratio": self.rs["reverse_split"]["ratio"], "new_price": st["spot"]})

    def go(self):
        """Advance to the next decision point that needs the player. Returns the list of
        (week, phase) packages passed through, in order, for display."""
        self._need_active()
        shown = []
        if self.phase == "mon":
            if not self.phase_events(self.week, "mon", {"sell", "buy_shares", "sell_shares"}):
                self._add({"type": "pass"})
            self._record_cash("mon")
            self.save["clock"]["phase"] = "wed"
            shown.append((self.week, "wed"))
        elif self.phase == "wed":
            if not self.phase_events(self.week, "wed", {"sell", "btc", "buy_shares", "sell_shares"}):
                self._add({"type": "pass"})
            self._record_cash("wed")
            self.save["clock"]["phase"] = "fri"
            self._settle_friday()
            shown.append((self.week, "fri"))
            if not self._fri_paused():
                self.save["clock"] = {"week": self.week + 1, "phase": "mon"}
                self._enter_monday()
                shown.append((self.week, "mon"))
        else:  # paused Friday -> Monday
            self.save["clock"] = {"week": self.week + 1, "phase": "mon"}
            self._enter_monday()
            shown.append((self.week, "mon"))
        self.write()
        return shown

    def week_values(self, week):
        """Account value at the previous Friday close and this Friday close."""
        def value_at(w):
            if w < 1:
                return self.save["run"]["start_cash"]
            b = bk.Book(self.save["run"]["start_cash"])
            for e in self.save["events"]:
                if e.get("week", 0) <= w:
                    b.apply(e)
            close = float(self.path.m["close"][self.path.day(w, 4)])
            return b.cash + b.shares() * close
        return value_at(week - 1), value_at(week)
