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
