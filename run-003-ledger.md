# SimQ Run 3 Ledger

- Seed: 943118079 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-003-journal.md

## Current state (Week 13, Monday open)
- SimQ spot: $39.38
- Cash: $3,579.04 | locked collateral: $0.00 | free: $3,579.04
- Shares: 100 SimQ bought at $49.00 in Week 9; effective basis $46.33 after option premiums
- Open positions: none
- Premium collected (gross): $1,122.00 | buy-to-close costs: $901.00 | interest: $58.04
- Realized P&L (options net of buy-backs + stock sales): +$921.00 (options +$221.00, stock +$700.00)
- Account value: $7,517.04 (+0.23% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Expired worthless (Fri SimQ 61.87) | premium 0.95% of collateral; held at midweek (ask 0.83) |
| 2 | SIMQ-W02-P51 | W2 open | $51 | 0.47 / 0.50 | $47.00 | $5,100.00 cash | Expired worthless (Fri SimQ 51.56) | premium 0.92% of collateral; held at midweek (ask 0.35) |
| 3 | SIMQ-W03-P38 | W3 open | $38 | 0.40 / 0.43 | $40.00 | $3,800.00 cash | Bought to close at 0.01 ($1.00), net +$39.00 | premium 1.05% of collateral |
| 4 | SIMQ-W03-P48 | W3 mid | $48 | 0.42 / 0.46 | $42.00 | $4,800.00 cash | Expired worthless (Fri SimQ 55.28) | premium 0.87% of collateral |
| 5 | SIMQ-W04-P45 | W4 open | $45 | 0.45 / 0.49 | $45.00 | $4,500.00 cash | Bought to close at 0.01 ($1.00), net +$44.00 | premium 1.00% of collateral |
| 6 | SIMQ-W04-P54 | W4 mid | $54 | 0.26 / 0.29 | $26.00 | $5,400.00 cash | Expired worthless (Fri SimQ 54.86) | premium 0.48% of collateral |
| 7 | SIMQ-W05-P48 | W5 open | $48 | 0.50 / 0.54 | $50.00 | $4,800.00 cash | Bought to close at 0.03 ($3.00), net +$47.00 | premium 1.04% of collateral |
| 8 | SIMQ-W05-P55 | W5 mid | $55 | 0.40 / 0.43 | $40.00 | $5,500.00 cash | ASSIGNED: bought 100 at $55.00 (Fri SimQ 54.88) | premium 0.73% of collateral |
| 9 | SIMQ-W06-C59 | W6 open | $59 | 1.19 / 1.26 | $119.00 | lot 1 | Bought to close at 4.01 ($401.00), net -$282.00 | premium 2.17% of share value |
| 10 | SIMQ-W06-C62 | W6 mid | $62 | 1.97 / 2.08 | $197.00 | lot 1 | CALLED AWAY: sold 100 at $62.00 (Fri SimQ 74.90) | premium 3.18% of share value |
| 11 | SIMQ-W07-P64.5 | W7 open | $64.5 | 1.04 / 1.10 | $104.00 | $6,450.00 cash | Bought to close at 0.73 ($73.00), net +$31.00 | premium 1.61% of collateral |
| 12 | SIMQ-W07-P62 | W7 mid | $62 | 0.19 / 0.21 | $19.00 | $6,200.00 cash | Expired worthless (Fri SimQ 63.92) | premium 0.31% of collateral |
| 13 | SIMQ-W08-P56 | W8 mid | $56 | 0.13 / 0.15 | $13.00 | $5,600.00 cash | Expired worthless (Fri SimQ 59.84) | premium 0.23% of collateral |
| 14 | SIMQ-W09-P54 | W9 open | $54 | 0.24 / 0.27 | $24.00 | $5,400.00 cash | Bought to close at 4.20 ($420.00), net -$396.00 | premium 0.44% of collateral |
| 15 | SIMQ-W09-P49 | W9 mid | $49 | 1.31 / 1.39 | $131.00 | $4,900.00 cash | ASSIGNED: bought 100 at $49.00 (Fri SimQ 45.34) | premium 2.67% of collateral |
| 16 | SIMQ-W10-C50 | W10 open | $50 | 0.55 / 0.59 | $55.00 | lot 2 | Expired worthless (Fri SimQ 46.73) | premium 1.21% of share value; held at midweek (ask 0.19) |
| 17 | SIMQ-W10-P30 | W10 open | $30 | 0.03 / 0.04 | $3.00 | $3,000.00 cash | Expired worthless (Fri SimQ 46.73) | premium 0.10% of collateral; held at midweek (ask 0.01) |
| 18 | SIMQ-W11-C50 | W11 open | $50 | 0.61 / 0.66 | $61.00 | lot 2 | Expired worthless (Fri SimQ 39.04) | premium 1.31% of share value; held at midweek (ask 0.05) |
| 19 | SIMQ-W12-P30 | W12 open | $30 | 0.32 / 0.35 | $32.00 | $3,000.00 cash | Bought to close at 0.01 ($1.00), net +$31.00 | premium 1.07% of collateral |
| 20 | SIMQ-W12-C46 | W12 open | $46 | 0.21 / 0.23 | $21.00 | lot 2 | Bought to close at 0.01 ($1.00), net +$20.00 | premium 0.54% of share value |

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W5 at $55.00 | W6 at $62.00 | +$700.00 | +$655.00 |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | selloff | 63.80 | 63.00 | 62.42 | 60.08 | 61.77 | 61.87 | -3.0% | 5.79 (7,553.00 x 7d) |
| 2 | crash | 61.87 | 56.24 | 56.98 | 58.00 | 53.51 | 51.56 | -16.7% | 5.83 (7,605.79 x 7d) |
| 3 | rebound | 51.56 | 52.83 | 52.73 | 52.59 | 54.90 | 55.28 | +7.2% | 5.89 (7,651.62 x 3d; 7,692.62 x 4d) |
| 4 | chop | 55.28 | 58.25 | 56.60 | 59.03 | 55.58 | 54.86 | -0.8% | 5.95 (7,743.51 x 3d; 7,768.51 x 4d) |
| 5 | rebound | 54.86 | 60.36 | 58.58 | 60.70 | 55.41 | 54.88 | +0.0% | 4.81 (7,824.46 x 3d; 7,861.46 x 2d; 2,361.46 x 2d) |
| 6 | rebound | 54.88 | 55.44 | 59.09 | 61.88 | 67.71 | 74.90 | +36.5% | 3.18 (2,485.27 x 3d; 2,281.27 x 2d; 8,481.27 x 2d) |
| 7 | calm_up | 74.90 | 74.37 | 65.78 | 65.90 | 63.35 | 63.92 | -14.7% | 6.56 (8,588.45 x 3d; 8,534.45 x 4d) |
| 8 | calm_up | 63.92 | 62.61 | 60.52 | 60.02 | 59.07 | 59.84 | -6.4% | 6.56 (8,541.01 x 3d; 8,554.01 x 4d) |
| 9 | chop | 59.84 | 60.11 | 56.81 | 50.51 | 48.57 | 45.34 | -24.2% | 5.38 (8,584.57 x 3d; 8,295.57 x 2d; 3,395.57 x 2d) |
| 10 | chop | 45.34 | 46.34 | 47.13 | 46.41 | 46.85 | 46.73 | +3.1% | 2.65 (3,458.95 x 7d) |
| 11 | selloff | 46.73 | 47.45 | 46.48 | 43.09 | 41.61 | 39.04 | -16.5% | 2.70 (3,522.60 x 7d) |
| 12 | calm_up | 39.04 | 39.26 | 39.49 | 40.12 | 40.44 | 39.38 | +0.9% | 2.74 (3,578.30 x 3d; 3,576.30 x 4d) |

## Scorecard
- 20 trades: 9 expired worthless, 6 closed for profit, 2 closed at a loss, 2 assigned, 1 called away | win rate 45% (75% counting profitable closes)
- Avg put premium: 0.90% of collateral
- Avg call premium: 1.68% of share value at sale
- Wheel cycles completed (shares called away): 1
- Account value at week 26 (comparison metric): pending
