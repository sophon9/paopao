"""Create, interact with, and grade practice/exam papers."""

import json
import sqlite3
import time

from backend.bank import SKILLS, TOPICS
from backend.bank.core import MISTAKE_TAGS, run_template, validate_item
from backend.bank.topics import DIAGNOSTIC, MOCK
from backend.db import connect
from backend.tutor import (
    _is_fresh,
    assemble_session_items,
    build_dashboard,
    pick_one,
)


def _now():
    return int(time.time() * 1000)


# Map legacy Thai topic names to new topic keys so legacy callers keep working
LEGACY_NAME_TO_TOPIC = {
    "จำนวนและการดำเนินการ": "m.num",
    "ทศนิยมเศษส่วน": "m.frac",
    "อัตราส่วนร้อยละ": "m.ratio",
    "สมการ": "m.alg",
    "เรขาคณิตพื้นที่ปริมาตร": "m.meas",
    "สถิติโจทย์ปัญหา": "m.data",
    "Grammar/Tenses": "e.gram",
    "Vocabulary": "e.vocab",
    "Conversation": "e.conv",
    "Reading": "e.read",
}


def _normalize_request(mode, subject, topic, focus, tutor, timer, count, difficulty):
    """Support both new modes (mock/diagnostic/adaptive/skill/review) and legacy modes."""
    if mode in ("math", "english"):
        return "mock", mode, None, False, True, count, difficulty
    if mode == "combined":
        return "mock", "combined", None, False, True, count, difficulty
    if mode == "practice":
        fk = focus or topic
        if fk in LEGACY_NAME_TO_TOPIC:
            fk = LEGACY_NAME_TO_TOPIC[fk]
        return "skill", subject, fk, bool(tutor), bool(timer), count or 8, difficulty
    fk = focus or topic
    if fk in LEGACY_NAME_TO_TOPIC:
        fk = LEGACY_NAME_TO_TOPIC[fk]
    return mode, subject, fk, bool(tutor), bool(timer), count, difficulty


def _insert_questions(conn, items):
    ids = []
    created = _now()
    for item in items:
        cur = conn.execute(
            """
            INSERT INTO questions (
              fingerprint, subject, topic, skill, difficulty, template,
              stem, passage, figure, table_json, choices_json, answer_index,
              why_json, hint, steps_json, group_key, legacy, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
            """,
            (
                item["fingerprint"],
                item["subject"],
                item["topic"],
                item["skill"],
                item["difficulty"],
                item.get("template"),
                item["stem"],
                item.get("passage"),
                item.get("figure"),
                json.dumps(item["table"], ensure_ascii=False) if item.get("table") else None,
                json.dumps(item["choices"], ensure_ascii=False),
                item["answer_index"],
                json.dumps(item["why"], ensure_ascii=False),
                item["hint"],
                json.dumps(item["steps"], ensure_ascii=False),
                item.get("group_key"),
                created,
            ),
        )
        ids.append(cur.lastrowid)
    return ids


def _label_for(conn, mode, subject, focus):
    count = conn.execute("SELECT COUNT(*) AS n FROM papers WHERE mode = ?", (mode,)).fetchone()["n"] + 1
    if mode == "mock":
        if subject == "math":
            return f"จำลองสอบ คณิตศาสตร์ ชุดที่ {count}"
        if subject == "english":
            return f"จำลองสอบ ภาษาอังกฤษ ชุดที่ {count}"
        return f"จำลองสอบรวม (คณิต + อังกฤษ) ชุดที่ {count}"
    if mode == "diagnostic":
        s_name = "คณิตศาสตร์" if subject == "math" else "ภาษาอังกฤษ"
        return f"วัดระดับ {s_name} ครั้งที่ {count}"
    if mode == "adaptive":
        s_name = "คณิตศาสตร์" if subject == "math" else ("ภาษาอังกฤษ" if subject == "english" else "รวมวิชา")
        return f"ฝึกปรับระดับ ({s_name}) ชุดที่ {count}"
    if mode == "review":
        return f"ทบทวนจุดที่เคยพลาด ชุดที่ {count}"
    if mode == "skill":
        if focus in SKILLS:
            return f"ฝึกทักษะ: {SKILLS[focus]['name']}"
        if focus in TOPICS:
            return f"ฝึกบท: {TOPICS[focus]['name']}"
    return f"ชุดฝึกที่ {count}"


