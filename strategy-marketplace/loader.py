"""Strategy loader v0.1.1 (2025-08-20)"""
from __future__ import annotations
import hashlib
import hmac
import subprocess  # nosec B404
import tempfile
from pathlib import Path


def verify_signature(file_path: str, signature: str, key: str) -> bool:
    """Return True if HMAC-SHA256 signature matches."""
    data = Path(file_path).read_bytes()
    digest = hmac.new(key.encode(), data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def run_strategy(file_path: str, image: str = "python:3.11") -> str:
    """Execute strategy inside a restricted Docker container and return output."""
    container_strategy_path = Path(tempfile.gettempdir()) / "strategy.py"
    cmd = [
        "docker",
        "run",
        "--rm",
        "--cpus",
        "1",
        "--memory",
        "512m",
        "-v",
        f"{file_path}:{container_strategy_path}:ro",
        image,
        "python",
        str(container_strategy_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)  # nosec B603
    return proc.stdout + proc.stderr

