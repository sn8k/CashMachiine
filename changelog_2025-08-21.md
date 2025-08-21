# Changelog v0.6.83

## 2025-08-21
- `setup_full.cmd` now detects missing `psql` or TimescaleDB and launches a `timescale/timescaledb` container with the provided credentials.
- `remove_full.cmd` stops and removes this TimescaleDB container during cleanup.
- Documented container usage in the user manual and bumped script and documentation versions.
- Replaced plaintext database password prompts with a PowerShell secure input in `setup_full.cmd` and `remove_full.cmd`.
- Setup scripts now wait for Docker containers to become healthy and roll back on failure.
- `setup_full.cmd` now ensures the database role exists and grants it privileges on the target database; `admin/db_check.php` verifies the role and permissions.
