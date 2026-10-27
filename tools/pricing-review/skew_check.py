"""Compare SimQ's skew with real TQQQ 25-delta / 10-delta skew (optionsanalysissuite monthly averages)."""
import math, sys
sys.path.insert(0, ".")
import simq
simq.SKEW_V2 = True; simq.SPREAD_V2 = True

def ncdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def delta(S, K, T, iv, kind):
    d1 = (math.log(S / K) + (simq.RATE + iv * iv / 2) * T) / (iv * math.sqrt(T))
    return ncdf(d1) if kind == "C" else ncdf(d1) - 1

def strike_at_delta(S, T, atm, target, kind):
    # walk strikes with SimQ skewed IV until |delta| hits target
    lo, hi = (S * 0.3, S) if kind == "P" else (S, S * 3)
    for _ in range(80):
        K = (lo + hi) / 2
        d = abs(delta(S, K, T, simq.skew_iv(S, K, atm), kind))
        if kind == "P":
            lo, hi = (K, hi) if d < target else (lo, K)
        else:
            lo, hi = (K, hi) if d > target else (lo, K)
    return K

real = {  # month: ATM, call25, put25, skew25, skew10 (30-day options)
    "Aug 2023 (calm)":    (56.9, 51.0, 63.6, 12.5, 24.4),
    "Mar 2026 (selloff)": (72.3, 56.7, 86.4, 29.7, 54.9),
    "May 2022 (crash)":   (101.5, 89.3, 110.5, 21.2, 41.1),
}
S = 100.0
for T_days, lab in ((5, "5-day (SimQ weekly)"), (21, "21-day (same tenor as the real data)")):
    T = T_days / 252
    print(f"\nSimQ skew formula, {lab}")
    print(f"{'month':20s} {'ATM':>5s} | {'real p25/ATM':>12s} {'SimQ':>6s} | {'real c25/ATM':>12s} {'SimQ':>6s} | {'real skew25':>11s} {'SimQ':>6s} | {'real skew10':>11s} {'SimQ':>6s} | SimQ 10d put strike")
    for m, (atm, c25, p25, s25, s10) in real.items():
        a = atm / 100
        out = {}
        for kind in "PC":
            for dlt in (0.25, 0.10):
                K = strike_at_delta(S, T, a, dlt, kind)
                out[(kind, dlt)] = (K, simq.skew_iv(S, K, a) * 100)
        sk25 = out[("P", .25)][1] - out[("C", .25)][1]
        sk10 = out[("P", .10)][1] - out[("C", .10)][1]
        print(f"{m:20s} {atm:5.1f} | {p25/atm:12.2f} {out[('P',.25)][1]/atm:6.2f} | {c25/atm:12.2f} {out[('C',.25)][1]/atm:6.2f} | {s25:11.1f} {sk25:6.1f} | {s10:11.1f} {sk10:6.1f} | {out[('P',.10)][0]-100:+.1f}%")
