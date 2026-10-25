# SimQ Run 3 Ledger

- Seed: 943118079 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-003-journal.md

## Current state (Week 4, Monday open)
- SimQ spot: $55.28
- Cash: $7,698.51 | locked collateral: $0.00 | free: $7,698.51
- Shares: 0
- Open positions: none
- Premium collected (gross): $182.00 | buy-to-close costs: $1.00 | interest: $17.51
- Realized P&L (options net of buy-backs + stock sales): +$181.00 (options +$181.00, stock +$0.00)
- Account value: $7,698.51 (+2.65% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Expired worthless (Fri SimQ 61.87) | premium 0.95% of collateral; held at midweek (ask 0.83) |
| 2 | SIMQ-W02-P51 | W2 open | $51 | 0.47 / 0.50 | $47.00 | $5,100.00 cash | Expired worthless (Fri SimQ 51.56) | premium 0.92% of collateral; held at midweek (ask 0.35) |
| 3 | SIMQ-W03-P38 | W3 open | $38 | 0.40 / 0.43 | $40.00 | $3,800.00 cash | Bought to close at 0.01 ($1.00), net +$39.00 | premium 1.05% of collateral |
| 4 | SIMQ-W03-P48 | W3 mid | $48 | 0.42 / 0.46 | $42.00 | $4,800.00 cash | Expired worthless (Fri SimQ 55.28) | premium 0.87% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | selloff | 63.80 | 63.00 | 62.42 | 60.08 | 61.77 | 61.87 | -3.0% | 5.79 (7,553.00 x 7d) |
| 2 | crash | 61.87 | 56.24 | 56.98 | 58.00 | 53.51 | 51.56 | -16.7% | 5.83 (7,605.79 x 7d) |
| 3 | rebound | 51.56 | 52.83 | 52.73 | 52.59 | 54.90 | 55.28 | +7.2% | 5.89 (7,651.62 x 3d; 7,692.62 x 4d) |

## Scorecard
- 4 trades: 3 expired worthless, 1 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 75% (100% counting profitable closes)
- Avg put premium: 0.95% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
