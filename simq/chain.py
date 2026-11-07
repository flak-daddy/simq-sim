"""Chain builder (SPEC §3): every listed strike quoted for this Friday's expiry.

Fills, buy-backs and the display all read the same chain, so they always agree.
"""
import numpy as np

from simq import pricing

EDGE_BID = 0.10


def contract_id(week, side, K):
    k = f"{K:g}"
    return f"SIMQ-W{week:02d}-{side}{k}"


def build(rs, seed, st, keep=()):
    """All strikes for the decision point `st` (from Path.state). `keep` adds strikes listed
    earlier this week, which stay listed until expiry. Returns list of rows."""
    pp = rs["pricing"]
    spot, days, rate, iv, fg = st["spot"], st["days"], st["rate"], st["iv"], st["fg"]
    key = f"{seed}|{st['week']}|{st['phase']}"
    ks = np.union1d(pricing.list_strikes(spot), np.asarray(list(keep), float))
    T = days / pricing.YEAR_DAYS
    rows = []
    for K in ks:
        pb, pa, pf, piv = pricing.quote(pp, spot, K, days, rate, iv, True, fg, key)
        cb, ca, cf, civ = pricing.quote(pp, spot, K, days, rate, iv, False, fg, key)
        rows.append({"K": float(K), "pb": pb, "pa": pa, "cb": cb, "ca": ca,
                     "pd": float(pricing.delta(spot, K, T, rate, piv, True)),
                     "cd": float(pricing.delta(spot, K, T, rate, civ, False))})
    # never out of order: put bids/asks rise with strike, call bids/asks fall. A messy
    # (deliberately wide) quote is clipped to its neighbours, never copied along the column.
    for side, rising in (("p", True), ("c", False)):
        seq = rows if rising else rows[::-1]        # ordered by rising option value
        for i in range(1, len(seq)):                # bid never below the cheaper neighbour's bid
            if seq[i][side + "b"] > 0 or seq[i - 1][side + "b"] > 0:
                seq[i][side + "b"] = max(seq[i][side + "b"], seq[i - 1][side + "b"])
        for i in range(len(seq) - 2, -1, -1):       # ask never above the richer neighbour's ask
            seq[i][side + "a"] = min(seq[i][side + "a"], seq[i + 1][side + "a"])
        for r in rows:
            if r[side + "b"] > 0:
                r[side + "a"] = max(r[side + "a"], round(r[side + "b"] + 0.01, 2))
    return rows


def find(rows, K):
    for r in rows:
        if abs(r["K"] - K) < 1e-9:
            return r
    return None


def window(rows, spot):
    """Default window: from spot outward until the OTM option's bid falls below $0.10
    (that edge strike shown) on each side."""
    below = [i for i, r in enumerate(rows) if r["K"] <= spot]
    above = [i for i, r in enumerate(rows) if r["K"] > spot]
    lo = below[0] if below else 0
    for i in reversed(below):
        lo = i
        if rows[i]["pb"] < EDGE_BID:
            break
    hi = above[-1] if above else len(rows) - 1
    for i in above:
        hi = i
        if rows[i]["cb"] < EDGE_BID:
            break
    return lo, hi
