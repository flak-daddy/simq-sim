"""Calibration statistics (SPEC §10) computed from generated market arrays."""
import numpy as np

DPY = 260  # 52 weeks x 5 days


def cc_returns(m):
    """Close-to-close SimQ returns, split-adjusted (N, T)."""
    c = m["close"]
    prev = np.concatenate([m["open"][:, :1], c[:, :-1]], axis=1)
    ratio = np.where(m["split"], 10.0, 1.0)  # split multiplies the prior close
    return c / (prev * ratio) - 1.0


def spells(mask_row):
    """Lengths of consecutive True runs in a 1-D bool array."""
    x = np.concatenate([[0], mask_row.astype(int), [0]])
    d = np.diff(x)
    st, en = np.where(d == 1)[0], np.where(d == -1)[0]
    return en - st


def all_spells(mask):
    return np.concatenate([spells(r) for r in mask]) if mask.size else np.array([])


def yearly(m, warm_years=1):
    r = cc_returns(m)
    N, T = r.shape
    Y = T // DPY
    rows = []
    for p in range(N):
        for y in range(warm_years, Y):
            ry = r[p, y * DPY:(y + 1) * DPY]
            lvl = np.cumprod(1 + ry)
            dd = (lvl / np.maximum.accumulate(np.concatenate([[1.0], lvl]))[1:] - 1).min()
            big = int((np.abs(ry) >= 0.10).sum())
            rows.append({
                "ret": lvl[-1] - 1, "vol": ry.std() * np.sqrt(252), "big10": big,
                "big5": int((np.abs(ry) >= 0.05).sum()), "big15": int((np.abs(ry) >= 0.15).sum()),
                "dd": dd, "worst": ry.min(), "crisis": big >= 20 or dd < -0.60,
            })
    return rows


def market_tests(m, fg, warm_years=1):
    rows = yearly(m, warm_years)
    w = warm_years * DPY
    ret = np.array([x["ret"] for x in rows])
    vol = np.array([x["vol"] for x in rows])
    big = np.array([x["big10"] for x in rows])
    crisis = np.array([x["crisis"] for x in rows])
    r = cc_returns(m)[:, w:]
    fgw = fg[:, w:]
    S = m["S"][:, w:]
    # Monday gaps (SimQ): open / prior close - 1 on Mondays (excluding split days)
    gaps = m["open"][:, w:] / np.concatenate([m["close"][:, w - 1:w], m["close"][:, w:-1]], 1) - 1
    mon = (np.arange(r.shape[1]) % 5 == 0)[None, :] & ~m["split"][:, w:]
    g = np.abs(gaps[mon])
    fg_mon = np.concatenate([fg[:, w - 1:w], fgw[:, :-1]], 1)[mon]  # F&G at the prior Friday
    worst_day_idx = np.unravel_index(np.argmin(r), r.shape)
    severe = r < -0.20
    out = {
        "years": len(rows),
        "big10_avg": big.mean(),
        "crisis_rate": crisis.mean(),
        "typical_vol_median": np.median(vol[~crisis]),
        "typical_vol_mean": vol[~crisis].mean(),
        "median_year": np.median(ret),
        "ef_spell_median": np.median(all_spells(fgw < 25)),
        "ef_spell_max": all_spells(fgw < 25).max(),
        "ef_spell_p99": np.percentile(all_spells(fgw < 25), 99),
        "eg_spell_max": all_spells(fgw > 75).max(),
        "eg_spell_median": np.median(all_spells(fgw > 75)),
        "fear_spell_median": np.median(all_spells(fgw < 45)),
        "fg_mean": fgw.mean(),
        "fg_ef_share": (fgw < 25).mean(),
        "fg_eg_share": (fgw > 75).mean(),
        "worst_day": r.min(),
        "worst_day_fg": fgw[worst_day_idx],
        "severe_days_per_year": severe.sum() / len(rows),
        "severe_outside_ef": int((severe & (fgw >= 25)).sum()),
        "mon_gap_abs": g.mean(),
        "mon_gap_fear": g[fg_mon < 45].mean() if (fg_mon < 45).any() else np.nan,
        "mon_gap_greed": g[fg_mon > 55].mean() if (fg_mon > 55).any() else np.nan,
        "big5_avg": np.mean([x["big5"] for x in rows]),
        "big15_avg": np.mean([x["big15"] for x in rows]),
        "year_p10": np.percentile(ret, 10), "year_p90": np.percentile(ret, 90),
        "years_up": (ret > 0).mean(),
        "dd_median": np.median([x["dd"] for x in rows]),
        "S_mean": S.mean(),
        "splits": int(m["split"].sum()),
        "rate_mean": m["rate"][:, w:].mean(),
        "rate_min": m["rate"][:, w:].min(), "rate_max": m["rate"][:, w:].max(),
    }
    db, ds = m["drift_backdrop"][:, w:], m["drift_sent"][:, w:]
    vb = db.var()
    vt = (m["u"][:, w:]).var()
    out["backdrop_share"] = vb / vt
    out["sentiment_share"] = 1 - vb / vt
    return out


def blind_put(m, fg, rs, dist=0.10, day="mon", warm_years=1):
    """Blind seller: sell the listed put nearest at/below (1-dist)*spot at the bid,
    hold to Friday close. Returns weekly edge (premium - payout) / collateral."""
    from simq import pricing
    pp = rs["pricing"]
    N, T = m["close"].shape
    w0 = warm_years * DPY
    edges = []
    for p in range(N):
        for t in range(w0, T - 4, 5):
            if day == "mon":
                spot = m["open"][p, t]
                gap = spot / m["close"][p, t - 1] - 1 if not m["split"][p, t] else 0.0
                iv = m["iv_atm"][p, t - 1] + pp["jump_per_loss"] * max(0.0, -gap)
                rate, g, days = m["rate"][p, t - 1], fg[p, t - 1], 5.0
            else:  # Wednesday close
                spot = m["close"][p, t + 2]
                iv, rate, g, days = m["iv_atm"][p, t + 2], m["rate"][p, t + 2], fg[p, t + 2], 2.0
            ks = pricing.list_strikes(spot)
            ks = ks[ks <= spot * (1 - dist) + 1e-9]
            if len(ks) == 0:
                continue
            K = ks[-1]
            bid, ask, f, _ = pricing.quote(pp, spot, K, days, rate, iv, True, g)
            if bid <= 0:
                edges.append(0.0)
                continue
            fri = m["close"][p, t + 4]
            edges.append((bid - max(0.0, K - fri)) / K)
    return np.array(edges)
