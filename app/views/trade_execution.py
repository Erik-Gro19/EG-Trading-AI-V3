# app/views/trade_execution.py

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QMessageBox, QDoubleSpinBox
)
from data.feeds.mt5 import MT5Connector
import config.mt5_settings as mt5_cfg

class TradeExecutionPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")

        # MT5 initialisieren & connecten
        self.mt5 = MT5Connector(
            login=mt5_cfg.MT5_LOGIN,
            password=mt5_cfg.MT5_PASSWORD,
            server=mt5_cfg.MT5_SERVER,
            path=mt5_cfg.MT5_PATH
        )
        try:
            self.mt5.connect()
        except Exception as e:
            QMessageBox.critical(self, "MT5 Connection Error", str(e))

        layout = QVBoxLayout()
        header = QLabel("<b>MANUELLES ORDERPANEL</b>")
        layout.addWidget(header)

        form = QHBoxLayout()

        self.symbol_box = QComboBox()
        self.symbol_box.addItems(self.mt5.get_symbols()[:10] or ["BTCUSD", "XAUUSD"])
        form.addWidget(QLabel("Symbol:"))
        form.addWidget(self.symbol_box)

        self.side_box = QComboBox()
        self.side_box.addItems(["BUY", "SELL"])
        form.addWidget(QLabel("Richtung:"))
        form.addWidget(self.side_box)

        form.addWidget(QLabel("Lot:"))
        self.lot_input = QDoubleSpinBox()
        self.lot_input.setValue(0.01)
        self.lot_input.setDecimals(3)
        self.lot_input.setSingleStep(0.01)
        form.addWidget(self.lot_input)

        form.addWidget(QLabel("SL:"))
        self.sl_input = QLineEdit()
        self.sl_input.setPlaceholderText("optional")
        form.addWidget(self.sl_input)

        form.addWidget(QLabel("TP:"))
        self.tp_input = QLineEdit()
        self.tp_input.setPlaceholderText("optional")
        form.addWidget(self.tp_input)

        layout.addLayout(form)

        order_btn = QPushButton("Order senden")
        order_btn.clicked.connect(self.submit_order)
        layout.addWidget(order_btn)

        self.resp_label = QLabel("")
        layout.addWidget(self.resp_label)

        self.setLayout(layout)

    def submit_order(self):
        symbol = self.symbol_box.currentText()
        side = "buy" if self.side_box.currentText() == "BUY" else "sell"
        lot = float(self.lot_input.value())
        sl = float(self.sl_input.text()) if self.sl_input.text() else None
        tp = float(self.tp_input.text()) if self.tp_input.text() else None

        try:
            result = self.mt5.send_order(symbol, lot, action=side, sl=sl, tp=tp)
            if result.get("retcode", None) == 10009:   # TRADE_RETCODE_DONE
                self.resp_label.setText(f"<font color='lime'>Order platziert, Ticket {result['order']}</font>")
            else:
                self.resp_label.setText(f"<font color='red'>Order Fehler ({result.get('retcode','?')})</font>")
        except Exception as e:
            self.resp_label.setText(f"<font color='red'>ERROR: {e}</font>")
