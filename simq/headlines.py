"""Headlines (SPEC §6): code decides every fact from the sim's own events; Claude polishes
the drafts into ALL-CAPS newspaper headlines when relaying (wording only, never facts).

Sets: 4 at Monday open, 3 at Friday close. Each set mixes
  - reported news and data about what happened (always true),
  - scheduled events (rate meetings, data releases),
  - opinions: TRUE ones point the right way, MISLEADING ones the wrong way, about either
    the near-term mood (next 1-2 weeks, ~70%) or the backdrop (coming months, ~30%),
  - noise (corporate, politics, global markets, routine data).
Opinions carry v1's credibility cues (basis and source), which shift odds, never decide.
Drafts never reveal which opinions are true.
"""
import random

import numpy as np

# ---------------------------------------------------------------- calendar
JOBS_WEEK, CPI_WEEK = 1, 3  # monthly cycle (4 sim weeks): jobs Friday of week 1, CPI Friday of week 3


def month_slot(week):
    return (week - 1) % 4 + 1


# ---------------------------------------------------------------- opinion pieces (v1 cues)
NEUTRAL_SRC = ["Some strategists", "Several sell-side analysts", "Trading desks", "A widely followed strategist",
               "Economists at a large bank", "A veteran tech analyst", "Market commentators",
               "A few desk heads", "Some portfolio managers", "Goldman Sachs strategists",
               "Morgan Stanley's equity team", "A JPMorgan desk note"]
SINGULAR = {"A widely followed strategist", "A veteran tech analyst", "A JPMorgan desk note",
            "Morgan Stanley's equity team"}
NOTE_VERBS = ["say", "argue", "suggest"]   # a written note can't "believe" or "think"
POSITIONED_SRC = {
    "up": ["A fund manager who is heavily long tech", "A bullish investment newsletter",
           "A leveraged-ETF issuer's market outlook", "Retail-trader forums"],
    "down": ["A short seller", "A fund manager positioned for a downturn", "A bearish investment newsletter",
             "A firm that sells crash-protection funds"],
    "flat": ["An options-selling fund manager", "A range-trading newsletter", "A volatility-selling strategy firm"],
}
BASIS = {
    "data": ["citing fund-flow data", "pointing to positioning data", "citing last week's breadth figures",
             "based on what their desks are seeing", "pointing to options-market activity",
             "citing recent client activity"],
    "indirect": ["citing valuations", "pointing to seasonal patterns", "citing a chart pattern",
                 "pointing to a historical parallel", "citing the long-run earnings outlook",
                 "citing the interest-rate backdrop"],
    "none": [""],
}
BASIS_W = {"true": [0.55, 0.25, 0.20], "misleading": [0.20, 0.45, 0.35]}
POSITIONED_P = {"true": 0.15, "misleading": 0.40}
VERBS = ["say", "expect", "argue", "think", "believe", "suggest"]
VERBS_S = {"say": "says", "expect": "expects", "argue": "argues", "think": "thinks", "believe": "believes",
           "suggest": "suggests", "warn": "warns"}
THESES = {
    ("mood", "up"): ["the selling looks exhausted and a rebound is due within a week or two",
                     "fear has run too far and stocks should bounce soon",
                     "the next couple of weeks favor a relief rally",
                     "buyers are about to step back in after the shakeout"],
    ("mood", "down"): ["the pullback has further to go in the coming weeks",
                       "more selling is likely before this settles",
                       "the recent optimism is set to fade over the next couple of weeks",
                       "the near-term path of least resistance is lower"],
    ("mood", "flat"): ["stocks will chop around current levels for the next few weeks",
                       "neither bulls nor bears have the edge in the near term",
                       "expect a quiet, range-bound stretch before any real move"],
    ("backdrop", "up"): ["the economic backdrop supports stocks for months to come",
                         "growth is strong enough to carry tech higher through the next few months",
                         "the macro picture is turning in stocks' favor"],
    ("backdrop", "down"): ["a broader slowdown is only just beginning",
                           "the economy is weakening in ways markets haven't priced",
                           "the next few months look tough for growth stocks"],
    ("backdrop", "flat"): ["growth is middling and the coming months lack a clear trend",
                           "the economy is neither overheating nor stalling",
                           "the macro backdrop is a wash for stocks this season"],
}
OPPOSITE = {"up": ["down", "flat"], "down": ["up", "flat"], "flat": ["up", "down"]}

