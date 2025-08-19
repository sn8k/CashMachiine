#!/bin/bash
# rabbitmq installer v0.1.0 (2025-08-19)
set -e

docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3-alpine
