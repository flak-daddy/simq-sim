#!/usr/bin/env python3
"""SimQ: synthetic TQQQ-like index for the cc-branch simulator.

Usage (add --seed N to every command; default seed is Run 1's):
  python simq.py newseed             # print a fresh random seed for a new run
  python simq.py open W --seed N     # Week W Monday-open spot + option chain (path not revealed)
  python simq.py mid  W --seed N     # Week W Mon, Tue, Wed closes + Wednesday-close chain
  python simq.py fri  W --seed N     # Week W Thu, Fri closes + Friday settlement price
  python simq.py meta W --seed N     # Claude-only: hidden regime for week W (spoils the game)
Runs: each playthrough has its own seed; start conditions are identical across runs.
Comparison window is 26 sim weeks (MAX_WEEKS).

Fully deterministic: same seed, same market. Weeks are generated in sequence, so
week W's opening price is week W-1's Friday close.
"""
import sys, math, random

BASE_SEED = 20261022
RESEED = {}  # {first_week: seed}: from that week on, a different random stream is used
S_START = 63.80
LEV, DRAG, RATE = 3, 0.0003, 0.04

REG = {
    "calm_up": dict(mu=0.0012, sig=0.009, iv=0.50),
    "chop":    dict(mu=0.0000, sig=0.013, iv=0.58),
    "selloff": dict(mu=-0.0050, sig=0.020, iv=0.72),
    "crash":   dict(mu=-0.0080, sig=0.024, iv=0.90),
    "rebound": dict(mu=0.0070, sig=0.018, iv=0.68),
}
TRANS = {
    "calm_up": {"calm_up": .55, "chop": .25, "selloff": .15, "crash": .03, "rebound": .02},
    "chop":    {"calm_up": .30, "chop": .35, "selloff": .25, "crash": .05, "rebound": .05},
    "selloff": {"calm_up": .05, "chop": .25, "selloff": .30, "crash": .20, "rebound": .20},
    "crash":   {"calm_up": .00, "chop": .10, "selloff": .30, "crash": .20, "rebound": .40},
    "rebound": {"calm_up": .35, "chop": .25, "selloff": .15, "crash": .05, "rebound": .20},
}


def t_draw(rng, df=4):
    z = rng.gauss(0, 1)
    chi = sum(rng.gauss(0, 1) ** 2 for _ in range(df))
    return z / math.sqrt(chi / df) / math.sqrt(df / (df - 2))  # unit variance, fat tails


def gen_week(w):
    S, reg, iv_prev = S_START, "chop", 0.58
    for k in range(1, w + 1):
        seed_k = BASE_SEED
        for w0, s0 in sorted(RESEED.items()):
            if k >= w0:
                seed_k = s0
        rng = random.Random(seed_k * 1000 + k)
        probs = TRANS[reg]
        reg = rng.choices(list(probs), weights=list(probs.values()))[0]
        p = REG[reg]
        s_open, closes, ivs = S, [], [iv_prev]
        for _ in range(5):
            u = p["mu"] + p["sig"] * t_draw(rng)
            r = LEV * u - DRAG
            S = max(0.5, S * max(0.3, 1 + r))
            iv = p["iv"] + 2.5 * max(0.0, -r) + rng.gauss(0, 0.02)
            iv = min(1.3, max(0.35, iv))
            closes.append(round(S, 2))
            ivs.append(iv)
        S = closes[-1]
        iv_prev = ivs[-1]
    return reg, s_open, closes, ivs


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs(S, K, T, iv, kind):
    if T <= 0:
        return max(0.0, (K - S) if kind == "P" else (S - K))
    d1 = (math.log(S / K) + (RATE + iv * iv / 2) * T) / (iv * math.sqrt(T))
    d2 = d1 - iv * math.sqrt(T)
    if kind == "C":
        return S * ncdf(d1) - K * math.exp(-RATE * T) * ncdf(d2)
    return K * math.exp(-RATE * T) * ncdf(-d2) - S * ncdf(-d1)


def quote(S, K, T, iv, kind):
    mid = bs(S, K, T, iv, kind)
    half = max(0.01, 0.03 * mid + 0.01)
    bid = round(max(0.0, mid - half), 2)
    ask = round(mid + half, 2)
    return bid, ask


def chain_rows(S, T_days, iv):
    T = T_days / 252
    # Wide chain: strikes from 50% to 150% of spot.
    # $0.50 steps within 15% of spot, $1 steps to 30%, $2.50 steps beyond.
    rows = []
    for n in range(1, int(S * 1.5 * 2) + 2):
        K = n / 2
        if K < S * 0.5 or K > S * 1.5:
            continue
        d = abs(K / S - 1)
        if d > 0.15 and (d <= 0.30 and K % 1 != 0):
            continue
        if d > 0.30 and K % 2.5 != 0:
            continue
        pb, pa = quote(S, K, T, iv, "P")
        cb, ca = quote(S, K, T, iv, "C")
        rows.append((K, pb, pa, cb, ca))
    return rows


def chain(S, T_days, iv, w):
    rows = chain_rows(S, T_days, iv)
    f = lambda x: "no bid" if x <= 0 else f"{x:.2f}"
    print(f"Spot ${S:.2f} | {T_days} trading day(s) to Friday close")
    print("| Strike | Put ID | Put bid | Put ask | Call bid | Call ask |")
    print("|---|---|---|---|---|---|")
    for K, pb, pa, cb, ca in rows:
        pid = f"SIMQ-W{w:02d}-P{K:g}"
        print(f"| {K:g} | {pid} | {f(pb)} | {pa:.2f} | {f(cb)} | {ca:.2f} |")


MAX_WEEKS = 26  # comparison window; a run may continue past it if the user wants


def main():
    global BASE_SEED
    args = sys.argv[1:]
    if args and args[0] == "newseed":
        import secrets
        print(secrets.randbelow(10**9 - 10**8) + 10**8)
        return
    if "--seed" in args:
        i = args.index("--seed")
        BASE_SEED = int(args[i + 1])
        del args[i:i + 2]
    cmd, w = args[0], int(args[1])
    reg, s_open, closes, ivs = gen_week(w)
    if cmd == "meta":
        print(reg)
    elif cmd == "open":
        print(f"SimQ Week {w} Monday open")
        chain(s_open, 5, ivs[0], w)
    elif cmd == "mid":
        print(f"SimQ Week {w}: Mon close {closes[0]:.2f}, Tue close {closes[1]:.2f}, Wed close {closes[2]:.2f}")
        chain(closes[2], 2, ivs[3], w)
    elif cmd == "fri":
        print(f"SimQ Week {w}: Thu close {closes[3]:.2f}, Fri close (settlement) {closes[4]:.2f}")


if __name__ == "__main__":
    main()
