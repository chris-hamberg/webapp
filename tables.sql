PRAGMA foreign_keys=on;

CREATE TABLE IF NOT EXISTS category (
name TEXT NOT NULL,
PRIMARY KEY(name)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS subject (
name TEXT NOT NULL,
category TEXT NOT NULL,
FOREIGN KEY(category) REFERENCES category(name),
PRIMARY KEY(name)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS theorem (
name TEXT NOT NULL,
url TEXT NOT NULL,
subject TEXT NOT NULL,
FOREIGN KEY(subject) REFERENCES subject(name)
);

CREATE TABLE IF NOT EXISTS plot (
name TEXT NOT NULL,
url TEXT NOT NULL,
subject TEXT NOT NULL,
FOREIGN KEY(subject) REFERENCES subject(name)
);

CREATE TABLE IF NOT EXISTS application (
name TEXT NOT NULL,
url TEXT NOT NULL,
category TEXT NOT NULL,
FOREIGN KEY(category) REFERENCES category(name)
);

CREATE TABLE IF NOT EXISTS users (
email TEXT NOT NULL,
salt TEXT NOT NULL,
hash TEXT NOT NULL,
username TEXT,
api_key TEXT,
api_secret TEXT,
access_token TEXT,
token_secret TEXT,
PRIMARY KEY(email)
) WITHOUT ROWID;
