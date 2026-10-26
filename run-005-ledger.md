# SimQ Run 5 Ledger

- Seed: 526270675 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-005-journal.md

## Current state (Week 47, Monday open)
- SimQ spot: $81.20
- Cash: $11,086.24 | locked collateral: $0.00 | free: $11,086.24
- Shares: 0
- Open positions: none
- Premium collected (gross): $3,158.00 | buy-to-close costs: $1,585.00 | interest: $263.24
- Realized P&L (options net of buy-backs + stock sales): +$3,323.00 (options +$1,573.00, stock +$1,750.00)
- Account value: $11,086.24 (+47.82% vs start)

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
| 9 | SIMQ-W05-P20 | W5 open | $20 | 0.18 / 0.20 | $18.00 | $2,000.00 cash | Bought to close at 0.04 ($4.00), net +$14.00 | premium 0.90% of collateral |
| 10 | SIMQ-W06-P20 | W6 open | $20 | 0.27 / 0.30 | $27.00 | $2,000.00 cash | Expired worthless (Fri SimQ 25.51) | premium 1.35% of collateral; held at midweek (ask 0.07) |
| 11 | SIMQ-W07-P23.5 | W7 open | $23.5 | 0.61 / 0.65 | $61.00 | $2,350.00 cash | Bought to close at 0.02 ($2.00), net +$59.00 | premium 2.60% of collateral |
| 12 | SIMQ-W07-P26.5 | W7 mid | $26.5 | 0.11 / 0.13 | $11.00 | $2,650.00 cash | Expired worthless (Fri SimQ 32.55) | premium 0.42% of collateral |
| 13 | SIMQ-W08-P27 | W8 open | $27 | 0.29 / 0.32 | $29.00 | $2,700.00 cash | Bought to close at 0.01 ($1.00), net +$28.00 | premium 1.07% of collateral |
| 14 | SIMQ-W09-P32.5 | W9 open | $32.5 | 0.35 / 0.38 | $35.00 | $3,250.00 cash | Bought to close at 0.03 ($3.00), net +$32.00 | premium 1.08% of collateral |
| 15 | SIMQ-W10-C40 | W10 open | $40 | 0.03 / 0.04 | $3.00 | lot 1 | Expired worthless (Fri SimQ 35.63) | premium 0.08% of share value; held at midweek (ask 0.01) |
| 16 | SIMQ-W10-P34 | W10 open | $34 | 0.45 / 0.48 | $45.00 | $3,400.00 cash | Expired worthless (Fri SimQ 35.63) | premium 1.32% of collateral; held at midweek (ask 0.11) |
| 17 | SIMQ-W11-C40.5 | W11 open | $40.5 | 0.02 / 0.04 | $2.00 | lot 1 | Expired worthless (Fri SimQ 36.91) | premium 0.06% of share value; held at midweek (ask 0.01) |
| 18 | SIMQ-W11-P33 | W11 open | $33 | 0.32 / 0.35 | $32.00 | $3,300.00 cash | Expired worthless (Fri SimQ 36.91) | premium 0.97% of collateral; held at midweek (ask 0.05) |
| 19 | SIMQ-W12-C41 | W12 open | $41 | 0.06 / 0.07 | $6.00 | lot 1 | Expired worthless (Fri SimQ 32.93) | premium 0.16% of share value; held at midweek (ask 0.01) |
| 20 | SIMQ-W12-P34.5 | W12 open | $34.5 | 0.35 / 0.37 | $35.00 | $3,450.00 cash | ASSIGNED: bought 100 at $34.50 (Fri SimQ 32.93) | premium 1.01% of collateral; held at midweek (ask 0.60) |
| 21 | SIMQ-W13-C35 | W13 open | $35 | 0.43 / 0.46 | $43.00 | lot 2 | CALLED AWAY: sold 100 at $35.00 (Fri SimQ 36.94) | premium 1.31% of share value; held at midweek (ask 0.91) |
| 22 | SIMQ-W14-P33.5 | W14 open | $33.5 | 0.17 / 0.19 | $17.00 | $3,350.00 cash | Bought to close at 0.05 ($5.00), net +$12.00 | premium 0.51% of collateral |
| 23 | SIMQ-W14-C41 | W14 open | $41 | 0.05 / 0.06 | $5.00 | lot 1 | Expired worthless (Fri SimQ 40.26) | premium 0.14% of share value; held at midweek (ask 0.30) |
| 24 | SIMQ-W14-P36.5 | W14 mid | $36.5 | 0.32 / 0.34 | $32.00 | $3,650.00 cash | Expired worthless (Fri SimQ 40.26) | premium 0.88% of collateral |
| 25 | SIMQ-W15-P36 | W15 open | $36 | 0.40 / 0.43 | $40.00 | $3,600.00 cash | Bought to close at 0.01 ($1.00), net +$39.00 | premium 1.11% of collateral |
| 26 | SIMQ-W15-C45 | W15 open | $45 | 0.18 / 0.20 | $18.00 | lot 1 | CALLED AWAY: sold 100 at $45.00 (Fri SimQ 48.96) | premium 0.45% of share value; held at midweek (ask 0.91) |
| 27 | SIMQ-W16-P44 | W16 open | $44 | 0.50 / 0.53 | $50.00 | $4,400.00 cash | Bought to close at 0.20 ($20.00), net +$30.00 | premium 1.14% of collateral |
| 28 | SIMQ-W17-P45.5 | W17 open | $45.5 | 0.21 / 0.23 | $21.00 | $4,550.00 cash | Bought to close at 0.01 ($1.00), net +$20.00 | premium 0.46% of collateral |
| 29 | SIMQ-W17-P51 | W17 mid | $51 | 0.22 / 0.24 | $22.00 | $5,100.00 cash | Expired worthless (Fri SimQ 52.89) | premium 0.43% of collateral |
| 30 | SIMQ-W18-P48.5 | W18 open | $48.5 | 0.49 / 0.53 | $49.00 | $4,850.00 cash | Expired worthless (Fri SimQ 50.81) | premium 1.01% of collateral; held at midweek (ask 1.12) |
| 31 | SIMQ-W19-P39 | W19 open | $39 | 0.17 / 0.19 | $17.00 | $3,900.00 cash | Bought to close at 0.01 ($1.00), net +$16.00 | premium 0.44% of collateral |
| 32 | SIMQ-W19-P41 | W19 open | $41 | 0.30 / 0.32 | $30.00 | $4,100.00 cash | Bought to close at 0.01 ($1.00), net +$29.00 | premium 0.73% of collateral |
| 33 | SIMQ-W19-P50 | W19 mid | $50 | 0.20 / 0.22 | $20.00 | $5,000.00 cash | Expired worthless (Fri SimQ 52.87) | premium 0.40% of collateral |
| 34 | SIMQ-W20-P45 | W20 open | $45 | 0.34 / 0.37 | $34.00 | $4,500.00 cash | ASSIGNED: bought 100 at $45.00 (Fri SimQ 44.14) | premium 0.76% of collateral; held at midweek (ask 1.13) |
| 35 | SIMQ-W20-P40 | W20 open | $40 | 0.07 / 0.08 | $7.00 | $4,000.00 cash | Bought to close at 0.23 ($23.00), net -$16.00 | premium 0.18% of collateral |
| 36 | SIMQ-W21-C49.5 | W21 open | $49.5 | 0.63 / 0.67 | $63.00 | lot 3 | CALLED AWAY: sold 100 at $49.50 (Fri SimQ 53.16) | premium 1.43% of share value; held at midweek (ask 1.85) |
| 37 | SIMQ-W21-P33 | W21 open | $33 | 0.27 / 0.29 | $27.00 | $3,300.00 cash | Bought to close at 0.01 ($1.00), net +$26.00 | premium 0.82% of collateral |
| 38 | SIMQ-W22-P41 | W22 open | $41 | 0.22 / 0.24 | $22.00 | $4,100.00 cash | Bought to close at 0.01 ($1.00), net +$21.00 | premium 0.54% of collateral |
| 39 | SIMQ-W22-P44 | W22 open | $44 | 0.46 / 0.49 | $46.00 | $4,400.00 cash | Bought to close at 0.01 ($1.00), net +$45.00 | premium 1.05% of collateral |
| 40 | SIMQ-W23-P46 | W23 open | $46 | 0.20 / 0.22 | $20.00 | $4,600.00 cash | Bought to close at 0.02 ($2.00), net +$18.00 | premium 0.43% of collateral |
| 41 | SIMQ-W23-P49 | W23 mid | $49 | 0.16 / 0.17 | $16.00 | $4,900.00 cash | Expired worthless (Fri SimQ 50.08) | premium 0.33% of collateral |
| 42 | SIMQ-W24-P45 | W24 open | $45 | 0.31 / 0.34 | $31.00 | $4,500.00 cash | Bought to close at 0.03 ($3.00), net +$28.00 | premium 0.69% of collateral |
| 43 | SIMQ-W24-P44 | W24 open | $44 | 0.21 / 0.23 | $21.00 | $4,400.00 cash | Bought to close at 0.02 ($2.00), net +$19.00 | premium 0.48% of collateral |
| 44 | SIMQ-W24-P48 | W24 mid | $48 | 0.15 / 0.16 | $15.00 | $4,800.00 cash | Expired worthless (Fri SimQ 49.73) | premium 0.31% of collateral |
| 45 | SIMQ-W25-P44 | W25 open | $44 | 0.52 / 0.55 | $52.00 | $4,400.00 cash | Bought to close at 0.01 ($1.00), net +$51.00 | premium 1.18% of collateral |
| 46 | SIMQ-W25-P40 | W25 open | $40 | 0.15 / 0.17 | $15.00 | $4,000.00 cash | Bought to close at 0.01 ($1.00), net +$14.00 | premium 0.38% of collateral |
| 47 | SIMQ-W26-P44.5 | W26 open | $44.5 | 0.15 / 0.17 | $15.00 | $4,450.00 cash | Expired worthless (Fri SimQ 50.32) | premium 0.34% of collateral; held at midweek (ask 0.11) |
| 48 | SIMQ-W27-P40 | W27 open | $40 | 0.33 / 0.35 | $33.00 | $4,000.00 cash | Bought to close at 0.01 ($1.00), net +$32.00 | premium 0.83% of collateral |
| 49 | SIMQ-W27-P43.5 | W27 open | $43.5 | 0.73 / 0.78 | $73.00 | $4,350.00 cash | Bought to close at 0.04 ($4.00), net +$69.00 | premium 1.68% of collateral |
| 50 | SIMQ-W28-P55 | W28 open | $55 | 0.59 / 0.63 | $59.00 | $5,500.00 cash | Bought to close at 0.01 ($1.00), net +$58.00 | premium 1.07% of collateral |
| 51 | SIMQ-W29-P56.5 | W29 open | $56.5 | 0.32 / 0.35 | $32.00 | $5,650.00 cash | Bought to close at 0.01 ($1.00), net +$31.00 | premium 0.57% of collateral |
| 52 | SIMQ-W29-P62 | W29 mid | $62 | 0.24 / 0.26 | $24.00 | $6,200.00 cash | Expired worthless (Fri SimQ 66.51) | premium 0.39% of collateral |
| 53 | SIMQ-W30-P70 | W30 mid | $70 | 0.52 / 0.56 | $52.00 | $7,000.00 cash | Expired worthless (Fri SimQ 72.20) | premium 0.74% of collateral |
| 54 | SIMQ-W31-P61 | W31 mid | $61 | 0.45 / 0.48 | $45.00 | $6,100.00 cash | Expired worthless (Fri SimQ 62.26) | premium 0.74% of collateral |
| 55 | SIMQ-W32-P40 | W32 open | $40 | 0.25 / 0.28 | $25.00 | $4,000.00 cash | Expired worthless (Fri SimQ 60.34) | premium 0.62% of collateral; held at midweek (ask 0.01) |
| 56 | SIMQ-W32-P50 | W32 open | $50 | 1.11 / 1.17 | $111.00 | $5,000.00 cash | Bought to close at 0.22 ($22.00), net +$89.00 | premium 2.22% of collateral |
| 57 | SIMQ-W33-P50 | W33 open | $50 | 0.52 / 0.56 | $52.00 | $5,000.00 cash | Bought to close at 0.17 ($17.00), net +$35.00 | premium 1.04% of collateral |
| 58 | SIMQ-W33-P43 | W33 open | $43 | 0.11 / 0.12 | $11.00 | $4,300.00 cash | Bought to close at 0.02 ($2.00), net +$9.00 | premium 0.26% of collateral |
| 59 | SIMQ-W33-P51.5 | W33 mid | $51.5 | 0.25 / 0.28 | $25.00 | $5,150.00 cash | Expired worthless (Fri SimQ 62.25) | premium 0.49% of collateral |
| 60 | SIMQ-W34-P47 | W34 open | $47 | 0.20 / 0.22 | $20.00 | $4,700.00 cash | Bought to close at 0.01 ($1.00), net +$19.00 | premium 0.43% of collateral |
| 61 | SIMQ-W34-P52 | W34 open | $52 | 0.57 / 0.61 | $57.00 | $5,200.00 cash | Bought to close at 0.01 ($1.00), net +$56.00 | premium 1.10% of collateral |
| 62 | SIMQ-W34-P62.5 | W34 mid | $62.5 | 0.26 / 0.29 | $26.00 | $6,250.00 cash | ASSIGNED: bought 100 at $62.50 (Fri SimQ 54.10) | premium 0.42% of collateral |
| 63 | SIMQ-W35-P37.5 | W35 open | $37.5 | 0.28 / 0.31 | $28.00 | $3,750.00 cash | Bought to close at 0.01 ($1.00), net +$27.00 | premium 0.75% of collateral |
| 64 | SIMQ-W35-C62.5 | W35 mid | $62.5 | 0.07 / 0.08 | $7.00 | lot 4 | Expired worthless (Fri SimQ 58.14) | premium 0.13% of share value |
| 65 | SIMQ-W36-C65 | W36 open | $65 | 0.57 / 0.61 | $57.00 | lot 4 | Expired worthless (Fri SimQ 64.26) | premium 0.98% of share value; held at midweek (ask 0.17) |
| 66 | SIMQ-W36-P37.5 | W36 open | $37.5 | 0.03 / 0.04 | $3.00 | $3,750.00 cash | Expired worthless (Fri SimQ 64.26) | premium 0.08% of collateral; held at midweek (ask 0.01) |
| 67 | SIMQ-W37-C67.5 | W37 open | $67.5 | 1.18 / 1.26 | $118.00 | lot 4 | Bought to close at 3.70 ($370.00), net -$252.00 | premium 1.84% of share value |
| 68 | SIMQ-W37-C70 | W37 mid | $70 | 2.00 / 2.12 | $200.00 | lot 4 | CALLED AWAY: sold 100 at $70.00 (Fri SimQ 70.76) | premium 2.86% of share value |
| 69 | SIMQ-W38-P65 | W38 open | $65 | 1.06 / 1.12 | $106.00 | $6,500.00 cash | Bought to close at 1.25 ($125.00), net -$19.00 | premium 1.63% of collateral |
| 70 | SIMQ-W39-P60 | W39 open | $60 | 1.04 / 1.11 | $104.00 | $6,000.00 cash | Bought to close at 0.01 ($1.00), net +$103.00 | premium 1.73% of collateral |
| 71 | SIMQ-W40-P65 | W40 open | $65 | 0.24 / 0.26 | $24.00 | $6,500.00 cash | Expired worthless (Fri SimQ 79.11) | premium 0.37% of collateral; held at midweek (ask 0.09) |
| 72 | SIMQ-W41-P70 | W41 open | $70 | 0.75 / 0.80 | $75.00 | $7,000.00 cash | Bought to close at 2.99 ($299.00), net -$224.00 | premium 1.07% of collateral |
| 73 | SIMQ-W43-P66 | W43 open | $66 | 0.46 / 0.49 | $46.00 | $6,600.00 cash | Expired worthless (Fri SimQ 71.90) | premium 0.70% of collateral; held at midweek (ask 0.29) |
| 74 | SIMQ-W44-P65 | W44 open | $65 | 0.35 / 0.38 | $35.00 | $6,500.00 cash | Bought to close at 0.02 ($2.00), net +$33.00 | premium 0.54% of collateral |
| 75 | SIMQ-W45-P70 | W45 open | $70 | 0.78 / 0.83 | $78.00 | $7,000.00 cash | Bought to close at 0.33 ($33.00), net +$45.00 | premium 1.11% of collateral |
| 76 | SIMQ-W45-P70.5 | W45 mid | $70.5 | 0.34 / 0.37 | $34.00 | $7,050.00 cash | Expired worthless (Fri SimQ 80.53) | premium 0.48% of collateral |
| 77 | SIMQ-W46-P69 | W46 open | $69 | 1.03 / 1.09 | $103.00 | $6,900.00 cash | Bought to close at 0.01 ($1.00), net +$102.00 | premium 1.49% of collateral |

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W12 at $34.50 | W13 at $35.00 | +$50.00 | +$128.00 |
| W3 at $40.00 | W15 at $45.00 | +$500.00 | +$663.00 |
| W20 at $45.00 | W21 at $49.50 | +$450.00 | +$547.00 |
| W34 at $62.50 | W37 at $70.00 | +$750.00 | +$788.00 |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | calm_up | 63.80 | 65.24 | 61.20 | 60.29 | 59.12 | 58.99 | -7.5% | 5.77 (7,525.00 x 3d; 7,523.00 x 4d) |
| 2 | selloff | 58.99 | 58.06 | 54.71 | 52.19 | 53.96 | 52.22 | -11.5% | 5.71 (7,579.77 x 3d; 7,350.77 x 4d) |
| 3 | crash | 52.22 | 52.24 | 42.32 | 41.41 | 32.41 | 31.30 | -40.1% | 4.76 (7,399.48 x 3d; 7,305.48 x 2d; 3,305.48 x 2d) |
| 4 | crash | 31.30 | 30.70 | 27.65 | 27.08 | 26.72 | 26.33 | -15.9% | 2.57 (3,387.24 x 3d; 3,330.24 x 4d) |
| 5 | crash | 26.33 | 24.02 | 22.25 | 24.76 | 21.78 | 24.37 | -7.4% | 2.57 (3,350.81 x 3d; 3,346.81 x 4d) |
| 6 | rebound | 24.37 | 25.16 | 24.65 | 23.77 | 25.55 | 25.51 | +4.7% | 2.59 (3,376.38 x 7d) |
| 7 | rebound | 25.51 | 28.79 | 29.26 | 30.30 | 31.49 | 32.55 | +27.6% | 2.64 (3,439.97 x 3d; 3,448.97 x 4d) |
| 8 | calm_up | 32.55 | 31.91 | 31.84 | 34.52 | 34.32 | 34.42 | +5.7% | 2.67 (3,480.61 x 3d; 3,479.61 x 4d) |
| 9 | calm_up | 34.42 | 34.82 | 35.97 | 35.80 | 35.75 | 35.70 | +3.7% | 2.70 (3,517.28 x 3d; 3,514.28 x 4d) |
| 10 | calm_up | 35.70 | 35.60 | 35.87 | 36.25 | 36.04 | 35.63 | -0.2% | 2.73 (3,564.98 x 7d) |
| 11 | calm_up | 35.63 | 36.16 | 36.27 | 36.06 | 36.68 | 36.91 | +3.6% | 2.76 (3,601.71 x 7d) |
| 12 | calm_up | 36.91 | 37.39 | 36.90 | 35.07 | 35.07 | 32.93 | -10.8% | 2.04 (3,645.47 x 5d; 195.47 x 2d) |
| 13 | calm_up | 32.93 | 34.03 | 33.85 | 35.36 | 36.95 | 36.94 | +12.2% | 0.95 (240.51 x 5d; 3,740.51 x 2d) |
| 14 | chop | 36.94 | 37.08 | 38.62 | 38.82 | 39.35 | 40.26 | +9.0% | 2.90 (3,763.46 x 3d; 3,790.46 x 4d) |
| 15 | chop | 40.26 | 41.17 | 43.33 | 44.33 | 44.87 | 48.96 | +21.6% | 3.94 (3,851.36 x 3d; 3,850.36 x 2d; 8,350.36 x 2d) |
| 16 | calm_up | 48.96 | 50.58 | 48.84 | 47.19 | 47.87 | 50.15 | +2.4% | 6.44 (8,404.30 x 3d; 8,384.30 x 4d) |
| 17 | calm_up | 50.15 | 50.27 | 52.48 | 53.88 | 54.31 | 52.89 | +5.5% | 6.46 (8,411.74 x 3d; 8,432.74 x 4d) |
| 18 | selloff | 52.89 | 50.73 | 51.45 | 50.12 | 50.71 | 50.81 | -3.9% | 6.51 (8,488.20 x 7d) |
| 19 | chop | 50.81 | 51.47 | 55.66 | 54.98 | 53.81 | 52.87 | +4.1% | 6.56 (8,541.71 x 3d; 8,559.71 x 4d) |
| 20 | crash | 52.87 | 49.96 | 48.93 | 47.15 | 45.10 | 44.14 | -16.5% | 5.61 (8,607.27 x 3d; 8,584.27 x 2d; 4,084.27 x 2d) |
| 21 | rebound | 44.14 | 46.23 | 47.97 | 49.82 | 49.87 | 53.16 | +20.4% | 4.29 (4,179.88 x 3d; 4,178.88 x 2d; 9,128.88 x 2d) |
| 22 | calm_up | 53.16 | 51.73 | 51.07 | 50.81 | 51.25 | 51.27 | -3.6% | 7.06 (9,201.17 x 3d; 9,199.17 x 4d) |
| 23 | calm_up | 51.27 | 51.39 | 52.02 | 52.05 | 51.60 | 50.08 | -2.3% | 7.08 (9,226.23 x 3d; 9,240.23 x 4d) |
| 24 | chop | 50.08 | 52.13 | 50.87 | 53.23 | 49.41 | 49.73 | -0.7% | 7.14 (9,299.31 x 3d; 9,309.31 x 4d) |
| 25 | calm_up | 49.73 | 50.15 | 51.47 | 52.29 | 49.55 | 50.10 | +0.7% | 7.20 (9,383.45 x 3d; 9,381.45 x 4d) |
| 26 | selloff | 50.10 | 51.33 | 50.37 | 52.29 | 51.59 | 50.32 | +0.4% | 7.21 (9,403.65 x 7d) |
| 27 | rebound | 50.32 | 52.80 | 50.40 | 53.67 | 60.45 | 66.30 | +31.8% | 7.30 (9,516.86 x 3d; 9,511.86 x 4d) |
| 28 | calm_up | 66.30 | 66.67 | 66.40 | 67.92 | 65.25 | 63.70 | -3.9% | 7.35 (9,578.16 x 3d; 9,577.16 x 4d) |
| 29 | calm_up | 63.70 | 63.49 | 65.13 | 65.39 | 64.97 | 66.51 | +4.4% | 7.39 (9,616.51 x 3d; 9,639.51 x 4d) |
| 30 | calm_up | 66.51 | 71.79 | 71.96 | 72.45 | 70.39 | 72.20 | +8.6% | 7.42 (9,646.90 x 3d; 9,698.90 x 4d) |
| 31 | crash | 72.20 | 72.78 | 70.64 | 69.20 | 67.80 | 62.26 | -13.8% | 7.47 (9,706.32 x 3d; 9,751.32 x 4d) |
| 32 | rebound | 62.26 | 60.06 | 56.60 | 56.58 | 59.05 | 60.34 | -3.1% | 7.58 (9,894.79 x 3d; 9,872.79 x 4d) |
| 33 | rebound | 60.34 | 63.25 | 61.84 | 59.64 | 60.71 | 62.25 | +3.2% | 7.63 (9,943.37 x 3d; 9,949.37 x 4d) |
| 34 | chop | 62.25 | 63.99 | 66.84 | 68.41 | 63.53 | 54.10 | -13.1% | 6.34 (10,034.00 x 3d; 10,058.00 x 2d; 3,808.00 x 2d) |
| 35 | rebound | 54.10 | 48.37 | 53.75 | 55.28 | 57.23 | 58.14 | +7.5% | 2.95 (3,842.34 x 3d; 3,848.34 x 4d) |
| 36 | chop | 58.14 | 57.58 | 59.46 | 59.97 | 62.86 | 64.26 | +10.5% | 3.00 (3,911.29 x 7d) |
| 37 | chop | 64.26 | 65.28 | 71.44 | 70.02 | 70.51 | 70.76 | +10.1% | 4.55 (4,032.29 x 3d; 3,862.29 x 2d; 10,862.29 x 2d) |
| 38 | selloff | 70.76 | 63.60 | 63.01 | 67.79 | 68.75 | 68.67 | -3.0% | 8.36 (10,972.84 x 3d; 10,847.84 x 4d) |
| 39 | calm_up | 68.67 | 71.83 | 73.56 | 73.63 | 72.33 | 72.75 | +5.9% | 8.41 (10,960.20 x 3d; 10,959.20 x 4d) |
| 40 | chop | 72.75 | 80.99 | 81.81 | 77.48 | 78.55 | 79.11 | +8.7% | 8.43 (10,991.61 x 7d) |
| 41 | selloff | 79.11 | 71.34 | 76.59 | 69.96 | 71.11 | 66.97 | -15.3% | 8.36 (11,075.04 x 3d; 10,776.04 x 4d) |
| 42 | calm_up | 66.97 | 67.73 | 68.99 | 68.70 | 73.53 | 72.73 | +8.6% | 8.27 (10,784.40 x 7d) |
| 43 | calm_up | 72.73 | 71.72 | 69.83 | 69.47 | 70.62 | 71.90 | -1.1% | 8.31 (10,838.67 x 7d) |
| 44 | calm_up | 71.90 | 72.73 | 72.79 | 73.27 | 74.58 | 74.01 | +2.9% | 8.35 (10,881.98 x 3d; 10,879.98 x 4d) |
| 45 | rebound | 74.01 | 76.92 | 77.25 | 79.66 | 82.11 | 80.53 | +8.8% | 8.41 (10,966.33 x 3d; 10,967.33 x 4d) |
| 46 | calm_up | 80.53 | 81.31 | 81.75 | 81.09 | 81.96 | 81.20 | +0.8% | 8.50 (11,078.74 x 3d; 11,077.74 x 4d) |

## Scorecard
- 77 trades: 28 expired worthless, 34 closed for profit, 7 closed at a loss, 4 assigned, 4 called away | win rate 36% (81% counting profitable closes)
- Avg put premium: 0.89% of collateral
- Avg call premium: 0.86% of share value at sale
- Wheel cycles completed (shares called away): 4
- Account value at week 26 (comparison metric): $9,410.86 (+25.48%) | buy-and-hold SimQ $5,915.36 (-21.13%) | cash only $7,649.59 (+1.99%)
