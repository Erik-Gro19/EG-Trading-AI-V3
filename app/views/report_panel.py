# app/views/report_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from engine.performance.reporter import TradeReporter

class ReportPanel(QFrame):
    def __init__(self, trade_logger):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>PDF-REPORT GENERIEREN</b>"))
        self.reporter = TradeReporter()
        self.trade_logger = trade_logger

        self.btn = QPushButton("PDF erstellen")
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.generate_pdf)

        self.status = QLabel("")
        layout.addWidget(self.status)

    def generate_pdf(self):
        trades = self.trade_logger.get_trades()
        stats = self.reporter.make_stats(trades)
        try:
            path = self.reporter.export_pdf(trades, stats)
            self.status.setText(f"<font color='green'>Report gespeichert: {path}</font>")
        except Exception as e:
            self.status.setText(f"<font color='red'>Fehler: {e}</font>")
