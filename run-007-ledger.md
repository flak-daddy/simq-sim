# SimQ Run 7 Ledger

- Seed: 104391084 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-007-journal.md

## Current state (Week 11, Monday open)
- SimQ spot: $35.00
- Cash: $3,314.42 | locked collateral: $0.00 | free: $3,314.42
- Shares: 100 SimQ bought at $46.00 in Week 4; effective basis $44.50 after option premiums
- Open positions: none
- Premium collected (gross): $396.00 | buy-to-close costs: $19.00 | interest: $37.42
- Realized P&L (options net of buy-backs + stock sales): +$377.00 (options +$377.00, stock +$0.00)
- Account value: $6,814.42 (-9.14% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56.5 | W1 open | $56.5 | 0.60 / 0.64 | $60.00 | $5,650.00 cash | Bought to close at 0.09 ($9.00), net +$51.00 | premium 1.06% of collateral |
| 2 | SIMQ-W01-P60 | W1 mid | $60 | 0.25 / 0.28 | $25.00 | $6,000.00 cash | Expired worthless (Fri SimQ 60.98) | premium 0.42% of collateral |
| 3 | SIMQ-W02-P53 | W2 open | $53 | 0.55 / 0.59 | $55.00 | $5,300.00 cash | Bought to close at 0.06 ($6.00), net +$49.00 | premium 1.04% of collateral |
| 4 | SIMQ-W03-P52.5 | W3 open | $52.5 | 0.25 / 0.27 | $25.00 | $5,250.00 cash | Expired worthless (Fri SimQ 52.70) | premium 0.48% of collateral; held at midweek (ask 1.66) |
| 5 | SIMQ-W04-P46 | W4 open | $46 | 0.55 / 0.59 | $55.00 | $4,600.00 cash | ASSIGNED: bought 100 at $46.00 (Fri SimQ 43.39) | premium 1.20% of collateral; held at midweek (ask 1.57) |
| 6 | SIMQ-W05-C46.5 | W5 open | $46.5 | 0.94 / 1.00 | $94.00 | lot 1 | Expired worthless (Fri SimQ 39.90) | premium 2.17% of share value; held at midweek (ask 0.13) |
| 7 | SIMQ-W06-C47 | W6 open | $47 | 0.02 / 0.03 | $2.00 | lot 1 | Bought to close at 0.01 ($1.00), net +$1.00 | premium 0.05% of share value |
| 8 | SIMQ-W06-P30 | W6 open | $30 | 0.03 / 0.04 | $3.00 | $3,000.00 cash | Expired worthless (Fri SimQ 40.92) | premium 0.10% of collateral; held at midweek (ask 0.01) |
| 9 | SIMQ-W09-P22 | W9 open | $22 | 0.21 / 0.23 | $21.00 | $2,200.00 cash | Bought to close at 0.02 ($2.00), net +$19.00 | premium 0.95% of collateral |
| 10 | SIMQ-W09-P26 | W9 mid | $26 | 0.16 / 0.18 | $16.00 | $2,600.00 cash | Expired worthless (Fri SimQ 30.32) | premium 0.62% of collateral |
| 11 | SIMQ-W10-P26 | W10 open | $26 | 0.40 / 0.44 | $40.00 | $2,600.00 cash | Bought to close at 0.01 ($1.00), net +$39.00 | premium 1.54% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 68.24 | 66.43 | 66.34 | 62.08 | 60.98 | -4.4% | 5.81 (7,560.00 x 3d; 7,576.00 x 4d) |
| 2 | calm_up | 60.98 | 59.71 | 57.59 | 58.25 | 57.16 | 57.84 | -5.1% | 5.86 (7,636.81 x 3d; 7,630.81 x 4d) |
| 3 | chop | 57.84 | 57.46 | 55.94 | 52.70 | 54.49 | 52.70 | -8.9% | 5.88 (7,661.67 x 7d) |
| 4 | selloff | 52.70 | 49.82 | 50.39 | 46.63 | 44.87 | 43.39 | -17.7% | 4.92 (7,722.55 x 5d; 3,122.55 x 2d) |
| 5 | chop | 43.39 | 42.45 | 40.35 | 43.14 | 39.36 | 39.90 | -8.0% | 2.47 (3,221.47 x 7d) |
| 6 | calm_up | 39.90 | 39.82 | 40.70 | 40.89 | 40.55 | 40.92 | +2.6% | 2.48 (3,228.94 x 3d; 3,227.94 x 4d) |
| 7 | calm_up | 40.92 | 40.80 | 40.95 | 37.97 | 38.10 | 38.68 | -5.5% | 2.48 (3,230.42 x 7d) |
| 8 | selloff | 38.68 | 35.26 | 34.12 | 34.83 | 32.25 | 29.13 | -24.7% | 2.48 (3,232.90 x 7d) |
| 9 | rebound | 29.13 | 29.86 | 30.35 | 29.61 | 29.86 | 30.32 | +4.1% | 2.50 (3,256.38 x 3d; 3,270.38 x 4d) |
| 10 | chop | 30.32 | 30.29 | 30.53 | 33.55 | 34.33 | 35.00 | +15.4% | 2.54 (3,312.88 x 3d; 3,311.88 x 4d) |

## Scorecard
- 11 trades: 5 expired worthless, 5 closed for profit, 0 closed at a loss, 1 assigned, 0 called away | win rate 45% (91% counting profitable closes)
- Avg put premium: 0.82% of collateral
- Avg call premium: 1.11% of share value at sale
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
