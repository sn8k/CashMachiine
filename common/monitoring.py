"""Shared monitoring utilities v0.1.1 (2025-08-19)"""
from __future__ import annotations

import json
import logging
import os
from logging.handlers import RotatingFileHandler
from functools import lru_cache
from typing import Optional

import requests
from prometheus_client import Counter, Summary, start_http_server, REGISTRY
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


class JsonFormatter(logging.Formatter):
    """Format logs as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        log = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log)


class RemoteLogHandler(logging.Handler):
    """Send logs to a remote HTTP sink."""

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def emit(self, record: logging.LogRecord) -> None:
        try:
            requests.post(self.url, json=json.loads(self.format(record)), timeout=1)
        except Exception:
            pass


def setup_logging(service_name: str, log_path: Optional[str] = None, remote_url: Optional[str] = None) -> logging.Logger:
    """Configure JSON logging to a file and optional remote sink."""
    if log_path is None:
        os.makedirs("logs", exist_ok=True)
        log_path = os.path.join("logs", f"{service_name}.log")
    else:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()

    file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if remote_url:
        remote_handler = RemoteLogHandler(remote_url)
        remote_handler.setFormatter(formatter)
        logger.addHandler(remote_handler)

    return logger


def setup_metrics(service_name: str, port: int = 8000) -> Counter:
    """Start Prometheus metrics server and return request counter."""
    try:
        start_http_server(port)
    except OSError:
        pass
    if "service_requests_total" in REGISTRY._names_to_collectors:
        counter = REGISTRY._names_to_collectors["service_requests_total"]
        return counter.labels(service=service_name)
    return Counter("service_requests_total", "Total requests", ["service"]).labels(service=service_name)


@lru_cache
def setup_performance_metrics(service_name: str) -> Summary:
    """Create and return a Prometheus summary for latency measurements."""
    if "service_latency_seconds" in REGISTRY._names_to_collectors:
        summary = REGISTRY._names_to_collectors["service_latency_seconds"]
        return summary.labels(service=service_name)
    return Summary(
        "service_latency_seconds",
        "Service latency in seconds",
        ["service"],
    ).labels(service=service_name)


def setup_tracer(service_name: str):
    """Initialize OpenTelemetry tracer for the given service."""
    provider = TracerProvider()
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)
