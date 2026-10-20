"""One-time migration from legacy ``quiz.db`` into ``tutor.db``.

Preserves all previously generated questions, papers, and student answers,
mapping old topic/skill names directly to the new 13-topic, 103-skill
curriculum so historical practice sessions appear in the timeline, skill
matrix, readiness scores, and mistake notebook with working lesson links.
"""

import json
import sqlite3
from pathlib import Path

LEGACY_TOPIC_MAP = {
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

LEGACY_SKILL_MAP = {
    # Math - Number
    "add-4digit": ("m.num", "m.num.order"),
    "sub-4digit": ("m.num", "m.num.order"),
    "mul-2digit": ("m.num", "m.num.order"),
    "div-exact": ("m.num", "m.num.div"),
    "order-ops": ("m.num", "m.num.order"),
    "gcd": ("m.num", "m.num.gcd_lcm"),
    "lcm": ("m.num", "m.num.gcd_lcm"),
    "which-prime": ("m.num", "m.num.prime"),
    "integers-between": ("m.num", "m.num.int"),
    "square": ("m.num", "m.num.exp"),
    # Math - Fraction & Decimal
    "frac-to-dec": ("m.frac", "m.frac.dec_rep"),
    "dec-to-frac": ("m.frac", "m.frac.dec_rep"),
    "add-frac": ("m.frac", "m.frac.addsub"),
    "sub-frac": ("m.frac", "m.frac.addsub"),
    "mul-frac": ("m.frac", "m.frac.muldiv"),
    "div-frac": ("m.frac", "m.frac.muldiv"),
    "frac-of-whole": ("m.frac", "m.frac.of_qty"),
    "greatest-frac": ("m.frac", "m.frac.compare"),
    "mixed-to-improper": ("m.frac", "m.frac.equiv"),
    # Math - Ratio & Percent
    "simplify-ratio": ("m.ratio", "m.ratio.basic"),
    "share-ratio": ("m.ratio", "m.ratio.share"),
    "percent-of": ("m.ratio", "m.ratio.pct_basic"),
    "what-percent": ("m.ratio", "m.ratio.pct_basic"),
    "discount": ("m.ratio", "m.ratio.discount"),
    "profit": ("m.ratio", "m.ratio.profit"),
    # Math - Algebra
    "eq-add": ("m.alg", "m.alg.eq_basic"),
    "eq-mul": ("m.alg", "m.alg.eq_basic"),
    "eq-two-step": ("m.alg", "m.alg.eq_basic"),
    "eq-word": ("m.alg", "m.alg.word_eq"),
    # Math - Geometry & Measurement
    "tri-angle": ("m.geo", "m.geo.tri_angles"),
    "rect-area": ("m.meas", "m.meas.rect_tri"),
    "tri-area": ("m.meas", "m.meas.rect_tri"),
    "rect-perim": ("m.meas", "m.meas.perim"),
    "box-volume": ("m.meas", "m.meas.volume"),
    "circle-22-7": ("m.meas", "m.meas.circle"),
    "composite-area": ("m.meas", "m.meas.shaded"),
    # Math - Data
    "mean": ("m.data", "m.data.central"),
    "median": ("m.data", "m.data.central"),
    "mode": ("m.data", "m.data.central"),
    "missing-mean": ("m.data", "m.data.mean_adv"),
    "table-max": ("m.data", "m.data.picto_table"),
    # Math - Word problems
    "speed": ("m.word", "m.word.speed"),
    "eq-age": ("m.word", "m.word.age"),
    "money-steps": ("m.word", "m.word.money"),
    "change": ("m.word", "m.word.money"),
    # English - Grammar
    "present-simple-3rd": ("e.gram", "e.gram.present"),
    "present-continuous": ("e.gram", "e.gram.present"),
    "past-simple": ("e.gram", "e.gram.past"),
    "past-when": ("e.gram", "e.gram.past"),
    "future-will": ("e.gram", "e.gram.perfect_future"),
    "there-is-are": ("e.gram", "e.gram.sva"),
    "article": ("e.gram", "e.gram.pron_det"),
    "preposition-time": ("e.gram", "e.gram.prep_conj"),
    "comparative": ("e.gram", "e.gram.compare"),
    "modal-must": ("e.gram", "e.gram.modal_cond_passive"),
    # English - Reading
    "reading-detail": ("e.read", "e.read.detail"),
    "reading-habit": ("e.read", "e.read.detail"),
    "reading-number": ("e.read", "e.read.detail"),
    "reading-place": ("e.read", "e.read.detail"),
    "reading-plan": ("e.read", "e.read.infer"),
    # English - Conversation
    "thanks": ("e.conv", "e.conv.polite"),
    "apology-late": ("e.conv", "e.conv.polite"),
    "permission": ("e.conv", "e.conv.polite"),
    "offer-help": ("e.conv", "e.conv.polite"),
    "shopping-price": ("e.conv", "e.conv.daily"),
    "restaurant": ("e.conv", "e.conv.daily"),
    "doctor": ("e.conv", "e.conv.daily"),
    "birthday": ("e.conv", "e.conv.daily"),
    "classroom-repeat": ("e.conv", "e.conv.school"),
    "library": ("e.conv", "e.conv.school"),
    "introduction": ("e.conv", "e.conv.school"),
    "suggestion": ("e.conv", "e.conv.opinion"),
    "agree": ("e.conv", "e.conv.opinion"),
    "weather-plan": ("e.conv", "e.conv.opinion"),
    "asking-way": ("e.conv", "e.conv.phone_direction"),
    "phone": ("e.conv", "e.conv.phone_direction"),
}


def map_legacy_topic_and_skill(old_topic, old_skill=""):
    if old_skill in LEGACY_SKILL_MAP:
        return LEGACY_SKILL_MAP[old_skill]
    if old_skill.startswith("cloze-"):
        return ("e.vocab", "e.vocab.context")
    if old_skill.startswith("meaning-"):
        return ("e.vocab", "e.vocab.synonym")
    if old_skill.startswith("opposite-"):
        return ("e.vocab", "e.vocab.antonym")
    tk = LEGACY_TOPIC_MAP.get(old_topic, "m.num")
    return (tk, f"{tk}.legacy.{old_skill}")


def map_legacy_topic(old_topic, old_skill=""):
    return map_legacy_topic_and_skill(old_topic, old_skill)[0]


def migrate_legacy(conn, legacy_path: Path):
    if not legacy_path.exists():
        return
    src = sqlite3.connect(legacy_path)
    src.row_factory = sqlite3.Row
    try:
        q_rows = src.execute("SELECT * FROM questions ORDER BY id").fetchall()
        p_rows = src.execute("SELECT * FROM papers ORDER BY id").fetchall()
        pi_rows = src.execute("SELECT * FROM paper_items ORDER BY paper_id, position").fetchall()
    except sqlite3.Error:
        src.close()
        return
    src.close()

    with conn:
        for q in q_rows:
            topic_key, skill_key = map_legacy_topic_and_skill(q["topic"], q["skill"])
            explanation = (q["explanation"] or "").strip()
            steps = [s.strip() for s in explanation.split("\n") if s.strip()] or [explanation or "ดูเฉลยด้านบน"]
            choices = json.loads(q["choices_json"])
            ans_idx = q["answer_index"]
            why = {}
            for i in range(len(choices)):
                if i != ans_idx:
                    why[str(i)] = {
                        "why": f"คำตอบที่ถูกคือ {choices[ans_idx]} — {steps[0]}",
                        "tag": "concept",
                    }
            conn.execute(
                """
                INSERT OR IGNORE INTO questions (
                  id, fingerprint, subject, topic, skill, difficulty, template,
                  stem, passage, figure, table_json, choices_json, answer_index,
                  why_json, hint, steps_json, group_key, legacy, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, ?, ?, ?, ?, 1, ?)
                """,
                (
                    q["id"],
                    q["fingerprint"],
                    q["subject"],
                    topic_key,
                    skill_key,
                    q["difficulty"] if q["difficulty"] in ("easy", "medium", "hard", "challenge") else "medium",
                    f"legacy.{q['skill']}",
                    q["stem"],
                    q["passage"],
                    json.dumps(choices, ensure_ascii=False),
                    ans_idx,
                    json.dumps(why, ensure_ascii=False),
                    "อ่านโจทย์อย่างละเอียด แล้วเทียบกับสูตรหรือหลักการของเรื่องนี้",
                    json.dumps(steps, ensure_ascii=False),
                    q["group_key"],
                    q["created_at"],
                ),
            )

        for p in p_rows:
            old_mode = p["mode"]
            subj = p["subject"]
            if old_mode in ("math", "english"):
                subj = old_mode
                new_mode = "mock"
            elif old_mode == "combined":
                subj = None
                new_mode = "mock"
            else:
                new_mode = "skill"
            focus = map_legacy_topic(p["topic"]) if p["topic"] else None
            conn.execute(
                """
                INSERT OR IGNORE INTO papers (
                  id, mode, subject, label, focus, tutor, seconds_limit,
                  created_at, submitted_at, auto_submit, used_sec,
                  correct, wrong, blank, total, percent, legacy
                ) VALUES (?, ?, ?, ?, ?, 0, NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    p["id"],
                    new_mode,
                    subj,
                    p["label"],
                    focus,
                    p["created_at"],
                    p["submitted_at"],
                    p["auto_submit"] or 0,
                    p["used_sec"],
                    p["correct"],
                    p["wrong"],
                    p["blank"],
                    p["total"],
                    p["percent"],
                ),
            )

        paper_sub = {p["id"]: p["submitted_at"] for p in p_rows}
        for pi in pi_rows:
            conn.execute(
                """
                INSERT OR IGNORE INTO paper_items (
                  paper_id, position, question_id, chosen, time_ms,
                  hint_used, flagged, answered_at
                ) VALUES (?, ?, ?, ?, NULL, 0, 0, ?)
                """,
                (
                    pi["paper_id"],
                    pi["position"],
                    pi["question_id"],
                    pi["chosen"],
                    paper_sub.get(pi["paper_id"]),
                ),
            )
