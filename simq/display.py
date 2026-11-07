"""Script output for each decision point (SPEC §3, §11). Claude relays it verbatim
(headlines are the one part Claude polishes)."""
from simq import chain as ch
from simq import headlines
from simq.indicators import fg_label

BREAK = "-----------------"
CONTRACT = 100


def money(x, sign=False):
    if abs(x) < 0.005:
        x = 0.0
    s = f"{abs(x):,.2f}"
    if sign:
        return ("+" if x >= 0 else "−") + "$" + s
    return ("−$" if x < 0 else "$") + s


def bar(v, width=20):
    n = int(round(max(0.0, min(100.0, v)) / 100 * width))
    return "█" * n + "░" * (width - n)


def osc_zone(k, rs):
    o = rs["osc"]
    return "oversold" if k < o["oversold"] else "overbought" if k > o["overbought"] else "neutral"


def indicators_block(run, ref, title):
    h = run.path.indicator_history(ref)
    fg = h["fg"]
    k, d = h["K"][-1], h["D"][-1]
    c = h["comps"]
    L = [f"INDICATORS ({title})",
         f"  Fear & Greed  {fg[-1]:5.1f}  {bar(fg[-1])}  {fg_label(fg[-1])}",
         "    last 10: " + " ".join(f"{x:.0f}" for x in fg),
         "    momentum {momentum:.0f} · volatility {volatility:.0f} · put/call {put_call:.0f} · "
         "safe haven {safe_haven:.0f} · breadth {breadth:.0f}".format(**c),
         f"  Sim-tastic Oscillator  %K {k:5.1f}  {bar(k)}  %D {d:5.1f}  {osc_zone(k, run.rs)}",
         "    %K last 10: " + " ".join(f"{x:.0f}" for x in h["K"]),
         "    %D last 10: " + " ".join(f"{x:.0f}" for x in h["D"])]
    return L


def lots_lines(run, price):
    b = run.book()
    L = []
    for l in b.open_lots():
        cov = b.covered(l["id"])
        src = (f"assigned at {l['strike']:g} (Week {l['week']})" if l["source"] == "assigned"
               else f"bought at {l['strike']:.2f} (Week {l['week']})")
        L.append(f"  Lot {l['id']}: {l['shares']} sh {src} · effective basis {b.eff_basis(l):.2f} · "
                 f"value {money(l['shares'] * price)}" + (f" · {cov} call(s) written" if cov else ""))
    return L


def chain_block(run, show_all=False):
    st = run.state()
    rows = run.chain()
    spot = st["spot"]
    lo, hi = (0, len(rows) - 1) if show_all else ch.window(rows, spot)
    b = run.book()
    held = {round(l["strike"], 2): l["id"] for l in b.open_lots() if l["source"] == "assigned"}
    idx = set(range(lo, hi + 1))
    for i, r in enumerate(rows):
        if round(r["K"], 2) in held:
            idx.add(i)
    days = st["days"]
    L = [f"CHAIN · SimQ {spot:.2f} · expires Friday close ({days:g} trading day{'s' if days != 1 else ''})",
         "  Call bid    ask      Δ │  Strike  │ Put bid    ask      Δ   prem%",
         "  ───────────────────────┼──────────┼──────────────────────────────"]
    marker = f"  ITM calls ▲            │ * {spot:7.2f}│ ▼ ITM puts"
    placed = False
    prev = None
    for i in sorted(idx):
        r = rows[i]
        if prev is not None and i != prev + 1:
            L.append("        ⋮                │    ⋮     │        ⋮")
        if not placed and r["K"] > spot:
            L.append(marker)
            placed = True
        cb = f"{r['cb']:7.2f}" if r["cb"] > 0 else "no bid "
        pb = f"{r['pb']:7.2f}" if r["pb"] > 0 else "no bid "
        prem = f"{r['pb'] / r['K'] * 100:6.2f}%" if r["pb"] > 0 else "      "
        mark = "◆" if round(r["K"], 2) in held else " "
        L.append(f"  {cb} {r['ca']:6.2f} {r['cd']:6.2f} │{mark}{r['K']:7.2f}  │ {pb} {r['pa']:6.2f} {r['pd']:6.2f} {prem}")
        prev = i
    if not placed:
        L.append(marker)
    for l in b.open_lots():
        if l["source"] == "assigned":
            L.append(f"  ◆ Lot {l['id']}: assigned at {l['strike']:g}, effective basis {b.eff_basis(l):.2f}")
    return L


