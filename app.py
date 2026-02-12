# app.py
import os
import pandas as pd
import asyncio
from Desision.database.repository import OHLCRepository
from Desision.Services.MarketDataScanner.top_volume_usdt import TopVolumeUSDTService
from Desision.Services.MarketDataScanner.validate import KlineValidator, KlineNormalizer
from Desision.Services.MarketDataScanner.persist import klines_to_rows
from PatternsDetect.chart_patterns_algo.triangles import find_triangle_pattern
from PatternsDetect.chart_patterns_algo.test_Tri import plot_triangle_pattern
from PatternsDetect.YoloModule.dataset_utils import save_pattern_png


BATCH_SIZE = 1000
INTERVAL = "60"
OUTPUT_DIR = "./cache"
TRIANGLE_TYPES = ["ascending", "descending", "symmetrical"]
WINDOW = 100
MIN_GAP = 15
LOOKBACK = 25

os.makedirs(OUTPUT_DIR, exist_ok=True)

def suppress_nearby(pattern_indices, min_gap=MIN_GAP):
    if not pattern_indices:
        return []
    pattern_indices = sorted(pattern_indices)
    filtered = [pattern_indices[0]]
    for idx in pattern_indices[1:]:
        if idx - filtered[-1] >= min_gap:
            filtered.append(idx)
    return filtered

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

        new_df = pd.DataFrame(rows)

        if not new_df.empty:
            ohlc_df = pd.concat([ohlc_df.reset_index(), new_df])
        else:
            ohlc_df = ohlc_df.reset_index()

        ohlc_df.reset_index(drop=True, inplace=True)

        if ohlc_df.empty:
            continue
        idx=0
        for triangle_type in TRIANGLE_TYPES:

            ohlc_with_patterns = find_triangle_pattern(
                ohlc_df.copy(),
                triangle_type=triangle_type,
                lookback=LOOKBACK,
                rlimit=0.9,
                slmax_limit=0.0001,
                slmin_limit=0.0001
            )

            pattern_indices = ohlc_with_patterns[
                ohlc_with_patterns.get("triangle_point", 0) > 0
            ].index.tolist()
            pattern_indices = suppress_nearby(pattern_indices, min_gap=LOOKBACK//2)

            if not pattern_indices:
                print(f"No {triangle_type} triangles for {symbol}")
                continue

            print(f"Found {len(pattern_indices)} {triangle_type} triangle(s) for {symbol}")

            if not pattern_indices:
                continue

            print(
                f"{symbol}: found {len(pattern_indices)} "
                f"{triangle_type} triangle(s)"
            )
             # --- HTML для отладки ---
            html_fig = plot_triangle_pattern(
                ohlc_with_patterns,
                pattern_indices,
                triangle_type=triangle_type,
                title=f"{symbol} - {triangle_type} triangles"
            )
            html_path = os.path.join(OUTPUT_DIR, f"{symbol}_{triangle_type}.html")
            html_fig.write_html(html_path)
            print(f"Saved HTML for debug: {html_path}")
            
            # png
            save_pattern_png(
                df=ohlc_with_patterns,
                pattern_indices=pattern_indices,
                symbol=symbol,
                pattern_type=triangle_type,
                output_dir=OUTPUT_DIR,
            )
            filename = f"{symbol}_{triangle_type}_{idx+1}.png"
            print("saved ->", filename)

if __name__ == "__main__":
    asyncio.run(main())
