from PatternsDetect.algo_detect_patterns_service.interfaces.Ipattern_base import BasePattern, PatternResult
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.test_Tri import plot_ihs_pattern
from PatternsDetect.yolo_detect_service.dataset_utils import save_pattern_png
from PatternsDetect.algo_detect_patterns_service.utils import suppress_nearby
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.inverse_head_and_shoulders import find_inverse_head_and_shoulders
from config import LOOKBACK


class InverseHeadShouldersPattern(BasePattern):

    def name(self):
        return "inverse_head_shoulders"

    def detect(self, df):

        ohlc = find_inverse_head_and_shoulders(
            df.copy(),
            lookback=60,
            pivot_interval=10,
            short_pivot_interval=5,
            head_ratio_before=0.98,
            head_ratio_after=0.98,
            upper_slmax=1e-4,
        )

        indices = ohlc[
            ohlc.get("chart_type", "") == "ihs"
        ].index.tolist()
        
        pattern_indices = suppress_nearby(indices, min_gap=LOOKBACK//2)


        return PatternResult(
            df=ohlc,
            pattern_indices=pattern_indices
        )

    def visualize(self, df, pattern_indices, symbol):

        fig = plot_ihs_pattern(
            df,
            pattern_indices,
            title=f"{symbol} - IHS"
        )

        fig.write_html(f"./cache/{symbol}_ihs.html")

        save_pattern_png(
            df=df,
            pattern_indices=pattern_indices,
            symbol=symbol,
            pattern_type=self.name(),
            output_dir="./cache",
        )
