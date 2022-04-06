CREATE TABLE users (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    tot_points INTEGER NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE activity_solving_quadratics (
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    points INTEGER NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(id)
);

