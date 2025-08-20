@echo off
REM run_perf.cmd v0.1.0 (2025-08-20)
IF "%1"=="--install" (
    pip install locust
    GOTO :EOF
)
IF "%1"=="--remove" (
    pip uninstall -y locust
    GOTO :EOF
)
IF "%RUN_TIME%"=="" (
    set RUN_TIME=1m
)
if not exist perf\reports mkdir perf\reports
locust -f tests\perf\locust_api_gateway.py --headless -u 10 -r 2 -t %RUN_TIME% --csv perf\reports\api_gateway --html perf\reports\api_gateway.html
locust -f tests\perf\locust_strategy_engine.py --headless -u 10 -r 2 -t %RUN_TIME% --csv perf\reports\strategy_engine --html perf\reports\strategy_engine.html
