"""SQLite storage for questions, sessions (papers), answers and the profile.

The database lives in ``backend/tutor.db`` (override with ``TUTOR_DB``).
On first start, history from the old ``quiz.db`` is copied in (see
``backend.migrate``) so earlier practice still counts.

Every attempt is a row in ``paper_items``. Mastery, readiness and the
mistake notebook are all computed from these rows, so there is one source
of truth.
"""

import os
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_PATH = HERE / "tutor.db"
LEGACY_PATH = HERE / "quiz.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY,
  fingerprint TEXT NOT NULL UNIQUE,
  subject TEXT NOT NULL,
  topic TEXT NOT NULL,
  skill TEXT NOT NULL,
  difficulty TEXT NOT NULL,
  template TEXT,
  stem TEXT NOT NULL,
  passage TEXT,
  figure TEXT,
  table_json TEXT,
  choices_json TEXT NOT NULL,
  answer_index INTEGER NOT NULL,
  why_json TEXT NOT NULL DEFAULT '{}',
  hint TEXT NOT NULL DEFAULT '',
  steps_json TEXT NOT NULL DEFAULT '[]',
  group_key TEXT,
  legacy INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_questions_skill ON questions(skill);

CREATE TABLE IF NOT EXISTS papers (
  id INTEGER PRIMARY KEY,
  mode TEXT NOT NULL,              -- mock | diagnostic | adaptive | skill | review | legacy
  subject TEXT,                    -- math | english | NULL (both)
  label TEXT NOT NULL,
  focus TEXT,                      -- topic or skill key for focused practice
  tutor INTEGER NOT NULL DEFAULT 0,-- 1 = instant feedback after each answer
  seconds_limit INTEGER,
  created_at INTEGER NOT NULL,
  submitted_at INTEGER,
  auto_submit INTEGER NOT NULL DEFAULT 0,
  used_sec INTEGER,
  correct INTEGER, wrong INTEGER, blank INTEGER, total INTEGER, percent INTEGER,
  legacy INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_papers_submitted ON papers(submitted_at);

CREATE TABLE IF NOT EXISTS paper_items (
  paper_id INTEGER NOT NULL,
  position INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  chosen INTEGER,
  time_ms INTEGER,
  hint_used INTEGER NOT NULL DEFAULT 0,
  flagged INTEGER NOT NULL DEFAULT 0,
  answered_at INTEGER,             -- set when the answer is final (tutor mode or on submit)
  PRIMARY KEY (paper_id, position),
  FOREIGN KEY (paper_id) REFERENCES papers(id),
  FOREIGN KEY (question_id) REFERENCES questions(id)
);
CREATE INDEX IF NOT EXISTS idx_items_question ON paper_items(question_id);

CREATE TABLE IF NOT EXISTS profile (
  key TEXT PRIMARY KEY,
  value TEXT
);
"""


def db_path():
    override = os.environ.get("TUTOR_DB")
    return Path(override) if override else DEFAULT_PATH


def connect():
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fresh = not path.exists()
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript(SCHEMA)
    if fresh and not os.environ.get("TUTOR_DB") and LEGACY_PATH.exists():
        from backend.migrate import migrate_legacy

        migrate_legacy(conn, LEGACY_PATH)
    return conn


def get_profile(conn):
    return {row["key"]: row["value"] for row in conn.execute("SELECT key, value FROM profile")}


def set_profile(conn, values):
    for k, v in values.items():
        conn.execute("INSERT INTO profile(key, value) VALUES(?, ?) "
                     "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (k, None if v is None else str(v)))
