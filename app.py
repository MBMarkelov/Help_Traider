# app.py
import asyncio
from datetime import datetime, timezone
from Desision.database.connection import get_connection
from Desision.database.repository import OHLCRepository
from Desision.Services.MarketDataScanner.top_volume_usdt import TopVolumeUSDTService
from Desision.Services.MarketDataScanner.Kline_WS import BybitKlineHandler

BATCH_SIZE = 25
INTERVAL = "60"  # часовые свечи

async def main():
    # 1. Подключаемся к БД
    repo = OHLCRepository()

    # 2. Получаем топ-10 символов по объему
    top_service = TopVolumeUSDTService(testnet=False)
    top_symbols = top_service.get_top_symbols()  # список SymbolVolume
    top_symbols_str = [s.symbol for s in top_symbols]
    print(f"Top symbols: {top_symbols_str}")

    # 3. Для каждого символа грузим свечи
    kline_handler = BybitKlineHandler(repo=repo, interval=INTERVAL)

    for symbol in top_symbols_str:
        print(f"Fetching {INTERVAL} candles for {symbol}")
        # Получаем свечи через HTTP API Bybit
        data = top_service.session.get_kline(
            symbol=symbol,
            interval=INTERVAL,
            limit=BATCH_SIZE
        )
        candles = data.get("result") or []
        if not isinstance(candles, list):
            print(f"Warning: unexpected kline format for {symbol}: {candles}")
            continue

        msg = {"type": "snapshot", "topic": f"kline.{INTERVAL}.{symbol}", "data": candles}
        kline_handler.on_message(msg)

    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
