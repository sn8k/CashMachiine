import importlib
import importlib.util
from pathlib import Path
import sys
import fakeredis

ROOT = Path(__file__).resolve().parents[2]
PKG_PATH = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

spec = importlib.util.spec_from_file_location(
    "execution_engine", PKG_PATH / "__init__.py", submodule_search_locations=[str(PKG_PATH)]
)
package = importlib.util.module_from_spec(spec)
sys.modules["execution_engine"] = package
spec.loader.exec_module(package)

order_handler_mod = importlib.import_module("execution_engine.order_handler")
OrderHandler = order_handler_mod.OrderHandler


class DummyAdapter:
    def place_order(self, order):
        return {"order_id": "abc", "price": 10, "qty": 1}


class FakeCursor:
    def __init__(self, executed):
        self.executed = executed

    def execute(self, sql, params):
        self.executed.append((sql.strip(), params))

    def fetchone(self):
        return [1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class FakeConn:
    def __init__(self, executed):
        self.executed = executed

    def cursor(self):
        return FakeCursor(self.executed)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


def test_order_persistence(monkeypatch):
    executed = []

    def fake_connect(**kwargs):
        return FakeConn(executed)

    monkeypatch.setattr(order_handler_mod.psycopg2, "connect", fake_connect)

    redis_client = fakeredis.FakeRedis()
    handler = OrderHandler(redis_client=redis_client)
    handler.adapters["binance"] = DummyAdapter()

    order_id = handler.place_order("binance", {"symbol": "BTC", "qty": 1})
    assert order_id == "abc"
    assert redis_client.get("order:abc") is not None
    assert any("INSERT INTO orders" in sql for sql, _ in executed)
    assert any("INSERT INTO executions" in sql for sql, _ in executed)
