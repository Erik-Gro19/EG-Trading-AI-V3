# app/views/risk_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from engine.risk.manager import RiskManager

class RiskPanel(QFrame):
    def __init__(self, risk_mgr: RiskManager):
        super().__init__()
        self.setObjectName("Card")
        self.risk_mgr = risk_mgr

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.status_label = QLabel("")
        self.loss_label = QLabel("")
        self.cons_loss_label = QLabel("")
        self.kill_switch_label = QLabel("")
        self.emergency_btn = QPushButton("EMERGENCY STOP")
        self.emergency_btn.clicked.connect(self.on_emergency)

        self.layout.addWidget(QLabel("<b>RISK STATUS</b>"))
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(QLabel("<b>Daily Loss</b>"))
        self.layout.addWidget(self.loss_label)
        self.layout.addWidget(QLabel("<b>Consecutive Losses</b>"))
        self.layout.addWidget(self.cons_loss_label)
        self.layout.addWidget(QLabel("<b>Kill Switch</b>"))
        self.layout.addWidget(self.kill_switch_label)
        self.layout.addWidget(self.emergency_btn)

        # Initial display
        self.update_panel()

    def update_panel(self):
        s = self.risk_mgr.status_summary()
        self.status_label.setText(f"Trading enabled: <b>{s['trading_enabled']}</b>")
        self.loss_label.setText(f"{s['daily_loss']:.2%} / max {s['daily_loss_limit']:.2%}")
        self.cons_loss_label.setText(f"{s['consecutive_losses']} / max {self.risk_mgr.max_consecutive_losses}")
        k = '<font color="red"><b>ACTIVE</b></font>' if s["kill_switch"] else '<font color="green"><b>OFF</b></font>'
        self.kill_switch_label.setText(k)

    def on_emergency(self):
        self.risk_mgr.emergency_stop()
        self.update_panel()
