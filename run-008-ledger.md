# SimQ Run 8 Ledger

- Seed: 683124076 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-008-journal.md

## Current state (Week 2, Monday open)
- SimQ spot: $65.02
- Cash: $7,581.80 | locked collateral: $0.00 | free: $7,581.80
- Shares: 0
- Open positions: none
- Premium collected (gross): $78.00 | buy-to-close costs: $2.00 | interest: $5.80
- Realized P&L (options net of buy-backs + stock sales): +$76.00 (options +$76.00, stock +$0.00)
- Account value: $7,581.80 (+1.09% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Bought to close at 0.02 ($2.00), net +$51.00 | premium 0.95% of collateral |
| 2 | SIMQ-W01-P62 | W1 mid | $62 | 0.25 / 0.28 | $25.00 | $6,200.00 cash | Expired worthless (Fri SimQ 65.02) | premium 0.40% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 66.25 | 66.67 | 67.62 | 67.31 | 65.02 | +1.9% | 5.80 (7,553.00 x 3d; 7,576.00 x 4d) |

## Scorecard
- 2 trades: 1 expired worthless, 1 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 50% (100% counting profitable closes)
- Avg put premium: 0.67% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
