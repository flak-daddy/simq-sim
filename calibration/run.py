"""Calibration runner (SPEC §10): 2,500 simulated years, all pass/fail tests.

usage: python3 -m calibration.run [ruleset.json] [--out report.md]
"""
import json
import sys
import time

import numpy as np

from simq import indicators, market, ruleset
from calibration import stats

N_PATHS, YEARS, WARM = 100, 26, 1   # 100 x 25 scored years = 2,500
SEED = 20261106


def tests(s, bp):
    sev_per_20y = s["severe_outside_ef"] / s["years"] * 20
    return [
        ("1", "Days moving +/-10% or more, average year", s["big10_avg"], "8-12", 8 <= s["big10_avg"] <= 12),
        ("2", "Crisis years (20+ big days or drawdown < -60%)", s["crisis_rate"], "12.5%-16.7%",
         1 / 8 <= s["crisis_rate"] <= 1 / 6),
        ("3", "Annualized vol, typical (non-crisis) year, median", s["typical_vol_median"], "55%-80%",
         0.55 <= s["typical_vol_median"] <= 0.80),
        ("4", "Median SimQ year", s["median_year"], "+5% to +15%", 0.05 <= s["median_year"] <= 0.15),
        ("5", "Extreme-fear spell length, median (days)", s["ef_spell_median"], "2-5", 2 <= s["ef_spell_median"] <= 5),
        ("6", "Blind put, Monday 10% below, edge %/week", bp, "+0.5% to +1.5%", 0.005 <= bp <= 0.015),
        ("7", "Simulated F&G mean", s["fg_mean"], "40-55", 40 <= s["fg_mean"] <= 55),
        ("8", "F&G extreme fear share of days", s["fg_ef_share"], "8%-20%", 0.08 <= s["fg_ef_share"] <= 0.20),
        ("9", "F&G extreme greed share of days", s["fg_eg_share"], "3%-10%", 0.03 <= s["fg_eg_share"] <= 0.10),
        ("10a", "Worst single day", s["worst_day"], ">= about -35% (-36%)", s["worst_day"] >= -0.36),
        ("10b", "Days worse than -20% with F&G >= 25, per 20 years", sev_per_20y, "< 1", sev_per_20y < 1.0),
        ("11a", "Monday gap, average absolute", s["mon_gap_abs"], "1.5%-2.5%", 0.015 <= s["mon_gap_abs"] <= 0.025),
        ("11b", "Monday gap larger in fear than greed", s["mon_gap_fear"] - s["mon_gap_greed"], "> 0",
         s["mon_gap_fear"] > s["mon_gap_greed"]),
    ]


def main(argv):
    rs = ruleset.load(argv[0]) if argv and argv[0].endswith(".json") else ruleset.default()
    t0 = time.time()
    m = market.generate(rs, SEED, YEARS * 260, N_PATHS)
    fg, _ = indicators.fear_greed(m, rs, SEED)
    s = stats.market_tests(m, fg, WARM)
    edges = {}
    for d, day in [(0.10, "mon"), (0.05, "mon"), (0.15, "mon"), (0.05, "wed"), (0.10, "wed")]:
        e = stats.blind_put(m, fg, rs, d, day, WARM)
        edges[f"{day} {int(d * 100)}%"] = (e.mean(), e.std(), e.min(), np.percentile(e, 1))
    bp = edges["mon 10%"][0]
    res = tests(s, bp)
    return rs, s, edges, res, time.time() - t0


if __name__ == "__main__":
    rs, s, edges, res, secs = main(sys.argv[1:])
    for r in res:
        print(f"{'PASS' if r[4] else 'FAIL'}  {r[0]:4s} {r[1]:52s} {r[2]:.4g}  [{r[3]}]")
    print("all pass:", all(r[4] for r in res), f"({secs:.0f}s)")
    for k, v in edges.items():
        print(f"blind {k}: mean {v[0]*100:+.3f}%  sd {v[1]*100:.2f}%  worst {v[2]*100:.1f}%  1st pct {v[3]*100:.1f}%")
    for k in ("big5_avg", "big15_avg", "year_p10", "year_p90", "years_up", "dd_median", "eg_spell_median",
              "fear_spell_median", "ef_spell_max", "splits", "rate_mean", "rate_min", "rate_max",
              "backdrop_share", "severe_days_per_year", "worst_day_fg", "typical_vol_mean"):
        print(f"  {k:22s} {s[k]:.4g}")
