# nosec
"""Unit tests for alert-engine v0.1.0 (2025-08-20)"""
import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[2]))

MODULE_PATH = Path(__file__).resolve().parents[1] / "main.py"
SPEC = importlib.util.spec_from_file_location("alert_engine_main", MODULE_PATH)
main = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(main)


def test_process_metric_triggers_alert():
    with patch.object(main, "_send_alert") as mock_alert:
        main.process_metric({"metric": "risk", "value": 1.2})
        mock_alert.assert_called_once()


def test_process_metric_no_alert():
    with patch.object(main, "_send_alert") as mock_alert:
        main.process_metric({"metric": "risk", "value": 0.1})
        mock_alert.assert_not_called()
