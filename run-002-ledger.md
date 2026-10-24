# SimQ Run 2 Ledger

- Seed: 865529296 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-002-journal.md

## Current state (Week 32, Monday open)
- SimQ spot: $69.78
- Cash: $2,412.72 | locked collateral: $0.00 | free: $2,412.72
- Shares: 100 SimQ bought at $71.00 in Week 31; effective basis $70.17 after option premiums
- Open positions: none
- Premium collected (gross): $2,749.00 | buy-to-close costs: $1,357.00 | interest: $170.72
- Realized P&L (options net of buy-backs + stock sales): +$1,842.00 (options +$1,392.00, stock +$450.00)
- Account value: $9,390.72 (+25.21% vs start)

## Trade log
| # | Contract | Opened | Strike | Fill (bid/ask) | Premium | Collateral/Cover | Result | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | SIMQ-W01-P56 | W1 open | $56 | 0.53 / 0.57 | $53.00 | $5,600.00 cash | Bought to close at 7.09 ($709.00), net -$656.00 | premium 0.95% of collateral |
| 2 | SIMQ-W01-P41 | W1 mid | $41 | 0.35 / 0.38 | $35.00 | $4,100.00 cash | ASSIGNED: bought 100 at $41.00 (Fri SimQ 38.44) | premium 0.85% of collateral |
| 3 | SIMQ-W02-P25 | W2 open | $25 | 0.42 / 0.46 | $42.00 | $2,500.00 cash | Bought to close at 0.01 ($1.00), net +$41.00 | premium 1.68% of collateral |
| 4 | SIMQ-W02-C45 | W2 open | $45 | 0.71 / 0.76 | $71.00 | lot 1 | Expired worthless (Fri SimQ 37.75) | premium 1.85% of share value; held at midweek (ask 0.01) |
| 5 | SIMQ-W03-C42 | W3 mid | $42 | 0.23 / 0.25 | $23.00 | lot 1 | Expired worthless (Fri SimQ 36.53) | premium 0.58% of share value |
| 6 | SIMQ-W04-C42 | W4 open | $42 | 0.22 / 0.24 | $22.00 | lot 1 | Expired worthless (Fri SimQ 40.02) | premium 0.60% of share value; held at midweek (ask 0.04) |
| 7 | SIMQ-W04-P29 | W4 open | $29 | 0.24 / 0.27 | $24.00 | $2,900.00 cash | Expired worthless (Fri SimQ 40.02) | premium 0.83% of collateral; held at midweek (ask 0.05) |
| 8 | SIMQ-W05-C43 | W5 open | $43 | 0.76 / 0.81 | $76.00 | lot 1 | Bought to close at 2.66 ($266.00), net -$190.00 | premium 1.90% of share value |
| 9 | SIMQ-W05-C44.5 | W5 mid | $44.5 | 1.59 / 1.68 | $159.00 | lot 1 | CALLED AWAY: sold 100 at $44.50 (Fri SimQ 47.59) | premium 3.55% of share value |
| 10 | SIMQ-W06-P40 | W6 open | $40 | 0.46 / 0.49 | $46.00 | $4,000.00 cash | Expired worthless (Fri SimQ 46.18) | premium 1.15% of collateral; held at midweek (ask 0.28) |
| 11 | SIMQ-W07-P36 | W7 open | $36 | 0.34 / 0.37 | $34.00 | $3,600.00 cash | Bought to close at 0.01 ($1.00), net +$33.00 | premium 0.94% of collateral |
| 12 | SIMQ-W07-P44 | W7 mid | $44 | 0.29 / 0.32 | $29.00 | $4,400.00 cash | Expired worthless (Fri SimQ 53.08) | premium 0.66% of collateral |
| 13 | SIMQ-W08-P43 | W8 open | $43 | 0.49 / 0.52 | $49.00 | $4,300.00 cash | Expired worthless (Fri SimQ 55.21) | premium 1.14% of collateral; held at midweek (ask 0.71) |
| 14 | SIMQ-W09-P44 | W9 open | $44 | 0.87 / 0.93 | $87.00 | $4,400.00 cash | Bought to close at 0.01 ($1.00), net +$86.00 | premium 1.98% of collateral |
| 15 | SIMQ-W09-P32.5 | W9 open | $32.5 | 0.09 / 0.11 | $9.00 | $3,250.00 cash | Bought to close at 0.01 ($1.00), net +$8.00 | premium 0.28% of collateral |
| 16 | SIMQ-W10-P51.5 | W10 open | $51.5 | 0.47 / 0.50 | $47.00 | $5,150.00 cash | Bought to close at 0.27 ($27.00), net +$20.00 | premium 0.91% of collateral |
| 17 | SIMQ-W10-P54 | W10 mid | $54 | 0.49 / 0.53 | $49.00 | $5,400.00 cash | Expired worthless (Fri SimQ 60.22) | premium 0.91% of collateral |
| 18 | SIMQ-W11-P49 | W11 open | $49 | 0.68 / 0.72 | $68.00 | $4,900.00 cash | Bought to close at 0.01 ($1.00), net +$67.00 | premium 1.39% of collateral |
| 19 | SIMQ-W11-P58 | W11 mid | $58 | 0.21 / 0.23 | $21.00 | $5,800.00 cash | Expired worthless (Fri SimQ 66.23) | premium 0.36% of collateral |
| 20 | SIMQ-W12-P56 | W12 open | $56 | 0.57 / 0.61 | $57.00 | $5,600.00 cash | Bought to close at 0.02 ($2.00), net +$55.00 | premium 1.02% of collateral |
| 21 | SIMQ-W13-P59 | W13 open | $59 | 0.60 / 0.64 | $60.00 | $5,900.00 cash | Bought to close at 0.44 ($44.00), net +$16.00 | premium 1.02% of collateral |
| 22 | SIMQ-W13-P57 | W13 mid | $57 | 0.19 / 0.21 | $19.00 | $5,700.00 cash | Expired worthless (Fri SimQ 66.69) | premium 0.33% of collateral |
| 23 | SIMQ-W14-P59.5 | W14 open | $59.5 | 0.61 / 0.66 | $61.00 | $5,950.00 cash | Bought to close at 0.13 ($13.00), net +$48.00 | premium 1.03% of collateral |
| 24 | SIMQ-W14-P64 | W14 mid | $64 | 0.50 / 0.54 | $50.00 | $6,400.00 cash | Expired worthless (Fri SimQ 72.47) | premium 0.78% of collateral |
| 25 | SIMQ-W15-P62 | W15 open | $62 | 0.68 / 0.72 | $68.00 | $6,200.00 cash | Bought to close at 0.01 ($1.00), net +$67.00 | premium 1.10% of collateral |
| 26 | SIMQ-W15-P70 | W15 mid | $70 | 0.36 / 0.39 | $36.00 | $7,000.00 cash | Expired worthless (Fri SimQ 78.18) | premium 0.51% of collateral |
| 27 | SIMQ-W16-P75 | W16 mid | $75 | 0.16 / 0.17 | $16.00 | $7,500.00 cash | ASSIGNED: bought 100 at $75.00 (Fri SimQ 71.26) | premium 0.21% of collateral |
| 28 | SIMQ-W17-C76 | W17 open | $76 | 0.70 / 0.75 | $70.00 | lot 2 | Expired worthless (Fri SimQ 72.04) | premium 0.98% of share value; held at midweek (ask 0.24) |
| 29 | SIMQ-W18-C76 | W18 open | $76 | 0.99 / 1.06 | $99.00 | lot 2 | CALLED AWAY: sold 100 at $76.00 (Fri SimQ 76.41) | premium 1.37% of share value; held at midweek (ask 0.86) |
| 30 | SIMQ-W19-P67 | W19 open | $67 | 0.65 / 0.69 | $65.00 | $6,700.00 cash | Bought to close at 0.21 ($21.00), net +$44.00 | premium 0.97% of collateral |
| 31 | SIMQ-W19-P72 | W19 mid | $72 | 0.61 / 0.66 | $61.00 | $7,200.00 cash | Expired worthless (Fri SimQ 83.96) | premium 0.85% of collateral |
| 32 | SIMQ-W20-P69 | W20 open | $69 | 1.02 / 1.08 | $102.00 | $6,900.00 cash | Expired worthless (Fri SimQ 75.32) | premium 1.48% of collateral; held at midweek (ask 0.32) |
| 33 | SIMQ-W21-P56 | W21 open | $56 | 0.66 / 0.71 | $66.00 | $5,600.00 cash | Bought to close at 0.01 ($1.00), net +$65.00 | premium 1.18% of collateral |
| 34 | SIMQ-W21-P63 | W21 mid | $63 | 0.17 / 0.18 | $17.00 | $6,300.00 cash | Expired worthless (Fri SimQ 74.38) | premium 0.27% of collateral |
| 35 | SIMQ-W22-P65.5 | W22 open | $65.5 | 0.64 / 0.68 | $64.00 | $6,550.00 cash | Bought to close at 0.18 ($18.00), net +$46.00 | premium 0.98% of collateral |
| 36 | SIMQ-W22-P70.5 | W22 mid | $70.5 | 0.50 / 0.53 | $50.00 | $7,050.00 cash | Expired worthless (Fri SimQ 89.56) | premium 0.71% of collateral |
| 37 | SIMQ-W23-P75 | W23 open | $75 | 1.11 / 1.17 | $111.00 | $7,500.00 cash | Bought to close at 0.96 ($96.00), net +$15.00 | premium 1.48% of collateral |
| 38 | SIMQ-W23-P73.5 | W23 mid | $73.5 | 0.71 / 0.76 | $71.00 | $7,350.00 cash | Expired worthless (Fri SimQ 78.90) | premium 0.97% of collateral |
| 39 | SIMQ-W24-P64 | W24 open | $64 | 0.91 / 0.97 | $91.00 | $6,400.00 cash | Expired worthless (Fri SimQ 77.25) | premium 1.42% of collateral; held at midweek (ask 0.07) |
| 40 | SIMQ-W25-P66 | W25 open | $66 | 0.43 / 0.46 | $43.00 | $6,600.00 cash | Expired worthless (Fri SimQ 79.89) | premium 0.65% of collateral; held at midweek (ask 0.59) |
| 41 | SIMQ-W26-P65 | W26 open | $65 | 0.72 / 0.76 | $72.00 | $6,500.00 cash | Bought to close at 0.09 ($9.00), net +$63.00 | premium 1.11% of collateral |
| 42 | SIMQ-W26-P70 | W26 mid | $70 | 0.22 / 0.24 | $22.00 | $7,000.00 cash | Expired worthless (Fri SimQ 92.15) | premium 0.31% of collateral |
| 43 | SIMQ-W27-P70 | W27 open | $70 | 1.00 / 1.06 | $100.00 | $7,000.00 cash | Expired worthless (Fri SimQ 86.08) | premium 1.43% of collateral; held at midweek (ask 0.01) |
| 44 | SIMQ-W28-P72 | W28 open | $72 | 0.36 / 0.39 | $36.00 | $7,200.00 cash | Expired worthless (Fri SimQ 84.37) | premium 0.50% of collateral; held at midweek (ask 0.50) |
| 45 | SIMQ-W29-P71 | W29 open | $71 | 0.70 / 0.75 | $70.00 | $7,100.00 cash | Bought to close at 0.02 ($2.00), net +$68.00 | premium 0.99% of collateral |
| 46 | SIMQ-W29-P77 | W29 mid | $77 | 0.17 / 0.19 | $17.00 | $7,700.00 cash | Expired worthless (Fri SimQ 81.71) | premium 0.22% of collateral |
| 47 | SIMQ-W30-P69 | W30 open | $69 | 0.46 / 0.50 | $46.00 | $6,900.00 cash | Bought to close at 0.01 ($1.00), net +$45.00 | premium 0.67% of collateral |
| 48 | SIMQ-W30-P74 | W30 mid | $74 | 0.10 / 0.11 | $10.00 | $7,400.00 cash | Expired worthless (Fri SimQ 81.16) | premium 0.14% of collateral |
| 49 | SIMQ-W31-P73 | W31 open | $73 | 0.72 / 0.77 | $72.00 | $7,300.00 cash | Bought to close at 1.42 ($142.00), net -$70.00 | premium 0.99% of collateral |
| 50 | SIMQ-W31-P71 | W31 mid | $71 | 0.83 / 0.88 | $83.00 | $7,100.00 cash | ASSIGNED: bought 100 at $71.00 (Fri SimQ 69.78) | premium 1.17% of collateral |

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W1 at $41.00 | W5 at $44.50 | +$350.00 | +$470.00 |
| W16 at $75.00 | W18 at $76.00 | +$100.00 | +$285.00 |

