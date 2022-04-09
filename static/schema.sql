CREATE TABLE users (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    tot_points INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY(id)
);

CREATE TABLE math_activities (
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    points INTEGER NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id)
);