# ---------------------------------------------------------------- noise banks (real names, ordinary events)
BIG = ["Nvidia", "Apple", "Microsoft", "Alphabet", "Amazon", "Meta", "Broadcom", "AMD", "Netflix", "Tesla",
       "Micron", "Qualcomm", "Intel", "Oracle", "Cisco", "Adobe", "Costco", "Salesforce", "Arm", "Palantir"]
EARN = ["{c} beats estimates and raises its outlook", "{c} tops profit forecasts but guides in line",
        "{c} misses revenue estimates, keeps full-year view", "{c} reports results in line with forecasts",
        "{c} posts record quarterly revenue", "{c} trims guidance on softer demand",
        "{c} beats on earnings, misses on revenue"]
CORP = ["{c} unveils a new flagship product line", "{c} announces a $10 billion buyback",
        "{c} names a new chief financial officer", "{c} prices a multi-tranche bond sale",
        "{c} expands its data-center footprint in Europe", "{c} closes a previously announced acquisition",
        "{c} sets the date for its annual developer conference", "{c} raises its quarterly dividend"]
POLITICS = ["Congress passes a short-term funding bill to avoid a shutdown",
            "Senate committee advances a bipartisan infrastructure bill",
            "White House nominates a new Treasury deputy secretary",
            "Lawmakers debate changes to semiconductor export rules",
            "Treasury's quarterly refunding announcement holds auction sizes steady",
            "Trade talks with Japan wrap up without a new agreement",
            "Governors meet in Washington to discuss disaster funding"]
ROUTINE = ["Weekly jobless claims come in near consensus", "Mortgage applications little changed last week",
           "Existing-home sales edge up slightly", "Consumer sentiment survey roughly unchanged",
           "Freight volumes flat week over week", "Treasury auction draws solid demand",
           "Durable-goods orders match forecasts", "Business inventories rise in line with estimates"]
GLOBAL_IDX = ["Europe's Stoxx 600", "Japan's Nikkei", "Korea's KOSPI", "Taiwan's Taiex", "Hong Kong's Hang Seng",
              "Germany's DAX", "the UK's FTSE 100"]


class _Ctx:
    def __init__(self, run, week, phase):
        self.run, self.p, self.week, self.phase = run, run.path, week, phase
        self.m = run.path.m
        self.rng = random.Random(f"headlines-v2|{run.seed}|{week}|{phase}")
        d4 = self.p.day(week, 4)
        self.ref = d4 if phase == "fri" else self.p.day(week, 0) - 1   # last Friday close for Monday
        self.rwk = week if phase == "fri" else week - 1                  # the week being reported
        self.used = set()

    # weekly underlying (Nasdaq-100-like) return for run week w, Monday open -> Friday close incl. gap
    def idx_week(self, w):
        a, b = self.p.day(w, 0), self.p.day(w, 4)
        return float(np.prod(1 + self.m["u"][a:b + 1]) - 1)

    def direction_mood(self):
        diff = float(self.m["L"][self.ref] - self.m["S"][self.ref])
        return "up" if diff > 6 else "down" if diff < -6 else "flat"

    def direction_backdrop(self):
        return {0: "up", 1: "flat", 2: "down"}[int(self.m["backdrop"][self.ref])]


# ---------------------------------------------------------------- macro data (monthly cycle)
def _jobs(run, week):
    m, p = run.path.m, run.path
    t = p.day(week, 4)
    r = random.Random(f"jobs|{run.seed}|{week}")
    b = int(m["backdrop"][t])
    trend = {0: 175, 1: 120, 2: 40}[b] + 1.2 * (m["S"][t] - 50)
    actual = int(round(trend + r.gauss(0, 45)))
    fc = int(round(({0: 160, 1: 125, 2: 70}[b] + r.gauss(0, 25)) / 5) * 5)
    ur = round(4.2 - 0.004 * (actual - 120) + r.gauss(0, 0.05), 1)
    return actual, fc, ur


