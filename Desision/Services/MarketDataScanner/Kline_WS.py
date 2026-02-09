from datetime import datetime, timezone

from Desision.database.repository import OHLCRepository

class BybitKlineHandler:
    def __init__(self, repo: OHLCRepository, interval: str):
        self.repo = repo
        self.interval = interval

    def on_message(self, msg: dict):
        """
        msg — payload из pybit websocket
        """
        if msg.get("type") != "snapshot":
            return

        rows = []

        for k in msg["data"]:
            if not k["confirm"]:
                continue  # только закрытые свечи

            rows.append({
                "symbol": msg["topic"].split(".")[-1],
                "interval": self.interval,
                "ts": datetime.fromtimestamp(k["start"] / 1000, tz=timezone.utc),
                "open": float(k["open"]),
                "high": float(k["high"]),
                "low": float(k["low"]),
                "close": float(k["close"]),
                "volume": float(k["volume"]),
                "turnover": float(k["turnover"]),
            })

        if rows:
            self.repo.insert_ohlc(rows)
