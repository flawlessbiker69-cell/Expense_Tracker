import os
import sqlite3

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "spendly.db",
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                amount      REAL NOT NULL CHECK (amount > 0),
                category    TEXT NOT NULL,
                description TEXT,
                date        TEXT NOT NULL,
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_expenses_user_date
                ON expenses (user_id, date);
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
            return
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.example", generate_password_hash("demo1234")),
        )
        user_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, description, date)"
            " VALUES (?, ?, ?, ?, ?)",
            [
                (user_id, 12.50, "Food", "Lunch", "2026-09-01"),
                (user_id, 45.00, "Food", "Groceries", "2026-09-03"),
                (user_id, 3.20, "Transport", "Bus fare", "2026-09-04"),
                (user_id, 60.00, "Transport", "Fuel", "2026-09-08"),
                (user_id, 120.00, "Bills", "Electricity", "2026-09-10"),
                (user_id, 25.00, "Health", "Pharmacy", "2026-09-12"),
                (user_id, 79.99, "Shopping", "Shoes", "2026-09-15"),
                (user_id, 15.00, "Other", "Gift", "2026-09-18"),
            ],
        )
        conn.commit()
    finally:
        conn.close()
