# SimQ Run 7 Ledger

- Seed: 104391084 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-007-journal.md

## Current state (Week 22, Monday open)
- SimQ spot: $33.75
- Cash: $3,668.10 | locked collateral: $0.00 | free: $3,668.10
- Shares: 100 SimQ bought at $46.00 in Week 4; effective basis $44.49 after option premiums
- Open positions: none
- Premium collected (gross): $725.00 | buy-to-close costs: $24.00 | interest: $67.10
- Realized P&L (options net of buy-backs + stock sales): +$701.00 (options +$701.00, stock +$0.00)
- Account value: $7,043.10 (-6.09% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56.5 | W1 open | $56.5 | 0.60 / 0.64 | $60.00 | $5,650.00 cash | Bought to close at 0.09 ($9.00), net +$51.00 | premium 1.06% of collateral |
| 2 | SIMQ-W01-P60 | W1 mid | $60 | 0.25 / 0.28 | $25.00 | $6,000.00 cash | Expired worthless (Fri SimQ 60.98) | premium 0.42% of collateral |
| 3 | SIMQ-W02-P53 | W2 open | $53 | 0.55 / 0.59 | $55.00 | $5,300.00 cash | Bought to close at 0.06 ($6.00), net +$49.00 | premium 1.04% of collateral |
| 4 | SIMQ-W03-P52.5 | W3 open | $52.5 | 0.25 / 0.27 | $25.00 | $5,250.00 cash | Expired worthless (Fri SimQ 52.70) | premium 0.48% of collateral; held at midweek (ask 1.66) |
| 5 | SIMQ-W04-P46 | W4 open | $46 | 0.55 / 0.59 | $55.00 | $4,600.00 cash | ASSIGNED: bought 100 at $46.00 (Fri SimQ 43.39) | premium 1.20% of collateral; held at midweek (ask 1.57) |
| 6 | SIMQ-W05-C46.5 | W5 open | $46.5 | 0.94 / 1.00 | $94.00 | lot 1 | Expired worthless (Fri SimQ 39.90) | premium 2.17% of share value; held at midweek (ask 0.13) |
| 7 | SIMQ-W06-C47 | W6 open | $47 | 0.02 / 0.03 | $2.00 | lot 1 | Bought to close at 0.01 ($1.00), net +$1.00 | premium 0.05% of share value |
| 8 | SIMQ-W06-P30 | W6 open | $30 | 0.03 / 0.04 | $3.00 | $3,000.00 cash | Expired worthless (Fri SimQ 40.92) | premium 0.10% of collateral; held at midweek (ask 0.01) |
| 9 | SIMQ-W09-P22 | W9 open | $22 | 0.21 / 0.23 | $21.00 | $2,200.00 cash | Bought to close at 0.02 ($2.00), net +$19.00 | premium 0.95% of collateral |
| 10 | SIMQ-W09-P26 | W9 mid | $26 | 0.16 / 0.18 | $16.00 | $2,600.00 cash | Expired worthless (Fri SimQ 30.32) | premium 0.62% of collateral |
| 11 | SIMQ-W10-P26 | W10 open | $26 | 0.40 / 0.44 | $40.00 | $2,600.00 cash | Bought to close at 0.01 ($1.00), net +$39.00 | premium 1.54% of collateral |
| 12 | SIMQ-W11-P31.5 | W11 open | $31.5 | 0.35 / 0.38 | $35.00 | $3,150.00 cash | Expired worthless (Fri SimQ 39.30) | premium 1.11% of collateral; held at midweek (ask 0.34) |
| 13 | SIMQ-W12-C47 | W12 open | $47 | 0.01 / 0.02 | $1.00 | lot 1 | Expired worthless (Fri SimQ 35.92) | premium 0.03% of share value; held at midweek (ask 0.01) |
| 14 | SIMQ-W12-P33 | W12 open | $33 | 0.19 / 0.21 | $19.00 | $3,300.00 cash | Expired worthless (Fri SimQ 35.92) | premium 0.58% of collateral; held at midweek (ask 0.06) |
| 15 | SIMQ-W13-P31 | W13 open | $31 | 0.32 / 0.35 | $32.00 | $3,100.00 cash | Expired worthless (Fri SimQ 32.10) | premium 1.03% of collateral; held at midweek (ask 0.38) |
| 16 | SIMQ-W14-P27 | W14 open | $27 | 0.26 / 0.28 | $26.00 | $2,700.00 cash | Expired worthless (Fri SimQ 32.87) | premium 0.96% of collateral; held at midweek (ask 0.24) |
| 17 | SIMQ-W15-P28 | W15 open | $28 | 0.35 / 0.38 | $35.00 | $2,800.00 cash | Expired worthless (Fri SimQ 28.03) | premium 1.25% of collateral; held at midweek (ask 0.32) |
| 18 | SIMQ-W16-P24 | W16 open | $24 | 0.24 / 0.26 | $24.00 | $2,400.00 cash | Bought to close at 0.02 ($2.00), net +$22.00 | premium 1.00% of collateral |
| 19 | SIMQ-W16-P28 | W16 mid | $28 | 0.19 / 0.21 | $19.00 | $2,800.00 cash | Expired worthless (Fri SimQ 29.93) | premium 0.68% of collateral |
| 20 | SIMQ-W17-P25 | W17 open | $25 | 0.55 / 0.59 | $55.00 | $2,500.00 cash | Bought to close at 0.01 ($1.00), net +$54.00 | premium 2.20% of collateral |
| 21 | SIMQ-W18-P32 | W18 open | $32 | 0.33 / 0.36 | $33.00 | $3,200.00 cash | Bought to close at 0.02 ($2.00), net +$31.00 | premium 1.03% of collateral |
| 22 | SIMQ-W19-P32.5 | W19 open | $32.5 | 0.32 / 0.34 | $32.00 | $3,250.00 cash | Expired worthless (Fri SimQ 34.35) | premium 0.98% of collateral; held at midweek (ask 0.06) |
| 23 | SIMQ-W20-P30.5 | W20 open | $30.5 | 0.18 / 0.20 | $18.00 | $3,050.00 cash | Expired worthless (Fri SimQ 34.49) | premium 0.59% of collateral; held at midweek (ask 0.05) |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 68.24 | 66.43 | 66.34 | 62.08 | 60.98 | -4.4% | 5.81 (7,560.00 x 3d; 7,576.00 x 4d) |
| 2 | calm_up | 60.98 | 59.71 | 57.59 | 58.25 | 57.16 | 57.84 | -5.1% | 5.86 (7,636.81 x 3d; 7,630.81 x 4d) |
| 3 | chop | 57.84 | 57.46 | 55.94 | 52.70 | 54.49 | 52.70 | -8.9% | 5.88 (7,661.67 x 7d) |
| 4 | selloff | 52.70 | 49.82 | 50.39 | 46.63 | 44.87 | 43.39 | -17.7% | 4.92 (7,722.55 x 5d; 3,122.55 x 2d) |
| 5 | chop | 43.39 | 42.45 | 40.35 | 43.14 | 39.36 | 39.90 | -8.0% | 2.47 (3,221.47 x 7d) |
| 6 | calm_up | 39.90 | 39.82 | 40.70 | 40.89 | 40.55 | 40.92 | +2.6% | 2.48 (3,228.94 x 3d; 3,227.94 x 4d) |
| 7 | calm_up | 40.92 | 40.80 | 40.95 | 37.97 | 38.10 | 38.68 | -5.5% | 2.48 (3,230.42 x 7d) |
| 8 | selloff | 38.68 | 35.26 | 34.12 | 34.83 | 32.25 | 29.13 | -24.7% | 2.48 (3,232.90 x 7d) |
| 9 | rebound | 29.13 | 29.86 | 30.35 | 29.61 | 29.86 | 30.32 | +4.1% | 2.50 (3,256.38 x 3d; 3,270.38 x 4d) |
| 10 | chop | 30.32 | 30.29 | 30.53 | 33.55 | 34.33 | 35.00 | +15.4% | 2.54 (3,312.88 x 3d; 3,311.88 x 4d) |
| 11 | chop | 35.00 | 35.27 | 33.95 | 33.37 | 37.92 | 39.30 | +12.3% | 2.57 (3,349.42 x 7d) |
| 12 | selloff | 39.30 | 39.15 | 38.09 | 38.70 | 35.12 | 35.92 | -8.6% | 2.59 (3,371.99 x 7d) |
| 13 | selloff | 35.92 | 35.87 | 34.21 | 33.41 | 32.47 | 32.10 | -10.6% | 2.61 (3,406.58 x 7d) |
| 14 | rebound | 32.10 | 30.57 | 28.59 | 29.95 | 32.10 | 32.87 | +2.4% | 2.64 (3,435.19 x 7d) |
| 15 | selloff | 32.87 | 32.74 | 32.00 | 30.48 | 27.65 | 28.03 | -14.7% | 2.66 (3,472.83 x 7d) |
| 16 | rebound | 28.03 | 28.99 | 30.11 | 31.39 | 31.95 | 29.93 | +6.8% | 2.69 (3,499.49 x 3d; 3,516.49 x 4d) |
| 17 | calm_up | 29.93 | 31.10 | 32.80 | 33.30 | 33.64 | 34.06 | +13.8% | 2.74 (3,574.18 x 3d; 3,573.18 x 4d) |
| 18 | calm_up | 34.06 | 35.65 | 35.78 | 36.13 | 36.46 | 35.59 | +4.5% | 2.77 (3,608.92 x 3d; 3,606.92 x 4d) |
| 19 | calm_up | 35.59 | 35.66 | 35.91 | 35.70 | 35.27 | 34.35 | -3.5% | 2.79 (3,641.69 x 7d) |
| 20 | calm_up | 34.35 | 34.40 | 33.28 | 33.38 | 34.13 | 34.49 | +0.4% | 2.81 (3,662.48 x 7d) |
| 21 | chop | 34.49 | 33.60 | 33.78 | 31.94 | 32.73 | 33.75 | -2.1% | 2.81 (3,665.29 x 7d) |

## Scorecard
- 23 trades: 14 expired worthless, 8 closed for profit, 0 closed at a loss, 1 assigned, 0 called away | win rate 61% (96% counting profitable closes)
- Avg put premium: 0.94% of collateral
- Avg call premium: 0.75% of share value at sale
- Wheel cycles completed (shares called away): 0
- Account value at week 26 (comparison metric): pending
