# app/widgets/dashboard_cards.py
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel

class DashboardSummaryCards(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")
        layout = QHBoxLayout(self)
        layout.setSpacing(24)
        # Balance, PnL, Drawdown, Winrate, AI Score, etc. — minimal, modern
        stat_labels = [
            ("Balance", "$ 0"),
            ("Daily PnL", "+0%"),
            ("Winrate", "0%"),
            ("Active Trades", "0"),
            ("AI Score", "N/A"),
            ("Drawdown", "0%"),
            ("Latency", "N/A"),
            ("Spread", "-"),
        ]
        for name, value in stat_labels:
            stat = QLabel(f"<b style='font-size:22px'>{value}</b><br><span style='font-size:14px; color:#888'>{name}</span>")
            stat.setStyleSheet("padding: 8px 16px;")
            layout.addWidget(stat)
        self.setLayout(layout)
