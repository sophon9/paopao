"""Validate question-bank content.

    python3 -m backend.bank.check              # everything
    python3 -m backend.bank.check m.geo e.read # only these topics (or skill keys / prefixes)
    python3 -m backend.bank.check m.geo --show 2   # also print 2 sample items per template

Checks per template: it produces valid items (4 distinct choices, a reason +
mistake tag for every wrong choice, hint, steps), runs without exceptions,
and has enough variety to avoid repeats. Per skill: lesson present and at
least one template. Per topic: every difficulty level is reachable.
"""

import sys
from collections import Counter, defaultdict

from backend.bank import SKILLS, TEMPLATES, TOPICS
from backend.bank.core import DIFFICULTIES, run_template, validate_item

RUNS = 60


def _selected(filters):
    if not filters:
        return list(TEMPLATES), set(SKILLS)
    def ok(key):
        return any(key == f or key.startswith(f + ".") or key.startswith(f) for f in filters)
    skills = {k for k in SKILLS if ok(k) or ok(SKILLS[k]["topic"])}
    temps = [t for t in TEMPLATES if t.skill in skills]
    return temps, skills


def _plain(text):
    return text.replace("\n", " ⏎ ")


def show(item):
    print("   ┌", item["skill"], "|", item["difficulty"], "|", item["template"])
    if item.get("passage"):
        print("   │ PASSAGE:", _plain(item["passage"])[:400])
    if item.get("table"):
        print("   │ TABLE:", item["table"])
    if item.get("figure"):
        print("   │ FIGURE: <svg …", len(item["figure"]), "chars>")
    print("   │ Q:", _plain(item["stem"]))
    for i, c in enumerate(item["choices"]):
        mark = "✔" if i == item["answer_index"] else " "
        why = item["why"].get(str(i))
        extra = f"   ← [{why['tag']}] {why['why']}" if why else ""
        print(f"   │ {mark} {i + 1}. {c}{extra}")
    print("   │ HINT:", item["hint"])
    for s in item["steps"]:
        print("   │  •", s)
    print("   └")


def main(argv):
    show_n = 0
    filters = []
    i = 0
    while i < len(argv):
        if argv[i] == "--show":
            show_n = int(argv[i + 1])
            i += 2
            continue
        filters.append(argv[i])
        i += 1

    temps, skills = _selected(filters)
    problems = []
    by_skill = defaultdict(list)
    diff_by_topic = defaultdict(set)
    for t in temps:
        by_skill[t.skill].append(t)
        diff_by_topic[SKILLS[t.skill]["topic"]].add(t.difficulty)

    print(f"{len(TOPICS)} topics · {len(SKILLS)} skills · {len(TEMPLATES)} templates loaded")
    print(f"checking {len(temps)} templates in {len(skills)} skills\n")

    for t in temps:
        made, fps, errors = 0, set(), Counter()
        samples = []
        for _ in range(RUNS):
            try:
                items = run_template(t)
            except Exception as exc:  # noqa: BLE001
                errors[f"{type(exc).__name__}: {exc}"] += 1
                continue
            for item in items:
                try:
                    validate_item(item)
                except ValueError as exc:
                    errors[str(exc)] += 1
                    continue
                made += 1
                fps.add(item["fingerprint"])
                if len(samples) < show_n:
                    samples.append(item)
        variety = len(fps)
        status = "ok "
        if errors:
            status = "ERR"
            problems.append(f"{t.name}: {errors.most_common(2)}")
        elif made < RUNS * 0.5:
            status = "LOW"
            problems.append(f"{t.name}: only {made}/{RUNS} runs made an item")
        elif variety < min(12, made):
            status = "REP"
            problems.append(f"{t.name}: only {variety} distinct items in {made} (needs more variety)")
        print(f"[{status}] {t.skill:<24} {t.difficulty:<9} made {made:>3}/{RUNS}  distinct {variety:>3}  {t.name}")
        for e, n in errors.most_common(3):
            print(f"        ! {n}× {e}")
        for s in samples:
            show(s)

    for sk in sorted(skills):
        if not by_skill.get(sk):
            problems.append(f"skill {sk} has no templates")
        lesson = SKILLS[sk]["lesson"]
        if not lesson.get("example", {}).get("steps"):
            problems.append(f"skill {sk}: lesson example needs steps")

    topics = {SKILLS[s]["topic"] for s in skills}
    for tp in sorted(topics):
        missing = [d for d in DIFFICULTIES if d not in diff_by_topic[tp]]
        if missing:
            problems.append(f"topic {tp} has no templates for: {', '.join(missing)}")

    print()
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    print("all good ✔")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
