# SimQ Run 6 Ledger

- Seed: 892542713 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-006-journal.md

## Current state (Week 5, Monday open)
- SimQ spot: $66.87
- Cash: $7,679.33 | locked collateral: $0.00 | free: $7,679.33
- Shares: 0
- Open positions: none
- Premium collected (gross): $157.00 | buy-to-close costs: $1.00 | interest: $23.33
- Realized P&L (options net of buy-backs + stock sales): +$156.00 (options +$156.00, stock +$0.00)
- Account value: $7,679.33 (+2.39% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P55 | W1 mid | $55 | 0.24 / 0.26 | $24.00 | $5,500.00 cash | Expired worthless (Fri SimQ 61.14) | premium 0.44% of collateral |
| 2 | SIMQ-W02-P53 | W2 open | $53 | 0.52 / 0.55 | $52.00 | $5,300.00 cash | Expired worthless (Fri SimQ 60.12) | premium 0.98% of collateral; held at midweek (ask 0.27) |
| 3 | SIMQ-W03-P53.5 | W3 open | $53.5 | 0.55 / 0.59 | $55.00 | $5,350.00 cash | Bought to close at 0.01 ($1.00), net +$54.00 | premium 1.03% of collateral |
| 4 | SIMQ-W03-P61 | W3 mid | $61 | 0.10 / 0.12 | $10.00 | $6,100.00 cash | Expired worthless (Fri SimQ 66.19) | premium 0.16% of collateral |
| 5 | SIMQ-W04-P63 | W4 mid | $63 | 0.16 / 0.18 | $16.00 | $6,300.00 cash | Expired worthless (Fri SimQ 66.87) | premium 0.25% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 60.66 | 61.34 | 60.88 | 62.29 | 61.14 | -4.2% | 5.76 (7,500.00 x 3d; 7,524.00 x 4d) |
| 2 | chop | 61.14 | 61.64 | 58.91 | 58.18 | 59.10 | 60.12 | -1.7% | 5.82 (7,581.76 x 7d) |
| 3 | calm_up | 60.12 | 61.53 | 63.24 | 66.02 | 66.71 | 66.19 | +10.1% | 5.87 (7,642.58 x 3d; 7,651.58 x 4d) |
| 4 | calm_up | 66.19 | 66.34 | 66.66 | 67.40 | 67.40 | 66.87 | +1.0% | 5.88 (7,657.45 x 3d; 7,673.45 x 4d) |

## Scorecard
- 5 trades: 4 expired worthless, 1 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 80% (100% counting profitable closes)
- Avg put premium: 0.57% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
