# models.py
from dataclasses import dataclass

@dataclass
class SymbolVolume:
    symbol: str
    turnover_24h: float
