@echo off
REM run_perf.cmd v0.1.3 (2025-08-20)
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
IF "%RATE_LIMIT_PER_MINUTE%"=="" (
    set RATE_LIMIT_PER_MINUTE=1000
)
if not exist perf\reports mkdir perf\reports

start "" /B python -m uvicorn main:app --app-dir api-gateway --host 127.0.0.1 --port 8000 >NUL
timeout /t 3 /nobreak >NUL
locust -f tests\perf\locust_api_gateway.py --headless -u 10 -r 2 -t %RUN_TIME% --csv perf\reports\api_gateway --html perf\reports\api_gateway.html
taskkill /IM python.exe /F >NUL 2>&1

set RISK_ENGINE_URL=http://127.0.0.1:8001
start "" /B python -m uvicorn api:app --app-dir risk-engine --host 127.0.0.1 --port 8001 >NUL
timeout /t 3 /nobreak >NUL
locust -f tests\perf\locust_strategy_engine.py --headless -u 10 -r 2 -t %RUN_TIME% --csv perf\reports\strategy_engine --html perf\reports\strategy_engine.html
taskkill /IM python.exe /F >NUL 2>&1