def _seconds_for(mode, subject, items, timer):
    if not timer:
        return None
    if mode == "mock":
        if subject == "math":
            return MOCK["math"]["seconds"]
        if subject == "english":
            return MOCK["english"]["seconds"]
        return MOCK["math"]["seconds"] + MOCK["english"]["seconds"]
    if mode == "diagnostic":
        return None
    return max(120, len(items) * 90)


def _public_question(qid, item, position=0):
    tmeta = TOPICS.get(item["topic"], {"name": item["topic"], "icon": ""})
    smeta = SKILLS.get(item["skill"], {"name": item["skill"]})
    return {
        "id": qid,
        "position": position,
        "subject": item["subject"],
        "topic": item["topic"],
        "topicName": tmeta["name"],
        "skill": item["skill"],
        "skillName": smeta["name"],
        "difficulty": item["difficulty"],
        "stem": item["stem"],
        "passage": item.get("passage"),
        "figure": item.get("figure"),
        "table": item.get("table"),
        "choices": item["choices"],
    }


def create_paper(mode, subject=None, topic=None, focus=None, tutor=False, timer=True, count=None, difficulty=None):
    mode, subject, focus, tutor, timer, count, difficulty = _normalize_request(
        mode, subject, topic, focus, tutor, timer, count, difficulty
    )
    last_error = None
    for _ in range(3):
        conn = connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            items = assemble_session_items(
                conn,
                mode=mode,
                subject=subject,
                focus=focus,
                count=count,
                difficulty=difficulty,
            )
            ids = _insert_questions(conn, items)
            label = _label_for(conn, mode, subject, focus)
            seconds = _seconds_for(mode, subject, items, timer)
            created = _now()
            cur = conn.execute(
                """
                INSERT INTO papers (mode, subject, label, focus, tutor, seconds_limit, created_at, total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mode,
                    None if subject == "combined" else subject,
                    label,
                    focus,
                    1 if tutor else 0,
                    seconds,
                    created,
                    len(items),
                ),
            )
            paper_id = cur.lastrowid
            public = []
            for pos, (qid, item) in enumerate(zip(ids, items)):
                conn.execute(
                    "INSERT INTO paper_items (paper_id, position, question_id) VALUES (?, ?, ?)",
                    (paper_id, pos, qid),
                )
                public.append(_public_question(qid, item, pos))
            conn.commit()
            return {
                "paperId": paper_id,
                "mode": mode,
                "subject": subject,
                "focus": focus,
                "tutor": tutor,
                "label": label,
                "seconds": seconds,
                "questions": public,
            }
        except sqlite3.IntegrityError as exc:
            conn.rollback()
            last_error = exc
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    raise RuntimeError(f"สร้างชุดข้อสอบไม่สำเร็จ: {last_error}")


def use_hint(paper_id, position):
    """Mark hint as used on this item and return the hint + concept tip."""
    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT q.hint, q.skill
            FROM paper_items pi
            JOIN questions q ON q.id = pi.question_id
            WHERE pi.paper_id = ? AND pi.position = ?
            """,
            (paper_id, int(position)),
        ).fetchone()
        if row is None:
            raise ValueError("ไม่พบข้อสอบข้อนี้")
        with conn:
            conn.execute(
                "UPDATE paper_items SET hint_used = 1 WHERE paper_id = ? AND position = ?",
                (paper_id, int(position)),
            )
        smeta = SKILLS.get(row["skill"])
        concept = smeta["lesson"]["concept"] if smeta else None
        return {
            "hint": row["hint"],
            "concept": concept,
            "skill": row["skill"],
            "skillName": smeta["name"] if smeta else row["skill"],
        }
    finally:
        conn.close()


