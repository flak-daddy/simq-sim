# SimQ v2 — Play handoff (Nov 6, 2026)

Start here to play a v2 run. The build is done; ruleset `v2.0` passed the calibration gate and is frozen.

## Setup each chat
1. Clone `flak-daddy/simq-sim`, check out branch `v2`.
2. `python3 cli.py status` shows the active run (if any) and where it stands. No active run: `python3 cli.py new --cash N` (the user picks N).
3. Rules live in `SPEC.md`. Calibration evidence: `calibration/report-v2.0.md`.

## Each decision point
- **Never run `go` unless the user's latest message contains orders or says pass/hold.** After `new`, and after every `go`, stop and wait: the CLI prints `WAITING for ...`. (`go` also refuses on its own until orders or an explicit `pass`/`hold` are entered.)
- Run the user's orders with the CLI, then `python3 cli.py go`. If the user says pass (Monday) or hold (Wednesday, or Friday when shares are held), run `pass`/`hold` first.
- A wrong order entered at the current decision point can be removed with `undo` before advancing. Advances can't be undone: they reveal new prices. If an advance happens by mistake, add a `note "..."` to the log explaining it and ask the user whether to continue or abandon.
- Auto-advance: Monday → Wednesday → Friday → next Monday, pausing on Friday only when shares are held. Separate days with `-----------------`.
- Relay script output only, **as markdown, not inside a code block**, so headers, bold lines and tables render (v1 style, decided Nov 6). No commentary unless the user asks. Monday order: account → headlines → indicators → position → chain. Keep every chain row in the window (user's choice).
- Headlines print as a numbered list of drafts. Rewrite each in place into an ALL-CAPS newspaper headline: wording only, never a fact, number or direction; keep the opinion's source and basis cue; never hint which opinions are true.
- Claude never picks, suggests or recommends strikes.
- Input slips: a call with no shares, or "buy" an option to open → don't execute; ask what was meant.

## Weekly
- After each Friday close (`PUSH DUE`): commit `runs/` as "Run N Week W", push `v2`, and copy the run's `save.json` and any new reports to the project (`claude/v2-runs/run-NNN/`).
- Weeks 26 and 52: the CLI writes the mentor one-pager PDF to `runs/run-NNN/reports/`; send it to the user.
- Run close (`close` / `abandon`): seed revealed; one-pager + workbook written.

## Incident log
- Nov 6, 2026: Run 1 (first chat) — `go` was run right after `new` without the user's orders, skipping Week 1 Monday. Fix: `go` guard, `pass`/`hold`, `undo`, `note`, and the rule above. Run 1 is abandoned ("operator error at Week 1 Monday"); play resumes with Run 2 on a new seed.

## Rule 0
Never change a run's rules mid-run. Bugs get fixed and the run continues. Rule changes go into the next ruleset (`v2.1`) and must pass the gate first.

## Known characteristics of v2.0 (decided, not bugs)
- Real-chain IV: a blind Monday put 10% below spot earns about +0.66% of collateral per week; a mechanical sell-8%-below / buy-back-at-80% strategy had a median year of +62% across 30 test years (6 of 30 down, worst −48%). The user kept this as is on Nov 6, 2026 (no IV trim, no blind-seller benchmark).
- Extreme-fear spells: median 4 days; rare long ones (99th percentile 29 days).
- Backdrop-topic opinions carry little near-term information; mood-topic opinions carry most of it.
