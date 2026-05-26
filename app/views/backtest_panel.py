# app/views/backtest_panel.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QTextEdit
from engine.backtester import Backtester
import asyncio

class BacktestPanel(QFrame):
    def __init__(self, get_candles, bot_factory, risk_mgr, ai_engine):
        super().__init__()
        self.setObjectName("Card")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>BACKTEST</b>"))

        self.start_btn = QPushButton("Backtest starten")
        layout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start_backtest)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        # benötigte Factories/hooks
        self.get_candles = get_candles
        self.bot_factory = bot_factory
        self.risk_mgr = risk_mgr
        self.ai_engine = ai_engine

    def start_backtest(self):
        # Run async
        loop = asyncio.get_event_loop()
        loop.create_task(self._run_backtest())

    async def _run_backtest(self):
        candles = self.get_candles()
        self.result_box.setHtml("Backtest läuft...")
        bt = Backtester(candles, self.bot_factory, self.risk_mgr, self.ai_engine)
        result = await bt.run()
        html = result.summarize()
        self.result_box.setHtml(html)
