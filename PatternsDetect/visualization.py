import os
from PatternsDetect.chart_patterns_algo.test_Tri import plot_triangle_pattern
from PatternsDetect.YoloModule.dataset_utils import save_pattern_png

from config import OUTPUT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_outputs(df, pattern_indices, symbol, triangle_type):

    html_fig = plot_triangle_pattern(
        df,
        pattern_indices,
        triangle_type=triangle_type,
        title=f"{symbol} - {triangle_type} triangles"
    )

    html_path = os.path.join(OUTPUT_DIR, f"{symbol}_{triangle_type}.html")
    html_fig.write_html(html_path)

    save_pattern_png(
        df=df,
        pattern_indices=pattern_indices,
        symbol=symbol,
        pattern_type=triangle_type,
        output_dir=OUTPUT_DIR,
    )
