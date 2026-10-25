# SimQ Run 3 Ledger

- Seed: 943118079 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-003-journal.md

## Current state (Week 3, Monday open)
- SimQ spot: $51.56
- Cash: $7,611.62 | locked collateral: $0.00 | free: $7,611.62
- Shares: 0
- Open positions: none
- Premium collected (gross): $100.00 | buy-to-close costs: $0.00 | interest: $11.62
- Realized P&L (options net of buy-backs + stock sales): +$100.00 (options +$100.00, stock +$0.00)
- Account value: $7,611.62 (+1.49% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Expired worthless (Fri SimQ 61.87) | premium 0.95% of collateral; held at midweek (ask 0.83) |
| 2 | SIMQ-W02-P51 | W2 open | $51 | 0.47 / 0.50 | $47.00 | $5,100.00 cash | Expired worthless (Fri SimQ 51.56) | premium 0.92% of collateral; held at midweek (ask 0.35) |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | selloff | 63.80 | 63.00 | 62.42 | 60.08 | 61.77 | 61.87 | -3.0% | 5.79 (7,553.00 x 7d) |
| 2 | crash | 61.87 | 56.24 | 56.98 | 58.00 | 53.51 | 51.56 | -16.7% | 5.83 (7,605.79 x 7d) |

## Scorecard
- 2 trades: 2 expired worthless, 0 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 100% (100% counting profitable closes)
- Avg put premium: 0.93% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
