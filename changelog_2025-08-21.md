# Changelog v0.6.81

## 2025-08-21
- `setup_full.cmd` now detects missing `psql` or TimescaleDB and launches a `timescale/timescaledb` container with the provided credentials.
- `remove_full.cmd` stops and removes this TimescaleDB container during cleanup.
- Documented container usage in the user manual and bumped script and documentation versions.
- Setup scripts now wait for Docker containers to become healthy and roll back on failure.
