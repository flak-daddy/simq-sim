# Spread and far-OTM premium check (Oct 26, 2026, after Run 5).
# Question: are SimQ's spreads too wide, and is there too little premium far from spot,
# compared with real TQQQ chains? Uses pricing v3 (skew v2, spreads v2).
# Usage: python3 tools/pricing-review/spread_skew_check.py
import json, math, os, sys, statistics as st
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import simq

simq.PRICING = "v3"; simq.SKEW_V2 = True; simq.SPREAD_V2 = True
N = simq.ncdf


def put_delta(S, K, T, iv):
    d1 = (math.log(S / K) + (simq.RATE + iv * iv / 2) * T) / (iv * math.sqrt(T))
    return N(d1) - 1


def implied_vol(price, S, K, T, kind):
    lo, hi = 0.05, 4.0
    for _ in range(80):
        m = (lo + hi) / 2
        if simq.bs(S, K, T, m, kind) > price: hi = m
        else: lo = m
    return (lo + hi) / 2


here = os.path.join(os.path.dirname(__file__), "..", "..")

# [1] What the player actually traded: put sells in Runs 3-5 (all pricing v3)
print("[1] Put sells in Runs 3-5 (pricing v3), by distance below spot")
rows = []
for run in (3, 4, 5):
    ev = json.load(open(os.path.join(here, f"run-00{run}-state.json")))["events"]
    for e in ev:
        if e.get("t") == "sell" and e.get("kind") == "P":
            S, K, b, a = e["spot"], e["k"], e["fill"], e["ask"]
            mid = (a + b) / 2
            T = (5 if e["ph"] == "open" else 2) / 252
            rows.append(dict(run=run, ph=e["ph"], d=1 - K / S, bid=b, ask=a, mid=mid,
                             sp=(a - b) / mid if mid > 0 else 0, pk=b / K,
                             iv=implied_vol(mid, S, K, T, "P"), T=T, S=S, K=K))
buckets = [(0, .05), (.05, .10), (.10, .15), (.15, .20), (.20, .30), (.30, 1)]
print("  distance  n   median bid  bid % strike  spread % of mid  half-spread lost on sale")
for lo, hi in buckets:
    r = [x for x in rows if lo <= x["d"] < hi]
    if not r: continue
    print(f"  {lo*100:3.0f}-{hi*100:3.0f}%  {len(r):3d}   {st.median(x['bid'] for x in r):6.2f}      "
          f"{st.median(x['pk'] for x in r)*100:5.2f}%        {st.median(x['sp'] for x in r)*100:5.1f}%"
          f"            {st.median((x['mid']-x['bid'])/x['mid'] for x in r)*100:5.1f}%")
ds = sorted(x["d"] for x in rows)
print(f"  all {len(rows)} sells: median distance {st.median(ds)*100:.1f}%, "
      f"share sold 15%+ below spot {sum(d >= .15 for d in ds)/len(ds)*100:.0f}%")

# Spread cost over Run 5: half-spread given up on every sale and every buy-back
ev5 = json.load(open(os.path.join(here, "run-005-state.json")))["events"]
prem = sum(e["fill"] * 100 for e in ev5 if e.get("t") == "sell")
half_sell = sum((e["ask"] - e["fill"]) / 2 * 100 for e in ev5 if e.get("t") == "sell")
half_btc = 0.0
for e in ev5:
    if e.get("t") == "btc":
        a = e["price"]
        mid = a  # solve ask = mid + half(mid) approximately
        for _ in range(20):
            mid = a - max(0.01, 0.01 + 0.05 * mid) / 2
        half_btc += (a - max(mid, 0)) * 100
print(f"\n  Run 5 spread cost: premium collected ${prem:,.0f}; half-spread given up on sales "
      f"${half_sell:,.0f}, on buy-backs about ${half_btc:,.0f}; total about ${half_sell+half_btc:,.0f} "
      f"({(half_sell+half_btc)/prem*100:.0f}% of premium)")

# [2] Spreads: SimQ formula vs real TQQQ quotes (snapshot 1a, Oct 23 2026, 1 day)
print("\n[2] Spreads: real TQQQ 1-day chain (Oct 23, 2026) vs SimQ formula at the same mid")
real = [(59, "P", .05, .07), (60, "P", .08, .10), (61, "P", .14, .16), (62, "P", .23, .26),
        (63, "P", .37, .40), (64, "P", .57, .62), (65, "P", .86, .91), (66, "P", 1.22, 1.28),
        (67, "C", 1.00, 1.05), (68, "C", .59, .63), (69, "C", .32, .35), (70, "C", .16, .17),
        (71, "C", .07, .08), (72, "C", .03, .04)]
tot_r = tot_s = 0
print("  strike  real bid/ask  real spread  SimQ spread at that mid")
for K, k, b, a in real:
    mid = (a + b) / 2; h = max(0.01, 0.01 + 0.05 * mid) / 2
    sb, sa = round(max(0, mid - h), 2), round(mid + h, 2)
    if sa - sb < .01: sa = round(sb + .01, 2)
    tot_r += a - b; tot_s += sa - sb
    print(f"  {K}{k}    {b:.2f}/{a:.2f}     {a-b:.2f}         {sa-sb:.2f}")
print(f"  total width: real {tot_r:.2f}, SimQ {tot_s:.2f}")

