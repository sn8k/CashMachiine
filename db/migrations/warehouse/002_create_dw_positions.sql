-- 002_create_dw_positions.sql v0.1.0 (2025-08-19)
CREATE TABLE IF NOT EXISTS warehouse.dw_positions (
    id BIGINT PRIMARY KEY,
    account_id BIGINT,
    symbol TEXT,
    qty NUMERIC,
    updated_at TIMESTAMP
);
