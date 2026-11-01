# SimQ Run 8 Ledger

- Seed: 683124076 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-008-journal.md

## Current state (Week 5, Monday open)
- SimQ spot: $65.66
- Cash: $7,745.50 | locked collateral: $0.00 | free: $7,745.50
- Shares: 0
- Open positions: none
- Premium collected (gross): $225.00 | buy-to-close costs: $3.00 | interest: $23.50
- Realized P&L (options net of buy-backs + stock sales): +$222.00 (options +$222.00, stock +$0.00)
- Account value: $7,745.50 (+3.27% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Bought to close at 0.02 ($2.00), net +$51.00 | premium 0.95% of collateral |
| 2 | SIMQ-W01-P62 | W1 mid | $62 | 0.25 / 0.28 | $25.00 | $6,200.00 cash | Expired worthless (Fri SimQ 65.02) | premium 0.40% of collateral |
| 3 | SIMQ-W02-P56 | W2 open | $56 | 0.59 / 0.63 | $59.00 | $5,600.00 cash | Expired worthless (Fri SimQ 60.28) | premium 1.05% of collateral; held at midweek (ask 0.36) |
| 4 | SIMQ-W03-P53.5 | W3 open | $53.5 | 0.55 / 0.59 | $55.00 | $5,350.00 cash | Bought to close at 0.01 ($1.00), net +$54.00 | premium 1.03% of collateral |
| 5 | SIMQ-W04-P61.5 | W4 mid | $61.5 | 0.33 / 0.36 | $33.00 | $6,150.00 cash | Expired worthless (Fri SimQ 65.66) | premium 0.54% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 66.25 | 66.67 | 67.62 | 67.31 | 65.02 | +1.9% | 5.80 (7,553.00 x 3d; 7,576.00 x 4d) |
| 2 | chop | 65.02 | 63.24 | 65.22 | 61.76 | 60.14 | 60.28 | -7.3% | 5.86 (7,640.80 x 7d) |
| 3 | calm_up | 60.28 | 61.97 | 64.45 | 64.24 | 65.08 | 65.99 | +9.5% | 5.91 (7,701.66 x 3d; 7,700.66 x 4d) |
| 4 | chop | 65.99 | 66.52 | 62.56 | 66.16 | 66.49 | 65.66 | -0.5% | 5.93 (7,706.57 x 3d; 7,739.57 x 4d) |

## Scorecard
- 5 trades: 3 expired worthless, 2 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 60% (100% counting profitable closes)
- Avg put premium: 0.79% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
