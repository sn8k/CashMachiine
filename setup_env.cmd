@echo off
rem setup_env.cmd v0.2.6 (2025-08-21)

call tools\log_create_win.cmd

pip install -r "%~dp0requirements.txt"

if not exist .env if exist .env.example copy .env.example .env

where docker >nul 2>nul
if %ERRORLEVEL%==0 (
  docker compose up -d 2>nul || docker-compose up -d
  powershell -NoProfile -Command "$timeout=120;$interval=5;$elapsed=0;while($elapsed -lt $timeout){$ps=(docker compose ps --format '{{.Service}} {{.Status}}' 2>$null);if($LASTEXITCODE -ne 0){$ps=(docker-compose ps --format '{{.Service}} {{.Status}}' 2>$null)};Write-Output $ps;if($ps -match 'unhealthy|exited'){exit 1};if($ps -notmatch 'running' -or $ps -match 'starting'){Start-Sleep -Seconds $interval;$elapsed+=$interval}else{exit 0}};exit 1"
  if %ERRORLEVEL% neq 0 (
    docker compose down 2>nul || docker-compose down 2>nul
    exit /b 1
  )
)
