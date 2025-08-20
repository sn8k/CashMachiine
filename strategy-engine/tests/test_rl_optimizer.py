from strategy_engine import rl_optimizer


def test_optimize_allocation_trains_and_predicts():
    rl_optimizer.train_allocation_model(timesteps=10)
    weight = rl_optimizer.optimize_allocation(0.01)
    assert 0.0 <= weight <= 1.0
