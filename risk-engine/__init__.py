"""risk-engine service v0.4.6 (2025-08-20)"""
__version__ = "0.4.6"

try:
    from .engine import volatility_target, var_es, kelly_fraction
    from .anomaly import detect_anomalies
except ImportError:  # pragma: no cover - package import fallback
    pass
