# engine/risk/manager.py

from typing import Dict

class RiskManager:
    def __init__(self, config=None):
        self.max_risk_per_trade = 0.01    # 1%
        self.daily_loss_limit = 0.03      # 3%
        self.max_consecutive_losses = 3
        self.consecutive_losses = 0
        self.daily_loss = 0.0
        self.trading_enabled = True
        self.last_equity = None
        self.open_trades = []
        self.kill_switch_triggered = False

    def reset_daily(self):
        self.daily_loss = 0.0
        self.consecutive_losses = 0
        self.trading_enabled = True
        self.kill_switch_triggered = False

    def register_trade_result(self, pnl: float):
        self.daily_loss += min(0, pnl)       # Only negative PnL
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
        if self.daily_loss <= -self.daily_loss_limit or self.consecutive_losses >= self.max_consecutive_losses:
            self.trading_enabled = False
            self.kill_switch_triggered = True

    def check_trade_allowed(self, risk_size: float, volatility: float, spread: float) -> Dict:
        result = {
            "allowed": True,
            "reason": "OK"
        }
        if not self.trading_enabled:
            result["allowed"] = False
            result["reason"] = "Trading disabled by risk engine"
            return result
        if risk_size > self.max_risk_per_trade:
            result["allowed"] = False
            result["reason"] = "Risk per trade exceeds max risk"
            return result
        if self.daily_loss <= -self.daily_loss_limit:
            result["allowed"] = False
            result["reason"] = "Daily loss limit reached"
            return result
        if self.consecutive_losses >= self.max_consecutive_losses:
            result["allowed"] = False
            result["reason"] = "Max consecutive losses hit"
            return result
        if spread > 50:  # Example: 50 pips/points
            result["allowed"] = False
            result["reason"] = "Spread too high"
            return result
        if volatility > 2:  # Example: ATR or custom metric
            result["allowed"] = False
            result["reason"] = "Volatility too high"
            return result
        return result

    def emergency_stop(self):
        self.trading_enabled = False
        self.kill_switch_triggered = True

    def status_summary(self):
        return {
            "trading_enabled": self.trading_enabled,
            "daily_loss": self.daily_loss,
            "consecutive_losses": self.consecutive_losses,
            "kill_switch": self.kill_switch_triggered,
            "max_risk_per_trade": self.max_risk_per_trade,
            "daily_loss_limit": self.daily_loss_limit
        }
