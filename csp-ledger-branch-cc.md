# SimQ Simulator: BRANCH "cc" (rules template)

## Branch info
- Forked from claude/csp-ledger.md (main, real-time TQQQ ledger) on Thu 2026-10-22; main is unchanged
- Separate account, synthetic market (SimQ), covered calls allowed, accelerated time
- Main ledger's Trade 1 (real-time TQQQ put) is NOT part of this branch
- Workflow: books are kept by script. See claude/RESUME.md for setup and commands; claude/run-index.md for runs and status
- Files: claude/simq.py (market engine), claude/simbook.py (bookkeeping, turn driver, headline plan), claude/run-NNN-state.json (append-only event log), claude/run-NNN-ledger.md and claude/run-NNN-journal.md (generated from the state). The GitHub repo flak-daddy/simq-sim holds the same current scripts and these rule docs.

## Current standard (from Oct 24, 2026; applies to Run 3 onward)
- Pricing v3 (state field `pricing: "v3"`): implied vol per regime set relative to that regime's own realized vol, using real TQQQ ratios (about 1.3x in calm/chop, 1.15x in rebound, 1.05x in selloff/crash). Skew and spreads as v2. See claude/market-calibration.md, snapshot 2.
- Headlines v2 (state field `headlines: "v2"`): 4 headlines per week, built from a reproducible plan (`simbook.py hints`). Each headline is TRUE, FALSE or NOISE; hints are no longer reliable.
- Runs 1 and 2 keep the rules they were played under (Run 1: v1 pricing W1-12, v2 from W13; Run 2: v2 pricing; both: about 6 headlines, mostly reliable hints). Their books replay unchanged.

## Run system
- Each playthrough is a numbered Run with its own random seed and its own state/ledger/journal
- Start conditions are identical every run: $7,500 cash, 4.00% APY, SimQ at $63.80, opening IV per the pricing version, rules below. Only the seed differs.
- Seeds for new runs are chosen randomly by Claude (`simq.py newseed`) and kept out of the chat until the run ends
- Comparison window: 26 sim weeks. A run may continue past 26 weeks if the user wants; cross-run comparison uses week-26 figures. Runs played under different pricing or headline versions are not directly comparable; note the versions when comparing.
- Starting a run: user says "start Run N" (new seed, current standard) or "replay Run K" (same seed, same market and headlines, for testing different choices; the path is no longer blind)
- Finished runs are archived, never overwritten

## Rules (apply to every run)
- Account: $7,500 paper cash; idle cash earns 4.00% APY (simple daily accrual, actual/365, on all cash including locked collateral; one sim week = 7 days of interest, posted at week end)
- Instrument: SimQ, a synthetic TQQQ-like index (3x leveraged daily, fat-tailed returns, regime-driven volatility). Options priced with Black-Scholes using regime/price-dependent implied vol, skew and a bid/ask spread
- Chain width: strikes from 50% to 150% of spot; $0.50 steps within 15% of spot, $1 steps to 30%, $2.50 steps beyond; strikes with a 0.00 bid show "no bid" and cannot be sold. Any listed strike can be quoted or sold
- Chain display (standard): trimmed chain of whole strikes near spot laid out as Call bid / ask | Strike | Put bid / ask, with a spot marker row ("ITM calls ▲ | * SimQ <spot> * | ▼ ITM puts") placed where the current SimQ price falls, followed by a "Lower puts" table listing every listed put strike below the trimmed chain (with bid / ask and % below spot) down to the bottom of the chain, including no-bid strikes. Shown at Monday open and midweek
- Pricing versions: v1 (original), v2 (calibrated to a real TQQQ chain: higher IV, put/call skew, spreads about $0.01 + 5% of mid), v3 (current standard: v2 skew and spreads, IV levels recalibrated to each regime's realized vol). See claude/market-calibration.md
- Size: 1 contract (100 shares) per trade; put collateral = strike x 100; calls must be covered by shares held (no naked calls)
- Strikes: chosen by the user; Claude does not pick or recommend strikes
- Contract IDs: SIMQ-W{week}-{P|C}{strike}
- Fills: sell-to-open at the bid; buy-to-close at the ask
- Weekly turn structure (3 phases):
  1. Monday open: Claude posts 4 headlines, the trimmed chain and the lower-puts table; user acts (sell put, sell covered call if holding shares, or pass)
  2. Midweek (Wednesday close): output is only the Mon-Wed path (% change measured from the Monday open price), buy-to-close prices for open positions, and the new chain plus lower-puts table; user may buy to close, sell a new put/call, or pass
  3. Friday close: Thu/Fri closes and settlement (puts assigned if SimQ closes below strike; calls called away if above), regime reveal, a 2-3 line hint recap that says which headlines were true, false or noise, interest, account line, week P&L table
- Headlines (v2 standard): exactly 4 per week, written from the week's `hints` plan:
  - TRUE: points at the real regime
  - FALSE: points, just as convincingly and in the same style, at the wrong regime the plan names
  - NOISE: realistic market news with no regime direction (earnings, product news, sector rotation, scheduled data)
  - Mix per week is drawn at random: 0-2 TRUE, 0-2 FALSE, the rest NOISE (about 25% / 22% / 53% of headlines overall). The true signal outnumbers the false one in about 40% of weeks, the false one wins about 25% of the time, and about 35% of weeks are unclear.
  - Headlines never state the regime by name and never comment on their own reliability. Claude writes them in display order and does not reorder by type.
- Regime: hidden during play, revealed at Friday settlement
- Assigned shares are eligible for covered calls; user decides if/when to sell calls and what to do with shares
- Premium credited at sale; no commissions; no early assignment
- No hindsight table of alternative strikes (replaying a seed is the allowed way to explore alternatives)
- Journal: claude/run-NNN-journal.md is append-only, one line per move, with the user's anecdote added only if given
- Reports: scorecard (win rate, premium, assignments, called-away count, totals) appears in each Friday output and in the ledger
- Honor system: the user agrees not to run `meta`/`hints`/`mid`/`fri` ahead of the phase or look up seeds of in-progress runs
