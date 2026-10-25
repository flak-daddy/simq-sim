# TQQQ Cash-Secured Put Simulator: Ledger

## Rules (agreed with user)
- Starting cash: $10,000 (paper)
- Size: 1 contract (100 shares) per trade; collateral = strike x 100 (max strike $100)
- Expiry: Fridays at market close, unless user says "buy to close" earlier
- First expiration: Friday Oct 30, 2026 (user chose to skip Oct 23)
- Strikes: chosen by the user each week from the listed whole or .5 strikes (Claude does not pick or recommend strikes)
- Contracts are identified by Yahoo-style option ID (e.g. TQQQ261030P00064500: ticker, YYMMDD expiry, P/C, strike x 1000); decode and verify each ID on entry
- Sell-to-open fill price: the bid, as pasted by user with time of quote (web lookups of option quotes are unreliable). Exception: when no bid is listed, user may direct use of the last price; noted per trade.
- Buy-to-close fill price: the ask (proposed by Claude, not yet explicitly confirmed by user)
- Mark-to-market of an open put: shown at the ask (cost to close) and at the mid for reference
- Assignment: put is assigned if TQQQ closes below strike on expiration Friday; what to do with shares decided case by case by user
- Idle cash earns money market interest (placeholder 4.00% APY, simple daily accrual, actual/365), accruing from Oct 22, 2026 (day first trade opened), until the rate is revised
- Premium is credited at open; commissions/fees ignored; early assignment not modeled
- Do not include a "hindsight table" of alternative strikes (user declined)
- TQQQ's price can be read from a Yahoo Finance quote/options page the user links, but the fetched copy may be a stale cached snapshot (once returned a Sept 4 page); always check the page's "As of" time. Preferred: user pastes TQQQ price plus put bid/ask with the time. Option contract rows on those pages have not loaded.

## Reports the user wants
- Ledger report on request: account summary, income breakdown, trade log, open position detail, quote history, interest log
- Settlement review after each expiration: where TQQQ closed vs. strike, and how the put's quote moved during the week (from logged snapshots)
- Running scorecard: win rate (expired worthless vs. assigned), average premium as % of collateral, number of assignments, totals

## Current state (as of Thu 2026-10-22, 1:49 PM CT; TQQQ about $66.00)
- Cash balance: $10,096.00 (includes $96 premium; $6,450 of it is locked as collateral)
- Free cash: $3,646.00
- Open position: Trade 1 (short 1 TQQQ261030P00064500), 8 days to expiration; user decided to HOLD (not buy to close) at 1:49 PM CT because the cost to close was too high
- Shares held: 0
- Premium collected to date: $96.00
- Interest earned to date: $0.00 (daily accrual posts as each day completes; about $1.11/day on current cash)
- Realized P&L: $0.00
- Unrealized P&L on Trade 1 (1:44 PM CT quote, bid 2.30 / ask 2.94): -$198.00 at the ask (cost to close $294 vs. $96 received); -$166.00 at the mid ($2.62)
- Account value marked at the ask: $9,802.00 (-$198.00 vs. start, before interest); at the mid: $9,834.00 (-$166.00)

## Trade log
| # | Contract ID | Opened (date/time) | Expiry | Strike | Fill | Ask at open | Premium | Collateral | Result | Notes |
|---|-------------|--------------------|--------|--------|------|-------------|---------|------------|--------|-------|
| 1 | TQQQ261030P00064500 | Thu Oct 22, 2026, 8:30 AM CT | Fri Oct 30, 2026 (8 days) | $64.50 | $0.96 (last price) | none listed | $96.00 | $6,450.00 | Open | No bid/ask listed at 8:30 AM; user directed fill at last price $0.96. Exception to bid rule, quote is not a verified live bid. Oct 22, 1:49 PM CT: user chose to hold rather than buy to close at the $2.94 ask. |

## Decision log
| Date/time (CT) | Trade | Decision | Context |
|----------------|-------|----------|---------|
| Oct 22, 1:49 PM | 1 | Hold (no buy to close) | TQQQ about $66.00 (-9% on day), put bid/ask $2.30/$2.94, cost to close $294 vs. $96 premium; user said cost to close was too high |

## Quote history
| Trade | Time | Bid | Ask | Last | TQQQ | TQQQ vs. $64.50 strike |
|-------|------|-----|-----|------|------|------------------------|
| 1 | Oct 22, 8:30 AM CT | none | none | $0.96 | not recorded | n/a |
| 1 | Oct 22, 8:36 AM CT | not loaded | not loaded | not loaded | $68.95 (-$3.67, -5.05% on day; prior close about $72.62; Yahoo, market open) | +$4.45 above strike (about 6.5%) |
| 1 | Oct 22, 10:47 AM CT (page snapshot) | not loaded | not loaded | not loaded | $67.46 (-$5.15, -7.09% on day; Yahoo) | +$2.96 above strike (about 4.4%) |
| 1 | Oct 22, 1:42 PM CT (user-supplied) | not supplied | not supplied | not supplied | $66.00 (about -9% on day, per user) | +$1.50 above strike (about 2.3%) |
| 1 | Oct 22, 1:44 PM CT (user-supplied) | $2.30 | $2.94 | not supplied | about $66.00 | +$1.50 above strike (about 2.3%) |

## Data quality notes
- 2026-10-21: web sources returned conflicting/stale TQQQ quotes and no verifiable put bid/ask; dry runs done outside the ledger.
- 2026-10-22: Trade 1 opened at 8:30 AM CT (market open) with no bid/ask displayed; fill taken from last price per user instruction.
- 2026-10-22: puts table on Yahoo pages returned "no puts" each time, so option bid/ask could not be read by Claude; user supplied the 1:44 PM bid/ask.
- 2026-10-22: fetch of the plain options link returned a stale Sept 4 page; not logged.
