"""Build a paper from fresh items and grade it.

Each question id is stored on exactly one paper. Later papers cannot
select it again.
"""

import json
import sqlite3
import time

from backend.db import connect
from backend.generate import (
    ENG_TOPICS,
    MATH_TOPICS,
    TOPICS,
    build_english_items,
    build_math_items,
    build_practice_items,
)

MODE_LABEL = {
    "math": "คณิตศาสตร์",
    "english": "ภาษาอังกฤษ",
    "combined": "สอบรวม",
    "practice": "ฝึก",
}

MODE_SECONDS = {
    "math": 40 * 60,
    "english": 35 * 60,
    "combined": 75 * 60,
}


def _now():
    return int(time.time() * 1000)


def _insert_items(conn, items):
    ids = []
    created = _now()
    for item in items:
        cur = conn.execute(
            """
            INSERT INTO questions (
              fingerprint, subject, topic, difficulty, skill, stem, passage,
              group_key, choices_json, answer_index, explanation, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["fingerprint"],
                item["subject"],
                item["topic"],
                item["difficulty"],
                item["skill"],
                item["stem"],
                item["passage"],
                item["group_key"],
                json.dumps(item["choices"], ensure_ascii=False),
                item["answer_index"],
                item["explanation"],
                created,
            ),
        )
        ids.append(cur.lastrowid)
    return ids


def _public_question(question_id, item_choices, meta):
    return {
        "id": question_id,
        "subject": meta["subject"],
        "topic": meta["topic"],
        "difficulty": meta["difficulty"],
        "stem": meta["stem"],
        "passage": meta["passage"],
        "choices": item_choices,
    }


def _label_for(conn, mode, topic):
    count = conn.execute("SELECT COUNT(*) AS n FROM papers WHERE mode = ?", (mode,)).fetchone()["n"]
    n = count + 1
    if mode == "practice":
        return f"ฝึก {topic} ชุดที่ {n}"
    return f"{MODE_LABEL[mode]} ชุดที่ {n}"


def _assemble(conn, mode, subject, topic, timer):
    batch = set()
    used = set()
    if mode == "math":
        items = build_math_items(conn, batch, used)
        seconds = MODE_SECONDS["math"]
    elif mode == "english":
        items = build_english_items(conn, batch, used)
        seconds = MODE_SECONDS["english"]
    elif mode == "combined":
        items = build_math_items(conn, batch, used) + build_english_items(conn, batch, used)
        seconds = MODE_SECONDS["combined"]
    elif mode == "practice":
        if subject not in TOPICS or topic not in TOPICS[subject]:
            raise ValueError("ไม่พบหัวข้อนี้")
        items = build_practice_items(conn, subject, topic)
        seconds = max(60, round(len(items) * 72)) if timer else None
    else:
        raise ValueError("ไม่รู้จักโหมดสอบ")

    ids = _insert_items(conn, items)
    label = _label_for(conn, mode, topic)
    created = _now()
    cur = conn.execute(
        """
        INSERT INTO papers (mode, label, subject, topic, created_at, total)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (mode, label, subject, topic, created, len(items)),
    )
    paper_id = cur.lastrowid
    public = []
    for position, (question_id, item) in enumerate(zip(ids, items)):
        conn.execute(
            """
            INSERT INTO paper_items (paper_id, position, question_id, choices_json, answer_index)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                paper_id,
                position,
                question_id,
                json.dumps(item["choices"], ensure_ascii=False),
                item["answer_index"],
            ),
        )
        public.append(_public_question(question_id, item["choices"], item))
    return {
        "paperId": paper_id,
        "mode": mode,
        "label": label,
        "seconds": seconds,
        "subject": subject,
        "topic": topic,
        "questions": public,
    }


def create_paper(mode, subject=None, topic=None, timer=True):
    last_error = None
    for _ in range(3):
        conn = connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            payload = _assemble(conn, mode, subject, topic, timer)
            conn.commit()
            return payload
        except sqlite3.IntegrityError as exc:
            conn.rollback()
            last_error = exc
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    raise RuntimeError(f"สร้างชุดข้อสอบไม่สำเร็จ: {last_error}")


def _topic_rows(rows):
    buckets = {}
    for row in rows:
        key = (row["subject"], row["topic"])
        bucket = buckets.setdefault(key, {"subject": row["subject"], "topic": row["topic"], "correct": 0, "total": 0})
        bucket["total"] += 1
        if row["chosen"] is not None and row["chosen"] == row["answer_index"]:
            bucket["correct"] += 1
    out = []
    for bucket in buckets.values():
        bucket["percent"] = round(100 * bucket["correct"] / bucket["total"]) if bucket["total"] else 0
        out.append(bucket)
    out.sort(key=lambda b: (b["percent"], -b["total"]))
    return out


def _choice_label(subject, index, choices):
    letters = ["A", "B", "C", "D"] if subject == "english" else ["ก", "ข", "ค", "ง"]
    letter = letters[index] if 0 <= index < len(letters) else str(index + 1)
    text = choices[index] if 0 <= index < len(choices) else ""
    return f"{letter}. {text}"


def _mistake_explanation(subject, choices, answer_index, chosen, explanation):
    """Explain a wrong or blank item from the choice the student made."""
    correct = _choice_label(subject, answer_index, choices)
    method = (explanation or "").strip()
    if chosen is None:
        return (
            f"ข้อนี้ไม่ได้ตอบ จึงยังไม่ได้ตรวจวิธีคิด\n"
            f"เฉลยที่ถูกคือ {correct}\n"
            f"วิธีคิด: {method}"
        )
    picked = _choice_label(subject, chosen, choices)
    return (
        f"คำตอบที่เลือกคือ {picked} ซึ่งไม่ตรงกับสิ่งที่โจทย์ถาม\n"
        f"เฉลยที่ถูกคือ {correct}\n"
        f"วิธีคิดที่ถูก: {method}"
    )


def _result_from_rows(paper, rows):
    correct = wrong = blank = 0
    questions = []
    for row in rows:
        chosen = row["chosen"]
        choices = json.loads(row["choices_json"])
        if chosen is None:
            blank += 1
            status = "blank"
        elif chosen == row["answer_index"]:
            correct += 1
            status = "ok"
        else:
            wrong += 1
            status = "bad"
        mistake = None
        if status != "ok":
            mistake = _mistake_explanation(
                row["subject"], choices, row["answer_index"], chosen, row["explanation"]
            )
        questions.append(
            {
                "id": row["question_id"],
                "subject": row["subject"],
                "topic": row["topic"],
                "difficulty": row["difficulty"],
                "stem": row["stem"],
                "passage": row["passage"],
                "choices": choices,
                "answerIndex": row["answer_index"],
                "chosen": chosen,
                "status": status,
                "explanation": row["explanation"],
                "mistakeExplanation": mistake,
            }
        )
    total = len(rows)
    percent = round(100 * correct / total) if total else 0
    topics = _topic_rows(rows)
    weak = [t for t in topics if t["percent"] < 80]
    if weak:
        improve = "ควรกลับไปฝึกให้แม่นก่อนสอบจริง: " + ", ".join(t["topic"] for t in weak[:3])
    else:
        improve = "ชุดนี้ถึง 80% ทุกหัวข้อ ลองทำชุดใหม่เพื่อยืนยันกับโจทย์คนละข้อ"
    return {
        "paperId": paper["id"],
        "mode": paper["mode"],
        "label": paper["label"],
        "percent": percent,
        "correct": correct,
        "wrong": wrong,
        "blank": blank,
        "total": total,
        "usedSec": paper["used_sec"] or 0,
        "topics": topics,
        "improve": improve,
        "questions": questions,
        "practiceSubject": paper["subject"],
        "practiceTopic": paper["topic"],
    }


def submit_paper(paper_id, answers, used_sec, auto):
    conn = connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        paper = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
        if paper is None:
            raise ValueError("ไม่พบชุดข้อสอบ")
        rows = conn.execute(
            """
            SELECT pi.position, pi.question_id, pi.choices_json, pi.answer_index, pi.chosen,
                   q.subject, q.topic, q.difficulty, q.stem, q.passage, q.explanation
            FROM paper_items pi
            JOIN questions q ON q.id = pi.question_id
            WHERE pi.paper_id = ?
            ORDER BY pi.position
            """,
            (paper_id,),
        ).fetchall()
        if paper["submitted_at"] is not None:
            conn.rollback()
            return _result_from_rows(paper, rows)

        if not isinstance(answers, list) or len(answers) != len(rows):
            raise ValueError("จำนวนคำตอบไม่ตรงกับข้อสอบ")

        for row, chosen in zip(rows, answers):
            if chosen is None:
                stored = None
            elif isinstance(chosen, int) and 0 <= chosen < 4:
                stored = chosen
            else:
                stored = None
            conn.execute(
                "UPDATE paper_items SET chosen = ? WHERE paper_id = ? AND position = ?",
                (stored, paper_id, row["position"]),
            )

        rows = conn.execute(
            """
            SELECT pi.position, pi.question_id, pi.choices_json, pi.answer_index, pi.chosen,
                   q.subject, q.topic, q.difficulty, q.stem, q.passage, q.explanation
            FROM paper_items pi
            JOIN questions q ON q.id = pi.question_id
            WHERE pi.paper_id = ?
            ORDER BY pi.position
            """,
            (paper_id,),
        ).fetchall()
        topics = _topic_rows(rows)
        correct = sum(1 for row in rows if row["chosen"] is not None and row["chosen"] == row["answer_index"])
        wrong = sum(1 for row in rows if row["chosen"] is not None and row["chosen"] != row["answer_index"])
        blank = sum(1 for row in rows if row["chosen"] is None)
        total = len(rows)
        percent = round(100 * correct / total) if total else 0
        submitted = _now()
        conn.execute(
            """
            UPDATE papers
            SET submitted_at = ?, auto_submit = ?, percent = ?, correct = ?, wrong = ?,
                blank = ?, total = ?, used_sec = ?
            WHERE id = ?
            """,
            (submitted, 1 if auto else 0, percent, correct, wrong, blank, total, int(used_sec or 0), paper_id),
        )
        conn.execute("DELETE FROM paper_topics WHERE paper_id = ?", (paper_id,))
        for topic in topics:
            conn.execute(
                """
                INSERT INTO paper_topics (paper_id, subject, topic, correct, total)
                VALUES (?, ?, ?, ?, ?)
                """,
                (paper_id, topic["subject"], topic["topic"], topic["correct"], topic["total"]),
            )
        conn.commit()
        paper = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
        return _result_from_rows(paper, rows)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _load_rows(conn, paper_id):
    return conn.execute(
        """
        SELECT pi.position, pi.question_id, pi.choices_json, pi.answer_index, pi.chosen,
               q.subject, q.topic, q.difficulty, q.stem, q.passage, q.explanation
        FROM paper_items pi
        JOIN questions q ON q.id = pi.question_id
        WHERE pi.paper_id = ?
        ORDER BY pi.position
        """,
        (paper_id,),
    ).fetchall()


def get_paper(paper_id):
    conn = connect()
    try:
        paper = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
        if paper is None or paper["submitted_at"] is None:
            raise ValueError("ไม่พบประวัติชุดนี้")
        return _result_from_rows(paper, _load_rows(conn, paper_id))
    finally:
        conn.close()


def home_summary():
    conn = connect()
    try:
        history_rows = conn.execute(
            """
            SELECT id, mode, label, submitted_at, percent, correct, wrong, blank, total, used_sec, topic
            FROM papers
            WHERE submitted_at IS NOT NULL
            ORDER BY submitted_at DESC
            LIMIT 30
            """
        ).fetchall()
        history = [
            {
                "at": row["submitted_at"],
                "paperId": row["id"],
                "mode": row["mode"],
                "label": row["label"],
                "percent": row["percent"],
                "correct": row["correct"],
                "wrong": row["wrong"],
                "blank": row["blank"],
                "total": row["total"],
                "usedSec": row["used_sec"],
                "topic": row["topic"],
            }
            for row in history_rows
        ]
        weak_rows = conn.execute(
            """
            SELECT subject, topic, SUM(correct) AS correct, SUM(total) AS total
            FROM paper_topics
            GROUP BY subject, topic
            HAVING total > 0
            ORDER BY (1.0 * SUM(correct) / SUM(total)), SUM(total) DESC
            """
        ).fetchall()
        weak = [
            {
                "subject": row["subject"],
                "topic": row["topic"],
                "correct": row["correct"],
                "total": row["total"],
                "percent": round(100 * row["correct"] / row["total"]),
            }
            for row in weak_rows
        ]
        used = conn.execute("SELECT COUNT(*) AS n FROM paper_items").fetchone()["n"]
        papers = conn.execute("SELECT COUNT(*) AS n FROM papers").fetchone()["n"]
        submitted = conn.execute(
            "SELECT COUNT(*) AS n FROM papers WHERE submitted_at IS NOT NULL"
        ).fetchone()["n"]
        return {
            "history": history,
            "weak": weak,
            "questionsUsed": used,
            "papers": papers,
            "submitted": submitted,
            "topics": {"math": MATH_TOPICS, "english": ENG_TOPICS},
        }
    finally:
        conn.close()
