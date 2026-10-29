# SimQ Run 7 Ledger

- Seed: 104391084 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-007-journal.md

## Current state (Week 5, Monday open)
- SimQ spot: $43.39
- Cash: $3,127.47 | locked collateral: $0.00 | free: $3,127.47
- Shares: 100 SimQ bought at $46.00 in Week 4; effective basis $45.45 after option premiums
- Open positions: none
- Premium collected (gross): $220.00 | buy-to-close costs: $15.00 | interest: $22.47
- Realized P&L (options net of buy-backs + stock sales): +$205.00 (options +$205.00, stock +$0.00)
- Account value: $7,466.47 (-0.45% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56.5 | W1 open | $56.5 | 0.60 / 0.64 | $60.00 | $5,650.00 cash | Bought to close at 0.09 ($9.00), net +$51.00 | premium 1.06% of collateral |
| 2 | SIMQ-W01-P60 | W1 mid | $60 | 0.25 / 0.28 | $25.00 | $6,000.00 cash | Expired worthless (Fri SimQ 60.98) | premium 0.42% of collateral |
| 3 | SIMQ-W02-P53 | W2 open | $53 | 0.55 / 0.59 | $55.00 | $5,300.00 cash | Bought to close at 0.06 ($6.00), net +$49.00 | premium 1.04% of collateral |
| 4 | SIMQ-W03-P52.5 | W3 open | $52.5 | 0.25 / 0.27 | $25.00 | $5,250.00 cash | Expired worthless (Fri SimQ 52.70) | premium 0.48% of collateral; held at midweek (ask 1.66) |
| 5 | SIMQ-W04-P46 | W4 open | $46 | 0.55 / 0.59 | $55.00 | $4,600.00 cash | ASSIGNED: bought 100 at $46.00 (Fri SimQ 43.39) | premium 1.20% of collateral; held at midweek (ask 1.57) |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 68.24 | 66.43 | 66.34 | 62.08 | 60.98 | -4.4% | 5.81 (7,560.00 x 3d; 7,576.00 x 4d) |
| 2 | calm_up | 60.98 | 59.71 | 57.59 | 58.25 | 57.16 | 57.84 | -5.1% | 5.86 (7,636.81 x 3d; 7,630.81 x 4d) |
| 3 | chop | 57.84 | 57.46 | 55.94 | 52.70 | 54.49 | 52.70 | -8.9% | 5.88 (7,661.67 x 7d) |
| 4 | selloff | 52.70 | 49.82 | 50.39 | 46.63 | 44.87 | 43.39 | -17.7% | 4.92 (7,722.55 x 5d; 3,122.55 x 2d) |

## Scorecard
- 5 trades: 2 expired worthless, 2 closed for profit, 0 closed at a loss, 1 assigned, 0 called away | win rate 40% (80% counting profitable closes)
- Avg put premium: 0.84% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
