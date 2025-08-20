@echo off
rem setup_full.cmd v0.1.7 (2025-08-20)

if not exist logs mkdir logs
set LOG_FILE=logs\setup_full.log
call :main %* > "%LOG_FILE%" 2>&1
exit /b %ERRORLEVEL%

:main
setlocal
call tools\log_create_win.cmd

set "SILENT=0"
set "CONFIG_FILE="

:parse_args
if "%~1"=="" goto after_parse
if /I "%~1"=="--silent" set "SILENT=1"
if /I "%~1"=="--config" (
  shift
  set "CONFIG_FILE=%~1"
)
shift
goto parse_args
:after_parse

set "DB_HOST=localhost"
set "DB_PORT=5432"
set "DB_NAME=cashmachiine"
set "DB_USER=postgres"
set "DB_PASS="
set "RABBITMQ_URL=amqp://guest:guest@localhost:5672/"
set "API_GATEWAY_URL=http://localhost:8000"
set "ALPHA_VANTAGE_KEY=demo"
set "BINANCE_API_KEY=demo"
set "BINANCE_API_SECRET=demo"
set "IBKR_API_KEY=demo"
set "FRED_API_KEY=demo"
set "LOAD_DEMO=N"

if defined CONFIG_FILE (
  if exist "%CONFIG_FILE%" (
    for /f "usebackq tokens=1* delims==" %%A in ("%CONFIG_FILE%") do set "%%A=%%B"
  ) else (
    echo Config file %CONFIG_FILE% not found.
    exit /b 1
  )
)

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

if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_HOST="Enter database host [%DB_HOST%]: "
if "%DB_HOST%"=="" set "DB_HOST=localhost"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_PORT="Enter database port [%DB_PORT%]: "
if "%DB_PORT%"=="" set "DB_PORT=5432"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_NAME="Enter database name [%DB_NAME%]: "
if "%DB_NAME%"=="" set "DB_NAME=cashmachiine"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_USER="Enter database user [%DB_USER%]: "
if "%DB_USER%"=="" set "DB_USER=postgres"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_PASS="Enter database password: "
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p RABBITMQ_URL="Enter RabbitMQ URL [%RABBITMQ_URL%]: "
if "%RABBITMQ_URL%"=="" set "RABBITMQ_URL=amqp://guest:guest@localhost:5672/"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p API_GATEWAY_URL="Enter API Gateway URL [%API_GATEWAY_URL%]: "
if "%API_GATEWAY_URL%"=="" set "API_GATEWAY_URL=http://localhost:8000"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p ALPHA_VANTAGE_KEY="Enter Alpha Vantage API key [%ALPHA_VANTAGE_KEY%]: "
if "%ALPHA_VANTAGE_KEY%"=="" set "ALPHA_VANTAGE_KEY=demo"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p BINANCE_API_KEY="Enter Binance API key [%BINANCE_API_KEY%]: "
if "%BINANCE_API_KEY%"=="" set "BINANCE_API_KEY=demo"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p BINANCE_API_SECRET="Enter Binance API secret [%BINANCE_API_SECRET%]: "
if "%BINANCE_API_SECRET%"=="" set "BINANCE_API_SECRET=demo"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p IBKR_API_KEY="Enter IBKR API key [%IBKR_API_KEY%]: "
if "%IBKR_API_KEY%"=="" set "IBKR_API_KEY=demo"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p FRED_API_KEY="Enter FRED API key [%FRED_API_KEY%]: "
if "%FRED_API_KEY%"=="" set "FRED_API_KEY=demo"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p LOAD_DEMO="Load demonstration data (db\\seeds\\*.sql)? [y/N]: "

echo Creating Python virtual environment...
if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r "%~dp0requirements.txt"

if not exist .env (
  echo Creating .env from sample...
  copy .env.example .env >nul
)

echo Updating .env with provided values...
powershell -Command ^
  "$envpath='.env';" ^
  "$vars = @{'DB_HOST'='%DB_HOST%'; 'DB_PORT'='%DB_PORT%'; 'DB_NAME'='%DB_NAME%'; 'DB_USER'='%DB_USER%'; 'DB_PASS'='%DB_PASS%'; 'RABBITMQ_URL'='%RABBITMQ_URL%'; 'API_GATEWAY_URL'='%API_GATEWAY_URL%'; 'ALPHA_VANTAGE_KEY'='%ALPHA_VANTAGE_KEY%'; 'BINANCE_API_KEY'='%BINANCE_API_KEY%'; 'BINANCE_API_SECRET'='%BINANCE_API_SECRET%'; 'IBKR_API_KEY'='%IBKR_API_KEY%'; 'FRED_API_KEY'='%FRED_API_KEY%'};" ^
  "if(!(Test-Path $envpath)){New-Item $envpath -ItemType File | Out-Null};" ^
  "$content = Get-Content $envpath;" ^
  "foreach($k in $vars.Keys){$pattern = '^' + [regex]::Escape($k) + '='; $replacement = \"$k=$($vars[$k])\"; if($content -match $pattern){$content = $content -replace $pattern + '.*', $replacement} else {$content += $replacement}};" ^
  "Set-Content $envpath $content"

echo Creating and migrating database...
set PGPASSWORD=%DB_PASS%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -tc "SELECT 1 FROM pg_database WHERE datname='%DB_NAME%';" | findstr 1 >nul || psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "CREATE DATABASE %DB_NAME%"
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
for %%f in (db\migrations\*.sql) do (
  echo Applying %%f
  psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %%f
)
if /I "%LOAD_DEMO%"=="Y" (
  echo Inserting demonstration data...
  for %%f in (db\seeds\*.sql) do (
    echo Applying %%f
    psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %%f
  )
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
endlocal
exit /b 0

