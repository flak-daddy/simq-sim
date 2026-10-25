# SimQ Run 4 Ledger

- Seed: 867728425 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-004-journal.md

## Current state (Week 14, Monday open)
- SimQ spot: $40.35
- Cash: $7,911.34 | locked collateral: $0.00 | free: $7,911.34
- Shares: 0
- Open positions: none
- Premium collected (gross): $914.00 | buy-to-close costs: $673.00 | interest: $70.34
- Realized P&L (options net of buy-backs + stock sales): +$341.00 (options +$241.00, stock +$100.00)
- Account value: $7,911.34 (+5.48% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Expired worthless (Fri SimQ 65.42) | premium 0.95% of collateral; held at midweek (ask 0.13) |
| 2 | SIMQ-W02-P56.5 | W2 open | $56.5 | 0.76 / 0.81 | $76.00 | $5,650.00 cash | Bought to close at 0.02 ($2.00), net +$74.00 | premium 1.35% of collateral |
| 3 | SIMQ-W02-P62 | W2 mid | $62 | 0.13 / 0.14 | $13.00 | $6,200.00 cash | Expired worthless (Fri SimQ 69.10) | premium 0.21% of collateral |
| 4 | SIMQ-W03-P60 | W3 open | $60 | 0.52 / 0.56 | $52.00 | $6,000.00 cash | Bought to close at 0.13 ($13.00), net +$39.00 | premium 0.87% of collateral |
| 5 | SIMQ-W03-P63.5 | W3 mid | $63.5 | 0.31 / 0.34 | $31.00 | $6,350.00 cash | Expired worthless (Fri SimQ 67.23) | premium 0.49% of collateral |
| 6 | SIMQ-W04-P55 | W4 open | $55 | 0.72 / 0.77 | $72.00 | $5,500.00 cash | Bought to close at 2.64 ($264.00), net -$192.00 | premium 1.31% of collateral |
| 7 | SIMQ-W04-P50 | W4 mid | $50 | 1.03 / 1.09 | $103.00 | $5,000.00 cash | Expired worthless (Fri SimQ 62.24) | premium 2.06% of collateral |
| 8 | SIMQ-W05-P53 | W5 open | $53 | 0.73 / 0.78 | $73.00 | $5,300.00 cash | Bought to close at 0.05 ($5.00), net +$68.00 | premium 1.38% of collateral |
| 9 | SIMQ-W05-P54.5 | W5 mid | $54.5 | 0.09 / 0.10 | $9.00 | $5,450.00 cash | Expired worthless (Fri SimQ 66.31) | premium 0.17% of collateral |
| 10 | SIMQ-W06-P58 | W6 open | $58 | 0.59 / 0.63 | $59.00 | $5,800.00 cash | Expired worthless (Fri SimQ 61.64) | premium 1.02% of collateral; held at midweek (ask 0.25) |
| 11 | SIMQ-W07-P50 | W7 open | $50 | 0.57 / 0.61 | $57.00 | $5,000.00 cash | Bought to close at 3.81 ($381.00), net -$324.00 | premium 1.14% of collateral |
| 12 | SIMQ-W07-P45 | W7 mid | $45 | 1.13 / 1.20 | $113.00 | $4,500.00 cash | ASSIGNED: bought 100 at $45.00 (Fri SimQ 38.80) | premium 2.51% of collateral |
| 13 | SIMQ-W08-P25 | W8 open | $25 | 0.31 / 0.33 | $31.00 | $2,500.00 cash | Bought to close at 0.01 ($1.00), net +$30.00 | premium 1.24% of collateral |
| 14 | SIMQ-W09-C49 | W9 open | $49 | 0.67 / 0.72 | $67.00 | lot 1 | Bought to close at 0.06 ($6.00), net +$61.00 | premium 1.50% of share value |
| 15 | SIMQ-W09-C46 | W9 mid | $46 | 0.74 / 0.79 | $74.00 | lot 1 | CALLED AWAY: sold 100 at $46.00 (Fri SimQ 46.23) | premium 1.62% of share value |
| 16 | SIMQ-W11-P35 | W11 open | $35 | 0.13 / 0.15 | $13.00 | $3,500.00 cash | Bought to close at 0.01 ($1.00), net +$12.00 | premium 0.37% of collateral |
| 17 | SIMQ-W12-P35 | W12 open | $35 | 0.03 / 0.04 | $3.00 | $3,500.00 cash | Expired worthless (Fri SimQ 40.47) | premium 0.09% of collateral; held at midweek (ask 0.01) |
| 18 | SIMQ-W13-P36 | W13 open | $36 | 0.15 / 0.17 | $15.00 | $3,600.00 cash | Expired worthless (Fri SimQ 40.35) | premium 0.42% of collateral; held at midweek (ask 0.04) |

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W7 at $45.00 | W9 at $46.00 | +$100.00 | +$348.00 |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 63.52 | 63.81 | 63.37 | 69.04 | 65.42 | +2.5% | 5.79 (7,553.00 x 7d) |
| 2 | chop | 65.42 | 69.74 | 70.24 | 70.42 | 66.91 | 69.10 | +5.6% | 5.86 (7,634.79 x 3d; 7,645.79 x 4d) |
| 3 | crash | 69.10 | 65.86 | 67.11 | 73.12 | 65.34 | 67.23 | -2.7% | 5.92 (7,703.65 x 3d; 7,721.65 x 4d) |
| 4 | rebound | 67.23 | 67.54 | 68.59 | 55.81 | 58.59 | 62.24 | -7.4% | 5.91 (7,799.57 x 3d; 7,638.57 x 4d) |
| 5 | chop | 62.24 | 63.41 | 62.79 | 61.83 | 66.62 | 66.31 | +6.5% | 5.92 (7,717.48 x 3d; 7,721.48 x 4d) |
| 6 | selloff | 66.31 | 67.79 | 69.92 | 67.37 | 63.85 | 61.64 | -7.0% | 5.97 (7,786.40 x 7d) |
| 7 | crash | 61.64 | 58.31 | 48.35 | 46.99 | 45.51 | 38.80 | -37.1% | 4.92 (7,849.37 x 3d; 7,581.37 x 2d; 3,081.37 x 2d) |
| 8 | rebound | 38.80 | 38.89 | 40.18 | 39.94 | 40.86 | 44.62 | +15.0% | 2.39 (3,117.29 x 3d; 3,116.29 x 4d) |
| 9 | calm_up | 44.62 | 45.18 | 45.58 | 45.80 | 46.29 | 46.23 | +3.6% | 3.48 (3,185.68 x 3d; 3,253.68 x 2d; 7,853.68 x 2d) |
| 10 | calm_up | 46.23 | 45.51 | 43.74 | 42.42 | 42.38 | 41.18 | -10.9% | 6.03 (7,857.16 x 7d) |
| 11 | calm_up | 41.18 | 41.43 | 41.72 | 41.24 | 41.33 | 41.73 | +1.3% | 6.04 (7,876.19 x 3d; 7,875.19 x 4d) |
| 12 | calm_up | 41.73 | 40.63 | 39.86 | 40.67 | 40.79 | 40.47 | -3.0% | 6.05 (7,884.23 x 7d) |
| 13 | chop | 40.47 | 39.93 | 40.36 | 41.81 | 40.24 | 40.35 | -0.3% | 6.06 (7,905.28 x 7d) |

## Scorecard
- 18 trades: 8 expired worthless, 6 closed for profit, 2 closed at a loss, 1 assigned, 1 called away | win rate 44% (78% counting profitable closes)
- Avg put premium: 0.97% of collateral
- Avg call premium: 1.56% of share value at sale
- Wheel cycles completed (shares called away): 1
- Account value at week 26 (comparison metric): pending
