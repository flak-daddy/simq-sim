"""Ruleset: every parameter of a run (SPEC.md Rule 0).

DEFAULT is the working ruleset during calibration. When the calibration report
passes, it is frozen to rulesets/ruleset-v2.0.json and runs read only that file.
"""
import copy
import json

DEFAULT = {
    "ruleset_id": "v2.0-draft",
    "days_per_week": 5,
    "weeks_per_year": 52,

    # §1.1 backdrop: 3 slow states; only moves sentiment's resting level
    "backdrop": {
        "states": ["bull", "neutral", "bear"],
        "rest_level": [58.0, 47.0, 28.0],
        "mean_days": [160.0, 120.0, 110.0],
        # where a backdrop goes when it changes (rows sum to 1, diagonal 0)
        "next": [[0.0, 0.85, 0.15],
                 [0.55, 0.0, 0.45],
                 [0.25, 0.75, 0.0]],
        "start_probs": [0.4, 0.4, 0.2],
    },

    # §1.1 sentiment 0-100
    "sentiment": {
        "half_life_days": 15.0,
        "start": 50.0,
        "price_feedback": 330.0,     # S points per unit of underlying return
        "noise_sd": 1.5,             # S points/day independent of price
        "noise_df": 4.0,
        "floor": 1.0,
        "ceil": 99.0,
    },

    # §1.2 underlying (pre-leverage) daily volatility by sentiment, linear interp
    "vol_curve": {
        "s":  [0.0, 10.0, 20.0, 35.0, 50.0, 60.0, 75.0, 100.0],
        "sd": [0.0265, 0.0220, 0.0186, 0.0160, 0.0130, 0.0114, 0.0100, 0.0090],
    },
    "drift": {
        "base_daily": 0.00065,       # underlying drift, all states
        "sentiment_link": 1.0,       # price drift = link * expected S recovery / feedback
    },
    "returns": {
        # Student-t tails by sentiment: fat in fear, thinner in calm/greed
        "df_curve": {"s": [0.0, 10.0, 25.0, 45.0, 100.0], "df": [3.2, 3.5, 4.5, 6.5, 8.0]},
        "leverage": 3.0,
        "expense_ratio": 0.0095,     # yearly
        "financing_mult": 2.0,       # 2x rate borrowed (3x fund)
        "max_abs_underlying": 0.117, # caps a day (incl. Monday gap) near -35% / +35%
    },
    "weekend_gap": {"scale": 0.70},  # weekend shock sd as a multiple of daily sd
    "intraday": {"range_scale": 0.55},

    # §1.3 / §1.4
    "start_price": {"min": 30.0, "max": 90.0},
    "reverse_split": {"threshold": 2.50, "ratio": 10},

    # §2.6 central bank
    "rates": {
        "start": 0.035, "min": 0.01, "max": 0.08, "step": 0.0025,
        "meeting_every_weeks": 6,
        "infl_persist": 0.995, "infl_sd": 0.07,
        "w_infl": 1.0, "w_sent": 0.025, "w_backdrop": [0.3, 0.0, -0.4],
        "w_level": 0.35,             # pull back toward 3.5% (neutral rate)
        "neutral": 0.035,
        "threshold": 1.0, "steepness": 2.0,
        "double_step_below_s": 12.0, "double_step_prob": 0.35,
        "surprise_s_per_step": -8.0,     # S points per 0.25% hawkish surprise
        "surprise_u_per_step": -0.008,   # underlying return per 0.25% hawkish surprise
    },

    # §2 option pricing
    "pricing": {
        # 5-day ATM implied vol by hidden sentiment (linear interp), before the down-day
        # jump; set so IV / forward realized = 1.05 (S<25) ... 1.30 (S>75), as real chains
        "iv_curve": {"s":  [0.0, 10.0, 20.0, 35.0, 50.0, 60.0, 75.0, 100.0],
                     "iv": [0.914, 0.773, 0.676, 0.649, 0.613, 0.584, 0.528, 0.484]},
        "jump_per_loss": 3.0,        # IV += 3 x SimQ loss on a down day
        "jump_half_life_days": 1.0,
        # IV x (1 - slope * (K/S - 1)); slope 1.3 at calm IV (Oct 23 chain) to 1.6 at
        # stressed IV (Nov 6 chain), linear in ATM IV between the two
        "skew_slope_range": [1.3, 1.6], "skew_iv_range": [0.82, 1.01],
        "skew_short_exp": 0.33,      # slope x (5/days)^0.33 under 5 days
        "skew_clamp": [0.55, 1.6],
        "floor_value": 0.02,         # far OTM mid floor, dollars
        "zero_below": 0.002,         # fair value below this: no bid
        "spread_base": 0.01, "spread_per_dollar": 0.05,
        "spread_itm_mult": 3.0, "spread_deep_itm_per_pct": 0.08,
        "spread_fear_mult": 0.6,     # +60% at F&G 0, fading to 0 at 25
        "messy_half_strike_frac": 0.10, "messy_mult": [3.0, 5.0],
    },

    # §12.1 Fear & Greed gauge
    "fg": {
        "mom_ma": 125, "mom_scale": 0.07, "mom_center": 0.02,
        "vol_ma": 50, "vol_scale": 0.20,
        "pc_days": 5, "pc_base": 0.90, "pc_per_s": 0.006, "pc_noise": 0.04, "pc_scale": 0.15,
        "haven_days": 20, "haven_scale": 0.06, "bond_beta": -0.15, "bond_noise": 0.002, "haven_center": 0.01,
        "breadth_span": 15, "breadth_noise": 0.4, "breadth_scale": 0.35,
        "noise_sd": 1.0,
        "smooth_down": 0.80, "smooth_up": 0.25,
    },
    "osc": {"k": 14, "d": 3, "oversold": 20.0, "overbought": 80.0},
}


def default():
    return copy.deepcopy(DEFAULT)


def load(path):
    with open(path) as f:
        return json.load(f)


def save(rs, path):
    with open(path, "w") as f:
        json.dump(rs, f, indent=1)
