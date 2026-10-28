# SimQ Run 6 Ledger

- Seed: 892542713 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-006-journal.md

## Current state (Week 8, Monday open)
- SimQ spot: $67.11
- Cash: $7,883.29 | locked collateral: $0.00 | free: $7,883.29
- Shares: 0
- Open positions: none
- Premium collected (gross): $361.00 | buy-to-close costs: $19.00 | interest: $41.29
- Realized P&L (options net of buy-backs + stock sales): +$342.00 (options +$342.00, stock +$0.00)
- Account value: $7,883.29 (+5.11% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P55 | W1 mid | $55 | 0.24 / 0.26 | $24.00 | $5,500.00 cash | Expired worthless (Fri SimQ 61.14) | premium 0.44% of collateral |
| 2 | SIMQ-W02-P53 | W2 open | $53 | 0.52 / 0.55 | $52.00 | $5,300.00 cash | Expired worthless (Fri SimQ 60.12) | premium 0.98% of collateral; held at midweek (ask 0.27) |
| 3 | SIMQ-W03-P53.5 | W3 open | $53.5 | 0.55 / 0.59 | $55.00 | $5,350.00 cash | Bought to close at 0.01 ($1.00), net +$54.00 | premium 1.03% of collateral |
| 4 | SIMQ-W03-P61 | W3 mid | $61 | 0.10 / 0.12 | $10.00 | $6,100.00 cash | Expired worthless (Fri SimQ 66.19) | premium 0.16% of collateral |
| 5 | SIMQ-W04-P63 | W4 mid | $63 | 0.16 / 0.18 | $16.00 | $6,300.00 cash | Expired worthless (Fri SimQ 66.87) | premium 0.25% of collateral |
| 6 | SIMQ-W05-P61 | W5 open | $61 | 0.40 / 0.43 | $40.00 | $6,100.00 cash | Bought to close at 0.08 ($8.00), net +$32.00 | premium 0.66% of collateral |
| 7 | SIMQ-W05-P65 | W5 mid | $65 | 0.33 / 0.36 | $33.00 | $6,500.00 cash | Expired worthless (Fri SimQ 66.39) | premium 0.51% of collateral |
| 8 | SIMQ-W06-P57 | W6 open | $57 | 0.58 / 0.62 | $58.00 | $5,700.00 cash | Bought to close at 0.01 ($1.00), net +$57.00 | premium 1.02% of collateral |
| 9 | SIMQ-W07-P62.5 | W7 open | $62.5 | 0.48 / 0.51 | $48.00 | $6,250.00 cash | Bought to close at 0.09 ($9.00), net +$39.00 | premium 0.77% of collateral |
| 10 | SIMQ-W07-P64.5 | W7 mid | $64.5 | 0.25 / 0.27 | $25.00 | $6,450.00 cash | Expired worthless (Fri SimQ 67.11) | premium 0.39% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 60.66 | 61.34 | 60.88 | 62.29 | 61.14 | -4.2% | 5.76 (7,500.00 x 3d; 7,524.00 x 4d) |
| 2 | chop | 61.14 | 61.64 | 58.91 | 58.18 | 59.10 | 60.12 | -1.7% | 5.82 (7,581.76 x 7d) |
| 3 | calm_up | 60.12 | 61.53 | 63.24 | 66.02 | 66.71 | 66.19 | +10.1% | 5.87 (7,642.58 x 3d; 7,651.58 x 4d) |
| 4 | calm_up | 66.19 | 66.34 | 66.66 | 67.40 | 67.40 | 66.87 | +1.0% | 5.88 (7,657.45 x 3d; 7,673.45 x 4d) |
| 5 | chop | 66.87 | 67.09 | 69.61 | 70.53 | 67.58 | 66.39 | -0.7% | 5.93 (7,719.33 x 3d; 7,744.33 x 4d) |
| 6 | calm_up | 66.39 | 66.00 | 66.00 | 67.54 | 68.80 | 68.07 | +2.5% | 5.99 (7,808.26 x 3d; 7,807.26 x 4d) |
| 7 | calm_up | 68.07 | 66.59 | 67.73 | 68.27 | 64.91 | 67.11 | -1.4% | 6.04 (7,861.25 x 3d; 7,877.25 x 4d) |

## Scorecard
- 10 trades: 6 expired worthless, 4 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 60% (100% counting profitable closes)
- Avg put premium: 0.62% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
