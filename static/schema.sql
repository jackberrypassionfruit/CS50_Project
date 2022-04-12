CREATE TABLE users (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE math_activities (
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    id INTEGER NOT NULL,
    correct INTEGER NOT NULL DEFAULT 0,
    attempted INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

