# SimQ v2

Weekly options practice simulator on a synthetic TQQQ-like index. `SPEC.md` is the rulebook.

- `simq/` engine: `market.py` (backdrop + sentiment price path, rates), `indicators.py` (Fear & Greed gauge, Sim-tastic Oscillator), `pricing.py` (Black-Scholes, skew, quotes), `ruleset.py` (working parameters).
- `rulesets/ruleset-v2.0.json` frozen ruleset; runs copy it whole into their save file.
- `calibration/` gate: `python3 -m calibration.run` (tests), `python3 -m calibration.report v2.0` (report + freeze).
- `data/` reference data: TQQQ daily OHLC (2020, 2022, Aug 2023 – Nov 2026), CNN Fear & Greed 2021–2026.

Status: Milestone 1 (engine + calibration) passed; playable layers built and play-tested (52 weeks, books reconcile).

## Playing (Claude runs these and relays the output)

```
python3 cli.py new --cash 25000          # start a run (seed hidden); prints Week 1 Monday open
python3 cli.py sell P 48 2               # sell 2 puts at the 48 strike (bid)
python3 cli.py sell C 55 1 [--lot 3]     # covered call; default lot = basis closest to strike
python3 cli.py btc 4                     # buy to close trade 4 (Wednesday, at the ask)
python3 cli.py buy 100 | sellsh 3 [100]  # share trades, round lots
python3 cli.py pass | hold               # explicit no-orders (pass = Monday, hold = Wed / paused Fri)
python3 cli.py undo                      # remove last order at this decision point (never undoes an advance)
python3 cli.py note "text"               # explanation in the run's log
python3 cli.py go                        # advance: Mon -> Wed -> Fri (+ next Mon unless shares held); refuses without orders or pass/hold
python3 cli.py show [--all]              # current decision point; --all = full chain
python3 cli.py report | compare 1 2      # one-pager on demand; cross-run table
python3 cli.py close|abandon "note"      # reveals seed; writes run-close one-pager + workbook
```

Weekly rhythm: after each Friday close (`PUSH DUE`), commit `runs/` as "Run N Week W" and push the v2 branch; copy the run's save and reports to the project. Headlines print as drafts; Claude polishes the wording into ALL-CAPS headlines without changing any fact. Claude never picks or suggests strikes.
