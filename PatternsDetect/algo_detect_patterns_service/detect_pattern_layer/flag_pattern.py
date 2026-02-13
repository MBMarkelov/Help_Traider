from PatternsDetect.algo_detect_patterns_service.interfaces.Ipattern_base import BasePattern, PatternResult
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.flag import find_flag_pattern
from PatternsDetect.algo_detect_patterns_service.chart_patterns_algo_module.test_Tri import plot_flag_pattern
from PatternsDetect.yolo_detect_service.dataset_utils import save_pattern_png
from PatternsDetect.algo_detect_patterns_service.utils import suppress_nearby

from config import LOOKBACK



class FlagPattern(BasePattern):

    def name(self):
        return "flag"
    
    def visualize(self, df, pattern_indices, symbol):
        fig = plot_flag_pattern(
            df,
            pattern_indices,
            title=f"{symbol} - flag"
        )

        fig.write_html(f"./cache/{symbol}_flag.html")

        save_pattern_png(
            df=df,
            pattern_indices=pattern_indices,
            symbol=symbol,
            pattern_type="flag",
            output_dir="./cache",
        )

    def detect(self, df):

        ohlc = find_flag_pattern(
            df.copy(),
            lookback=25,
            min_points=3,
            r_max=0.9,
            r_min=0.9
        )

        indices = ohlc[
            ohlc.get("flag_point", 0) > 0
        ].index.tolist()

        pattern_indices = suppress_nearby(indices, min_gap=LOOKBACK//2)


        return PatternResult(df=ohlc, pattern_indices=pattern_indices)
