# SimQ market calibration notes (from real TQQQ chains)

## Snapshot 1a: Fri Oct 23, 2026 close, TQQQ $66.29, expiry Mon Oct 26 (1 trading day)
(Corrected: I first assumed Oct 30; the user confirmed this chain was the 26th, so all vols below use T = 1 day.) Mids are bid/ask midpoints; IV backed out with the SimQ Black-Scholes (4% rate).

| Strike | Side | Bid/Ask | Spread | Implied vol |
|---|---|---|---|---|
| 59 | P | 0.05/0.07 | 0.02 | 103.6% |
| 60 | P | 0.08/0.10 | 0.02 | 98.7% |
| 61 | P | 0.14/0.16 | 0.02 | 96.3% |
| 62 | P | 0.23/0.26 | 0.03 | 94.1% |
| 63 | P | 0.37/0.40 | 0.03 | 91.6% |
| 64 | P | 0.57/0.62 | 0.05 | 89.6% |
| 65 | P | 0.86/0.91 | 0.05 | 87.5% |
| 66 | P | 1.22/1.28 | 0.06 | 83.9% |
| 67 | C | 1.00/1.05 | 0.05 | 80.4% |
| 68 | C | 0.59/0.63 | 0.04 | 76.2% |
| 69 | C | 0.32/0.35 | 0.03 | 73.3% |
| 70 | C | 0.16/0.17 | 0.01 | 70.9% |
| 71 | C | 0.07/0.08 | 0.01 | 69.3% |
| 72 | C | 0.03/0.04 | 0.01 | 69.5% |
In-the-money options were wide and stale (e.g. 62 call 3.95/5.20), so only OTM sides were used.


## Snapshot 1b: same close, expiry Fri Oct 30 (5 trading days), user screenshots
OTM-side implied vols (T = 5 days), clean quotes: 60 put 92%, 62 put 88%, 65 put 84%, 66 put 82%, 67 call 79%, 70 call 74%, 72 call 71%, 73 call 70%. Many strikes (especially .5 strikes and stale ones) had erratic, much wider quotes (e.g. 64 put 1.80/2.20, 73.5 call 0.16/0.71); SimQ stays idealized and does not model those.
ATM straddle vol: 83% (1-day) and 82% (5-day).

## Findings (snapshot 1)
- Spreads: least-squares fit on the 22 clean quotes (under 12% wide) from both chains: spread = 0.013 + 0.054 x mid. **Applied (v2, kept in v3):** spread = max(0.01, 0.01 + 0.05 x mid), centered on mid, rounded to cents (about 0.02 at $0.15, 0.05 at $0.9, 0.08 at $1.4, 0.15 at $3). Spreads depend on the option's price, so they shrink in dollars automatically as expiry approaches and premium decays. Run 1 uses v1 (0.06 x mid + 0.02) through Week 12 and v2 from Week 13; Run 2 uses v2 from Week 1. v1 was only ~20-35% wider than v2 for mids above $1, and ~40-60% wider for cheap options.
- Skew: **Applied (pricing v2, kept in v3).** Each strike's IV = ATM IV x clamp(1 - 1.3 x (K/S - 1), 0.6, 1.5). Reproduces the 5-day chain: puts about +12% at -10% strike (92% vs 82%), calls about -11% at +8.6% (72% vs 82%). Confirmed against the volatile stretch in snapshot 2.
- IV level: **Applied (pricing v2; superseded by v3 for new runs, see below).** Baselines raised to calm_up 62%, chop 75%, rebound 90%, selloff 102%, crash 125% (were 50/58/68/72/90), with a down-day bump of 3.0 x loss (was 2.5). Price paths and regimes are unchanged; only option prices change.
- Versioning: Run 1 uses v1 pricing through Week 12 and v2 (IV level, skew, spreads) from Week 13; Run 2 uses v2 from Week 1 (state fields `pricing_v2_from`, `spread_v2_from`). Runs created from Oct 24, 2026 use v3 (state field `pricing`).

