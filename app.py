# app.py
import os
import pandas as pd
import asyncio
from Desision.database.repository import OHLCRepository
from Desision.Services.MarketDataScanner.top_volume_usdt import TopVolumeUSDTService
from Desision.Services.MarketDataScanner.validate import KlineValidator, KlineNormalizer
from Desision.Services.MarketDataScanner.persist import klines_to_rows
from PatternsDetect.chart_patterns_algo.triangles import find_triangle_pattern, find_triangle_pattern
from PatternsDetect.chart_patterns_algo.test_Tri import plot_triangle_pattern

BATCH_SIZE = 1000
INTERVAL = "60"
OUTPUT_DIR = "./cache"

os.makedirs(OUTPUT_DIR, exist_ok=True)


async def main():
    repo = OHLCRepository()

    top_service = TopVolumeUSDTService(testnet=False)
    top_symbols = top_service.get_top_symbols()
    symbols = [s.symbol for s in top_symbols]

    print(f"Top symbols: {symbols}")

    for symbol in symbols:
        print(f"Fetching {INTERVAL} candles for {symbol}")
        ohlc_df = repo.fetch_ohlc(symbol, INTERVAL, limit=1000)
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

        ohlc_df = pd.DataFrame(rows).set_index('ts')
        if ohlc_df.empty:
            print(f"No OHLC data for {symbol}, skipping pattern detection")
            continue

        ohlc_df = pd.DataFrame(rows).reset_index()
        ohlc_with_patterns = find_triangle_pattern(ohlc_df, triangle_type="ascending", lookback=25, rlimit=0.7, slmax_limit=0.001, slmin_limit=0.001)
        pattern_indices = ohlc_with_patterns[ohlc_with_patterns.get("triangle_point", 0) > 0].index.tolist()

        if pattern_indices:
            print(f"Found {len(pattern_indices)} triangle pattern(s) for {symbol}")
            fig = plot_triangle_pattern(
                ohlc_with_patterns,
                pattern_indices,
                triangle_type="ascending",
                title=f"{symbol} - Ascending Triangles"
            )
            output_file = os.path.join(OUTPUT_DIR, f"{symbol}_triangles.html")
            fig.write_html(output_file)
            print(f"Saved chart to {output_file}")
        else:
            print(f"No triangle patterns found for {symbol}")

if __name__ == "__main__":
    asyncio.run(main())
