# Market v4 check (Oct 28, 2026): v3 table vs v3 + rebound rule (rebound only within 3 weeks of a
# selloff/crash, or with SimQ below half its start price; blocked odds split even / prop / calmchop).
# SimQ year distribution, regime mix, drawdowns, 17-week tail, and the blind put-seller edge (pricing v4 IVs,
# no commission, messy quotes not included). Run from the repo root: python3 tools/pricing-review/market_v4.py
import random, sys, os
sys.path.insert(0, os.getcwd())
import simq
simq.SKEW_V2 = True; simq.SPREAD_V2 = True; simq.PRICING = "v4"
REGS = list(simq.REG)

def year(seed, market, weeks=52, split="even"):
    S, reg, iv = simq.S_START, "chop", 0.76
    hist, out = [], []
    for k in range(1, weeks + 1):
        rng = random.Random(seed * 1000 + k)
        probs = simq.trans_probs(reg, hist, S, market, split)
        reg = rng.choices(list(probs), weights=list(probs.values()))[0]
        hist.append(reg)
        p = simq.REG[reg]; s0 = S; cl = []; ivs = [iv]
        for _ in range(5):
            u = p["mu"] + p["sig"] * simq.t_draw(rng); r = 3 * u - simq.DRAG
            S = max(0.5, S * max(0.3, 1 + r)); g = rng.gauss(0, 0.02)
            ivs.append(min(1.7, max(0.4, simq.REG4_IV[reg] + 3.0 * max(0.0, -r) + g)))
            cl.append(round(S, 2))
        S = cl[-1]; iv = ivs[-1]
        out.append((reg, s0, cl, ivs))
    return out

def stats(market, n=8000, seed0=11, split="even"):
    rng = random.Random(seed0); fin = []; mix = dict.fromkeys(REGS, 0); dd = []; w17 = []
    for _ in range(n):
        y = year(rng.randrange(10**8, 10**9), market, split=split)
        pk = simq.S_START; worst = 0
        for reg, s0, cl, ivs in y:
            mix[reg] += 1
            for c in cl:
                pk = max(pk, c); worst = min(worst, c / pk - 1)
        dd.append(worst); fin.append(y[-1][2][4] / simq.S_START - 1); w17.append(y[16][2][4])
    fin.sort(); dd.sort(); N = len(fin)
    return dict(median=fin[N // 2], p10=fin[N // 10], p90=fin[9 * N // 10], up=sum(f > 0 for f in fin) / N,
                mix={r: mix[r] / (52 * N) for r in REGS}, dd_med=dd[N // 2], dd50=sum(d < -0.5 for d in dd) / N,
                dbl17=sum(x >= 2 * simq.S_START for x in w17) / N, at134=sum(x >= 134.30 for x in w17) / N)

def edge(market, n=300, seed0=7, split="even"):
    rng = random.Random(seed0); acc = {}
    for _ in range(n):
        for reg, s0, cl, ivs in year(rng.randrange(10**8, 10**9), market, split=split):
            for ph, S, td, j in (("Mon", s0, 5, 0), ("Wed", cl[2], 2, 3)):
                for c in (0.10, 0.15):
                    K = round(S * (1 - c) * 2) / 2
                    b = simq.quote(S, K, td / 252, ivs[j], "P")[0]
                    a = acc.setdefault((ph, c), [0, 0, 0]); a[0] += b; a[1] += max(0.0, K - cl[4]); a[2] += K
    return {k: (a[0] - a[1]) / a[2] * 100 for k, a in acc.items()}

if __name__ == "__main__":
    for m, sp in (("v3", "even"), ("v4", "even"), ("v4", "prop"), ("v4", "calmchop")):
        s = stats(m, split=sp); e = edge(m, split=sp)
        print(f"market {m}{'' if m == 'v3' else ' / split ' + sp}: median {s['median']:+.1%}, p10 {s['p10']:+.1%}, p90 {s['p90']:+.1%}, up {s['up']:.0%}")
        print("  mix " + " / ".join(f"{s['mix'][r]:.1%}" for r in REGS) + f" ({'/'.join(REGS)})")
        print(f"  median worst drawdown {s['dd_med']:.0%}, P(dd<-50%) {s['dd50']:.0%}, "
              f"P(doubled by W17) {s['dbl17']:.1%}, P(>=134.30 at W17) {s['at134']:.1%}")
        print("  blind put edge (% collateral/wk): " + ", ".join(f"{ph} {c:.0%} {v:+.2f}%" for (ph, c), v in sorted(e.items())))