def headline_block(run, week, phase):
    hs = headlines.draft(run, week, phase)
    return ["HEADLINES"] + [f"  {h}" for h in hs] if hs else ["HEADLINES", "  (none)"]


def monday(run, show_all=False):
    st = run.state()
    b = run.book()
    spot = st["spot"]
    prev_close = float(run.path.m["close"][st["t"] - 1])
    sh = b.shares()
    L = [f"=== {run.path.label(run.week, 'mon')} ===",
         f"Shares {sh} × {money(spot)} = {money(sh * spot)} | Cash available {money(b.free_cash())} | "
         f"Total {money(b.cash + sh * spot)}"]
    if st["split"]:
        L.append(f"REVERSE SPLIT 1-for-{run.rs['reverse_split']['ratio']} before the open: "
                 f"share counts ÷{run.rs['reverse_split']['ratio']}, prices ×{run.rs['reverse_split']['ratio']}.")
        gap_txt = ""
    else:
        gap_txt = f" (Friday close {prev_close:.2f}, gap {st['gap'] * 100:+.1f}%)"
    L.append(f"SimQ opens {spot:.2f}{gap_txt}")
    L += headline_block(run, run.week, "mon")
    L += indicators_block(run, st["ref"], "as of Friday close")
    L += ["POSITION", f"  Cash {money(b.cash)} · collateral locked {money(b.collateral())} · "
                      f"free {money(b.free_cash())}"]
    L += lots_lines(run, spot) or ["  No shares held."]
    L += chain_block(run, show_all)
    return L


def wednesday(run, show_all=False):
    st = run.state()
    b = run.book()
    w = run.week
    mon_open = float(run.path.m["open"][run.path.day(w, 0)])
    bars = run.path.bars(w, 0, 2)
    names = ("Mon", "Tue", "Wed")
    L = [f"=== {run.path.label(w, 'wed')} ===",
         "Closes vs Monday open " + f"{mon_open:.2f}: " +
         " · ".join(f"{n} {x['close']:.2f} ({(x['close'] / mon_open - 1) * 100:+.1f}%)" for n, x in zip(names, bars)),
         "  (H/L " + " · ".join(f"{n} {x['high']:.2f}/{x['low']:.2f}" for n, x in zip(names, bars)) + ")"]
    L += indicators_block(run, st["ref"], "Wednesday close")
    L.append("OPEN POSITIONS (buy to close at the ask)")
    ops = b.open_trades()
    if not ops:
        L.append("  None.")
    rows = run.chain()
    for t in ops:
        r = ch.find(rows, t["K"])
        ask = r["pa"] if t["side"] == "P" else r["ca"]
        frees = f" · frees {money(t['K'] * CONTRACT * t['open_n'])} collateral" if t["side"] == "P" else \
            f" · frees lot {t['lot']}"
        L.append(f"  [{t['tid']}] {t['cid']} ×{t['open_n']} sold {t['price']:.2f} → BTC {ask:.2f} "
                 f"({money(ask * CONTRACT * t['open_n'])}){frees}")
    L.append(f"  Cash {money(b.cash)} · collateral locked {money(b.collateral())} · free {money(b.free_cash())}")
    if b.free_cash() < st["spot"] * 0.7 * CONTRACT and ops:
        tot = b.free_cash() + sum(t["K"] * CONTRACT * t["open_n"] - (ch.find(rows, t["K"])["pa"]) * CONTRACT * t["open_n"]
                                  for t in ops if t["side"] == "P")
        fit = [r["K"] for r in rows if r["K"] * CONTRACT <= tot and r["pb"] > 0]
        if fit:
            L.append(f"  If every put were closed: free {money(tot)}; highest put strike that fits {max(fit):g}")
    L += lots_lines(run, st["spot"])
    L += chain_block(run, show_all)
    return L


