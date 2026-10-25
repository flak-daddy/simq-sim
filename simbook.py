#!/usr/bin/env python3
"""simbook.py: bookkeeping + turn driver for the SimQ simulator (uses simq.py).

All state is an append-only event log in run-NNN-state.json. Cash, positions, interest,
scorecard, ledger and journal are derived by replaying that log, so nothing is retyped.

Commands (run from the folder holding simq.py, simbook.py and the state file):
  new --run N --seed S [--headlines v2]   create a fresh run (seed from `simq.py newseed`);
                            default headlines v3 = scripted, printed by `open` (opinion can mislead, data never does)
  open                      show the current week's Monday-open package (account + chain)
  mid                       advance to midweek: Mon-Wed path, buy-to-close prices, new chain
  fri                       advance to Friday: settle, post interest, advance to next week
  sell P|C STRIKE           sell to open 1 contract at the current bid
  btc ID                    buy to close trade ID at the current ask
  pass                      record a pass (or a hold if a position is open)
  note "text"               attach the user's comment to the latest move
  quote P|C STRIKE          bid/ask for one strike at the current phase
  chain [--half] [--n 15] [--all]   re-show the current chain (open/mid/chain also list every
                            lower put strike below the trimmed chain, down to the chain bottom)
  status                    one-line account summary
  weekpnl W                 week W P&L breakdown (also printed automatically at Friday close)
  render                    rewrite run-NNN-ledger.md and run-NNN-journal.md
  hints [W]                 Claude only: hidden regime + this week's 4-headline plan (spoils the game)
Options: --state PATH (default: highest run-*-state.json next to this script)
"""
import sys, os, json, glob, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simq
import headlines

DAY = {"open": 0, "mid": 3, "fri": 5}
PH = {"open": "Monday open", "mid": "Wednesday close", "fri": "Friday close"}
SHORT = {"open": "open", "mid": "mid", "fri": "fri"}


# ---------------------------------------------------------------- state io
def default_state_path():
    d = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(d, "run-*-state.json")))
    return files[-1] if files else os.path.join(d, "run-001-state.json")


def new_state(run, seed):
    return {"run": run, "seed": seed, "start_cash": 7500.0, "apy": 0.04,
            "pricing": "v3", "headlines": "v3", "week": 1, "phase": "open", "events": []}


def load(path):
    with open(path) as f:
        return json.load(f)


def save(st, path):
    with open(path, "w") as f:
        json.dump(st, f, indent=1)


def money(x, sign=False):
    s = f"{abs(x):,.2f}"
    if sign:
        return ("+" if x >= 0 else "-") + "$" + s
    return ("-" if x < 0 else "") + "$" + s


# ---------------------------------------------------------------- engine access
def wk(st, w):
    simq.BASE_SEED = st["seed"]
    simq.RESEED = {int(a): int(c) for a, c in st.get("reseed", {}).items()}
    simq.PRICING_V2_FROM = st.get("pricing_v2_from", 1)
    simq.PRICING = st.get("pricing", "v2")  # states written before Oct 24, 2026 (Runs 1-2) use v1/v2
    simq.SKEW_V2 = w >= simq.PRICING_V2_FROM
    return simq.gen_week(w)  # regime, s_open, closes, ivs


def view(st, w, ph):
    simq.SPREAD_V2 = w >= st.get("spread_v2_from", 1)
    reg, s_open, closes, ivs = wk(st, w)
    if ph == "open":
        return s_open, 5, ivs[0]
    if ph == "mid":
        return closes[2], 2, ivs[3]
    return closes[4], 0, ivs[5]


def rows_at(st, w, ph):
    S, td, iv = view(st, w, ph)
    return S, simq.chain_rows(S, td, iv)


def quote_k(st, w, ph, kind, k):
    S, td, iv = view(st, w, ph)
    return simq.quote(S, k, td / 252, iv, kind)


