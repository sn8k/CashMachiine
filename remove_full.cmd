@echo off
rem remove_full.cmd v0.1.3 (2025-08-20)

echo CashMachiine full removal

echo Checking prerequisites...
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Python not found. Please install from https://www.python.org/downloads/
  exit /b 1
)
where pip >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo pip not found. Downloading installer...
  start https://bootstrap.pypa.io/get-pip.py
  exit /b 1
)
where psql >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo PostgreSQL not found. Please install from https://www.postgresql.org/download/
  exit /b 1
)
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Docker not found. Please install from https://www.docker.com/get-started/
  exit /b 1
)
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Node.js not found. Please install from https://nodejs.org/en/download/
  exit /b 1
)

echo.
set /p DB_HOST="Enter database host [localhost]: "
if "%DB_HOST%"=="" set DB_HOST=localhost
set /p DB_PORT="Enter database port [5432]: "
if "%DB_PORT%"=="" set DB_PORT=5432
set /p DB_NAME="Enter database name [cashmachiine]: "
if "%DB_NAME%"=="" set DB_NAME=cashmachiine
set /p DB_USER="Enter database user [postgres]: "
if "%DB_USER%"=="" set DB_USER=postgres
set /p DB_PASS="Enter database password: "

echo Dropping tables...
set PGPASSWORD=%DB_PASS%
for %%T in (actions backtests metrics_daily risk_anomalies risk_limits signals prices executions orders positions portfolios accounts goals users audit_events) do (
  echo Dropping %%T
  psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -c "DROP TABLE IF EXISTS %%T CASCADE;"
)
set PGPASSWORD=

echo Uninstalling Python dependencies...
pip uninstall -r "%~dp0requirements.txt" -y

where docker >nul 2>nul
if %ERRORLEVEL%==0 (
  docker compose down 2>nul || docker-compose down
) else (
  echo Docker not found, skipping container stop.
)

echo Removal complete.
