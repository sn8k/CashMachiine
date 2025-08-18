-- backtests table migration v0.1.0
CREATE TABLE IF NOT EXISTS backtests (
    id SERIAL PRIMARY KEY,
    cfg_json JSONB,
    start DATE,
    end DATE,
    kpis_json JSONB,
    report_path TEXT
);
