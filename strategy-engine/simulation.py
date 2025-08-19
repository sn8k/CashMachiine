"""Monte Carlo simulation utilities v0.1.0 (2025-08-20)"""
import numpy as np

__version__ = "0.1.0"

def generate_paths(s0: float, mu: float, sigma: float, steps: int, n_paths: int, dt: float = 1/252, seed: int | None = None) -> np.ndarray:
    """Generate geometric Brownian motion paths.

    Args:
        s0: Initial asset price.
        mu: Drift of the process.
        sigma: Volatility of the process.
        steps: Number of time steps to simulate.
        n_paths: Number of simulation paths.
        dt: Time increment in years, defaults to daily (1/252).
        seed: Optional random seed for reproducibility.

    Returns:
        ndarray of shape (n_paths, steps + 1) with simulated price paths.
    """
    rng = np.random.default_rng(seed)
    increments = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), (n_paths, steps))
    log_paths = np.cumsum(increments, axis=1)
    paths = s0 * np.exp(log_paths)
    return np.column_stack([np.full(n_paths, s0), paths])


def probability_of_hitting(paths: np.ndarray, barrier: float) -> float:
    """Probability that simulated paths hit a barrier level.

    Args:
        paths: Simulated price paths.
        barrier: Price level to evaluate.

    Returns:
        Fraction of paths that touch or cross the barrier.
    """
    hits = (paths >= barrier).any(axis=1)
    return float(hits.mean())
