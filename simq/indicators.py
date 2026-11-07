"""Fear & Greed gauge (SPEC §12.1) and Sim-tastic Oscillator (§12.2).

The gauge reads simulated market data, not the hidden sentiment directly, so it
tracks the mood with lag and noise and can mislead at turning points.
"""
import numpy as np


def _roll_mean(x, n):
    """Trailing mean over n days (shorter at the start), axis 1."""
    c = np.cumsum(x, axis=1)
    out = c.copy()
    out[:, n:] = c[:, n:] - c[:, :-n]
    cnt = np.minimum(np.arange(1, x.shape[1] + 1), n)
    return out / cnt


def _ema(x, span):
    a = 2.0 / (span + 1.0)
    out = np.empty_like(x)
    out[:, 0] = x[:, 0]
    for t in range(1, x.shape[1]):
        out[:, t] = a * x[:, t] + (1 - a) * out[:, t - 1]
    return out


def _asym_smooth(x, a_down, a_up):
    """Fear arrives fast, greed returns slowly (like the real index)."""
    out = np.empty_like(x)
    out[:, 0] = x[:, 0]
    for t in range(1, x.shape[1]):
        a = np.where(x[:, t] < out[:, t - 1], a_down, a_up)
        out[:, t] = a * x[:, t] + (1 - a) * out[:, t - 1]
    return out


def _to_score(z):
    return 50.0 + 50.0 * np.tanh(z)


def fear_greed(m, rs, seed):
    """Returns (score, components dict), each (N, T), 0-100."""
    p = rs["fg"]
    rng = np.random.default_rng([seed, 12])
    u, S, iv = m["u"], m["S"], m["iv_atm"]
    N, T = u.shape
    idx = np.cumprod(1.0 + u, axis=1)  # underlying index, split-free

    mom = _to_score((idx / _roll_mean(idx, p["mom_ma"]) - 1.0 - p["mom_center"]) / p["mom_scale"])
    vol = _to_score(-(iv / _roll_mean(iv, p["vol_ma"]) - 1.0) / p["vol_scale"])
    pcr_daily = p["pc_base"] - p["pc_per_s"] * (S - 50.0) + p["pc_noise"] * rng.normal(size=(N, T))
    pc = _to_score(-(_roll_mean(pcr_daily, p["pc_days"]) - p["pc_base"]) / p["pc_scale"])
    bond = p["bond_beta"] * u + p["bond_noise"] * rng.normal(size=(N, T))
    haven = _to_score((_roll_mean(u - bond, p["haven_days"]) * p["haven_days"] - p["haven_center"]) / p["haven_scale"])
    sd = np.interp(S, rs["vol_curve"]["s"], rs["vol_curve"]["sd"])
    up = (u - 0.0) / sd + p["breadth_noise"] * rng.normal(size=(N, T))
    breadth = _to_score(_ema(up, p["breadth_span"]) / (p["breadth_scale"] * 3.0))

    comps = {"momentum": mom, "volatility": vol, "put_call": pc,
             "safe_haven": haven, "breadth": breadth}
    score = np.mean(list(comps.values()), axis=0) + p["noise_sd"] * rng.normal(size=(N, T))
    score = np.clip(_asym_smooth(score, p["smooth_down"], p["smooth_up"]), 0.0, 100.0)
    return score, comps


def fg_label(x):
    if x < 25:
        return "extreme fear"
    if x < 45:
        return "fear"
    if x <= 55:
        return "neutral"
    if x <= 75:
        return "greed"
    return "extreme greed"


def stochastic(high, low, close, k=14, d=3):
    """%K and %D, (N, T); NaN until k days exist."""
    N, T = close.shape
    K = np.full((N, T), np.nan)
    for t in range(k - 1, T):
        hh = high[:, t - k + 1:t + 1].max(1)
        ll = low[:, t - k + 1:t + 1].min(1)
        K[:, t] = 100.0 * (close[:, t] - ll) / np.maximum(hh - ll, 1e-12)
    D = np.full((N, T), np.nan)
    for t in range(k + d - 2, T):
        D[:, t] = K[:, t - d + 1:t + 1].mean(1)
    return K, D
