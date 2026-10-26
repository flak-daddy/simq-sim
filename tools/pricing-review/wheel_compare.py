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

def run_path(n, pricing):
    st = json.load(open(f"./run-{n:03d}-state.json"))
    setp(pricing)
    weeks = 26 if n == 1 else 52
    return path(st["seed"], {int(k): v for k, v in st.get("reseed", {}).items()}, st.get("market", "v1"), weeks)

if __name__ == "__main__":
    # Usage: python3 tools/pricing-review/wheel_compare.py [RUN RUN ...]   (default: 1 2 5)
    runs = [int(a) for a in sys.argv[1:]] or [1, 2, 5]
    for otm in (0.10, 0.15):
        for pr in ("v1", "v2", "v3"):
            cells = []
            for n in runs:
                v = wheel(run_path(n, pr), pr, otm)[0]
                cells.append(f"run {n}: 26w {v[26]/v[0]-1:+.1%}" + (f", 52w {v[52]/v[0]-1:+.1%}, H2 {v[52]/v[26]-1:+.1%}" if len(v) > 27 else ""))
            print(f"blind wheel {otm:.0%} pricing {pr} | " + " | ".join(cells))
    rng = random.Random(9)
    for mk, pr in (("v1", "v2"), ("v2", "v3"), ("v3", "v3")):
        for otm in (0.10, 0.15):
            r = []
            for _ in range(600):
                setp(pr); v = wheel(path(rng.randrange(10**8, 10**9), {}, mk, 52), pr, otm)[0]; r.append(v[52] / v[0] - 1)
            r.sort(); N = len(r)
            print(f"MC market {mk}, pricing {pr}, blind {otm:.0%} wheel, 52w: median {r[N//2]:+.1%}, p10 {r[N//10]:+.1%}, p90 {r[9*N//10]:+.1%}, beats cash {sum(x > 0.04 for x in r)/N:.0%}")
