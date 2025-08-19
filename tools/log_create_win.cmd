@echo off
REM log directory creator v0.6.7 (2025-08-20)
mkdir logs 2>nul
mkdir logs\containers 2>nul
mkdir logs\analytics 2>nul
mkdir backtester\reports 2>nul
mkdir ui\.next 2>nul
mkdir perf 2>nul
type nul > logs\orchestrator.log
type nul > logs\data-ingestion.log
type nul > logs\strategy-engine.log
type nul > logs\risk-engine.log
type nul > logs\execution-engine.log
type nul > logs\messaging.log
type nul > logs\feasibility-calculator.log
