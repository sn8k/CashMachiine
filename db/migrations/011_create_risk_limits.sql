-- risk_limits table migration v0.1.0
CREATE TABLE IF NOT EXISTS risk_limits (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios(id),
    max_dd NUMERIC,
    max_var NUMERIC,
    vol_target NUMERIC,
    kelly_cap NUMERIC
);
