"""RabbitMQ event consumer v0.1.0 (2025-08-19)"""
import json
import pika
from typing import Callable, Any


class EventConsumer:
    """Consume events from a RabbitMQ exchange."""

    def __init__(self, url: str, queue: str, exchange: str = "events"):
        self._conn = pika.BlockingConnection(pika.URLParameters(url))
        self._channel = self._conn.channel()
        self._channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)
        self._channel.queue_declare(queue=queue, durable=True)
        self._channel.queue_bind(queue=queue, exchange=exchange)
        self._queue = queue

    def start(self, handler: Callable[[dict], Any]) -> None:
        def _callback(ch, method, properties, body):
            message = json.loads(body)
            handler(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self._channel.basic_consume(queue=self._queue, on_message_callback=_callback)
        self._channel.start_consuming()

    def close(self) -> None:
        self._conn.close()
