"""Utilities to compute broker fees and taxes per order v0.1.0 (2025-08-20)"""
__version__ = "0.1.0"

def compute_fee(order_value: float, fee_rate: float) -> float:
    """Return broker fee for a given order value."""
    return round(order_value * fee_rate, 2)

def compute_tax(order_value: float, tax_rate: float) -> float:
    """Return tax for a given order value."""
    return round(order_value * tax_rate, 2)

def compute_order_cost(qty: float, price: float, side: str,
                       fee_rate: float = 0.001, tax_rate: float = 0.005) -> dict:
    """Calculate gross, fee, tax and net totals for an order."""
    gross = qty * price
    fee = compute_fee(gross, fee_rate)
    tax = compute_tax(gross, tax_rate)
    sign = 1 if side.lower() == "buy" else -1
    net = gross + sign * (fee + tax)
    return {"gross": gross, "fee": fee, "tax": tax, "net": net}
