"""Strategy interface for strategy-engine v0.1.0 (2025-08-18)"""
from abc import ABC, abstractmethod

__version__ = "0.1.0"


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
