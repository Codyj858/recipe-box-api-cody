import sqlite3
from flask import current_app, g



SCHEMA = """
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL DEFAULT '',
    is_public INTEGER NOT NULL DEFAULT 1
    );
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
"""

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = sqlite3.connect(current_app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        g._database = db
    return db


def init_db(app):
    with app.app_context():
        conn = sqlite3.connect(app.config["DATABASE"])
        cur = conn.cursor()
        cur.executescript(SCHEMA)
        conn.commit()
        conn.close()