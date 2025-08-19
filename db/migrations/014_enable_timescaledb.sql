-- enable timescaledb and convert prices to hypertable v0.1.0 (2025-08-19)
CREATE EXTENSION IF NOT EXISTS timescaledb;
SELECT create_hypertable('prices', 'ts', if_not_exists => TRUE);