def check_item_answer(paper_id, position, chosen, time_ms=None, flagged=False):
    """Grade one question immediately (used in Tutor mode) and return rich feedback."""
    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT pi.position, pi.question_id, pi.hint_used,
                   q.*
            FROM paper_items pi
            JOIN questions q ON q.id = pi.question_id
            WHERE pi.paper_id = ? AND pi.position = ?
            """,
            (paper_id, int(position)),
        ).fetchone()
        if row is None:
            raise ValueError("ไม่พบข้อสอบข้อนี้")
        choices = json.loads(row["choices_json"])
        why_map = json.loads(row["why_json"] or "{}")
        steps = json.loads(row["steps_json"] or "[]")
        ans_idx = row["answer_index"]
        stored = chosen if (isinstance(chosen, int) and 0 <= chosen < len(choices)) else None

        with conn:
            conn.execute(
                """
                UPDATE paper_items
                SET chosen = ?, time_ms = COALESCE(?, time_ms), flagged = ?, answered_at = ?
                WHERE paper_id = ? AND position = ?
                """,
                (stored, int(time_ms) if time_ms else None, 1 if flagged else 0, _now(), paper_id, int(position)),
            )

        is_ok = stored == ans_idx
        chosen_why = why_map.get(str(stored)) if (stored is not None and not is_ok) else None
        smeta = SKILLS.get(row["skill"])
        return {
            "position": int(position),
            "chosen": stored,
            "answerIndex": ans_idx,
            "correct": is_ok,
            "status": "ok" if is_ok else ("blank" if stored is None else "bad"),
            "chosenWhy": chosen_why["why"] if chosen_why else None,
            "mistakeTag": chosen_why["tag"] if chosen_why else None,
            "mistakeLabel": MISTAKE_TAGS.get(chosen_why["tag"]) if chosen_why else None,
            "whyAll": why_map,
            "hint": row["hint"],
            "steps": steps,
            "skill": row["skill"],
            "skillName": smeta["name"] if smeta else row["skill"],
            "lesson": smeta["lesson"] if smeta else None,
        }
    finally:
        conn.close()


def append_similar_question(paper_id, position):
    """Generate a fresh question of the same skill & difficulty and append it to the paper."""
    conn = connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            """
            SELECT q.skill, q.topic, q.difficulty
            FROM paper_items pi
            JOIN questions q ON q.id = pi.question_id
            WHERE pi.paper_id = ? AND pi.position = ?
            """,
            (paper_id, int(position)),
        ).fetchone()
        if row is None:
            raise ValueError("ไม่พบข้อต้นแบบ")
        sk = row["skill"]
        tk = row["topic"]
        diff = row["difficulty"]
        if sk in SKILLS:
            item = pick_one(conn, set(), set(), skill_key=sk, difficulty=diff)
        else:
            item = pick_one(conn, set(), set(), topic_key=tk, difficulty=diff)
        qid = _insert_questions(conn, [item])[0]
        next_pos = conn.execute(
            "SELECT COALESCE(MAX(position), -1) + 1 AS p FROM paper_items WHERE paper_id = ?",
            (paper_id,),
        ).fetchone()["p"]
        conn.execute(
            "INSERT INTO paper_items (paper_id, position, question_id) VALUES (?, ?, ?)",
            (paper_id, next_pos, qid),
        )
        conn.execute("UPDATE papers SET total = total + 1 WHERE id = ?", (paper_id,))
        conn.commit()
        return _public_question(qid, item, next_pos)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _load_paper_rows(conn, paper_id):
    return conn.execute(
        """
        SELECT pi.position, pi.question_id, pi.chosen, pi.time_ms, pi.hint_used, pi.flagged,
               q.*
        FROM paper_items pi
        JOIN questions q ON q.id = pi.question_id
        WHERE pi.paper_id = ?
        ORDER BY pi.position
        """,
        (paper_id,),
    ).fetchall()


def _result_from_rows(paper, rows):
    correct = wrong = blank = 0
    questions = []
    topic_buckets = {}
    skill_buckets = {}
    mistake_counts = {}

    for row in rows:
        chosen = row["chosen"]
        choices = json.loads(row["choices_json"])
        why_map = json.loads(row["why_json"] or "{}")
        steps = json.loads(row["steps_json"] or "[]")
        ans_idx = row["answer_index"]

        if chosen is None:
            blank += 1
            status = "blank"
        elif chosen == ans_idx:
            correct += 1
            status = "ok"
        else:
            wrong += 1
            status = "bad"

        chosen_why = why_map.get(str(chosen)) if status == "bad" else None
        if chosen_why and chosen_why.get("tag") in MISTAKE_TAGS:
            tag = chosen_why["tag"]
            mistake_counts[tag] = mistake_counts.get(tag, 0) + 1

        tk = row["topic"]
        tmeta = TOPICS.get(tk, {"name": tk, "icon": "", "subject": row["subject"]})
        tb = topic_buckets.setdefault(
            tk,
            {
                "key": tk,
                "subject": row["subject"],
                "topic": tmeta["name"],
                "icon": tmeta.get("icon", ""),
                "correct": 0,
                "total": 0,
            },
        )
        tb["total"] += 1
        if status == "ok":
            tb["correct"] += 1

        sk = row["skill"]
        smeta = SKILLS.get(sk)
        sb = skill_buckets.setdefault(
            sk,
            {
                "key": sk,
                "topic": tk,
                "subject": row["subject"],
                "name": smeta["name"] if smeta else sk,
                "hasLesson": smeta is not None,
                "correct": 0,
                "total": 0,
            },
        )
        sb["total"] += 1
        if status == "ok":
            sb["correct"] += 1

        explanation = "\n".join(steps)
        mistake_text = None
        if status != "ok":
            if chosen_why:
                mistake_text = f"ทำไมตัวเลือกที่เลือกถึงผิด: {chosen_why['why']}\nวิธีคิดที่ถูก:\n" + "\n".join(
                    f"• {s}" for s in steps
                )
            else:
                mistake_text = "ยังไม่ได้เลือกคำตอบ\nวิธีคิด:\n" + "\n".join(f"• {s}" for s in steps)

        questions.append(
            {
                "id": row["question_id"],
                "position": row["position"],
                "subject": row["subject"],
                "topic": tmeta["name"],
                "topicKey": tk,
                "skill": sk,
                "skillName": smeta["name"] if smeta else sk,
                "hasLesson": smeta is not None,
                "difficulty": row["difficulty"],
                "stem": row["stem"],
                "passage": row["passage"],
                "figure": row["figure"],
                "table": json.loads(row["table_json"]) if row["table_json"] else None,
                "choices": choices,
                "answerIndex": ans_idx,
                "chosen": chosen,
                "status": status,
                "timeMs": row["time_ms"],
                "hintUsed": bool(row["hint_used"]),
                "flagged": bool(row["flagged"]),
                "chosenWhy": chosen_why["why"] if chosen_why else None,
                "mistakeTag": chosen_why["tag"] if chosen_why else None,
                "mistakeLabel": MISTAKE_TAGS.get(chosen_why["tag"]) if chosen_why else None,
                "whyAll": why_map,
                "hint": row["hint"],
                "steps": steps,
                "explanation": explanation,
                "mistakeExplanation": mistake_text,
            }
        )

    total = len(rows)
    percent = round(100 * correct / total) if total else 0
    topics = []
    for tb in topic_buckets.values():
        tb["percent"] = round(100 * tb["correct"] / tb["total"]) if tb["total"] else 0
        topics.append(tb)
    topics.sort(key=lambda b: (b["percent"], -b["total"]))

    skills = []
    for sb in skill_buckets.values():
        sb["percent"] = round(100 * sb["correct"] / sb["total"]) if sb["total"] else 0
        skills.append(sb)
    skills.sort(key=lambda b: (b["percent"], -b["total"]))

    session_mistakes = [
        {"tag": tag, "label": MISTAKE_TAGS[tag], "count": cnt}
        for tag, cnt in sorted(mistake_counts.items(), key=lambda kv: -kv[1])
    ]

    weak_skills = [s for s in skills if s["percent"] < 80]
    if weak_skills:
        improve = "ทักษะที่ควรทบทวนและฝึกเพิ่มจากชุดนี้: " + ", ".join(s["name"] for s in weak_skills[:3])
    else:
        improve = "ยอดเยี่ยม! ทำได้เกิน 80% ทุกทักษะในชุดนี้ ลองขยับความยากหรือทำชุดจำลองสอบต่อได้เลย"

    return {
        "paperId": paper["id"],
        "mode": paper["mode"],
        "subject": paper["subject"],
        "focus": paper["focus"],
        "tutor": bool(paper["tutor"]),
        "label": paper["label"],
        "percent": percent,
        "correct": correct,
        "wrong": wrong,
        "blank": blank,
        "total": total,
        "usedSec": paper["used_sec"] or 0,
        "topics": topics,
        "skills": skills,
        "sessionMistakes": session_mistakes,
        "improve": improve,
        "questions": questions,
    }


def submit_paper(paper_id, answers, used_sec=0, auto=False, times_ms=None, flags=None):
    conn = connect()
    try:
        conn.execute("BEGIN IMMEDIATE")
        paper = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
        if paper is None:
            raise ValueError("ไม่พบชุดข้อสอบ")
        rows = _load_paper_rows(conn, paper_id)
        if paper["submitted_at"] is not None:
            conn.rollback()
            return _result_from_rows(paper, rows)

        if not isinstance(answers, list) or len(answers) != len(rows):
            raise ValueError("จำนวนคำตอบไม่ตรงกับข้อสอบ")

        now = _now()
        times_ms = times_ms if isinstance(times_ms, list) and len(times_ms) == len(rows) else [None] * len(rows)
        flags = flags if isinstance(flags, list) and len(flags) == len(rows) else [False] * len(rows)

        for row, chosen, t_ms, flg in zip(rows, answers, times_ms, flags):
            stored = chosen if (isinstance(chosen, int) and 0 <= chosen < 4) else None
            conn.execute(
                """
                UPDATE paper_items
                SET chosen = ?,
                    time_ms = COALESCE(?, time_ms),
                    flagged = ?,
                    answered_at = COALESCE(answered_at, ?)
                WHERE paper_id = ? AND position = ?
                """,
                (
                    stored,
                    int(t_ms) if isinstance(t_ms, (int, float)) and t_ms > 0 else None,
                    1 if flg else 0,
                    now,
                    paper_id,
                    row["position"],
                ),
            )

        rows = _load_paper_rows(conn, paper_id)
        correct = sum(1 for r in rows if r["chosen"] is not None and r["chosen"] == r["answer_index"])
        wrong = sum(1 for r in rows if r["chosen"] is not None and r["chosen"] != r["answer_index"])
        blank = len(rows) - correct - wrong
        total = len(rows)
        percent = round(100 * correct / total) if total else 0

        conn.execute(
            """
            UPDATE papers
            SET submitted_at = ?, auto_submit = ?, percent = ?, correct = ?,
                wrong = ?, blank = ?, total = ?, used_sec = ?
            WHERE id = ?
            """,
            (now, 1 if auto else 0, percent, correct, wrong, blank, total, int(used_sec or 0), paper_id),
        )
        conn.commit()
        paper = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
        return _result_from_rows(paper, rows)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_paper(paper_id):
    conn = connect()
    try:
        paper = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
        if paper is None or paper["submitted_at"] is None:
            raise ValueError("ไม่พบประวัติชุดนี้")
        return _result_from_rows(paper, _load_paper_rows(conn, paper_id))
    finally:
        conn.close()


def home_summary():
    conn = connect()
    try:
        dash = build_dashboard(conn)
        # Keep backward-compatible top-level keys alongside rich dashboard data
        weak = [
            {
                "subject": t["subject"],
                "topic": t["name"],
                "topicKey": t["key"],
                "correct": t["correct"],
                "total": t["attempts"],
                "percent": t["accuracy"],
                "mastery": t["mastery"],
            }
            for t in sorted(dash["topics"], key=lambda x: (x["mastery"], -x["attempts"]))
        ]
        return {
            **dash,
            "weak": weak,
            "questionsUsed": dash["bankStats"]["questionsGenerated"],
            "papers": len(dash["history"]),
            "submitted": len(dash["history"]),
        }
    finally:
        conn.close()
