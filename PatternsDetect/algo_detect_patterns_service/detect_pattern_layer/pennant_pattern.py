from PatternsDetect.algo_detect_patterns_service.interfaces.Ipattern_base import BasePattern, PatternResult
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.test_Tri import plot_pennant_pattern
from PatternsDetect.yolo_detect_service.dataset_utils import save_pattern_png
from PatternsDetect.algo_detect_patterns_service.utils import suppress_nearby
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.pennant import find_pennant
from config import LOOKBACK

class PennantPattern(BasePattern):

    def name(self):
        return "pennant"

    def detect(self, df):

        ohlc = find_pennant(
            df.copy(),
            lookback=20,
            min_points=3,
            r_max=0.9,
            r_min=0.9,
            slope_max=-0.0001,
            slope_min=0.0001,
            lower_ratio_slope=0.95,
            upper_ratio_slope=1
        )

        indices = ohlc[
            ohlc.get("pennant_point", 0) > 0
        ].index.tolist()
    
        pattern_indices = suppress_nearby(indices, min_gap=LOOKBACK//2)


        return PatternResult(
            df=ohlc,
            pattern_indices=pattern_indices
        )
    
    def visualize(self, df, pattern_indices, symbol):

        fig = plot_pennant_pattern(
            df,
            pattern_indices,
            title=f"{symbol} - Pennant"
        )

        fig.write_html(f"./cache/{symbol}_pennant.html")

        save_pattern_png(
            df=df,
            pattern_indices=pattern_indices,
            symbol=symbol,
            pattern_type=self.name(),
            output_dir="./cache",
        )
