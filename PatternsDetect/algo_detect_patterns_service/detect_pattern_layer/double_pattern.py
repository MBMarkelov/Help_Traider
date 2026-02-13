from PatternsDetect.algo_detect_patterns_service.interfaces.Ipattern_base import BasePattern, PatternResult
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.test_Tri import plot_double_pattern
from PatternsDetect.yolo_detect_service.dataset_utils import save_pattern_png
from PatternsDetect.algo_detect_patterns_service.utils import suppress_nearby
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.doubles import find_doubles_pattern
from config import LOOKBACK


class DoublePattern(BasePattern):

    def __init__(self, double_type: str = "both"):
        self.double_type = double_type

    def name(self):
        return f"double_{self.double_type}"

    def detect(self, df):

        ohlc = find_doubles_pattern(
            df.copy(),
            lookback=25,
            double=self.double_type,
            tops_max_ratio=1.01,
            bottoms_min_ratio=0.98,
            progress=False
        )

        indices = ohlc[
            ohlc.get("chart_type", "") == "double"
        ].index.tolist()

        pattern_indices = suppress_nearby(indices, min_gap=LOOKBACK//2)

        return PatternResult(
            df=ohlc,
            pattern_indices=pattern_indices
        )
    
    def visualize(self, df, pattern_indices, symbol):

        fig = plot_double_pattern(
            df,
            pattern_indices,
            title=f"{symbol} - Double"
        )

        fig.write_html(f"./cache/{symbol}_double.html")

        save_pattern_png(
            df=df,
            pattern_indices=pattern_indices,
            symbol=symbol,
            pattern_type=self.name(),
            output_dir="./cache",
        )
