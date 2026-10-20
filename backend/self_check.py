"""Check that generated papers stay unique and that answers are well formed."""

import os
import tempfile
from collections import Counter

from backend.db import connect
from backend.generate import TEMPLATES, make_reading_group, validate_item
from backend.papers import create_paper, submit_paper


def check_templates():
    for tmpl in TEMPLATES:
        made = 0
        for _ in range(12):
            item = tmpl()
            if item is None:
                continue
            validate_item(item)
            made += 1
        if made < 4:
            raise SystemExit(f"{tmpl.skill} produced only {made} items")
    for _ in range(8):
        group = make_reading_group()
        if not group:
            continue
        passages = {item["passage"] for item in group}
        if len(group) != 3 or len(passages) != 1:
            raise SystemExit("reading group shape is wrong")
        for item in group:
            validate_item(item)


def check_papers():
    stems = []
    ids = []
    for _ in range(2):
        paper = create_paper("math")
        if len(paper["questions"]) != 30:
            raise SystemExit("math paper length")
        topics = Counter(q["topic"] for q in paper["questions"])
        if len(topics) < 6:
            raise SystemExit(f"math topics missing: {topics}")
        stems.extend((q["stem"], q.get("passage") or "") for q in paper["questions"])
        ids.extend(q["id"] for q in paper["questions"])
        _grade_perfect(paper)

    for _ in range(2):
        paper = create_paper("english")
        if len(paper["questions"]) != 30:
            raise SystemExit("english paper length")
        topics = Counter(q["topic"] for q in paper["questions"])
        if set(topics) != {"Grammar/Tenses", "Vocabulary", "Conversation", "Reading"}:
            raise SystemExit(f"english topics: {topics}")
        if topics["Reading"] != 6:
            raise SystemExit("reading count")
        stems.extend((q["stem"], q.get("passage") or "") for q in paper["questions"])
        ids.extend(q["id"] for q in paper["questions"])

    combined = create_paper("combined")
    if len(combined["questions"]) != 60:
        raise SystemExit("combined length")
    if combined["questions"][0]["subject"] != "math" or combined["questions"][30]["subject"] != "english":
        raise SystemExit("combined order")
    stems.extend((q["stem"], q.get("passage") or "") for q in combined["questions"])
    ids.extend(q["id"] for q in combined["questions"])

    practice = create_paper("practice", subject="math", topic="สมการ", timer=False)
    if len(practice["questions"]) != 8 or any(q["topic"] != "สมการ" for q in practice["questions"]):
        raise SystemExit("practice topic filter failed")
    stems.extend((q["stem"], q.get("passage") or "") for q in practice["questions"])
    ids.extend(q["id"] for q in practice["questions"])

    if len(ids) != len(set(ids)):
        raise SystemExit("question ids repeated across papers")
    if len(stems) != len(set(stems)):
        dupes = [stem for stem, n in Counter(stems).items() if n > 1]
        raise SystemExit(f"stems repeated: {dupes[:3]}")

    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT question_id, COUNT(*) AS n
            FROM paper_items
            GROUP BY question_id
            HAVING n > 1
            """
        ).fetchone()
        if row:
            raise SystemExit("database allowed a repeated question")
    finally:
        conn.close()


def _grade_perfect(paper):
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT answer_index FROM paper_items WHERE paper_id = ? ORDER BY position",
            (paper["paperId"],),
        ).fetchall()
    finally:
        conn.close()
    answers = [row["answer_index"] for row in rows]
    result = submit_paper(paper["paperId"], answers, 90, False)
    if result["percent"] != 100 or result["correct"] != 30:
        raise SystemExit(f"perfect paper graded as {result['percent']}")
    answers[0] = (answers[0] + 1) % 4
    again = submit_paper(paper["paperId"], answers, 90, False)
    if again["percent"] != 100:
        raise SystemExit("resubmit changed a finished paper")


def main():
    check_templates()
    check_papers()
    print("self-check ok")


if __name__ == "__main__":
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["QUIZ_DB"] = path
    try:
        main()
    finally:
        os.remove(path)
        for extra in (path + "-wal", path + "-shm"):
            if os.path.exists(extra):
                os.remove(extra)
