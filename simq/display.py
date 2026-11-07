"""Script output for each decision point (SPEC §3, §11), as chat markdown (v1 style):
headers, bold lines, numbered headlines, rendered tables. Claude relays it as-is, outside
a code block, so it renders; headline drafts are the one part Claude rewords."""
from simq import chain as ch
from simq import headlines
from simq.indicators import fg_label

BREAK = "\n-----------------\n"   # blank lines around it so markdown draws a rule, not a heading
CONTRACT = 100


def money(x, sign=False):
    if abs(x) < 0.005:
        x = 0.0
    s = f"{abs(x):,.2f}"
    if sign:
        return ("+" if x >= 0 else "−") + "$" + s
    return ("−$" if x < 0 else "$") + s


def pct(x, sign=True):
    return f"{x * 100:+.1f}%" if sign else f"{x * 100:.1f}%"


def k_txt(K):
    return f"{K:g}"


def osc_zone(k, rs):
    o = rs["osc"]
    return "oversold" if k < o["oversold"] else "overbought" if k > o["overbought"] else "neutral"


def indicators_block(run, ref, title):
    h = run.path.indicator_history(ref)
    fg, K, D = h["fg"], h["K"], h["D"]
    c = h["comps"]
    row = lambda xs: " ".join(f"{x:.0f}" for x in xs)
    return [f"**Indicators** ({title})", "",
            "| Indicator | Today | Reading | Last 10 days (oldest → today) |",
            "|---|---:|---|---|",
            f"| Fear & Greed | **{fg[-1]:.0f}** | {fg_label(fg[-1])} | {row(fg)} |",
            f"| Sim-tastic %K | **{K[-1]:.0f}** | {osc_zone(K[-1], run.rs)} | {row(K)} |",
            f"| Sim-tastic %D | **{D[-1]:.0f}** | | {row(D)} |",
            "",
            "F&G components: momentum {momentum:.0f} · volatility {volatility:.0f} · put/call {put_call:.0f} · "
            "safe haven {safe_haven:.0f} · breadth {breadth:.0f}".format(**c), ""]


