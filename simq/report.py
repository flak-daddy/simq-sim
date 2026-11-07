"""Reporting (SPEC §9): weekly series, mentor one-pager (PDF with charts), run-end
week-by-week workbook (.xlsx), and cross-run comparison.

Benchmarks: buy-and-hold SimQ (starting cash at Week 1 Monday open, split-adjusted)
and cash at the sim rate. The blind put seller is not a reported benchmark.
"""
import datetime
import io
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from simq import book as bk  # noqa: E402

CONTRACT = 100


def completed_weeks(run):
    """Weeks whose Friday has settled."""
    w, ph = run.week, run.phase
    return w if ph == "fri" else w - 1


def series(run):
    p = run.path
    start_cash = run.save["run"]["start_cash"]
    t0 = p.day(1, 0)
    open0 = float(p.m["open"][t0]) * p.adj[t0]
    rows = []
    cash_bench = start_cash
    b = bk.Book(start_cash)
    evs = run.save["events"]
    i = 0
    prev_v = start_cash
    peak = start_cash
    for w in range(1, completed_weeks(run) + 1):
        while i < len(evs) and evs[i].get("week", 0) <= w:
            b.apply(evs[i])
            i += 1
        t4 = p.day(w, 4)
        close = float(p.m["close"][t4])
        v = b.cash + b.shares() * close
        bh = start_cash * float(p.m["close"][t4]) * p.adj[t4] / open0
        rate = float(p.m["rate"][max(p.day(w, 0) - 1, t0)])
        cash_bench *= 1 + rate * 7 / 365
        wk = b.weeks.get(w, {"premium": 0.0, "buyback": 0.0, "capital": 0.0, "interest": 0.0, "opened": []})
        net = wk["premium"] - wk["buyback"]
        peak = max(peak, v)
        rows.append({"week": w, "simq_close": round(close, 2), "fg": round(float(p.fg[t4]), 1),
                     "rate": rate, "account": round(v, 2), "buy_hold": round(bh, 2), "cash_bench": round(cash_bench, 2),
                     "net_premium": round(net, 2), "capital": round(wk["capital"], 2),
                     "prem_pct": (net / wk["capital"]) if wk["capital"] else None,
                     "interest": round(wk["interest"], 2), "trades": len(wk["opened"]),
                     "week_pnl": round(v - prev_v, 2), "drawdown": v / peak - 1})
        prev_v = v
    return rows, b


def _charts(rows, title):
    weeks = [r["week"] for r in rows]
    fig, ax = plt.subplots(2, 1, figsize=(7.2, 5.2), gridspec_kw={"height_ratios": [3, 2]})
    ax[0].plot(weeks, [r["account"] for r in rows], color="#1f4e79", lw=2, label="Account")
    ax[0].plot(weeks, [r["buy_hold"] for r in rows], color="#c55a11", lw=1.4, label="Buy-and-hold SimQ")
    ax[0].plot(weeks, [r["cash_bench"] for r in rows], color="#7f7f7f", lw=1.2, ls="--", label="Cash")
    ax[0].set_title("Account value vs. benchmarks", fontsize=10, loc="left")
    ax[0].legend(fontsize=8, frameon=False)
    ax[0].yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("${x:,.0f}"))
    pct = [(r["prem_pct"] or 0) * 100 for r in rows]
    ax[1].bar(weeks, pct, color=["#1f4e79" if x > 0 else "#bfbfbf" for x in pct], width=0.8)
    ax[1].axhline(1.0, color="#c55a11", lw=0.8, ls=":")
    ax[1].text(weeks[-1], 1.02, "1%", color="#c55a11", fontsize=7, ha="right", va="bottom")
    ax[1].set_title("Weekly premium, % of capital committed", fontsize=10, loc="left")
    ax[1].set_xlabel("Week", fontsize=8)
    for a in ax:
        a.tick_params(labelsize=7)
        a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf


def summary_numbers(run):
    rows, b = series(run)
    if not rows:
        return rows, b, None
    sc = b.scorecard()
    last = rows[-1]
    sc_start = run.save["run"]["start_cash"]
    traded = [r for r in rows if r["capital"] > 0]
    nums = {
        "weeks": last["week"], "account": last["account"],
        "ret": last["account"] / sc_start - 1, "bh_ret": last["buy_hold"] / sc_start - 1,
        "cash_ret": last["cash_bench"] / sc_start - 1,
        "max_dd": min(r["drawdown"] for r in rows),
        "avg_prem": sum(r["prem_pct"] for r in traded) / len(traded) if traded else None,
        "weeks_traded": len(traded),
        "weeks_1pct": sum(1 for r in traded if r["prem_pct"] >= 0.01),
        "interest": sum(r["interest"] for r in rows), "sc": sc,
    }
    return rows, b, nums


