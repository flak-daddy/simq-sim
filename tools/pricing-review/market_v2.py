# Market v2 check (Oct 25, 2026): SimQ year distribution and the pricing-v3 put-seller edge
# under the v1 vs v2 regime-transition tables. Run from the repo root: python3 tools/pricing-review/market_v2.py
import random, math, statistics as st, sys, os
sys.path.insert(0, os.getcwd()); import simq
simq.SKEW_V2 = True; simq.SPREAD_V2 = True
REGS = list(simq.REG)

def year(seed, T):
    S, reg, iv = simq.S_START, "chop", 0.76
    out = []
    for k in range(1, 53):
        rng = random.Random(seed * 1000 + k)
        reg = rng.choices(REGS, weights=[T[reg][x] for x in REGS])[0]
        p = simq.REG[reg]; s0 = S; cl = []; ivs = [iv]
        for _ in range(5):
            u = p["mu"] + p["sig"] * simq.t_draw(rng); r = 3 * u - simq.DRAG
            S = max(0.5, S * max(0.3, 1 + r)); g = rng.gauss(0, 0.02)
            ivs.append(min(1.7, max(0.4, simq.REG3_IV[reg] + 3.0 * max(0.0, -r) + g)))
            cl.append(round(S, 2))
        S = cl[-1]; iv = ivs[-1]
        out.append((reg, s0, cl, ivs))
    return out

def run(T, n=300, seed0=7):
    rng = random.Random(seed0); acc = {}; byreg = {}; fin = []
    for _ in range(n):
        y = year(rng.randrange(10**8, 10**9), T)
        fin.append(y[-1][2][4] / simq.S_START - 1)
        for reg, s0, cl, ivs in y:
            for ph, S, td, j in (("Mon", s0, 5, 0), ("Wed", cl[2], 2, 3)):
                for c in (0.10, 0.15):
                    K = round(S * (1 - c) * 2) / 2
                    b = simq.quote(S, K, td / 252, ivs[j], "P")[0]
                    pay = max(0.0, K - cl[4])
                    a = acc.setdefault((ph, c), [0, 0, 0]); a[0] += b; a[1] += pay; a[2] += K
                    if ph == "Mon" and c == 0.15:
                        x = byreg.setdefault(reg, [0, 0, 0]); x[0] += b; x[1] += pay; x[2] += K
    fin.sort()
    return acc, byreg, fin

if __name__ == "__main__":
    res = {name: run(T) for name, T in (("v1", simq.TRANS), ("v2", simq.TRANS_V2))}
    print("Put held to Friday, edge = bid premium minus payout, % of collateral per week (pricing v3, 300 years):")
    print("| Put | market v1 | market v2 |\n|---|---|---|")
    for ph in ("Mon", "Wed"):
        for c in (0.10, 0.15):
            e = [(a[0] - a[1]) / a[2] * 100 for a in (res[m][0][(ph, c)] for m in ("v1", "v2"))]
            print(f"| {'Monday' if ph == 'Mon' else 'Wednesday'}, {c:.0%} below spot | {e[0]:+.2f}% | {e[1]:+.2f}% |")
    print("\nMonday 15%-below put by regime (edge % of collateral), market v2:")
    for reg in REGS:
        x = res["v2"][1][reg]; print(f"  {reg:8s} {(x[0]-x[1])/x[2]*100:+.2f}%")
    for m in ("v1", "v2"):
        f = res[m][2]; N = len(f)
        print(f"SimQ year, market {m}: median {f[N//2]:+.1%}, P(up) {sum(v > 0 for v in f)/N:.0%}")
