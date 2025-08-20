@echo off
rem setup_env.cmd v0.2.4 (2025-08-20)

call tools\log_create_win.cmd

pip install -r "%~dp0requirements.txt"

if not exist .env if exist .env.example copy .env.example .env

where docker >nul 2>nul
if %ERRORLEVEL%==0 (
  docker compose up -d 2>nul || docker-compose up -d
)
