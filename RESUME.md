# RESUME: how to run the SimQ simulator in a fresh chat

Rules: claude/csp-ledger-branch-cc.md. Index: claude/run-index.md. Calibration: claude/market-calibration.md. Books are kept by script; do not hand-edit ledgers.

## Active run
**None.** Run 3 closed after Week 52 (Sun 2026-10-25): $8,974.05 (+19.65%), holding 100 shares (lot 3, cost $50, marked $36.62); buy-and-hold SimQ $4,304.86 (-42.60%); cash-only $7,799.18 (+3.99%). Week 26 comparison figure $9,779.00 (+30.39%). Seed 943118079. Review: claude/run-003-summary.txt.
To start Run 4: `python3 simq.py newseed` (keep the seed hidden), then `python3 simbook.py new --run 4 --seed S`, and follow the same setup and weekly flow below with run-004 files. Consider the regime-vs-price-direction check noted in run-003-summary.txt section 6 first.
At Week 52 of any run: reveal the seed, write claude/run-NNN-summary.txt (full-year review), set the closed status_note, update run-index.md.
Previous: Run 2 closed after Week 52: $11,924.36 (+58.99%); Week 26 figure $9,189.18 (+22.52%). Review: claude/run-002-summary.txt.
New runs automatically use the current standard (pricing v3, headlines v3): `simbook.py new` writes `pricing: "v3"` and `headlines: "v3"` into the state (`--headlines v2` for the old style). Old states without those fields replay exactly as they were played.
A closed run's ledger shows its closed status via a `status_note` (or older `status`) key in its state file.

## Setup (once per chat) — via GitHub, no retyping
Code, rule docs and state live in the private repo **flak-daddy/simq-sim** (branch main): simq.py, simbook.py, headlines.py, RESUME.md, csp-ledger-branch-cc.md, market-calibration.md, run-NNN-state.json, run-NNN-ledger.md, run-NNN-journal.md (and run summaries). Same content as the project copies.
1. Call `add_repo` with owner `flak-daddy`, repo `simq-sim`, access `push`.
2. `git clone --depth 1 https://github.com/flak-daddy/simq-sim /home/claude/simq-sim` (generous timeout).
3. Copy simq.py, simbook.py, headlines.py and the active run's files into a separate working folder (e.g. /home/claude/simq-runN/) and play the week there; the repo clone is only touched at Friday close (see below). This keeps the repo clean mid-week.
4. `python3 simbook.py status` (in the working folder) confirms where the run stands.
Do NOT project_read the scripts and re-Write them; that is the token-expensive path this replaces.
Fallback only if GitHub is unreachable: project_read claude/simq.py, claude/simbook.py, claude/run-NNN-state.json and save them locally.
Before using either copy, check that simbook.py contains `print_week_pnl` and `headline_plan`, and simq.py contains `SKEW_V2` and `REG3_IV`. If not, it's stale.

## Commands (all in the working folder)
- `python3 simbook.py open` : Monday open (spot, trimmed chain, lower-puts table, account line).
- Headlines v3 runs (state has `headlines: "v3"`): `open` prints the 4 headlines itself from headlines.py. Relay them verbatim; do NOT run `hints` and do not write headlines. Friday shows the regime only (no per-headline recap). v3 rules: reported data is always true; misleading headlines are always opinion; true signals can also come as vague opinion. Opinions carry credibility cues (basis: current data / indirect / none; neutral vs positioned source) that shift the odds but never decide them.
- Headlines v2 runs only: `python3 simbook.py hints` : Claude only. Hidden regime plus this week's 4-headline plan (TRUE / FALSE:<regime> / NOISE, in display order). Write the 4 headlines from it. Never show this output to the user.
- `sell P|C STRIKE [--lot N]` (calls pick their covering lot with --lot; default is the oldest free lot), `relot ID LOT` (move an open call to another free lot, logged in the journal), `btc ID`, `pass`, `note "user anecdote"`, `quote P|C STRIKE`, `chain [--all]`, `status`, `weekpnl W`
- `python3 simbook.py mid` : midweek path, buy-to-close prices, trimmed chain, lower-puts table
- `python3 simbook.py fri` : settle, post interest, print the week P&L breakdown, advance to next week
- `python3 simbook.py new --run N --seed S` : start a new run on the current standard (seed from `python3 simq.py newseed`, keep hidden)
- Ledger and journal regenerate via `python3 simbook.py render` (also automatic).

