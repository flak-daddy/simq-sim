# SimQ Run 1 Ledger

- Seed: 20261022 (path reseeded from Week 13; see state file) | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-001-journal.md

## Current state (Week 18, Monday open)
- SimQ spot: $48.54
- Cash: $7,674.11 | locked collateral: $0.00 | free: $7,674.11
- Shares: 0
- Open positions: none
- Premium collected (gross): $579.00 | buy-to-close costs: $22.00 | interest: $67.11
- Realized P&L (options net of buy-backs + stock sales): +$107.00 (options +$557.00, stock -$450.00)
- Account value: $7,674.11 (+2.32% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P57 | W1 mid | $57 | 0.24 / 0.27 | $24.00 | $5,700.00 cash | Expired worthless (Fri SimQ 58.24) | premium 0.42% of collateral |
| 2 | SIMQ-W02-P52.5 | W2 open | $52.5 | 0.65 / 0.71 | $65.00 | $5,250.00 cash | ASSIGNED: bought 100 at $52.50 (Fri SimQ 45.88) | premium 1.24% of collateral; held at midweek (ask 5.06) |
| 3 | SIMQ-W03-C54 | W3 mid | $54 | 0.42 / 0.47 | $42.00 | lot 1 | Expired worthless (Fri SimQ 39.40) | premium 0.84% of share value |
| 4 | SIMQ-W05-C52 | W5 open | $52 | 0.24 / 0.28 | $24.00 | lot 1 | Expired worthless (Fri SimQ 43.77) | premium 0.52% of share value; held at midweek (ask 0.03) |
| 5 | SIMQ-W06-C48 | W6 open | $48 | 0.52 / 0.57 | $52.00 | lot 1 | Bought to close at 0.01 ($1.00), net +$51.00 | premium 1.19% of share value |
| 6 | SIMQ-W07-C40 | W7 open | $40 | 0.52 / 0.57 | $52.00 | lot 1 | Bought to close at 0.01 ($1.00), net +$51.00 | premium 1.44% of share value |
| 7 | SIMQ-W09-C46 | W9 open | $46 | 0.19 / 0.22 | $19.00 | lot 1 | Bought to close at 0.20 ($20.00), net -$1.00 | premium 0.47% of share value |
| 8 | SIMQ-W10-C48 | W10 open | $48 | 0.16 / 0.19 | $16.00 | lot 1 | CALLED AWAY: sold 100 at $48.00 (Fri SimQ 49.64) | premium 0.36% of share value; held at midweek (ask 0.19) |
| 9 | SIMQ-W11-P47 | W11 open | $47 | 0.34 / 0.39 | $34.00 | $4,700.00 cash | Expired worthless (Fri SimQ 48.76) | premium 0.72% of collateral; held at midweek (ask 0.11) |
| 10 | SIMQ-W12-P46 | W12 open | $46 | 0.56 / 0.61 | $56.00 | $4,600.00 cash | Expired worthless (Fri SimQ 47.04) | premium 1.22% of collateral; held at midweek (ask 0.55) |
| 11 | SIMQ-W13-P44 | W13 open | $44 | 0.35 / 0.39 | $35.00 | $4,400.00 cash | Expired worthless (Fri SimQ 46.43) | premium 0.80% of collateral; held at midweek (ask 0.20) |
| 12 | SIMQ-W14-P43.5 | W14 open | $43.5 | 0.29 / 0.33 | $29.00 | $4,350.00 cash | Expired worthless (Fri SimQ 45.58) | premium 0.67% of collateral; held at midweek (ask 0.15) |
| 13 | SIMQ-W15-P43.5 | W15 open | $43.5 | 0.47 / 0.52 | $47.00 | $4,350.00 cash | Expired worthless (Fri SimQ 47.33) | premium 1.08% of collateral; held at midweek (ask 0.06) |
| 14 | SIMQ-W16-P45 | W16 open | $45 | 0.44 / 0.49 | $44.00 | $4,500.00 cash | Expired worthless (Fri SimQ 49.07) | premium 0.98% of collateral; held at midweek (ask 0.06) |
| 15 | SIMQ-W17-P46.5 | W17 open | $46.5 | 0.40 / 0.44 | $40.00 | $4,650.00 cash | Expired worthless (Fri SimQ 48.54) | premium 0.86% of collateral; held at midweek (ask 0.51) |

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W2 at $52.50 | W10 at $48.00 | -$450.00 | -$202.00 |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | selloff | 63.80 | 61.75 | 58.60 | 61.00 | 60.79 | 58.24 | -8.7% | 5.76 (7,500.00 x 3d; 7,524.00 x 4d) |
| 2 | selloff | 58.24 | 58.34 | 56.41 | 48.05 | 47.03 | 45.88 | -21.2% | 4.68 (7,594.76 x 5d; 2,344.76 x 2d) |
| 3 | crash | 45.88 | 53.79 | 51.53 | 49.95 | 37.97 | 39.40 | -14.1% | 1.82 (2,349.44 x 3d; 2,391.44 x 4d) |
| 4 | rebound | 39.40 | 41.84 | 40.53 | 42.12 | 42.16 | 46.26 | +17.4% | 1.84 (2,393.26 x 7d) |
| 5 | selloff | 46.26 | 43.83 | 45.72 | 45.81 | 44.48 | 43.77 | -5.4% | 1.86 (2,419.10 x 7d) |
| 6 | crash | 43.77 | 41.34 | 38.59 | 37.93 | 36.07 | 36.13 | -17.5% | 1.90 (2,472.96 x 3d; 2,471.96 x 4d) |
| 7 | rebound | 36.13 | 37.26 | 32.14 | 34.36 | 35.72 | 38.13 | +5.5% | 1.94 (2,525.86 x 3d; 2,524.86 x 4d) |
| 8 | rebound | 38.13 | 40.48 | 42.38 | 41.29 | 40.82 | 40.72 | +6.8% | 1.94 (2,526.80 x 7d) |
| 9 | calm_up | 40.72 | 40.34 | 43.39 | 44.14 | 43.73 | 44.60 | +9.5% | 1.95 (2,547.74 x 3d; 2,527.74 x 4d) |
| 10 | calm_up | 44.60 | 45.08 | 45.71 | 45.83 | 47.79 | 49.64 | +11.3% | 3.00 (2,545.69 x 5d; 7,345.69 x 2d) |
| 11 | calm_up | 49.64 | 49.70 | 49.25 | 49.81 | 50.43 | 48.76 | -1.8% | 5.66 (7,382.69 x 7d) |
| 12 | calm_up | 48.76 | 48.51 | 47.68 | 46.93 | 47.50 | 47.04 | -3.5% | 5.71 (7,444.35 x 7d) |
| 13 | calm_up | 47.04 | 44.92 | 44.99 | 45.76 | 46.21 | 46.43 | -1.3% | 5.74 (7,485.06 x 7d) |
| 14 | calm_up | 46.43 | 46.71 | 46.74 | 45.97 | 45.37 | 45.58 | -1.8% | 5.77 (7,519.80 x 7d) |
| 15 | calm_up | 45.58 | 46.26 | 46.19 | 46.68 | 47.38 | 47.33 | +3.8% | 5.81 (7,572.57 x 7d) |
| 16 | calm_up | 47.33 | 47.50 | 48.70 | 48.50 | 48.96 | 49.07 | +3.7% | 5.85 (7,622.38 x 7d) |
| 17 | calm_up | 49.07 | 48.98 | 49.43 | 47.67 | 46.38 | 48.54 | -1.1% | 5.88 (7,668.23 x 7d) |

## Scorecard
- 15 trades: 10 expired worthless, 2 closed for profit, 1 closed at a loss, 1 assigned, 1 called away | win rate 67% (80% counting profitable closes)
- Avg put premium: 0.89% of collateral
- Avg call premium: 0.80% of share value at sale
- Wheel cycles completed (shares called away): 1
- Account value at week 26 (comparison metric): pending
