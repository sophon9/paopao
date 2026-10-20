"""Core registry for skills, topics and question templates.

Every question in the app is produced by a *template* that belongs to one
*skill*. A skill belongs to one *topic*, and a topic belongs to one subject.
Skills carry a short lesson so the app can teach, not just test.

Content modules (``math_*.py``, ``english_*.py``) only need three things:

    from backend.bank.core import skill, template, mcq, W

    skill("m.frac.add", "m.frac", "บวกลบเศษส่วน", lesson={...})

    @template("m.frac.add", "medium")
    def _():
        ...
        return mcq(stem=..., correct=..., wrongs=[W(...), ...],
                   hint=..., steps=[...])

Text markup understood by the front end (keep it simple):
    [[3/4]]        stacked fraction            [[2 3/4]]  mixed number
    **bold**       bold                        ==text==   underlined/highlighted
    ____           (3+ underscores) an answer blank
    \\n             new line
"""

import hashlib
import random

# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

SUBJECTS = {
    "math": "คณิตศาสตร์",
    "english": "ภาษาอังกฤษ",
}

# Ordered dicts (insertion order is display order).
TOPICS = {}      # key -> {key, subject, name, icon, blurb}
SKILLS = {}      # key -> {key, topic, subject, name, lesson, weight}
TEMPLATES = []   # list of callables with .skill .difficulty .group

DIFFICULTIES = ["easy", "medium", "hard", "challenge"]
DIFF_RANK = {d: i for i, d in enumerate(DIFFICULTIES)}

# Mistake categories. Every wrong choice should carry one of these tags so the
# tutor can tell the student *what kind* of mistake they keep making.
MISTAKE_TAGS = {
    "concept": "เข้าใจหลักการคลาดเคลื่อน",
    "calc": "คำนวณพลาด",
    "partial": "ทำไม่ครบทุกขั้นตอน",
    "misread": "อ่านโจทย์ไม่ละเอียด / ตอบคนละสิ่งที่ถาม",
    "unit": "หน่วยหรือการแปลงหน่วยผิด",
    "sign": "ลืมเครื่องหมายหรือทิศทาง (บวก/ลบ, มาก/น้อย)",
    "formula": "ใช้สูตรผิด",
    "form": "ใช้รูปคำ/รูปกริยาผิด",
    "meaning": "เข้าใจความหมายคำผิด",
    "context": "ไม่ได้ดูบริบทของประโยค/เรื่อง",
    "agreement": "ประธานกับกริยาไม่สอดคล้องกัน",
    "detail": "จับรายละเอียดในเรื่องผิด",
    "inference": "อนุมาน/ตีความเกินจากข้อความ",
    "trap": "ติดกับดักตัวเลือกที่ดูคล้ายถูก",
}


def topic(key, subject, name, icon="", blurb=""):
    """Register a topic. Call once per topic, in display order."""
    if subject not in SUBJECTS:
        raise ValueError(f"unknown subject {subject}")
    TOPICS[key] = {"key": key, "subject": subject, "name": name, "icon": icon, "blurb": blurb}
    return key


def skill(key, topic_key, name, lesson, weight=1.0):
    """Register a skill with its mini lesson.

    lesson = {
        "concept":  "หลักคิดสั้น ๆ 1-3 ประโยค",
        "steps":    ["ขั้นที่ 1 ...", "ขั้นที่ 2 ..."],      # how to solve
        "example":  {"q": "โจทย์ตัวอย่าง", "steps": ["..."], "a": "คำตอบ"},
        "mistakes": ["ข้อผิดพลาดที่พบบ่อย ..."],
        "tips":     ["เคล็ดลับทำข้อสอบเร็ว ..."],
    }
    weight = importance of this skill in a real entrance exam (0.5–2.0).
    """
    if topic_key not in TOPICS:
        raise ValueError(f"skill {key}: unknown topic {topic_key}")
    if key in SKILLS:
        raise ValueError(f"duplicate skill {key}")
    for field in ("concept", "steps", "example", "mistakes", "tips"):
        if field not in lesson:
            raise ValueError(f"skill {key}: lesson missing {field}")
    SKILLS[key] = {
        "key": key,
        "topic": topic_key,
        "subject": TOPICS[topic_key]["subject"],
        "name": name,
        "lesson": lesson,
        "weight": float(weight),
    }
    return key


