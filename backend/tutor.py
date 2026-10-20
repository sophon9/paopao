"""Adaptive tutoring, mastery estimation, diagnostics and study-plan engine.

Computes skill and topic mastery, exam readiness for top M.1 schools,
mistake-tag patterns, pace analysis, and next-step recommendations from the
attempt history stored in SQLite.
"""

import json
import math
import random
import time
from collections import Counter, defaultdict

from backend.bank import SKILLS, TEMPLATES, TOPICS
from backend.bank.core import DIFF_RANK, DIFFICULTIES, MISTAKE_TAGS, run_template, validate_item
from backend.bank.topics import DIAGNOSTIC, MOCK, TARGET_SECONDS

DIFF_WEIGHT = {"easy": 0.78, "medium": 1.0, "hard": 1.28, "challenge": 1.55}

MISTAKE_ADVICE = {
    "concept": "ทบทวนนิยามและหลักคิดในหน้า 'บทเรียน' ก่อนเริ่มทำโจทย์ชุดถัดไป",
    "calc": "ทดเลขเป็นระเบียบทีละบรรทัด และตรวจคำตอบย้อนกลับทุกครั้งก่อนกดส่ง",
    "partial": "ขีดเส้นใต้สิ่งที่โจทย์ถามตอนท้ายสุด เพื่อเช็กว่าคำนวณครบทุกขั้นหรือยัง",
    "misread": "วงคำสำคัญในโจทย์ เช่น 'เหลือ', 'ไม่ถูกต้อง', 'มากกว่าอยู่เท่าไร' ก่อนลงมือคิด",
    "unit": "เขียนหน่วยกำกับทุกตัวเลขตั้งแต่บรรทัดแรก และแปลงหน่วยให้ตรงกันก่อนคำนวณ",
    "sign": "ระวังเครื่องหมายบวก-ลบ และลำดับมาก-น้อย ลองวาดเส้นจำนวนช่วยเช็กทิศทาง",
    "formula": "เขียนสูตรออกมาก่อนแทนค่า และเช็กว่าไม่สลับสูตรพื้นที่กับเส้นรอบรูป",
    "form": "สังเกตคำบอกเวลา (yesterday, since, every day) และโครงสร้างกริยาที่ตามหลัง",
    "meaning": "จดคำศัพท์ที่พบบ่อยพร้อมคำเหมือน-คำตรงข้าม และดูบริบทประโยคประกอบ",
    "context": "อ่านประโยคข้างหน้าและข้างหลังช่องว่างให้ครบก่อนเลือกคำตอบ",
    "agreement": "หาประธานตัวจริงของประโยคให้เจอ (ระวังคำขยายคั่นกลาง) แล้วเช็กเอกพจน์/พหูพจน์",
    "detail": "เทียบตัวเลือกกับประโยคในบทอ่านคำต่อคำ ระวังตัวเลขและชื่อเฉพาะที่หลอก",
    "inference": "เลือกข้อที่สรุปได้จากหลักฐานในบทอ่านเท่านั้น อย่าเดาต่อเติมเองเกินเรื่อง",
    "trap": "เมื่อเจอตัวเลือกที่ดูคุ้นตา ให้เช็กเงื่อนไขโจทย์ซ้ำอีกครั้งว่ามีจุดหลอกหรือไม่",
}

SCHOOL_BENCHMARKS = [
    {"key": "regular", "name": "ม.1 ห้องเรียนทั่วไป (ร.ร.รัฐบาลชั้นนำ)", "target": 65},
    {"key": "competitive", "name": "สวนกุหลาบ · สาธิต · เตรียมฯ น้อย", "target": 78},
    {"key": "gifted", "name": "ห้องเรียนพิเศษ Gifted / EP / SMTE", "target": 86},
]


def _now_ms():
    return int(time.time() * 1000)


def _load_attempts(conn):
    """Return all graded paper_items joined with question & paper metadata."""
    return conn.execute(
        """
        SELECT pi.paper_id, pi.position, pi.question_id, pi.chosen, pi.time_ms,
               pi.hint_used, pi.flagged,
               COALESCE(pi.answered_at, p.submitted_at) AS at_ms,
               q.subject, q.topic, q.skill, q.difficulty, q.answer_index,
               q.why_json, q.legacy
        FROM paper_items pi
        JOIN questions q ON q.id = pi.question_id
        JOIN papers p ON p.id = pi.paper_id
        WHERE pi.answered_at IS NOT NULL OR p.submitted_at IS NOT NULL
        ORDER BY COALESCE(pi.answered_at, p.submitted_at) ASC, pi.paper_id ASC, pi.position ASC
        """
    ).fetchall()


