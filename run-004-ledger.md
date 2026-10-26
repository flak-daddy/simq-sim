# SimQ Run 4 Ledger

- Seed: 867728425 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-004-journal.md

## Current state (Week 51, Monday open)
- SimQ spot: $9.81
- Cash: $2,503.40 | locked collateral: $0.00 | free: $2,503.40
- Shares: 100 SimQ bought at $25.00 in Week 30; effective basis $24.79 after option premiums
- Shares: 100 SimQ bought at $12.00 in Week 45; effective basis $11.31 after option premiums
- Shares: 100 SimQ bought at $13.00 in Week 45; effective basis $12.43 after option premiums
- Shares: 100 SimQ bought at $10.50 in Week 46; effective basis $10.04 after option premiums
- Open positions: none
- Premium collected (gross): $1,821.00 | buy-to-close costs: $1,118.00 | interest: $250.40
- Realized P&L (options net of buy-backs + stock sales): +$803.00 (options +$703.00, stock +$100.00)
- Account value: $6,427.40 (-14.30% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Expired worthless (Fri SimQ 65.42) | premium 0.95% of collateral; held at midweek (ask 0.13) |
| 2 | SIMQ-W02-P56.5 | W2 open | $56.5 | 0.76 / 0.81 | $76.00 | $5,650.00 cash | Bought to close at 0.02 ($2.00), net +$74.00 | premium 1.35% of collateral |
| 3 | SIMQ-W02-P62 | W2 mid | $62 | 0.13 / 0.14 | $13.00 | $6,200.00 cash | Expired worthless (Fri SimQ 69.10) | premium 0.21% of collateral |
| 4 | SIMQ-W03-P60 | W3 open | $60 | 0.52 / 0.56 | $52.00 | $6,000.00 cash | Bought to close at 0.13 ($13.00), net +$39.00 | premium 0.87% of collateral |
| 5 | SIMQ-W03-P63.5 | W3 mid | $63.5 | 0.31 / 0.34 | $31.00 | $6,350.00 cash | Expired worthless (Fri SimQ 67.23) | premium 0.49% of collateral |
| 6 | SIMQ-W04-P55 | W4 open | $55 | 0.72 / 0.77 | $72.00 | $5,500.00 cash | Bought to close at 2.64 ($264.00), net -$192.00 | premium 1.31% of collateral |
| 7 | SIMQ-W04-P50 | W4 mid | $50 | 1.03 / 1.09 | $103.00 | $5,000.00 cash | Expired worthless (Fri SimQ 62.24) | premium 2.06% of collateral |
| 8 | SIMQ-W05-P53 | W5 open | $53 | 0.73 / 0.78 | $73.00 | $5,300.00 cash | Bought to close at 0.05 ($5.00), net +$68.00 | premium 1.38% of collateral |
| 9 | SIMQ-W05-P54.5 | W5 mid | $54.5 | 0.09 / 0.10 | $9.00 | $5,450.00 cash | Expired worthless (Fri SimQ 66.31) | premium 0.17% of collateral |
| 10 | SIMQ-W06-P58 | W6 open | $58 | 0.59 / 0.63 | $59.00 | $5,800.00 cash | Expired worthless (Fri SimQ 61.64) | premium 1.02% of collateral; held at midweek (ask 0.25) |
| 11 | SIMQ-W07-P50 | W7 open | $50 | 0.57 / 0.61 | $57.00 | $5,000.00 cash | Bought to close at 3.81 ($381.00), net -$324.00 | premium 1.14% of collateral |
| 12 | SIMQ-W07-P45 | W7 mid | $45 | 1.13 / 1.20 | $113.00 | $4,500.00 cash | ASSIGNED: bought 100 at $45.00 (Fri SimQ 38.80) | premium 2.51% of collateral |
| 13 | SIMQ-W08-P25 | W8 open | $25 | 0.31 / 0.33 | $31.00 | $2,500.00 cash | Bought to close at 0.01 ($1.00), net +$30.00 | premium 1.24% of collateral |
| 14 | SIMQ-W09-C49 | W9 open | $49 | 0.67 / 0.72 | $67.00 | lot 1 | Bought to close at 0.06 ($6.00), net +$61.00 | premium 1.50% of share value |
| 15 | SIMQ-W09-C46 | W9 mid | $46 | 0.74 / 0.79 | $74.00 | lot 1 | CALLED AWAY: sold 100 at $46.00 (Fri SimQ 46.23) | premium 1.62% of share value |
| 16 | SIMQ-W11-P35 | W11 open | $35 | 0.13 / 0.15 | $13.00 | $3,500.00 cash | Bought to close at 0.01 ($1.00), net +$12.00 | premium 0.37% of collateral |
| 17 | SIMQ-W12-P35 | W12 open | $35 | 0.03 / 0.04 | $3.00 | $3,500.00 cash | Expired worthless (Fri SimQ 40.47) | premium 0.09% of collateral; held at midweek (ask 0.01) |
| 18 | SIMQ-W13-P36 | W13 open | $36 | 0.15 / 0.17 | $15.00 | $3,600.00 cash | Expired worthless (Fri SimQ 40.35) | premium 0.42% of collateral; held at midweek (ask 0.04) |
| 19 | SIMQ-W14-P35 | W14 open | $35 | 0.28 / 0.30 | $28.00 | $3,500.00 cash | Expired worthless (Fri SimQ 35.53) | premium 0.80% of collateral; held at midweek (ask 0.20) |
| 20 | SIMQ-W16-P22 | W16 open | $22 | 0.06 / 0.08 | $6.00 | $2,200.00 cash | Expired worthless (Fri SimQ 28.83) | premium 0.27% of collateral; held at midweek (ask 0.01) |
| 21 | SIMQ-W16-P24 | W16 open | $24 | 0.17 / 0.19 | $17.00 | $2,400.00 cash | Bought to close at 0.01 ($1.00), net +$16.00 | premium 0.71% of collateral |
| 22 | SIMQ-W17-P24 | W17 open | $24 | 0.12 / 0.14 | $12.00 | $2,400.00 cash | Expired worthless (Fri SimQ 26.89) | premium 0.50% of collateral; held at midweek (ask 0.06) |
| 23 | SIMQ-W17-P25 | W17 open | $25 | 0.22 / 0.24 | $22.00 | $2,500.00 cash | Expired worthless (Fri SimQ 26.89) | premium 0.88% of collateral; held at midweek (ask 0.14) |
| 24 | SIMQ-W18-P23 | W18 open | $23 | 0.22 / 0.25 | $22.00 | $2,300.00 cash | Bought to close at 0.01 ($1.00), net +$21.00 | premium 0.96% of collateral |
| 25 | SIMQ-W19-P25 | W19 open | $25 | 0.21 / 0.23 | $21.00 | $2,500.00 cash | Bought to close at 0.02 ($2.00), net +$19.00 | premium 0.84% of collateral |
| 26 | SIMQ-W20-P26 | W20 open | $26 | 0.32 / 0.35 | $32.00 | $2,600.00 cash | Expired worthless (Fri SimQ 27.37) | premium 1.23% of collateral; held at midweek (ask 0.27) |
| 27 | SIMQ-W20-P23 | W20 mid | $23 | 0.01 / 0.02 | $1.00 | $2,300.00 cash | Expired worthless (Fri SimQ 27.37) | premium 0.04% of collateral |
| 28 | SIMQ-W21-P24 | W21 open | $24 | 0.28 / 0.31 | $28.00 | $2,400.00 cash | Bought to close at 0.01 ($1.00), net +$27.00 | premium 1.17% of collateral |
| 29 | SIMQ-W22-P27 | W22 mid | $27 | 0.22 / 0.24 | $22.00 | $2,700.00 cash | Expired worthless (Fri SimQ 29.30) | premium 0.81% of collateral |
| 30 | SIMQ-W23-P26 | W23 open | $26 | 0.33 / 0.35 | $33.00 | $2,600.00 cash | Bought to close at 0.01 ($1.00), net +$32.00 | premium 1.27% of collateral |
| 31 | SIMQ-W24-P28 | W24 open | $28 | 0.22 / 0.24 | $22.00 | $2,800.00 cash | Expired worthless (Fri SimQ 31.13) | premium 0.79% of collateral; held at midweek (ask 0.09) |
| 32 | SIMQ-W26-P28 | W26 mid | $28 | 0.03 / 0.05 | $3.00 | $2,800.00 cash | Expired worthless (Fri SimQ 29.10) | premium 0.11% of collateral |
| 33 | SIMQ-W27-P23 | W27 open | $23 | 0.02 / 0.04 | $2.00 | $2,300.00 cash | Expired worthless (Fri SimQ 31.14) | premium 0.09% of collateral; held at midweek (ask 0.01) |
| 34 | SIMQ-W27-P25 | W27 open | $25 | 0.11 / 0.13 | $11.00 | $2,500.00 cash | Bought to close at 0.01 ($1.00), net +$10.00 | premium 0.44% of collateral |
| 35 | SIMQ-W28-P28 | W28 open | $28 | 0.12 / 0.14 | $12.00 | $2,800.00 cash | Expired worthless (Fri SimQ 33.46) | premium 0.43% of collateral; held at midweek (ask 0.01) |
| 36 | SIMQ-W29-P30 | W29 open | $30 | 0.11 / 0.13 | $11.00 | $3,000.00 cash | Expired worthless (Fri SimQ 31.17) | premium 0.37% of collateral; held at midweek (ask 0.17) |
| 37 | SIMQ-W30-P25 | W30 open | $25 | 0.21 / 0.23 | $21.00 | $2,500.00 cash | ASSIGNED: bought 100 at $25.00 (Fri SimQ 21.49) | premium 0.84% of collateral; held at midweek (ask 3.25) |
| 38 | SIMQ-W30-P26 | W30 open | $26 | 0.31 / 0.33 | $31.00 | $2,600.00 cash | Bought to close at 4.26 ($426.00), net -$395.00 | premium 1.19% of collateral |
| 39 | SIMQ-W31-P15 | W31 mid | $15 | 0.14 / 0.16 | $14.00 | $1,500.00 cash | Expired worthless (Fri SimQ 16.42) | premium 0.93% of collateral |
| 40 | SIMQ-W32-P10 | W32 open | $10 | 0.08 / 0.09 | $8.00 | $1,000.00 cash | Bought to close at 0.01 ($1.00), net +$7.00 | premium 0.80% of collateral |
| 41 | SIMQ-W32-P12 | W32 open | $12 | 0.23 / 0.25 | $23.00 | $1,200.00 cash | Bought to close at 0.01 ($1.00), net +$22.00 | premium 1.92% of collateral |
| 42 | SIMQ-W33-P11 | W33 open | $11 | 0.03 / 0.04 | $3.00 | $1,100.00 cash | Expired worthless (Fri SimQ 16.14) | premium 0.27% of collateral; held at midweek (ask 0.01) |
| 43 | SIMQ-W33-P12 | W33 open | $12 | 0.08 / 0.09 | $8.00 | $1,200.00 cash | Bought to close at 0.01 ($1.00), net +$7.00 | premium 0.67% of collateral |
| 44 | SIMQ-W33-P13 | W33 open | $13 | 0.18 / 0.20 | $18.00 | $1,300.00 cash | Bought to close at 0.02 ($2.00), net +$16.00 | premium 1.38% of collateral |
| 45 | SIMQ-W33-P16 | W33 mid | $16 | 0.47 / 0.50 | $47.00 | $1,600.00 cash | Expired worthless (Fri SimQ 16.14) | premium 2.94% of collateral |
| 46 | SIMQ-W34-P10 | W34 open | $10 | 0.01 / 0.02 | $1.00 | $1,000.00 cash | Expired worthless (Fri SimQ 16.42) | premium 0.10% of collateral; held at midweek (ask 0.01) |
| 47 | SIMQ-W34-P12 | W34 open | $12 | 0.07 / 0.08 | $7.00 | $1,200.00 cash | Expired worthless (Fri SimQ 16.42) | premium 0.58% of collateral; held at midweek (ask 0.01) |
| 48 | SIMQ-W34-P14 | W34 open | $14 | 0.27 / 0.30 | $27.00 | $1,400.00 cash | Expired worthless (Fri SimQ 16.42) | premium 1.93% of collateral; held at midweek (ask 0.01) |
| 49 | SIMQ-W36-P13 | W36 open | $13 | 0.18 / 0.20 | $18.00 | $1,300.00 cash | Expired worthless (Fri SimQ 14.65) | premium 1.38% of collateral; held at midweek (ask 0.20) |
| 50 | SIMQ-W37-P11 | W37 open | $11 | 0.03 / 0.04 | $3.00 | $1,100.00 cash | Expired worthless (Fri SimQ 13.97) | premium 0.27% of collateral; held at midweek (ask 0.01) |
| 51 | SIMQ-W37-P12 | W37 open | $12 | 0.09 / 0.11 | $9.00 | $1,200.00 cash | Expired worthless (Fri SimQ 13.97) | premium 0.75% of collateral; held at midweek (ask 0.04) |
| 52 | SIMQ-W40-P13 | W40 open | $13 | 0.17 / 0.19 | $17.00 | $1,300.00 cash | Expired worthless (Fri SimQ 17.60) | premium 1.31% of collateral; held at midweek (ask 0.01) |
| 53 | SIMQ-W41-P13 | W41 open | $13 | 0.05 / 0.06 | $5.00 | $1,300.00 cash | Bought to close at 0.01 ($1.00), net +$4.00 | premium 0.38% of collateral |
| 54 | SIMQ-W41-P14 | W41 open | $14 | 0.11 / 0.13 | $11.00 | $1,400.00 cash | Bought to close at 0.01 ($1.00), net +$10.00 | premium 0.79% of collateral |
| 55 | SIMQ-W41-P15 | W41 open | $15 | 0.22 / 0.24 | $22.00 | $1,500.00 cash | Bought to close at 0.01 ($1.00), net +$21.00 | premium 1.47% of collateral |
| 56 | SIMQ-W42-P16 | W42 open | $16 | 0.19 / 0.21 | $19.00 | $1,600.00 cash | Expired worthless (Fri SimQ 17.26) | premium 1.19% of collateral; held at midweek (ask 0.07) |
| 57 | SIMQ-W43-P11 | W43 mid | $11 | 0.01 / 0.02 | $1.00 | $1,100.00 cash | Expired worthless (Fri SimQ 12.03) | premium 0.09% of collateral |
| 58 | SIMQ-W43-P12 | W43 mid | $12 | 0.04 / 0.05 | $4.00 | $1,200.00 cash | Expired worthless (Fri SimQ 12.03) | premium 0.33% of collateral |
| 59 | SIMQ-W44-P9 | W44 open | $9 | 0.07 / 0.09 | $7.00 | $900.00 cash | Bought to close at 0.01 ($1.00), net +$6.00 | premium 0.78% of collateral |
| 60 | SIMQ-W44-P10 | W44 open | $10 | 0.18 / 0.20 | $18.00 | $1,000.00 cash | Bought to close at 0.01 ($1.00), net +$17.00 | premium 1.80% of collateral |
| 61 | SIMQ-W44-P10.5 | W44 open | $10.5 | 0.26 / 0.28 | $26.00 | $1,050.00 cash | Bought to close at 0.02 ($2.00), net +$24.00 | premium 2.48% of collateral |
| 62 | SIMQ-W45-P11 | W45 open | $11 | 0.09 / 0.10 | $9.00 | $1,100.00 cash | Expired worthless (Fri SimQ 11.94) | premium 0.82% of collateral; held at midweek (ask 0.01) |
| 63 | SIMQ-W45-P12 | W45 open | $12 | 0.21 / 0.23 | $21.00 | $1,200.00 cash | ASSIGNED: bought 100 at $12.00 (Fri SimQ 11.94) | premium 1.75% of collateral; held at midweek (ask 0.05) |
| 64 | SIMQ-W45-P13 | W45 open | $13 | 0.45 / 0.48 | $45.00 | $1,300.00 cash | ASSIGNED: bought 100 at $13.00 (Fri SimQ 11.94) | premium 3.46% of collateral; held at midweek (ask 0.21) |
| 65 | SIMQ-W46-C12 | W46 open | $12 | 0.48 / 0.51 | $48.00 | lot 3 | Expired worthless (Fri SimQ 9.87) | premium 4.02% of share value; held at midweek (ask 0.01) |
| 66 | SIMQ-W46-C13 | W46 open | $13 | 0.12 / 0.14 | $12.00 | lot 4 | Expired worthless (Fri SimQ 9.87) | premium 1.01% of share value; held at midweek (ask 0.01) |
| 67 | SIMQ-W46-P10.5 | W46 open | $10.5 | 0.11 / 0.12 | $11.00 | $1,050.00 cash | ASSIGNED: bought 100 at $10.50 (Fri SimQ 9.87) | premium 1.05% of collateral; held at midweek (ask 1.09) |
| 68 | SIMQ-W47-C10.5 | W47 open | $10.5 | 0.15 / 0.17 | $15.00 | lot 5 | Expired worthless (Fri SimQ 9.51) | premium 1.52% of share value; held at midweek (ask 0.08) |
| 69 | SIMQ-W47-P9 | W47 open | $9 | 0.13 / 0.14 | $13.00 | $900.00 cash | Expired worthless (Fri SimQ 9.51) | premium 1.44% of collateral; held at midweek (ask 0.01) |
| 70 | SIMQ-W48-P9 | W48 open | $9 | 0.10 / 0.12 | $10.00 | $900.00 cash | Expired worthless (Fri SimQ 9.96) | premium 1.11% of collateral; held at midweek (ask 0.04) |
| 71 | SIMQ-W48-C10.5 | W48 open | $10.5 | 0.01 / 0.03 | $1.00 | lot 5 | Expired worthless (Fri SimQ 9.96) | premium 0.11% of share value; held at midweek (ask 0.01) |
| 72 | SIMQ-W49-C10.5 | W49 open | $10.5 | 0.09 / 0.11 | $9.00 | lot 5 | Expired worthless (Fri SimQ 9.98) | premium 0.90% of share value; held at midweek (ask 0.03) |
| 73 | SIMQ-W50-C10.5 | W50 open | $10.5 | 0.10 / 0.12 | $10.00 | lot 5 | Expired worthless (Fri SimQ 9.81) | premium 1.00% of share value; held at midweek (ask 0.01) |
| 74 | SIMQ-W50-P8.5 | W50 mid | $8.5 | 0.08 / 0.09 | $8.00 | $850.00 cash | Expired worthless (Fri SimQ 9.81) | premium 0.94% of collateral |
| 75 | SIMQ-W50-P9 | W50 mid | $9 | 0.22 / 0.24 | $22.00 | $900.00 cash | Expired worthless (Fri SimQ 9.81) | premium 2.44% of collateral |

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W7 at $45.00 | W9 at $46.00 | +$100.00 | +$348.00 |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | chop | 63.80 | 63.52 | 63.81 | 63.37 | 69.04 | 65.42 | +2.5% | 5.79 (7,553.00 x 7d) |
| 2 | chop | 65.42 | 69.74 | 70.24 | 70.42 | 66.91 | 69.10 | +5.6% | 5.86 (7,634.79 x 3d; 7,645.79 x 4d) |
| 3 | crash | 69.10 | 65.86 | 67.11 | 73.12 | 65.34 | 67.23 | -2.7% | 5.92 (7,703.65 x 3d; 7,721.65 x 4d) |
| 4 | rebound | 67.23 | 67.54 | 68.59 | 55.81 | 58.59 | 62.24 | -7.4% | 5.91 (7,799.57 x 3d; 7,638.57 x 4d) |
| 5 | chop | 62.24 | 63.41 | 62.79 | 61.83 | 66.62 | 66.31 | +6.5% | 5.92 (7,717.48 x 3d; 7,721.48 x 4d) |
| 6 | selloff | 66.31 | 67.79 | 69.92 | 67.37 | 63.85 | 61.64 | -7.0% | 5.97 (7,786.40 x 7d) |
| 7 | crash | 61.64 | 58.31 | 48.35 | 46.99 | 45.51 | 38.80 | -37.1% | 4.92 (7,849.37 x 3d; 7,581.37 x 2d; 3,081.37 x 2d) |
| 8 | rebound | 38.80 | 38.89 | 40.18 | 39.94 | 40.86 | 44.62 | +15.0% | 2.39 (3,117.29 x 3d; 3,116.29 x 4d) |
| 9 | calm_up | 44.62 | 45.18 | 45.58 | 45.80 | 46.29 | 46.23 | +3.6% | 3.48 (3,185.68 x 3d; 3,253.68 x 2d; 7,853.68 x 2d) |
| 10 | calm_up | 46.23 | 45.51 | 43.74 | 42.42 | 42.38 | 41.18 | -10.9% | 6.03 (7,857.16 x 7d) |
| 11 | calm_up | 41.18 | 41.43 | 41.72 | 41.24 | 41.33 | 41.73 | +1.3% | 6.04 (7,876.19 x 3d; 7,875.19 x 4d) |
| 12 | calm_up | 41.73 | 40.63 | 39.86 | 40.67 | 40.79 | 40.47 | -3.0% | 6.05 (7,884.23 x 7d) |
| 13 | chop | 40.47 | 39.93 | 40.36 | 41.81 | 40.24 | 40.35 | -0.3% | 6.06 (7,905.28 x 7d) |
| 14 | calm_up | 40.35 | 39.59 | 38.25 | 37.30 | 36.30 | 35.53 | -11.9% | 6.09 (7,939.34 x 7d) |
| 15 | selloff | 35.53 | 36.06 | 31.02 | 30.06 | 29.13 | 29.81 | -16.1% | 6.10 (7,945.43 x 7d) |
| 16 | chop | 29.81 | 30.62 | 29.35 | 29.24 | 28.97 | 28.83 | -3.3% | 6.12 (7,974.53 x 3d; 7,973.53 x 4d) |
| 17 | chop | 28.83 | 28.76 | 28.53 | 27.43 | 27.61 | 26.89 | -6.7% | 6.15 (8,013.65 x 7d) |
| 18 | calm_up | 26.89 | 27.56 | 27.24 | 27.24 | 27.25 | 27.10 | +0.8% | 6.17 (8,041.80 x 3d; 8,040.80 x 4d) |
| 19 | calm_up | 27.10 | 27.48 | 27.38 | 27.69 | 27.50 | 27.46 | +1.3% | 6.19 (8,067.97 x 3d; 8,065.97 x 4d) |
| 20 | chop | 27.46 | 28.34 | 28.76 | 27.80 | 27.94 | 27.37 | -0.3% | 6.22 (8,104.16 x 3d; 8,105.16 x 4d) |
| 21 | calm_up | 27.37 | 27.62 | 27.53 | 27.37 | 27.52 | 27.71 | +1.2% | 6.24 (8,139.38 x 3d; 8,138.38 x 4d) |
| 22 | chop | 27.71 | 27.41 | 30.02 | 29.00 | 29.65 | 29.30 | +5.7% | 6.26 (8,144.62 x 3d; 8,166.62 x 4d) |
| 23 | calm_up | 29.30 | 29.03 | 29.16 | 31.07 | 30.69 | 30.27 | +3.3% | 6.29 (8,205.88 x 3d; 8,204.88 x 4d) |
| 24 | calm_up | 30.27 | 31.27 | 31.06 | 30.11 | 31.02 | 31.13 | +2.8% | 6.32 (8,233.17 x 7d) |
| 25 | calm_up | 31.13 | 31.02 | 31.20 | 31.55 | 31.78 | 31.57 | +1.4% | 6.32 (8,239.49 x 7d) |
| 26 | calm_up | 31.57 | 31.26 | 30.52 | 30.48 | 30.13 | 29.10 | -7.8% | 6.33 (8,245.81 x 3d; 8,248.81 x 4d) |
| 27 | calm_up | 29.10 | 31.14 | 31.06 | 30.97 | 30.50 | 31.14 | +7.0% | 6.34 (8,268.14 x 3d; 8,267.14 x 4d) |
| 28 | calm_up | 31.14 | 32.20 | 34.35 | 33.92 | 33.61 | 33.46 | +7.5% | 6.36 (8,285.48 x 7d) |
| 29 | selloff | 33.46 | 33.95 | 32.63 | 33.36 | 31.33 | 31.17 | -6.8% | 6.37 (8,302.84 x 7d) |
| 30 | selloff | 31.17 | 22.31 | 21.74 | 21.84 | 21.08 | 21.49 | -31.1% | 5.68 (8,361.21 x 3d; 7,935.21 x 2d; 5,435.21 x 2d) |
| 31 | crash | 21.49 | 19.90 | 18.66 | 17.32 | 18.73 | 16.42 | -23.6% | 4.18 (5,440.89 x 3d; 5,454.89 x 4d) |
| 32 | selloff | 16.42 | 16.67 | 16.33 | 16.54 | 15.04 | 15.14 | -7.8% | 4.21 (5,490.07 x 3d; 5,488.07 x 4d) |
| 33 | crash | 15.14 | 14.78 | 14.68 | 16.28 | 16.01 | 16.14 | +6.6% | 4.25 (5,521.28 x 3d; 5,565.28 x 4d) |
| 34 | rebound | 16.14 | 16.96 | 17.35 | 17.95 | 16.42 | 16.42 | +1.7% | 4.30 (5,604.53 x 7d) |
| 35 | chop | 16.42 | 15.29 | 15.85 | 14.33 | 14.15 | 14.23 | -13.3% | 4.30 (5,608.83 x 7d) |
| 36 | selloff | 14.23 | 13.17 | 13.47 | 13.73 | 13.71 | 14.65 | +3.0% | 4.32 (5,631.13 x 7d) |
| 37 | chop | 14.65 | 13.92 | 13.55 | 13.47 | 13.71 | 13.97 | -4.6% | 4.33 (5,647.45 x 7d) |
| 38 | calm_up | 13.97 | 14.32 | 13.93 | 13.67 | 13.92 | 14.05 | +0.6% | 4.34 (5,651.78 x 7d) |
| 39 | chop | 14.05 | 13.85 | 14.01 | 14.51 | 14.44 | 14.38 | +2.3% | 4.34 (5,656.12 x 7d) |
| 40 | rebound | 14.38 | 14.29 | 15.52 | 17.60 | 17.39 | 17.60 | +22.4% | 4.36 (5,677.46 x 7d) |
| 41 | calm_up | 17.60 | 17.42 | 17.36 | 17.53 | 18.02 | 17.32 | -1.6% | 4.39 (5,719.82 x 3d; 5,716.82 x 4d) |
| 42 | calm_up | 17.32 | 17.41 | 16.93 | 17.00 | 17.27 | 17.26 | -0.3% | 4.40 (5,740.21 x 7d) |
| 43 | selloff | 17.26 | 16.93 | 15.33 | 14.33 | 13.00 | 12.03 | -30.3% | 4.41 (5,744.61 x 3d; 5,749.61 x 4d) |
| 44 | rebound | 12.03 | 12.01 | 12.46 | 12.67 | 12.91 | 13.67 | +13.6% | 4.45 (5,805.02 x 3d; 5,801.02 x 4d) |
| 45 | chop | 13.67 | 14.08 | 13.96 | 13.61 | 12.08 | 11.94 | -12.7% | 3.96 (5,880.47 x 5d; 3,380.47 x 2d) |
| 46 | chop | 11.94 | 10.98 | 10.23 | 9.47 | 9.45 | 9.87 | -17.3% | 2.42 (3,455.43 x 5d; 2,405.43 x 2d) |
| 47 | calm_up | 9.87 | 9.98 | 10.36 | 10.12 | 9.58 | 9.51 | -3.6% | 1.87 (2,435.85 x 7d) |
| 48 | calm_up | 9.51 | 9.63 | 9.70 | 9.55 | 9.51 | 9.96 | +4.7% | 1.88 (2,448.72 x 7d) |
| 49 | calm_up | 9.96 | 10.02 | 10.02 | 9.87 | 10.07 | 9.98 | +0.2% | 1.89 (2,459.60 x 7d) |
| 50 | chop | 9.98 | 9.87 | 9.41 | 9.10 | 9.35 | 9.81 | -1.7% | 1.91 (2,471.49 x 3d; 2,501.49 x 4d) |

## Scorecard
- 75 trades: 44 expired worthless, 22 closed for profit, 3 closed at a loss, 5 assigned, 1 called away | win rate 59% (88% counting profitable closes)
- Avg put premium: 1.00% of collateral
- Avg call premium: 1.46% of share value at sale
- Wheel cycles completed (shares called away): 1
- Account value at week 26 (comparison metric): $8,255.14 (+10.07%) | buy-and-hold SimQ $3,420.85 (-54.39%) | cash only $7,649.59 (+1.99%)
