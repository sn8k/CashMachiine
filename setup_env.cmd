@echo off
rem setup_env.cmd v0.2.0

pip install -r "%~dp0requirements.txt"

if not exist .env if exist .env.example copy .env.example .env
