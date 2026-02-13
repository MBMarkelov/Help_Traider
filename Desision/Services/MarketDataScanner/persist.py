# Desision/Services/MarketDataScanner/persist.py
from typing import List
from Desision.database.models import Kline

def klines_to_rows(klines: List[Kline]) -> list[dict]:
    return [
        {
            "symbol": k.symbol,
            "interval": k.interval,
            "ts": k.ts,
            "open": k.open,
            "high": k.high,
            "low": k.low,
            "close": k.close,
            "volume": k.volume,
            "turnover": k.turnover,
        }
        for k in klines
    ]