def friday(run, week):
    b = run.book()
    t4 = run.path.day(week, 4)
    close = float(run.path.m["close"][t4])
    bars = run.path.bars(week, 3, 4)
    mon_open = float(run.path.m["open"][run.path.day(week, 0)])
    L = [f"=== {run.path.label(week, 'fri')} ===",
         f"Thu {bars[0]['close']:.2f} · Fri {bars[1]['close']:.2f} "
         f"(week {(close / mon_open - 1) * 100:+.1f}% from Monday open {mon_open:.2f})",
         "SETTLEMENT"]
    evs = [e for e in run.save["events"] if e.get("week") == week and e.get("phase") == "fri"]
    any_set = False
    for e in evs:
        if e["type"] in ("expire", "assign", "called"):
            any_set = True
            t = b.trades[e["tid"]]
            n = t["n"] - t["btc_n"]
            if e["type"] == "expire":
                L.append(f"  {t['cid']} ×{n}: expired worthless (close {e['close']:.2f})")
            elif e["type"] == "assign":
                L.append(f"  {t['cid']} ×{n}: ASSIGNED — bought {n * CONTRACT} sh at {t['K']:g} → Lot {e['lot']} "
                         f"(close {e['close']:.2f})")
            else:
                L.append(f"  {t['cid']} ×{n}: CALLED AWAY — sold {n * CONTRACT} sh of Lot {t['lot']} at {t['K']:g} "
                         f"(close {e['close']:.2f})")
    if not any_set:
        L.append("  No options open.")
    for e in evs:
        if e["type"] == "interest":
            L.append(f"INTEREST {money(e['amount'])} at {e['rate'] * 100:.2f}%")
        if e["type"] == "rate":
            d = e["decision"]
            verb = "held" if d == 0 else ("raised" if d > 0 else "cut")
            L.append(f"CENTRAL BANK {verb} {'' if d == 0 else f'{abs(d) * 25}bp '}→ {e['rate'] * 100:.2f}%")
    L += headline_block(run, week, "fri")
    L += indicators_block(run, t4, "Friday close")
    prev_v, v = run.week_values(week)
    sh = b.shares()
    L.append(f"ACCOUNT  Cash {money(b.cash)} · Shares {sh} × {money(close)} = {money(sh * close)} · "
             f"Total {money(b.cash + sh * close)}")
    sc = b.scorecard()
    wr = f"{sc['win_rate'] * 100:.0f}% ({sc['wins']}/{sc['judged']} judged)" if sc["win_rate"] is not None else "—"
    ap = f"{sc['avg_week_prem_pct'] * 100:.2f}%" if sc["avg_week_prem_pct"] is not None else "—"
    hp = f"{sc['held_to_expiry']} ({sc['held_pct'] * 100:.0f}%)" if sc["held_pct"] is not None else "0"
    L.append(f"SCORECARD  trades {sc['trades']} · win rate {wr} · pending {sc['pending']} · held to expiry {hp} · "
             f"assigned {sc['assigned']} · called away {sc['called']} · avg weekly premium {ap} of capital")
    L += week_pnl(run, week, prev_v, v)
    return L


def week_pnl(run, week, prev_v, v):
    b = run.book()
    wk = b.weeks.get(week, {"opened": [], "interest": 0.0})
    L = [f"WEEK {week} P&L", "  Trade                          Premium     Buyback         Net"]
    opt = 0.0
    for tid in wk["opened"]:
        t = b.trades[tid]
        prem = t["price"] * CONTRACT * t["n"]
        net = prem - t["btc_cost"]
        opt += net
        when = {"mon": "Mon", "wed": "Wed"}[t["phase"]]
        L.append(f"  {t['cid']:>14} ×{t['n']:<2} ({when})   {money(prem, True):>10} {money(-t['btc_cost'], True):>11} "
                 f"{money(net, True):>11}")
    L.append(f"  Options subtotal{'':>36}{money(opt, True):>11}")
    L.append(f"  Interest{'':>44}{money(wk['interest'], True):>11}")
    share = (v - prev_v) - opt - wk["interest"]
    L.append(f"  Shares (assignment, marks, called away, trades){'':>4}{money(share, True):>11}")
    pct = (v / prev_v - 1) * 100 if prev_v else 0.0
    L.append(f"  Week total  {money(prev_v)} → {money(v)}   {money(v - prev_v, True)} ({pct:+.2f}%)")
    return L


def package(run, week, phase, show_all=False):
    if phase == "mon":
        return monday(run, show_all)
    if phase == "wed":
        return wednesday(run, show_all)
    return friday(run, week)
