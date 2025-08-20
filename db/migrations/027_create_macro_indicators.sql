-- 027_create_macro_indicators.sql v0.1.0 (2025-08-20)
CREATE TABLE IF NOT EXISTS macro_indicators (
    id SERIAL PRIMARY KEY,
    indicator TEXT NOT NULL,
    source TEXT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    ts TIMESTAMPTZ NOT NULL
);
