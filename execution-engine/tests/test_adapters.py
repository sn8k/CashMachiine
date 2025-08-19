import importlib
import importlib.util
from pathlib import Path
import sys
import pytest
import requests

ROOT = Path(__file__).resolve().parents[2]
PKG_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

spec = importlib.util.spec_from_file_location(
    "execution_engine", PKG_PATH / "__init__.py", submodule_search_locations=[str(PKG_PATH)]
)
package = importlib.util.module_from_spec(spec)
sys.modules["execution_engine"] = package
spec.loader.exec_module(package)

binance_mod = importlib.import_module("execution_engine.adapters.binance")
ibkr_mod = importlib.import_module("execution_engine.adapters.ibkr")
BinanceAdapter = binance_mod.BinanceAdapter
IBKRAdapter = ibkr_mod.IBKRAdapter


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.HTTPError("error")

    def json(self):
        return self._payload


def test_binance_adapter_success(monkeypatch):
    adapter = BinanceAdapter()

    def fake_post(url, headers, json, timeout):
        if "X-MBX-APIKEY" not in headers:
            raise AssertionError("missing API key")
        return DummyResponse({"orderId": "1", "executedQty": "1", "fills": [{"price": "10"}]})

    monkeypatch.setattr(binance_mod.requests, "post", fake_post)
    result = adapter.place_order({"symbol": "BTCUSDT"})
    if result["order_id"] != "1":
        raise AssertionError("unexpected order_id")
    if result["price"] != "10":
        raise AssertionError("unexpected price")


def test_ibkr_adapter_error(monkeypatch):
    adapter = IBKRAdapter()

    def fake_post(*args, **kwargs):
        raise requests.RequestException("boom")

    monkeypatch.setattr(ibkr_mod.requests, "post", fake_post)
    with pytest.raises(RuntimeError):
        adapter.place_order({"symbol": "AAPL"})
