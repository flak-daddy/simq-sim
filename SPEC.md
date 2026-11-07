# SimQ v2 — Specification

Written Nov 6, 2026, from `claude/v2-design-checklist.md` (design phase complete). Updated the same day with the Milestone 1 calibration results; ruleset `v2.0` passed the gate (`calibration/report-v2.0.md`). This file is the single source of truth for v2. Every decision is stated; there are no open questions. Where this spec and the checklist disagree, this spec wins and the checklist is corrected.

v1 (`main` branch, `ARCHIVE-v1-RULEBOOK.md`) is reference only. v2 is a ground-up rebuild on the `v2` branch.

---

## 0. Rule 0 — Static rulesets

1. A run's ruleset is fixed when the run starts and never changes during that run.
2. Rule changes go into the next run's ruleset, never retrofitted.
3. Every run stores its full ruleset (every parameter in §1–§12) inside its own save file. The code reads parameters from the save file, never from version flags.
4. **Bugs:** code doing something the run's ruleset never intended is a bug. Bugs are fixed and the run continues. A rule change is never allowed mid-run.
5. **Abandoned runs** are kept, marked `abandoned` with the reason, and excluded from comparisons.
6. **Old runs** stay viewable (results and trade log), not re-runnable. New code is not required to replay them.
7. **Hard gate:** a run may only start on a ruleset whose calibration report (§10) shows every threshold passing. The report is saved alongside the ruleset.

### Ruleset file
- `rulesets/ruleset-v2.N.json` holds every parameter. Run 1 uses `ruleset-v2.0.json`.
- At run start the chosen ruleset is copied whole into the run's save file, plus the run-specific values: seed (hidden), start price, starting cash, start rate.
- Parameters marked **[fit]** below are given starting values here and final values by the Milestone 1 calibration; the frozen values are whatever `ruleset-v2.0.json` holds when its calibration report passes.

---

## 1. Market engine (price path)

SimQ is modeled on **TQQQ** (3× daily Nasdaq-100) at the scale of days and weeks.

### 1.1 Structure: backdrop + sentiment
- **Backdrop:** 3 slow macro states — `bull`, `neutral`, `bear` — lasting months (mean duration [fit], starting value ~6 months). The backdrop only shifts where sentiment tends to rest (its mean-reversion target); it never sets price drift directly.
- **Sentiment:** a hidden value 0–100.
  - Mean-reverts toward the backdrop's resting level with a half-life of about **3 weeks** (15 trading days), matching the real CNN series.
  - Pushed by news shocks: random daily shocks (fat-tailed), rate-meeting surprises (§2.6), and feedback from large price moves (big down days push fear, big up days push greed).
  - Sets each day's drift and volatility: fear → lower drift and higher volatility; greed → modest positive drift and low volatility. Mapping curves [fit].
- **Intent:** sentiment clearly dominates the backdrop ("≥75%" is intent, not a target). Calibration reports the variance split; there is no threshold and no tuning to an exact number.
- **No unexplained extremes:** every extreme bullish or bearish stretch comes from sentiment, so it is always visible on the Fear & Greed gauge (§12) and in headlines (§6). Stretches must not drag on unrealistically long; spell lengths are tested (§10).

### 1.2 Daily bar
- Each sim day produces open, high, low, close.
- SimQ daily return = 3 × underlying return − daily drag (expense ratio + 2× the sim rate). Shocks are Student-t with tails fattening as sentiment falls (df 8 in greed down to about 3 in extreme fear), so extremes cluster in fear.
- One day's move, including a Monday gap, is capped near ±35%.
- Weekday opens equal the prior close. High/low are generated around the open→close move with intraday range scaled by that day's volatility [fit].
- **Weekend gaps only:** Monday's open may differ from Friday's close. Average absolute Monday gap about 2%, larger in fear.
- Down-moves cluster: fear raises volatility and pulls price down in steps with relief bounces.
- Every sim week has 5 trading days; holidays are ignored for trading.
- **Labels (decided Nov 6):** week + day only, e.g. "Week 47 (Year 1, week 47) · Monday open". Week 1 is the first week of January; holiday weeks are marked: week 1 New Year's, 27 Independence Day, 36 Labor Day, 47 Thanksgiving, 52 Christmas.
- A sim year is 52 weeks (260 trading days); the calibration report scores calendar sim years.

### 1.3 Start price
Randomized per run, uniform $30–$90, rounded to cents, recorded in the run's save file.

