# orderbook_ws.py
from pybit.unified_trading import WebSocket
from typing import List
import json
from config import CATEGORY

class OrderBookSubscriber:
    def __init__(self, testnet: bool = False):
        self.ws = WebSocket(
            testnet=testnet,
            channel_type=CATEGORY
        )

    def subscribe(self, symbols: List[str]):
        for chunk in self._chunk(symbols, 10):
            self.ws.orderbook_stream(
                depth=50,
                symbol=chunk,
                callback=self.on_message
            )

    @staticmethod
    def on_message(message: dict):
        topic = message.get("topic")
        data = message.get("data")

        if not data:
            return

        symbol = data.get("s")
        bids = data.get("b", [])
        asks = data.get("a", [])

        print(
            f"[ORDERBOOK] {symbol} | "
            f"Bids: {len(bids)} | Asks: {len(asks)}"
        )

    @staticmethod
    def _chunk(items: list, size: int):
        for i in range(0, len(items), size):
            yield items[i:i + size]
