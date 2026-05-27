# api/server.py

from flask import Flask, request, jsonify
from engine.utils.accounts_service import AccountsService
from engine.performance.logger import TradeLogger
from engine.performance.reporter import TradeReporter

app = Flask(__name__)

# Pfade der Datenbanken (nutzt deine .json)
accounts_service = AccountsService("accounts.json")
trade_logger = TradeLogger()
reporter = TradeReporter()

@app.route("/api/accounts")
def get_accounts():
    return jsonify(accounts_service.get_accounts())

@app.route("/api/trades")
def get_trades():
    return jsonify(trade_logger.get_trades())

@app.route("/api/stats")
def get_stats():
    trades = trade_logger.get_trades()
    return jsonify(reporter.make_stats(trades))

@app.route("/api/add_trade", methods=["POST"])
def add_trade():
    trade = request.json
    trade_logger.add_trade(trade)
    return jsonify({"success": True})

@app.route("/api/trigger_alert", methods=["POST"])
def trigger_alert():
    # Du kannst hier z. B. deinen zentralen NotificationBus nutzen
    message = request.json.get('msg', '')
    # notification_bus.notify(message, level="info")  # Falls NotificationBus zugänglich ist
    return jsonify({"success": True, "msg": message})

# Optional: REST-Schutz mit Token
@app.before_request
def check_auth():
    # Hier könntest du einen "API-Key" prüfen, z. B. via Header:
    # if request.headers.get("X-API-KEY") != "dein_geheimer_key":
    #     return jsonify({"error": "Unauthorized"}), 401
    pass

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
