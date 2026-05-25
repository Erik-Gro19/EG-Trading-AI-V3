# app/views/bot_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QMessageBox
import asyncio

class BotControlPanel(QFrame):
    def __init__(self, autopilot):
        super().__init__()
        self.autopilot = autopilot
        self.setObjectName("Card")
        layout = QVBoxLayout(self)

        self.status = QLabel("<b>Status:</b> <font color='red'>Stopped</font>")
        self.start_btn = QPushButton("START BOT")
        self.stop_btn = QPushButton("STOP BOT")
        self.stop_btn.setEnabled(False)

        layout.addWidget(QLabel("<b>BOT CONTROL</b>"))
        layout.addWidget(self.status)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.start_btn.clicked.connect(self.start_bot)
        self.stop_btn.clicked.connect(self.stop_bot)

        self.running_task = None

    def start_bot(self):
        if self.running_task is not None and not self.running_task.done():
            QMessageBox.warning(self, "Already Running", "Bot is already running!")
            return
        self.status.setText("<b>Status:</b> <font color='green'>Running</font>")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.autopilot.running = True
        self.running_task = asyncio.create_task(self.autopilot.run(self.autopilot.candle_provider, poll_interval=10))

    def stop_bot(self):
        if self.running_task and not self.running_task.done():
            self.autopilot.stop()
            self.running_task.cancel()
        self.status.setText("<b>Status:</b> <font color='red'>Stopped</font>")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
