from dataclasses import dataclass
from typing import List, Iterable, Union
from datetime import datetime, timezone


@dataclass(frozen=True)
class Kline:
    symbol: str
    interval: str
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    turnover: float


class KlineNormalizationError(Exception):
    pass


class KlineNormalizer:
    """
    Универсальный нормализатор Kline для REST и WebSocket
    """

    @staticmethod
    def from_rest(raw: Iterable[list], *, symbol: str, interval: str) -> List[Kline]:
        klines: List[Kline] = []

        for row in raw:
            try:
                ts_ms, open_, high, low, close, volume, turnover = row
                klines.append(
                    Kline(
                        symbol=symbol,
                        interval=interval,
                        ts=datetime.fromtimestamp(int(ts_ms) / 1000, tz=timezone.utc),
                        open=float(open_),
                        high=float(high),
                        low=float(low),
                        close=float(close),
                        volume=float(volume),
                        turnover=float(turnover),
                    )
                )
            except (IndexError, ValueError, TypeError):
                continue  # пропускаем битые свечи

        return klines

    @staticmethod
    def from_ws(msg: dict, *, interval: str) -> List[Kline]:
        if msg.get("type") != "snapshot":
            return []

        symbol = msg.get("topic", "").split(".")[-1]
        klines: List[Kline] = []

        for k in msg.get("data", []):
            if not k.get("confirm"):
                continue
            try:
                klines.append(
                    Kline(
                        symbol=symbol,
                        interval=interval,
                        ts=datetime.fromtimestamp(k["start"] / 1000, tz=timezone.utc),
                        open=float(k["open"]),
                        high=float(k["high"]),
                        low=float(k["low"]),
                        close=float(k["close"]),
                        volume=float(k["volume"]),
                        turnover=float(k["turnover"]),
                    )
                )
            except (KeyError, ValueError, TypeError):
                continue  # пропускаем битые свечи

        return klines

    @staticmethod
    def normalize(raw: Union[Iterable[list], dict], *, symbol: str = "", interval: str = "") -> List[Kline]:
        """
        Универсальный метод для нормализации REST или WS.
        Если передан dict → WS, если list → REST
        """
        if isinstance(raw, dict):
            return KlineNormalizer.from_ws(raw, interval=interval)
        else:
            return KlineNormalizer.from_rest(raw, symbol=symbol, interval=interval)


class KlineValidator:
    """Проверка качества свечей"""

    @staticmethod
    def validate(klines: List[Kline]) -> bool:
        if len(klines) < 5:
            return False

        for k in klines:
            if k.high < k.low:
                return False
            if min(k.open, k.close) < k.low:
                return False
            if max(k.open, k.close) > k.high:
                return False
            if k.volume < 0 or k.turnover < 0:
                return False

        return True
