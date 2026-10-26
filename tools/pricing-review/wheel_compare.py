# Run 5 vs Run 1 review (Oct 26, 2026). Run from the repo root: python3 tools/pricing-review/wheel_compare.py
# Note: set the pricing (setp) before generating a path, since implied vols are produced with the path.
# Mechanical wheel on any SimQ path under any pricing version, to separate path, pricing and behavior.
import sys, math, random, json, statistics as stt
sys.path.insert(0, '.'); import simq

def setp(pricing):
    if pricing == "v1": simq.PRICING, simq.PRICING_V2_FROM, simq.SKEW_V2, simq.SPREAD_V2 = "v2", 999, False, False
    elif pricing == "v2": simq.PRICING, simq.PRICING_V2_FROM, simq.SKEW_V2, simq.SPREAD_V2 = "v2", 1, True, True
    else: simq.PRICING, simq.PRICING_V2_FROM, simq.SKEW_V2, simq.SPREAD_V2 = "v3", 1, True, True

def path(seed, reseed, market, weeks):
    simq.BASE_SEED, simq.RESEED, simq.MARKET = seed, reseed, market
    return [simq.gen_week(w) for w in range(1, weeks + 1)]

def wheel(P, pricing, otm=0.10, call_otm=0.05, cash=7500.0):
    setp(pricing); lots = []; vals = [cash]; prem_tot = 0; regs = []
    for reg, s0, cl, ivs in P:
        regs.append(reg)
        S = s0; iv = ivs[0]; T = 5 / 252; Fri = cl[4]
        # covered calls on each lot
        calls = []
        for lot in lots:
            K = max(lot, math.ceil(S * (1 + call_otm) * 2) / 2)
            b = simq.quote(S, K, T, iv, "C")[0]
            if b > 0: cash += b * 100; prem_tot += b * 100; calls.append((lot, K))
            else: calls.append((lot, None))
        # puts with free cash
        K = math.floor(S * (1 - otm) * 2) / 2
        n = int(cash // (100 * K)); b = simq.quote(S, K, T, iv, "P")[0]
        if n and b > 0: cash += n * b * 100; prem_tot += n * b * 100
        else: n = 0
        # interest (approx, whole week on cash)
        cash += cash * 0.04 / 52
        # Friday settlement
        newlots = []
        for lot, Kc in calls:
            if Kc is not None and Fri > Kc: cash += Kc * 100
            else: newlots.append(lot)
        if n and Fri < K:
            cash -= n * K * 100; newlots += [K] * n
        lots = newlots
        vals.append(cash + len(lots) * 100 * Fri)
    return vals, prem_tot

def summ(v): return v[-1] / v[0] - 1

if __name__ == "__main__":
    st1 = json.load(open('./run-001-state.json'))
    st5 = json.load(open('./run-005-state.json'))
    def paths(pr):
        setp(pr)
        return (path(st1["seed"], {int(k): v for k, v in st1["reseed"].items()}, "v1", 26), path(st5["seed"], {}, "v2", 52))
    for otm in (0.10, 0.15):
        for pr in ("v1", "v2", "v3"):
            P1, P5 = paths(pr)
            a = summ(wheel(P1, pr, otm)[0]); b = summ(wheel(P5[:26], pr, otm)[0]); c = summ(wheel(P5, pr, otm)[0])
            print(f"wheel {otm:.0%} pricing {pr}: run1 path 26w {a:+.1%} | run5 path 26w {b:+.1%} | run5 path 52w {c:+.1%}")
    # Monte Carlo: blind wheel, 52 weeks, random seeds
    rng = random.Random(5); setp("v3")
    for mk in ("v1", "v2", "v3"):
        for otm in (0.10, 0.15):
            r26 = []; r52 = []; bh = []
            for _ in range(600):
                P = path(rng.randrange(10**8, 10**9), {}, mk, 52)
                v = wheel(P, "v3", otm)[0]; r26.append(v[26] / v[0] - 1); r52.append(v[52] / v[0] - 1); bh.append(P[51][2][4] / simq.S_START - 1)
            r52s = sorted(r52); N = len(r52s)
            pct = sum(x < 0.5213 for x in r52) / N
            print(f"MC market {mk} wheel {otm:.0%} pricing v3: 26w median {stt.median(r26):+.1%} | 52w median {stt.median(r52):+.1%} p10 {r52s[N//10]:+.1%} p90 {r52s[9*N//10]:+.1%}, P(>cash +4%) {sum(x>0.04 for x in r52)/N:.0%}; +52.1% sits at {pct:.0%} pctile; SimQ median {stt.median(bh):+.1%}")
