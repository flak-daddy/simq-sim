"""Market engine (SPEC §1, §2.6): backdrop + sentiment -> daily OHLC, IV level, rates.

Vectorized over n_paths so the calibration runner and the game share one code path.
The price path never depends on the player's trades, so a run's whole path is a pure
function of (ruleset, seed).
"""
import numpy as np

LN2 = np.log(2.0)


def _tnorm(rng, df, size):
    """Student-t draw scaled to unit variance."""
    return rng.standard_t(df, size) * np.sqrt((df - 2.0) / df)


def _interp(x, xs, ys):
    return np.interp(x, xs, ys)


def generate(rs, seed, n_days, n_paths=1, start_price=None, rate_reset_day=None):
    rng = np.random.default_rng(seed)
    N, T = n_paths, n_days
    bd, se, rt, pr = rs["backdrop"], rs["sentiment"], rs["returns"], rs["pricing"]
    rr = rs["rates"]
    lev = rt["leverage"]
    k = 1.0 - np.exp(-LN2 / se["half_life_days"])
    phi = se["price_feedback"]
    rest = np.array(bd["rest_level"])
    mean_days = np.array(bd["mean_days"])
    nxt = np.array(bd["next"])
    vs, vsd = rs["vol_curve"]["s"], rs["vol_curve"]["sd"]
    ivs, ivv = pr["iv_curve"]["s"], pr["iv_curve"]["iv"]
    jdecay = 0.5 ** (1.0 / pr["jump_half_life_days"])
    cap = rt["max_abs_underlying"]
    step = rr["step"]
    meet_every = rr["meeting_every_weeks"]

    if start_price is None:
        sp = rs["start_price"]
        start_price = np.round(rng.uniform(sp["min"], sp["max"], N), 2)
    P0 = np.broadcast_to(np.asarray(start_price, float), (N,)).copy()

    out = {key: np.zeros((N, T)) for key in
           ("open", "high", "low", "close", "S", "iv_atm", "rate", "u", "gap", "u_shock",
            "drift_backdrop", "drift_sent", "p_hike", "p_cut", "infl", "L")}
    out["backdrop"] = np.zeros((N, T), dtype=np.int8)
    out["split"] = np.zeros((N, T), dtype=bool)
    out["meeting"] = np.zeros((N, T), dtype=bool)
    out["decision"] = np.zeros((N, T))          # rate change in steps
    out["start_price"] = P0.copy()

    b = rng.choice(3, size=N, p=bd["start_probs"])
    S = np.full(N, se["start"], float)
    rate = np.full(N, rr["start"], float)
    infl = rng.normal(0.0, rr["infl_sd"] / np.sqrt(1 - rr["infl_persist"] ** 2), N)
    jump = np.zeros(N)
    close_prev = P0.copy()

    for t in range(T):
        wd = t % 5
        if t == rate_reset_day:          # a run's Week 1 starts at the ruleset's start rate
            rate = np.full(N, rr["start"], float)
        # backdrop switch
        sw = rng.random(N) < 1.0 / mean_days[b]
        if sw.any():
            cum = nxt[b[sw]].cumsum(1)
            b[sw] = (rng.random(sw.sum())[:, None] > cum).sum(1)
        L = rest[b]
        sd = _interp(S, vs, vsd)

        # open: weekend gap + reverse split check (Friday close below threshold)
        gap = np.zeros(N)
        if t == 0:
            opn = P0.copy()
        elif wd == 0:
            low = close_prev < rs["reverse_split"]["threshold"]
            if low.any():
                close_prev = np.where(low, close_prev * rs["reverse_split"]["ratio"], close_prev)
                out["split"][low, t] = True
            gdf = _interp(S, rt["df_curve"]["s"], rt["df_curve"]["df"])
            gap = np.clip(rs["weekend_gap"]["scale"] * sd * rng.standard_t(gdf) * np.sqrt((gdf - 2.0) / gdf),
                          -cap, cap)
            opn = close_prev * (1.0 + lev * gap)
            S = S + phi * gap
        else:
            opn = close_prev.copy()

        # sentiment-set drift: the expected sentiment recovery shows up in price
        exp_dS = k * (L - S)
        mu_sent = rs["drift"]["sentiment_link"] * exp_dS / phi
        mu = rs["drift"]["base_daily"] + mu_sent
        out["drift_backdrop"][:, t] = rs["drift"]["sentiment_link"] * k * (L - 47.0) / phi
        out["drift_sent"][:, t] = mu_sent

        # central bank meeting at Friday close every N weeks
        rate_u = np.zeros(N)
        rate_s = np.zeros(N)
        if wd == 4 and ((t // 5) + 1) % meet_every == 0:
            score = (rr["w_infl"] * infl + rr["w_sent"] * (S - 50.0)
                     + np.array(rr["w_backdrop"])[b]
                     + rr["w_level"] * (rr["neutral"] - rate) / step / 4.0)
            ph = 1 / (1 + np.exp(-rr["steepness"] * (score - rr["threshold"])))
            pc = 1 / (1 + np.exp(-rr["steepness"] * (-score - rr["threshold"])))
            tot = ph + pc
            over = tot > 0.95
            ph = np.where(over, ph * 0.95 / tot, ph)
            pc = np.where(over, pc * 0.95 / tot, pc)
            x = rng.random(N)
            dec = np.where(x < ph, 1.0, np.where(x < ph + pc, -1.0, 0.0))
            dbl = (dec != 0) & (S < rr["double_step_below_s"]) & (rng.random(N) < rr["double_step_prob"])
            dec = np.where(dbl, dec * 2, dec)
            new = np.clip(rate + dec * step, rr["min"], rr["max"])
            dec = np.round((new - rate) / step)
            surprise = dec - (ph - pc)
            rate = new
            rate_s = rr["surprise_s_per_step"] * surprise
            rate_u = rr["surprise_u_per_step"] * surprise
            out["meeting"][:, t] = True
            out["decision"][:, t] = dec
            out["p_hike"][:, t] = ph
            out["p_cut"][:, t] = pc
        infl = rr["infl_persist"] * infl + rr["infl_sd"] * rng.normal(size=N)

        df = _interp(S, rt["df_curve"]["s"], rt["df_curve"]["df"])
        shock = sd * rng.standard_t(df) * np.sqrt((df - 2.0) / df)
        # intraday move within the cap, and Friday close -> Monday close also within it
        lo_b = np.maximum(-cap, ((1 - lev * cap) / (1 + lev * gap) - 1) / lev)
        hi_b = np.minimum(cap, ((1 + lev * cap) / (1 + lev * gap) - 1) / lev)
        u = np.clip(mu + shock + rate_u, lo_b, hi_b)
        r = lev * u - (rt["expense_ratio"] + rt["financing_mult"] * rate) / 252.0
        cls = opn * (1.0 + r)

        # sentiment update: mean reversion + price feedback + independent news noise
        S = (S + exp_dS + phi * (u - mu) + se["noise_sd"] * _tnorm(rng, se["noise_df"], N)
             + rate_s)
        S = np.clip(S, se["floor"], se["ceil"])

        # intraday range
        rsd = rs["intraday"]["range_scale"] * lev * sd
        hi = np.maximum(opn, cls) * (1 + np.abs(rng.normal(size=N)) * rsd)
        lo = np.minimum(opn, cls) * np.maximum(1 - np.abs(rng.normal(size=N)) * rsd, 0.5)

        cc = cls / close_prev - 1.0
        jump = jump * jdecay + pr["jump_per_loss"] * np.maximum(0.0, -cc)
        iv = _interp(S, ivs, ivv) + jump

        o = out
        o["open"][:, t], o["close"][:, t] = opn, cls
        o["high"][:, t], o["low"][:, t] = hi, lo
        o["S"][:, t], o["backdrop"][:, t] = S, b
        o["iv_atm"][:, t], o["rate"][:, t] = iv, rate
        o["u"][:, t], o["gap"][:, t] = u + gap, gap
        o["u_shock"][:, t] = shock
        o["infl"][:, t], o["L"][:, t] = infl, L
        close_prev = cls
    return out