# ---------------------------------------------------------------- replay
def replay(st, upto_week=None, upto_index=None):
    cash = st["start_cash"]
    trades, lots, closed_lots = {}, {}, []
    nid = nlot = 0
    interest = 0.0
    evs = st["events"] if upto_index is None else st["events"][:upto_index]
    for e in evs:
        if upto_week is not None and e["w"] > upto_week:
            break
        t = e["t"]
        if t == "sell":
            nid += 1
            tr = dict(id=nid, w=e["w"], ph=e["ph"], kind=e["kind"], k=e["k"], fill=e["fill"],
                      ask=e["ask"], spot=e["spot"], status="open", close=None, lot=None,
                      end_w=None, end_spot=None)
            if tr["kind"] == "C" and e.get("lot") in lots:
                tr["lot"] = e["lot"]
                lots[e["lot"]]["credit"] += e["fill"] * 100
            elif tr["kind"] == "C":
                for lid, lot in lots.items():
                    if not any(x["lot"] == lid and x["status"] == "open" for x in trades.values()
                               if x["kind"] == "C"):
                        tr["lot"] = lid
                        lot["credit"] += e["fill"] * 100
                        break
            trades[nid] = tr
            cash += e["fill"] * 100
        elif t == "btc":
            tr = trades[e["id"]]
            tr["status"], tr["close"], tr["end_w"], tr["end_ph"] = "btc", e["price"], e["w"], e["ph"]
            cash -= e["price"] * 100
            if tr["kind"] == "C" and tr["lot"] in lots:
                lots[tr["lot"]]["credit"] -= e["price"] * 100
        elif t == "relot":
            # move an open covered call onto a different share lot (user's choice of cover)
            tr = trades[e["id"]]
            if tr["lot"] in lots:
                lots[tr["lot"]]["credit"] -= tr["fill"] * 100
            tr["lot"] = e["lot"]
            lots[e["lot"]]["credit"] += tr["fill"] * 100
        elif t == "expire":
            tr = trades[e["id"]]
            tr["status"], tr["end_w"], tr["end_spot"] = "expired", e["w"], e["spot"]
        elif t == "assign":
            tr = trades[e["id"]]
            tr["status"], tr["end_w"], tr["end_spot"] = "assigned", e["w"], e["spot"]
            cash -= e["k"] * 100
            nlot += 1
            lots[nlot] = dict(id=nlot, w=e["w"], cost=e["k"], credit=tr["fill"] * 100, put=tr["id"])
        elif t == "called":
            tr = trades[e["id"]]
            tr["status"], tr["end_w"], tr["end_spot"] = "called", e["w"], e["spot"]
            cash += e["k"] * 100
            lot = lots.pop(tr["lot"])
            lot.update(sold=e["k"], sold_w=e["w"])
            closed_lots.append(lot)
        elif t == "interest":
            cash += e["amount"]
            interest += e["amount"]
        cash = round(cash, 10)
    open_tr = [x for x in trades.values() if x["status"] == "open"]
    locked = sum(x["k"] * 100 for x in open_tr if x["kind"] == "P")
    return dict(cash=round(cash, 2), trades=trades, lots=lots, closed_lots=closed_lots,
                open=open_tr, locked=locked, free=round(cash - locked, 2),
                shares=100 * len(lots), interest=round(interest, 2))


def basis(lot):
    return lot["cost"] - lot["credit"] / 100.0


def week_interest(st, w):
    base = replay(st, upto_week=w - 1)["cash"]
    deltas = []
    for e in st["events"]:
        if e["w"] != w:
            continue
        t, d = e["t"], DAY.get(e.get("ph", "open"), 0)
        if t == "sell":
            deltas.append((d, e["fill"] * 100))
        elif t == "btc":
            deltas.append((d, -e["price"] * 100))
        elif t == "assign":
            deltas.append((5, -e["k"] * 100))
        elif t == "called":
            deltas.append((5, e["k"] * 100))
    deltas.sort(key=lambda x: x[0])
    segs, cash, day = [], base, 0
    for d, delta in deltas:
        if d > day:
            segs.append((round(cash, 2), d - day))
            day = d
        cash += delta
    segs.append((round(cash, 2), 7 - day))
    amt = sum(c * st["apy"] / 365 * n for c, n in segs)
    return round(amt, 2), segs


def account_value(st, r, w, ph):
    S, td, iv = view(st, w, ph)
    liab = 0.0
    if ph != "fri":
        for tr in r["open"]:
            liab += simq.quote(S, tr["k"], td / 252, iv, tr["kind"])[1] * 100
    return round(r["cash"] + r["shares"] * S - liab, 2)


def scorecard(st, r):
    tr = list(r["trades"].values())
    n = len(tr)
    exp = [x for x in tr if x["status"] == "expired"]
    btc = [x for x in tr if x["status"] == "btc"]
    btc_win = [x for x in btc if x["fill"] * 100 - x["close"] * 100 > 0]
    btc_loss = [x for x in btc if x["fill"] * 100 - x["close"] * 100 <= 0]
    asg = [x for x in tr if x["status"] == "assigned"]
    cld = [x for x in tr if x["status"] == "called"]
    puts = [x for x in tr if x["kind"] == "P"]
    calls = [x for x in tr if x["kind"] == "C"]
    prem = sum(x["fill"] for x in tr) * 100
    cost = sum(x["close"] for x in btc) * 100
    pp = [x["fill"] / x["k"] * 100 for x in puts]
    cp = [x["fill"] / x["spot"] * 100 for x in calls]
    stock = sum((l["sold"] - l["cost"]) * 100 for l in r["closed_lots"])
    done = [x for x in tr if x["status"] != "open"]
    opt_net = sum(x["fill"] * 100 for x in done) - cost
    return dict(n=n, exp=len(exp), btc_win=len(btc_win), btc_loss=len(btc_loss), asg=len(asg),
                cld=len(cld), prem=prem, cost=cost, put_avg=(sum(pp) / len(pp) if pp else None),
                call_avg=(sum(cp) / len(cp) if cp else None), stock=stock, opt_net=opt_net,
                realized=opt_net + stock)


