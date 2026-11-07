# SimQ calibration report — ruleset v2.0

Generated 2026-11-06 by `python3 -m calibration.report v2.0`. 2,500 scored simulated years (100 paths x 25 years after a 1-year warm-up), seed 20261106, 31 s.

**Gate: PASS — every test passes; the ruleset is frozen.**

## Pass/fail tests (SPEC §10)

| # | Test | Result | Pass band | |
|---|---|---|---|---|
| 1 | Days moving +/-10% or more, average year | 8.95 | 8-12 | PASS |
| 2 | Crisis years (20+ big days or drawdown < -60%) | 13.88% | 12.5%-16.7% | PASS |
| 3 | Annualized vol, typical (non-crisis) year, median | 67.97% | 55%-80% | PASS |
| 4 | Median SimQ year | 7.80% | +5% to +15% | PASS |
| 5 | Extreme-fear spell length, median (days) | 4.00 | 2-5 | PASS |
| 6 | Blind put, Monday 10% below, edge %/week | 0.66% | +0.5% to +1.5% | PASS |
| 7 | Simulated F&G mean | 47.05 | 40-55 | PASS |
| 8 | F&G extreme fear share of days | 12.80% | 8%-20% | PASS |
| 9 | F&G extreme greed share of days | 5.19% | 3%-10% | PASS |
| 10a | Worst single day | -35.16% | >= about -35% (-36%) | PASS |
| 10b | Days worse than -20% with F&G >= 25, per 20 years | 0.52 | < 1 | PASS |
| 11a | Monday gap, average absolute | 2.16% | 1.5%-2.5% | PASS |
| 11b | Monday gap larger in fear than greed | 0.64% | > 0 | PASS |

Two thresholds were revised by the user on Nov 6, 2026, during calibration, after first runs showed the original wording could not be met as intended (see SPEC §10 and the checklist):
- Test 6 was 0% to +0.15%. At real-chain IV levels with a price path that matches real TQQQ weekly moves, a blind seller earns well above that; the user chose to keep real IV and move the band to +0.5% to +1.5%.
- Test 10 said −20% days outside extreme fear should 'essentially never' happen; the user set the measurable form: fewer than one such day per 20 sim years (gauge at 25 or above at that close).

## Blind put seller (internal check; not a reported benchmark)

Edge = bid premium − payout at Friday close, as % of collateral per week. Strike = nearest listed strike at or below the stated distance.

| Sold | Mean | Weekly sd | Worst week | 1st percentile |
|---|---|---|---|---|
| mon 10% below | +0.659% | 2.34% | -46.9% | -10.3% |
| mon 5% below | +0.820% | 3.56% | -48.5% | -13.9% |
| mon 15% below | +0.406% | 1.49% | -44.5% | -5.4% |
| wed 5% below | +0.301% | 1.91% | -39.6% | -8.4% |
| wed 10% below | +0.132% | 1.08% | -37.5% | -3.9% |

## Reported only (no threshold)

### Price path vs. real TQQQ

| Series | Ann. vol | ±5% days/yr | ±10% days/yr | ±15% days/yr | Worst day |
|---|---|---|---|---|---|
| TQQQ 2020 (crisis) | 104% | 78.0 | 26.0 | 10.0 | -34.5% |
| TQQQ 2022 (crisis) | 96% | 103.8 | 22.2 | 2.0 | -16.5% |
| TQQQ Aug 2023 - Nov 2026 | 61% | 38.2 | 4.4 | 1.3 | -18.9% |
| SimQ, all years | typical-year 68% (mean) | 53.5 | 9.0 | 2.1 | -35.2% |

- SimQ year: 10th pct -38%, median +7.8%, 90th pct +67%; 58% of years finish up; median in-year drawdown -44%.
- Days worse than −20%: 0.26 per year; on the worst day of all, F&G read 4.
- Monday gap: 2.47% after a fear Friday (F&G < 45) vs 1.83% after a greed Friday (> 55).
- Reverse splits (close < $2.50): 2 in 2,500 years.

### Fear & Greed vs. CNN 2021–2026

| | CNN | SimQ |
|---|---|---|
| Mean | 47.0 | 47.1 |
| Extreme fear share | 13.5% | 12.8% |
| Extreme greed share | 5.5% | 5.2% |
| Extreme-fear spell, median / max | 2 / 20 days | 4 / 63 days (99th pct 29) |
| Extreme-greed spell, median / max | 4 / 26 days | 3 / 33 days |
| Fear (< 45) spell, median / max | 6 / 51 days | 6 days |
| Span | 1,448 days | 2,500 years |

SimQ maxima come from 2,500 years against CNN's ~6, so longer single extremes are expected; the 99th percentile shows how rare they are.

### Sentiment vs. backdrop

Share of daily underlying-return variance explained by the backdrop's pull on drift: 1.0%; sentiment and shocks: 99.0%. (Intent: sentiment clearly dominates. No threshold.)

### Central bank

Rate across scored years: mean 3.41%, range 1.00%–7.00% (bounds 1%–8%, start 3.50%).

### Option pricing vs. reference chains

Stressed: Nov 6, 2026 close, Nov 13 expiry (5 days), spot $52.25, model ATM IV 101%, F&G 20.

| Strike | Model bid/ask | Model IV | Real |
|---|---|---|---|
| 45P | 0.87 / 0.94 | 123% | 45P ≈ $0.89 |
| 50P | 2.02 / 2.15 | 108% |  |
| 52.5C | 2.75 / 2.93 | 100% |  |
| 55C | 1.58 / 1.69 | 92% |  |
| 60C | 0.28 / 0.31 | 77% | 60C ≈ $0.31 |
| 65C | 0.01 / 0.03 | 62% | a few cents |

Calm: Oct 23, 2026 close, spot $66.29 (v1 snapshot 1). 1-day expiry, model ATM IV 83%:

| Strike | Model bid/ask | Real bid/ask |
|---|---|---|
| 59P | 0.05 / 0.07 | 0.05 / 0.07 |
| 60P | 0.09 / 0.11 | 0.08 / 0.10 |
| 62P | 0.24 / 0.27 | 0.23 / 0.26 |
| 64P | 0.57 / 0.62 | 0.57 / 0.62 |
| 66P | 1.21 / 1.29 | 1.22 / 1.28 |
| 67C | 1.00 / 1.07 | 1.00 / 1.05 |
| 68C | 0.61 / 0.67 | 0.59 / 0.63 |
| 70C | 0.16 / 0.19 | 0.16 / 0.17 |
| 72C | 0.02 / 0.04 | 0.03 / 0.04 |

5-day expiry, model ATM IV 82% (real IVs from v1 snapshot 1b):

| Strike | Model IV | Real IV |
|---|---|---|
| 60P | 92.1% | 92% |
| 62P | 88.9% | 88% |
| 65P | 84.1% | 84% |
| 66P | 82.5% | 82% |
| 67C | 80.9% | 79% |
| 70C | 76.0% | 74% |
| 72C | 72.8% | 71% |
| 73C | 71.2% | 70% |

IV level is set by sentiment so that 5-day ATM IV / forward realized vol runs about 1.05 in extreme fear to 1.30 in greed (v1's real-chain ratios). SimQ's calm stretches move less than TQQQ did in Oct 2026, so calm SimQ ATM IV (about 55–65%) sits below that day's real 82% while keeping the real ratio.

## Independent recheck

Big days, crisis rate, typical-year vol, median year, worst day, F&G shares, Monday gap and the blind put edge were recomputed with separately written loop code and its own Black-Scholes; all matched (blind edge on a 1-in-5 path subsample +0.68% vs +0.66% full).

