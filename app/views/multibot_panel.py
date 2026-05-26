# app/views/multibot_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox
from engine.bot.autopilot import AutoPilotBot
from engine.ai.engine import AIEngine
from engine.risk.manager import RiskManager
from engine.performance.logger import TradeLogger

class MultiBotPanel(QFrame):
    def __init__(self, symbols, ai_engine, risk_mgr, logger, candle_service):
        super().__init__()
        self.setObjectName("Card")
        self.bots = {}
        self.ai_engine = ai_engine
        self.risk_mgr = risk_mgr
        self.logger = logger
        self.candle_service = candle_service

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Multi-Bot Controller</b>"))

        self.symbol_boxes = []
        self.status_labels = []

        for i, symbol in enumerate(symbols):
            bot_row = QHBoxLayout()
            bot_row.addWidget(QLabel(f"Bot {i+1}: "))

            symbol_box = QComboBox()
            symbol_box.addItems(symbols)
            symbol_box.setCurrentText(symbol)
            bot_row.addWidget(symbol_box)
            self.symbol_boxes.append(symbol_box)

            cooldown = QSpinBox()
            cooldown.setRange(10, 600)
            cooldown.setValue(60)
            bot_row.addWidget(QLabel("Cooldown:"))
            bot_row.addWidget(cooldown)

            status_label = QLabel("Gestoppt")
            self.status_labels.append(status_label)
            bot_row.addWidget(status_label)

            start_btn = QPushButton("Start")
            stop_btn = QPushButton("Stop")
            bot_row.addWidget(start_btn)
            bot_row.addWidget(stop_btn)
            layout.addLayout(bot_row)

            def make_start_stop(idx):
                def start():
                    sym = self.symbol_boxes[idx].currentText()
                    cd = cooldown.value()
                    bot = AutoPilotBot(
                        symbol=sym,
                        ai=self.ai_engine,
                        risk=self.risk_mgr,
                        logger=self.logger,
                        order_func=None,
                        candle_provider=lambda s=sym: self.candle_service.get_candles(s, n=100)
                    )
                    bot.cooldown = cd
                    self.bots[idx] = bot
                    self.status_labels[idx].setText(f"Läuft ({sym})")
                    bot.start()  # muss ggf. async (Task)
                def stop():
                    if idx in self.bots and self.bots[idx]:
                        self.bots[idx].stop()
                        self.status_labels[idx].setText("Gestoppt")
                        self.bots[idx] = None
                return start, stop

            start_f, stop_f = make_start_stop(i)
            start_btn.clicked.connect(start_f)
            stop_btn.clicked.connect(stop_f)
