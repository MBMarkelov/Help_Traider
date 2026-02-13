from dataclasses import dataclass
from PatternsDetect.chart_patterns_algo.triangles import find_triangle_pattern
from config import WINDOW, LOOKBACK, MIN_GAP

@dataclass
class PatternResult:
    df: object
    pattern_indices: list

def suppress_nearby(pattern_indices, min_gap=MIN_GAP):
    if not pattern_indices:
        return []

    pattern_indices = sorted(pattern_indices)
    filtered = [pattern_indices[0]]

    for idx in pattern_indices[1:]:
        if idx - filtered[-1] >= min_gap:
            filtered.append(idx)

    return filtered

def detect_triangles(df, triangle_type):

    ohlc_with_patterns = find_triangle_pattern(
        df.copy(),
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

    return PatternResult(
        df=ohlc_with_patterns,
        pattern_indices=pattern_indices
    )
