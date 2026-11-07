"""Option pricing (SPEC §2): Black-Scholes + sentiment IV, steep skew, price floor,
short-expiry steepening, spreads by price/moneyness/fear, light messy quotes."""
import hashlib
import numpy as np
from scipy.special import ndtr

YEAR_DAYS = 252.0


def bs(S, K, T, r, iv, put):
    """T in years. Vectorized; returns option fair value."""
    S, K, T, iv = (np.asarray(x, float) for x in (S, K, T, iv))
    sq = iv * np.sqrt(np.maximum(T, 1e-9))
    d1 = (np.log(S / K) + (r + 0.5 * iv * iv) * T) / sq
    d2 = d1 - sq
    call = S * ndtr(d1) - K * np.exp(-r * T) * ndtr(d2)
    p = call - S + K * np.exp(-r * T)  # put-call parity
    return np.where(put, p, call)


def delta(S, K, T, r, iv, put):
    sq = iv * np.sqrt(np.maximum(T, 1e-9))
    d1 = (np.log(S / K) + (r + 0.5 * iv * iv) * T) / sq
    return np.where(put, ndtr(d1) - 1.0, ndtr(d1))


def strike_iv(pp, spot, K, atm_iv, days):
    """Skew: IV x clamp(1 - slope*(K/S - 1)). Slope steepens with the IV level
    (calm Oct 23 chain 1.3, stressed Nov 6 chain 1.6) and under 5 days to expiry."""
    lo_iv, hi_iv = pp["skew_iv_range"]
    lo_sl, hi_sl = pp["skew_slope_range"]
    w = np.clip((atm_iv - lo_iv) / (hi_iv - lo_iv), 0.0, 1.0)
    slope = (lo_sl + (hi_sl - lo_sl) * w) * (5.0 / np.minimum(np.maximum(days, 0.25), 5.0)) ** pp["skew_short_exp"]
    lo, hi = pp["skew_clamp"]
    return atm_iv * np.clip(1.0 - slope * (np.asarray(K) / spot - 1.0), lo, hi)


def fair(pp, spot, K, days, rate, atm_iv, put):
    T = days / YEAR_DAYS
    iv = strike_iv(pp, spot, K, atm_iv, days)
    return bs(spot, K, T, rate, iv, put), iv


def list_strikes(spot):
    """$1 steps (plus .5 strikes near the money), scaled with price (SPEC §3)."""
    if spot < 15:
        step, half_band = 0.5, None
    elif spot < 150:
        step, half_band = 1.0, 0.10
    else:
        step, half_band = 2.5, None
    lo, hi = spot * 0.40, spot * 1.60
    ks = np.arange(np.floor(lo / step) * step, hi + step, step)
    if half_band is not None:
        halves = np.arange(np.floor(spot * (1 - half_band)) + 0.5, spot * (1 + half_band), 1.0)
        ks = np.union1d(ks, halves)
    return np.round(ks[ks > 0], 2)


def _messy(seed_key, K, frac):
    h = hashlib.sha256(f"{seed_key}|{K:.2f}".encode()).digest()
    x = int.from_bytes(h[:8], "big") / 2 ** 64
    y = int.from_bytes(h[8:16], "big") / 2 ** 64
    return x < frac, y


def quote(pp, spot, K, days, rate, atm_iv, put, fg_score, seed_key=None):
    """Returns (bid, ask, fair, iv) for one strike. bid 0.0 = no bid."""
    f, iv = fair(pp, spot, K, days, rate, atm_iv, put)
    f, iv = float(f), float(iv)
    if f < pp["zero_below"]:
        return 0.0, 0.01, f, iv
    mid = max(f, pp["floor_value"]) if f < pp["floor_value"] else f
    width = pp["spread_base"] + pp["spread_per_dollar"] * mid
    itm = (K > spot) if put else (K < spot)
    if itm:
        depth = abs(K / spot - 1.0) * 100.0
        width *= pp["spread_itm_mult"] * (1.0 + pp["spread_deep_itm_per_pct"] * min(depth, pp["spread_deep_itm_cap_pct"]))
    fear = max(0.0, (25.0 - fg_score) / 25.0)
    width *= 1.0 + pp["spread_fear_mult"] * fear
    if seed_key is not None and abs(K - round(K)) > 0.25:
        hit, y = _messy(seed_key, K, pp["messy_half_strike_frac"])
        if hit:
            lo, hi = pp["messy_mult"]
            width *= lo + (hi - lo) * y
    bid = np.floor((mid - width / 2.0) * 100.0) / 100.0
    ask = np.ceil((mid + width / 2.0) * 100.0) / 100.0
    bid = max(bid, 0.01)
    ask = max(ask, bid + 0.01)
    return round(bid, 2), round(ask, 2), f, iv
