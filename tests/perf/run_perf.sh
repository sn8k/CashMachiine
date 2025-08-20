#!/bin/bash
# run_perf.sh v0.1.0 (2025-08-20)
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
locust -f tests/perf/locust_api_gateway.py --headless -u 10 -r 2 -t $RUN_TIME --csv perf/reports/api_gateway --html perf/reports/api_gateway.html
locust -f tests/perf/locust_strategy_engine.py --headless -u 10 -r 2 -t $RUN_TIME --csv perf/reports/strategy_engine --html perf/reports/strategy_engine.html
