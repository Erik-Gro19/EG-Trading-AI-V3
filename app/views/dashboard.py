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
from app.widgets.dashboard_cards import DashboardSummaryCards
from app.theme.styles import apply_luxury_theme

from engine.risk.manager import RiskManager
from engine.performance.logger import TradeLogger
from engine.ai.engine import AIEngine
from engine.bot.autopilot import AutoPilotBot
from engine.bot.candle_service import CandleService
from engine.utils.notifications import NotificationBus
from engine.utils.session_config import SessionConfig

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

        # Instantiate shared state/services
        self.session_config = SessionConfig()
        self.risk_mgr = RiskManager()
        self.trade_logger = TradeLogger()
        self.ai_engine = AIEngine()
        self.candle_service = CandleService()
        self.notification_bus = NotificationBus()

        # ----- Data Streamer -----
        self.data_streamer = DataStreamer()
        self.data_streamer.register_callback(self.on_new_candle)

        # ----- Panels and main layout -----
        central = QWidget(self)
        vbox = QVBoxLayout(central)
        vbox.setSpacing(16)
        vbox.setContentsMargins(24, 18, 24, 18)

        # Dashboard summary (cards)
        summary_cards = DashboardSummaryCards()
        vbox.addWidget(summary_cards)

        # Splitter for main content (charts left, panels right)
        hsplitter = QSplitter()

        # ----- Left column -----
        from PyQt6.QtWidgets import QVBoxLayout, QWidget
        left_col = QVBoxLayout()
        self.live_chart_panel = LiveChartPanel()
        self.performance_panel = PerformancePanel(self.trade_logger)
        left_col.addWidget(self.live_chart_panel)
        left_col.addWidget(self.performance_panel)

        left_widget = QWidget()
        left_widget.setLayout(left_col)

        # ----- Right column -----
        right_col = QVBoxLayout()
        right_col.setSpacing(18)

        # Session Config Panel (top of right col)
        self.config_panel = ConfigPanel(self.session_config)
        right_col.addWidget(self.config_panel)

        self.risk_panel = RiskPanel(self.risk_mgr)
        self.ai_panel = AIAnalysisPanel(self.ai_engine)
        right_col.addWidget(self.risk_panel)
        right_col.addWidget(self.ai_panel)

        # Bot autopilot (with candle provider)
        async def live_candle_provider(symbol):
            return self.candle_service.get_candles(symbol, n=100)

        self.autopilot = AutoPilotBot(
            symbol=self.session_config.default_symbol,
            ai=self.ai_engine,
            risk=self.risk_mgr,
            logger=self.trade_logger,
            order_func=None,  # Use MT5 when live, None for sim
            candle_provider=live_candle_provider
        )
        self.bot_panel = BotControlPanel(self.autopilot)
        right_col.addWidget(self.bot_panel)

        # Account/Trade Monitor
        self.account_monitor_panel = AccountMonitorPanel()
        right_col.addWidget(self.account_monitor_panel)

        # Notification/Event Log Panel
        self.notification_panel = NotificationPanel(self.notification_bus)
        right_col.addWidget(self.notification_panel)

        right_widget = QWidget()
        right_widget.setLayout(right_col)

        # Add to splitter
        hsplitter.addWidget(left_widget)
        hsplitter.addWidget(right_widget)
        hsplitter.setSizes([1200, 700])

        vbox.addWidget(hsplitter)
        central.setLayout(vbox)
        self.setCentralWidget(central)

        # Subscribe to session config changes
        self.session_config.subscribe(self.on_config_change)

        # -- AI Panel live refresh --
        def refresh_ai_panel():
            latest = self.ai_engine.analyze_market(self.candle_service.get_candles(self.session_config.default_symbol, 100))
            self.ai_panel.update_panel(latest)
        self.ai_timer = QTimer()
        self.ai_timer.timeout.connect(refresh_ai_panel)
        self.ai_timer.start(3500)

        # -- Start Data Streamer in background --
        asyncio.create_task(self.data_streamer.start())

    def on_new_candle(self, symbol, candle):
        # Store in central history for bot, charts, AI, etc.
        self.candle_service.add_candle(symbol, candle)
        # Optionally, update GUI panels if needed:
        # self.live_chart_panel.on_new_candle(symbol, candle)

    def on_config_change(self, conf):
        # Updates all relevant modules with new config LIVE (no restart needed!)
        self.autopilot.symbol = conf.default_symbol
        self.autopilot.cooldown = conf.bot_cooldown
        # Add further reactivity here as you grow (e.g., push to other panels)
        self.notification_bus.notify(
            f"Session config changed: symbol={conf.default_symbol}, live={conf.live_mode}"
        )
        # Optionally update the AI panel instantly
        self.ai_panel.update_panel(self.ai_engine.analyze_market(
            self.candle_service.get_candles(conf.default_symbol, 100)
        ))