### 1.4 Reverse split (rare fallback)
- If a Friday close is below **$2.50**, a **1-for-10** reverse split applies before the next Monday open: price ×10, shares ÷10 (rounded down), cash value preserved.
- Leftover odd-lot shares can only be sold outright; they cannot cover calls. Cost basis per share scales ×10.
- Open options cannot exist at that moment (settlement is Friday close), so no contract adjustment is needed.
- Calibrated runs should almost never reach it; the calibration report counts how often it fires.

### 1.5 Long-run behavior
- Median SimQ year +5% to +15%; bad years stay common.
- Daily tail frequencies (±5%, ±10%, ±15%) match real TQQQ, with extremes clustering in fear.

---

## 2. Option pricing

### 2.1 Method
Black-Scholes with the central-bank rate (§2.6) as the risk-free rate, plus the adjustments below. Time in trading days / 252.

### 2.2 IV level
- At-the-money IV is a function of the hidden sentiment: IV rises as sentiment falls (like VIX vs. fear). The curve is set so 5-day ATM IV / forward realized vol runs about **1.05 in extreme fear to 1.30 in greed**, the ratios seen in real chains (v1 notes).
- Down-day jump: after a down day, IV += **3 × the day's loss** (v1 rule), easing back as Fear & Greed recovers.
- Response speed is best-effort, set by judgment against the Nov 6 stressed chain and v1's Oct 2026 notes; no dedicated fit.
- Anchors: calm weekly ATM IV ≈ 1.25–1.3× realized vol (v1 notes, Oct 23 chain: 82% vs. 63% realized); stressed ATM ≈ 100–106% (Nov 6 chain).

### 2.3 Skew
- Steep downward slope: strike IV = ATM IV × (1 − slope × (K/S − 1)). Slope **1.3 at calm IV (fits the Oct 23 chain) rising to 1.6 at stressed IV (fits the Nov 13 chain, spot $52.25)**, linear in ATM IV between 82% and 101%. IV highest on puts, ~100–106% near the money in stress, falling to ~70% on far calls.
- Puts far richer than equidistant calls (reference: 45P ≈ $0.89 vs. 60C ≈ $0.31 on Nov 6).
- **Price floor:** far strikes bottom out at a few cents; this floor is what makes far-call IV tick up. There is no true smile.
- **Short-expiry steepening:** the skew slope scales up as expiry nears; the 1-day slope ≈ **1.7×** the 5-day slope (Wednesday chains steeper than Monday's).
- Put-call parity holds between puts and calls at every strike.

### 2.4 Quotes
- **Spread width** depends on option price, moneyness and fear: wider for pricier options, for in-the-money strikes, and in extreme fear. Reference (Nov 6): ~2–5¢ on cheap options, ~12–18¢ near $2–3, dollars wide deep in the money.
- **Messy quotes (light):** occasional wide quotes on .5 strikes and in-the-money options, seeded by (seed, week, phase, strike) so display, fills and buy-backs agree. Bid and ask are never out of order and the chain is never non-monotone.
- **No-bid rule:** a strike shows no bid only when its fair value is essentially zero; bids persist down to $0.01.
- Prices rounded to cents; ask ≥ bid + $0.01.

### 2.5 Calibration references
- **Run 1 is fit now** to: the Nov 6, 2026 stressed chain (Nov 13 expiry, spot $52.25, puts and calls) and v1's Oct 23, 2026 1-day and 5-day chains plus calm-period IV notes (`claude/market-calibration.md`).
- Calm-day, Monday and Wednesday snapshots are still to collect; when collected they refine the **next** ruleset, not Run 1.

### 2.6 Interest rate (central bank)
- Start rate **3.50%**, the same for every run under `ruleset-v2.0`; bounds **1.00%–8.00%**; moves in **0.25%** steps.
- Scheduled sim meetings every **6 sim weeks** (announced at Friday close of meeting week). Outcomes: hike / hold / cut, with odds set by the backdrop, sentiment and simulated macro data [fit]. Moves of more than one step are allowed only in extreme states [fit].
- Feeds: cash interest (§4), option pricing (§2.1), and sentiment (a surprise hike is a fear shock; a surprise cut is mixed). Headlines report meetings and expectations (§6).
- The mechanism is fixed per run; only the rate value moves.

### 2.7 Blind put seller target
Positive edge with painful drawdowns, as real weekly TQQQ puts imply when real IV meets real moves: about +0.5% to +1.5% of collateral per week for a blind Monday put 10% below spot (§10 test 6), with worst weeks near −50%. Reading the market should beat it.

---

## 3. Chain builder and display

- **Strikes:** $1 steps, plus .5 strikes near the money, spacing scaled with price (like the real chain).
- **Expiry:** this Friday only.
- **Default window:** from spot outward on each side until the OTM option's bid falls below $0.10; that edge strike is shown (confirmed Nov 6 over v1's first-no-bid edge). Full chain on request (`show --all`).
- **Columns:** call bid / ask / delta | strike | put bid / ask / delta / premium % of collateral (put bid ÷ strike).
- **Layout:** calls left, strike middle, puts right.
- **Spot marker row** at the in-the-money boundary: `| ITM calls ▲ | ** * SimQ <spot> * ** | ▼ ITM puts |`.
- **Held-lot marker:** `◆` on the strike where each still-held lot was assigned (row always shown, with a `⋮` gap row if outside the window), plus a legend line: lot number, assigned strike, effective basis. Disappears when the lot exits.
- **Contract IDs:** `SIMQ-W{week:02d}-{P|C}{strike}`, e.g. `SIMQ-W05-P52`, `SIMQ-W05-P52.5`.
- Claude never picks, suggests or recommends strikes.

