"""strategy-engine service v0.3.0 (2025-08-19)"""
__version__ = "0.3.0"

from strategy_engine.interface import Strategy
from strategy_engine.risk_client import adjust_risk
from strategy_engine.simulation import generate_paths, probability_of_hitting
