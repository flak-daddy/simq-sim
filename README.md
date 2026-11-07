# SimQ v2

Weekly options practice simulator on a synthetic TQQQ-like index. `SPEC.md` is the rulebook.

- `simq/` engine: `market.py` (backdrop + sentiment price path, rates), `indicators.py` (Fear & Greed gauge, Sim-tastic Oscillator), `pricing.py` (Black-Scholes, skew, quotes), `ruleset.py` (working parameters).
- `rulesets/ruleset-v2.0.json` frozen ruleset; runs copy it whole into their save file.
- `calibration/` gate: `python3 -m calibration.run` (tests), `python3 -m calibration.report v2.0` (report + freeze).
- `data/` reference data: TQQQ daily OHLC (2020, 2022, Aug 2023 – Nov 2026), CNN Fear & Greed 2021–2026.

Status: Milestone 1 (engine + calibration) passed. Next: playable layers (account, clock, chain display, headlines, bookkeeping, runs, reports).
