@echo off
rem setup_full.cmd v0.1.26 (2025-08-22)

echo Checking for administrator privileges...
net session >nul 2>&1 || (echo Administrator privileges required. Please run as administrator & exit /b 1)

call tools\log_create_win.cmd
set LOG_FILE=logs\setup\setup_full.log
call :main %* > "%LOG_FILE%" 2>&1
exit /b %ERRORLEVEL%

:main
setlocal
set "EXIT_CODE=0"
set "ERROR_MSG="

set "SILENT=0"
set "CONFIG_FILE="
set "RUN_SEEDS=N"

:parse_args
if "%~1"=="" goto after_parse
if /I "%~1"=="--silent" set "SILENT=1"
if /I "%~1"=="--config" (
  shift
  set "CONFIG_FILE=%~1"
)
if /I "%~1"=="--seed" set "RUN_SEEDS=Y"
shift
goto parse_args
:after_parse

set "DB_HOST=localhost"
set "DB_PORT=5432"
set "DB_NAME=cashmachiine"
set "DB_USER=postgres"
set "DB_PASS="
set "DB_SCHEMA_VERSION=v0.1.7"
set "RABBITMQ_URL=amqp://guest:guest@localhost:5672/"
set "API_GATEWAY_URL=http://localhost:8000"
set "ALPHA_VANTAGE_KEY=demo"
set "BINANCE_API_KEY=demo"
set "BINANCE_API_SECRET=demo"
set "IBKR_API_KEY=demo"
set "FRED_API_KEY=demo"

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
where choco >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Chocolatey not found. Please install it from https://chocolatey.org/install and rerun this script.
  exit /b 1
)
where powershell >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo PowerShell not found. Installing PowerShell via Chocolatey...
  choco install powershell -y
  where powershell >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo PowerShell installation failed.
    exit /b 1
  )
  echo PowerShell installed.
)
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Python not found. Installing Python via Chocolatey...
  choco install python -y
  where python >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Python installation failed.
    exit /b 1
  )
  echo Python installed.
)
where pip >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo pip not found. Installing pip via Chocolatey...
  choco install pip -y
  where pip >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo pip installation failed.
    exit /b 1
  )
  echo pip installed.
)
where php >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo PHP not found. Installing PHP via Chocolatey...
  choco install php -y
  where php >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo PHP installation failed.
    exit /b 1
  )
  echo PHP installed.
)
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Node.js not found. Installing Node.js via Chocolatey...
  choco install nodejs -y
  where node >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Node.js installation failed.
    exit /b 1
  )
  echo Node.js installed.
)
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo npm not found. Installing Node.js via Chocolatey...
  choco install nodejs -y
  where npm >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo npm installation failed.
    exit /b 1
  )
  echo npm installed.
)
set "USE_DOCKER_DB=0"
set "PSQL_CMD=psql"
where psql >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo psql not found. Installing PostgreSQL via Chocolatey...
  choco install postgresql -y
  where psql >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo PostgreSQL installation failed. A TimescaleDB container will be started.
    set "USE_DOCKER_DB=1"
  ) else (
    echo PostgreSQL installed.
  )
)
where pg_dump >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo pg_dump not found. Installing PostgreSQL via Chocolatey...
  choco install postgresql -y
  where pg_dump >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo PostgreSQL installation failed. A TimescaleDB container will be started.
    set "USE_DOCKER_DB=1"
  ) else (
    echo PostgreSQL installed.
  )
)
if "%USE_DOCKER_DB%"=="0" (
  set PGPASSWORD=%DB_PASS%
  %PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "SELECT 1" >nul 2>&1
  if %ERRORLEVEL% neq 0 set "USE_DOCKER_DB=1"
  set PGPASSWORD=
)
if "%USE_DOCKER_DB%"=="1" (
  where docker >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Docker not found. Installing Docker Desktop via Chocolatey...
    choco install docker-desktop -y
    where docker >nul 2>nul
    if %ERRORLEVEL% neq 0 (
      echo Docker installation failed.
      exit /b 1
    )
    echo Docker installed.
  )
  docker run -d --name cashmachiine-timescaledb -e POSTGRES_USER=%DB_USER% -e POSTGRES_PASSWORD=%DB_PASS% -e POSTGRES_DB=%DB_NAME% -p %DB_PORT%:5432 timescale/timescaledb
  if %ERRORLEVEL% neq 0 (
    echo Failed to start TimescaleDB container.
    exit /b 1
  )
  set "PSQL_CMD=docker exec -e PGPASSWORD=%DB_PASS% -i cashmachiine-timescaledb psql"
  set "DB_HOST=localhost"
)
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Docker not found. Installing Docker Desktop via Chocolatey...
  choco install docker-desktop -y
  where docker >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Docker installation failed.
    exit /b 1
  )
  echo Docker installed.
)
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Node.js not found. Installing Node.js via Chocolatey...
  choco install nodejs -y
  where node >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Node.js installation failed.
    exit /b 1
  )
  echo Node.js installed.
)

