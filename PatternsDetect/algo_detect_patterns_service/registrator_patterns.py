from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.triangle_pattern import TrianglePattern
from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.flag_pattern import FlagPattern
from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.INS_pattern import InverseHeadShouldersPattern
from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.pennant_pattern import PennantPattern
from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.HS_pattern import HeadAndShouldersPattern
from PatternsDetect.algo_detect_patterns_service.detect_pattern_layer.double_pattern import DoublePattern

def get_registered_patterns():

    return [
        TrianglePattern("ascending"),
        TrianglePattern("descending"),
        TrianglePattern("symmetrical"),
        FlagPattern(),
        PennantPattern(),
        InverseHeadShouldersPattern(),
        HeadAndShouldersPattern(),
        DoublePattern("both"),
    ]