from strategy_engine import rl_optimizer


def test_optimize_allocation_range():
    weight = rl_optimizer.optimize_allocation(0.01)
    if not 0.0 <= weight <= 1.0:
        raise AssertionError("weight out of range")
