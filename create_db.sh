#!/bin/sh

sqlite3 data.db <<END_SQL
.timeout 2000
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    group_id TEXT NOT NULL UNIQUE,
    role_id TEXT NOT NULL UNIQUE
);
INSERT INTO users(username, password, group_id, role_id) VALUES('admin', 'changeme', 1, '1');
END_SQL