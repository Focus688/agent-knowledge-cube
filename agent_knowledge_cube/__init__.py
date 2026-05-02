"""Agent Knowledge Cube — 三维知识约束框架"""

from .loader import Cube
from .optimizer import WeightedOptimizer, WeightedResult, OptimizationConfig

__version__ = "0.2.0"
__all__ = ["Cube", "WeightedOptimizer", "WeightedResult", "OptimizationConfig"]
