# app/views/indicator_overlay.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QPushButton, QSpinBox
import numpy as np

class IndicatorOverlayPanel(QFrame):
    def __init__(self, chart_panel):
        super().__init__()
        self.setObjectName("Card")
        self.chart_panel = chart_panel

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Indikator-Overlays</b>"))

        row = QHBoxLayout()
        layout.addLayout(row)

        self.indicator_box = QComboBox()
        self.indicator_box.addItems(["EMA", "SMA"])  # Erweiterbar, z.B. "Bollinger"
        row.addWidget(QLabel("Indikator:"))
        row.addWidget(self.indicator_box)

        self.length_box = QSpinBox()
        self.length_box.setRange(2, 200)
        self.length_box.setValue(20)
        row.addWidget(QLabel("Periode:"))
        row.addWidget(self.length_box)

        self.btn_apply = QPushButton("Overlay anzeigen")
        row.addWidget(self.btn_apply)

        self.btn_apply.clicked.connect(self.apply_overlay)

        self.status = QLabel("")
        layout.addWidget(self.status)

    def apply_overlay(self):
        ind = self.indicator_box.currentText()
        length = self.length_box.value()
        try:
            closes = [c["close"] for c in self.chart_panel.candles]
            if not closes or len(closes) < length:
                self.status.setText("<font color='red'>Nicht genug Daten!</font>")
                return
            if ind == "EMA":
                vals = self.ema(closes, length)
                color = (40, 100, 200)
            elif ind == "SMA":
                vals = self.sma(closes, length)
                color = (200, 150, 30)
            else:
                self.status.setText("<font color='red'>Unbekannter Indikator</font>")
                return
            self.chart_panel.add_overlay(vals, color=color, name=f"{ind}-{length}")
            self.status.setText(f"<font color='green'>Overlay: {ind}({length}) hinzugefügt</font>")
        except Exception as e:
            self.status.setText(f"<font color='red'>Fehler: {e}</font>")

    @staticmethod
    def ema(data, length):
        arr = np.array(data)
        if len(arr) < length:
            return []
        return list(pd.Series(arr).ewm(span=length, adjust=False).mean())

    @staticmethod
    def sma(data, length):
        arr = np.array(data)
        if len(arr) < length:
            return []
        return list(pd.Series(arr).rolling(length).mean())
