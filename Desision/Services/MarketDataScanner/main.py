# main.py
import time
from config import BYBIT_REST_TESTNET, TOP_REFRESH_INTERVAL
from top_volume_usdt import TopVolumeUSDTService
from orderBook_WS import OrderBookSubscriber

def main():
    top_service = TopVolumeUSDTService(testnet=BYBIT_REST_TESTNET)
    ws_service = OrderBookSubscriber(testnet=BYBIT_REST_TESTNET)

    top_symbols = top_service.get_top_symbols()
    symbols = [s.symbol for s in top_symbols]

    print("TOP USDT PAIRS:")
    for s in top_symbols:
        print(f"{s.symbol} -> {s.turnover_24h:,.0f}")

    ws_service.subscribe(symbols)

    while True:
        time.sleep(TOP_REFRESH_INTERVAL)

if __name__ == "__main__":
    main()