def _compute_skill_stats(attempts, now_ms=None):
    """Compute mastery and review priority for every registered skill."""
    now_ms = now_ms or _now_ms()
    by_skill = defaultdict(list)
    for row in attempts:
        by_skill[row["skill"]].append(row)

    out = {}
    for sk, meta in SKILLS.items():
        rows = by_skill.get(sk, [])
        n = len(rows)
        correct = sum(1 for r in rows if r["chosen"] is not None and r["chosen"] == r["answer_index"])
        wrong = sum(1 for r in rows if r["chosen"] is not None and r["chosen"] != r["answer_index"])
        blank = n - correct - wrong
        acc = round(100 * correct / n) if n else 0

        if n == 0:
            mastery = 0
            status = "unseen"
            last_at = None
            streak = 0
            next_diff = "easy"
        else:
            # Recency-weighted & difficulty-weighted score
            num_w = 0.0
            den_w = 0.0
            for idx, r in enumerate(reversed(rows)):  # idx=0 is most recent
                decay = 0.84 ** idx
                dw = DIFF_WEIGHT.get(r["difficulty"], 1.0)
                is_ok = r["chosen"] is not None and r["chosen"] == r["answer_index"]
                if is_ok:
                    credit = (0.68 if r["hint_used"] else 1.0) * dw
                    cap = dw
                else:
                    credit = 0.0
                    cap = max(1.0, dw * 0.95)
                num_w += decay * credit
                den_w += decay * cap
            raw = (num_w / den_w) if den_w else 0.0
            # Highest difficulty solved boosts ceiling; only doing easy caps at ~76
            max_ok_diff = max(
                (DIFF_RANK.get(r["difficulty"], 0) for r in rows
                 if r["chosen"] is not None and r["chosen"] == r["answer_index"]),
                default=-1,
            )
            diff_ceiling = {
                -1: 35,
                0: 76,   # only easy solved
                1: 90,   # medium solved
                2: 97,   # hard solved
                3: 100,  # challenge solved
            }[max_ok_diff]
            conf = 1.0 - math.exp(-n / 3.2)
            mastery = min(diff_ceiling, round(100 * raw * (0.45 + 0.55 * conf)))

            last_at = rows[-1]["at_ms"]
            days_since = max(0.0, (now_ms - (last_at or now_ms)) / 86_400_000)

            streak = 0
            for r in reversed(rows):
                if r["chosen"] is not None and r["chosen"] == r["answer_index"] and not r["hint_used"]:
                    streak += 1
                else:
                    break

            recent_bad = sum(
                1 for r in rows[-2:] if r["chosen"] is None or r["chosen"] != r["answer_index"]
            )
            if mastery >= 78 and n >= 3 and recent_bad == 0 and days_since <= 7:
                status = "mastered"
            elif mastery >= 65 and n >= 3 and (days_since > 7 or recent_bad > 0):
                status = "rusty"
            elif mastery >= 48 and n >= 2:
                status = "practicing"
            else:
                status = "learning"

            if mastery < 45 or (streak == 0 and max_ok_diff <= 0):
                next_diff = "easy"
            elif mastery < 68 or max_ok_diff < 1:
                next_diff = "medium"
            elif mastery < 84 or max_ok_diff < 2:
                next_diff = "hard"
            else:
                next_diff = "challenge"

        # Review priority: higher = coach should recommend sooner
        if n == 0:
            priority = 45.0 * meta["weight"]
        else:
            days_since = max(0.0, (now_ms - (last_at or now_ms)) / 86_400_000)
            weakness = max(0, 88 - mastery)
            recency_err = 22 if (rows[-1]["chosen"] != rows[-1]["answer_index"]) else 0
            forgetting = min(25.0, days_since * 2.5) if mastery < 90 else min(12.0, days_since * 1.0)
            priority = (weakness + recency_err + forgetting) * meta["weight"]

        out[sk] = {
            "key": sk,
            "topic": meta["topic"],
            "subject": meta["subject"],
            "name": meta["name"],
            "weight": meta["weight"],
            "attempts": n,
            "correct": correct,
            "wrong": wrong,
            "blank": blank,
            "accuracy": acc,
            "mastery": mastery,
            "status": status,
            "streak": streak,
            "nextDifficulty": next_diff,
            "lastAt": last_at,
            "priority": round(priority, 1),
        }
    return out


