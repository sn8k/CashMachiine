-- portfolios table migration v0.1.0
CREATE TABLE IF NOT EXISTS portfolios (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    goal_id INTEGER REFERENCES goals(id),
    name TEXT NOT NULL
);
