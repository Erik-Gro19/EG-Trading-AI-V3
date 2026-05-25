# app/views/ai_analysis.py

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from engine.ai.engine import AIEngine

class AIAnalysisPanel(QFrame):
    def __init__(self, ai_engine: AIEngine):
        super().__init__()
        self.setObjectName("Card")
        self.ai_engine = ai_engine

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.header = QLabel("<b>AI ANALYSIS</b>")
        self.score = QLabel()
        self.quality = QLabel()
        self.regime = QLabel()
        self.reason = QLabel()
        self.patterns = QLabel()
        self.volatility = QLabel()
        self.liquidity = QLabel()
        self.probability = QLabel()

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.score)
        self.layout.addWidget(self.quality)
        self.layout.addWidget(self.regime)
        self.layout.addWidget(self.reason)
        self.layout.addWidget(self.patterns)
        self.layout.addWidget(self.volatility)
        self.layout.addWidget(self.liquidity)
        self.layout.addWidget(self.probability)

        self.update_panel()

    def update_panel(self, latest=None):
        # typically 'latest' would be injected by your main loop, 
        # but let's show a demo for now

        if latest is None:
            latest = self.ai_engine.analyze_market([])

        self.score.setText(f"AI Confidence Score: <b style='color:#FFD700'>{latest['score']}</b> / 100")
        self.quality.setText(f"Trade Quality: <b>{latest['quality']}</b>")
        self.regime.setText(f"Market Regime: <b>{latest['regime']}</b>")
        self.reason.setText(f"Reasoning: <i>{latest['reason']}</i>")
        self.patterns.setText(f"Patterns: {', '.join(latest['patterns'])}")
        self.volatility.setText(f"Volatility: {latest['volatility']}")
        self.liquidity.setText(f"Liquidity: {latest['liquidity']}")
        self.probability.setText(f"Trade Probability: {int(100*latest['probability'])}%")