## Snapshot 2: volatile 4-week stretch, March 2 - March 31, 2026 (pricing v3)
Source: optionsanalysissuite.com TQQQ daily history (Mar 2026 page; Apr 1-2 and Oct 5-23, 2026 pages for context); news context from ts2.tech / stockti.com (Mar 27, 2026: Nasdaq Composite about 11% off its October high, TQQQ near $40, oil above $110, 10-year near 4.47%). Option IVs here are the site's ATM / 25-delta figures (about 30-day), not weekly chains.
- TQQQ fell from $49.66 (Mar 2) to $37.63 (Mar 30), about -24%, closing the month at $41.69. Worst stretch: Mar 25-30 (-15% in three sessions).
- ATM IV: 62-87% (average 72%); peaks of about 80-87% on the sharpest down days (Mar 13, 20, 26, 27, 30).
- 20-day realized vol rose from about 47-57% to 72% by Mar 31. Average IV across the month (72%) was about equal to the realized vol of the month itself (72%): in a sharp selloff, implied vol carried little or no premium over what actually happened.
- Skew: 25-delta put minus call about 25-30 vol points (Apr 1-2: put 83%, ATM 71%, call 58%, so put = ATM x 1.18, call = ATM x 0.82). SimQ's v2 skew gives x1.16 / x0.81 at the matching strikes, so skew is unchanged in v3.
- Calm comparison (Oct 5-21, 2026): ATM IV 53-64% vs 20-day realized 50-55%, about 1.1-1.15x for 30-day options; the Oct 23 weekly chain (snapshot 1) showed 82% vs 63% realized, about 1.3x.

## Finding and change: pricing v3 (standard for new runs from Oct 24, 2026)
v2 set implied vol from the real chain's level, but SimQ's calm regimes move less than real TQQQ, so v2 calm/chop puts were rich relative to SimQ's own moves (calm_up IV about 1.5x its realized vol), while volatile regimes were closer to real. A blind put seller earned about +0.2% of collateral per week under v2, with large positive edges in calm/rebound weeks.
v3 sets each regime's IV relative to its own realized vol (3 x daily sigma x sqrt(252): calm_up 43%, chop 62%, selloff 95%, crash 114%, rebound 86%) using the real ratios above: about 1.3x in calm/chop (weekly options carry extra premium), about 1.05x in selloff/crash, about 1.15x in rebound. Baselines: calm_up 54%, chop 75%, selloff 92%, crash 105%, rebound 95% (down-day bump 3.0 x loss, skew and spreads as v2).
Monte Carlo check (300 random 52-week markets, put held to Friday, edge = bid premium minus payout, % of collateral per week):

| Put | v1 | v2 | v3 |
|---|---|---|---|
| Monday, 10% below spot | -1.10% | +0.20% | -0.05% |
| Monday, 15% below spot | -0.78% | +0.20% | +0.01% |
| Wednesday, 10% below spot | -0.32% | +0.19% | +0.09% |
| Wednesday, 15% below spot | -0.16% | +0.08% | +0.02% |

Under v3 a seller who ignores the market roughly breaks even: positive in calm/chop/rebound weeks, negative in selloff/crash weeks. Any lasting edge has to come from reading the market and managing trades.
Versioning: state field `pricing` ("v3" for runs created from Oct 24, 2026; absent = v2 behaviour, so Runs 1-2 replay unchanged). Price paths and regimes are identical across v1/v2/v3; only option prices differ.
Limits: snapshot 2 uses third-party 30-day IV summaries, not a full weekly chain. If a weekly chain from a volatile day becomes available, add it as snapshot 3.

## Check: regime label vs. weekly direction (Oct 25, 2026, after Run 3)
Question: Run 3 had 11 of 41 directional weeks (calm_up, rebound, selloff, crash) close against their label (e.g. W46 rebound -9.1%, W42 selloff +5.2%, W7 calm_up -14.7%). Bug or design?
Monte Carlo of simq.gen_week's weekly draw (40,000 weeks per regime, no code changes):

| Regime | Mean week | Weekly sd | Weeks against label | Weeks moving >10% |
|---|---|---|---|---|
| calm_up | +1.7% | 6.1% | 38% | 10% |
| chop | -0.2% | 8.7% | n/a | 22% |
| selloff | -7.4% | 12.6% | 25% | 50% |
| crash | -11.7% | 14.7% | 19% | 63% |
| rebound | +10.7% | 13.1% | 19% | 55% |

Finding: not a bug. A regime sets the week's drift and volatility, not its result; one week of noise is several times the drift, so roughly 1 in 4 directional weeks should end against the label. Run 3's 27% (11/41) is in line. Real leveraged-ETF weeks behave similarly (a calm uptrend still has many down weeks; bear markets have sharp up weeks). Thinner tails for calm regimes (t df 10 instead of 4) were tested and barely change this (calm_up down weeks 39% -> 40%), so no change was made. Making labels match outcomes more often would need less noise or more drift per regime, which would make the sim easier and less realistic.

