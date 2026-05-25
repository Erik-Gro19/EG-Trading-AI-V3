# app/widgets/lux_chart_widget.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
import plotly.io as pio
from data.indicators.overlays import ema, vwap, session_high_low

class LuxCandlestickChart(QWidget):
    def __init__(self, symbol="BTCUSD", timeframe="1m"):
        super().__init__()
        self.symbol = symbol
        self.timeframe = timeframe
        self.candles = []
        self.overlays_enabled = {
            "EMA20": True,
            "EMA50": True,
            "VWAP": True,
            "SESSION": True,
        }
        self.view = QWebEngineView()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

    def add_candle(self, candle: dict):
        self.candles.append(candle)
        if len(self.candles) > 300:
            self.candles.pop(0)
        self.update_chart()

    def update_chart(self):
        if not self.candles:
            return

        times = [c['timestamp'] for c in self.candles]
        opens = [c['open'] for c in self.candles]
        highs = [c['high'] for c in self.candles]
        lows = [c['low'] for c in self.candles]
        closes = [c['close'] for c in self.candles]
        volumes = [c['volume'] for c in self.candles]

        fig = go.Figure()

        # Candle
        fig.add_trace(go.Candlestick(
            x=times, open=opens, high=highs, low=lows, close=closes,
            name="Candles", increasing_line_color="#EFD469", decreasing_line_color="#444"
        ))

        # EMA20, EMA50
        if self.overlays_enabled["EMA20"]:
            ema20 = ema(closes, 20)
            fig.add_trace(go.Scatter(
                x=times, y=ema20, mode='lines',
                line=dict(color='#00CCFF', width=2, dash='solid'),
                name="EMA20", opacity=0.8))
        if self.overlays_enabled["EMA50"]:
            ema50 = ema(closes, 50)
            fig.add_trace(go.Scatter(
                x=times, y=ema50, mode='lines',
                line=dict(color='#FF8888', width=2, dash='dot'),
                name="EMA50", opacity=0.8))

        # VWAP
        if self.overlays_enabled["VWAP"]:
            vwap_ = vwap(self.candles)
            fig.add_trace(go.Scatter(
                x=times, y=vwap_, mode='lines',
                line=dict(color='#FFD700', width=1, dash='dash'),
                name="VWAP", opacity=0.7))
        
        # Session High/Low
        if self.overlays_enabled["SESSION"]:
            session = session_high_low(self.candles)
            fig.add_trace(go.Scatter(
                x=times, y=session["session_high"], mode='lines',
                line=dict(color='#33FF99', width=1, dash='dot'),
                name="Session High", opacity=0.5, showlegend=True))
            fig.add_trace(go.Scatter(
                x=times, y=session["session_low"], mode='lines',
                line=dict(color='#3399FF', width=1, dash='dot'),
                name="Session Low", opacity=0.5, showlegend=True))

        fig.update_layout(
            template='plotly_dark',
            margin=dict(l=0, r=0, t=20, b=0),
            height=380,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            legend=dict(bgcolor='#181818', borderwidth=0, bordercolor="#333")
        )
        html = pio.to_html(fig, full_html=False, config={"displayModeBar": False})
        self.view.setHtml(html)
