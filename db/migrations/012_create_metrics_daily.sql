-- metrics_daily table migration v0.1.0
CREATE TABLE IF NOT EXISTS metrics_daily (
    date DATE,
    portfolio_id INTEGER REFERENCES portfolios(id),
    nav NUMERIC,
    ret NUMERIC,
    vol NUMERIC,
    dd NUMERIC,
    var95 NUMERIC,
    es97 NUMERIC,
    PRIMARY KEY(date, portfolio_id)
);
