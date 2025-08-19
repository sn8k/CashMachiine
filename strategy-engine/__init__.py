"""strategy-engine service v0.4.5 (2025-08-20)"""
__version__ = "0.4.5"

from strategy_engine.interface import Strategy
from strategy_engine.risk_client import adjust_risk
from strategy_engine.simulation import generate_paths, probability_of_hitting
