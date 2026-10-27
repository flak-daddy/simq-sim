"""Is SimQ too stingy far from spot? (1) spread cost in actual runs, (2) premium vs distance,
SimQ skew vs a skew shaped like real TQQQ 25-/10-delta data, (3) blind-edge impact."""
import json, math, random, sys
sys.path.insert(0, "."); sys.path.insert(0, "tools/pricing-review")
import simq
simq.SKEW_V2 = True; simq.SPREAD_V2 = True
REG = simq.REG3_IV
def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ---------- 1. spread cost actually paid (pricing v3 runs) ----------
def half(mid): return max(0.01, 0.01 + 0.05 * mid) / 2
print("1. SPREAD COST IN YOUR RUNS (quoted half-spread you gave up at each fill)")
for run in (3, 4, 5):
    ev = json.load(open(f"run-00{run}-state.json"))["events"]
    prem = cost_s = cost_b = 0.0; nb = ns = 0; byd = {}
    for e in ev:
        if e["t"] == "sell":
            mid = (e["fill"] + e["ask"]) / 2; c = (mid - e["fill"]) * 100
            prem += e["fill"] * 100; cost_s += c; ns += 1
            if e["kind"] == "P":
                d = 1 - e["k"] / e["spot"]
                b = "<5%" if d < .05 else "5-10%" if d < .10 else "10-15%" if d < .15 else "15-20%" if d < .20 else "20%+"
                x = byd.setdefault(b, [0, 0.0, 0.0]); x[0] += 1; x[1] += e["fill"]; x[2] += c / 100
        elif e["t"] == "btc":
            p = e["price"]; m = p
            for _ in range(20): m = p - half(m)   # mid implied by the ask paid
            m = max(m, p / 2) if p <= 0.02 else m
            cost_b += (p - m) * 100; nb += 1
    tot = cost_s + cost_b
    print(f"  Run {run}: {ns} sells, {nb} buy-backs | premium ${prem:,.0f} | half-spread on sells ${cost_s:,.0f}, on buy-backs ~${cost_b:,.0f} | total ~${tot:,.0f} = {tot/prem*100:.1f}% of premium")
    if run == 5:
        print("    Run 5 puts by distance below spot: n, avg bid, half-spread as % of mid")
        for b in ("<5%", "5-10%", "10-15%", "15-20%", "20%+"):
            if b in byd:
                n, f, c = byd[b]; print(f"      {b:7s} n={n:3d}  avg bid {f/n:.2f}  half-spread {c/(f+c)*100:4.1f}% of mid")

# ---------- 2. premium vs distance: SimQ skew vs real-shaped skew ----------
# Real 30-day TQQQ (optionsanalysissuite monthly avgs): put25/ATM 1.12 (Aug 2023), 1.09 (May 2022), 1.20 (Mar 2026);
# skew10 ~ 1.9-2.0x skew25. Decomposed (call10/ATM ~ call25/ATM - .02): put10/ATM ~ 1.31 (Aug 23), 1.26 (May 22), 1.52 (Mar 26).
# "Real-shaped" weekly skew: IV multiplier by standardized moneyness z = ln(K/S)/(ATM*sqrt(T)) (~ put delta N(z)).
SHAPES = {"typical (Aug 23 / May 22)": [(0, 1.0), (-0.674, 1.11), (-1.28, 1.29), (-1.645, 1.40)],
          "steep (Mar 2026)":          [(0, 1.0), (-0.674, 1.20), (-1.28, 1.52), (-1.645, 1.66)]}
def real_iv(S, K, T, atm, shape):
    z = math.log(K / S) / (atm * math.sqrt(T))
    if z >= 0: return atm * max(0.6, 1 - 1.3 * (K / S - 1))
    pts = SHAPES[shape]
    for (z0, m0), (z1, m1) in zip(pts, pts[1:]):
        if z >= z1: return atm * (m0 + (m1 - m0) * (z - z0) / (z1 - z0))
    (z0, m0), (z1, m1) = pts[-2], pts[-1]
    return atm * min(2.0, m1 + (m1 - m0) * (z - z1) / (z1 - z0))
def bid_at(S, K, T, iv):
    mid = simq.bs(S, K, T, iv, "P"); return max(0.0, round(mid - half(mid), 2)), mid

S, T = 50.0, 5 / 252
print("\n2. MONDAY 5-DAY PUT BID ($ per contract on a $50 SimQ) vs DISTANCE BELOW SPOT")
print("   SimQ = pricing v3 as is; 'real-shape' = same ATM IV, skew shaped like real TQQQ 25d/10d data")
for reg in ("calm_up", "chop", "rebound", "selloff", "crash"):
    atm = REG[reg]; sd = atm * math.sqrt(T)
    print(f"  {reg:8s} ATM {atm:.0%}, 1-week sd {sd:.1%}")
    for d in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
        K = round(S * (1 - d) * 2) / 2
        b0, m0 = bid_at(S, K, T, simq.skew_iv(S, K, atm))
        b1, _ = bid_at(S, K, T, real_iv(S, K, T, atm, "typical (Aug 23 / May 22)"))
        b2, _ = bid_at(S, K, T, real_iv(S, K, T, atm, "steep (Mar 2026)"))
        z = math.log(K / S) / sd
        print(f"    {d:4.0%} below (K {K:5.1f}, ~{abs(ncdf(z))*100:4.1f}-delta): SimQ ${b0*100:5.0f} ({b0/K*100:.2f}% of strike) | real-shape ${b1*100:5.0f} | steep ${b2*100:5.0f}")

# ---------- 3. blind edge if skew were real-shaped, and if fills were better than the bid ----------
from realism_internal import year  # same daily step as simq market v3
def edge(otm, shape=None, eq=1.0, n=300, seed0=7):
    # mirrors realism_internal.py: Monday open uses last Friday's close and implied vol
    rng = random.Random(seed0); a = [0.0, 0.0, 0.0]
    for _ in range(n):
        d = year(rng.randrange(10**8, 10**9), simq.TRANS_V3)
        S0 = simq.S_START; iv0 = 0.76
        for w in range(52):
            days = d[w*5:(w+1)*5]
            K = round(S0 * (1 - otm) * 2) / 2
            iv = simq.skew_iv(S0, K, iv0) if shape is None else real_iv(S0, K, 5/252, iv0, shape)
            mid = simq.bs(S0, K, 5/252, iv, "P")
            if round(mid - half(mid), 2) > 0:
                a[0] += max(0.0, mid - eq * half(mid)); a[1] += max(0.0, K - days[-1][3])
            a[2] += K
            S0 = days[-1][3]; iv0 = days[-1][4]
    return (a[0] - a[1]) / a[2] * 100
print("\n3. BLIND MONDAY PUT, HELD TO FRIDAY: edge, % of collateral per week (300 years, market v3)")
print("   eq = share of the quoted half-spread you give up (1.0 = always sell at the bid, as SimQ does)")
for otm in (0.10, 0.15, 0.20, 0.25):
    print(f"  {otm:.0%} below: SimQ {edge(otm):+.3f}% | real-shape skew {edge(otm,'typical (Aug 23 / May 22)'):+.3f}% "
          f"| SimQ skew, eq 0.75 {edge(otm,eq=0.75):+.3f}% | eq 0.5 {edge(otm,eq=0.5):+.3f}%")
