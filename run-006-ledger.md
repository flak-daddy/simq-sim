# SimQ Run 6 Ledger

- Seed: 892542713 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-006-journal.md

## Current state (Week 3, Monday open)
- SimQ spot: $60.12
- Cash: $7,587.58 | locked collateral: $0.00 | free: $7,587.58
- Shares: 0
- Open positions: none
- Premium collected (gross): $76.00 | buy-to-close costs: $0.00 | interest: $11.58
- Realized P&L (options net of buy-backs + stock sales): +$76.00 (options +$76.00, stock +$0.00)
- Account value: $7,587.58 (+1.17% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P55 | W1 mid | $55 | 0.24 / 0.26 | $24.00 | $5,500.00 cash | Expired worthless (Fri SimQ 61.14) | premium 0.44% of collateral |
| 2 | SIMQ-W02-P53 | W2 open | $53 | 0.52 / 0.55 | $52.00 | $5,300.00 cash | Expired worthless (Fri SimQ 60.12) | premium 0.98% of collateral; held at midweek (ask 0.27) |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 60.66 | 61.34 | 60.88 | 62.29 | 61.14 | -4.2% | 5.76 (7,500.00 x 3d; 7,524.00 x 4d) |
| 2 | chop | 61.14 | 61.64 | 58.91 | 58.18 | 59.10 | 60.12 | -1.7% | 5.82 (7,581.76 x 7d) |

## Scorecard
- 2 trades: 2 expired worthless, 0 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 100% (100% counting profitable closes)
- Avg put premium: 0.71% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