def template(skill_key, difficulty, group=False):
    """Decorate a generator function.

    The function takes no arguments and returns an item from ``mcq`` (or
    ``None`` to ask for a retry). With ``group=True`` it returns a *list* of
    items that share one passage/figure (reading passages, one chart with
    several questions). Items inside a group may set ``skill=`` themselves.
    """
    if difficulty not in DIFF_RANK:
        raise ValueError(f"bad difficulty {difficulty}")

    def deco(fn):
        fn.skill = skill_key
        fn.difficulty = difficulty
        fn.group = group
        fn.name = f"{fn.__module__}.{fn.__name__}"
        TEMPLATES.append(fn)
        return fn

    return deco


# ---------------------------------------------------------------------------
# Item builder
# ---------------------------------------------------------------------------

class W:
    """A wrong choice with the reason a student would pick it.

    W("5/7", "นำตัวเศษบวกกันและตัวส่วนบวกกัน ซึ่งทำไม่ได้", "concept")
    """

    __slots__ = ("text", "why", "tag")

    def __init__(self, text, why, tag="concept"):
        if tag not in MISTAKE_TAGS:
            raise ValueError(f"unknown mistake tag {tag}")
        self.text = str(text).strip()
        self.why = str(why).strip()
        self.tag = tag


def mcq(*, stem, correct, wrongs, hint, steps, passage=None, figure=None, table=None,
        skill=None, difficulty=None, group_key=None, extra_wrongs=None):
    """Build one multiple-choice item with exactly four choices.

    stem     question text (markup allowed)
    correct  correct choice text
    wrongs   list of ``W`` — the best 3 distinct ones are used. Put the most
             tempting (most common mistake) first.
    extra_wrongs  optional plain fallback strings used only if ``wrongs`` has
             fewer than three distinct options (reason = generic).
    hint     one nudge that does not give the answer away
    steps    list of solution steps (each a short sentence), last step states
             the answer
    passage  optional reading passage / shared context text
    figure   optional SVG string (see ``backend.bank.svg``)
    table    optional {"head": [...], "rows": [[...], ...], "caption": "..."}

    Returns ``None`` when the item cannot be made (template should retry).
    """
    correct = str(correct).strip()
    if not correct or not str(stem).strip() or not str(hint).strip():
        return None
    if isinstance(steps, str):
        steps = [steps]
    steps = [str(s).strip() for s in steps if str(s).strip()]
    if not steps:
        return None

    picked = []
    seen = {_norm(correct)}
    pool = list(wrongs or [])
    for raw in extra_wrongs or []:
        pool.append(W(raw, "ตัวเลือกนี้ไม่ตรงกับเงื่อนไขของโจทย์ ลองเทียบกับวิธีทำที่ถูกทีละขั้น", "trap"))
    for w in pool:
        if not isinstance(w, W):
            w = W(w, "ตัวเลือกนี้ไม่ตรงกับเงื่อนไขของโจทย์ ลองเทียบกับวิธีทำที่ถูกทีละขั้น", "trap")
        key = _norm(w.text)
        if not w.text or key in seen:
            continue
        seen.add(key)
        picked.append(w)
        if len(picked) == 3:
            break
    if len(picked) < 3:
        return None

    choices = [correct] + [w.text for w in picked]
    order = list(range(4))
    random.shuffle(order)
    shuffled = [choices[i] for i in order]
    answer_index = order.index(0)
    why = {}
    for new_pos, old_pos in enumerate(order):
        if old_pos == 0:
            continue
        w = picked[old_pos - 1]
        why[str(new_pos)] = {"why": w.why, "tag": w.tag}

    return {
        "stem": str(stem).strip(),
        "passage": passage.strip() if isinstance(passage, str) and passage.strip() else None,
        "figure": figure or None,
        "table": table or None,
        "choices": shuffled,
        "answer_index": answer_index,
        "why": why,
        "hint": str(hint).strip(),
        "steps": steps,
        "skill": skill,
        "difficulty": difficulty,
        "group_key": group_key,
    }


def _norm(text):
    return " ".join(str(text).split()).lower()


def finalize(item, tmpl):
    """Fill skill/topic/subject/difficulty from the template and fingerprint it."""
    if item is None:
        return None
    sk = item.get("skill") or tmpl.skill
    if sk not in SKILLS:
        raise ValueError(f"{tmpl.name}: unknown skill {sk}")
    meta = SKILLS[sk]
    item["skill"] = sk
    item["topic"] = meta["topic"]
    item["subject"] = meta["subject"]
    item["difficulty"] = item.get("difficulty") or tmpl.difficulty
    item["template"] = tmpl.name
    identity = "\n".join([
        sk,
        item["stem"],
        item.get("passage") or "",
        item.get("figure") or "",
        repr(item.get("table") or ""),
        item["choices"][item["answer_index"]],
    ])
    item["fingerprint"] = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return item


