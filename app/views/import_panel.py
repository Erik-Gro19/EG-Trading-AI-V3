# app/views/import_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QMessageBox
from engine.performance.importer import TradeImporter

class ImportPanel(QFrame):
    def __init__(self, trade_logger):
        super().__init__()
        self.setObjectName("Card")
        self.trade_logger = trade_logger
        self.importer = TradeImporter()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Trades importieren (CSV/XLSX/MT5)</b>"))

        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV (Standard)", "Excel (XLSX)", "MT5 (CSV)"])
        layout.addWidget(self.format_combo)

        self.browse_btn = QPushButton("Datei wählen & importieren")
        layout.addWidget(self.browse_btn)
        self.browse_btn.clicked.connect(self.browse_and_import)

        self.status = QLabel("")
        layout.addWidget(self.status)

    def browse_and_import(self):
        fmt = self.format_combo.currentText()
        if "Excel" in fmt:
            f, _ = QFileDialog.getOpenFileName(self, "Excel-File auswählen", "", "Excel (*.xlsx)")
        else:
            f, _ = QFileDialog.getOpenFileName(self, "CSV-Datei auswählen", "", "CSV-Dateien (*.csv *.txt)")
        if not f:
            return
        try:
            if fmt == "CSV (Standard)":
                trades = self.importer.import_csv(f)
            elif fmt == "Excel (XLSX)":
                trades = self.importer.import_xlsx(f)
            elif fmt == "MT5 (CSV)":
                trades = self.importer.import_mt5_csv(f)
            else:
                self.status.setText("Unbekanntes Format.")
                return
            for t in trades:
                self.trade_logger.add_trade(t)
            self.status.setText(f"<font color='green'>Erfolg: {len(trades)} Trades importiert.</font>")
            QMessageBox.information(self, "Import abgeschlossen", f"Importiert: {len(trades)} Trades.")
        except Exception as e:
            self.status.setText(f"<font color='red'>Fehler: {e}</font>")
            QMessageBox.critical(self, "Fehler", str(e))
