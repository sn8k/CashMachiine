"""Reinforcement learning optimizer utilities v0.1.0 (2025-08-20)"""
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

__version__ = "0.1.0"

MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(exist_ok=True)


class AllocationEnv(gym.Env):
    """Minimal environment optimizing allocation based on returns."""

    metadata = {"render_modes": []}

    def __init__(self, returns: Sequence[float]):
        super().__init__()
        self.returns = np.array(returns, dtype=np.float32)
        self.current_step = 0
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(1,), dtype=np.float32)

    def reset(self, *, seed: int | None = None, options: dict | None = None):  # type: ignore[override]
        super().reset(seed=seed)
        self.current_step = 0
        return np.array([self.returns[self.current_step]], dtype=np.float32), {}

    def step(self, action):  # type: ignore[override]
        alloc = float(np.clip(action[0], 0.0, 1.0))
        reward = alloc * self.returns[self.current_step]
        self.current_step += 1
        terminated = self.current_step >= len(self.returns)
        obs = np.array([self.returns[self.current_step]], dtype=np.float32) if not terminated else np.array([0.0], dtype=np.float32)
        return obs, reward, terminated, False, {}


def train_allocation_model(timesteps: int = 1000) -> Path:
    """Train a PPO model on historical returns and save it."""
    data_path = MODEL_DIR / "historical_returns.csv"
    if not data_path.exists():
        pd.DataFrame({"return": [0.01, -0.02, 0.015, 0.005, -0.01, 0.02]}).to_csv(data_path, index=False)
    df = pd.read_csv(data_path)
    env = DummyVecEnv([lambda: AllocationEnv(df["return"].values)])
    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=timesteps)
    model_path = MODEL_DIR / "ppo_allocation.zip"
    model.save(model_path)
    return model_path


def optimize_allocation(recent_return: float) -> float:
    """Return optimized allocation for the latest return."""
    model_path = MODEL_DIR / "ppo_allocation.zip"
    if not model_path.exists():
        train_allocation_model(timesteps=500)
    model = PPO.load(model_path)
    action, _ = model.predict(np.array([recent_return], dtype=np.float32))
    return float(np.clip(action[0], 0.0, 1.0))


if __name__ == "__main__":  # pragma: no cover - manual training hook
    train_allocation_model()