---

## 4. Account and trading rules

| Item | Rule |
|---|---|
| Starting cash | User picks at run start; recorded in the save file |
| Interest | On all cash including locked collateral, at the current sim rate (§2.6); simple daily accrual, actual/365, 7 calendar days per sim week, posted at Friday close |
| Commissions | None |
| Size | Multiple contracts per trade, up to what collateral (puts) or held shares (calls) cover |
| Put collateral | strike × 100 × contracts, in free cash; shares never collateralize puts |
| Calls | Covered by 100 held shares per contract from round lots; no naked calls |
| Allowed | Sell cash-secured puts, sell covered calls, buy to close, buy shares, sell shares |
| Not allowed | Long options, spreads, single-action rolls, limit orders |
| Option fills | Sell at the bid; buy to close at the ask; immediate |
| Share trades | Round lots of 100 only; buy at SimQ price + $0.01–0.02, sell at − $0.01–0.02 (seeded) |
| Early assignment | Never |
| Settlement | Friday close only. Put assigned if close < strike by even $0.01; call called away if close > strike by even $0.01 |
| Assigned shares | Sell outright at market, or exit through covered calls |
| Cost basis | Per lot. Effective basis = assigned (or bought) price − all option premium credited to that lot ÷ shares |
| Call cover lot | Default: free lot whose effective basis is closest to the strike (ties → oldest); user may override; the choice is recorded in the event |

---

## 5. Turn and clock

### 5.1 Decision points
| Point | Allowed actions |
|---|---|
| Monday open | Sell puts / covered calls; buy / sell shares |
| Wednesday close | Buy to close; sell new puts / calls (this Friday expiry); buy / sell shares |
| Friday close | Options settle automatically, then share trades only |

### 5.2 Auto-advance
- A Monday sale (or pass) jumps straight to Wednesday close in the same turn.
- "Hold" at Wednesday settles Friday in the same turn; acting at Wednesday executes, then settles Friday.
- Friday pauses for a decision **only when shares are held after settlement**; otherwise it runs straight into next Monday open in the same turn.
- Each day's package is separated by a page-break line: `-----------------`.

### 5.3 Run length
Open-ended; the user closes a run when they choose. Checkpoints at Weeks 26 and 52.

---

## 6. News and sentiment layer

- **Count and timing:** **4 headlines at Monday open, 3 at Friday close.** ALL CAPS, newspaper style.
- **Writer:** code templates decide every fact from the sim's own events (price moves, sentiment shocks, rate meetings, simulated data, earnings); Claude polishes the wording into natural headlines without changing any fact, number or direction.
- **Data rule:** reported data and official decisions are never false. Only opinion can mislead.
- **Time focus:** mostly past (what happened, the shocks that moved sentiment); some forward (scheduled rate meetings, earnings, opinions that may or may not pan out).
- **Mix:** proportions match `market_headlines_nov2-6_2026.txt`: macro, earnings, central banks, politics, global markets, and irrelevant noise.
- **Opinion cues** shift the odds, never guarantee: basis (current data vs. indirect vs. none) and source (neutral vs. positioned). Weights as v1 v3 standard: true opinions basis .55/.25/.20, positioned 15%; misleading opinions basis .20/.45/.35, positioned 40%.
- **Names:** real companies and institutions (the Fed etc.), invented events. Invented events stay ordinary market news (earnings, guidance, products, deals, data, rate decisions), never fabricated scandals or wrongdoing.
- Headlines never name the backdrop or sentiment state and never comment on their own reliability.
- **Reveal:** none. Price and Fear & Greed history are the record.
- **Truth target (decided Nov 6):** opinions are about either the near-term mood (~70%: where hidden sentiment is heading over the next 1–2 weeks, i.e. recovery vs. further slide toward its resting level) or the backdrop (~30%: bull / neutral / bear over the coming months). TRUE opinions point the right way, MISLEADING ones the wrong way. Measured: when the mood is set to recover, the index rose over the next two weeks 73% of the time vs. 36% when it is set to slide; backdrop opinions carry much less near-term information (they speak mostly to crash risk).
- **Signal mix (decided Nov 6):** per set, 0–2 TRUE opinions (25/50/25%) and 0–2 MISLEADING (30/45/25%), with at least one reported item; the rest is reported news, scheduled events and noise.
- **Monthly macro cycle (decided Nov 6):** every 4 sim weeks, a jobs report (Friday of week 1) and a CPI report (Friday of week 3). Prints follow the hidden inflation pressure (which also sets rate odds) and the backdrop, so reading them helps anticipate rate meetings. Rate meetings: the week before, a heads-up; meeting-week Monday, the market's hike/cut odds; meeting Friday, the decision vs. those odds.
- **Monday vs. Friday:** Friday reports the week (weekly move, big days, data, decision); Monday leads with the weekend futures move and anything from last week Friday didn't run.
- Friday results name nothing beyond the headlines and settlement (no regime recap; there is no regime label to reveal).

