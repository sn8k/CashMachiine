-- actions table migration v0.1.0
CREATE TABLE IF NOT EXISTS actions (
    id SERIAL PRIMARY KEY,
    goal_id INTEGER REFERENCES goals(id),
    day DATE,
    title TEXT NOT NULL,
    details_json JSONB,
    status TEXT CHECK (status IN ('pending','done','ignored')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
