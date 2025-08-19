@echo off
rem remove_env.cmd v0.1.1

pip uninstall -r "%~dp0requirements.txt" -y

where docker >nul 2>nul
if %ERRORLEVEL%==0 (
  docker compose down 2>nul || docker-compose down
)
