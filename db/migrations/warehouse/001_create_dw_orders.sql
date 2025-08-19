-- 001_create_dw_orders.sql v0.1.0 (2025-08-19)
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE TABLE IF NOT EXISTS warehouse.dw_orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    symbol TEXT,
    qty NUMERIC,
    price NUMERIC,
    created_at TIMESTAMP
);
