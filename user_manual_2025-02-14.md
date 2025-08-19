# User Manual v0.6.0

Date: 2025-02-14

This document will evolve into a comprehensive encyclopedia for the project.

## Installation
- Run `./setup_env.sh` (Linux/Mac) or `setup_env.cmd` (Windows) to install Python dependencies.
- Use `./remove_env.sh` or `remove_env.cmd` to uninstall these dependencies.
- Each service provides `install.sh` and `remove.sh` scripts.

## Usage
- Authenticate and interact with the API Gateway at `/goals` and `/actions`.
- Start the scheduler with `python orchestrator/main.py`.
- Pass `--install` or `--remove` to service scripts for setup and teardown.

## Architecture
- Services communicate via structured logs, metrics, and traces.
- Review the [README](README.md#6-architecture-technique) for the full technical specification.

## Troubleshooting
- If dependencies are missing, rerun `./setup_env.sh`.
- Verify database connectivity with `php admin/db_check.php`.
- Check service logs under the `logs/` directory for error details.