def score_line(sc):
    if not sc["n"]:
        return "no trades yet"
    wr1 = sc["exp"] / sc["n"] * 100
    wr2 = (sc["exp"] + sc["btc_win"]) / sc["n"] * 100
    return (f"{sc['n']} trades: {sc['exp']} expired worthless, {sc['btc_win']} closed for profit, "
            f"{sc['btc_loss']} closed at a loss, {sc['asg']} assigned, {sc['cld']} called away | "
            f"win rate {wr1:.0f}% ({wr2:.0f}% counting profitable closes)")


# ---------------------------------------------------------------- display helpers
def fq(b):
    return "no bid" if b <= 0 else f"{b:.2f}"


def print_chain(rows, S, always=(), n=15, half=False, all_=False, marks=None):
    marks = marks or {}
    disp = [r for r in rows if all_ or half or abs(r[0] - round(r[0])) < 1e-9 or r[0] in always]
    if not all_:
        idx = min(range(len(disp)), key=lambda i: abs(disp[i][0] - S))
        lo = max(0, idx - n // 2)
        hi = min(len(disp), lo + n)
        lo = max(0, hi - n)
        keep = set(range(lo, hi))
        for i, r in enumerate(disp):
            if r[0] in always:
                keep.add(i)
        gaps = {disp[i][0] for j, i in enumerate(sorted(keep)) if j and i - sorted(keep)[j - 1] > 1}
        disp = [disp[i] for i in sorted(keep)]
    else:
        gaps = set()
    print("| Call bid / ask | Strike | Put bid / ask |")
    print("|---|:---:|---|")
    marked = False
    for K, pb, pa, cb, ca in disp:
        if not marked and K >= S:
            # spot marker row: calls above it are out of the money, puts below it are out of the money
            print(f"| ITM calls ▲ | **\\* SimQ {S:.2f} \\*** | ▼ ITM puts |")
            marked = True
        if K in gaps:
            print("| ⋮ | ⋮ | ⋮ |")
        tag = " ◆" if K in marks else ""
        print(f"| {fq(cb)} / {ca:.2f} | **{K:g}**{tag} | {fq(pb)} / {pa:.2f} |")
    if not marked:
        print(f"| ITM calls ▲ | **\\* SimQ {S:.2f} \\*** | ▼ ITM puts |")
    return disp


def print_lower_puts(rows, S, below):
    # Standard output: every listed put strike (incl. .5 and $2.50 steps) below the
    # trimmed chain, highest first, down to the bottom of the chain (no-bid strikes included).
    low = sorted((r for r in rows if r[0] < below), key=lambda r: -r[0])
    if not low:
        return
    print("")
    print("Lower puts")
    print("| Strike | Put bid / ask | % below spot |")
    print("|:---:|---|---|")
    for K, pb, pa, cb, ca in low:
        print(f"| **{K:g}** | {fq(pb)} / {pa:.2f} | {(1 - K / S) * 100:.1f}% |")


def contract(tr):
    return f"{tr['kind']}{tr['k']:g}"


def free_calls(r):
    return sum(1 for lid in r["lots"]
               if not any(x["lot"] == lid and x["status"] == "open" for x in r["trades"].values()))


def acct_line(st, r, w, ph):
    S = view(st, w, ph)[0]
    v = account_value(st, r, w, ph)
    pct = (v / st["start_cash"] - 1) * 100
    parts = [f"Cash {money(r['cash'])}"]
    if r["locked"]:
        parts.append(f"free {money(r['free'])}")
    if r["lots"]:
        b = ", ".join(f"basis ${basis(l):.2f}" for l in r["lots"].values())
        parts.append(f"{r['shares']} shares ({b})")
    else:
        parts.append("0 shares")
    parts.append(f"Account {money(v)} ({pct:+.2f}%)")
    return " | ".join(parts)


def positions_text(st, r, w, ph):
    out = []
    for tr in r["open"]:
        b, a = quote_k(st, w, ph, tr["kind"], tr["k"])
        pl = tr["fill"] * 100 - a * 100
        out.append(f"#{tr['id']} short {contract(tr)} (sold {tr['fill']:.2f}): bid {fq(b)} / ask {a:.2f} "
                   f"-> buy to close {money(a * 100)} (P/L {money(pl, True)})")
    return out


# ---------------------------------------------------------------- commands
def need_move(st):
    return any(e["w"] == st["week"] and e["ph"] == st["phase"] and e["t"] in ("sell", "btc", "pass")
               for e in st["events"])


def cmd_status(st):
    r = replay(st)
    w, ph = st["week"], st["phase"]
    print(f"Week {w} {PH[ph]} | SimQ ${view(st, w, ph)[0]:.2f} | {acct_line(st, r, w, ph)}")
    for line in positions_text(st, r, w, ph):
        print(line)


def show_chain(st, w, ph, r, **kw):
    S, rows = rows_at(st, w, ph)
    # held share lots: mark the strike each was assigned at (its purchase price) so calls can be
    # kept at or above cost; the row is always shown, even when it sits outside the trimmed window
    marks = {}
    for l in sorted(r["lots"].values(), key=lambda x: x["id"]):
        marks.setdefault(l["cost"], []).append(l)
    listed = {x[0] for x in rows}
    always = tuple(tr["k"] for tr in r["open"]) + tuple(k for k in marks if k in listed)
    disp = print_chain(rows, S, always=always, marks=marks, **kw)
    if marks:
        parts = []
        for k, ls in sorted(marks.items()):
            for l in ls:
                where = "" if k in listed else ", above the listed chain"
                parts.append(f"lot {l['id']} assigned at ${k:g} (basis ${basis(l):.2f}{where})")
        print(f"◆ = held lot's assigned strike: " + "; ".join(parts))
    if not kw.get("all_"):
        print_lower_puts(rows, S, min(x[0] for x in disp if x[0] not in always or x[0] >= S))


def cmd_open(st, **kw):
    w, ph = st["week"], st["phase"]
    if ph != "open":
        sys.exit(f"Current phase is {PH[ph]}, not Monday open.")
    r = replay(st)
    S = view(st, w, "open")[0]
    print(f"SimQ Week {w}, Monday open | spot ${S:.2f} | 5 trading days to Friday close")
    if st.get("headlines") == "v3":
        headlines.print_monday(st["seed"], w, wk(st, w)[0])
    print(acct_line(st, r, w, "open"))
    show_chain(st, w, "open", r, **kw)


def cmd_mid(st, **kw):
    w = st["week"]
    if st["phase"] == "open":
        if not need_move(st):
            st["events"].append({"w": w, "ph": "open", "t": "pass"})
        st["phase"] = "mid"
    elif st["phase"] == "fri":
        sys.exit("Already past midweek.")
    reg, s_open, closes, ivs = wk(st, w)
    r = replay(st)
    print(f"SimQ Week {w}: Mon {closes[0]:.2f} | Tue {closes[1]:.2f} | Wed {closes[2]:.2f} "
          f"(spot ${closes[2]:.2f}, {(closes[2] / s_open - 1) * 100:+.1f}% vs Monday open) | 2 days to Friday")
    for line in positions_text(st, r, w, "mid"):
        print(line)
    print(f"Cash {money(r['cash'])}" + (f" | free {money(r['free'])}" if r["locked"] else "")
          + f" | shares {r['shares']}")
    show_chain(st, w, "mid", r, **kw)


def week_pnl(st, w):
    """Friday breakdown of the week's account change: each option trade opened this week
    (premium in, buy-back out), interest, and share/stock moves (assignment marked to the
    Friday close, mark-to-market on held shares, call-away proceeds). Rows sum to the change."""
    prev = replay(st, upto_week=w - 1)
    prev_spot = wk(st, w - 1)[2][4] if w > 1 else simq.S_START
    v_prev = prev["cash"] + prev["shares"] * prev_spot
    cur = replay(st, upto_week=w)
    spot = wk(st, w)[2][4]
    v_now = cur["cash"] + cur["shares"] * spot
    rows, opt = [], 0.0
    for tr in sorted(cur["trades"].values(), key=lambda x: x["id"]):
        if tr["w"] != w:
            continue
        prem = tr["fill"] * 100
        cost = (tr["close"] or 0) * 100 if tr["status"] == "btc" else 0.0
        net = prem - cost
        opt += net
        if tr["status"] == "btc":
            how = f"sold {tr['fill']:.2f}, bought back {tr['close']:.2f}"
        else:
            how = f"sold {tr['fill']:.2f}, " + {"expired": "expired", "assigned": "assigned",
                                                  "called": "called away"}.get(tr["status"], "open")
        rows.append((f"#{tr['id']} {contract(tr)} ({SHORT[tr['ph']]})", how, net))
    interest = sum(e["amount"] for e in st["events"] if e["t"] == "interest" and e["w"] == w)
    stock = round(v_now - v_prev - opt - interest, 2)
    return rows, opt, interest, stock, v_prev, v_now


def print_week_pnl(st, w):
    rows, opt, interest, stock, v_prev, v_now = week_pnl(st, w)
    print("")
    print(f"Week {w} P&L")
    print("| Item | Detail | Amount |")
    print("|---|---|---|")
    for name, how, net in rows:
        print(f"| {name} | {how} | {money(net, True)} |")
    if not rows:
        print("| Options | no trades this week | $0.00 |")
    print(f"| Options subtotal | | {money(opt, True)} |")
    print(f"| Interest | | {money(interest, True)} |")
    if abs(stock) >= 0.005:
        print(f"| Shares | assignment, mark-to-market or called-away sale | {money(stock, True)} |")
    print(f"| **Week total** | {money(v_prev)} -> {money(v_now)} | **{money(v_now - v_prev, True)}** "
          f"({(v_now / v_prev - 1) * 100:+.2f}%) |")


def cmd_fri(st):
    w = st["week"]
    if st["phase"] == "open":
        if not need_move(st):
            st["events"].append({"w": w, "ph": "open", "t": "pass"})
        st["phase"] = "mid"
    if st["phase"] == "mid":
        if not need_move(st):
            st["events"].append({"w": w, "ph": "mid", "t": "pass"})
        st["phase"] = "fri"
    reg, s_open, closes, ivs = wk(st, w)
    spot = closes[4]
    r = replay(st)
    lines = []
    for tr in r["open"]:
        itm = spot < tr["k"] if tr["kind"] == "P" else spot > tr["k"]
        if itm and tr["kind"] == "P":
            st["events"].append({"w": w, "ph": "fri", "t": "assign", "id": tr["id"], "k": tr["k"], "spot": spot})
            lines.append(f"#{tr['id']} {contract(tr)} ASSIGNED: bought 100 shares at ${tr['k']:.2f} "
                         f"(SimQ ${spot:.2f}, ${tr['k'] - spot:.2f} below strike); premium kept {money(tr['fill'] * 100)}")
        elif itm:
            st["events"].append({"w": w, "ph": "fri", "t": "called", "id": tr["id"], "k": tr["k"], "spot": spot})
            lines.append(f"#{tr['id']} {contract(tr)} CALLED AWAY: sold 100 shares at ${tr['k']:.2f} "
                         f"(SimQ ${spot:.2f}, ${spot - tr['k']:.2f} above strike); premium kept {money(tr['fill'] * 100)}")
        else:
            st["events"].append({"w": w, "ph": "fri", "t": "expire", "id": tr["id"], "k": tr["k"], "spot": spot})
            gap = abs(spot - tr["k"])
            lines.append(f"#{tr['id']} {contract(tr)} expired worthless, +{money(tr['fill'] * 100)} "
                         f"(SimQ ${spot:.2f}, ${gap:.2f} {'above' if tr['kind'] == 'P' else 'below'} strike)")
    amt, segs = week_interest(st, w)
    st["events"].append({"w": w, "ph": "fri", "t": "interest", "amount": amt,
                         "segs": [[c, n] for c, n in segs]})
    st["week"], st["phase"] = w + 1, "open"
    r2 = replay(st)
    v = r2["cash"] + 0.0 + r2["shares"] * spot
    pct = (v / st["start_cash"] - 1) * 100
    print(f"SimQ Week {w} Friday: Thu {closes[3]:.2f} | Fri {spot:.2f} "
          f"(week {(spot / s_open - 1) * 100:+.1f}%, from {s_open:.2f})")
    for line in lines or ["No position open at Friday close."]:
        print(line)
    print(f"Regime: {reg}")
    print(f"Interest +{money(amt)} | Cash {money(r2['cash'])} | shares {r2['shares']} "
          f"| Account {money(v)} ({pct:+.2f}%)")
    print(score_line(scorecard(st, r2)))
    print_week_pnl(st, w)
    print(f"Next: Week {w + 1} Monday open")


def lot_is_free(r, lid):
    return lid in r["lots"] and not any(x["lot"] == lid and x["status"] == "open" and x["kind"] == "C"
                                        for x in r["trades"].values())


def cmd_relot(st, tid, lid):
    w, ph = st["week"], st["phase"]
    if ph == "fri":
        sys.exit("Friday is settlement; no changes.")
    r = replay(st)
    tr = r["trades"].get(tid)
    if not tr or tr["status"] != "open" or tr["kind"] != "C":
        sys.exit(f"#{tid} is not an open covered call.")
    if tr["lot"] == lid:
        sys.exit(f"#{tid} is already covered by lot {lid}.")
    if not lot_is_free(r, lid):
        sys.exit(f"Lot {lid} is not held or already covers an open call.")
    st["events"].append({"w": w, "ph": ph, "t": "relot", "id": tid, "lot": lid})
    r = replay(st)
    b = ", ".join(f"lot {l['id']} basis ${basis(l):.2f}" for l in r["lots"].values())
    print(f"#{tid} {contract(tr)} now covered by lot {lid} (was lot {tr['lot']}); {b}")


def cmd_sell(st, kind, k, lot=None):
    kind = kind.upper()
    w, ph = st["week"], st["phase"]
    if ph == "fri":
        sys.exit("Friday is settlement; no trading.")
    S, rows = rows_at(st, w, ph)
    row = next((x for x in rows if abs(x[0] - k) < 1e-9), None)
    if not row:
        sys.exit(f"Strike {k:g} is not on the chain.")
    bid, ask = (row[1], row[2]) if kind == "P" else (row[3], row[4])
    if bid <= 0:
        sys.exit(f"{kind}{k:g} has no bid; it cannot be sold.")
    r = replay(st)
    if kind == "P" and r["free"] < k * 100:
        sys.exit(f"Not enough free cash for a ${k:g} put: needs ${k * 100:,.0f}, free {money(r['free'])}. "
                 f"(Collateral is strike x 100; shares do not collateralize a put.)")
    if kind == "C" and free_calls(r) < 1:
        sys.exit("No uncovered shares: a call must be covered by 100 shares you hold (no naked calls).")
    ev = {"w": w, "ph": ph, "t": "sell", "kind": kind, "k": k, "fill": bid, "ask": ask, "spot": S}
    if kind == "C" and lot is not None:
        if not lot_is_free(r, lot):
            sys.exit(f"Lot {lot} is not held or already covers an open call.")
        ev["lot"] = lot
    st["events"].append(ev)
    r = replay(st)
    tr = max(r["trades"].values(), key=lambda x: x["id"])
    extra = f"collateral {money(k * 100)}, free cash {money(r['free'])}" if kind == "P" else \
        f"covered by {tr['lot'] and 'lot ' + str(tr['lot'])}"
    print(f"Sold #{tr['id']} {contract(tr)} at the bid {bid:.2f} (ask {ask:.2f}) for +{money(bid * 100)}; {extra}")


def cmd_btc(st, tid):
    w, ph = st["week"], st["phase"]
    if ph == "fri":
        sys.exit("Friday is settlement; no trading.")
    r = replay(st)
    tr = r["trades"].get(tid)
    if not tr or tr["status"] != "open":
        sys.exit(f"#{tid} is not an open position.")
    b, a = quote_k(st, w, ph, tr["kind"], tr["k"])
    st["events"].append({"w": w, "ph": ph, "t": "btc", "id": tid, "price": a})
    print(f"Bought to close #{tid} {contract(tr)} at the ask {a:.2f} for {money(a * 100)}; "
          f"net {money(tr['fill'] * 100 - a * 100, True)} on the trade")


def cmd_pass(st):
    st["events"].append({"w": st["week"], "ph": st["phase"], "t": "pass"})
    print("Recorded: pass")


def add_note(st, text, w=None, ph=None):
    st["events"].append({"w": w or st["week"], "ph": ph or st["phase"], "t": "note", "text": text})


def cmd_quote(st, kind, k):
    w, ph = st["week"], st["phase"]
    S, rows = rows_at(st, w, ph)
    row = next((x for x in rows if abs(x[0] - k) < 1e-9), None)
    if not row:
        sys.exit(f"Strike {k:g} is not on the chain.")
    b, a = (row[1], row[2]) if kind.upper() == "P" else (row[3], row[4])
    print(f"SIMQ-W{w:02d}-{kind.upper()}{k:g}: bid {fq(b)} / ask {a:.2f} (spot ${S:.2f})")


# ---------------------------------------------------------------- rendering
def render_journal(st):
    out = [f"# SimQ Decision Journal, Run {st['run']}", "",
           "One line per move, appended as the run goes. Your own comments are added only when you make one.", ""]
    lines = []
    for i, e in enumerate(st["events"]):
        t, w, ph = e["t"], e["w"], e.get("ph", "open")
        tag = f"W{w} {SHORT[ph]}"
        if t == "sell":
            what = f"sold {e['kind']}{e['k']:g} at {e['fill']:.2f} (SimQ {e['spot']:.2f})"
        elif t == "btc":
            r = replay(st, upto_index=i)
            tr = r["trades"][e["id"]]
            pl = tr["fill"] * 100 - e["price"] * 100
            what = f"bought to close {contract(tr)} at {e['price']:.2f} ({money(pl, True)})"
        elif t == "pass":
            r = replay(st, upto_index=i)
            held = [contract(x) for x in r["open"]]
            what = f"held {', '.join(held)}" if held else "passed"
        elif t in ("expire", "assign", "called"):
            r = replay(st, upto_index=i)
            tr = r["trades"][e["id"]]
            res = {"expire": f"{contract(tr)} expired worthless (+{money(tr['fill'] * 100)})",
                   "assign": f"{contract(tr)} assigned, bought 100 at ${e['k']:.2f}",
                   "called": f"{contract(tr)} called away, sold 100 at ${e['k']:.2f}"}[t]
            tag, what = f"W{w} fri", f"{res}; SimQ {e['spot']:.2f}"
        elif t == "relot":
            r = replay(st, upto_index=i)
            what = f"moved {contract(r['trades'][e['id']])} cover to lot {e['lot']}"
        elif t == "note":
            if lines:
                lines[-1] += f' — your read: "{e["text"]}"'
            continue
        else:
            continue
        lines.append(f"- **{tag}**: {what}")
    return "\n".join(out + lines) + "\n"


def render_ledger(st):
    r = replay(st)
    w, ph = st["week"], st["phase"]
    sc = scorecard(st, r)
    S = view(st, w, ph)[0]
    v = account_value(st, r, w, ph)
    pct = (v / st["start_cash"] - 1) * 100
    L = [f"# SimQ Run {st['run']} Ledger", "",
         f"- Seed: {st['seed']}" + (f" (path reseeded from Week {min(int(a) for a in st['reseed'])}; see state file)" if st.get("reseed") else "") + f" | Start: ${st['start_cash']:,.0f}, {st['apy'] * 100:.2f}% APY | Rules: claude/csp-ledger-branch-cc.md",
         f"- Status: {st.get('status_note', st.get('status', 'in progress'))} | Comparison window: 26 sim weeks | Journal: claude/run-{st['run']:03d}-journal.md", "",
         f"## Current state (Week {w}, {PH[ph]})",
         f"- SimQ spot: ${S:.2f}",
         f"- Cash: {money(r['cash'])} | locked collateral: {money(r['locked'])} | free: {money(r['free'])}"]
    if r["lots"]:
        for l in r["lots"].values():
            L.append(f"- Shares: 100 SimQ bought at ${l['cost']:.2f} in Week {l['w']}; effective basis ${basis(l):.2f} "
                     f"after option premiums")
    else:
        L.append("- Shares: 0")
    if r["open"]:
        for tr in r["open"]:
            L.append(f"- Open: #{tr['id']} short {contract(tr)} sold at {tr['fill']:.2f} in Week {tr['w']}")
    else:
        L.append("- Open positions: none")
    L += [f"- Premium collected (gross): {money(sc['prem'])} | buy-to-close costs: {money(sc['cost'])} | "
          f"interest: {money(r['interest'])}",
          f"- Realized P&L (options net of buy-backs + stock sales): {money(sc['realized'], True)} "
          f"(options {money(sc['opt_net'], True)}, stock {money(sc['stock'], True)})",
          f"- Account value: {money(v)} ({pct:+.2f}% vs start)", "",
          "## Trade log",
          "| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |",
          "|---|---|---|---|---|---|---|---|---|"]
    for tr in sorted(r["trades"].values(), key=lambda x: x["id"]):
        k = tr["k"]
        coll = money(k * 100) + " cash" if tr["kind"] == "P" else (f"lot {tr['lot']}" if tr["lot"] else "-")
        if tr["status"] == "open":
            res = "OPEN"
        elif tr["status"] == "expired":
            res = f"Expired worthless (Fri SimQ {tr['end_spot']:.2f})"
        elif tr["status"] == "assigned":
            res = f"ASSIGNED: bought 100 at ${k:.2f} (Fri SimQ {tr['end_spot']:.2f})"
        elif tr["status"] == "called":
            res = f"CALLED AWAY: sold 100 at ${k:.2f} (Fri SimQ {tr['end_spot']:.2f})"
        else:
            net = tr["fill"] * 100 - tr["close"] * 100
            res = f"Bought to close at {tr['close']:.2f} ({money(tr['close'] * 100)}), net {money(net, True)}"
        notes = []
        pct_prem = tr["fill"] / (k if tr["kind"] == "P" else tr["spot"]) * 100
        notes.append(f"premium {pct_prem:.2f}% of {'collateral' if tr['kind'] == 'P' else 'share value'}")
        if tr["ph"] == "open" and tr["status"] in ("expired", "assigned", "called"):
            b, a = quote_k(st, tr["w"], "mid", tr["kind"], k)
            notes.append(f"held at midweek (ask {a:.2f})")
        L.append(f"| {tr['id']} | SIMQ-W{tr['w']:02d}-{contract(tr)} | W{tr['w']} {SHORT[tr['ph']]} | ${k:g} | "
                 f"{tr['fill']:.2f} / {tr['ask']:.2f} | {money(tr['fill'] * 100)} | {coll} | {res} | {'; '.join(notes)} |")
    if r["closed_lots"]:
        L += ["", "## Closed share lots", "| Bought | Sold | Stock P&L | Net after option premiums |", "|---|---|---|---|"]
        for l in r["closed_lots"]:
            L.append(f"| W{l['w']} at ${l['cost']:.2f} | W{l['sold_w']} at ${l['sold']:.2f} | "
                     f"{money((l['sold'] - l['cost']) * 100, True)} | {money((l['sold'] - basis(l)) * 100, True)} |")
    L += ["", "## Weeks", "| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    ints = {e["w"]: e for e in st["events"] if e["t"] == "interest"}
    for wk_ in sorted(ints):
        reg, so, cl, _ = wk(st, wk_)
        segs = "; ".join(f"{c:,.2f} x {n}d" for c, n in ints[wk_]["segs"])
        L.append(f"| {wk_} | {reg} | {so:.2f} | " + " | ".join(f"{c:.2f}" for c in cl)
                 + f" | {(cl[4] / so - 1) * 100:+.1f}% | {ints[wk_]['amount']:.2f} ({segs}) |")
    L += ["", "## Scorecard", f"- {score_line(sc)}"]
    if sc["put_avg"] is not None:
        L.append(f"- Avg put premium: {sc['put_avg']:.2f}% of collateral")
    if sc["call_avg"] is not None:
        L.append(f"- Avg call premium: {sc['call_avg']:.2f}% of share value at sale")
    L.append(f"- Wheel cycles completed (shares called away): {sc['cld']}")
    for mark in (26, 52):
        if any(e["t"] == "interest" and e["w"] == mark for e in st["events"]):
            rm = replay(st, upto_week=mark)
            sm = wk(st, mark)[2][4]
            vm = rm["cash"] + rm["shares"] * sm
            bh = st["start_cash"] / simq.S_START * sm
            cash_only = st["start_cash"] * (1 + st["apy"] * mark * 7 / 365)
            tag = "comparison metric" if mark == 26 else "full year"
            L.append(f"- Account value at week {mark} ({tag}): {money(vm)} ({(vm / st['start_cash'] - 1) * 100:+.2f}%) | "
                     f"buy-and-hold SimQ {money(bh)} ({(sm / simq.S_START - 1) * 100:+.2f}%) | "
                     f"cash only {money(cash_only)} ({(cash_only / st['start_cash'] - 1) * 100:+.2f}%)")
        elif mark == 26:
            L.append("- Account value at week 26 (comparison metric): pending")
    return "\n".join(L) + "\n"


def render(st, path):
    d, n = os.path.dirname(os.path.abspath(path)), st["run"]
    with open(os.path.join(d, f"run-{n:03d}-ledger.md"), "w") as f:
        f.write(render_ledger(st))
    with open(os.path.join(d, f"run-{n:03d}-journal.md"), "w") as f:
        f.write(render_journal(st))


# ---------------------------------------------------------------- headline plan (v2 headlines)
# Four headlines per week. Each slot is TRUE (hints at the real regime), FALSE (hints, just as
# convincingly, at a wrong regime) or NOISE (market news with no regime direction). The mix is drawn
# from its own random stream, so it is reproducible and never changes the market path.
REG_LABEL = {"calm_up": "calm, drifting up", "chop": "range-bound / directionless",
             "selloff": "steady selling", "crash": "violent, high-stress drop",
             "rebound": "sharp recovery / relief rally"}
CONFUSE = {"calm_up": ["chop", "rebound", "selloff"], "chop": ["calm_up", "selloff", "rebound"],
           "selloff": ["crash", "chop", "rebound"], "crash": ["selloff", "rebound", "chop"],
           "rebound": ["calm_up", "crash", "selloff"]}


def headline_plan(st, w):
    import random
    reg = wk(st, w)[0]
    rng = random.Random(f"headlines-{st['seed']}-{w}")
    n_true = rng.choices([0, 1, 2], weights=[0.25, 0.50, 0.25])[0]
    n_false = rng.choices([0, 1, 2], weights=[0.30, 0.45, 0.25])[0]
    n_false = min(n_false, 3 - n_true)
    wrong = rng.choice(CONFUSE[reg])
    slots = ["TRUE"] * n_true
    for _ in range(n_false):
        slots.append("FALSE:" + (wrong if rng.random() < 0.7 else rng.choice(CONFUSE[reg])))
    slots += ["NOISE"] * (4 - len(slots))
    rng.shuffle(slots)
    return reg, slots


def cmd_hints(st, w):
    if st.get("headlines") == "v3":
        sys.exit("This run uses scripted headlines (v3): `open` prints them. "
                 "Friday shows the regime only. No hints needed.")
    reg, slots = headline_plan(st, w)
    print(f"Week {w} regime (hidden): {reg} ({REG_LABEL[reg]})")
    print("Headline plan, in display order:")
    for i, s in enumerate(slots, 1):
        if s == "TRUE":
            print(f"  {i}. TRUE  - hint at {reg} ({REG_LABEL[reg]})")
        elif s.startswith("FALSE"):
            r = s.split(":")[1]
            print(f"  {i}. FALSE - hint, just as convincingly, at {r} ({REG_LABEL[r]})")
        else:
            print(f"  {i}. NOISE - real-sounding market news with no regime direction")


# ---------------------------------------------------------------- main
def main(argv):
    path = default_state_path()
    kw = {}
    a = list(argv)
    if "--state" in a:
        i = a.index("--state")
        path = a[i + 1]
        del a[i:i + 2]
    if "--half" in a:
        a.remove("--half")
        kw["half"] = True
    if "--all" in a:
        a.remove("--all")
        kw["all_"] = True
    if "--n" in a:
        i = a.index("--n")
        kw["n"] = int(a[i + 1])
        del a[i:i + 2]
    cmd = a[0]
    if cmd == "new":
        run = int(a[a.index("--run") + 1])
        seed = int(a[a.index("--seed") + 1])
        hv = a[a.index("--headlines") + 1] if "--headlines" in a else None
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"run-{run:03d}-state.json")
        st = new_state(run, seed)
        if hv:
            st["headlines"] = hv
        save(st, path)
        render(st, path)
        print(f"Created {path}")
        return
    st = load(path)
    mutating = True
    if cmd == "open":
        cmd_open(st, **kw); mutating = False
    elif cmd == "mid":
        cmd_mid(st, **kw)
    elif cmd == "fri":
        cmd_fri(st)
    elif cmd == "sell":
        cmd_sell(st, a[1], float(a[2]), lot=int(a[a.index("--lot") + 1]) if "--lot" in a else None)
    elif cmd == "relot":
        cmd_relot(st, int(a[1]), int(a[2]))
    elif cmd == "btc":
        cmd_btc(st, int(a[1]))
    elif cmd == "pass":
        cmd_pass(st)
    elif cmd == "note":
        add_note(st, " ".join(a[1:])); print("Note recorded")
    elif cmd == "quote":
        cmd_quote(st, a[1], float(a[2])); mutating = False
    elif cmd == "chain":
        r = replay(st)
        S, _, _ = view(st, st["week"], st["phase"])
        show_chain(st, st["week"], st["phase"], r, **kw); mutating = False
    elif cmd == "status":
        cmd_status(st); mutating = False
    elif cmd == "weekpnl":
        print_week_pnl(st, int(a[1])); mutating = False
    elif cmd == "render":
        pass
    elif cmd == "hints":
        cmd_hints(st, int(a[1]) if len(a) > 1 else st["week"]); mutating = False
    else:
        sys.exit(__doc__)
    if mutating:
        save(st, path)
    render(st, path)


if __name__ == "__main__":
    main(sys.argv[1:])
