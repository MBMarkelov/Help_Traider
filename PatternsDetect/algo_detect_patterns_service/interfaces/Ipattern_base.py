from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PatternResult:
    df: object
    pattern_indices: list

class BasePattern(ABC):

    @abstractmethod
    def detect(self, df):
        pass

    @abstractmethod
    def visualize(self, df, pattern_indices, symbol):
        pass

    @abstractmethod
    def name(self) -> str:
        pass