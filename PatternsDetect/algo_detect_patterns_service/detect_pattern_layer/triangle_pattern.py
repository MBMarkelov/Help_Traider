from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.triangles import find_triangle_pattern
from config import LOOKBACK
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.test_Tri import plot_triangle_pattern
from PatternsDetect.yolo_detect_service.dataset_utils import save_pattern_png
from PatternsDetect.algo_detect_patterns_service.utils import suppress_nearby

from PatternsDetect.algo_detect_patterns_service.interfaces.Ipattern_base import BasePattern, PatternResult


class TrianglePattern(BasePattern):

    def __init__(self, triangle_type: str):
        self.triangle_type = triangle_type

    def name(self):
        return f"triangle_{self.triangle_type}"
    
    def visualize(self, df, pattern_indices, symbol):

        fig = plot_triangle_pattern(
            df,
            pattern_indices,
            triangle_type=self.triangle_type,
            title=f"{symbol} - {self.name()}"
        )

        fig.write_html(f"./cache/{symbol}_{self.name()}.html")

        save_pattern_png(
            df=df,
            pattern_indices=pattern_indices,
            symbol=symbol,
            pattern_type=self.name(),
            output_dir="./cache",
        )

    def detect(self, df):

        ohlc = find_triangle_pattern(
            df.copy(),
            triangle_type=self.triangle_type,
            lookback=LOOKBACK,
            rlimit=0.9,
            slmax_limit=0.0001,
            slmin_limit=0.0001
        )

        indices = ohlc[
            ohlc.get("triangle_point", 0) > 0
        ].index.tolist()
        
        pattern_indices = suppress_nearby(indices, min_gap=LOOKBACK//2)

        return PatternResult(df=ohlc, pattern_indices=pattern_indices)
