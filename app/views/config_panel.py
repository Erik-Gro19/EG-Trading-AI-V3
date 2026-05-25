# app/views/config_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QCheckBox, QComboBox, QLabel, QDoubleSpinBox, QPushButton
from engine.utils.session_config import SessionConfig

class ConfigPanel(QFrame):
    def __init__(self, session_config: SessionConfig):
        super().__init__()
        self.conf = session_config
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>SESSION CONFIGURATION</b>"))

        self.live_box = QCheckBox("Live Trading Mode")
        self.live_box.setChecked(self.conf.live_mode)
        layout.addWidget(self.live_box)

        layout.addWidget(QLabel("Default Symbol:"))
        self.symbol_box = QComboBox()
        self.symbol_box.addItems(self.conf.available_symbols)
        self.symbol_box.setCurrentText(self.conf.default_symbol)
        layout.addWidget(self.symbol_box)

        layout.addWidget(QLabel("Default Lot Size:"))
        self.lot_spin = QDoubleSpinBox()
        self.lot_spin.setValue(self.conf.default_lot)
        self.lot_spin.setSingleStep(0.01)
        self.lot_spin.setDecimals(3)
        self.lot_spin.setMinimum(0.001)
        layout.addWidget(self.lot_spin)

        layout.addWidget(QLabel("Risk per Trade (%):"))
        self.risk_spin = QDoubleSpinBox()
        self.risk_spin.setValue(self.conf.default_risk * 100)
        self.risk_spin.setMinimum(0.1)
        self.risk_spin.setMaximum(20.0)
        self.risk_spin.setSingleStep(0.1)
        layout.addWidget(self.risk_spin)

        layout.addWidget(QLabel("Bot Cooldown (sec):"))
        self.cooldown_spin = QDoubleSpinBox()
        self.cooldown_spin.setValue(self.conf.bot_cooldown)
        self.cooldown_spin.setMinimum(5)
        self.cooldown_spin.setMaximum(600)
        self.cooldown_spin.setSingleStep(1)
        layout.addWidget(self.cooldown_spin)

        self.save_btn = QPushButton("Apply & Save")
        layout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.save_config)

        self.emergency_btn = QPushButton("EMERGENCY STOP")
        self.emergency_btn.setStyleSheet("background: #ff4444; color: white;")
        layout.addWidget(self.emergency_btn)
        self.emergency_btn.clicked.connect(self.emergency_stop)

    def save_config(self):
        self.conf.live_mode = self.live_box.isChecked()
        self.conf.default_symbol = self.symbol_box.currentText()
        self.conf.default_lot = self.lot_spin.value()
        self.conf.default_risk = self.risk_spin.value() / 100.0
        self.conf.bot_cooldown = int(self.cooldown_spin.value())
        self.conf.notify_all()  # Notify subscribers whenever the config changes

    def emergency_stop(self):
        from datetime import datetime
        self.conf.last_emergency = datetime.utcnow().isoformat()
        self.live_box.setChecked(False)
        self.conf.live_mode = False
        self.conf.notify_all()
