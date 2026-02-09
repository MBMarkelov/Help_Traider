# top_volume_usdt.py
from pybit.unified_trading import HTTP
from typing import List
from .models import SymbolVolume
from .config import CATEGORY, TOP_N, STABLES

class TopVolumeUSDTService:
    def __init__(self, testnet: bool = False):
        self.session = HTTP(testnet=testnet)
    
    @staticmethod
    def is_valid_spot_symbol(symbol: str) -> bool:
        return (
            symbol.endswith("USDT")
            and not symbol.startswith(STABLES)
        )

    def get_top_symbols(self) -> List[SymbolVolume]:
        response = self.session.get_tickers(category=CATEGORY)

        result = response.get("result", {}).get("list", [])
        usdt_pairs = []

        for item in result:
            symbol = item.get("symbol")
            turnover = item.get("turnover24h")

            if not symbol or not symbol.endswith("USDT"):
                continue
            if symbol.startswith(STABLES):
                continue
            try:
                usdt_pairs.append(
                    SymbolVolume(
                        symbol=symbol,
                        turnover_24h=float(turnover)
                    )
                )
            except (TypeError, ValueError):
                continue

        usdt_pairs.sort(key=lambda x: x.turnover_24h, reverse=True)
        return usdt_pairs[:TOP_N]
