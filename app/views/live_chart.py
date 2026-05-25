# app/views/live_chart.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from app.widgets.lux_chart_widget import LuxCandlestickChart
from data.streamer import DataStreamer
from data.feeds.binance import BinanceFeed
from data.feeds.forexcom import ForexComFeed
from data.normalizer import normalize_candle
import asyncio

class LiveChartPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Chart widgets for both instruments
        self.btc_chart = LuxCandlestickChart(symbol="BTCUSD", timeframe="1m")
        self.xau_chart = LuxCandlestickChart(symbol="XAUUSD", timeframe="1m")

        self.btc_label = QLabel("BTC/USD Chart (1m)")
        self.xau_label = QLabel("XAU/USD Chart (1m)")

        layout.addWidget(self.btc_label)
        layout.addWidget(self.btc_chart)
        layout.addWidget(self.xau_label)
        layout.addWidget(self.xau_chart)

        # Create data streamer and register callback
        self.data_streamer = DataStreamer()
        self.data_streamer.register_callback(self.on_new_candle)
        asyncio.create_task(self.data_streamer.start())

        # Load recent history at startup (does not block UI)
        asyncio.create_task(self.load_history())

    async def load_history(self):
        # BTC/USD history
        btc_feed = BinanceFeed("BTCUSDT", "1m")
        btc_history = await btc_feed.fetch_historical(limit=120)
        for c in btc_history:
            candle = normalize_candle(c, "binance")
            self.btc_chart.add_candle(candle)

        # XAU/USD history
        xau_feed = ForexComFeed("XAU/USD", "1min")
        xau_history = await xau_feed.fetch_historical(limit=120)
        for c in reversed(xau_history): # TwelveData returns newest first.
            candle = normalize_candle(c, "forexcom")
            self.xau_chart.add_candle(candle)

    def on_new_candle(self, symbol: str, candle: dict):
        if symbol == "BTCUSD":
            self.btc_chart.add_candle(candle)
        elif symbol == "XAUUSD":
            self.xau_chart.add_candle(candle)
