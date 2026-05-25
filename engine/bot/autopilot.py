# engine/bot/autopilot.py

import asyncio
import time
from engine.ai.engine import AIEngine
from engine.risk.manager import RiskManager
from engine.performance.logger import TradeLogger

class AutoPilotBot:
    def __init__(self, symbol, ai: AIEngine, risk: RiskManager, logger: TradeLogger, order_func=None, candle_provider=None):
        self.symbol = symbol
        self.ai = ai
        self.risk = risk
        self.logger = logger
        self.order_func = order_func  # assign mt5 send_order, or mock
        self.candle_provider = candle_provider
        self.running = False
        self.last_trade_time = 0
        self.cooldown = 60  # seconds between trades

    async def run(self, candle_provider, poll_interval=5):
        self.running = True
        while self.running:
            candles = await candle_provider(self.symbol)
            signal = self.ai.analyze_market(candles)
            take_trade = signal['score'] >= 80 and signal['regime'] == "Trend"
            risk_params = self.risk.check_trade_allowed(
                risk_size=0.01,   # 1% - in a real bot, dynamic
                volatility=1.0,   # placeholder
                spread=10         # placeholder
            )
            if take_trade and risk_params['allowed']:
                now = int(time.time())
                if now - self.last_trade_time > self.cooldown:
                    side = "buy" if "bullish" in signal['reason'].lower() else "sell"
                    order_resp = None
                    if self.order_func:
                        try:
                            order_resp = self.order_func(symbol=self.symbol, lot=0.01, action=side)
                        except Exception as e:
                            order_resp = {"error": str(e)}
                    else:
                        order_resp = {"sim": True, "side": side}
                    trade = {
                        "symbol": self.symbol,
                        "side": side.upper(),
                        "qty": 0.01,
                        "entry": "auto",
                        "exit": "",
                        "pnl": 100 if side == "buy" else -50,
                        "timestamp_open": now,
                        "timestamp_close": now + 10,
                        "info": order_resp
                    }
                    self.logger.log_trade(trade)
                    self.risk.register_trade_result(trade['pnl'])
                    self.last_trade_time = now
            await asyncio.sleep(poll_interval)

    def stop(self):
        self.running = False
