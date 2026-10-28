# SimQ Run 6 Ledger

- Seed: 892542713 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-006-journal.md

## Current state (Week 16, Monday open)
- SimQ spot: $98.86
- Cash: $8,258.74 | locked collateral: $0.00 | free: $8,258.74
- Shares: 0
- Open positions: none
- Premium collected (gross): $893.00 | buy-to-close costs: $225.00 | interest: $90.74
- Realized P&L (options net of buy-backs + stock sales): +$668.00 (options +$668.00, stock +$0.00)
- Account value: $8,258.74 (+10.12% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P55 | W1 mid | $55 | 0.24 / 0.26 | $24.00 | $5,500.00 cash | Expired worthless (Fri SimQ 61.14) | premium 0.44% of collateral |
| 2 | SIMQ-W02-P53 | W2 open | $53 | 0.52 / 0.55 | $52.00 | $5,300.00 cash | Expired worthless (Fri SimQ 60.12) | premium 0.98% of collateral; held at midweek (ask 0.27) |
| 3 | SIMQ-W03-P53.5 | W3 open | $53.5 | 0.55 / 0.59 | $55.00 | $5,350.00 cash | Bought to close at 0.01 ($1.00), net +$54.00 | premium 1.03% of collateral |
| 4 | SIMQ-W03-P61 | W3 mid | $61 | 0.10 / 0.12 | $10.00 | $6,100.00 cash | Expired worthless (Fri SimQ 66.19) | premium 0.16% of collateral |
| 5 | SIMQ-W04-P63 | W4 mid | $63 | 0.16 / 0.18 | $16.00 | $6,300.00 cash | Expired worthless (Fri SimQ 66.87) | premium 0.25% of collateral |
| 6 | SIMQ-W05-P61 | W5 open | $61 | 0.40 / 0.43 | $40.00 | $6,100.00 cash | Bought to close at 0.08 ($8.00), net +$32.00 | premium 0.66% of collateral |
| 7 | SIMQ-W05-P65 | W5 mid | $65 | 0.33 / 0.36 | $33.00 | $6,500.00 cash | Expired worthless (Fri SimQ 66.39) | premium 0.51% of collateral |
| 8 | SIMQ-W06-P57 | W6 open | $57 | 0.58 / 0.62 | $58.00 | $5,700.00 cash | Bought to close at 0.01 ($1.00), net +$57.00 | premium 1.02% of collateral |
| 9 | SIMQ-W07-P62.5 | W7 open | $62.5 | 0.48 / 0.51 | $48.00 | $6,250.00 cash | Bought to close at 0.09 ($9.00), net +$39.00 | premium 0.77% of collateral |
| 10 | SIMQ-W07-P64.5 | W7 mid | $64.5 | 0.25 / 0.27 | $25.00 | $6,450.00 cash | Expired worthless (Fri SimQ 67.11) | premium 0.39% of collateral |
| 11 | SIMQ-W08-P61.5 | W8 open | $61.5 | 0.42 / 0.45 | $42.00 | $6,150.00 cash | Expired worthless (Fri SimQ 68.72) | premium 0.68% of collateral; held at midweek (ask 0.13) |
| 12 | SIMQ-W09-P61 | W9 open | $61 | 0.67 / 0.71 | $67.00 | $6,100.00 cash | Bought to close at 1.95 ($195.00), net -$128.00 | premium 1.10% of collateral |
| 13 | SIMQ-W09-P59 | W9 mid | $59 | 0.99 / 1.05 | $99.00 | $5,900.00 cash | Expired worthless (Fri SimQ 64.74) | premium 1.68% of collateral |
| 14 | SIMQ-W10-P61 | W10 open | $61 | 0.71 / 0.76 | $71.00 | $6,100.00 cash | Bought to close at 0.02 ($2.00), net +$69.00 | premium 1.16% of collateral |
| 15 | SIMQ-W12-P68 | W12 open | $68 | 0.58 / 0.62 | $58.00 | $6,800.00 cash | Bought to close at 0.05 ($5.00), net +$53.00 | premium 0.85% of collateral |
| 16 | SIMQ-W12-P71 | W12 mid | $71 | 0.24 / 0.26 | $24.00 | $7,100.00 cash | Expired worthless (Fri SimQ 74.56) | premium 0.34% of collateral |
| 17 | SIMQ-W13-P68 | W13 open | $68 | 0.60 / 0.64 | $60.00 | $6,800.00 cash | Bought to close at 0.01 ($1.00), net +$59.00 | premium 0.88% of collateral |
| 18 | SIMQ-W13-P74.5 | W13 mid | $74.5 | 0.15 / 0.17 | $15.00 | $7,450.00 cash | Expired worthless (Fri SimQ 83.57) | premium 0.20% of collateral |
| 19 | SIMQ-W14-P81 | W14 mid | $81 | 0.47 / 0.50 | $47.00 | $8,100.00 cash | Expired worthless (Fri SimQ 92.32) | premium 0.58% of collateral |
| 20 | SIMQ-W15-P78 | W15 open | $78 | 0.49 / 0.52 | $49.00 | $7,800.00 cash | Bought to close at 0.03 ($3.00), net +$46.00 | premium 0.63% of collateral |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 60.66 | 61.34 | 60.88 | 62.29 | 61.14 | -4.2% | 5.76 (7,500.00 x 3d; 7,524.00 x 4d) |
| 2 | chop | 61.14 | 61.64 | 58.91 | 58.18 | 59.10 | 60.12 | -1.7% | 5.82 (7,581.76 x 7d) |
| 3 | calm_up | 60.12 | 61.53 | 63.24 | 66.02 | 66.71 | 66.19 | +10.1% | 5.87 (7,642.58 x 3d; 7,651.58 x 4d) |
| 4 | calm_up | 66.19 | 66.34 | 66.66 | 67.40 | 67.40 | 66.87 | +1.0% | 5.88 (7,657.45 x 3d; 7,673.45 x 4d) |
| 5 | chop | 66.87 | 67.09 | 69.61 | 70.53 | 67.58 | 66.39 | -0.7% | 5.93 (7,719.33 x 3d; 7,744.33 x 4d) |
| 6 | calm_up | 66.39 | 66.00 | 66.00 | 67.54 | 68.80 | 68.07 | +2.5% | 5.99 (7,808.26 x 3d; 7,807.26 x 4d) |
| 7 | calm_up | 68.07 | 66.59 | 67.73 | 68.27 | 64.91 | 67.11 | -1.4% | 6.04 (7,861.25 x 3d; 7,877.25 x 4d) |
| 8 | chop | 67.11 | 66.92 | 67.21 | 69.87 | 69.07 | 68.72 | +2.4% | 6.08 (7,925.29 x 7d) |
| 9 | calm_up | 68.72 | 71.64 | 66.56 | 60.82 | 62.58 | 64.74 | -5.8% | 6.09 (7,998.37 x 3d; 7,902.37 x 4d) |
| 10 | calm_up | 64.74 | 64.92 | 65.51 | 70.19 | 70.30 | 73.30 | +13.2% | 6.12 (7,979.46 x 3d; 7,977.46 x 4d) |
| 11 | calm_up | 73.30 | 75.38 | 75.00 | 71.14 | 76.22 | 74.71 | +1.9% | 6.12 (7,983.58 x 7d) |
| 12 | calm_up | 74.71 | 75.29 | 74.24 | 74.95 | 75.88 | 74.56 | -0.2% | 6.18 (8,047.70 x 3d; 8,066.70 x 4d) |
| 13 | calm_up | 74.56 | 74.09 | 76.51 | 80.49 | 81.26 | 83.57 | +12.1% | 6.25 (8,132.88 x 3d; 8,146.88 x 4d) |
| 14 | chop | 83.57 | 89.72 | 94.40 | 90.51 | 89.35 | 92.32 | +10.5% | 6.28 (8,153.13 x 3d; 8,200.13 x 4d) |
| 15 | chop | 92.32 | 91.29 | 96.27 | 96.73 | 88.49 | 98.86 | +7.1% | 6.33 (8,255.41 x 3d; 8,252.41 x 4d) |

## Scorecard
- 20 trades: 11 expired worthless, 8 closed for profit, 1 closed at a loss, 0 assigned, 0 called away | win rate 55% (95% counting profitable closes)
- Avg put premium: 0.72% of collateral
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
