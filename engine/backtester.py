# engine/backtester.py

import asyncio
import pandas as pd

class BacktestResult:
    def __init__(self):
        self.trades = []
        self.balance_curve = []
        self.pnl_total = 0.0
        self.win_count = 0
        self.loss_count = 0
        self.max_drawdown = 0.0

    def summarize(self):
        trades = pd.DataFrame(self.trades)
        if len(trades) == 0:
            return "Keine Trades ausgeführt."
        wins = trades[trades['pnl'] > 0]
        losses = trades[trades['pnl'] <= 0]
        self.pnl_total = trades['pnl'].sum()
        self.win_count = len(wins)
        self.loss_count = len(losses)
        self.max_drawdown = self._max_drawdown(trades['cum_balance'])
        report = (f"<b>Backtest: {len(trades)} Trades</b><br>"
                  f"Gewinn-Trades: {self.win_count} &nbsp;&nbsp; "
                  f"Verlust-Trades: {self.loss_count}<br>"
                  f"Gesamtergebnis: <b>{self.pnl_total:.2f}</b><br>"
                  f"Max Drawdown: <b>{self.max_drawdown:.2f}</b><br>")
        return report

    @staticmethod
    def _max_drawdown(balance_series):
        peak = balance_series.cummax()
        dd = (balance_series - peak).min()
        return abs(dd)

class Backtester:
    def __init__(self, candles, bot_factory, risk_mgr, ai_engine, starting_balance=10000):
        self.candles = candles  # Liste von Kerzen-Dicts
        self.bot_factory = bot_factory  # Funktion, die einen Bot mit Logger zurückgibt
        self.risk_mgr = risk_mgr
        self.ai_engine = ai_engine
        self.starting_balance = starting_balance

    async def run(self):
        result = BacktestResult()
        balance = self.starting_balance
        balances = []
        fake_logger = FakeLogger()

        # Bot-Bau: neuer Bot für Backtest
        bot = self.bot_factory(logger=fake_logger)

        for idx in range(100, len(self.candles)):
            recent_candles = self.candles[idx-100:idx]
            # Simulierter CandleProvider für Bot
            async def candle_provider(symbol):
                return recent_candles

            # Bot Signal holen
            signal = self.ai_engine.analyze_market(recent_candles)
            take_trade = signal['score'] >= 80 and signal['regime'] == "Trend"
            risk_ok = self.risk_mgr.check_trade_allowed(
                risk_size=0.01, volatility=1.0, spread=10)['allowed']
            if take_trade and risk_ok:
                # trade simulation
                side = "buy" if "bullish" in signal['reason'].lower() else "sell"
                # Simple Modell: +100 Pips Gewinn trade, -50 Verlust für Beispiel
                pnl = 100 if side == "buy" else -50
                trade = {
                    "symbol": "BTCUSD",
                    "side": side.upper(),
                    "qty": 0.01,
                    "entry": recent_candles[-1]['close'],
                    "exit": "",
                    "pnl": pnl,
                    "timestamp_open": recent_candles[-1]['timestamp'],
                    "timestamp_close": recent_candles[-1]['timestamp']+1000,
                    "info": {}
                }
                fake_logger.log_trade(trade)
                balance += pnl
            balances.append(balance)
        # Ergebnisse erfassen
        result.trades = fake_logger.trades
        result.balance_curve = balances
        # Pandas-DataFrame für Drawdown etc.
        pd_curve = pd.Series(balances)
        if len(pd_curve):
            result.max_drawdown = result._max_drawdown(pd_curve)
        return result

class FakeLogger:
    def __init__(self):
        self.trades = []

    def log_trade(self, trade):
        self.trades.append(trade)
