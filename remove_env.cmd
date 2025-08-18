@echo off
rem remove_env.cmd v0.1.0

pip uninstall -r "%~dp0requirements.txt" -y