def _compute_topic_stats(attempts, skill_stats):
    """Aggregate skill stats + any legacy attempts into per-topic analytics."""
    by_topic_rows = defaultdict(list)
    for r in attempts:
        if r["topic"] in TOPICS:
            by_topic_rows[r["topic"]].append(r)

    topics_out = []
    for tk, tmeta in TOPICS.items():
        t_skills = [s for s in skill_stats.values() if s["topic"] == tk]
        rows = by_topic_rows.get(tk, [])
        total = len(rows)
        correct = sum(1 for r in rows if r["chosen"] is not None and r["chosen"] == r["answer_index"])
        wrong = sum(1 for r in rows if r["chosen"] is not None and r["chosen"] != r["answer_index"])
        blank = total - correct - wrong
        acc = round(100 * correct / total) if total else 0

        # Skill mastery average (across practiced skills) + coverage + legacy fallback
        practiced = [s for s in t_skills if s["attempts"] > 0]
        coverage = round(100 * len(practiced) / len(t_skills)) if t_skills else 0
        if practiced:
            w_sum = sum(s["weight"] for s in practiced)
            practiced_avg = sum(s["mastery"] * s["weight"] for s in practiced) / (w_sum or 1)
            # Blend practiced average with overall topic coverage so practicing 1/8 skills isn't 90% topic mastery
            cov_factor = 0.45 + 0.55 * (len(practiced) / max(1, len(t_skills)))
            mastery = round(practiced_avg * cov_factor)
        elif total > 0:
            # Legacy attempts exist in this topic before new skills were practiced
            conf = 1.0 - math.exp(-total / 8.0)
            mastery = round(acc * (0.4 + 0.45 * conf))
        else:
            mastery = 0

        # Difficulty breakdown
        by_diff = {}
        for d in DIFFICULTIES:
            drows = [r for r in rows if r["difficulty"] == d]
            dc = sum(1 for r in drows if r["chosen"] is not None and r["chosen"] == r["answer_index"])
            by_diff[d] = {"correct": dc, "total": len(drows)}

        # Pace analysis (when time_ms is recorded)
        timed = [r for r in rows if r["time_ms"] and r["time_ms"] > 500]
        avg_sec = round(sum(r["time_ms"] for r in timed) / len(timed) / 1000, 1) if timed else None
        target_sec = TARGET_SECONDS.get(tmeta["subject"], {}).get("medium", 75)

        topics_out.append({
            "key": tk,
            "subject": tmeta["subject"],
            "name": tmeta["name"],
            "icon": tmeta["icon"],
            "blurb": tmeta["blurb"],
            "mastery": mastery,
            "accuracy": acc,
            "attempts": total,
            "correct": correct,
            "wrong": wrong,
            "blank": blank,
            "coverage": coverage,
            "skillsTotal": len(t_skills),
            "skillsPracticed": len(practiced),
            "skillsMastered": sum(1 for s in t_skills if s["status"] == "mastered"),
            "byDifficulty": by_diff,
            "avgSec": avg_sec,
            "targetSec": target_sec,
            "skills": sorted(t_skills, key=lambda s: (-s["priority"], s["key"])),
        })
    return topics_out


def _mistake_patterns(attempts):
    """Analyse the types of mistakes the student makes most frequently."""
    counts = Counter()
    recent_counts = Counter()
    wrong_rows = [r for r in attempts if r["chosen"] is not None and r["chosen"] != r["answer_index"]]
    recent_cut = max(0, len(wrong_rows) - 30)
    for idx, r in enumerate(wrong_rows):
        if r["legacy"]:
            continue
        try:
            why = json.loads(r["why_json"] or "{}")
            tag = (why.get(str(r["chosen"])) or {}).get("tag")
        except json.JSONDecodeError:
            tag = None
        if tag in MISTAKE_TAGS:
            counts[tag] += 1
            if idx >= recent_cut:
                recent_counts[tag] += 1

    total_tagged = sum(counts.values())
    out = []
    for tag, cnt in counts.most_common(5):
        out.append({
            "tag": tag,
            "label": MISTAKE_TAGS[tag],
            "count": cnt,
            "recent": recent_counts[tag],
            "percent": round(100 * cnt / total_tagged) if total_tagged else 0,
            "advice": MISTAKE_ADVICE.get(tag, ""),
        })
    return out


