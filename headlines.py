#!/usr/bin/env python3
"""headlines.py: scripted Monday headlines for SimQ (headlines v3).

Rules (v3):
  - Four headlines per week, built from template banks with a seeded random stream, so a
    run's headlines are reproducible and never touch the price path.
  - TRUE slots point at the real regime. They are either hard reported data (rare, about one
    week in three) or opinion.
  - MISLEADING slots point at a wrong regime and are ALWAYS opinion. Reported data never lies.
  - NOISE slots carry no regime direction (company news, routine data, split opinions).
  - Opinion headlines carry honest credibility cues that shift the odds but never decide them:
      basis:     current data (flows, positioning, desk activity) / indirect (valuations,
                 seasonality, chart patterns, history) / none
      incentive: neutral source / positioned source (talking its book)
    True opinions lean toward current-data bases and neutral sources; misleading opinions lean
    toward indirect or no basis and positioned sources. Both kinds appear on both sides.

Friday shows the regime only; there is no per-headline recap in play (print_recap exists for
end-of-run reviews).

Usage:
  python3 headlines.py sample REGIME [--weeks N] [--seed S] [--reveal]
"""
import random
import sys

REGIMES = ["calm_up", "chop", "selloff", "crash", "rebound"]
CONFUSE = {"calm_up": ["chop", "rebound", "selloff"], "chop": ["calm_up", "selloff", "rebound"],
           "selloff": ["crash", "chop", "rebound"], "crash": ["selloff", "rebound", "chop"],
           "rebound": ["calm_up", "crash", "selloff"]}

# ------------------------------------------------------------------ hard reported data (TRUE only)
# Each entry is a statement of fact; FACT_SRC (below) picks who reported it.
FACTS = {
    "calm_up": [
        "realized volatility fell for a fourth straight week",
        "inflows into broad tech funds continued at a steady pace last week",
        "advancing issues outnumbered decliners on four of five days",
        "intraday trading ranges narrowed to their tightest in two months",
        "every pullback of more than 1% last week drew buying within the session",
        "tech fund holdings rose for a third week in modest daily increments",
    ],
    "chop": [
        "the index has closed inside a 3% band for eight straight sessions",
        "tech fund flows flipped between inflows and outflows every day last week",
        "breadth finished last week almost exactly flat",
        "intraday reversals hit their highest count of the quarter",
        "sector leadership changed hands on each of the last five sessions",
        "net positioning in tech futures barely moved for a third week",
    ],
    "selloff": [
        "tech ETF outflows hit a third straight week",
        "decliners outnumbered advancers on four of the last five days",
        "new 52-week lows outpaced new highs for a second week",
        "long-only funds were net sellers into each bounce last week",
        "redemptions from leveraged tech products rose for a second week",
        "tech holdings at large funds fell in steady daily steps last week",
    ],
    "crash": [
        "margin calls at prime brokers hit their highest level in a year",
        "implied volatility jumped to multi-month highs overnight",
        "forced liquidations hit several leveraged tech funds over the weekend",
        "bid-ask spreads on index futures widened to their worst since spring",
        "redemption requests at leveraged ETFs spiked on Friday",
        "overnight futures fell more than 3% with heavy volume",
    ],
    "rebound": [
        "short-covering volume surged in Friday's final hour",
        "the put-call ratio fell sharply from last week's extreme high",
        "buy-side inflows returned after weeks of selling",
        "short interest in leveraged tech products sits at a two-year high and began falling Friday",
        "systematic funds started adding equity exposure from multi-year lows",
        "overnight futures rose more than 2% as heavily shorted names led",
    ],
}
FACT_FORMS = ["{src}: {fact}", "{Fact}, {src_l} show", "{src} show {fact}"]

# ------------------------------------------------------------------ opinions
NEUTRAL_SRC = ["Some strategists", "Several sell-side analysts", "Trading desks", "A widely followed strategist",
               "Economists at a large bank", "A veteran tech analyst", "Market commentators",
               "A few desk heads", "Some portfolio managers"]
