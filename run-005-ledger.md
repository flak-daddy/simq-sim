# SimQ Run 5 Ledger

- Seed: 526270675 | Start: $7,500, 4.00% APY | Rules: claude/csp-ledger-branch-cc.md
- Status: in progress | Comparison window: 26 sim weeks | Journal: claude/run-005-journal.md

## Current state (Week 18, Monday open)
- SimQ spot: $52.89
- Cash: $8,439.20 | locked collateral: $0.00 | free: $8,439.20
- Shares: 0
- Open positions: none
- Premium collected (gross): $995.00 | buy-to-close costs: $666.00 | interest: $60.20
- Realized P&L (options net of buy-backs + stock sales): +$879.00 (options +$329.00, stock +$550.00)
- Account value: $8,439.20 (+12.52% vs start)

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

## Closed share lots
| Bought | Sold | Stock P&L | Net after option premiums |
|---|---|---|---|
| W12 at $34.50 | W13 at $35.00 | +$50.00 | +$128.00 |
| W3 at $40.00 | W15 at $45.00 | +$500.00 | +$663.00 |

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

## Scorecard
- 29 trades: 12 expired worthless, 10 closed for profit, 3 closed at a loss, 2 assigned, 2 called away | win rate 41% (76% counting profitable closes)
- Avg put premium: 1.14% of collateral
- Avg call premium: 0.45% of share value at sale
- Wheel cycles completed (shares called away): 2
- Account value at week 26 (comparison metric): pending
