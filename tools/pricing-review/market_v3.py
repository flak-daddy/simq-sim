# Market v3 check (Oct 26, 2026): v2 vs v3 regime tables. SimQ year distribution, regime mix,
# crash/selloff weeks per year, worst in-year drawdown, and the pricing-v3 blind put-seller edge.
# Run from the repo root: python3 tools/pricing-review/market_v3.py
import random, sys, os
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(__file__))
import simq
from market_v2 import year
REGS = list(simq.REG)

def stats(T, n=8000, seed0=11):
    rng = random.Random(seed0); fin = []; mix = dict.fromkeys(REGS, 0); dd = []
    for _ in range(n):
        y = year(rng.randrange(10**8, 10**9), T)
        pk = simq.S_START; worst = 0
        for reg, s0, cl, ivs in y:
            mix[reg] += 1
            for c in cl:
                pk = max(pk, c); worst = min(worst, c / pk - 1)
        dd.append(worst); fin.append(y[-1][2][4] / simq.S_START - 1)
    fin.sort(); dd.sort(); N = len(fin)
    return dict(median=fin[N // 2], p10=fin[N // 10], p90=fin[9 * N // 10], up=sum(f > 0 for f in fin) / N,
                mix={r: mix[r] / (52 * N) for r in REGS}, crash=mix["crash"] / N, selloff=mix["selloff"] / N,
                dd_med=dd[N // 2], dd50=sum(d < -0.5 for d in dd) / N)

def edge(T, n=300, seed0=7):
    from market_v2 import run
    acc, byreg, fin = run(T, n, seed0)
    return {k: (a[0] - a[1]) / a[2] * 100 for k, a in acc.items()}

if __name__ == "__main__":
    for name in ("v2", "v3"):
        T = simq.TRANS_BY_MARKET[name]; s = stats(T); e = edge(T)
        print(f"market {name}: SimQ median {s['median']:+.1%}, p10 {s['p10']:+.1%}, p90 {s['p90']:+.1%}, up {s['up']:.0%}; "
              f"mix " + " / ".join(f"{s['mix'][r]:.0%}" for r in REGS) + f" ({'/'.join(REGS)}); crash wk/yr {s['crash']:.1f}, "
              f"selloff wk/yr {s['selloff']:.1f}; median worst drawdown {s['dd_med']:.0%}, P(dd<-50%) {s['dd50']:.0%}")
        print("  blind put edge (% collateral/wk): " + ", ".join(f"{ph} {c:.0%} {v:+.2f}%" for (ph, c), v in sorted(e.items())))
