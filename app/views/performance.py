# app/views/performance.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
import plotly.io as pio
from engine.performance.logger import TradeLogger

class PerformancePanel(QFrame):
    def __init__(self, trade_logger: TradeLogger):
        super().__init__()
        self.setObjectName("Card")
        self.trade_logger = trade_logger

        self.layout = QVBoxLayout(self)
        self.stats_label = QLabel("Performance Stats")
        self.chart = QWebEngineView()
        self.table = QTableWidget()
        self.layout.addWidget(self.stats_label)
        self.layout.addWidget(self.chart)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.refresh_panel()

    def refresh_panel(self):
        # Update stats
        stats = self.trade_logger.get_basic_stats()
        self.stats_label.setText(
            f"<b>Winrate:</b> {stats['winrate']:.1f}% &nbsp;&nbsp; "
            f"<b>PnL:</b> {stats['profit']:.2f} &nbsp;&nbsp; "
            f"<b>Avg Win:</b> {stats['avg_win']:.2f} &nbsp;&nbsp; "
            f"<b>Avg Loss:</b> {stats['avg_loss']:.2f}"
        )
        # Equity curve
        curve = self.trade_logger.get_equity_curve()
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=curve, mode="lines", line=dict(color="#78FAFA", width=2), name="Equity"))
        fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=20, b=0), height=160)
        html = pio.to_html(fig, full_html=False, config={"displayModeBar": False})
        self.chart.setHtml(html)

        # Trade history table
        trades = self.trade_logger.get_trade_history()
        headers = ["Symbol", "Side", "Entry", "Exit", "PnL", "Open Time", "Close Time"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(trades))
        for i, t in enumerate(trades):
            self.table.setItem(i, 0, QTableWidgetItem(str(t.get("symbol", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(str(t.get("side", ""))))
            self.table.setItem(i, 2, QTableWidgetItem(str(t.get("entry", ""))))
            self.table.setItem(i, 3, QTableWidgetItem(str(t.get("exit", ""))))
            self.table.setItem(i, 4, QTableWidgetItem(f"{t.get('pnl', 0):.2f}"))
            self.table.setItem(i, 5, QTableWidgetItem(str(t.get("timestamp_open", ""))))
            self.table.setItem(i, 6, QTableWidgetItem(str(t.get("timestamp_close", ""))))
        self.table.resizeColumnsToContents()
