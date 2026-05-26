# app/views/live_chart.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from engine.performance.logger import TradeLogger
import pyqtgraph as pg

class LiveChartPanel(QFrame):
    def __init__(self, trade_logger=None):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Live Chart</b>"))

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setBackground('w')
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Chart-Daten
        self.candles = []
        self.trade_logger = trade_logger or TradeLogger()
        self.overlays = []

        # Farben/Stil für Trades
        self.trade_symbol_buy = "t1"  # triangle up
        self.trade_symbol_sell = "t2" # triangle down
        self._entry_color = (0,200,0)
        self._exit_color = (200,0,0)

    def set_candles(self, candles):
        # candles: Liste von Dicts mit 'timestamp', 'open', 'high', 'low', 'close'
        self.candles = candles
        self.redraw()

    def on_new_candle(self, symbol, candle):
        # Nutze für Live-Streaming/Push
        self.candles.append(candle)
        if len(self.candles) > 200:
            self.candles = self.candles[-200:]
        self.redraw()

    def redraw(self):
        self.plot_widget.clear()
        if not self.candles or len(self.candles) < 2:
            return

        x = list(range(len(self.candles)))
        closes = [c["close"] for c in self.candles]
        highs = [c["high"] for c in self.candles]
        lows = [c["low"] for c in self.candles]
        opens = [c["open"] for c in self.candles]

        # Candle-Stabdiagramm (jeder Balken ein Candle)
        for i in range(len(x)):
            color = 'g' if closes[i]>=opens[i] else 'r'
            self.plot_widget.plot([x[i],x[i]], [lows[i],highs[i]], pen=pg.mkPen(color, width=1))
            self.plot_widget.plot([x[i]-0.15, x[i]+0.15], [opens[i], opens[i]], pen=pg.mkPen(color, width=6))
            self.plot_widget.plot([x[i]-0.15, x[i]+0.15], [closes[i], closes[i]], pen=pg.mkPen(color, width=6))

        # Overlay: Indikatoren (EMA/SMA/Bollinger ...), alle aktiven
        for overlay in self.overlays:
            self.plot_widget.addItem(overlay)

        # Overlay: Trades
        self.draw_trades()

    def add_overlay(self, yvals, color=(0,0,255), name="Overlay"):
        from pyqtgraph import PlotDataItem
        if not yvals or len(yvals) != len(self.candles):
            return
        x = list(range(len(self.candles)))
        overlay = PlotDataItem(x, yvals, pen={'color': color, 'width': 2}, name=name)
        self.overlays.append(overlay)
        self.redraw()

    def clear_overlays(self):
        self.overlays = []
        self.redraw()

    def draw_trades(self):
        trades = self.trade_logger.get_trades()
        if not trades or not self.candles:
            return
        candle_times = [c["timestamp"] for c in self.candles]

        for trade in trades:
            try:
                entry_idx = candle_times.index(trade["timestamp_open"])
                exit_idx = candle_times.index(trade["timestamp_close"]) if "timestamp_close" in trade and trade["timestamp_close"] in candle_times else None
                entry_price = trade["entry"]
                exit_price = trade.get("exit", None) or trade.get("entry", None)
                is_buy = trade["side"].upper() == "BUY"
                # Entry
                self._draw_marker(entry_idx, entry_price, "E", color=self._entry_color)
                # Optional: Exit
                if exit_idx is not None and exit_price:
                    self._draw_marker(exit_idx, exit_price, "X", color=self._exit_color)
            except Exception:
                continue

    def _draw_marker(self, x_idx, y_value, txt, color=(0,0,255)):
        scatter = pg.ScatterPlotItem([x_idx], [y_value],
                                     size=16, brush=pg.mkBrush(*color),
                                     symbol='o')
        self.plot_widget.addItem(scatter)
        label = pg.TextItem(txt, color=pg.mkColor(*color))
        label.setPos(x_idx, y_value)
        self.plot_widget.addItem(label)
