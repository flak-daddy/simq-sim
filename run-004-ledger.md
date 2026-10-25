# SimQ Run 4 Ledger

- Seed: 867728425 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-004-journal.md

## Current state (Week 4, Monday open)
- SimQ spot: $67.23
- Cash: $7,727.57 | locked collateral: $0.00 | free: $7,727.57
- Shares: 0
- Open positions: none
- Premium collected (gross): $225.00 | buy-to-close costs: $15.00 | interest: $17.57
- Realized P&L (options net of buy-backs + stock sales): +$210.00 (options +$210.00, stock +$0.00)
- Account value: $7,727.57 (+3.03% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Expired worthless (Fri SimQ 65.42) | premium 0.95% of collateral; held at midweek (ask 0.13) |
| 2 | SIMQ-W02-P56.5 | W2 open | $56.5 | 0.76 / 0.81 | $76.00 | $5,650.00 cash | Bought to close at 0.02 ($2.00), net +$74.00 | premium 1.35% of collateral |
| 3 | SIMQ-W02-P62 | W2 mid | $62 | 0.13 / 0.14 | $13.00 | $6,200.00 cash | Expired worthless (Fri SimQ 69.10) | premium 0.21% of collateral |
| 4 | SIMQ-W03-P60 | W3 open | $60 | 0.52 / 0.56 | $52.00 | $6,000.00 cash | Bought to close at 0.13 ($13.00), net +$39.00 | premium 0.87% of collateral |
| 5 | SIMQ-W03-P63.5 | W3 mid | $63.5 | 0.31 / 0.34 | $31.00 | $6,350.00 cash | Expired worthless (Fri SimQ 67.23) | premium 0.49% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 63.52 | 63.81 | 63.37 | 69.04 | 65.42 | +2.5% | 5.79 (7,553.00 x 7d) |
| 2 | chop | 65.42 | 69.74 | 70.24 | 70.42 | 66.91 | 69.10 | +5.6% | 5.86 (7,634.79 x 3d; 7,645.79 x 4d) |
| 3 | crash | 69.10 | 65.86 | 67.11 | 73.12 | 65.34 | 67.23 | -2.7% | 5.92 (7,703.65 x 3d; 7,721.65 x 4d) |

## Scorecard
- 5 trades: 3 expired worthless, 2 closed for profit, 0 closed at a loss, 0 assigned, 0 called away | win rate 60% (100% counting profitable closes)
- Avg put premium: 0.77% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
