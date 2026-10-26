# Realism checks on SimQ's own internals (Oct 26, 2026). Run from the repo root:
#   python3 tools/pricing-review/realism_internal.py
# Market v3, pricing v3 unless stated. Re-implements gen_week's daily step so the
# unleveraged index return is visible alongside SimQ's.
import sys, os, math, random, statistics as stt
sys.path.insert(0, os.getcwd()); import simq
simq.SKEW_V2 = True; simq.SPREAD_V2 = True
REGS = list(simq.REG)

def year(rng_seed, T, weeks=52):
    S, I, reg = simq.S_START, 100.0, "chop"
    days = []  # (reg, simq_ret, index_ret, S_close, iv3)
    for k in range(1, weeks + 1):
        rng = random.Random(rng_seed * 1000 + k)
        reg = rng.choices(REGS, weights=[T[reg][x] for x in REGS])[0]
        p = simq.REG[reg]
        for _ in range(5):
            u = p["mu"] + p["sig"] * simq.t_draw(rng)
            r = simq.LEV * u - simq.DRAG
            S = max(0.5, S * max(0.3, 1 + r)); g = rng.gauss(0, 0.02)
            iv3 = min(1.7, max(0.4, simq.REG3_IV[reg] + 3.0 * max(0.0, -r) + g))
            I *= (1 + u)
            days.append((reg, r, u, S, iv3, I))
    return days

def pct(xs, q): xs = sorted(xs); return xs[int(q * (len(xs) - 1))]

