# SimQ Run 8 Ledger

- Seed: 683124076 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-008-journal.md

## Current state (Week 3, Monday open)
- SimQ spot: $60.28
- Cash: $7,646.66 | locked collateral: $0.00 | free: $7,646.66
- Shares: 0
- Open positions: none
- Premium collected (gross): $137.00 | buy-to-close costs: $2.00 | interest: $11.66
- Realized P&L (options net of buy-backs + stock sales): +$135.00 (options +$135.00, stock +$0.00)
- Account value: $7,646.66 (+1.96% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Bought to close at 0.02 ($2.00), net +$51.00 | premium 0.95% of collateral |
| 2 | SIMQ-W01-P62 | W1 mid | $62 | 0.25 / 0.28 | $25.00 | $6,200.00 cash | Expired worthless (Fri SimQ 65.02) | premium 0.40% of collateral |
| 3 | SIMQ-W02-P56 | W2 open | $56 | 0.59 / 0.63 | $59.00 | $5,600.00 cash | Expired worthless (Fri SimQ 60.28) | premium 1.05% of collateral; held at midweek (ask 0.36) |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 66.25 | 66.67 | 67.62 | 67.31 | 65.02 | +1.9% | 5.80 (7,553.00 x 3d; 7,576.00 x 4d) |
| 2 | chop | 65.02 | 63.24 | 65.22 | 61.76 | 60.14 | 60.28 | -7.3% | 5.86 (7,640.80 x 7d) |

## Scorecard
- 3 trades: 2 expired worthless, 1 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 67% (100% counting profitable closes)
- Avg put premium: 0.80% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
