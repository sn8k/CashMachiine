"""strategy-engine service v0.3.1 (2025-08-20)"""
__version__ = "0.3.1"

from strategy_engine.interface import Strategy
from strategy_engine.risk_client import adjust_risk
from strategy_engine.simulation import generate_paths, probability_of_hitting
from strategy_engine.fees_tax import compute_order_cost
