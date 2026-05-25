# data/normalizer.py

def normalize_candle(candle: dict, source: str) -> dict:
    """
    Converts different candle formats to unified schema.
    """
    if source == "binance":
        return {
            "timestamp": candle["timestamp"],
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle["volume"],
        }
    elif source == "forexcom":
        from dateutil import parser
        ts = parser.isoparse(candle["timestamp"])
        return {
            "timestamp": int(ts.timestamp() * 1000),
            "open": candle["open"],
            "high": candle["high"],
            "low": candle["low"],
            "close": candle["close"],
            "volume": candle["volume"],
        }
    else:
        raise ValueError(f"Unknown candle source {source}")
