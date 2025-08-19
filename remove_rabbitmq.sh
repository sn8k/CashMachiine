#!/bin/bash
# rabbitmq removal v0.1.0 (2025-08-19)
set -e

docker rm -f rabbitmq 2>/dev/null || true