if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_HOST="Enter database host [%DB_HOST%]: "
if "%DB_HOST%"=="" set "DB_HOST=localhost"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_PORT="Enter database port [%DB_PORT%]: "
if "%DB_PORT%"=="" set "DB_PORT=5432"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_NAME="Enter database name [%DB_NAME%]: "
if "%DB_NAME%"=="" set "DB_NAME=cashmachiine"
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p DB_USER="Enter database user [%DB_USER%]: "
if "%DB_USER%"=="" set "DB_USER=postgres"
if "%SILENT%"=="0" if not defined CONFIG_FILE for /f "usebackq delims=" %%p in (`powershell -Command "$p = Read-Host -Prompt 'Enter database password' -AsSecureString; $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($p); [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)"`) do set DB_PASS=%%p
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
if "%SILENT%"=="0" if not defined CONFIG_FILE set /p RUN_SEEDS="Execute database seeds (db\\seeds\\*.sql)? [y/N]: "

%PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='%DB_USER%';" | findstr 1 >nul || %PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U postgres -c "CREATE ROLE %DB_USER% WITH LOGIN PASSWORD '%DB_PASS%';"

if not exist .env (
  echo Creating .env from sample...
  copy .env.example .env >nul
)

echo Updating .env with provided values...
powershell -Command ^
  "$envpath='.env';" ^
  "$vars = @{'DB_HOST'='%DB_HOST%'; 'DB_PORT'='%DB_PORT%'; 'DB_NAME'='%DB_NAME%'; 'DB_USER'='%DB_USER%'; 'DB_PASS'='%DB_PASS%'; 'DB_SCHEMA_VERSION'='%DB_SCHEMA_VERSION%'; 'RABBITMQ_URL'='%RABBITMQ_URL%'; 'API_GATEWAY_URL'='%API_GATEWAY_URL%'; 'ALPHA_VANTAGE_KEY'='%ALPHA_VANTAGE_KEY%'; 'BINANCE_API_KEY'='%BINANCE_API_KEY%'; 'BINANCE_API_SECRET'='%BINANCE_API_SECRET%'; 'IBKR_API_KEY'='%IBKR_API_KEY%'; 'FRED_API_KEY'='%FRED_API_KEY%'};" ^
  "if(!(Test-Path $envpath)){New-Item $envpath -ItemType File | Out-Null};" ^
  "$content = Get-Content $envpath;" ^
  "foreach($k in $vars.Keys){$pattern = '^' + [regex]::Escape($k) + '='; $replacement = \"$k=$($vars[$k])\"; if($content -match $pattern){$content = $content -replace $pattern + '.*', $replacement} else {$content += $replacement}};" ^
  "Set-Content $envpath $content"

echo Creating Python virtual environment...
if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r "%~dp0requirements.txt"
if %ERRORLEVEL% neq 0 (
  set "ERROR_MSG=Python dependency installation failed."
  goto cleanup
)

