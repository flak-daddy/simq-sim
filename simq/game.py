"""A run's market: the whole path for one seed, and the market state at each decision point.

The path is a pure function of (ruleset, seed). Week 1 Monday is preceded by one hidden
warm-up year so sentiment, the gauge and the oscillator start in a settled state.
"""
import numpy as np

from simq import indicators, market

WARM_DAYS = 260
HORIZON_YEARS = 40          # a run can go 40 sim years (2,080 weeks)
HOLIDAYS = {1: "New Year's week", 27: "Independence Day week", 36: "Labor Day week",
            47: "Thanksgiving week", 52: "Christmas week"}
PHASES = ("mon", "wed", "fri")
PHASE_NAME = {"mon": "Monday open", "wed": "Wednesday close", "fri": "Friday close"}
DAYS_LEFT = {"mon": 5.0, "wed": 2.0}


def start_price_for(rs, seed):
    sp = rs["start_price"]
    return round(float(np.random.default_rng([seed, 1]).uniform(sp["min"], sp["max"])), 2)


class Path:
    def __init__(self, rs, seed):
        self.rs, self.seed = rs, seed
        T = WARM_DAYS + HORIZON_YEARS * 260
        target = start_price_for(rs, seed)
        # The random stream never depends on price level, so a level-free first pass
        # gives the scale that puts Week 1 Monday's open at the run's start price.
        probe = market.generate(rs, seed, WARM_DAYS + 1, 1, start_price=1e6, rate_reset_day=WARM_DAYS)
        scale = target / probe["open"][0, WARM_DAYS]
        m = market.generate(rs, seed, T, 1, start_price=1e6 * scale, rate_reset_day=WARM_DAYS)
        self.m = {k: (v[0] if getattr(v, "ndim", 0) == 2 else v) for k, v in m.items()}
        fg, comps = indicators.fear_greed(m, rs, seed)
        self.fg = fg[0]
        self.comps = {k: v[0] for k, v in comps.items()}
        # split-adjusted series for the oscillator (back-scale history before each split)
        adj = np.ones(T)
        for t in np.where(self.m["split"])[0]:
            adj[:t] *= rs["reverse_split"]["ratio"]
        self.adj = adj
        o = rs["osc"]
        K, D = indicators.stochastic((self.m["high"] * adj)[None], (self.m["low"] * adj)[None],
                                     (self.m["close"] * adj)[None], o["k"], o["d"])
        self.K, self.D = K[0], D[0]
        self.start_price = round(float(self.m["open"][WARM_DAYS]), 2)

    # ---- calendar ----
    @staticmethod
    def day(week, d):
        """Path index of weekday d (0=Mon .. 4=Fri) of run week `week` (1-based)."""
        return WARM_DAYS + (week - 1) * 5 + d

    @staticmethod
    def label(week, phase):
        y, wy = (week - 1) // 52 + 1, (week - 1) % 52 + 1
        s = f"Week {week} (Year {y}, week {wy}) · {PHASE_NAME[phase]}"
        if wy in HOLIDAYS:
            s += f" · {HOLIDAYS[wy]}"
        return s

    # ---- market state at a decision point ----
    def state(self, week, phase):
        m, pp = self.m, self.rs["pricing"]
        if phase == "mon":
            t = self.day(week, 0)
            spot = float(m["open"][t])
            prev = float(m["close"][t - 1]) * (self.rs["reverse_split"]["ratio"] if m["split"][t] else 1.0)
            gap = spot / prev - 1.0
            iv = float(m["iv_atm"][t - 1]) + pp["jump_per_loss"] * max(0.0, -gap)
            ref = t - 1                      # indicators as of last Friday's close
        else:
            t = self.day(week, 2 if phase == "wed" else 4)
            spot, iv, ref, gap = float(m["close"][t]), float(m["iv_atm"][t]), t, None
        return {"week": week, "phase": phase, "t": t, "ref": ref, "spot": round(spot, 2),
                "iv": iv, "rate": float(m["rate"][max(ref, WARM_DAYS)]), "fg": float(self.fg[ref]),
                "days": DAYS_LEFT.get(phase), "gap": gap, "split": bool(m["split"][t]) if phase == "mon" else False}

    def bars(self, week, d0, d1):
        """Daily bars for weekdays d0..d1 of a week."""
        out = []
        for d in range(d0, d1 + 1):
            t = self.day(week, d)
            out.append({k: round(float(self.m[k][t]), 2) for k in ("open", "high", "low", "close")})
        return out

    def indicator_history(self, ref, n=10):
        lo = ref - n + 1
        return {"fg": self.fg[lo:ref + 1].tolist(),
                "comps": {k: float(v[ref]) for k, v in self.comps.items()},
                "K": self.K[lo:ref + 1].tolist(), "D": self.D[lo:ref + 1].tolist()}

    def meeting(self, week):
        t = self.day(week, 4)
        if not self.m["meeting"][t]:
            return None
        return {"decision": int(self.m["decision"][t]), "rate": float(self.m["rate"][t]),
                "p_hike": float(self.m["p_hike"][t]), "p_cut": float(self.m["p_cut"][t])}
