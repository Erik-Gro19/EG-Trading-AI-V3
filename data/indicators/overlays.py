# data/indicators/overlays.py

import numpy as np
from typing import List, Dict, Optional

def ema(prices: List[float], period: int) -> List[Optional[float]]:
    ema_list = []
    k = 2 / (period + 1)
    ema_val = None
    for price in prices:
        if ema_val is None:
            ema_val = price
        else:
            ema_val = (price * k) + (ema_val * (1 - k))
        ema_list.append(round(ema_val, 2))
    # Pad initial values as None
    for i in range(period-1):
        ema_list[i] = None
    return ema_list

def vwap(ohlc: List[Dict]) -> List[float]:
    vwap_vals = []
    cumul_pv, cumul_vol = 0.0, 0.0
    for c in ohlc:
        price = (c['high'] + c['low'] + c['close']) / 3
        vol = c['volume']
        cumul_pv += price * vol
        cumul_vol += vol
        if cumul_vol == 0:
            vwap_vals.append(None)
        else:
            vwap_vals.append(round(cumul_pv / cumul_vol, 2))
    return vwap_vals

def session_high_low(ohlc: List[Dict]) -> Dict[str, List[Optional[float]]]:
    # New York session: 13:00-21:00 UTC, Tokyo: 00:00-09:00 UTC, London: 08:00-17:00 UTC
    import datetime
    highs, lows = [], []
    high = low = None
    last_session = None

    for c in ohlc:
        ts = c['timestamp']
        dt = datetime.datetime.utcfromtimestamp(ts/1000)
        session = get_session(dt)
        if session != last_session:
            high = c['high']
            low = c['low']
            last_session = session
        else:
            high = max(high, c['high'])
            low = min(low, c['low'])
        highs.append(high)
        lows.append(low)
    return {"session_high": highs, "session_low": lows}

def get_session(dt):
    hour = dt.hour
    if 13 <= hour < 21:
        return "NY"
    elif 8 <= hour < 17:
        return "LDN"
    elif 0 <= hour < 9:
        return "TKY"
    else:
        return "OTHER"