def one_pager(run, label):
    """Writes runs/run-NNN/reports/<label>.pdf; returns its path."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    rows, b, n = summary_numbers(run)
    R = run.save["run"]
    out_dir = os.path.join(run.dir, "reports")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{label}.pdf")
    st = getSampleStyleSheet()
    small = ParagraphStyle("small", parent=st["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#555555"))
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.6 * inch, rightMargin=0.6 * inch,
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    story = [Paragraph(f"SimQ Run {R['id']} — {label.replace('-', ' ').title()}", st["Title"]),
             Paragraph(f"Weekly-1% cash-secured put practice · ruleset {R['ruleset_id']} · started {R['created']} · "
                       f"starting cash ${R['start_cash']:,.0f} · SimQ start ${R['start_price']:.2f} · "
                       f"status {R['status']}" + (f" · REPLAY of Run {R['replay_of']}" if R.get("replay_of") else "")
                       + (f" · seed {R['seed']}" if R["status"] != "active" else ""), small),
             Spacer(1, 8)]
    if n is None:
        story.append(Paragraph("No completed weeks yet.", st["Normal"]))
        doc.build(story)
        return path
    sc = n["sc"]
    pct = lambda x: "—" if x is None else f"{x * 100:+.1f}%"
    data = [["Through week", f"{n['weeks']}", "Account value", f"${n['account']:,.2f}"],
            ["Account return", pct(n["ret"]), "Buy-and-hold SimQ", pct(n["bh_ret"])],
            ["Cash benchmark", pct(n["cash_ret"]), "Max drawdown", f"{n['max_dd'] * 100:.1f}%"],
            ["Avg weekly premium", "—" if n["avg_prem"] is None else f"{n['avg_prem'] * 100:.2f}%",
             "Weeks at 1%+ premium", f"{n['weeks_1pct']} of {n['weeks_traded']} traded"],
            ["Trades", f"{sc['trades']}", "Win rate",
             "—" if sc["win_rate"] is None else f"{sc['win_rate'] * 100:.0f}% ({sc['wins']}/{sc['judged']})"],
            ["Held to expiry", f"{sc['held_to_expiry']}" + ("" if sc["held_pct"] is None else f" ({sc['held_pct'] * 100:.0f}%)"),
             "Assigned / called away", f"{sc['assigned']} / {sc['called']}"],
            ["Interest earned", f"${n['interest']:,.2f}", "Pending wheel outcomes", f"{sc['pending']}"]]
    t = Table(data, colWidths=[1.55 * inch, 1.6 * inch, 1.75 * inch, 2.1 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9),
                           ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9), ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 9),
                           ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story += [t, Spacer(1, 10), Image(_charts(rows, label), width=7.1 * inch, height=5.1 * inch), Spacer(1, 6),
              Paragraph("Win rate counts a trade as a win if it expired worthless or closed for a profit; an assigned "
                        "put (and a called-away call) is judged when its shares exit, put + shares as one wheel outcome. "
                        "Weekly premium % = net option premium of trades opened that week ÷ capital committed "
                        "(put strike × 100, or share value for calls). Buy-and-hold puts the starting cash in SimQ at "
                        "Week 1 Monday open.", small)]
    doc.build(story)
    return path


def workbook(run):
    """Week-by-week workbook (.xlsx) with formulas; returns its path."""
    from openpyxl import Workbook
    from openpyxl.chart import LineChart, Reference
    from openpyxl.styles import Alignment, Font, PatternFill

    rows, b, n = summary_numbers(run)
    R = run.save["run"]
    out_dir = os.path.join(run.dir, "reports")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"run-{R['id']:03d}-workbook.xlsx")
    wb = Workbook()
    F = "Arial"
    hdr = Font(name=F, bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="1F4E79")
    body = Font(name=F)
    blue = Font(name=F, color="0000FF")

    ws = wb.active
    ws.title = "Weekly"
    cols = ["Week", "SimQ close", "Fear & Greed", "Rate", "Account value", "Buy-and-hold", "Cash benchmark",
            "Net premium", "Capital committed", "Premium %", "Interest", "Trades opened", "Week P&L",
            "Week return", "Cumulative return", "Buy-and-hold return"]
    ws.append(cols)
    for c in ws[1]:
        c.font, c.fill, c.alignment = hdr, fill, Alignment(horizontal="center", wrap_text=True)
    start = R["start_cash"]
    for i, r in enumerate(rows, start=2):
        ws.append([r["week"], r["simq_close"], r["fg"], r["rate"], r["account"], r["buy_hold"], r["cash_bench"],
                   r["net_premium"], r["capital"], f"=IF(I{i}>0,H{i}/I{i},\"\")", r["interest"], r["trades"],
                   f"=E{i}-{'Summary!$B$4' if i == 2 else f'E{i - 1}'}",
                   f"=M{i}/{'Summary!$B$4' if i == 2 else f'E{i - 1}'}",
                   f"=E{i}/Summary!$B$4-1", f"=F{i}/Summary!$B$4-1"])
        for c in ws[i]:
            c.font = blue if c.column in (2, 3, 4, 5, 6, 7, 8, 9, 11, 12) else body
    money = '$#,##0.00;($#,##0.00);"-"'
    fmts = {"B": "0.00", "C": "0.0", "D": "0.00%", "E": money, "F": money, "G": money, "H": money, "I": money,
            "J": "0.00%", "K": money, "L": "0", "M": money, "N": "0.00%", "O": "0.0%", "P": "0.0%"}
    for col, f in fmts.items():
        for c in ws[col][1:]:
            c.number_format = f
        ws.column_dimensions[col].width = 13
    ws.freeze_panes = "B2"
    if rows:
        ch = LineChart()
        ch.title, ch.height, ch.width = "Account vs. benchmarks", 8, 18
        ch.add_data(Reference(ws, min_col=5, max_col=7, min_row=1, max_row=len(rows) + 1), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=2, max_row=len(rows) + 1))
        ws.add_chart(ch, "R2")

    tr = wb.create_sheet("Trades")
    tcols = ["ID", "Contract", "Side", "Strike", "Contracts", "Week", "Phase", "Sell price", "Premium in",
             "Bought back", "Buy-back cost", "Net", "Status", "Outcome", "Lot"]
    tr.append(tcols)
    for c in tr[1]:
        c.font, c.fill = hdr, fill
    for i, t in enumerate(b.trades.values(), start=2):
        tr.append([t["tid"], t["cid"], t["side"], t["K"], t["n"], t["week"], t["phase"], t["price"],
                   f"=H{i}*E{i}*100", t["btc_n"], t["btc_cost"], f"=I{i}-K{i}", t["status"], t["outcome"] or "pending",
                   t.get("lot_made") or t.get("lot") or ""])
        for c in tr[i]:
            c.font = blue if c.column in (4, 5, 8, 10, 11) else body
    for col in "HIKL":
        for c in tr[col][1:]:
            c.number_format = money
    for col in "ABCDEFGHIJKLMNO":
        tr.column_dimensions[col].width = 14
    tr.column_dimensions["B"].width = 18

    sm = wb.create_sheet("Summary", 0)
    sm.column_dimensions["A"].width = 40
    sm.column_dimensions["B"].width = 24
    sm["A1"] = "SimQ week-by-week workbook"
    sm["A1"].font = Font(name=F, bold=True, size=14)
    last = len(rows) + 1
    nt = len(b.trades) + 1
    keys = ["run", "ruleset", "status", "cash", "price", "weeks", "final", "ret", "bh", "cashb", "prem",
            "int", "avgp", "w1", "trades", "wins", "losses", "wr", "seed"]
    row = {k: i + 3 for i, k in enumerate(keys)}          # items start on row 3
    B = lambda k: f"B{row[k]}"
    items = {
        "run": ("SimQ run", f"Run {R['id']}"), "ruleset": ("Ruleset", R["ruleset_id"]),
        "status": ("Status", R["status"]), "cash": ("Starting cash", start),
        "price": ("SimQ start price", R["start_price"]),
        "weeks": ("Weeks completed", f"=COUNT(Weekly!A2:A{last})"),
        "final": ("Final account value", f"=INDEX(Weekly!E2:E{last},{B('weeks')})"),
        "ret": ("Account return", f"={B('final')}/{B('cash')}-1"),
        "bh": ("Buy-and-hold return", f"=INDEX(Weekly!F2:F{last},{B('weeks')})/{B('cash')}-1"),
        "cashb": ("Cash benchmark return", f"=INDEX(Weekly!G2:G{last},{B('weeks')})/{B('cash')}-1"),
        "prem": ("Total net premium", f"=SUM(Weekly!H2:H{last})"),
        "int": ("Total interest", f"=SUM(Weekly!K2:K{last})"),
        "avgp": ("Average weekly premium % (traded weeks)", f"=IFERROR(AVERAGE(Weekly!J2:J{last}),\"\")"),
        "w1": ("Weeks with premium of 1% or more", f"=COUNTIF(Weekly!J2:J{last},\">=0.01\")"),
        "trades": ("Trades", f"=COUNTA(Trades!A2:A{nt})"),
        "wins": ("Wins (judged)", f"=COUNTIF(Trades!N2:N{nt},\"win\")"),
        "losses": ("Losses (judged)", f"=COUNTIF(Trades!N2:N{nt},\"loss\")"),
        "wr": ("Win rate (judged trades)", f"=IFERROR({B('wins')}/({B('wins')}+{B('losses')}),\"\")"),
        "seed": ("Seed", R["seed"] if R["status"] != "active" else "hidden (run active)"),
    }
    money = '$#,##0.00;($#,##0.00);"-"'
    fmt = {"cash": money, "final": money, "prem": money, "int": money, "price": "0.00",
           "ret": "0.0%", "bh": "0.0%", "cashb": "0.0%", "avgp": "0.00%", "wr": "0.0%"}
    for k in keys:
        label, val = items[k]
        sm[f"A{row[k]}"] = label
        sm[f"A{row[k]}"].font = Font(name=F, bold=True)
        sm[B(k)] = val
        sm[B(k)].font = body if isinstance(val, str) and val.startswith("=") else blue
        if k in fmt:
            sm[B(k)].number_format = fmt[k]
    sm[f"A{row['seed'] + 2}"] = "Blue = values written by the sim from the run's event log; black = formulas."
    sm[f"A{row['seed'] + 2}"].font = Font(name=F, italic=True, color="7F7F7F")
    for c in ws["M"][1:] + ws["N"][1:] + ws["O"][1:] + ws["P"][1:]:
        c.value = c.value.replace("Summary!$B$4", f"Summary!$B${row['cash']}")
    wb.save(path)
    return path


def compare(runs):
    """Cross-run comparison table with ruleset differences."""
    lines = []
    hdr = f"{'Run':>4} {'Status':<10} {'Ruleset':<8} {'Weeks':>5} {'Return':>8} {'B&H':>8} {'MaxDD':>7} {'AvgPrem':>8} {'WinRate':>8}"
    lines.append(hdr)
    for r in runs:
        rows, b, n = summary_numbers(r)
        R = r.save["run"]
        if n is None:
            lines.append(f"{R['id']:>4} {R['status']:<10} {R['ruleset_id']:<8}   no completed weeks")
            continue
        wr = n["sc"]["win_rate"]
        lines.append(f"{R['id']:>4} {R['status']:<10} {R['ruleset_id']:<8} {n['weeks']:>5} {n['ret'] * 100:>+7.1f}% "
                     f"{n['bh_ret'] * 100:>+7.1f}% {n['max_dd'] * 100:>6.1f}% "
                     f"{'—' if n['avg_prem'] is None else f'{n['avg_prem'] * 100:.2f}%':>8} "
                     f"{'—' if wr is None else f'{wr * 100:.0f}%':>8}")
    base = runs[0].save["ruleset"]
    for r in runs[1:]:
        d = _diff(base, r.save["ruleset"])
        lines.append(f"Ruleset differences Run {runs[0].save['run']['id']} vs Run {r.save['run']['id']}: "
                     + ("none" if not d else "; ".join(d)))
    ab = [r.save["run"]["id"] for r in runs if r.save["run"]["status"] == "abandoned"]
    if ab:
        lines.append(f"Abandoned runs listed for reference only, not compared: {ab}")
    return lines


def _diff(a, b, prefix=""):
    out = []
    for k in sorted(set(a) | set(b)):
        if k in ("ruleset_id", "calibration"):
            continue
        va, vb = a.get(k), b.get(k)
        if isinstance(va, dict) and isinstance(vb, dict):
            out += _diff(va, vb, prefix + k + ".")
        elif va != vb:
            out.append(f"{prefix}{k}: {va} → {vb}")
    return out