## Weeks
| Week | Regime | Open | Mon | Tue | Wed | Thu | Fri | Week % | Interest |
|---|---|---|---|---|---|---|---|---|---|
| 1 | crash | 63.80 | 58.59 | 51.69 | 49.36 | 43.29 | 38.44 | -39.7% | 4.60 (7,553.00 x 3d; 6,879.00 x 2d; 2,779.00 x 2d) |
| 2 | chop | 38.44 | 38.52 | 39.27 | 38.21 | 37.61 | 37.75 | -1.8% | 2.22 (2,896.60 x 3d; 2,895.60 x 4d) |
| 3 | chop | 37.75 | 36.91 | 38.32 | 39.56 | 39.83 | 36.53 | -3.2% | 2.23 (2,897.82 x 3d; 2,920.82 x 4d) |
| 4 | rebound | 36.53 | 37.56 | 38.44 | 36.40 | 37.81 | 40.02 | +9.6% | 2.28 (2,969.05 x 7d) |
| 5 | rebound | 40.02 | 40.90 | 43.78 | 44.81 | 45.36 | 47.59 | +18.9% | 3.27 (3,047.33 x 3d; 2,940.33 x 2d; 7,390.33 x 2d) |
| 6 | selloff | 47.59 | 47.69 | 45.28 | 45.16 | 45.36 | 46.18 | -3.0% | 5.71 (7,439.60 x 7d) |
| 7 | selloff | 46.18 | 48.28 | 49.44 | 49.74 | 51.59 | 53.08 | +14.9% | 5.75 (7,479.31 x 3d; 7,507.31 x 4d) |
| 8 | crash | 53.08 | 53.79 | 55.87 | 50.42 | 52.39 | 55.21 | +4.0% | 5.80 (7,562.06 x 7d) |
| 9 | chop | 55.21 | 54.14 | 56.68 | 57.65 | 59.47 | 58.89 | +6.7% | 5.88 (7,663.86 x 3d; 7,661.86 x 4d) |
| 10 | selloff | 58.89 | 59.02 | 63.59 | 60.99 | 62.00 | 60.22 | +2.3% | 5.93 (7,714.74 x 3d; 7,736.74 x 4d) |
| 11 | rebound | 60.22 | 62.77 | 58.51 | 65.88 | 66.84 | 66.23 | +10.0% | 6.00 (7,810.67 x 3d; 7,830.67 x 4d) |
| 12 | chop | 66.23 | 65.44 | 66.57 | 67.47 | 66.47 | 67.10 | +1.3% | 6.05 (7,893.67 x 3d; 7,891.67 x 4d) |
| 13 | chop | 67.10 | 67.61 | 65.03 | 63.73 | 63.86 | 66.69 | -0.6% | 6.09 (7,957.72 x 3d; 7,932.72 x 4d) |
| 14 | rebound | 66.69 | 68.04 | 67.71 | 69.96 | 69.79 | 72.47 | +8.7% | 6.15 (7,999.81 x 3d; 8,036.81 x 4d) |
| 15 | calm_up | 72.47 | 72.95 | 74.88 | 74.45 | 74.91 | 78.18 | +7.9% | 6.24 (8,110.96 x 3d; 8,145.96 x 4d) |
| 16 | calm_up | 78.18 | 78.02 | 79.43 | 81.51 | 70.38 | 71.26 | -8.9% | 4.62 (8,152.20 x 3d; 8,168.20 x 2d; 668.20 x 2d) |
| 17 | calm_up | 71.26 | 72.02 | 72.04 | 71.66 | 72.89 | 72.04 | +1.1% | 0.57 (742.82 x 7d) |
| 18 | chop | 72.04 | 71.58 | 72.94 | 73.43 | 74.82 | 76.41 | +6.1% | 2.31 (842.39 x 5d; 8,442.39 x 2d) |
| 19 | selloff | 76.41 | 79.39 | 81.02 | 80.44 | 85.49 | 83.96 | +9.9% | 6.55 (8,509.70 x 3d; 8,549.70 x 4d) |
| 20 | selloff | 83.96 | 83.36 | 82.33 | 80.79 | 79.81 | 75.32 | -10.3% | 6.64 (8,658.25 x 7d) |
| 21 | chop | 75.32 | 73.93 | 71.63 | 70.79 | 72.74 | 74.38 | -1.2% | 6.70 (8,730.89 x 3d; 8,746.89 x 4d) |
| 22 | selloff | 74.38 | 82.25 | 83.43 | 80.93 | 88.89 | 89.56 | +20.4% | 6.78 (8,817.59 x 3d; 8,849.59 x 4d) |
| 23 | selloff | 89.56 | 93.03 | 94.22 | 85.65 | 79.90 | 78.90 | -11.9% | 6.87 (8,967.37 x 3d; 8,942.37 x 4d) |
| 24 | chop | 78.90 | 74.46 | 74.88 | 74.20 | 74.16 | 77.25 | -2.1% | 6.93 (9,040.24 x 7d) |
| 25 | selloff | 77.25 | 74.75 | 78.57 | 74.95 | 78.46 | 79.89 | +3.4% | 6.97 (9,090.17 x 7d) |
| 26 | crash | 79.89 | 68.67 | 70.66 | 88.03 | 86.82 | 92.15 | +15.3% | 7.04 (9,169.14 x 3d; 9,182.14 x 4d) |
| 27 | chop | 92.15 | 91.05 | 89.65 | 88.78 | 86.67 | 86.08 | -6.6% | 7.13 (9,289.18 x 7d) |
| 28 | rebound | 86.08 | 86.70 | 90.21 | 83.49 | 83.59 | 84.37 | -2.0% | 7.16 (9,332.31 x 7d) |
| 29 | calm_up | 84.37 | 83.25 | 84.91 | 84.31 | 85.89 | 81.71 | -3.2% | 7.22 (9,409.47 x 3d; 9,424.47 x 4d) |
| 30 | calm_up | 81.71 | 82.41 | 82.75 | 82.34 | 82.36 | 81.16 | -0.7% | 7.27 (9,477.69 x 3d; 9,486.69 x 4d) |
| 31 | chop | 81.16 | 85.06 | 79.71 | 75.71 | 76.44 | 69.78 | -14.0% | 5.76 (9,565.96 x 3d; 9,506.96 x 2d; 2,406.96 x 2d) |

## Scorecard
- 50 trades: 25 expired worthless, 17 closed for profit, 3 closed at a loss, 3 assigned, 2 called away | win rate 50% (84% counting profitable closes)
- Avg put premium: 0.90% of collateral
- Avg call premium: 1.55% of share value at sale
- Wheel cycles completed (shares called away): 2
- Account value at week 26 (comparison metric): $9,189.18 (+22.52%) | buy-and-hold SimQ $10,832.68 (+44.44%) | cash only $7,649.59 (+1.99%)
