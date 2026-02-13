from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.triangle_pattern import TrianglePattern
from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.flag_pattern import FlagPattern

def get_registered_patterns():

    return [
        TrianglePattern("ascending"),
        TrianglePattern("descending"),
        TrianglePattern("symmetrical"),
        FlagPattern(),
    ]