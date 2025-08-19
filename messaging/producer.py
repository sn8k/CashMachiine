"""RabbitMQ event producer v0.1.0 (2025-08-19)"""
import json
import pika


class EventProducer:
    """Publish events to a RabbitMQ exchange."""

    def __init__(self, url: str, exchange: str = "events"):
        self._url = url
        self._exchange = exchange
        self._conn = pika.BlockingConnection(pika.URLParameters(url))
        self._channel = self._conn.channel()
        self._channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)

    def publish(self, event: str, payload: dict) -> None:
        body = json.dumps({"event": event, "payload": payload})
        self._channel.basic_publish(exchange=self._exchange, routing_key="", body=body)

    def close(self) -> None:
        self._conn.close()
