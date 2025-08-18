# Changelog v0.5.1

## 2025-08-18
- Added initial development tasks outline.
- Initialized user manual skeleton.
- Created first changelog entry.
- Scaffolded service directories with versioned bootstraps and scripts.
- Added .gitignore for build artifacts and volatile paths.
- Expanded user manual with service overview.
- Added requirements.txt with runtime and development dependencies.
- Introduced setup_env and remove_env scripts for Linux/Mac and Windows.
- Documented installer usage in user manuals.
- Added initial database schema migrations.
- Introduced admin/db_check.php for schema validation.
- Added install_db.sh and remove_db.sh scripts.
- Documented database setup in user manuals.
- Added FastAPI API gateway with JWT auth, role checks, version header, install scripts, tests, and updated requirements.
- Introduced orchestrator scheduler with APScheduler for daily 08:00 Europe/Paris jobs and configurable logging.
- Added log creation scripts for orchestrator logs.
- Updated user manual with scheduling details.
- Added APScheduler dependency to requirements.
- Updated orchestrator install/remove scripts to v0.3.0.
