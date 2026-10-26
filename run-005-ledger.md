# SimQ Run 5 Ledger

- Seed: 526270675 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-005-journal.md

## Current state (Week 5, Monday open)
- SimQ spot: $26.33
- Cash: $3,332.81 | locked collateral: $0.00 | free: $3,332.81
- Shares: 100 SimQ bought at $40.00 in Week 3; effective basis $38.71 after option premiums
- Open positions: none
- Premium collected (gross): $443.00 | buy-to-close costs: $629.00 | interest: $18.81
- Realized P&L (options net of buy-backs + stock sales): -$186.00 (options -$186.00, stock +$0.00)
- Account value: $5,965.81 (-20.46% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P53 | W1 open | $53 | 0.25 / 0.27 | $25.00 | $5,300.00 cash | Bought to close at 0.02 ($2.00), net +$23.00 | premium 0.47% of collateral |
| 2 | SIMQ-W02-P55 | W2 open | $55 | 0.51 / 0.54 | $51.00 | $5,500.00 cash | Bought to close at 3.64 ($364.00), net -$313.00 | premium 0.93% of collateral |
| 3 | SIMQ-W02-P51 | W2 mid | $51 | 1.35 / 1.43 | $135.00 | $5,100.00 cash | Expired worthless (Fri SimQ 52.22) | premium 2.65% of collateral |
| 4 | SIMQ-W03-P42 | W3 open | $42 | 0.43 / 0.47 | $43.00 | $4,200.00 cash | Bought to close at 1.95 ($195.00), net -$152.00 | premium 1.02% of collateral |
| 5 | SIMQ-W03-P40 | W3 mid | $40 | 1.01 / 1.07 | $101.00 | $4,000.00 cash | ASSIGNED: bought 100 at $40.00 (Fri SimQ 31.30) | premium 2.53% of collateral |
| 6 | SIMQ-W04-P26 | W4 open | $26 | 0.48 / 0.52 | $48.00 | $2,600.00 cash | Bought to close at 0.67 ($67.00), net -$19.00 | premium 1.85% of collateral |
| 7 | SIMQ-W04-C36 | W4 open | $36 | 0.29 / 0.32 | $29.00 | lot 1 | Bought to close at 0.01 ($1.00), net +$28.00 | premium 0.93% of share value |
| 8 | SIMQ-W04-P23 | W4 mid | $23 | 0.11 / 0.12 | $11.00 | $2,300.00 cash | Expired worthless (Fri SimQ 26.33) | premium 0.48% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | calm_up | 63.80 | 65.24 | 61.20 | 60.29 | 59.12 | 58.99 | -7.5% | 5.77 (7,525.00 x 3d; 7,523.00 x 4d) |
| 2 | selloff | 58.99 | 58.06 | 54.71 | 52.19 | 53.96 | 52.22 | -11.5% | 5.71 (7,579.77 x 3d; 7,350.77 x 4d) |
| 3 | crash | 52.22 | 52.24 | 42.32 | 41.41 | 32.41 | 31.30 | -40.1% | 4.76 (7,399.48 x 3d; 7,305.48 x 2d; 3,305.48 x 2d) |
| 4 | crash | 31.30 | 30.70 | 27.65 | 27.08 | 26.72 | 26.33 | -15.9% | 2.57 (3,387.24 x 3d; 3,330.24 x 4d) |

## Scorecard
- 8 trades: 2 expired worthless, 2 closed for profit, 3 closed at a loss, 1 assigned, 0 called away | win rate 25% (50% counting profitable closes)
- Avg put premium: 1.42% of collateral
- Avg call premium: 0.93% of share value at sale
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