---

## 7. Bookkeeping

- **Source of truth:** append-only event log per run (`events`: sell, btc, buy_shares, sell_shares, relot, pass, expire, assign, called, interest, rate, split, note). Everything else is derived by replay; nothing is hand-edited.
- **Ledger** (generated): account state, trade log, weekly path, scorecard.
- **Journal:** none.
- **Week P&L table** (every Friday): each trade opened that week (premium in, buy-back out, net), options subtotal, interest, share moves (assignment / mark-to-market / called away / share trades), week total from last Friday's account value to this Friday's, with %.
- **Scorecard:**
  - Weekly premium % of collateral (reported only; no 1% hit/miss target).
  - Win rate = share of trades with a profitable outcome (expired worthless or closed for a profit), with how many / what % were held to expiry.
  - Assignment and called-away counts.
  - An assigned put is judged when its shares exit: put + share lot = one wheel outcome, a win if premiums plus the share sale net positive.

---

## 8. Run management

- **Seed:** random, hidden during play, revealed when the run closes.
- **Blindness:** honor system; the user does not look ahead or look up seeds.
- **One active run at a time;** finish or abandon before starting the next.
- **Replay:** any closed run's seed can be run again on its ruleset, marked as a replay.
- **Saves:** GitHub `flak-daddy/simq-sim`, branch `v2`, pushed once per sim week at Friday close (commit `Run N Week W`); the project gets copies.
- **Closing:** user's call. Abandoned runs are kept and marked (Rule 0).

---

## 9. Reporting and review