POSITIONED_SRC = {
    # sources talking their book: positioned for the view they voice
    "up": ["A fund manager who is heavily long tech", "A bullish investment newsletter",
           "A leveraged-ETF issuer's market outlook", "Retail-trader forums"],
    "down": ["A short seller", "A fund manager positioned for a downturn", "A bearish investment newsletter",
             "A firm that sells crash-protection funds"],
    "flat": ["An options-selling fund manager", "A range-trading newsletter", "A volatility-selling strategy firm"],
}
DIRECTION = {"calm_up": "up", "rebound": "up", "selloff": "down", "crash": "down", "chop": "flat"}
SINGULAR_SRC = {"A widely followed strategist", "A veteran tech analyst"}
VERBS = ["say", "expect", "argue", "see", "think", "suggest", "believe", "warn"]
VERBS_SING = {"say": "says", "expect": "expects", "argue": "argues", "see": "sees", "think": "thinks",
              "suggest": "suggests", "believe": "believes", "warn": "warns"}
THESES = {
    "calm_up": ["the slow grind higher has further to run", "low volatility should hold for the next few weeks",
                "buyers will keep stepping in on small dips", "a quiet, steady drift higher is the likeliest path",
                "nothing on the calendar looks likely to break the calm uptrend"],
    "chop": ["the market is stuck in a range until a real catalyst shows up",
             "neither bulls nor bears have the upper hand right now",
             "back-and-forth trading near current levels is the likeliest path",
             "rallies and dips will keep fading before they get far",
             "this is a market without a direction for now"],
    "selloff": ["tech is due for a stretch of steady selling", "investors will keep trimming exposure into strength",
                "the rally has run out of buyers", "a slow grind lower is more likely than a bounce",
                "the path of least resistance is down, one step at a time"],
    "crash": ["conditions look ripe for a sharp, disorderly drop", "leverage in the system could unwind violently",
              "a sudden liquidation event is a growing risk", "the market is one bad headline from a cascade",
              "a high-stress plunge could come with little warning"],
    "rebound": ["a sharp relief rally is overdue", "bears are positioned too heavily and could get squeezed",
                "the selling looks exhausted and a snap-back may come fast",
                "a violent move higher could catch underweight funds off guard",
                "the bounce, when it comes, should be quick and large"],
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
# odds for opinion cues: (data, indirect, none) and P(positioned source)
BASIS_W = {"true": [0.55, 0.25, 0.20], "misleading": [0.20, 0.45, 0.35]}
POSITIONED_P = {"true": 0.15, "misleading": 0.40}

# ------------------------------------------------------------------ noise
NOISE_FACTS = [
    "A large chipmaker names a new head of its data-center unit",
    "Weekly jobless claims came in close to consensus",
    "A major cloud provider confirms two new regions for next year, capex guidance unchanged",
    "Exchanges publish next year's holiday trading calendar, matching this year's",
    "A semiconductor equipment maker completes a previously announced acquisition",
    "The revised retail sales figure was unchanged from the first estimate",
    "A large software firm moves its earnings date up a week to avoid a holiday",
    "Freight-rail volumes were flat week over week",
    "A payments network reports transaction volume in line with last year",
    "An index provider confirms minor weight changes at its next rebalance",
    "A telecom carrier extends a network-equipment contract on existing terms",
    "A memory-chip maker sets the date for its annual investor day",
    "Mortgage applications were little changed last week",
    "A large e-commerce platform confirms its shareholder meeting date",
    "A chip foundry says its next-generation node remains on schedule",
    "A GPU designer opens a new engineering campus overseas",
]
NOISE_OPINIONS = [
    "Analysts are split on whether chip earnings guidance gets raised or trimmed",
    "Economists disagree on whether next month's jobs report matters for tech",
    "Strategists are divided on what the coming index rebalance means for big tech",
    "Some analysts think AI spending will rise next year; others expect a pause",
    "Commentators debate whether the latest CEO change at a chipmaker matters",
    "Desk strategists are mixed on the holiday-season retail outlook",
]


def _cap(s):
    return s[0].upper() + s[1:]


FACT_SRC = [  # first keyword match picks plausible sources for a fact
    (("margin", "liquidation", "systematic"), ["Prime-broker data", "Prime-broker reports"]),
    (("volatility", "put-call", "implied"), ["Options-market data", "Volatility index data"]),
    (("flow", "redemption", "holdings", "net sellers", "inflows"), ["Fund-flow trackers", "Weekly ETF filings"]),
    (("short interest", "short-covering", "positioning"), ["Futures positioning data", "Exchange short-interest data"]),
    (("advanc", "decliner", "breadth", "lows", "leadership"), ["Breadth figures", "Exchange data"]),
    (("", ), ["Exchange data", "Trading-desk tallies"]),
]


def _fact(rng, reg):
    fact = rng.choice(FACTS[reg])
    src = rng.choice(next(srcs for keys, srcs in FACT_SRC if any(k in fact for k in keys)))
    form = rng.choice(FACT_FORMS)
    text = form.format(src=src, src_l=src[0].lower() + src[1:], fact=fact, Fact=_cap(fact))
    if form == "{src}: {fact}":
        text = f"{src}: {_cap(fact)}"
    return text


def _opinion(rng, reg, kind):
    basis = rng.choices(["data", "indirect", "none"], weights=BASIS_W[kind])[0]
    positioned = rng.random() < POSITIONED_P[kind]
    if positioned:
        src = rng.choice(POSITIONED_SRC[DIRECTION[reg]])
        plural = src.startswith("Retail")
    else:
        src = rng.choice(NEUTRAL_SRC)
        plural = src not in SINGULAR_SRC
    verb = rng.choice(VERBS if DIRECTION[reg] == "down" else [x for x in VERBS if x != "warn"])
    v = verb if plural else VERBS_SING[verb]
    if verb == "see":
        v += " signs that"
    thesis = rng.choice(THESES[reg])
    b = rng.choice(BASIS[basis])
    text = f"{src} {v} {thesis}" + (f", {b}" if b else "")
    return text, basis, positioned


def make_week(seed, w, reg):
    """Return four headline dicts in display order for week w of a run with the given seed."""
    rng = random.Random(f"headlines-v3-{seed}-{w}")
    n_true = rng.choices([0, 1, 2], weights=[0.25, 0.50, 0.25])[0]
    n_mis = rng.choices([0, 1, 2], weights=[0.30, 0.45, 0.25])[0]
    n_mis = min(n_mis, 3 - n_true)
    wrong = rng.choice(CONFUSE[reg])
    slots = ["true"] * n_true
    for _ in range(n_mis):
        slots.append("misleading:" + (wrong if rng.random() < 0.7 else rng.choice(CONFUSE[reg])))
    slots += ["noise"] * (4 - len(slots))
    rng.shuffle(slots)
    # about one week in three carries a hard fact (only ever in a TRUE slot)
    fact_week = n_true > 0 and rng.random() < 0.40
    fact_done = False
    noise_pool_f, noise_pool_o = NOISE_FACTS[:], NOISE_OPINIONS[:]
    rng.shuffle(noise_pool_f); rng.shuffle(noise_pool_o)
    out = []
    for s in slots:
        if s == "true":
            if fact_week and not fact_done:
                fact_done = True
                out.append(dict(text=_fact(rng, reg), label="TRUE", form="reported data",
                                points_to=reg, basis=None, positioned=None))
            else:
                t, b, p = _opinion(rng, reg, "true")
                out.append(dict(text=t, label="TRUE", form="opinion", points_to=reg, basis=b, positioned=p))
        elif s.startswith("misleading"):
            r = s.split(":")[1]
            t, b, p = _opinion(rng, r, "misleading")
            out.append(dict(text=t, label="MISLEADING", form="opinion", points_to=r, basis=b, positioned=p))
        else:
            if rng.random() < 0.7:
                out.append(dict(text=noise_pool_f.pop(), label="NOISE", form="reported news",
                                points_to=None, basis=None, positioned=None))
            else:
                out.append(dict(text=noise_pool_o.pop(), label="NOISE", form="opinion (split)",
                                points_to=None, basis=None, positioned=None))
    return out


def cue_text(h):
    if h["form"] != "opinion":
        return h["form"]
    b = {"data": "cites current data", "indirect": "indirect basis", "none": "no basis given"}[h["basis"]]
    return f"opinion; {b}; {'positioned source' if h['positioned'] else 'neutral source'}"


def print_monday(seed, w, reg):
    print("Headlines")
    for i, h in enumerate(make_week(seed, w, reg), 1):
        print(f"{i}. {h['text']}.")


def print_recap(seed, w, reg):
    print("Headline recap")
    for i, h in enumerate(make_week(seed, w, reg), 1):
        tail = f" (pointed at {h['points_to']})" if h["label"] == "MISLEADING" else ""
        print(f"{i}. {h['label']}{tail}: {cue_text(h)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] != "sample" or len(a) < 2 or a[1] not in REGIMES:
        sys.exit(__doc__)
    n = int(a[a.index("--weeks") + 1]) if "--weeks" in a else 3
    seed = int(a[a.index("--seed") + 1]) if "--seed" in a else 12345
    for w in range(1, n + 1):
        print(f"--- sample week {w} (regime {a[1]}) ---")
        print_monday(seed, w, a[1])
        if "--reveal" in a:
            print_recap(seed, w, a[1])
        print()