def _cpi(run, week):
    m, p = run.path.m, run.path
    t = p.day(week, 4)
    r = random.Random(f"cpi|{run.seed}|{week}")
    infl = float(m["infl"][t])
    core = round(0.25 + 0.10 * infl + r.gauss(0, 0.04), 1)
    fc = round(0.25 + 0.08 * float(m["infl"][t - 20]) + r.gauss(0, 0.03), 1)
    yoy = round(2.6 + 1.1 * infl + r.gauss(0, 0.1), 1)
    return core, fc, yoy


# ---------------------------------------------------------------- builders
def _opinion(c, kind, truth_dir, topic):
    r = c.rng
    d = truth_dir if kind == "true" else r.choice(OPPOSITE[truth_dir])
    basis = r.choices(["data", "indirect", "none"], weights=BASIS_W[kind])[0]
    if r.random() < POSITIONED_P[kind]:
        src = r.choice(POSITIONED_SRC[d])
        plural = src.startswith("Retail")
    else:
        src = r.choice(NEUTRAL_SRC)
        plural = src not in SINGULAR
    verbs = NOTE_VERBS if "note" in src else VERBS
    verb = r.choice(verbs + (["warn"] if d == "down" else []))
    v = verb if plural else VERBS_S[verb]
    b = r.choice(BASIS[basis])
    theses = [x for x in THESES[(topic, d)] if x not in c.used] or THESES[(topic, d)]
    th = r.choice(theses)
    c.used.add(th)
    return f"{src} {v} {th}" + (f", {b}" if b else "")


def _market_news(c):
    """What happened (reported, true). Monday leads with the weekend move and skips
    anything Friday's set already ran."""
    out = []
    if c.phase == "mon":
        g = float(c.m["gap"][c.p.day(c.week, 0)])
        if abs(g) >= 0.004:
            out.append(f"Nasdaq futures point to a {abs(g) * 100:.1f}% {'higher' if g > 0 else 'lower'} open after the weekend")
    m, w = c.m, c.rwk
    if w >= 1:
        wr = c.idx_week(w)
        a, b = c.p.day(w, 0), c.p.day(w, 4)
        days = m["u"][a:b + 1]
        worst, best = float(days.min()), float(days.max())
        verb = "rises" if wr > 0 else "falls"
        out.append(f"Nasdaq 100 {verb} {abs(wr) * 100:.1f}% on the week")
        if worst < -0.03:
            prev = m["u"][:a]
            since = int(np.sum(prev[-260:] <= worst))
            tail = " — worst day in a year" if since == 0 else ""
            out.append(f"Nasdaq 100 sinks {abs(worst) * 100:.1f}% in a single session{tail}")
        if best > 0.03:
            out.append(f"Nasdaq 100 jumps {best * 100:.1f}% in its best day in weeks")
    fg = c.p.fg[c.ref]
    fg_prev = c.p.fg[c.ref - 5]
    if fg < 25 or fg > 75 or abs(fg - fg_prev) > 15:
        lab = "extreme fear" if fg < 25 else "extreme greed" if fg > 75 else ("fear" if fg < 45 else "greed" if fg > 55 else "neutral")
        out.append(f"Fear & Greed gauge {'drops' if fg < fg_prev else 'climbs'} to {fg:.0f} ({lab}) from {fg_prev:.0f} a week ago")
    iv = float(m["iv_atm"][c.ref])
    iv_prev = float(m["iv_atm"][c.ref - 5])
    if abs(iv - iv_prev) > 0.12:
        out.append(f"Options traders {'pay up for protection' if iv > iv_prev else 'unwind hedges'} as implied volatility "
                   f"{'jumps' if iv > iv_prev else 'falls'} to {iv * 100:.0f}%")
    return out


