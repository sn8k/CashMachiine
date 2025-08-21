@echo off
rem remove_full.cmd v0.1.10 (2025-08-21)

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

if defined CONFIG_FILE (
  if exist "%CONFIG_FILE%" (
    for /f "usebackq tokens=1* delims==" %%A in ("%CONFIG_FILE%") do set "%%A=%%B"
  ) else (
    echo Config file %CONFIG_FILE% not found.
    exit /b 1
  )
)

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
set "PSQL_CMD=psql"
where psql >nul 2>nul
if %ERRORLEVEL% neq 0 (
  set "PSQL_CMD=docker exec -e PGPASSWORD=%DB_PASS% -i cashmachiine-timescaledb psql"
) else (
  set PGPASSWORD=%DB_PASS%
  %PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "SELECT 1" >nul 2>&1
  if %ERRORLEVEL% neq 0 set "PSQL_CMD=docker exec -e PGPASSWORD=%DB_PASS% -i cashmachiine-timescaledb psql"
  set PGPASSWORD=
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
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_HOST="Enter database host [%DB_HOST%]: "
if "%DB_HOST%"=="" set DB_HOST=localhost
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_PORT="Enter database port [%DB_PORT%]: "
if "%DB_PORT%"=="" set DB_PORT=5432
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_NAME="Enter database name [%DB_NAME%]: "
if "%DB_NAME%"=="" set DB_NAME=cashmachiine
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_USER="Enter database user [%DB_USER%]: "
if "%DB_USER%"=="" set DB_USER=postgres
if "%SILENT%"=="0" if not defined CONFIG_FILE for /f "usebackq delims=" %%p in (`powershell -Command "$p = Read-Host 'Enter database password' -AsSecureString; $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($p); [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($BSTR)"`) do set DB_PASS=%%p

echo Dropping database %DB_NAME%...
set PGPASSWORD=%DB_PASS%
%PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "DROP DATABASE IF EXISTS %DB_NAME%"
set PGPASSWORD=

echo Removing Python environment...
if exist venv (
  call venv\Scripts\activate
  echo Uninstalling Python dependencies...
  pip uninstall -r "%~dp0requirements.txt" -y
  deactivate
  rmdir /s /q venv
) else (
  echo venv not found. Attempting global uninstall.
  pip uninstall -r "%~dp0requirements.txt" -y
)

where docker >nul 2>nul
if %ERRORLEVEL%==0 (
  docker compose down 2>nul || docker-compose down
  docker rm -f cashmachiine-timescaledb >nul 2>&1
) else (
  echo Docker not found, skipping container stop.
)

echo Removing UI dependencies and build artifacts...
if exist ui (
  pushd ui
  if exist node_modules rmdir /s /q node_modules
  if exist .next rmdir /s /q .next
  popd
)

if exist .env (
  echo Clearing service credentials from .env...
  powershell -Command ^
    "$envpath='.env'; $vars = 'DB_HOST','DB_PORT','DB_NAME','DB_USER','DB_PASS','RABBITMQ_URL','API_GATEWAY_URL','ALPHA_VANTAGE_KEY','BINANCE_API_KEY','BINANCE_API_SECRET','IBKR_API_KEY','FRED_API_KEY'; $content = Get-Content $envpath; foreach($k in $vars){$pattern = '^' + [regex]::Escape($k) + '='; if($content -match $pattern){$content = $content -replace $pattern + '.*', $k + '='}}; Set-Content $envpath $content"
)

echo Removal complete.
