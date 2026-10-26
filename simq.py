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
SPREAD_V2 = True  # tighter spreads calibrated to real TQQQ chains (Oct 24, 2026); set per week by simbook
SKEW_V2 = True      # put/call skew calibrated to real TQQQ chains; set per week by simbook
PRICING_V2_FROM = 1  # weeks >= this use the v2 implied-vol level (REG2) and skew
PRICING = "v3"      # implied-vol level: "v3" (standard for new runs since Oct 24, 2026) or "v2"
                    # (Run 1 W13-26 and Run 2). simbook sets this from the state file; v3 keeps v2 skew/spreads
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
# v2 implied-vol baselines (Oct 24, 2026 calibration: real TQQQ ATM IV ~82% in a calm week)
REG2_IV = {"calm_up": 0.62, "chop": 0.75, "selloff": 1.02, "crash": 1.25, "rebound": 0.90}
# v3 implied-vol baselines (Oct 24, 2026 recalibration; see claude/market-calibration.md, snapshot 2):
# implied vol set relative to each regime's own realized vol, using real TQQQ ratios:
# ~1.3x in calm weeks (weekly options, Oct 2026 chain) and ~1.05x in a sharp selloff (Mar 2026).
REG3_IV = {"calm_up": 0.54, "chop": 0.75, "selloff": 0.92, "crash": 1.05, "rebound": 0.95}
TRANS = {
    "calm_up": {"calm_up": .55, "chop": .25, "selloff": .15, "crash": .03, "rebound": .02},
    "chop":    {"calm_up": .30, "chop": .35, "selloff": .25, "crash": .05, "rebound": .05},
    "selloff": {"calm_up": .05, "chop": .25, "selloff": .30, "crash": .20, "rebound": .20},
    "crash":   {"calm_up": .00, "chop": .10, "selloff": .30, "crash": .20, "rebound": .40},
    "rebound": {"calm_up": .35, "chop": .25, "selloff": .15, "crash": .05, "rebound": .20},
}
# Market v2 (Oct 25, 2026, from Run 5): same regimes (drift, vol, IV), different odds of moving between
# them. v1 above drifted the unleveraged index about -15%/yr (SimQ median year about -58%); v2 drifts it
# about +11%/yr (Nasdaq-like; SimQ median year about +4%). Selloffs are less sticky and dips draw buyers
# (selloff -> rebound .30, crash -> rebound .55). See claude/market-calibration.md, "Market v2".
TRANS_V2 = {
    "calm_up": {"calm_up": .68, "chop": .20, "selloff": .08, "crash": .02, "rebound": .02},
    "chop":    {"calm_up": .43, "chop": .33, "selloff": .14, "crash": .03, "rebound": .07},
    "selloff": {"calm_up": .12, "chop": .30, "selloff": .20, "crash": .08, "rebound": .30},
    "crash":   {"calm_up": .00, "chop": .15, "selloff": .20, "crash": .10, "rebound": .55},
    "rebound": {"calm_up": .50, "chop": .25, "selloff": .10, "crash": .02, "rebound": .13},
}
# Market v3 (Oct 26, 2026, after Run 5; standard from Run 6): v2 with two rows changed by the user.
# crash -> rebound .55 -> .45 (the .10 moves to crash -> chop .15 -> .25); selloff -> rebound .30 -> .35
# (taken from selloff -> chop .30 -> .25). crash -> crash .10 and selloff -> selloff .20 unchanged.
TRANS_V3 = {
    "calm_up": {"calm_up": .68, "chop": .20, "selloff": .08, "crash": .02, "rebound": .02},
    "chop":    {"calm_up": .43, "chop": .33, "selloff": .14, "crash": .03, "rebound": .07},
    "selloff": {"calm_up": .12, "chop": .25, "selloff": .20, "crash": .08, "rebound": .35},
    "crash":   {"calm_up": .00, "chop": .25, "selloff": .20, "crash": .10, "rebound": .45},
    "rebound": {"calm_up": .50, "chop": .25, "selloff": .10, "crash": .02, "rebound": .13},
}
TRANS_BY_MARKET = {"v1": TRANS, "v2": TRANS_V2, "v3": TRANS_V3}
MARKET = "v1"  # regime-transition table: "v1" (Runs 1-4), "v2" (Run 5) or "v3" (standard from Run 6); set by simbook


def t_draw(rng, df=4):
    z = rng.gauss(0, 1)
    chi = sum(rng.gauss(0, 1) ** 2 for _ in range(df))
    return z / math.sqrt(chi / df) / math.sqrt(df / (df - 2))  # unit variance, fat tails


def gen_week(w):
    S, reg, iv_prev, iv_prev2, iv_prev3 = S_START, "chop", 0.58, 0.76, 0.76
    for k in range(1, w + 1):
        seed_k = BASE_SEED
        for w0, s0 in sorted(RESEED.items()):
            if k >= w0:
                seed_k = s0
        rng = random.Random(seed_k * 1000 + k)
        probs = TRANS_BY_MARKET[MARKET][reg]
        reg = rng.choices(list(probs), weights=list(probs.values()))[0]
        p = REG[reg]
        s_open, closes, ivs, ivs2, ivs3 = S, [], [iv_prev], [iv_prev2], [iv_prev3]
        for _ in range(5):
            u = p["mu"] + p["sig"] * t_draw(rng)
            r = LEV * u - DRAG
            S = max(0.5, S * max(0.3, 1 + r))
            g = rng.gauss(0, 0.02)
            iv = min(1.3, max(0.35, p["iv"] + 2.5 * max(0.0, -r) + g))
            iv2 = min(1.7, max(0.5, REG2_IV[reg] + 3.0 * max(0.0, -r) + g))
            iv3 = min(1.7, max(0.4, REG3_IV[reg] + 3.0 * max(0.0, -r) + g))
            closes.append(round(S, 2))
            ivs.append(iv)
            ivs2.append(iv2)
            ivs3.append(iv3)
        S = closes[-1]
        iv_prev, iv_prev2, iv_prev3 = ivs[-1], ivs2[-1], ivs3[-1]
    if PRICING == "v3":
        return reg, s_open, closes, ivs3
    return reg, s_open, closes, (ivs2 if w >= PRICING_V2_FROM else ivs)


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


def skew_iv(S, K, iv):
    # real chains: IV falls ~1.1 vol pts per +1% strike at 82% ATM (puts rich, calls cheap)
    return iv * min(1.5, max(0.6, 1.0 - 1.3 * (K / S - 1.0)))


def quote(S, K, T, iv, kind):
    if SKEW_V2:
        iv = skew_iv(S, K, iv)
    mid = bs(S, K, T, iv, kind)
    if SPREAD_V2:
        # fit to two real TQQQ chains (1-day and 5-day): ~0.02 wide when cheap, ~0.05 near $0.9, ~0.08 near $1.4, ~0.15 near $3
        half = max(0.01, 0.01 + 0.05 * mid) / 2
    else:
        half = max(0.01, 0.03 * mid + 0.01)  # v1, used by Run 1 weeks 1-12
    bid = round(max(0.0, mid - half), 2)
    ask = round(mid + half, 2)
    if ask - bid < 0.01:
        ask = round(bid + 0.01, 2)
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
