# app.py
import asyncio
from Desision.database.repository import OHLCRepository
from Desision.Services.MarketDataScanner.top_volume_usdt import TopVolumeUSDTService
from Desision.Services.MarketDataScanner.validate import KlineValidator, KlineNormalizer
from Desision.Services.MarketDataScanner.persist import klines_to_rows

BATCH_SIZE = 25
INTERVAL = "60"

async def main():
    repo = OHLCRepository()

    top_service = TopVolumeUSDTService(testnet=False)
    top_symbols = top_service.get_top_symbols()
    symbols = [s.symbol for s in top_symbols]

    print(f"Top symbols: {symbols}")

    for symbol in symbols:
        print(f"Fetching {INTERVAL} candles for {symbol}")

        try:
            response = top_service.session.get_kline(
                category="spot",
                symbol=symbol,
                interval=INTERVAL,
                limit=BATCH_SIZE,
            )
        except Exception as e:
            print(f"HTTP error for {symbol}: {e}")
            continue

        raw = response.get("result", {}).get("list")
        if not isinstance(raw, list):
            print(f"Skipping {symbol}: invalid response format")
            continue

        klines = KlineNormalizer.from_rest(
            raw,
            symbol=symbol,
            interval=INTERVAL,
        )

        if not KlineValidator.validate(klines):
            print(f"Skipping {symbol}: validation failed")
            continue

        rows = klines_to_rows(klines)
        if rows:
            repo.insert_ohlc(rows)

    print("Done")

if __name__ == "__main__":
    asyncio.run(main())
