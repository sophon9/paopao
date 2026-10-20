"""SQLite storage for generated questions and papers.

A question row can be attached to only one paper. That is what keeps
later quizzes from repeating items the student has already seen.
"""

import os
import sqlite3
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent / "quiz.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY,
  fingerprint TEXT NOT NULL UNIQUE,
  subject TEXT NOT NULL,
  topic TEXT NOT NULL,
  difficulty TEXT NOT NULL,
  skill TEXT NOT NULL,
  stem TEXT NOT NULL,
  passage TEXT,
  group_key TEXT,
  choices_json TEXT NOT NULL,
  answer_index INTEGER NOT NULL,
  explanation TEXT NOT NULL,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS papers (
  id INTEGER PRIMARY KEY,
  mode TEXT NOT NULL,
  label TEXT NOT NULL,
  subject TEXT,
  topic TEXT,
  created_at INTEGER NOT NULL,
  submitted_at INTEGER,
  auto_submit INTEGER NOT NULL DEFAULT 0,
  percent INTEGER,
  correct INTEGER,
  wrong INTEGER,
  blank INTEGER,
  total INTEGER,
  used_sec INTEGER
);

CREATE TABLE IF NOT EXISTS paper_items (
  paper_id INTEGER NOT NULL,
  position INTEGER NOT NULL,
  question_id INTEGER NOT NULL UNIQUE,
  choices_json TEXT NOT NULL,
  answer_index INTEGER NOT NULL,
  chosen INTEGER,
  PRIMARY KEY (paper_id, position),
  FOREIGN KEY (paper_id) REFERENCES papers(id),
  FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE IF NOT EXISTS paper_topics (
  paper_id INTEGER NOT NULL,
  subject TEXT NOT NULL,
  topic TEXT NOT NULL,
  correct INTEGER NOT NULL,
  total INTEGER NOT NULL,
  PRIMARY KEY (paper_id, subject, topic),
  FOREIGN KEY (paper_id) REFERENCES papers(id)
);
"""


def db_path():
    override = os.environ.get("QUIZ_DB")
    return Path(override) if override else DEFAULT_PATH


def connect():
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript(SCHEMA)
    return conn


def fingerprint_exists(conn, fingerprint):
    row = conn.execute(
        "SELECT 1 FROM questions WHERE fingerprint = ?",
        (fingerprint,),
    ).fetchone()
    return row is not None
