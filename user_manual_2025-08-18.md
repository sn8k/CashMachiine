# User Manual v0.4.0

Date: 2025-08-18

This document will evolve into a comprehensive encyclopedia for the project.

## Overview
- Goal-based investment platform with daily actionable recommendations.

## Installation
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.

## Database Setup
- Run `./install_db.sh` to create tables.
- Run `./remove_db.sh` to drop tables.
- Verify with `php admin/db_check.php`.

## Usage
- Pending implementation.

## Architecture
- See README for initial specification.


## Services Overview
- api-gateway
- orchestrator
- data-ingestion
- strategy-engine
- risk-engine
- execution-engine
- backtester
- ui
- db
