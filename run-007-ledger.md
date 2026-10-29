# SimQ Run 7 Ledger

- Seed: 104391084 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-007-journal.md

## Current state (Week 3, Monday open)
- SimQ spot: $57.84
- Cash: $7,636.67 | locked collateral: $0.00 | free: $7,636.67
- Shares: 0
- Open positions: none
- Premium collected (gross): $140.00 | buy-to-close costs: $15.00 | interest: $11.67
- Realized P&L (options net of buy-backs + stock sales): +$125.00 (options +$125.00, stock +$0.00)
- Account value: $7,636.67 (+1.82% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56.5 | W1 open | $56.5 | 0.60 / 0.64 | $60.00 | $5,650.00 cash | Bought to close at 0.09 ($9.00), net +$51.00 | premium 1.06% of collateral |
| 2 | SIMQ-W01-P60 | W1 mid | $60 | 0.25 / 0.28 | $25.00 | $6,000.00 cash | Expired worthless (Fri SimQ 60.98) | premium 0.42% of collateral |
| 3 | SIMQ-W02-P53 | W2 open | $53 | 0.55 / 0.59 | $55.00 | $5,300.00 cash | Bought to close at 0.06 ($6.00), net +$49.00 | premium 1.04% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 68.24 | 66.43 | 66.34 | 62.08 | 60.98 | -4.4% | 5.81 (7,560.00 x 3d; 7,576.00 x 4d) |
| 2 | calm_up | 60.98 | 59.71 | 57.59 | 58.25 | 57.16 | 57.84 | -5.1% | 5.86 (7,636.81 x 3d; 7,630.81 x 4d) |

## Scorecard
- 3 trades: 1 expired worthless, 2 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 33% (100% counting profitable closes)
- Avg put premium: 0.84% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
