import os
import sqlite3
from typing import Optional

DB_PATH = os.getenv("DB_PATH", "whoa.db")

def get_conn():
  return sqlite3.connect(DB_PATH)

def init_db():
  with get_conn() as conn:
    c = conn.cursor()
    c.execute("""
      CREATE TABLE IF NOT EXISTS whoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        whoa_reason TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    """)
    conn.commit()

def track_whoa(username: str, reason: str) -> None:
  with get_conn() as conn:
    c = conn.cursor()
    c.execute(
      "INSERT INTO whoas (username, whoa_reason) VALUES (?, ?)",
      (username, reason)
    )
    conn.commit()

def count_whoa(username: str) -> int:
  with get_conn() as conn:
    c = conn.cursor()
    c.execute(
      "SELECT COUNT(*) FROM whoas WHERE username = ?",
      (username,)
    )
    row = c.fetchone()
    return int(row[0]) if row else 0

def last_reason(username: str) -> Optional[str]:
  with get_conn() as conn:
    c = conn.cursor()
    c.execute(
      "SELECT whoa_reason FROM whoas WHERE username = ? ORDER BY id DESC LIMIT 1",
      (username,)
    )
    row = c.fetchone()
    return row[0] if row else None
