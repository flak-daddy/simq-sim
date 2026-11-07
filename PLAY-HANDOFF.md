# SimQ v2 — Play handoff (Nov 6, 2026)

Start here to play a v2 run. The build is done; ruleset `v2.0` passed the calibration gate and is frozen.

## Current state (Nov 6, 2026, end of build chat)
- Branch `v2` is clean and verified from a fresh clone: `new` → guard blocks `go` → `pass` → Wednesday → `hold` → Friday settles → next Monday.
- Run 1: abandoned (operator error), kept in `runs/run-001/`. The next run is **Run 2**.
- Output is rendered chat markdown (v1 style). Wednesday includes the buy-to-close table (cost to close, P/L if closed).
- Opening a new chat: just say "Start SimQ" (new run) or "Resume SimQ" (continue the active run). Claude does setup and asks only for starting cash.

## Starting a session (standard: Claude does all setup)
The user's opening message can be as short as **"Start SimQ"** or **"Resume SimQ"**. Claude then, without asking the user to run or read any commands:
1. Clones `flak-daddy/simq-sim`, checks out branch `v2`, and runs `python3 cli.py status`.
2. **If a run is active** (only possible within the same chat workspace): shows where it stands and relays the current decision point with `show`.
3. **If no run is active:** asks the user one question, the starting cash, as a multiple-choice prompt (e.g. $10,000 / $25,000 / $50,000, with "Other" for any amount). Nothing else is asked.
4. Runs `python3 cli.py new --cash N` with the answer, relays Week 1 Monday open as rendered markdown with polished headlines, then stops and waits for orders.
5. Resuming in a new chat works from the last push: `status` finds the active run in `runs/` on its own and continues from its last pushed Friday close. Anything played after the last push lived only in the old chat; Claude says so if the run's clock looks behind what the user remembers.

Rules live in `SPEC.md`. Calibration evidence: `calibration/report-v2.0.md`.

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
