-- prices table migration v0.1.0
CREATE TABLE IF NOT EXISTS prices (
    symbol TEXT NOT NULL,
    venue TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    o NUMERIC,
    h NUMERIC,
    l NUMERIC,
    c NUMERIC,
    v NUMERIC,
    PRIMARY KEY(symbol, venue, ts)
);
