-- executions table migration v0.1.0
CREATE TABLE IF NOT EXISTS executions (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    price NUMERIC,
    qty NUMERIC,
    fee NUMERIC,
    ts TIMESTAMPTZ
);
