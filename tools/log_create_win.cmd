@echo off
REM log directory creator v0.6.15 (2025-08-19)
mkdir logs 2>nul
mkdir logs\containers 2>nul
mkdir logs\analytics 2>nul
mkdir backtester\reports 2>nul
mkdir tests\e2e\reports 2>nul
mkdir ui\.next 2>nul
mkdir perf 2>nul
mkdir execution-engine\logs 2>nul
mkdir logs\notification-service 2>nul
mkdir logs\strategy-marketplace 2>nul
mkdir logs\mobile 2>nul
mkdir strategy-engine\models 2>nul
mkdir strategy-marketplace\assets 2>nul
mkdir backups 2>nul
type nul > logs\orchestrator.log
type nul > logs\data-ingestion.log
type nul > logs\strategy-engine.log
type nul > logs\risk-engine.log
type nul > logs\execution-engine.log
type nul > logs\messaging.log
type nul > logs\feasibility-calculator.log
type nul > logs\backtester.log
type nul > logs\notification-service\notification.log
type nul > logs\strategy-marketplace\marketplace.log
type nul > execution-engine\logs\orders.log
type nul > logs\mobile\build.log