## Market v2: regime transitions with an upward drift (Oct 25, 2026, after Run 4; standard from Run 5)
Question (user, after Run 4): is it bad luck that runs keep hitting major crashes, or does the model lean that way?
Finding: the model leaned that way. Under the original transition table (market v1), the long-run regime mix was calm_up 30%, chop 26%, selloff 22%, rebound 12%, crash 9%, which drifts the unleveraged index about -15%/yr. With 3x leverage and volatility drag, SimQ's median year was about -58%, only about 1 year in 6 finished up, 87% of years had a drawdown worse than -50%, and the average year had 4.7 crash weeks. Selloffs were sticky: from a selloff, the next week was selloff or crash 50% of the time and calm_up only 5%. Runs 1, 3 and 4 (-57% by W26, -43%, -86%) were typical draws; Run 2 (+1%) was the lucky one. Real TQQQ has had years like that (2022 about -79%), but its long-run drift is positive because the Nasdaq-100 under it trends up.

Change (market v2): only the transition odds change. Each regime's drift, volatility, implied vol, skew and spreads are untouched, so a selloff or crash week looks exactly as it did; they just come less often, and dips draw buyers (selloff -> rebound .30, crash -> rebound .55, selloff -> selloff .20).

| From \ to | calm_up | chop | selloff | crash | rebound |
|---|---|---|---|---|---|
| calm_up | .68 (.55) | .20 (.25) | .08 (.15) | .02 (.03) | .02 (.02) |
| chop | .43 (.30) | .33 (.35) | .14 (.25) | .03 (.05) | .07 (.05) |
| selloff | .12 (.05) | .30 (.25) | .20 (.30) | .08 (.20) | .30 (.20) |
| crash | .00 (.00) | .15 (.10) | .20 (.30) | .10 (.20) | .55 (.40) |
| rebound | .50 (.35) | .25 (.25) | .10 (.15) | .02 (.05) | .13 (.20) |
(v1 values in parentheses.)

Monte Carlo, 8,000 random 52-week years each:

| | Market v1 | Market v2 |
|---|---|---|
| Regime mix (calm_up / chop / selloff / crash / rebound) | 30 / 26 / 22 / 9 / 13% | 52 / 25 / 11 / 3 / 9% |
| Unleveraged index drift | about -15%/yr | about +11%/yr |
| SimQ median year | about -58% | about +4% (target was about +5%) |
| SimQ 10th / 90th percentile year | -88% / +30% | -60% / +155% |
| Years finishing up | 17% | 53% |
| Median worst drawdown within the year | -74% | -50% |
| Years with a drawdown worse than -50% | 87% | 49% |
| Crash weeks per year | 4.7 | 1.7 |
| Selloff weeks per year | 11.6 | 6.0 |

The SimQ target is about +5% for the median year, deliberately below real TQQQ's history: SimQ's selloff and crash weeks are very volatile (weekly sd 13-15%), so volatility drag eats much of an +11% index drift. Bad years remain common (1 in 10 is -60% or worse).

Effect on the pricing-v3 put-seller check (tools/pricing-review/market_v2.py, 300 years each, put held to Friday, bid premium minus payout, % of collateral per week):

| Put | Market v1 | Market v2 |
|---|---|---|
| Monday, 10% below spot | -0.13% | +0.36% |
| Monday, 15% below spot | -0.03% | +0.21% |
| Wednesday, 10% below spot | +0.03% | +0.10% |
| Wednesday, 15% below spot | -0.00% | +0.02% |

Per-regime edges are unchanged (Monday 15% put under v2: calm_up +0.41%, chop +0.53%, rebound +1.21%, selloff -1.19%, crash -3.61%); the blind-seller edge turns positive only because calm and rebound weeks are now more common. That is the real-world variance risk premium showing up in a rising market, but it does make blind put selling profitable on average (about +0.2-0.4% of collateral per week on Mondays). Whether to trim calm/chop implied vol to restore a near-zero blind edge is an open decision (it would be a pricing v4, separate from market v2). Decision (user, Oct 26, 2026): keep pricing v3 for Run 5; ask again after Run 5 closes. Decided after Run 5 (user, Oct 26, 2026): no pricing v4. The user considers the spread fair over the long haul, so pricing v3 stays the standard.

