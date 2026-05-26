# app/views/dashboard.py

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from app.views.live_chart import LiveChartPanel
from app.views.risk_panel import RiskPanel
from app.views.performance import PerformancePanel
from app.views.ai_analysis import AIAnalysisPanel
from app.views.bot_panel import BotControlPanel
from app.views.account_monitor import AccountMonitorPanel
from app.views.notification_panel import NotificationPanel
from app.views.config_panel import ConfigPanel
from app.views.trade_execution import TradeExecutionPanel
from app.views.backtest_panel import BacktestPanel
from app.views.export_panel import ExportPanel
from app.views.multisymbol_panel import MultiSymbolPanel
from app.views.multibot_panel import MultiBotPanel
from app.widgets.dashboard_cards import DashboardSummaryCards
from app.theme.styles import apply_luxury_theme

from engine.risk.manager import RiskManager
from engine.performance.logger import TradeLogger
from engine.ai.engine import AIEngine
from engine.bot.autopilot import AutoPilotBot
from engine.bot.candle_service import CandleService
from engine.utils.notifications import NotificationBus
from engine.utils.session_config import SessionConfig
from engine.utils.error_report import report_exception

from data.streamer import DataStreamer

from PyQt6.QtCore import QTimer

import asyncio

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Institutional Trading Terminal")
        self.resize(1920, 1080)
        self.setMinimumSize(1600, 900)
        apply_luxury_theme(self)

        self.session_config = SessionConfig()
        self.risk_mgr = RiskManager()
        self.trade_logger = TradeLogger()
        self.ai_engine = AIEngine()
        self.candle_service = CandleService()
        self.notification_bus = NotificationBus()

        self.data_streamer = DataStreamer()
        self.data_streamer.register_callback(self.on_new_candle)

        central = QWidget(self)
        vbox = QVBoxLayout(central)
        vbox.setSpacing(16)
        vbox.setContentsMargins(24, 18, 24, 18)
        summary_cards = DashboardSummaryCards()
        vbox.addWidget(summary_cards)
        hsplitter = QSplitter()

        from PyQt6.QtWidgets import QVBoxLayout, QWidget
        left_col = QVBoxLayout()
        self.live_chart_panel = LiveChartPanel(trade_logger=self.trade_logger)
        self.performance_panel = PerformancePanel(self.trade_logger)
        left_col.addWidget(self.live_chart_panel)
        left_col.addWidget(self.performance_panel)
        left_widget = QWidget()
        left_widget.setLayout(left_col)

        right_col = QVBoxLayout()
        right_col.setSpacing(18)
        self.config_panel = ConfigPanel(self.session_config)
        right_col.addWidget(self.config_panel)

        self.multisymbol_panel = MultiSymbolPanel(self.session_config)
        right_col.addWidget(self.multisymbol_panel)

        # ⭐ MULTIBOT PANEL JETZT AKTIV
        self.multibot_panel = MultiBotPanel(
            symbols=self.session_config.available_symbols,
            ai_engine=self.ai_engine,
            risk_mgr=self.risk_mgr,
            logger=self.trade_logger,
            candle_service=self.candle_service
        )
        right_col.addWidget(self.multibot_panel)

        self.trade_execution_panel = TradeExecutionPanel()
        right_col.addWidget(self.trade_execution_panel)
        self.risk_panel = RiskPanel(self.risk_mgr)
        self.ai_panel = AIAnalysisPanel(self.ai_engine)
        right_col.addWidget(self.risk_panel)
        right_col.addWidget(self.ai_panel)

        async def live_candle_provider(symbol):
            return self.candle_service.get_candles(symbol, n=100)

        self.autopilot = AutoPilotBot(
            symbol=self.session_config.default_symbol,
            ai=self.ai_engine,
            risk=self.risk_mgr,
            logger=self.trade_logger,
            order_func=None,
            candle_provider=live_candle_provider
        )
        self.bot_panel = BotControlPanel(self.autopilot)
        right_col.addWidget(self.bot_panel)
        self.account_monitor_panel = AccountMonitorPanel()
        right_col.addWidget(self.account_monitor_panel)

        def bot_factory(logger):
            return AutoPilotBot(
                symbol=self.session_config.default_symbol,
                ai=self.ai_engine,
                risk=self.risk_mgr,
                logger=logger,
                order_func=None,
                candle_provider=None,
            )

        def get_all_candles():
            return self.candle_service.get_candles(self.session_config.default_symbol, None)

        self.backtest_panel = BacktestPanel(
            get_candles=get_all_candles,
            bot_factory=bot_factory,
            risk_mgr=self.risk_mgr,
            ai_engine=self.ai_engine
        )
        right_col.addWidget(self.backtest_panel)

        self.export_panel = ExportPanel(self.trade_logger)
        right_col.addWidget(self.export_panel)

        self.notification_panel = NotificationPanel(self.notification_bus)
        right_col.addWidget(self.notification_panel)

        right_widget = QWidget()
        right_widget.setLayout(right_col)

        hsplitter.addWidget(left_widget)
        hsplitter.addWidget(right_widget)
        hsplitter.setSizes([1200, 700])

        vbox.addWidget(hsplitter)
        central.setLayout(vbox)
        self.setCentralWidget(central)

        self.session_config.subscribe(self.on_config_change)

        def refresh_ai_panel():
            latest = self.ai_engine.analyze_market(self.candle_service.get_candles(self.session_config.default_symbol, 100))
            self.ai_panel.update_panel(latest)
        self.ai_timer = QTimer()
        self.ai_timer.timeout.connect(refresh_ai_panel)
        self.ai_timer.start(3500)

        def refresh_chart():
            candles = self.candle_service.get_candles(self.session_config.default_symbol, 200)
            self.live_chart_panel.set_candles(candles)
        self.chart_timer = QTimer()
        self.chart_timer.timeout.connect(refresh_chart)
        self.chart_timer.start(3000)

        asyncio.create_task(self.data_streamer.start())

    def on_new_candle(self, symbol, candle):
        try:
            self.candle_service.add_candle(symbol, candle)
            self.live_chart_panel.on_new_candle(symbol, candle)
        except Exception as err:
            report_exception(err, self.notification_bus, context="Chart/Candle")

    def on_config_change(self, conf):
        try:
            self.autopilot.symbol = conf.default_symbol
            self.autopilot.cooldown = conf.bot_cooldown
            self.notification_bus.notify(f"Session config changed: symbol={conf.default_symbol}, live={conf.live_mode}")
            self.ai_panel.update_panel(self.ai_engine.analyze_market(
                self.candle_service.get_candles(conf.default_symbol, 100)
            ))
        except Exception as err:
            report_exception(err, self.notification_bus, context="SessionConfig")
