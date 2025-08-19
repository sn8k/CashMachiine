"""Strategy interface for strategy-engine v0.1.1 (2025-08-20)"""
from abc import ABC, abstractmethod

__version__ = "0.1.1"


class Strategy(ABC):
    """Base strategy interface defining signals and target weights methods."""

    @abstractmethod
    def signals(self, market_data):
        """Return trading signals based on market data."""
        raise NotImplementedError

    @abstractmethod
    def target_weights(self, signals):
        """Return target portfolio weights based on signals."""
        raise NotImplementedError

    @abstractmethod
    def explain(self) -> str:
        """Return human-readable justification for the latest weights."""
        raise NotImplementedError