def _scheduled(c):
    out, must = [], []
    w, ph = c.week, c.phase
    meet_this = bool(c.m["meeting"][c.p.day(w, 4)])
    meet_next = bool(c.m["meeting"][c.p.day(w + 1, 4)])
    if ph == "fri":
        mt = c.p.meeting(w)
        if mt:
            d = mt["decision"]
            verb = "holds rates at" if d == 0 else (f"raises rates {abs(d) * 25}bp to" if d > 0 else f"cuts rates {abs(d) * 25}bp to")
            exp = max((mt["p_hike"], "a hike"), (mt["p_cut"], "a cut"), (1 - mt["p_hike"] - mt["p_cut"], "a hold"))
            must.append(f"Fed {verb} {mt['rate'] * 100:.2f}%; futures had priced {exp[0] * 100:.0f}% odds of {exp[1]}")
        if month_slot(w) == JOBS_WEEK:
            a, fc, ur = _jobs(c.run, w)
            must.append(f"Payrolls {'rise' if a >= 0 else 'fall'} {abs(a)},000 vs {fc},000 forecast; unemployment {ur:.1f}%")
        if month_slot(w) == CPI_WEEK:
            core, fc, yoy = _cpi(c.run, w)
            must.append(f"Core CPI rises {core:.1f}% on the month vs {fc:.1f}% expected; headline inflation {yoy:.1f}% on the year")
    else:
        if meet_this:
            t = c.p.day(w, 4)
            ph_, pc_ = float(c.m["p_hike"][t]), float(c.m["p_cut"][t])
            must.append(f"Fed decides Friday; futures price {ph_ * 100:.0f}% odds of a hike, {pc_ * 100:.0f}% a cut")
        elif meet_next:
            out.append("Fed meets next week; traders weigh this week's data")
        if month_slot(w) == JOBS_WEEK:
            out.append("Week ahead: monthly jobs report due Friday")
        if month_slot(w) == CPI_WEEK:
            out.append("Week ahead: consumer prices report due Friday")
    return must, out


def _noise(c):
    r = c.rng
    wy = (c.week - 1) % 52 + 1
    season = (wy % 13) in (3, 4, 5, 6, 7)
    kind = r.choices(["corp", "politics", "global", "routine"], weights=[0.4, 0.15, 0.25, 0.2])[0]
    if kind == "corp":
        bank = EARN if season and r.random() < 0.7 else CORP
        return r.choice(bank).format(c=r.choice(BIG))
    if kind == "politics":
        return r.choice(POLITICS)
    if kind == "routine":
        return r.choice(ROUTINE)
    wr = c.idx_week(c.rwk) if c.rwk >= 1 else 0.0
    g = 0.5 * wr + r.gauss(0, 0.015)
    return f"{r.choice(GLOBAL_IDX)} {'gains' if g > 0 else 'slips'} {abs(g) * 100:.1f}% over the week"


def draft(run, week, phase):
    """Headline drafts in display order (4 Monday, 3 Friday)."""
    n = 4 if phase == "mon" else 3
    c = _Ctx(run, week, phase)
    r = c.rng
    must, sched = _scheduled(c)
    news = _market_news(c)
    if phase == "mon" and week > 1:
        ran = set(draft(run, week - 1, "fri"))
        lead = [x for x in news[:1] if x.startswith("Nasdaq futures")]
        rest = [x for x in news[len(lead):] if x not in ran]
        r.shuffle(rest)
        news = lead + rest
    else:
        r.shuffle(news)
    n_true = r.choices([0, 1, 2], weights=[0.25, 0.50, 0.25])[0]
    n_mis = r.choices([0, 1, 2], weights=[0.30, 0.45, 0.25])[0]
    room = n - len(must) - 1                     # keep at least one reported item
    n_true = min(n_true, max(room, 0))
    n_mis = min(n_mis, max(room - n_true, 0))
    slots = list(must)
    if news:
        slots.append(news.pop(0))
    for kind, k in (("true", n_true), ("misleading", n_mis)):
        for _ in range(k):
            topic = "mood" if r.random() < 0.7 else "backdrop"
            truth = c.direction_mood() if topic == "mood" else c.direction_backdrop()
            slots.append(_opinion(c, kind, truth, topic))
    pool = news + sched
    while len(slots) < n:
        if pool and r.random() < 0.5:
            slots.append(pool.pop(0))
        else:
            h = _noise(c)
            if h not in slots:
                slots.append(h)
    slots = slots[:n]
    head = slots[:len(must)]
    rest = slots[len(must):]
    r.shuffle(rest)
    return head + rest