- **Benchmarks:** buy-and-hold SimQ (from the run's starting cash at Week 1 Monday open) and cash at the sim rate. The blind put seller is an internal calibration check only.
- **Checkpoints:** Week 26, Week 52, and run close.
- **Charts:** account value vs. benchmarks; weekly premium %.
- **Mentor format:** one-page summary at each checkpoint; at run end, a one-page summary plus a week-by-week workbook.
- **Cross-run:** any runs can be compared, with ruleset differences listed.

---

## 10. Calibration (Milestone 1 gate)

Run over **2,500 simulated years**. Thresholds were written before testing and do not move to fit results.

| # | Test | Pass |
|---|---|---|
| 1 | Days with a move of ±10% or more, average year | 8–12 |
| 2 | Crisis years (20+ days of ±10%, or in-year drawdown worse than −60%) | about 1 in 6–8 years (12.5%–16.7%) |
| 3 | Annualized volatility, typical (non-crisis) year | 55–80% |
| 4 | Median SimQ year | +5% to +15% |
| 5 | Extreme-fear (F&G < 25) spell length, median | 2–5 days |
| 6 | Blind put seller: Monday open, strike 10% below spot (nearest listed strike at or below), sold at bid, held to Friday; edge = premium − payout, % of collateral per week | +0.5% to +1.5% |
| 7 | Simulated F&G mean | 40–55 |
| 8 | Simulated F&G extreme fear (< 25) share of days | 8–20% |
| 9 | Simulated F&G extreme greed (> 75) share of days | 3–10% |
| 10a | Worst single day | no worse than about −35% (−36%) |
| 10b | Days worse than −20% while F&G (at that close) is 25 or above | fewer than 1 per 20 sim years |
| 11a | Monday gap, average absolute | about 2% (1.5–2.5%) |
| 11b | Monday gap after a fear Friday vs. a greed Friday | larger in fear |

Reported only (no threshold): sentiment vs. backdrop share of variance; ±5% / ±15% day frequencies vs. TQQQ; spell lengths for fear (< 45) and extreme greed vs. CNN; reverse-split frequency; rate path distribution; option pricing fit vs. the reference chains (ATM IV, skew, put/call richness, spreads).

**Reference data** (project `claude/data/` and project files):
- TQQQ daily OHLC+volume: 2020, 2022, Aug 31 2023 – Nov 6 2026.
- CNN Fear & Greed, Feb 1 2021 – Nov 5 2026 (1,448 unique days after dropping the duplicated last row): mean 47.0, extreme fear 13.5% of days, extreme greed 5.5%; extreme-fear spells median 2–3 days (max 20); extreme-greed median 4 (max 26); fear (< 45) median 6 (max 51).
- Reference chains as in §2.5.

Note: 8–12 big days on average with crises 1 in 6–8 years means normal years carry about 5–9, a bit rougher than 2024–2025 (2–7).

**Threshold revisions (user, Nov 6, 2026, during calibration):** test 6 was 0% to +0.15%; at real-chain IV with a price path matching real TQQQ weekly moves a blind seller earns far more, so the user kept real IV and moved the band to +0.5% to +1.5%. Test 10 was "essentially never"; the user set the measurable form in 10b.

**Output:** `calibration/report-v2.0.md` (all tests, values, pass/fail, reported-only figures) saved next to the ruleset. No run starts until every test passes.

---

## 11. Interface

- Played in chat with Claude: code runs the sim; Claude relays output and polishes headlines only.
- **Verbosity:** script output only; Claude adds no commentary and answers questions only when asked.
- **Monday open order:** account (share value, cash available, total) → headlines → indicators (Fear & Greed, Sim-tastic Oscillator) → position (available cash, held lots) → chain.
- **Wednesday close:** Mon–Wed bars, indicators, buy-to-close price per open position, chain.
- **Friday close:** Thu–Fri bars, settlement, interest, rate decision if a meeting week, headlines, indicators, account, scorecard line, Week P&L table.
- **Input slips:** selling a call with no shares, or "buying" an option to open → not executed; ask what was meant. Puts that exceed collateral → say so.

### Repo layout (`v2` branch)
```
SPEC.md                 this file
rulesets/               ruleset-v2.N.json
simq/                   engine package: market, sentiment, fg (Fear & Greed), osc, rates, pricing, chain, account, headlines, report
calibration/            calibration runner + report-v2.N.md
data/                   reference data (TQQQ, CNN F&G, chains)
runs/run-NNN/           save file (ruleset + event log), ledger, checkpoint reports
cli.py                  play commands
```

---

## 12. Fear & Greed index + Sim-tastic Oscillator

### 12.1 Fear & Greed (simulated, CNN-style 0–100)
- The hidden sentiment drives the market (§1); the gauge reflects it, computed from simulated market data like the real CNN index.
- **5 components**, each 0–100 and shown with its own reading:
  1. Momentum (SimQ vs. its 125-day average)
  2. Volatility (current IV vs. its 50-day average)
  3. Put/call demand
  4. Safe-haven demand
  5. Breadth
- Score = average of the 5, smoothed asymmetrically: it falls fast (weight 0.80 on a lower reading) and recovers slowly (0.25), like the real index on crash days. **Close but noisy:** tracks the true mood with lag and measurement noise and can mislead at turning points (e.g. extreme fear near bottoms).
- Labels: extreme fear < 25, fear 25–44, neutral 45–55, greed 56–75, extreme greed > 75.
- **Display:** today's reading with a text bar, plus the last 10 days as a number row, with each component, at every decision point (decided Nov 6: both).

### 12.2 Sim-tastic Oscillator (lite stochastic)
- %K over 14 days from daily highs, lows, closes; %D = 3-day average of %K.
- Zones: oversold < 20, overbought > 80, otherwise neutral.
- **Display:** %K (with a text bar), %D and zone label today, plus %K and %D number rows for the last 10 days, at every decision point.

---

## Build plan

1. **Spec** (this file) committed to `v2`. Doubles as the template for `ruleset-v2.0.json`.
2. **Milestone 1 — engine + calibration report:** market (§1), Fear & Greed (§12.1), oscillator (§12.2), rates (§2.6), pricing (§2), calibration runner (§10). Hard gate.
3. **Playable layers:** account/trading (§4), clock (§5), chain display (§3), headlines (§6), bookkeeping (§7), run management (§8), reporting (§9).

Commits land as milestones complete during the build; during play, one push per sim week at Friday close.
