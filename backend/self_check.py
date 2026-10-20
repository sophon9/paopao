"""End-to-end verification of the question bank, tutoring engine, and paper lifecycle."""

import os
import tempfile
from collections import Counter

from backend.bank import SKILLS, TEMPLATES, TOPICS
from backend.bank.check import main as check_bank
from backend.db import connect
from backend.papers import (
    append_similar_question,
    check_item_answer,
    create_paper,
    get_paper,
    home_summary,
    submit_paper,
    use_hint,
)
from backend.tutor import get_lesson_payload, mistake_notebook


def _grade_sample(paper, all_correct=True):
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT position, question_id FROM paper_items WHERE paper_id = ? ORDER BY position",
            (paper["paperId"],),
        ).fetchall()
        answers = []
        for idx, r in enumerate(rows):
            ans = conn.execute("SELECT answer_index FROM questions WHERE id = ?", (r["question_id"],)).fetchone()[
                "answer_index"
            ]
            if all_correct or idx % 3 != 0:
                answers.append(ans)
            else:
                answers.append((ans + 1) % 4)
    finally:
        conn.close()
    res = submit_paper(paper["paperId"], answers, used_sec=320, auto=False)
    if all_correct and res["percent"] != 100:
        raise SystemExit(f"expected 100%, got {res['percent']}%")
    return res


def check_papers_and_tutor():
    stems = []
    ids = []

    # 1. Mock Math (30 items across 8 topics)
    for _ in range(2):
        paper = create_paper("math")
        if len(paper["questions"]) != 30:
            raise SystemExit(f"math paper length {len(paper['questions'])} != 30")
        topics = Counter(q["topic"] for q in paper["questions"])
        if len(topics) < 8:
            raise SystemExit(f"math topics missing: {topics}")
        stems.extend((q["stem"], tuple(q["choices"]), q.get("passage") or "", q.get("figure") or "") for q in paper["questions"])
        ids.extend(q["id"] for q in paper["questions"])
        _grade_sample(paper, all_correct=True)

    # 2. Mock English (40 items across 5 topics)
    for _ in range(2):
        paper = create_paper("english")
        if len(paper["questions"]) != 40:
            raise SystemExit(f"english paper length {len(paper['questions'])} != 40")
        topics = Counter(q["topic"] for q in paper["questions"])
        if len(topics) < 5:
            raise SystemExit(f"english topics missing: {topics}")
        stems.extend((q["stem"], tuple(q["choices"]), q.get("passage") or "", q.get("figure") or "") for q in paper["questions"])
        ids.extend(q["id"] for q in paper["questions"])
        _grade_sample(paper, all_correct=False)

    # 3. Diagnostic, Adaptive, Skill, Review + Tutor interactions
    diag = create_paper("diagnostic", subject="math")
    if len(diag["questions"]) < 16:
        raise SystemExit("diagnostic math too short")
    _grade_sample(diag, all_correct=False)

    sample_skill = next(iter(SKILLS))
    drill = create_paper("skill", subject=SKILLS[sample_skill]["subject"], focus=sample_skill, tutor=True, count=6)
    h = use_hint(drill["paperId"], 0)
    if not h.get("hint"):
        raise SystemExit("missing hint")
    chk = check_item_answer(drill["paperId"], 0, 0, time_ms=4200, flagged=True)
    if "steps" not in chk or not chk["steps"]:
        raise SystemExit("missing steps in check_item_answer")
    sim = append_similar_question(drill["paperId"], 0)
    if not sim.get("stem"):
        raise SystemExit("append_similar_question failed")

    # Submit the drill (now 7 items because 1 similar was appended)
    submit_paper(drill["paperId"], [0] * 7, used_sec=120, auto=False)
    loaded = get_paper(drill["paperId"])
    if loaded["total"] != 7:
        raise SystemExit("expected 7 items after similar append")

    # 4. Lesson & Mistake Notebook & Home Dashboard
    conn = connect()
    try:
        les = get_lesson_payload(conn, sample_skill)
        if not les.get("lesson", {}).get("concept"):
            raise SystemExit("lesson missing concept")
        nb = mistake_notebook(conn, limit=20)
        if not nb:
            raise SystemExit("expected mistake notebook items after wrong answers")
    finally:
        conn.close()

    dash = home_summary()
    if not dash.get("topics") or not dash.get("studyPlan"):
        raise SystemExit("dashboard missing topics or studyPlan")

    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate question id across papers")
    if len(stems) != len(set(stems)):
        raise SystemExit("duplicate question across mock papers")


def main():
    rc = check_bank([])
    if rc != 0:
        raise SystemExit(rc)
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["TUTOR_DB"] = os.path.join(tmp, "check.db")
        conn = connect()
        conn.close()
        check_papers_and_tutor()
    print(f"self_check passed: {len(TOPICS)} topics · {len(SKILLS)} skills · {len(TEMPLATES)} templates")


if __name__ == "__main__":
    main()
