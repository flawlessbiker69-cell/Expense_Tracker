import sqlite3

import pytest

from database import db


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))


def count(table):
    conn = db.get_db()
    try:
        return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    finally:
        conn.close()


def test_init_creates_tables():
    db.init_db()
    conn = db.get_db()
    names = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert {"users", "expenses"} <= names


def test_init_and_seed_idempotent():
    for _ in range(2):
        db.init_db()
        db.seed_db()
    assert count("users") == 1
    assert count("expenses") == 8


def test_foreign_keys_enforced():
    db.init_db()
    conn = db.get_db()
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date) VALUES (999, 1, 'Food', '2026-01-01')"
        )
    conn.close()


def test_duplicate_email_rejected():
    db.init_db()
    db.seed_db()
    conn = db.get_db()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES ('x', 'demo@spendly.example', 'h')"
        )
    conn.close()


def test_seed_password_is_hashed():
    db.init_db()
    db.seed_db()
    conn = db.get_db()
    h = conn.execute("SELECT password_hash FROM users").fetchone()[0]
    conn.close()
    assert h != "demo1234"