# [3] Skew in the far wing
print("\n[3] Far-wing skew: SimQ vs real")
S = 66.29
# 3a: 1-day chain, OTM puts, SimQ IV vs real IV (ATM 83%)
print("  3a. Oct 23 1-day chain (ATM 83%): real put IV vs SimQ skewed IV")
for K, k, b, a in real[:6]:
    riv = implied_vol((a + b) / 2, S, K, 1 / 252, "P")
    print(f"    P{K} ({(1-K/S)*100:4.1f}% below): real {riv*100:5.1f}%  SimQ {simq.skew_iv(S, K, .83)*100:5.1f}%")
# 3b: 30-day 10-delta put vs ATM (real: ATM 71.7%, 10d put = ATM + 29.9 pts, Oct 23 2026)
T = 20 / 252; atm = .717
K = S
while put_delta(S, K, T, simq.skew_iv(S, K, atm)) < -0.10: K -= 0.01
iv10 = simq.skew_iv(S, K, atm)
print(f"  3b. 30-day options, ATM 71.7%: SimQ 10-delta put sits {(1-K/S)*100:.0f}% below spot at IV "
      f"{iv10*100:.1f}% (ATM + {(iv10-atm)*100:.1f} pts); real Oct 23: ATM + 29.9 pts (91st percentile)")
# 3c: same for 5-day options under each regime baseline
print("  3c. 5-day (Monday) options: where the 10-delta and 5-delta puts sit, by regime")
for reg, atm in simq.REG3_IV.items():
    out = []
    for dl in (-0.10, -0.05):
        K = 100.0
        while put_delta(100, K, 5 / 252, simq.skew_iv(100, K, atm)) < dl: K -= 0.01
        out.append(f"{abs(dl)*100:.0f}d at -{100-K:.1f}% (IV x{simq.skew_iv(100, K, atm)/atm:.2f})")
    print(f"    {reg:8s} ATM {atm*100:.0f}%: " + ", ".join(out))

# [4] Premium left far from spot: Monday bid as % of strike by distance and regime
print("\n[4] Monday put bid as % of strike (5-day, regime baseline IV, spot $100, $0.50 strikes)")
dist = [.05, .10, .15, .20, .25, .30]
print("  regime     " + "".join(f"{d*100:>8.0f}%" for d in dist) + "   first no-bid")
for reg, atm in simq.REG3_IV.items():
    cells = []
    for d in dist:
        K = round(100 * (1 - d) * 2) / 2
        b = simq.quote(100, K, 5 / 252, atm, "P")[0]
        cells.append(f"{b/K*100:8.2f}%")
    K = 100.0
    while simq.quote(100, K, 5 / 252, atm, "P")[0] > 0: K -= 0.5
    print(f"  {reg:8s} " + "".join(cells) + f"   {100-K:.0f}% below")
print("  (at SimQ ~$50-75, a $0.01 bid is 0.013-0.02% of strike; '0.00%' means at or near the penny)")

# [5] Candidate: convex put wing (skew v3 candidate), IV factor + C * m^2 for puts, m = 1 - K/S
print("\n[5] Candidate convex put wing: factor = 1 - 1.3(K/S-1) + C*(1-K/S)^2 for K < S (cap 1.5)")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from realism_internal import year
import random
orig = simq.skew_iv
def make(C):
    def f(S, K, iv):
        m = max(0.0, 1 - K / S)
        return iv * min(1.5, max(0.6, 1.0 - 1.3 * (K / S - 1.0) + C * m * m))
    return f
C = 1.0
simq.skew_iv = make(C)
T = 20 / 252; atm = .717; K = S
while put_delta(S, K, T, simq.skew_iv(S, K, atm)) < -0.10: K -= 0.01
print(f"  C={C}: 30-day 10-delta put at ATM + {(simq.skew_iv(S, K, atm)-atm)*100:.1f} pts (real 29.9, current SimQ 24.7); "
      f"5-day P60 on Oct 23 chain {simq.skew_iv(66.29, 60, .82)*100:.1f}% (real 92%, current {orig(66.29, 60, .82)*100:.1f}%)")
print("  Monday bid % of strike, current -> candidate (regime baseline IV, spot $100)")
for reg in ("calm_up", "chop", "selloff"):
    atm = simq.REG3_IV[reg]; cells = []
    for d in (.10, .15, .20, .25):
        K = round(100 * (1 - d) * 2) / 2
        simq.skew_iv = orig; b0 = simq.quote(100, K, 5/252, atm, "P")[0]
        simq.skew_iv = make(C); b1 = simq.quote(100, K, 5/252, atm, "P")[0]
        cells.append(f"{d*100:.0f}%: {b0/K*100:.2f}->{b1/K*100:.2f}")
    print(f"    {reg:8s} " + " | ".join(cells))
def edge(otm, n=300):
    rng = random.Random(7); a = [0, 0, 0]
    for _ in range(n):
        d = year(rng.randrange(10**8, 10**9), simq.TRANS_V3); S0 = simq.S_START; iv0 = .76
        for w in range(52):
            days = d[w*5:(w+1)*5]; K = round(S0 * (1 - otm) * 2) / 2
            b = simq.quote(S0, K, 5/252, iv0, "P")[0]; pay = max(0.0, K - days[-1][3])
            a[0] += b; a[1] += pay; a[2] += K; S0 = days[-1][3]; iv0 = days[-1][4]
    return (a[0] - a[1]) / a[2] * 100
print("  Blind Monday put edge (% collateral/week, 300 years, market v3): current vs candidate")
for otm in (.10, .15, .20):
    simq.skew_iv = orig; e0 = edge(otm); simq.skew_iv = make(C); e1 = edge(otm)
    print(f"    {otm*100:.0f}% below: {e0:+.3f}% -> {e1:+.3f}%")
simq.skew_iv = orig
