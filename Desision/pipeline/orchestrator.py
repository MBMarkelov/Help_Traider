from Desision.Services.MarketDataScanner.top_volume_usdt import get_top_symbols
from Desision.Services.MarketDataScanner.data_loader import load_symbol_data
from PatternsDetect.pattern_service import detect_triangles
from PatternsDetect.visualization import save_outputs
from config import INTERVAL, TRIANGLE_TYPES

class PatternPipeline:

    def __init__(self):
        self.interval = INTERVAL
        self.triangle_types = TRIANGLE_TYPES

    async def run(self):
        symbols = get_top_symbols()

        for symbol in symbols:
            df = load_symbol_data(symbol, self.interval)

            if df.empty:
                continue

            for triangle_type in self.triangle_types:
                result = detect_triangles(df, triangle_type)

                if not result.pattern_indices:
                    continue

                save_outputs(
                    df=result.df,
                    pattern_indices=result.pattern_indices,
                    symbol=symbol,
                    triangle_type=triangle_type
                )
