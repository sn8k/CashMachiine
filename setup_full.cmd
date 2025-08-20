@echo off
rem setup_full.cmd v0.1.2 (2025-08-20)

echo CashMachiine full interactive setup

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

echo Installing Python dependencies...
pip install -r "%~dp0requirements.txt"

if not exist .env (
  echo Creating .env from sample...
  copy .env.example .env >nul
)

echo Creating and migrating database...
set PGPASSWORD=%DB_PASS%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -tc "SELECT 1 FROM pg_database WHERE datname='%DB_NAME%';" | findstr 1 >nul || psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "CREATE DATABASE %DB_NAME%"
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
for %%f in (db\migrations\*.sql) do (
  echo Applying %%f
  psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %%f
)
set PGPASSWORD=

echo Starting services with Docker...
where docker >nul 2>nul
if %ERRORLEVEL%==0 (
  docker compose up -d 2>nul || docker-compose up -d
) else (
  echo Docker not found, skipping container start.
)

echo Setup complete.