Versioning: state field `market` ("v2" written by `simbook.py new` from Run 5; absent = v1, so Runs 1-4 replay unchanged, verified byte-for-byte on ledgers, journals, status and week P&L). `simq.py` standalone commands (meta/open/mid/fri) default to v1.


## Market v3: two transition rows adjusted (Oct 26, 2026, after Run 5; standard from Run 6)

Change (user, after Run 5): crash -> rebound .55 -> .45, with the freed .10 going to crash -> chop (.15 -> .25); selloff -> rebound .30 -> .35, taken from selloff -> chop (.30 -> .25). crash -> crash (.10) and selloff -> selloff (.20) unchanged, as are all other rows and every regime's drift, volatility, implied vol, skew and spreads.

| From \ to | calm_up | chop | selloff | crash | rebound |
|---|---|---|---|---|---|
| selloff | .12 | .25 (.30) | .20 | .08 | .35 (.30) |
| crash | .00 | .25 (.15) | .20 | .10 | .45 (.55) |
(v2 values in parentheses; other rows as in market v2.)

Monte Carlo (tools/pricing-review/market_v3.py; 8,000 years for the distribution, 300 for the put edge):

| | Market v2 | Market v3 |
|---|---|---|
| Regime mix (calm_up / chop / selloff / crash / rebound) | 51 / 25 / 11 / 3 / 9% | 51 / 25 / 11 / 3 / 9% |
| SimQ median year | +7.0% | +7.7% |
| SimQ 10th / 90th percentile | -60.0% / +164.5% | -59.8% / +165.0% |
| Years finishing up | 54% | 54% |
| Crash / selloff weeks per year | 1.6 / 5.9 | 1.7 / 6.0 |
| Median worst in-year drawdown | -52% | -52% |
| Blind Monday put 10% / 15% below spot (edge, % collateral/week) | +0.36% / +0.21% | +0.37% / +0.22% |

The two rows only apply in the week after a crash or selloff (about 14% of weeks), so the annual statistics barely move; the differences above are within simulation noise. The effect is on the shape of recoveries: after a crash, chop is now more likely and an immediate rebound less likely; after a selloff, a rebound is a little more likely.

Versioning: state field `market` = "v3" is written by `simbook.py new` from Run 6. Run 5 keeps "v2" and Runs 1-4 have no field (v1); replays of Runs 2-5 were verified byte-for-byte on ledgers and journals after the change. (Run 1's stored ledger already differed from a fresh render before this change, in the midweek ask shown for held positions, because Run 1 predates the pricing fields; fills are stored and unaffected.)


## Realism check (Oct 26, 2026, after Run 5)

Full write-up: simq-realism-report.txt (internal stats from tools/pricing-review/realism_internal.py, market v3 + pricing v3, against published TQQQ, QQQ and Cboe put-write figures). Findings: calm-week IV/realized ratio 1.25x is in line with real TQQQ (1.12x on 30-day options, about 1.3x on weeklies); crash/selloff ratios 0.93-0.96x are richer for sellers than real TQQQ in May 2022 (about 0.81x). The price path is harsher than TQQQ history (median year +8% vs +57% in 2010-2025; drawdowns worse than -50% in 54% of years vs about 25%). Blind-wheel Sharpe about 0.4 vs real S&P put-write indexes 0.5-0.67. The blind edge vanishes if all IVs fall about 13%, or calm/chop IVs about 20%.


## Spread and far-OTM premium review (Oct 26, 2026, after Run 5)

Full write-up: simq-spread-skew-review.txt (tools/pricing-review/spread_skew_check.py). Spreads match the real Oct 23 chain (total width 0.45 vs real 0.43 over 14 strikes) and cost about 6% of premium in Run 5: no change. The linear put skew matches real 5-day quotes to about 10% below spot but is thin beyond (real 30-day 10-delta put ATM + 29.9 pts vs SimQ + 24.7; real 1-day IV up to 8.7 pts above SimQ at -11%). Candidate fixes (not adopted, user to decide): put-wing term + C x (1 - K/S)^2 with C 0.7-1.0, short-expiry skew scaling (5 / days)^0.33, selloff/crash IV trim of 8%, $0.65/contract commissions, and messy quotes on .5 strikes.
