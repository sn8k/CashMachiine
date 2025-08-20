# nosec
"""Unit tests for fees and tax utilities v0.1.0 (2025-08-20)"""
import strategy_engine.fees_tax as ft

__version__ = "0.1.0"

def test_buy_order_cost():
    res = ft.compute_order_cost(qty=10, price=100, side="buy", fee_rate=0.01, tax_rate=0.02)
    assert res["fee"] == 10  # nosec
    assert res["tax"] == 20  # nosec
    assert res["net"] == 1000 + 10 + 20  # nosec

def test_sell_order_cost():
    res = ft.compute_order_cost(qty=10, price=100, side="sell", fee_rate=0.01, tax_rate=0.02)
    assert res["net"] == 1000 - 10 - 20  # nosec