if __name__ == "__main__":
    T = simq.TRANS_V3; rng = random.Random(21); N = 3000
    yr_s, yr_i, yr_3x, dd, vol_d, wk = [], [], [], [], [], []
    big_days = worst_day = 0; worst_days = []; flat_decay = []
    regday = {r: [] for r in REGS}
    for _ in range(N):
        d = year(rng.randrange(10**8, 10**9), T)
        s_end, i_end = d[-1][3], d[-1][5]
        yr_s.append(s_end / simq.S_START - 1); yr_i.append(i_end / 100 - 1); yr_3x.append(3 * (i_end / 100 - 1))
        pk = simq.S_START; w = 0
        for x in d:
            pk = max(pk, x[3]); w = min(w, x[3] / pk - 1)
            regday[x[0]].append(x[1])
        dd.append(w)
        rs = [x[1] for x in d]; vol_d.append(stt.pstdev(rs) * math.sqrt(252))
        worst_days.append(min(rs)); big_days += sum(abs(r) > 0.05 for r in rs)
        prev = simq.S_START
        for j in range(4, len(d), 5):
            wk.append(d[j][3] / prev - 1); prev = d[j][3]
        if abs(i_end / 100 - 1) < 0.03: flat_decay.append(s_end / simq.S_START - 1)
    print(f"[1] Years simulated: {N} (market v3)")
    print(f"    SimQ annual return: p10 {pct(yr_s,.1):+.0%}, p25 {pct(yr_s,.25):+.0%}, median {pct(yr_s,.5):+.0%}, p75 {pct(yr_s,.75):+.0%}, p90 {pct(yr_s,.9):+.0%}; mean {stt.mean(yr_s):+.0%}; years up {sum(y>0 for y in yr_s)/N:.0%}")
    print(f"    Unleveraged index annual: median {pct(yr_i,.5):+.1%}, p10 {pct(yr_i,.1):+.0%}, p90 {pct(yr_i,.9):+.0%}")
    print(f"    SimQ vs 3x index return (median gap, decay): {stt.median([a-b for a,b in zip(yr_s, yr_3x)]):+.0%}")
    print(f"    Years with index within +/-3%: n={len(flat_decay)}, SimQ median {stt.median(flat_decay):+.0%} (volatility decay + drag)")
    print(f"    Annualized daily vol: median {stt.median(vol_d):.0%} (p10 {pct(vol_d,.1):.0%}, p90 {pct(vol_d,.9):.0%})")
    print(f"    Max drawdown within year: median {pct(dd,.5):.0%}, p10 {pct(dd,.1):.0%}; years worse than -50%: {sum(x<-.5 for x in dd)/N:.0%}, worse than -70%: {sum(x<-.7 for x in dd)/N:.0%}")
    print(f"    Weekly moves: sd {stt.pstdev(wk):.1%}; weeks < -10%: {sum(w<-.1 for w in wk)/len(wk):.1%} ({sum(w<-.1 for w in wk)/N:.1f}/yr); < -20%: {sum(w<-.2 for w in wk)/N:.2f}/yr; > +10%: {sum(w>.1 for w in wk)/N:.1f}/yr")
    print(f"    Days with |move| > 5%: {big_days/N:.1f}/yr; worst day per year median {stt.median(worst_days):.1%}, p10 {pct(worst_days,.1):.1%}")
    for r in REGS:
        x = regday[r]; print(f"    {r:8s} realized vol {stt.pstdev(x)*math.sqrt(252):.0%} vs v3 base IV {simq.REG3_IV[r]:.0%} (ratio {simq.REG3_IV[r]/(stt.pstdev(x)*math.sqrt(252)):.2f})")

    # [2] pricing sanity
    viol = 0; checks = 0
    for S in (20, 50, 80):
        for iv in (0.5, 0.9, 1.3):
            for Td in (1, 2, 5):
                Tt = Td / 252; Ks = [S * (0.7 + 0.01 * i) for i in range(61)]
                mids = []
                for K in Ks:
                    simq.SKEW_V2 = True
                    ivk = simq.skew_iv(S, K, iv)
                    c = simq.bs(S, K, Tt, ivk, "C"); p = simq.bs(S, K, Tt, ivk, "P")
                    par = c - p - (S - K * math.exp(-simq.RATE * Tt)); checks += 1
                    if abs(par) > 1e-6: viol += 1
                    mids.append(p)
                mono = sum(mids[i+1] < mids[i] - 1e-9 for i in range(len(mids)-1))
                conv = sum(mids[i+1] - 2*mids[i] + mids[i-1] < -1e-6 for i in range(1, len(mids)-1))
                if mono or conv: print(f"    arbitrage flag S{S} iv{iv} T{Td}: monotonic {mono}, convexity {conv}")
    print(f"[2] Put-call parity on mids: {checks - viol}/{checks} pass")

    # [3] blind-edge sensitivity: scale all regime IVs, and calm/chop only
    def edge(scale_all=1.0, scale_calm=1.0, n=300, seed0=7, otm=0.10):
        rng = random.Random(seed0); a = [0, 0, 0]; byr = {r: [0, 0, 0] for r in REGS}
        for _ in range(n):
            d = year(rng.randrange(10**8, 10**9), T)
            S0 = simq.S_START; iv0 = 0.76
            for wkk in range(52):
                days = d[wkk*5:(wkk+1)*5]; reg = days[0][0]
                f = scale_all * (scale_calm if reg in ("calm_up", "chop") else 1.0)
                K = round(S0 * (1 - otm) * 2) / 2
                b = simq.quote(S0, K, 5/252, iv0 * f, "P")[0]
                pay = max(0.0, K - days[-1][3])
                for z in (a, byr[reg]): z[0] += b; z[1] += pay; z[2] += K
                S0 = days[-1][3]; iv0 = days[-1][4]
        return (a[0]-a[1])/a[2]*100, {r: (v[0]-v[1])/v[2]*100 for r, v in byr.items() if v[2]}
    e, byr = edge()
    print(f"[3] Monday 10% put edge, pricing v3: {e:+.2f}%/wk; by regime " + ", ".join(f"{r} {v:+.2f}%" for r, v in byr.items()))
    for f in (0.95, 0.9, 0.85, 0.8):
        print(f"    all IVs x{f}: {edge(scale_all=f)[0]:+.2f}%/wk | calm/chop IVs only x{f}: {edge(scale_calm=f)[0]:+.2f}%/wk")
