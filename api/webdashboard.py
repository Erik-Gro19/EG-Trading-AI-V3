# api/webdashboard.py

from flask import Flask, render_template_string
from engine.utils.accounts_service import AccountsService
from engine.performance.logger import TradeLogger
from engine.performance.reporter import TradeReporter

app = Flask(__name__)
accounts_service = AccountsService("accounts.json")
trade_logger = TradeLogger()
reporter = TradeReporter()

TEMPLATE = """
<html>
<head>
    <title>Trading-Terminal Live-Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin:40px; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #888; padding: 6px 12px; }
        th { background: #EEE; }
        .section { margin-bottom: 24px; }
    </style>
</head>
<body>
<h2>📊 Trading-Terminal Monitoring</h2>
<div class="section">
    <b>Aktive Konten:</b>
    <table>
        <tr><th>Name</th><th>Balance</th><th>Währung</th><th>Statistik</th></tr>
        {% for acc in accounts %}
        <tr>
            <td>{{ acc.name }}</td>
            <td>{{ "%.2f"|format(acc.balance) }}</td>
            <td>{{ acc.currency }}</td>
            <td>{% if acc.stats %}{% for k,v in acc.stats.items() %}{{k}}: {{v}}<br>{% endfor %}{% endif %}</td>
        </tr>
        {% endfor %}
    </table>
</div>
<div class="section">
    <b>Letzte Trades:</b>
    <table>
        <tr>
            <th>Zeit</th><th>Symbol</th><th>Side</th><th>Qty</th><th>Entry</th><th>Exit</th><th>PnL</th>
        </tr>
        {% for t in trades[-12:] %}
        <tr>
            <td>{{ t.timestamp_open }}</td>
            <td>{{ t.symbol }}</td>
            <td>{{ t.side }}</td>
            <td>{{ t.qty }}</td>
            <td>{{ t.entry }}</td>
            <td>{{ t.exit }}</td>
            <td>{{ t.pnl }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
<div class="section">
    <b>Kennzahlen:</b>
    <ul>
        <li>Anzahl Trades: {{ stats.total_trades }}</li>
        <li>Gesamtgewinn: {{ stats.total_pnl }}</li>
        <li>Drawdown: {{ stats.drawdown }}</li>
        <li>Winrate: {{ stats.winrate }}</li>
        <li>Expectancy: {{ stats.expectancy }}</li>
    </ul>
</div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    accounts = accounts_service.get_accounts()
    trades = trade_logger.get_trades()
    stats_raw = reporter.make_stats(trades)
    # Template braucht alle Keys, auch wenn leer
    stats = {**{"total_trades": len(trades), "total_pnl": 0, "drawdown":0, "winrate": 0, "expectancy": 0}, **stats_raw}
    return render_template_string(TEMPLATE, accounts=accounts, trades=trades, stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=False)
