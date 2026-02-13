from Desision.Services.MarketDataScanner.top_volume_usdt import get_top_symbols
from Desision.Services.MarketDataScanner.data_loader import load_symbol_data
from PatternsDetect.algo_detect_patterns_service.registrator_patterns import get_registered_patterns
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

            patterns = get_registered_patterns()

            for pattern in patterns:

                result = pattern.detect(df)

                if not result.pattern_indices:
                    continue

                pattern.visualize(
                    df=result.df,
                    pattern_indices=result.pattern_indices,
                    symbol=symbol
                )
