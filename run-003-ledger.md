# SimQ Run 3 Ledger

- Seed: 943118079 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-003-journal.md

## Current state (Week 33, Monday open)
- SimQ spot: $17.94
- Cash: $1,508.88 | locked collateral: $0.00 | free: $1,508.88
- Shares: 100 SimQ bought at $50.00 in Week 28; effective basis $48.73 after option premiums
- Shares: 100 SimQ bought at $33.00 in Week 30; effective basis $32.89 after option premiums
- Open positions: none
- Premium collected (gross): $2,091.00 | buy-to-close costs: $1,231.00 | interest: $148.88
- Realized P&L (options net of buy-backs + stock sales): +$2,160.00 (options +$860.00, stock +$1,300.00)
- Account value: $5,096.88 (-32.04% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Expired worthless (Fri SimQ 61.87) | premium 0.95% of collateral; held at midweek (ask 0.83) |
| 2 | SIMQ-W02-P51 | W2 open | $51 | 0.47 / 0.50 | $47.00 | $5,100.00 cash | Expired worthless (Fri SimQ 51.56) | premium 0.92% of collateral; held at midweek (ask 0.35) |
| 3 | SIMQ-W03-P38 | W3 open | $38 | 0.40 / 0.43 | $40.00 | $3,800.00 cash | Bought to close at 0.01 ($1.00), net +$39.00 | premium 1.05% of collateral |
| 4 | SIMQ-W03-P48 | W3 mid | $48 | 0.42 / 0.46 | $42.00 | $4,800.00 cash | Expired worthless (Fri SimQ 55.28) | premium 0.87% of collateral |
| 5 | SIMQ-W04-P45 | W4 open | $45 | 0.45 / 0.49 | $45.00 | $4,500.00 cash | Bought to close at 0.01 ($1.00), net +$44.00 | premium 1.00% of collateral |
| 6 | SIMQ-W04-P54 | W4 mid | $54 | 0.26 / 0.29 | $26.00 | $5,400.00 cash | Expired worthless (Fri SimQ 54.86) | premium 0.48% of collateral |
| 7 | SIMQ-W05-P48 | W5 open | $48 | 0.50 / 0.54 | $50.00 | $4,800.00 cash | Bought to close at 0.03 ($3.00), net +$47.00 | premium 1.04% of collateral |
| 8 | SIMQ-W05-P55 | W5 mid | $55 | 0.40 / 0.43 | $40.00 | $5,500.00 cash | ASSIGNED: bought 100 at $55.00 (Fri SimQ 54.88) | premium 0.73% of collateral |
| 9 | SIMQ-W06-C59 | W6 open | $59 | 1.19 / 1.26 | $119.00 | lot 1 | Bought to close at 4.01 ($401.00), net -$282.00 | premium 2.17% of share value |
| 10 | SIMQ-W06-C62 | W6 mid | $62 | 1.97 / 2.08 | $197.00 | lot 1 | CALLED AWAY: sold 100 at $62.00 (Fri SimQ 74.90) | premium 3.18% of share value |
| 11 | SIMQ-W07-P64.5 | W7 open | $64.5 | 1.04 / 1.10 | $104.00 | $6,450.00 cash | Bought to close at 0.73 ($73.00), net +$31.00 | premium 1.61% of collateral |
| 12 | SIMQ-W07-P62 | W7 mid | $62 | 0.19 / 0.21 | $19.00 | $6,200.00 cash | Expired worthless (Fri SimQ 63.92) | premium 0.31% of collateral |
| 13 | SIMQ-W08-P56 | W8 mid | $56 | 0.13 / 0.15 | $13.00 | $5,600.00 cash | Expired worthless (Fri SimQ 59.84) | premium 0.23% of collateral |
| 14 | SIMQ-W09-P54 | W9 open | $54 | 0.24 / 0.27 | $24.00 | $5,400.00 cash | Bought to close at 4.20 ($420.00), net -$396.00 | premium 0.44% of collateral |
| 15 | SIMQ-W09-P49 | W9 mid | $49 | 1.31 / 1.39 | $131.00 | $4,900.00 cash | ASSIGNED: bought 100 at $49.00 (Fri SimQ 45.34) | premium 2.67% of collateral |
| 16 | SIMQ-W10-C50 | W10 open | $50 | 0.55 / 0.59 | $55.00 | lot 2 | Expired worthless (Fri SimQ 46.73) | premium 1.21% of share value; held at midweek (ask 0.19) |
| 17 | SIMQ-W10-P30 | W10 open | $30 | 0.03 / 0.04 | $3.00 | $3,000.00 cash | Expired worthless (Fri SimQ 46.73) | premium 0.10% of collateral; held at midweek (ask 0.01) |
| 18 | SIMQ-W11-C50 | W11 open | $50 | 0.61 / 0.66 | $61.00 | lot 2 | Expired worthless (Fri SimQ 39.04) | premium 1.31% of share value; held at midweek (ask 0.05) |
| 19 | SIMQ-W12-P30 | W12 open | $30 | 0.32 / 0.35 | $32.00 | $3,000.00 cash | Bought to close at 0.01 ($1.00), net +$31.00 | premium 1.07% of collateral |
| 20 | SIMQ-W12-C46 | W12 open | $46 | 0.21 / 0.23 | $21.00 | lot 2 | Bought to close at 0.01 ($1.00), net +$20.00 | premium 0.54% of share value |
| 21 | SIMQ-W13-P34 | W13 open | $34 | 0.13 / 0.15 | $13.00 | $3,400.00 cash | Bought to close at 0.02 ($2.00), net +$11.00 | premium 0.38% of collateral |
| 22 | SIMQ-W14-C49 | W14 open | $49 | 0.18 / 0.19 | $18.00 | lot 2 | Expired worthless (Fri SimQ 45.99) | premium 0.41% of share value; held at midweek (ask 0.05) |
| 23 | SIMQ-W14-P35 | W14 open | $35 | 0.11 / 0.13 | $11.00 | $3,500.00 cash | Bought to close at 0.01 ($1.00), net +$10.00 | premium 0.31% of collateral |
| 24 | SIMQ-W16-C50 | W16 open | $50 | 0.28 / 0.31 | $28.00 | lot 2 | Bought to close at 0.01 ($1.00), net +$27.00 | premium 0.64% of share value |
| 25 | SIMQ-W16-P34 | W16 open | $34 | 0.17 / 0.18 | $17.00 | $3,400.00 cash | Expired worthless (Fri SimQ 49.02) | premium 0.50% of collateral; held at midweek (ask 0.05) |
| 26 | SIMQ-W17-C55 | W17 open | $55 | 0.46 / 0.50 | $46.00 | lot 2 | Expired worthless (Fri SimQ 47.49) | premium 0.94% of share value; held at midweek (ask 0.01) |
| 27 | SIMQ-W17-P32.5 | W17 open | $32.5 | 0.04 / 0.05 | $4.00 | $3,250.00 cash | Expired worthless (Fri SimQ 47.49) | premium 0.12% of collateral; held at midweek (ask 0.01) |
| 28 | SIMQ-W18-C52 | W18 open | $52 | 0.17 / 0.19 | $17.00 | lot 2 | Bought to close at 0.42 ($42.00), net -$25.00 | premium 0.36% of share value |
| 29 | SIMQ-W18-C53 | W18 mid | $53 | 0.17 / 0.19 | $17.00 | lot 2 | Expired worthless (Fri SimQ 51.57) | premium 0.34% of share value |
| 30 | SIMQ-W19-C54 | W19 open | $54 | 0.62 / 0.66 | $62.00 | lot 2 | Expired worthless (Fri SimQ 51.49) | premium 1.20% of share value; held at midweek (ask 0.45) |
| 31 | SIMQ-W20-C55 | W20 open | $55 | 0.83 / 0.88 | $83.00 | lot 2 | CALLED AWAY: sold 100 at $55.00 (Fri SimQ 57.68) | premium 1.61% of share value; held at midweek (ask 1.02) |
| 32 | SIMQ-W21-P49 | W21 open | $49 | 0.23 / 0.25 | $23.00 | $4,900.00 cash | Expired worthless (Fri SimQ 52.07) | premium 0.47% of collateral; held at midweek (ask 0.17) |
| 33 | SIMQ-W22-P46 | W22 open | $46 | 0.57 / 0.61 | $57.00 | $4,600.00 cash | Expired worthless (Fri SimQ 46.02) | premium 1.24% of collateral; held at midweek (ask 1.28) |
| 34 | SIMQ-W22-P42 | W22 mid | $42 | 0.27 / 0.30 | $27.00 | $4,200.00 cash | Expired worthless (Fri SimQ 46.02) | premium 0.64% of collateral |
| 35 | SIMQ-W23-P38 | W23 open | $38 | 0.35 / 0.38 | $35.00 | $3,800.00 cash | Bought to close at 0.01 ($1.00), net +$34.00 | premium 0.92% of collateral |
| 36 | SIMQ-W23-P36 | W23 open | $36 | 0.20 / 0.22 | $20.00 | $3,600.00 cash | Bought to close at 0.01 ($1.00), net +$19.00 | premium 0.56% of collateral |
| 37 | SIMQ-W24-P44 | W24 mid | $44 | 0.09 / 0.10 | $9.00 | $4,400.00 cash | Expired worthless (Fri SimQ 48.04) | premium 0.20% of collateral |
| 38 | SIMQ-W25-P47 | W25 open | $47 | 0.91 / 0.97 | $91.00 | $4,700.00 cash | Bought to close at 0.12 ($12.00), net +$79.00 | premium 1.94% of collateral |
| 39 | SIMQ-W25-P44 | W25 mid | $44 | 0.01 / 0.02 | $1.00 | $4,400.00 cash | Expired worthless (Fri SimQ 54.53) | premium 0.02% of collateral |
| 40 | SIMQ-W26-P49 | W26 open | $49 | 0.64 / 0.69 | $64.00 | $4,900.00 cash | Expired worthless (Fri SimQ 51.27) | premium 1.31% of collateral; held at midweek (ask 0.44) |
| 41 | SIMQ-W26-P48 | W26 open | $48 | 0.49 / 0.53 | $49.00 | $4,800.00 cash | Expired worthless (Fri SimQ 51.27) | premium 1.02% of collateral; held at midweek (ask 0.31) |
| 42 | SIMQ-W27-P43 | W27 open | $43 | 0.51 / 0.54 | $51.00 | $4,300.00 cash | Bought to close at 0.02 ($2.00), net +$49.00 | premium 1.19% of collateral |
| 43 | SIMQ-W27-P41 | W27 open | $41 | 0.31 / 0.34 | $31.00 | $4,100.00 cash | Bought to close at 0.01 ($1.00), net +$30.00 | premium 0.76% of collateral |
| 44 | SIMQ-W27-P47 | W27 mid | $47 | 0.07 / 0.08 | $7.00 | $4,700.00 cash | Expired worthless (Fri SimQ 58.11) | premium 0.15% of collateral |
| 45 | SIMQ-W28-P50 | W28 open | $50 | 0.50 / 0.54 | $50.00 | $5,000.00 cash | ASSIGNED: bought 100 at $50.00 (Fri SimQ 45.12) | premium 1.00% of collateral; held at midweek (ask 4.90) |
| 46 | SIMQ-W28-P47 | W28 open | $47 | 0.23 / 0.26 | $23.00 | $4,700.00 cash | Bought to close at 2.65 ($265.00), net -$242.00 | premium 0.49% of collateral |
| 47 | SIMQ-W28-P35 | W28 mid | $35 | 0.03 / 0.04 | $3.00 | $3,500.00 cash | Expired worthless (Fri SimQ 45.12) | premium 0.09% of collateral |
| 48 | SIMQ-W29-C52 | W29 open | $52 | 0.37 / 0.40 | $37.00 | lot 3 | Bought to close at 0.01 ($1.00), net +$36.00 | premium 0.82% of share value |
| 49 | SIMQ-W29-P33 | W29 open | $33 | 0.23 / 0.25 | $23.00 | $3,300.00 cash | Bought to close at 0.01 ($1.00), net +$22.00 | premium 0.70% of collateral |
| 50 | SIMQ-W30-C51 | W30 open | $51 | 0.15 / 0.17 | $15.00 | lot 3 | Expired worthless (Fri SimQ 32.95) | premium 0.34% of share value; held at midweek (ask 0.01) |
| 51 | SIMQ-W30-P33 | W30 open | $33 | 0.11 / 0.13 | $11.00 | $3,300.00 cash | ASSIGNED: bought 100 at $33.00 (Fri SimQ 32.95) | premium 0.33% of collateral; held at midweek (ask 0.78) |
| 52 | SIMQ-W31-C34 | W31 mid | $34 | 0.26 / 0.29 | $26.00 | lot 3 | Expired worthless (Fri SimQ 27.36) | premium 0.84% of share value |

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W5 at $55.00 | W6 at $62.00 | +$700.00 | +$655.00 |
| W9 at $49.00 | W20 at $55.00 | +$600.00 | +$1,095.00 |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | selloff | 63.80 | 63.00 | 62.42 | 60.08 | 61.77 | 61.87 | -3.0% | 5.79 (7,553.00 x 7d) |
| 2 | crash | 61.87 | 56.24 | 56.98 | 58.00 | 53.51 | 51.56 | -16.7% | 5.83 (7,605.79 x 7d) |
| 3 | rebound | 51.56 | 52.83 | 52.73 | 52.59 | 54.90 | 55.28 | +7.2% | 5.89 (7,651.62 x 3d; 7,692.62 x 4d) |
| 4 | chop | 55.28 | 58.25 | 56.60 | 59.03 | 55.58 | 54.86 | -0.8% | 5.95 (7,743.51 x 3d; 7,768.51 x 4d) |
| 5 | rebound | 54.86 | 60.36 | 58.58 | 60.70 | 55.41 | 54.88 | +0.0% | 4.81 (7,824.46 x 3d; 7,861.46 x 2d; 2,361.46 x 2d) |
| 6 | rebound | 54.88 | 55.44 | 59.09 | 61.88 | 67.71 | 74.90 | +36.5% | 3.18 (2,485.27 x 3d; 2,281.27 x 2d; 8,481.27 x 2d) |
| 7 | calm_up | 74.90 | 74.37 | 65.78 | 65.90 | 63.35 | 63.92 | -14.7% | 6.56 (8,588.45 x 3d; 8,534.45 x 4d) |
| 8 | calm_up | 63.92 | 62.61 | 60.52 | 60.02 | 59.07 | 59.84 | -6.4% | 6.56 (8,541.01 x 3d; 8,554.01 x 4d) |
| 9 | chop | 59.84 | 60.11 | 56.81 | 50.51 | 48.57 | 45.34 | -24.2% | 5.38 (8,584.57 x 3d; 8,295.57 x 2d; 3,395.57 x 2d) |
| 10 | chop | 45.34 | 46.34 | 47.13 | 46.41 | 46.85 | 46.73 | +3.1% | 2.65 (3,458.95 x 7d) |
| 11 | selloff | 46.73 | 47.45 | 46.48 | 43.09 | 41.61 | 39.04 | -16.5% | 2.70 (3,522.60 x 7d) |
| 12 | calm_up | 39.04 | 39.26 | 39.49 | 40.12 | 40.44 | 39.38 | +0.9% | 2.74 (3,578.30 x 3d; 3,576.30 x 4d) |
| 13 | chop | 39.38 | 38.51 | 39.40 | 40.44 | 41.10 | 43.48 | +10.4% | 2.75 (3,592.04 x 3d; 3,590.04 x 4d) |
| 14 | calm_up | 43.48 | 44.25 | 45.03 | 45.62 | 46.05 | 45.99 | +5.8% | 2.78 (3,621.79 x 3d; 3,620.79 x 4d) |
| 15 | selloff | 45.99 | 44.75 | 44.31 | 42.33 | 42.83 | 44.03 | -4.3% | 2.78 (3,623.57 x 7d) |
| 16 | rebound | 44.03 | 44.14 | 43.03 | 41.90 | 43.78 | 49.02 | +11.3% | 2.82 (3,671.35 x 3d; 3,670.35 x 4d) |
| 17 | calm_up | 49.02 | 45.86 | 47.15 | 47.29 | 48.05 | 47.49 | -3.1% | 2.86 (3,723.17 x 7d) |
| 18 | calm_up | 47.49 | 50.39 | 48.74 | 50.60 | 50.07 | 51.57 | +8.6% | 2.86 (3,743.03 x 3d; 3,718.03 x 4d) |
| 19 | chop | 51.57 | 51.75 | 51.42 | 51.36 | 52.23 | 51.49 | -0.2% | 2.90 (3,782.89 x 7d) |
| 20 | chop | 51.49 | 52.66 | 53.66 | 53.88 | 56.36 | 57.68 | +12.0% | 4.17 (3,868.79 x 5d; 9,368.79 x 2d) |
| 21 | chop | 57.68 | 55.54 | 55.75 | 54.87 | 53.35 | 52.07 | -9.7% | 7.21 (9,395.96 x 7d) |
| 22 | selloff | 52.07 | 50.01 | 47.73 | 46.83 | 45.54 | 46.02 | -11.6% | 7.27 (9,460.17 x 3d; 9,487.17 x 4d) |
| 23 | calm_up | 46.02 | 47.43 | 47.93 | 46.31 | 47.33 | 46.31 | +0.6% | 7.32 (9,549.44 x 3d; 9,547.44 x 4d) |
| 24 | calm_up | 46.31 | 45.95 | 47.31 | 47.37 | 47.26 | 48.04 | +3.7% | 7.33 (9,554.76 x 3d; 9,563.76 x 4d) |
| 25 | chop | 48.04 | 47.55 | 48.12 | 52.60 | 54.71 | 54.53 | +13.5% | 7.41 (9,662.09 x 3d; 9,651.09 x 4d) |
| 26 | selloff | 54.53 | 53.95 | 53.43 | 53.51 | 51.64 | 51.27 | -6.0% | 7.50 (9,771.50 x 7d) |
| 27 | chop | 51.27 | 52.14 | 59.69 | 56.40 | 59.12 | 58.11 | +13.3% | 7.57 (9,861.00 x 3d; 9,865.00 x 4d) |
| 28 | selloff | 58.11 | 56.56 | 48.31 | 45.48 | 47.87 | 45.12 | -22.4% | 6.42 (9,945.57 x 3d; 9,683.57 x 2d; 4,683.57 x 2d) |
| 29 | selloff | 45.12 | 43.65 | 42.65 | 43.64 | 42.85 | 43.96 | -2.6% | 3.64 (4,749.99 x 3d; 4,747.99 x 4d) |
| 30 | selloff | 43.96 | 39.35 | 37.90 | 34.76 | 32.39 | 32.95 | -25.0% | 2.94 (4,777.63 x 5d; 1,477.63 x 2d) |
| 31 | selloff | 32.95 | 34.07 | 34.31 | 31.04 | 29.03 | 27.36 | -17.0% | 1.15 (1,480.57 x 3d; 1,506.57 x 4d) |
| 32 | crash | 27.36 | 21.78 | 23.23 | 22.12 | 20.98 | 17.94 | -34.4% | 1.16 (1,507.72 x 7d) |

## Scorecard
- 52 trades: 26 expired worthless, 16 closed for profit, 4 closed at a loss, 4 assigned, 2 called away | win rate 50% (81% counting profitable closes)
- Avg put premium: 0.75% of collateral
- Avg call premium: 1.06% of share value at sale
- Wheel cycles completed (shares called away): 2
- Account value at week 26 (comparison metric): $9,779.00 (+30.39%) | buy-and-hold SimQ $6,027.04 (-19.64%) | cash only $7,649.59 (+1.99%)
