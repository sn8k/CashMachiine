#!/bin/bash
# run_perf.sh v0.1.4 (2025-08-20)
set -e
if [ "$1" = "--install" ]; then
  pip install locust
  exit 0
fi
if [ "$1" = "--remove" ]; then
  pip uninstall -y locust
  exit 0
fi
RUN_TIME=${RUN_TIME:-1m}
mkdir -p perf/reports

export RATE_LIMIT_PER_MINUTE=${RATE_LIMIT_PER_MINUTE:-1000}

# Start API gateway
PYTHONPATH=. uvicorn main:app --app-dir api-gateway --host 127.0.0.1 --port 8000 >/dev/null 2>&1 &
SERVER_PID=$!
trap "kill $SERVER_PID" EXIT
for i in {1..10}; do curl -sf http://127.0.0.1:8000/docs >/dev/null && break; sleep 1; done

locust -f tests/perf/locust_api_gateway.py --headless -u 10 -r 2 -t $RUN_TIME --csv perf/reports/api_gateway --html perf/reports/api_gateway.html

kill $SERVER_PID 2>/dev/null || true
trap - EXIT

# Start risk-engine on separate port
export RISK_ENGINE_URL="http://127.0.0.1:8001"
PYTHONPATH=risk-engine uvicorn api:app --app-dir risk-engine --host 127.0.0.1 --port 8001 >/dev/null 2>&1 &
RISK_PID=$!
trap "kill $RISK_PID" EXIT
for i in {1..10}; do curl -sf http://127.0.0.1:8001/docs >/dev/null && break; sleep 1; done

PYTHONPATH=./strategy-engine locust -f tests/perf/locust_strategy_engine.py --headless -u 10 -r 2 -t $RUN_TIME --csv perf/reports/strategy_engine --html perf/reports/strategy_engine.html

kill $RISK_PID 2>/dev/null || true
trap - EXIT
