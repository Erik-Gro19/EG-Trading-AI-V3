# app/views/stats_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from engine.performance.reporter import TradeReporter

class StatsPanel(QFrame):
    def __init__(self, trade_logger):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(QLabel("<b>Statistische Kennzahlen</b>"))

        self.labels = {
            "Anzahl Trades": QLabel(),
            "Gesamtgewinn (PnL)": QLabel(),
            "Winrate": QLabel(),
            "Max Drawdown": QLabel(),
            "Erwartungswert": QLabel()
        }
        for lbl in self.labels.values():
            layout.addWidget(lbl)

        self.reporter = TradeReporter()
        self.trade_logger = trade_logger

        self.refresh_stats()

    def refresh_stats(self):
        trades = self.trade_logger.get_trades()
        stats = self.reporter.make_stats(trades)
        total_trades = len(trades)
        total_pnl = stats.get("total_pnl", 0)
        winrate = stats.get("winrate", 0)
        drawdown = stats.get("drawdown", 0)
        expectancy = stats.get("expectancy", 0)

        self.labels["Anzahl Trades"].setText(f"Anzahl Trades: {total_trades}")
        self.labels["Gesamtgewinn (PnL)"].setText(f"Gesamtgewinn: {total_pnl:.2f}")
        self.labels["Winrate"].setText(f"Winrate: {winrate:.2f} %")
        self.labels["Max Drawdown"].setText(f"Max Drawdown: {drawdown:.2f}")
        self.labels["Erwartungswert"].setText(f"Erwartungswert: {expectancy:.2f}")

    def update_panel(self):
        self.refresh_stats()