echo Creating and migrating database...
set PGPASSWORD=
%PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='%DB_NAME%';" | findstr 1 >nul || %PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U postgres -c "CREATE DATABASE %DB_NAME%"
%PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %DB_USER%;"
set PGPASSWORD=%DB_PASS%
%PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
mkdir "%~dp0backups" 2>nul
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% %DB_NAME% > backups\%DB_NAME%_%DATE:~-4%%DATE:~4,2%%DATE:~7,2%.sql
for %%f in (db\migrations\*.sql) do (
  echo Applying %%f
  %PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %%f
  if %ERRORLEVEL% neq 0 (
    set "ERROR_MSG=Database migration failed (%%f)."
    goto cleanup
  )
)
for %%f in (db\migrations\warehouse\*.sql) do (
  echo Applying %%f
  %PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %%f
  if %ERRORLEVEL% neq 0 (
    set "ERROR_MSG=Warehouse migration failed (%%f)."
    goto cleanup
  )
)
if /I "%RUN_SEEDS%"=="Y" (
  echo Executing seed files...
  for %%f in (db\seeds\*.sql) do (
    echo Applying %%f
    %PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f %%f
    if %ERRORLEVEL% neq 0 (
      set "ERROR_MSG=Seed execution failed (%%f)."
      goto cleanup
    )
  )
)
set PGPASSWORD=

echo Verifying database schema...
php admin\db_check.php
if %ERRORLEVEL% neq 0 (
  set "ERROR_MSG=Database verification failed."
  goto cleanup
)

echo Installing UI dependencies and building...
pushd ui
call npm install
if %ERRORLEVEL% neq 0 (
  popd
  set "ERROR_MSG=UI dependency installation failed."
  goto cleanup
)
call npm run build
if %ERRORLEVEL% neq 0 (
  popd
  set "ERROR_MSG=UI build failed."
  goto cleanup
)
popd

echo Starting services with Docker...
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Docker not found. Installing Docker Desktop via Chocolatey...
  choco install docker-desktop -y
  where docker >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Docker installation failed.
  ) else (
    echo Docker installed.
  )
)
if %ERRORLEVEL%==0 (
  docker compose up -d 2>nul || docker-compose up -d
  if %ERRORLEVEL% neq 0 (
    set "ERROR_MSG=Docker startup failed."
    goto cleanup
  )
  powershell -NoProfile -Command "$timeout=120;$interval=5;$elapsed=0;while($elapsed -lt $timeout){$ps=(docker compose ps --format '{{.Service}} {{.State}}' 2>$null);if($LASTEXITCODE -ne 0){$ps=(docker-compose ps --format '{{.Service}} {{.State}}' 2>$null)};if($ps -match 'unhealthy|exited'){exit 1};if($ps -notmatch 'healthy'){Start-Sleep -Seconds $interval;$elapsed+=$interval}else{exit 0}};exit 1"
  if %ERRORLEVEL% neq 0 (
    set "ERROR_MSG=Container health check failed."
    goto cleanup
  )
) else (
  echo Docker not found, skipping container start.
)

echo Setup complete.
goto end

:cleanup
echo Setup failed: %ERROR_MSG%
if exist "%LOG_FILE%" echo ERROR: %ERROR_MSG%>>"%LOG_FILE%"
set PGPASSWORD=%DB_PASS%
%PSQL_CMD% -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -c "DROP DATABASE IF EXISTS %DB_NAME%" >nul 2>&1
set PGPASSWORD=
if exist venv (
  call venv\Scripts\activate
  pip uninstall -r "%~dp0requirements.txt" -y >nul 2>&1
  deactivate
  rmdir /s /q venv
)
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Docker not found. Installing Docker Desktop via Chocolatey for cleanup...
  choco install docker-desktop -y
  where docker >nul 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Docker installation failed.
  ) else (
    echo Docker installed.
  )
)
if %ERRORLEVEL%==0 (
  docker compose down 2>nul || docker-compose down 2>nul
  docker rm -f cashmachiine-timescaledb >nul 2>&1
) else (
  echo Docker not found, skipping container stop.
)
if exist ui\node_modules rmdir /s /q ui\node_modules
if exist ui\.next rmdir /s /q ui\.next
set "EXIT_CODE=1"

:end
endlocal
exit /b %EXIT_CODE%

