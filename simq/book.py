"""Bookkeeping (SPEC §4, §7): the append-only event log is the only source of truth.
Cash, positions, lots, scorecard and week P&L are all derived by replaying it.

Event types: sell, btc, buy_shares, sell_shares, relot, pass, expire, assign, called,
interest, split, note, close_run.
"""
from collections import OrderedDict

CONTRACT = 100


class Book:
    def __init__(self, start_cash):
        self.start_cash = start_cash
        self.cash = start_cash
        self.trades = OrderedDict()   # tid -> trade
        self.lots = OrderedDict()     # lot id -> lot
        self.weeks = {}               # week -> dict of week flows
        self.interest_total = 0.0

    # ---- helpers ----
    def wk(self, w):
        return self.weeks.setdefault(w, {"premium": 0.0, "buyback": 0.0, "interest": 0.0,
                                         "capital": 0.0, "opened": [], "events": []})

    def open_trades(self, side=None):
        return [t for t in self.trades.values() if t["open_n"] > 0 and (side is None or t["side"] == side)]

    def collateral(self):
        return sum(t["K"] * CONTRACT * t["open_n"] for t in self.open_trades("P"))

    def free_cash(self):
        return self.cash - self.collateral()

    def covered(self, lot_id):
        return sum(t["open_n"] for t in self.open_trades("C") if t["lot"] == lot_id)

    def free_contracts(self, lot_id):
        lot = self.lots[lot_id]
        return lot["shares"] // CONTRACT - self.covered(lot_id)

    def open_lots(self):
        return [l for l in self.lots.values() if l["shares"] > 0]

    def shares(self):
        return sum(l["shares"] for l in self.open_lots())

    @staticmethod
    def eff_basis(lot):
        return (lot["cost"] - lot["credit"] - lot["proceeds"]) / lot["shares"] if lot["shares"] else None

    # ---- replay ----
    def apply(self, e):
        f = getattr(self, "_" + e["type"], None)
        if f:
            f(e)
        if "week" in e:
            self.wk(e["week"])["events"].append(e)

    def _sell(self, e):
        amt = e["price"] * CONTRACT * e["n"]
        self.cash += amt
        t = {"tid": e["tid"], "cid": e["cid"], "side": e["side"], "K": e["K"], "n": e["n"], "open_n": e["n"],
             "price": e["price"], "week": e["week"], "phase": e["phase"], "lot": e.get("lot"),
             "spot": e["spot"], "btc_n": 0, "btc_cost": 0.0, "expired_n": 0, "assigned_n": 0,
             "called_n": 0, "status": "open", "outcome": None}
        self.trades[e["tid"]] = t
        w = self.wk(e["week"])
        w["premium"] += amt
        w["capital"] += (e["K"] if e["side"] == "P" else e["spot"]) * CONTRACT * e["n"]
        w["opened"].append(e["tid"])
        if e["side"] == "C":
            self.lots[e["lot"]]["credit"] += amt

    def _btc(self, e):
        t = self.trades[e["tid"]]
        amt = e["price"] * CONTRACT * e["n"]
        self.cash -= amt
        t["open_n"] -= e["n"]
        t["btc_n"] += e["n"]
        t["btc_cost"] += amt
        self.wk(t["week"])["buyback"] += amt
        if t["side"] == "C":
            self.lots[t["lot"]]["credit"] -= amt
        self._maybe_resolve(t)

    def _expire(self, e):
        t = self.trades[e["tid"]]
        t["expired_n"] += t["open_n"]
        t["open_n"] = 0
        self._maybe_resolve(t)

    def _assign(self, e):
        t = self.trades[e["tid"]]
        n = t["open_n"]
        self.cash -= t["K"] * CONTRACT * n
        prem_share = t["price"] * CONTRACT * n   # premium on the assigned contracts goes to the lot
        self.lots[e["lot"]] = {"id": e["lot"], "shares": CONTRACT * n, "orig": CONTRACT * n,
                               "cost": t["K"] * CONTRACT * n, "credit": prem_share, "proceeds": 0.0,
                               "source": "assigned", "strike": t["K"], "week": e["week"], "put": t["tid"],
                               "status": "open", "outcome": None}
        t["assigned_n"] += n
        t["open_n"] = 0
        t["lot_made"] = e["lot"]
        t["status"] = "assigned"

    def _called(self, e):
        t = self.trades[e["tid"]]
        n = t["open_n"]
        lot = self.lots[t["lot"]]
        amt = t["K"] * CONTRACT * n
        self.cash += amt
        t["called_n"] += n
        t["open_n"] = 0
        t["status"] = "called"
        self._reduce_lot(lot, CONTRACT * n, amt)

    def _buy_shares(self, e):
        cost = e["price"] * e["n"]
        self.cash -= cost
        self.lots[e["lot"]] = {"id": e["lot"], "shares": e["n"], "orig": e["n"], "cost": cost, "credit": 0.0,
                               "proceeds": 0.0, "source": "bought", "strike": e["price"], "week": e["week"],
                               "put": None, "status": "open", "outcome": None}

    def _sell_shares(self, e):
        amt = e["price"] * e["n"]
        self.cash += amt
        self._reduce_lot(self.lots[e["lot"]], e["n"], amt)

    def _relot(self, e):
        t = self.trades[e["tid"]]
        amt = t["price"] * CONTRACT * t["n"] - t["btc_cost"]
        self.lots[t["lot"]]["credit"] -= amt
        self.lots[e["lot"]]["credit"] += amt
        t["lot"] = e["lot"]

    def _interest(self, e):
        self.cash += e["amount"]
        self.interest_total += e["amount"]
        self.wk(e["week"])["interest"] += e["amount"]

    def _split(self, e):
        r = e["ratio"]
        for lot in self.open_lots():
            new = lot["shares"] // r
            frac = lot["shares"] / r - new
            cash_in_lieu = round(frac * e["new_price"], 2)
            if cash_in_lieu:
                self.cash += cash_in_lieu
                lot["proceeds"] += cash_in_lieu
            lot["shares"] = new
            lot["orig"] = lot["orig"] / r
        e["applied"] = True

    def _reduce_lot(self, lot, shares, proceeds):
        lot["shares"] -= shares
        lot["proceeds"] += proceeds
        if lot["shares"] == 0:
            lot["status"] = "closed"
            net = lot["proceeds"] + lot["credit"] - lot["cost"]
            lot["outcome"] = net
            # resolve the trades whose outcome waited on this lot
            for t in self.trades.values():
                if t.get("lot_made") == lot["id"] or (t["side"] == "C" and t["lot"] == lot["id"] and t["status"] == "called"):
                    # wheel outcome: the lot's result plus any contracts of this trade bought back earlier
                    extra = t["price"] * CONTRACT * t["btc_n"] - t["btc_cost"] if t.get("lot_made") else 0.0
                    t["lot_net"] = net + extra
                    t["outcome"] = "win" if t["lot_net"] > 0 else "loss"

    def _maybe_resolve(self, t):
        if t["open_n"] > 0 or t["status"] in ("assigned",):
            return
        if t["status"] == "called":
            return  # judged when its lot exits
        net = t["price"] * CONTRACT * t["n"] - t["btc_cost"]
        t["status"] = "expired" if t["btc_n"] == 0 else ("closed" if t["expired_n"] == 0 else "mixed")
        t["outcome"] = "win" if net > 0 else "loss"
        t["net"] = net

    # ---- views ----
    def shares_value(self, price):
        return self.shares() * price

    def account_value(self, price, option_liab=0.0):
        return self.cash + self.shares_value(price) - option_liab

    def scorecard(self):
        ts = list(self.trades.values())
        judged = [t for t in ts if t["outcome"] in ("win", "loss")]
        wins = [t for t in judged if t["outcome"] == "win"]
        held = [t for t in ts if t["status"] in ("expired", "assigned", "called")]
        weeks = [w for w in self.weeks.values() if w["capital"] > 0]
        prem_pct = [(w["premium"] - w["buyback"]) / w["capital"] for w in weeks]
        return {
            "trades": len(ts), "open": len([t for t in ts if t["open_n"] > 0]),
            "judged": len(judged), "wins": len(wins),
            "win_rate": len(wins) / len(judged) if judged else None,
            "pending": len([t for t in ts if t["outcome"] is None and t["open_n"] == 0]),
            "held_to_expiry": len(held), "held_pct": len(held) / len(ts) if ts else None,
            "assigned": len([t for t in ts if t["assigned_n"] > 0]),
            "called": len([t for t in ts if t["called_n"] > 0]),
            "avg_week_prem_pct": sum(prem_pct) / len(prem_pct) if prem_pct else None,
            "weeks_traded": len(weeks),
        }


def replay(save):
    b = Book(save["run"]["start_cash"])
    for e in save["events"]:
        b.apply(e)
    return b
