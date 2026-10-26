# SimQ Run 5 Ledger

- Seed: 526270675 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-005-journal.md

## Current state (Week 3, Monday open)
- SimQ spot: $52.22
- Cash: $7,356.48 | locked collateral: $0.00 | free: $7,356.48
- Shares: 0
- Open positions: none
- Premium collected (gross): $211.00 | buy-to-close costs: $366.00 | interest: $11.48
- Realized P&L (options net of buy-backs + stock sales): -$155.00 (options -$155.00, stock +$0.00)
- Account value: $7,356.48 (-1.91% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P53 | W1 open | $53 | 0.25 / 0.27 | $25.00 | $5,300.00 cash | Bought to close at 0.02 ($2.00), net +$23.00 | premium 0.47% of collateral |
| 2 | SIMQ-W02-P55 | W2 open | $55 | 0.51 / 0.54 | $51.00 | $5,500.00 cash | Bought to close at 3.64 ($364.00), net -$313.00 | premium 0.93% of collateral |
| 3 | SIMQ-W02-P51 | W2 mid | $51 | 1.35 / 1.43 | $135.00 | $5,100.00 cash | Expired worthless (Fri SimQ 52.22) | premium 2.65% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | calm_up | 63.80 | 65.24 | 61.20 | 60.29 | 59.12 | 58.99 | -7.5% | 5.77 (7,525.00 x 3d; 7,523.00 x 4d) |
| 2 | selloff | 58.99 | 58.06 | 54.71 | 52.19 | 53.96 | 52.22 | -11.5% | 5.71 (7,579.77 x 3d; 7,350.77 x 4d) |

## Scorecard
- 3 trades: 1 expired worthless, 1 closed for profit, 1 closed at a loss, 0 assigned, 0 called away | win rate 33% (67% counting profitable closes)
- Avg put premium: 1.35% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