def _study_plan(topics, skill_stats, mistake_patterns):
    """Build 3–4 concrete recommended actions for today."""
    recs = []
    for subj, subj_label in (("math", "คณิตศาสตร์"), ("english", "ภาษาอังกฤษ")):
        s_topics = [t for t in topics if t["subject"] == subj]
        practiced_topics = sum(1 for t in s_topics if t["skillsPracticed"] > 0)
        if practiced_topics < max(2, len(s_topics) // 2):
            recs.append({
                "kind": "diagnostic",
                "badge": f"วัดระดับ · {subj_label}",
                "title": f"ทำแบบวัดระดับ{subj_label}ให้ครบทุกบท",
                "reason": f"ยังมีหัวข้อใน{subj_label}ที่ยังไม่เคยลองวัดผล ระบบจะคัดโจทย์ครอบคลุมทุกบทเพื่อหาจุดแข็ง-จุดอ่อนอย่างแม่นยำ",
                "action": {"mode": "diagnostic", "subject": subj, "tutor": False},
                "cta": f"เริ่มวัดระดับ{subj_label}",
            })

    # Weakest / highest-priority practiced skills (where student has stumbled)
    practiced_weak = sorted(
        [s for s in skill_stats.values() if s["attempts"] > 0 and s["mastery"] < 80],
        key=lambda s: -s["priority"],
    )
    for s in practiced_weak[:2]:
        tname = TOPICS[s["topic"]]["name"]
        recs.append({
            "kind": "weak_skill",
            "badge": f"ซ่อมจุดอ่อน · {tname}",
            "title": f"ติวเข้มเรื่อง “{s['name']}” (ความแม่น {s['mastery']}%)",
            "reason": f"ทำไป {s['attempts']} ข้อ ถูก {s['correct']} ข้อ — อ่านสรุปหลักคิด 1 นาที แล้วฝึกทีละข้อพร้อมคำใบ้และเฉลยละเอียด",
            "skill": s["key"],
            "action": {"mode": "skill", "subject": s["subject"], "focus": s["key"], "tutor": True},
            "cta": "เรียน + ฝึกเรื่องนี้",
        })

    # Rusty skills due for spaced repetition
    rusty = [s for s in skill_stats.values() if s["status"] == "rusty"]
    if rusty:
        s = rusty[0]
        recs.append({
            "kind": "review",
            "badge": "ทบทวนกันลืม",
            "title": f"ทบทวน “{s['name']}”",
            "reason": "เคยทำได้ดีแล้ว แต่เริ่มทิ้งช่วงหรือเพิ่งมีข้อที่พลาด ทบทวนสั้น ๆ เพื่อให้จำแม่นถึงวันสอบ",
            "skill": s["key"],
            "action": {"mode": "skill", "subject": s["subject"], "focus": s["key"], "tutor": True},
            "cta": "ทบทวน 6 ข้อ",
        })

    # Unseen high-weight skill
    unseen = sorted(
        [s for s in skill_stats.values() if s["attempts"] == 0],
        key=lambda s: (-s["weight"], s["key"]),
    )
    if unseen and len(recs) < 4:
        s = unseen[0]
        tname = TOPICS[s["topic"]]["name"]
        recs.append({
            "kind": "new_skill",
            "badge": f"บทสำคัญออกสอบบ่อย · {tname}",
            "title": f"เริ่มฝึก “{s['name']}”",
            "reason": "หัวข้อนี้เป็นแนวข้อสอบยอดนิยมของโรงเรียนแข่งขันสูง มาดูบทเรียนพร้อมตัวอย่างแล้วลองทำโจทย์กัน",
            "skill": s["key"],
            "action": {"mode": "skill", "subject": s["subject"], "focus": s["key"], "tutor": True},
            "cta": "เปิดบทเรียน + เริ่มฝึก",
        })

    if len(recs) < 4:
        recs.append({
            "kind": "adaptive",
            "badge": "คู่คิดจัดชุดให้",
            "title": "ฝึกแบบปรับระดับอัตโนมัติ (Adaptive Tutor)",
            "reason": "ระบบเลือกโจทย์จากเรื่องที่ยังไม่แม่นและปรับความยากตามฝีมือ พร้อมเฉลยทีละขั้นตอน",
            "action": {"mode": "adaptive", "subject": "math", "tutor": True},
            "cta": "เริ่มฝึกกับติวเตอร์",
        })

    return recs[:4]


def _streak_and_activity(conn):
    """Compute daily practice streak and 14-day activity counts."""
    rows = conn.execute(
        """
        SELECT COALESCE(pi.answered_at, p.submitted_at) AS at_ms,
               pi.chosen, q.answer_index
        FROM paper_items pi
        JOIN papers p ON p.id = pi.paper_id
        JOIN questions q ON q.id = pi.question_id
        WHERE pi.answered_at IS NOT NULL OR p.submitted_at IS NOT NULL
        """
    ).fetchall()
    by_day = defaultdict(lambda: {"total": 0, "correct": 0})
    for r in rows:
        if not r["at_ms"]:
            continue
        day = time.strftime("%Y-%m-%d", time.localtime(r["at_ms"] / 1000))
        by_day[day]["total"] += 1
        if r["chosen"] is not None and r["chosen"] == r["answer_index"]:
            by_day[day]["correct"] += 1

    now = time.time()
    days_14 = []
    for i in range(13, -1, -1):
        d = time.strftime("%Y-%m-%d", time.localtime(now - i * 86400))
        info = by_day.get(d, {"total": 0, "correct": 0})
        days_14.append({"date": d, "total": info["total"], "correct": info["correct"]})

    # Streak ending today or yesterday
    streak = 0
    start_offset = 0
    today_key = time.strftime("%Y-%m-%d", time.localtime(now))
    if by_day.get(today_key, {}).get("total", 0) == 0:
        start_offset = 1
    for i in range(start_offset, 365):
        d = time.strftime("%Y-%m-%d", time.localtime(now - i * 86400))
        if by_day.get(d, {}).get("total", 0) > 0:
            streak += 1
        else:
            break
    return streak, days_14, by_day.get(today_key, {"total": 0, "correct": 0})


def mistake_notebook(conn, limit=60, subject=None, topic=None):
    """Return recent wrong/blank items with full diagnostic explanation."""
    clauses = ["(pi.answered_at IS NOT NULL OR p.submitted_at IS NOT NULL)",
               "(pi.chosen IS NULL OR pi.chosen != q.answer_index)"]
    params = []
    if subject in ("math", "english"):
        clauses.append("q.subject = ?")
        params.append(subject)
    if topic:
        clauses.append("q.topic = ?")
        params.append(topic)
    where = " AND ".join(clauses)
    rows = conn.execute(
        f"""
        SELECT pi.paper_id, pi.position, pi.chosen, pi.time_ms, pi.hint_used,
               COALESCE(pi.answered_at, p.submitted_at) AS at_ms,
               p.label AS paper_label,
               q.*
        FROM paper_items pi
        JOIN questions q ON q.id = pi.question_id
        JOIN papers p ON p.id = pi.paper_id
        WHERE {where}
        ORDER BY COALESCE(pi.answered_at, p.submitted_at) DESC
        LIMIT ?
        """,
        (*params, limit),
    ).fetchall()

    items = []
    for r in rows:
        choices = json.loads(r["choices_json"])
        why_map = json.loads(r["why_json"] or "{}")
        steps = json.loads(r["steps_json"] or "[]")
        chosen = r["chosen"]
        chosen_why = why_map.get(str(chosen)) if chosen is not None else None
        sk = r["skill"]
        smeta = SKILLS.get(sk)
        tmeta = TOPICS.get(r["topic"], {"name": r["topic"], "icon": ""})
        items.append({
            "questionId": r["id"],
            "paperId": r["paper_id"],
            "paperLabel": r["paper_label"],
            "at": r["at_ms"],
            "subject": r["subject"],
            "topic": r["topic"],
            "topicName": tmeta["name"],
            "skill": sk,
            "skillName": smeta["name"] if smeta else sk,
            "hasLesson": smeta is not None,
            "difficulty": r["difficulty"],
            "stem": r["stem"],
            "passage": r["passage"],
            "figure": r["figure"],
            "table": json.loads(r["table_json"]) if r["table_json"] else None,
            "choices": choices,
            "answerIndex": r["answer_index"],
            "chosen": chosen,
            "chosenWhy": chosen_why["why"] if chosen_why else None,
            "mistakeTag": chosen_why["tag"] if chosen_why else ("blank" if chosen is None else "concept"),
            "mistakeLabel": MISTAKE_TAGS.get(chosen_why["tag"], "เข้าใจคลาดเคลื่อน") if chosen_why else (
                "ไม่ได้ตอบ" if chosen is None else "เข้าใจคลาดเคลื่อน"
            ),
            "hint": r["hint"],
            "steps": steps,
        })
    return items


def build_dashboard(conn):
    """Build the complete dashboard payload for the home, analytics & learn views."""
    attempts = _load_attempts(conn)
    skill_stats = _compute_skill_stats(attempts)
    topics = _compute_topic_stats(attempts, skill_stats)
    patterns = _mistake_patterns(attempts)
    plan = _study_plan(topics, skill_stats, patterns)
    streak, days_14, today = _streak_and_activity(conn)

    def subj_readiness(subj):
        ts = [t for t in topics if t["subject"] == subj]
        if not ts:
            return {"readiness": 0, "accuracy": 0, "coverage": 0, "attempts": 0}
        readiness = round(sum(t["mastery"] for t in ts) / len(ts))
        tot_att = sum(t["attempts"] for t in ts)
        tot_ok = sum(t["correct"] for t in ts)
        acc = round(100 * tot_ok / tot_att) if tot_att else 0
        cov = round(sum(t["coverage"] for t in ts) / len(ts))
        return {"readiness": readiness, "accuracy": acc, "coverage": cov, "attempts": tot_att}

    math_summary = subj_readiness("math")
    eng_summary = subj_readiness("english")
    overall_readiness = round((math_summary["readiness"] + eng_summary["readiness"]) / 2)

    history_rows = conn.execute(
        """
        SELECT id, mode, subject, label, focus, tutor, submitted_at, percent,
               correct, wrong, blank, total, used_sec, legacy
        FROM papers
        WHERE submitted_at IS NOT NULL
        ORDER BY submitted_at DESC
        LIMIT 40
        """
    ).fetchall()
    history = [
        {
            "paperId": r["id"],
            "mode": r["mode"],
            "subject": r["subject"],
            "label": r["label"],
            "focus": r["focus"],
            "tutor": bool(r["tutor"]),
            "at": r["submitted_at"],
            "percent": r["percent"],
            "correct": r["correct"],
            "wrong": r["wrong"],
            "blank": r["blank"],
            "total": r["total"],
            "usedSec": r["used_sec"] or 0,
            "legacy": bool(r["legacy"]),
        }
        for r in history_rows
    ]

    total_questions = conn.execute("SELECT COUNT(*) AS n FROM questions").fetchone()["n"]
    mistake_count = conn.execute(
        """
        SELECT COUNT(*) AS n
        FROM paper_items pi
        JOIN questions q ON q.id = pi.question_id
        JOIN papers p ON p.id = pi.paper_id
        WHERE (pi.answered_at IS NOT NULL OR p.submitted_at IS NOT NULL)
          AND (pi.chosen IS NULL OR pi.chosen != q.answer_index)
        """
    ).fetchone()["n"]

    return {
        "readiness": {
            "overall": overall_readiness,
            "math": math_summary,
            "english": eng_summary,
            "benchmarks": SCHOOL_BENCHMARKS,
        },
        "streak": {
            "days": streak,
            "todayTotal": today["total"],
            "todayCorrect": today["correct"],
            "dailyGoal": 15,
            "activity14d": days_14,
        },
        "studyPlan": plan,
        "topics": topics,
        "mistakePatterns": patterns,
        "mistakeCount": mistake_count,
        "history": history,
        "bankStats": {
            "questionsGenerated": total_questions,
            "topicsCount": len(TOPICS),
            "skillsCount": len(SKILLS),
            "templatesCount": len(TEMPLATES),
        },
    }


def get_lesson_payload(conn, skill_key):
    """Return a skill's lesson, its mastery stats, and 2 freshly generated worked examples."""
    if skill_key not in SKILLS:
        raise ValueError("ไม่พบบทเรียนนี้")
    meta = SKILLS[skill_key]
    tmeta = TOPICS[meta["topic"]]
    attempts = _load_attempts(conn)
    s_stats = _compute_skill_stats(attempts).get(skill_key)

    # Generate up to 2 sample problems (not stored in DB) so the student can see extra worked examples
    samples = []
    matching = [t for t in TEMPLATES if t.skill == skill_key and not t.group]
    if matching:
        seen_fp = set()
        for _ in range(15):
            if len(samples) >= 2:
                break
            t = random.choice(matching)
            for item in run_template(t):
                if item["fingerprint"] in seen_fp:
                    continue
                seen_fp.add(item["fingerprint"])
                samples.append({
                    "difficulty": item["difficulty"],
                    "stem": item["stem"],
                    "passage": item["passage"],
                    "figure": item["figure"],
                    "table": item["table"],
                    "answer": item["choices"][item["answer_index"]],
                    "hint": item["hint"],
                    "steps": item["steps"],
                })
                break

    return {
        "key": skill_key,
        "name": meta["name"],
        "topic": meta["topic"],
        "topicName": tmeta["name"],
        "subject": meta["subject"],
        "lesson": meta["lesson"],
        "stats": s_stats,
        "samples": samples,
    }


# ---------------------------------------------------------------------------
# Question generation & selection for sessions
# ---------------------------------------------------------------------------

def _is_fresh(conn, fp, batch_fps):
    if fp in batch_fps:
        return False
    row = conn.execute("SELECT 1 FROM questions WHERE fingerprint = ?", (fp,)).fetchone()
    return row is None


def pick_one(conn, batch_fps, used_templates, *, skill_key=None, topic_key=None, difficulty=None):
    """Generate one fresh validated non-group item matching the constraints."""
    pool = [t for t in TEMPLATES if not t.group]
    if skill_key:
        pool = [t for t in pool if t.skill == skill_key]
    elif topic_key:
        pool = [t for t in pool if SKILLS[t.skill]["topic"] == topic_key]
    if not pool:
        raise RuntimeError(f"ยังไม่มีแม่แบบโจทย์สำหรับ {skill_key or topic_key}")

    if difficulty:
        target_rank = DIFF_RANK.get(difficulty, 1)
        exact = [t for t in pool if t.difficulty == difficulty]
        near = sorted(pool, key=lambda t: abs(DIFF_RANK[t.difficulty] - target_rank))
        ordered_pools = [exact, near] if exact else [near]
    else:
        ordered_pools = [pool]

    for cand_pool in ordered_pools:
        for attempt in range(70):
            sub = [t for t in cand_pool if t.name not in used_templates] if attempt < 40 else cand_pool
            if not sub:
                sub = cand_pool
            tmpl = random.choice(sub)
            items = run_template(tmpl)
            if not items:
                continue
            item = items[0]
            if not _is_fresh(conn, item["fingerprint"], batch_fps):
                continue
            validate_item(item)
            batch_fps.add(item["fingerprint"])
            used_templates.add(tmpl.name)
            return item
    raise RuntimeError(f"สร้างโจทย์ใหม่ไม่สำเร็จสำหรับ {skill_key or topic_key}")


def pick_group(conn, batch_fps, used_templates, *, topic_key=None, skill_key=None, max_items=4):
    """Generate a fresh group of items sharing one passage/chart (e.g. Reading)."""
    pool = [t for t in TEMPLATES if t.group]
    if skill_key:
        pool = [t for t in pool if t.skill == skill_key]
    elif topic_key:
        pool = [t for t in pool if SKILLS[t.skill]["topic"] == topic_key]
    if not pool:
        return []
    for attempt in range(50):
        sub = [t for t in pool if t.name not in used_templates] if attempt < 30 else pool
        if not sub:
            sub = pool
        tmpl = random.choice(sub)
        items = run_template(tmpl)
        if not items:
            continue
        items = items[:max_items]
        if not all(_is_fresh(conn, it["fingerprint"], batch_fps) for it in items):
            continue
        for it in items:
            validate_item(it)
        for it in items:
            batch_fps.add(it["fingerprint"])
        used_templates.add(tmpl.name)
        return items
    return []


def difficulties_for_mix(count, mix):
    """Turn a difficulty mix dict into a list of ``count`` difficulty labels."""
    order = []
    for d in DIFFICULTIES:
        k = round(count * mix.get(d, 0.25))
        order.extend([d] * k)
    while len(order) < count:
        order.append("medium")
    order = order[:count]
    random.shuffle(order)
    return order


def assemble_session_items(conn, *, mode, subject=None, focus=None, count=None, difficulty=None):
    """Build a list of fresh question dicts for the requested session mode."""
    batch_fps = set()
    used_templates = set()
    attempts = _load_attempts(conn)
    skill_stats = _compute_skill_stats(attempts)

    if mode == "mock":
        subjects = ["math", "english"] if subject in (None, "combined", "all") else [subject]
        all_items = []
        for subj in subjects:
            spec = MOCK[subj]
            subj_items = []
            for tk, n in spec["plan"]:
                diffs = difficulties_for_mix(n, spec["mix"])
                # Use group templates for reading (or topics with group templates)
                group_tmpls = [t for t in TEMPLATES if t.group and SKILLS[t.skill]["topic"] == tk]
                remaining = n
                if group_tmpls and remaining >= 3:
                    groups_wanted = 2 if remaining >= 6 else 1
                    for _ in range(groups_wanted):
                        if remaining < 3:
                            break
                        grp = pick_group(conn, batch_fps, used_templates, topic_key=tk, max_items=min(4, remaining))
                        if grp:
                            subj_items.extend(grp)
                            remaining -= len(grp)
                for d in diffs[:remaining]:
                    subj_items.append(pick_one(conn, batch_fps, used_templates, topic_key=tk, difficulty=d))
            all_items.extend(subj_items)
        return all_items

    if mode == "diagnostic":
        subj = subject if subject in ("math", "english") else "math"
        spec = DIAGNOSTIC[subj]
        per_topic = spec["per_topic"]
        items = []
        for tk, tmeta in TOPICS.items():
            if tmeta["subject"] != subj:
                continue
            if tk == "e.read":
                grp = pick_group(conn, batch_fps, used_templates, topic_key=tk, max_items=per_topic)
                if grp:
                    items.extend(grp)
                    continue
            diffs = ["easy", "medium", "hard", "challenge"][:per_topic]
            for d in diffs:
                items.append(pick_one(conn, batch_fps, used_templates, topic_key=tk, difficulty=d))
        return items

    if mode == "skill":
        n = count or 8
        if focus in SKILLS:
            sk = focus
            s_stat = skill_stats.get(sk)
            # Check if this skill only has group templates
            has_single = any(not t.group and t.skill == sk for t in TEMPLATES)
            if not has_single:
                items = []
                while len(items) < n:
                    grp = pick_group(conn, batch_fps, used_templates, skill_key=sk, max_items=min(4, n - len(items)))
                    if not grp:
                        break
                    items.extend(grp)
                return items
            if difficulty in DIFF_RANK:
                diffs = [difficulty] * n
            else:
                # Progressive ladder centred on student's nextDifficulty
                base = s_stat["nextDifficulty"] if s_stat else "medium"
                rank = DIFF_RANK.get(base, 1)
                ladder = [
                    DIFFICULTIES[max(0, rank - 1)],
                    DIFFICULTIES[rank],
                    DIFFICULTIES[rank],
                    DIFFICULTIES[min(3, rank + 1)],
                ]
                diffs = [ladder[i % len(ladder)] for i in range(n)]
            return [pick_one(conn, batch_fps, used_templates, skill_key=sk, difficulty=d) for d in diffs]

        if focus in TOPICS:
            tk = focus
            if tk == "e.read":
                items = []
                while len(items) < n:
                    grp = pick_group(conn, batch_fps, used_templates, topic_key=tk, max_items=min(4, n - len(items)))
                    if not grp:
                        break
                    items.extend(grp)
                while len(items) < n:
                    items.append(pick_one(conn, batch_fps, used_templates, topic_key=tk))
                return items[:n]
            t_skills = [s for s in skill_stats.values() if s["topic"] == tk]
            t_skills.sort(key=lambda s: -s["priority"])
            items = []
            for i in range(n):
                sk_stat = t_skills[i % len(t_skills)]
                diff = difficulty if difficulty in DIFF_RANK else sk_stat["nextDifficulty"]
                has_single = any(not t.group and t.skill == sk_stat["key"] for t in TEMPLATES)
                if has_single:
                    items.append(pick_one(conn, batch_fps, used_templates, skill_key=sk_stat["key"], difficulty=diff))
                else:
                    items.append(pick_one(conn, batch_fps, used_templates, topic_key=tk, difficulty=diff))
            return items
        raise ValueError("ไม่พบหัวข้อหรือทักษะที่เลือก")

    if mode in ("adaptive", "review"):
        n = count or 10
        subj = subject if subject in ("math", "english") else None
        candidates = [
            s for s in skill_stats.values()
            if (subj is None or s["subject"] == subj)
        ]
        if mode == "review":
            # Focus on skills where the student has made mistakes or is rusty
            prioritized = [s for s in candidates if s["wrong"] + s["blank"] > 0 or s["status"] == "rusty"]
            if not prioritized:
                prioritized = candidates
        else:
            prioritized = candidates
        prioritized.sort(key=lambda s: -s["priority"])
        top_pool = prioritized[: max(5, min(10, len(prioritized)))]
        items = []
        i = 0
        while len(items) < n:
            s_stat = top_pool[i % len(top_pool)]
            i += 1
            sk = s_stat["key"]
            has_single = any(not t.group and t.skill == sk for t in TEMPLATES)
            if has_single:
                items.append(pick_one(conn, batch_fps, used_templates, skill_key=sk, difficulty=s_stat["nextDifficulty"]))
            else:
                grp = pick_group(conn, batch_fps, used_templates, topic_key=s_stat["topic"], max_items=min(3, n - len(items)))
                if grp:
                    items.extend(grp)
                else:
                    items.append(pick_one(conn, batch_fps, used_templates, topic_key=s_stat["topic"]))
        return items[:n]

    raise ValueError(f"ไม่รู้จักโหมด {mode}")
