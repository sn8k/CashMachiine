"""Event helpers v0.1.0 (2025-08-20)"""
from messaging import EventProducer
from config import settings

_producer: EventProducer | None = None

def get_event_producer() -> EventProducer:
    """Return a singleton RabbitMQ event producer."""
    global _producer
    if _producer is None:
        _producer = EventProducer(settings.rabbitmq_url)
    return _producer

def emit_event(event: str, payload: dict) -> None:
    """Publish an event with the given payload."""
    producer = get_event_producer()
    producer.publish(event, payload)
