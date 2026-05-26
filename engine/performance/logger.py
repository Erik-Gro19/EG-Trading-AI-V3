# engine/performance/logger.py

from engine.utils.persistence import PersistenceManager
import pandas as pd

class TradeLogger:
    def __init__(self):
        self.pers = PersistenceManager()
        self.trades = self.pers.load_json("trades.json", default=[])

    def log_trade(self, trade):
        self.trades.append(trade)
        self.pers.save_json(self.trades, "trades.json")

    def get_trades(self):
        return self.trades

    def as_dataframe(self):
        # DataFrame für weitere Auswertungen (Winrate, etc.)
        if not self.trades:
            return pd.DataFrame()
        return pd.DataFrame(self.trades)

    def total_pnl(self):
        df = self.as_dataframe()
        if df.empty or 'pnl' not in df:
            return 0
        return df['pnl'].sum()

    def win_loss_count(self):
        df = self.as_dataframe()
        if df.empty or 'pnl' not in df:
            return 0, 0
        wins = df[df['pnl'] > 0]
        losses = df[df['pnl'] <= 0]
        return len(wins), len(losses)

    def win_rate(self):
        wins, losses = self.win_loss_count()
        total = wins + losses
        return (wins / total) * 100 if total > 0 else 0

    def max_drawdown(self):
        df = self.as_dataframe()
        if df.empty or 'pnl' not in df:
            return 0
        eq_curve = df['pnl'].cumsum()
        peak = eq_curve.cummax()
        drawdown = (eq_curve - peak).min()
        return abs(drawdown)

    def clear(self):
        self.trades = []
        self.pers.save_json(self.trades, "trades.json")
