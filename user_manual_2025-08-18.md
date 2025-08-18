# User Manual v0.5.0

Date: 2025-08-18

This document will evolve into a comprehensive encyclopedia for the project.

## Overview
- Goal-based investment platform with daily actionable recommendations.

## Installation
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.
- Each service includes install.sh and remove.sh scripts (v0.2.1).

## Database Setup
- Run `./install_db.sh` to create tables.
- Run `./remove_db.sh` to drop tables.
- Verify with `php admin/db_check.php`.

## Usage
- API Gateway exposes `/goals` (user role) and `/actions` (admin role).
- Send JWT tokens with a `role` claim in the `Authorization` header.
- Responses include header `X-API-Version: v0.2.0`.

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
