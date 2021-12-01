-- Table: adepts
-- DROP TABLE adepts;

CREATE TABLE adepts
(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Table: themes
-- DROP TABLE themes;

CREATE TABLE themes
(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    adept_id integer NOT NULL,
    trust_level integer NOT NULL,
    FOREIGN KEY (adept_id) REFERENCES adepts(id)
);

-- Table: questions
-- DROP TABLE questions;

CREATE TABLE questions
(
    id INTEGER PRIMARY KEY,
    theme_id integer,
    name TEXT NOT NULL
);

-- Table: answers
-- DROP TABLE answers;

CREATE TABLE answers
(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Table: connections
-- DROP TABLE connections;

CREATE TABLE connections
(
    id INTEGER PRIMARY KEY,
    prev_question_id integer NOT NULL,
    answer_id integer,
    next_question_id integer,
    FOREIGN KEY (prev_question_id) REFERENCES questions(id)
);

-- Table: checkpoints
-- DROP TABLE checkpoints;

CREATE TABLE checkpoints
(
    id INTEGER PRIMARY KEY,
    connection_id INTEGER NOT NULL,
    user_id integer NOT NULL,
    solved boolean NOT NULL CHECK (solved IN (0, 1)) DEFAULT 0,
    finished boolean NOT NULL CHECK (solved IN (0, 1)) DEFAULT 0,
    FOREIGN KEY (connection_id) REFERENCES connections(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table: suggestion
-- DROP TABLE suggestions;

CREATE TABLE suggestions
(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    user_id integer NOT NULL
);

CREATE TABLE users
(
    id INTEGER PRIMARY KEY,
    coin integer NOT NULL DEFAULT 100 CHECK(coin >= 0),
    energy integer NOT NULL DEFAULT 200 CHECK(energy >= 0),
    rank integer NOT NULL DEFAULT 1 CHECK(rank > 0)
);

CREATE TABLE trust
(
    id INTEGER PRIMARY KEY,
    user_id integer NOT NULL,
    adept_id integer NOT NULL,
    trust_level integer NOT NULL,
    points integer NOT NULL
);