## Output style (user asked for less bloat)
- Chain layout: Call bid / ask | Strike | Put bid / ask (strike in the middle, calls left, puts right).
- Spot marker: the chain includes a row "ITM calls ▲ | * SimQ <spot> * | ▼ ITM puts" placed where the current SimQ price falls between strikes. simbook prints it automatically; keep it when relaying the chain.
- Held-lot marker: the strike where each held share lot was assigned gets a ◆ in the chain (row always shown, with a ⋮ gap row if it sits outside the trimmed window), plus a legend line under the table with lot number, assigned strike and effective basis. The marker disappears when the lot is called away. simbook prints it automatically; keep it when relaying.
- Standard at Monday open and midweek: after the trimmed chain, show a "Lower puts" table listing EVERY listed put strike below the trimmed chain (including .5 strikes and $2.50 steps), highest first, with bid / ask and % below spot, all the way to the bottom of the chain (no-bid strikes included). simbook prints this automatically.
- Monday (v2 runs): exactly 4 headlines written from the `hints` plan, in the plan's order. TRUE points at the real regime; FALSE points at the named wrong regime just as convincingly; NOISE is regime-neutral market news. Never name the regime or signal which headlines are reliable. Then the trimmed chain + lower-puts table and one account line.
- Midweek: Mon-Wed path, buy-to-close price for open positions, new chain + lower-puts table. Midweek % change is measured from the Monday open price and labeled that way. When free cash is short, show what closing each position would free and the highest strike that then fits.
- Friday: result lines, regime reveal (v3: regime only, no headline recap; v2: 2-3 line hint recap labeling each headline), account line, and the **Week P&L table** (each trade opened that week with premium in / buy-back out and its net, options subtotal, interest, share moves if any, and the week total from last Friday's account value to this Friday's, with %). simbook prints the table automatically. No full hint walk-through unless asked.
- Never recommend strikes. Fills: sell at bid, buy to close at ask. Calls must be covered; puts need free cash (check collateral before executing and say so if a strike doesn't fit). If the user asks to sell a call with no shares, don't execute; ask whether they meant the put. If the user says "buy" a put/call to open, don't execute; the sim has no long options, so ask whether they meant sell (it has always been a slip so far).
- Journal: one line per move, user anecdote added only if given.
- Auto-advance: when the user sells a put/call at Monday open, record the fill and immediately run `mid` in the same turn (show the fill line, then the midweek package). Don't stop to ask.
- At midweek, "hold" means hold and settle Friday. When the user acts at midweek (buy to close and/or sell new), execute it and settle Friday in the same turn.

## After each Friday (only then)
1. Copy the run's state/ledger/journal (and any changed scripts or rule docs) from the working folder into the repo clone, then `git add -A && git commit -m "Run N Week W" && git push` (end the commit message with the session's attribution lines). One commit per sim week; no mid-week pushes.
2. Upload to the project with `project_write` using `local_path` (no token cost): claude/run-NNN-state.json, claude/run-NNN-ledger.md, claude/run-NNN-journal.md (and claude/simbook.py / simq.py / rule docs if they changed).
Update claude/run-index.md only when status changes.

## Honor system
User agrees not to run `meta`/`hints`/`mid`/`fri` ahead of the phase or look up in-progress seeds. Recommend a fresh chat every 4-5 weeks (the user has been comfortable going longer).