def lots_lines(run, price):
    b = run.book()
    L = []
    for l in b.open_lots():
        cov = b.covered(l["id"])
        src = (f"assigned at {k_txt(l['strike'])} (Week {l['week']})" if l["source"] == "assigned"
               else f"bought at {l['strike']:.2f} (Week {l['week']})")
        L.append(f"- Lot {l['id']}: {l['shares']} sh {src} · effective basis **{b.eff_basis(l):.2f}** · "
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
    L = [f"**Chain** · SimQ {spot:.2f} · expires Friday close ({days:g} trading day{'s' if days != 1 else ''})", "",
         "| Call bid / ask | Strike | Put bid / ask | Put Δ | Prem % |",
         "|---|:---:|---|---:|---:|"]
    marker = f"| ITM calls ▲ | **\\* SimQ {spot:.2f} \\*** | ▼ ITM puts | | |"
    placed, prev = False, None
    for i in sorted(idx):
        r = rows[i]
        if prev is not None and i != prev + 1:
            L.append("| ⋮ | ⋮ | ⋮ | | |")
        if not placed and r["K"] > spot:
            L.append(marker)
            placed = True
        cq = f"{r['cb']:.2f} / {r['ca']:.2f}" if r["cb"] > 0 else f"no bid / {r['ca']:.2f}"
        pq = f"{r['pb']:.2f} / {r['pa']:.2f}" if r["pb"] > 0 else f"no bid / {r['pa']:.2f}"
        prem = f"{r['pb'] / r['K'] * 100:.2f}%" if r["pb"] > 0 else ""
        mark = " ◆" if round(r["K"], 2) in held else ""
        L.append(f"| {cq} | **{k_txt(r['K'])}**{mark} | {pq} | {r['pd']:.2f} | {prem} |")
        prev = i
    if not placed:
        L.append(marker)
    leg = [f"◆ Lot {l['id']}: assigned at {k_txt(l['strike'])}, effective basis {b.eff_basis(l):.2f}"
           for l in b.open_lots() if l["source"] == "assigned"]
    if leg:
        L += ["", " · ".join(leg)]
    return L


def headline_block(run, week, phase):
    hs = headlines.draft(run, week, phase)
    if not hs:
        return ["**Headlines**", "", "_(none)_", ""]
    return ["**Headlines**", ""] + [f"{i}. {h}" for i, h in enumerate(hs, 1)] + [""]


def monday(run, show_all=False):
    st = run.state()
    b = run.book()
    spot = st["spot"]
    prev_close = float(run.path.m["close"][st["t"] - 1])
    sh = b.shares()
    L = [f"### {run.path.label(run.week, 'mon')}", ""]
    if st["split"]:
        r = run.rs["reverse_split"]["ratio"]
        L.append(f"**REVERSE SPLIT 1-for-{r} before the open:** share counts ÷{r}, prices ×{r}.  ")
        L.append(f"**SimQ opens {spot:.2f}**  ")
    else:
        L.append(f"**SimQ opens {spot:.2f}** (Friday close {prev_close:.2f}, gap {pct(st['gap'])})  ")
    L += [f"**Shares {sh} × {money(spot)} = {money(sh * spot)} · Cash available {money(b.free_cash())} · "
          f"Total {money(b.cash + sh * spot)}**", ""]
    L += headline_block(run, run.week, "mon")
    L += indicators_block(run, st["ref"], "as of Friday close")
    L.append(f"**Position:** cash {money(b.cash)} · collateral locked {money(b.collateral())} · "
             f"free {money(b.free_cash())}" + ("" if b.shares() else " · no shares"))
    L += lots_lines(run, spot) + [""]
    L += chain_block(run, show_all)
    return L


def wednesday(run, show_all=False):
    st = run.state()
    b = run.book()
    w = run.week
    mon_open = float(run.path.m["open"][run.path.day(w, 0)])
    bars = run.path.bars(w, 0, 2)
    L = [f"### {run.path.label(w, 'wed')}", "",
         f"**SimQ {st['spot']:.2f}** · from Monday open {mon_open:.2f}:", "",
         "| | Mon | Tue | Wed |", "|---|---:|---:|---:|",
         "| Close | " + " | ".join(f"{x['close']:.2f}" for x in bars) + " |",
         "| vs Mon open | " + " | ".join(pct(x["close"] / mon_open - 1) for x in bars) + " |",
         "| High / low | " + " | ".join(f"{x['high']:.2f} / {x['low']:.2f}" for x in bars) + " |", ""]
    L += indicators_block(run, st["ref"], "Wednesday close")
    L += ["**Open positions** (buy to close at the ask)", ""]
    ops = b.open_trades()
    rows = run.chain()
    if not ops:
        L.append("- None.")
    for t in ops:
        r = ch.find(rows, t["K"])
        ask = r["pa"] if t["side"] == "P" else r["ca"]
        frees = (f" · frees {money(t['K'] * CONTRACT * t['open_n'])} collateral" if t["side"] == "P"
                 else f" · frees Lot {t['lot']}")
        L.append(f"- [{t['tid']}] {t['cid']} ×{t['open_n']}, sold {t['price']:.2f} → **BTC {ask:.2f}** "
                 f"({money(ask * CONTRACT * t['open_n'])}){frees}")
    L += ["", f"**Cash {money(b.cash)} · collateral locked {money(b.collateral())} · free {money(b.free_cash())}**"]
    if b.free_cash() < st["spot"] * 0.7 * CONTRACT and any(t["side"] == "P" for t in ops):
        tot = b.free_cash() + sum(t["K"] * CONTRACT * t["open_n"] - ch.find(rows, t["K"])["pa"] * CONTRACT * t["open_n"]
                                  for t in ops if t["side"] == "P")
        fit = [r["K"] for r in rows if r["K"] * CONTRACT <= tot and r["pb"] > 0]
        if fit:
            L.append(f"If every put were closed: free {money(tot)}; highest put strike that fits **{k_txt(max(fit))}**")
    L += lots_lines(run, st["spot"]) + [""]
    L += chain_block(run, show_all)
    return L


def friday(run, week):
    b = run.book()
    t4 = run.path.day(week, 4)
    close = float(run.path.m["close"][t4])
    bars = run.path.bars(week, 3, 4)
    mon_open = float(run.path.m["open"][run.path.day(week, 0)])
    L = [f"### {run.path.label(week, 'fri')}", "",
         f"**Thu {bars[0]['close']:.2f} · Fri {bars[1]['close']:.2f}** "
         f"(week {pct(close / mon_open - 1)} from Monday open {mon_open:.2f})", "",
         "**Settlement**", ""]
    evs = [e for e in run.save["events"] if e.get("week") == week and e.get("phase") == "fri"]
    any_set = False
    for e in evs:
        if e["type"] in ("expire", "assign", "called"):
            any_set = True
            t = b.trades[e["tid"]]
            n = t["n"] - t["btc_n"]
            if e["type"] == "expire":
                L.append(f"- {t['cid']} ×{n}: expired worthless (close {e['close']:.2f})")
            elif e["type"] == "assign":
                L.append(f"- {t['cid']} ×{n}: **ASSIGNED** — bought {n * CONTRACT} sh at {k_txt(t['K'])} → "
                         f"Lot {e['lot']} (close {e['close']:.2f})")
            else:
                L.append(f"- {t['cid']} ×{n}: **CALLED AWAY** — sold {n * CONTRACT} sh of Lot {t['lot']} at "
                         f"{k_txt(t['K'])} (close {e['close']:.2f})")
    if not any_set:
        L.append("- No options open.")
    for e in evs:
        if e["type"] == "interest":
            L.append(f"- Interest {money(e['amount'])} at {e['rate'] * 100:.2f}%")
        if e["type"] == "rate":
            d = e["decision"]
            verb = "held" if d == 0 else ("raised" if d > 0 else "cut")
            L.append(f"- **Central bank {verb}** {'' if d == 0 else f'{abs(d) * 25}bp '}→ {e['rate'] * 100:.2f}%")
    L.append("")
    L += headline_block(run, week, "fri")
    L += indicators_block(run, t4, "Friday close")
    prev_v, v = run.week_values(week)
    sh = b.shares()
    L.append(f"**Account:** cash {money(b.cash)} · shares {sh} × {money(close)} = {money(sh * close)} · "
             f"**total {money(b.cash + sh * close)}**  ")
    sc = b.scorecard()
    wr = f"{sc['win_rate'] * 100:.0f}% ({sc['wins']}/{sc['judged']} judged)" if sc["win_rate"] is not None else "—"
    ap = f"{sc['avg_week_prem_pct'] * 100:.2f}%" if sc["avg_week_prem_pct"] is not None else "—"
    hp = f"{sc['held_to_expiry']} ({sc['held_pct'] * 100:.0f}%)" if sc["held_pct"] is not None else "0"
    L.append(f"**Scorecard:** trades {sc['trades']} · win rate {wr} · pending {sc['pending']} · held to expiry {hp} · "
             f"assigned {sc['assigned']} · called away {sc['called']} · avg weekly premium {ap} of capital")
    L.append("")
    L += week_pnl(run, week, prev_v, v)
    return L


def week_pnl(run, week, prev_v, v):
    b = run.book()
    wk = b.weeks.get(week, {"opened": [], "interest": 0.0})
    L = [f"**Week {week} P&L**", "", "| Item | Premium | Buy-back | Net |", "|---|---:|---:|---:|"]
    opt = 0.0
    for tid in wk["opened"]:
        t = b.trades[tid]
        prem = t["price"] * CONTRACT * t["n"]
        net = prem - t["btc_cost"]
        opt += net
        when = {"mon": "Mon", "wed": "Wed"}[t["phase"]]
        L.append(f"| {t['cid']} ×{t['n']} ({when}) | {money(prem, True)} | {money(-t['btc_cost'], True)} | {money(net, True)} |")
    L.append(f"| **Options subtotal** | | | **{money(opt, True)}** |")
    L.append(f"| Interest | | | {money(wk['interest'], True)} |")
    share = (v - prev_v) - opt - wk["interest"]
    L.append(f"| Shares (assignment, marks, called away, trades) | | | {money(share, True)} |")
    p = (v / prev_v - 1) * 100 if prev_v else 0.0
    L.append(f"| **Week total** {money(prev_v)} → {money(v)} | | | **{money(v - prev_v, True)} ({p:+.2f}%)** |")
    return L


def package(run, week, phase, show_all=False):
    if phase == "mon":
        return monday(run, show_all)
    if phase == "wed":
        return wednesday(run, show_all)
    return friday(run, week)