def run_template(tmpl):
    """Run a template once. Returns a list of finalized items (maybe empty)."""
    out = tmpl()
    if out is None:
        return []
    items = out if tmpl.group else [out]
    if any(i is None for i in items):
        return []
    import uuid

    gk = uuid.uuid4().hex[:12] if tmpl.group else None
    done = []
    for item in items:
        if gk and not item.get("group_key"):
            item["group_key"] = gk
        done.append(finalize(item, tmpl))
    return done


def validate_item(item):
    """Raise ValueError if an item is malformed. Used by self_check and at build time."""
    if item is None:
        raise ValueError("empty item")
    ch = item["choices"]
    if len(ch) != 4 or len({_norm(c) for c in ch}) != 4:
        raise ValueError(f"{item.get('template')}: choices must be 4 distinct: {ch}")
    idx = item["answer_index"]
    if not isinstance(idx, int) or not 0 <= idx < 4:
        raise ValueError("bad answer index")
    for key in ("stem", "hint", "fingerprint", "skill", "topic", "subject"):
        if not item.get(key):
            raise ValueError(f"{item.get('template')}: missing {key}")
    if not item["steps"]:
        raise ValueError(f"{item.get('template')}: missing steps")
    if set(item["why"].keys()) != {str(i) for i in range(4) if i != idx}:
        raise ValueError(f"{item.get('template')}: every wrong choice needs a reason")
    for w in item["why"].values():
        if not w["why"] or w["tag"] not in MISTAKE_TAGS:
            raise ValueError(f"{item.get('template')}: bad wrong-choice reason {w}")
    if item["difficulty"] not in DIFF_RANK:
        raise ValueError("bad difficulty")
    if item.get("figure") and not str(item["figure"]).lstrip().startswith("<svg"):
        raise ValueError(f"{item.get('template')}: figure must be an <svg> string")
    t = item.get("table")
    if t is not None:
        if not isinstance(t, dict) or "rows" not in t:
            raise ValueError("table must be a dict with rows")


# ---------------------------------------------------------------------------
# Small helpers shared by content modules
# ---------------------------------------------------------------------------

def num(n):
    """Format an integer with thousands separators: 12345 -> '12,345'."""
    n = int(n)
    return f"{n:,}"


def dec(x, places=2):
    """Format a float/Fraction as a short decimal: 2.50 -> '2.5', 3.0 -> '3'."""
    s = f"{float(x):,.{places}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def frac(fr, mixed=False):
    """Markup for a Fraction: Fraction(3,4) -> '[[3/4]]'; whole numbers stay plain.

    mixed=True turns 7/4 into '[[1 3/4]]'.
    """
    from fractions import Fraction

    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    sign = "-" if fr < 0 else ""
    a = abs(fr)
    if mixed and a > 1:
        whole = a.numerator // a.denominator
        rest = a - whole
        return f"{sign}[[{whole} {rest.numerator}/{rest.denominator}]]"
    return f"{sign}[[{a.numerator}/{a.denominator}]]"


def pick(seq, k=None):
    return random.choice(seq) if k is None else random.sample(seq, k)


NAMES_TH = ["มินตรา", "ภูมิ", "อาร์ม", "แพรวา", "ธนัท", "ขวัญข้าว", "ปิ่น", "กันต์", "มีนา", "ต้นกล้า",
            "ใบเตย", "ภาคิน", "ณิชา", "ปัณณ์", "พลอย", "ก้อง", "ฟ้าใส", "ธีร์"]
NAMES_EN = [("Amy", "she"), ("Ben", "he"), ("Cindy", "she"), ("David", "he"), ("Emma", "she"),
            ("Frank", "he"), ("Grace", "she"), ("Henry", "he"), ("Ivy", "she"), ("Jack", "he"),
            ("Kate", "she"), ("Leo", "he"), ("Mali", "she"), ("Nat", "he"), ("Ploy", "she"), ("Tom", "he")]


def name_th(k=None):
    return pick(NAMES_TH, k)


def name_en():
    """Returns (name, subject pronoun lower-case)."""
    return pick(NAMES_EN)
