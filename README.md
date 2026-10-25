# simq-sim

Paper-trading simulator for weekly cash-secured puts and covered calls on SimQ, a synthetic 3x leveraged Nasdaq-like index (the "weekly 1%" project).

- Start here: RESUME.md (setup, commands, output style). Rules: csp-ledger-branch-cc.md. Calibration: market-calibration.md. Runs: run-index.md.
- Engine: simq.py (market paths + option pricing). Bookkeeping and turn driver: simbook.py.
- Runs: run-NNN-state.json (append-only event log; ledgers and journals are generated from it).
- Current standard for new runs: pricing v3, headlines v2 (4 per week, unreliable hints).
- reports/: Run 2 week-by-week workbook and the scripts that build it.
- tools/pricing-review/: scripts behind the Oct 24, 2026 pricing review (v1 vs v2 vs v3 Monte Carlo checks).
- csp-ledger.md: the separate real-time TQQQ paper ledger (main branch of the project, not SimQ).
