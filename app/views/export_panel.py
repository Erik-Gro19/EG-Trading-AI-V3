# app/views/export_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from engine.performance.exporter import TradeExporter

class ExportPanel(QFrame):
    def __init__(self, trade_logger):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>TRADES EXPORTIEREN</b>"))
        self.exporter = TradeExporter()

        self.btn_csv = QPushButton("Als CSV exportieren")
        self.btn_xlsx = QPushButton("Als XLSX exportieren")
        layout.addWidget(self.btn_csv)
        layout.addWidget(self.btn_xlsx)
        self.status = QLabel("")
        layout.addWidget(self.status)

        self.btn_csv.clicked.connect(self.export_csv)
        self.btn_xlsx.clicked.connect(self.export_xlsx)

        self.trade_logger = trade_logger

    def export_csv(self):
        try:
            path = self.exporter.export_csv(self.trade_logger.get_trades())
            self.status.setText(f"<font color='green'>Exportiert: {path}</font>")
        except Exception as e:
            self.status.setText(f"<font color='red'>Fehler: {e}</font>")

    def export_xlsx(self):
        try:
            path = self.exporter.export_xlsx(self.trade_logger.get_trades())
            self.status.setText(f"<font color='green'>Exportiert: {path}</font>")
        except Exception as e:
            self.status.setText(f"<font color='red'>Fehler: {e}</font>")
