# SimQ Run 5 Ledger

- Seed: 526270675 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-005-journal.md

## Current state (Week 4, Monday open)
- SimQ spot: $31.30
- Cash: $3,310.24 | locked collateral: $0.00 | free: $3,310.24
- Shares: 100 SimQ bought at $40.00 in Week 3; effective basis $38.99 after option premiums
- Open positions: none
- Premium collected (gross): $355.00 | buy-to-close costs: $561.00 | interest: $16.24
- Realized P&L (options net of buy-backs + stock sales): -$206.00 (options -$206.00, stock +$0.00)
- Account value: $6,440.24 (-14.13% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P53 | W1 open | $53 | 0.25 / 0.27 | $25.00 | $5,300.00 cash | Bought to close at 0.02 ($2.00), net +$23.00 | premium 0.47% of collateral |
| 2 | SIMQ-W02-P55 | W2 open | $55 | 0.51 / 0.54 | $51.00 | $5,500.00 cash | Bought to close at 3.64 ($364.00), net -$313.00 | premium 0.93% of collateral |
| 3 | SIMQ-W02-P51 | W2 mid | $51 | 1.35 / 1.43 | $135.00 | $5,100.00 cash | Expired worthless (Fri SimQ 52.22) | premium 2.65% of collateral |
| 4 | SIMQ-W03-P42 | W3 open | $42 | 0.43 / 0.47 | $43.00 | $4,200.00 cash | Bought to close at 1.95 ($195.00), net -$152.00 | premium 1.02% of collateral |
| 5 | SIMQ-W03-P40 | W3 mid | $40 | 1.01 / 1.07 | $101.00 | $4,000.00 cash | ASSIGNED: bought 100 at $40.00 (Fri SimQ 31.30) | premium 2.53% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | calm_up | 63.80 | 65.24 | 61.20 | 60.29 | 59.12 | 58.99 | -7.5% | 5.77 (7,525.00 x 3d; 7,523.00 x 4d) |
| 2 | selloff | 58.99 | 58.06 | 54.71 | 52.19 | 53.96 | 52.22 | -11.5% | 5.71 (7,579.77 x 3d; 7,350.77 x 4d) |
| 3 | crash | 52.22 | 52.24 | 42.32 | 41.41 | 32.41 | 31.30 | -40.1% | 4.76 (7,399.48 x 3d; 7,305.48 x 2d; 3,305.48 x 2d) |

## Scorecard
- 5 trades: 1 expired worthless, 1 closed for profit, 2 closed at a loss, 1 assigned, 0 called away | win rate 20% (40% counting profitable closes)
- Avg put premium: 1.52% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
