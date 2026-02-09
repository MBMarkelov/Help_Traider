from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class OHLCData:
    """Модель OHLC данных"""
    symbol: str
    timeframe: str
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    quote_volume: Optional[Decimal] = None
    trades: Optional[int] = None
    taker_buy_volume: Optional[Decimal] = None
    taker_buy_quote_volume: Optional[Decimal] = None
    
    def to_dict(self):
        """Преобразование в словарь для вставки в БД"""
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "open_time": self.open_time,
            "close_time": self.close_time,
            "open": float(self.open),
            "high": float(self.high),
            "low": float(self.low),
            "close": float(self.close),
            "volume": float(self.volume),
            "quote_volume": float(self.quote_volume) if self.quote_volume else None,
            "trades": self.trades,
            "taker_buy_volume": float(self.taker_buy_volume) if self.taker_buy_volume else None,
            "taker_buy_quote_volume": float(self.taker_buy_quote_volume) if self.taker_buy_quote_volume else None,
        }

@dataclass
class OHLCError:
    """Модель ошибки обработки данных"""
    error_type: str
    error_message: str
    raw_data: dict
    timestamp: datetime = datetime.now()
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            "error_type": self.error_type,
            "error_message": self.error_message,
            "raw_data": self.raw_data,
            "timestamp": self.timestamp
        }