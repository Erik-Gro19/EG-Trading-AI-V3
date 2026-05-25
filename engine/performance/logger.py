# engine/performance/logger.py

from typing import List, Dict

class TradeLogger:
    def __init__(self):
        self.trades: List[Dict] = []

    def log_trade(self, trade: Dict):
        """
        trade must include keys:
            symbol, side, qty, entry, exit, pnl, timestamp_open, timestamp_close
        """
        self.trades.append(trade)

    def get_trade_history(self) -> List[Dict]:
        return self.trades

    def get_equity_curve(self, start_balance=10000.0) -> List[float]:
        equity = start_balance
        curve = []
        for t in self.trades:
            equity += t.get("pnl", 0)
            curve.append(equity)
        return curve

    def get_basic_stats(self):
        wins = sum(1 for t in self.trades if t.get("pnl", 0) > 0)
        losses = sum(1 for t in self.trades if t.get("pnl", 0) <= 0)
        total = len(self.trades)
        winrate = wins / total * 100 if total > 0 else 0
        profit = sum(t.get("pnl", 0) for t in self.trades)
        avg_win = sum(t.get("pnl", 0) for t in self.trades if t.get("pnl", 0) > 0) / wins if wins else 0
        avg_loss = sum(t.get("pnl", 0) for t in self.trades if t.get("pnl", 0) <= 0) / losses if losses else 0
        return {"winrate": winrate, "profit": profit, "avg_win": avg_win, "avg_loss": avg_loss}
