"""Original Suankularb-style items.

Math answers are computed, then checked, before an item is kept.
English items come from graded-level frames whose correct choice is fixed
by the grammar or the facts in the passage. Nothing here is copied from
a published exam.

Fingerprints include the full stem, passage, and correct choice, so the
same item is never stored twice. Display order of choices is shuffled
and is not part of identity.
"""

import hashlib
import random
import uuid
from fractions import Fraction

from backend.db import fingerprint_exists

MATH_TOPICS = [
    "จำนวนและการดำเนินการ",
    "ทศนิยมเศษส่วน",
    "อัตราส่วนร้อยละ",
    "สมการ",
    "เรขาคณิตพื้นที่ปริมาตร",
    "สถิติโจทย์ปัญหา",
]

ENG_TOPICS = [
    "Grammar/Tenses",
    "Vocabulary",
    "Conversation",
    "Reading",
]

TOPICS = {"math": MATH_TOPICS, "english": ENG_TOPICS}

TEMPLATES = []

NAMES_TH = ["มินตรา", "ภูมิ", "อาร์ม", "แพร", "ธนัท", "ขวัญ", "ปิ่น", "โอฬาร", "มีนา", "ต้นน้ำ"]
NAMES_EN = [
    ("Amy", "She", "her"),
    ("Ben", "He", "his"),
    ("Cindy", "She", "her"),
    ("David", "He", "his"),
    ("Emma", "She", "her"),
    ("Frank", "He", "his"),
    ("Gina", "She", "her"),
    ("Harry", "He", "his"),
    ("Ivy", "She", "her"),
    ("Jack", "He", "his"),
]


def template(topic, difficulty, skill):
    def deco(fn):
        fn.topic = topic
        fn.difficulty = difficulty
        fn.skill = skill
        TEMPLATES.append(fn)
        return fn

    return deco


def num(n):
    return f"{int(n):,}"


def show_frac(fr):
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"


def show_dec(fr):
    fr = Fraction(fr)
    whole = fr.numerator // fr.denominator
    rem = abs(fr.numerator) % fr.denominator
    digits = []
    seen = {}
    value = rem
    while value and len(digits) < 6:
        if value in seen:
            break
        seen[value] = len(digits)
        value *= 10
        digits.append(str(value // fr.denominator))
        value %= fr.denominator
    body = "".join(digits).rstrip("0")
    if not body:
        return str(whole)
    sign = "-" if fr < 0 and whole == 0 else ""
    return f"{sign}{whole}.{body}" if whole or sign else f"0.{body}"


def mcq(*, subject, topic, difficulty, skill, stem, correct, wrongs, explanation, passage=None, group_key=None):
    correct = str(correct).strip()
    cleaned = []
    seen = {correct}
    for raw in wrongs:
        text = str(raw).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
        if len(cleaned) == 3:
            break
    if len(cleaned) < 3 or not correct or not str(stem).strip() or not str(explanation).strip():
        return None
    choices = [correct, *cleaned]
    random.shuffle(choices)
    identity = "\n".join([subject, str(stem).strip(), passage or "", correct])
    fingerprint = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return {
        "fingerprint": fingerprint,
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "skill": skill,
        "stem": str(stem).strip(),
        "passage": passage,
        "group_key": group_key,
        "choices": choices,
        "answer_index": choices.index(correct),
        "explanation": str(explanation).strip(),
    }


def validate_item(item):
    if item is None:
        raise ValueError("empty item")
    choices = item["choices"]
    if len(choices) != 4 or len(set(choices)) != 4:
        raise ValueError(f"bad choices for {item.get('skill')}: {choices}")
    idx = item["answer_index"]
    if not isinstance(idx, int) or not 0 <= idx < 4:
        raise ValueError("bad answer index")
    if not item["stem"] or not item["explanation"] or not item["fingerprint"]:
        raise ValueError("missing text")
    if item["subject"] == "english" and item["topic"] == "Reading":
        passage = item["passage"] or ""
        correct = choices[idx]
        if correct not in passage:
            raise ValueError(f"reading answer not in passage: {correct}")
        for wrong in choices:
            if wrong != correct and wrong in passage:
                raise ValueError(f"reading distractor leaked into passage: {wrong}")


def _fresh(conn, item, batch):
    if item is None:
        return False
    if item["fingerprint"] in batch:
        return False
    if conn is not None and fingerprint_exists(conn, item["fingerprint"]):
        return False
    return True


def generate_one(conn, topic, difficulty, used_skills, batch):
    matching = [t for t in TEMPLATES if t.topic == topic]
    if not matching:
        raise RuntimeError(f"no templates for {topic}")
    preferred = [t for t in matching if t.difficulty == difficulty] or matching
    for attempt in range(80):
        pool = preferred
        unused = [t for t in pool if t.skill not in used_skills]
        if unused and attempt < 50:
            pool = unused
        tmpl = random.choice(pool)
        item = tmpl()
        if not _fresh(conn, item, batch):
            continue
        if item["skill"] in used_skills and unused and attempt < 50:
            continue
        validate_item(item)
        batch.add(item["fingerprint"])
        used_skills.add(item["skill"])
        return item
    raise RuntimeError(f"could not build a new {topic} item")


def difficulties(n):
    pattern = ["easy", "medium", "medium", "hard"]
    return [pattern[i % len(pattern)] for i in range(n)]


def _pick_person():
    return random.choice(NAMES_EN)


# ---------------------------------------------------------------------------
# Math — จำนวนและการดำเนินการ
# ---------------------------------------------------------------------------

@template("จำนวนและการดำเนินการ", "easy", "add-4digit")
def t_add():
    a = random.randint(1000, 8999)
    b = random.randint(1000, 9999)
    ans = a + b
    if ans != a + b:
        return None
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="easy",
        skill="add-4digit",
        stem=f"ผลบวกของ {num(a)} + {num(b)} เท่ากับเท่าใด",
        correct=num(ans),
        wrongs=[num(ans + 10), num(ans - 10), num(ans + 100), num(a + b + 1000), num(abs(a - b))],
        explanation=f"จัดหลักแล้วบวก: {num(a)} + {num(b)} = {num(ans)}",
    )


@template("จำนวนและการดำเนินการ", "easy", "sub-4digit")
def t_sub():
    a = random.randint(4000, 9999)
    b = random.randint(1000, a - 150)
    ans = a - b
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="easy",
        skill="sub-4digit",
        stem=f"ผลลบของ {num(a)} − {num(b)} เท่ากับเท่าใด",
        correct=num(ans),
        wrongs=[num(a + b), num(ans + 10), num(ans + 100), num(max(1, ans - 100)), num(b - a if b > a else ans + 9)],
        explanation=f"ตั้งลบแล้วกระจายเมื่อหลักไม่พอ: {num(a)} − {num(b)} = {num(ans)}",
    )


@template("จำนวนและการดำเนินการ", "medium", "mul-2digit")
def t_mul():
    a = random.randint(12, 48)
    b = random.randint(12, 36)
    ans = a * b
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="medium",
        skill="mul-2digit",
        stem=f"ผลคูณของ {a} × {b} เท่ากับเท่าใด",
        correct=num(ans),
        wrongs=[num(a * (b + 1)), num((a + 1) * b), num(a + b), num(a * (b - 1)), num(ans + 10)],
        explanation=f"คูณทีละหลักแล้วบวก: {a} × {b} = {num(ans)}",
    )


@template("จำนวนและการดำเนินการ", "medium", "div-exact")
def t_div():
    divisor = random.randint(4, 12)
    quot = random.randint(18, 90)
    total = divisor * quot
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="medium",
        skill="div-exact",
        stem=f"{num(total)} ÷ {divisor} เท่ากับเท่าใด",
        correct=num(quot),
        wrongs=[num(quot + 1), num(max(1, quot - 1)), num(quot + divisor), num(total - divisor), num(quot * 2)],
        explanation=f"เพราะ {divisor} × {quot} = {num(total)} ดังนั้น {num(total)} ÷ {divisor} = {quot}",
    )


@template("จำนวนและการดำเนินการ", "medium", "order-ops")
def t_order():
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    c = random.randint(2, 9)
    ans = a + b * c
    left_first = (a + b) * c
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="medium",
        skill="order-ops",
        stem=f"ค่าของ {a} + {b} × {c} เท่ากับเท่าใด",
        correct=str(ans),
        wrongs=[str(left_first), str(a * b + c), str(a * b * c), str(a + b + c), str(ans + b)],
        explanation=f"คูณก่อนบวก: {b} × {c} = {b * c} แล้ว {a} + {b * c} = {ans} ไม่ใช่ ({a} + {b}) × {c} = {left_first}",
    )


@template("จำนวนและการดำเนินการ", "medium", "gcd")
def t_gcd():
    g = random.choice([2, 3, 4, 5, 6, 8, 9, 12])
    x = random.randint(2, 9)
    y = random.randint(2, 9)
    if x == y:
        y += 1
    a, b = g * x, g * y
    from math import gcd as math_gcd
    from math import lcm as math_lcm

    ans = math_gcd(a, b)
    if ans != g and math_gcd(x, y) != 1:
        ans = math_gcd(a, b)
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="medium",
        skill="gcd",
        stem=f"ห.ร.ม. ของ {a} และ {b} เท่ากับเท่าใด",
        correct=str(ans),
        wrongs=[str(math_lcm(a, b)), str(max(1, ans // 2)), str(ans * 2), str(x), str(y), str(a + b)],
        explanation=f"ตัวหารร่วมมากของ {a} และ {b} คือ {ans} เพราะ {a} = {ans} × {a // ans} และ {b} = {ans} × {b // ans}",
    )


@template("จำนวนและการดำเนินการ", "medium", "lcm")
def t_lcm():
    from math import gcd as math_gcd
    from math import lcm as math_lcm

    a = random.randint(4, 16)
    b = random.randint(4, 16)
    if a == b:
        b += 2
    ans = math_lcm(a, b)
    g = math_gcd(a, b)
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="medium",
        skill="lcm",
        stem=f"ค.ร.น. ของ {a} และ {b} เท่ากับเท่าใด",
        correct=str(ans),
        wrongs=[str(a * b), str(g), str(a + b), str(max(a, b)), str(ans + a)],
        explanation=f"ค.ร.น. คือพหุคูณร่วมน้อย: {a} × {b} ÷ ห.ร.ม. {g} = {ans}",
    )


@template("จำนวนและการดำเนินการ", "medium", "which-prime")
def t_prime():
    def is_prime(n):
        if n < 2:
            return False
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
        return True

    primes = [n for n in range(11, 97) if is_prime(n)]
    composites = [n for n in range(12, 96) if not is_prime(n)]
    prime = random.choice(primes)
    comps = random.sample([n for n in composites if n != prime], 3)
    nums = [prime, *comps]
    if sum(1 for n in nums if is_prime(n)) != 1:
        return None
    listed = ", ".join(str(n) for n in sorted(nums))
    why = ", ".join(f"{n}={_factor_hint(n)}" for n in sorted(comps))
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="medium",
        skill="which-prime",
        stem=f"จำนวนใดเป็นจำนวนเฉพาะ จาก {listed}",
        correct=str(prime),
        wrongs=[str(n) for n in comps],
        explanation=f"{prime} หารลงตัวเฉพาะ 1 และตัวเอง ส่วนจำนวนอื่นแยกตัวประกอบได้ เช่น {why}",
    )


def _factor_hint(n):
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return f"{d}×{n // d}"
    return str(n)


@template("จำนวนและการดำเนินการ", "easy", "integers-between")
def t_between():
    lo = random.randint(-15, 4)
    hi = lo + random.randint(4, 9)
    vals = list(range(lo + 1, hi))
    ans = len(vals)
    if ans != hi - lo - 1 or ans < 3:
        return None
    shown = ", ".join(str(v) for v in vals)
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="easy",
        skill="integers-between",
        stem=f"จำนวนเต็มที่อยู่ระหว่าง {lo} และ {hi} มีกี่จำนวน",
        correct=str(ans),
        wrongs=[str(ans + 1), str(ans - 1), str(hi - lo), str(ans + 2), str(abs(hi) + abs(lo))],
        explanation=f"ระหว่าง {lo} กับ {hi} คือ {shown} รวม {ans} จำนวน ไม่นับหัวท้าย",
    )


@template("จำนวนและการดำเนินการ", "medium", "square")
def t_square():
    a = random.randint(6, 25)
    b = random.randint(2, 9)
    kind = random.choice(["square", "sum", "diff"])
    if kind == "square":
        ans = a * a
        stem = f"ค่าของ {a}² เท่ากับเท่าใด"
        explain = f"{a} × {a} = {ans}"
        wrongs = [str((a - 1) ** 2), str((a + 1) ** 2), str(a * 2), str(a * a + a)]
    elif kind == "sum":
        ans = a * a + b * b
        stem = f"ค่าของ {a}² + {b}² เท่ากับเท่าใด"
        explain = f"{a}² = {a * a} และ {b}² = {b * b} รวมเป็น {ans}"
        wrongs = [str((a + b) ** 2), str(a * a + b), str(a + b * b), str(ans + 2)]
    else:
        if a * a <= b * b:
            return None
        ans = a * a - b * b
        stem = f"ค่าของ {a}² − {b}² เท่ากับเท่าใด"
        explain = f"{a * a} − {b * b} = {ans} ซึ่งเท่ากับ ({a} − {b})({a} + {b}) = {(a - b) * (a + b)}"
        wrongs = [str((a - b) ** 2), str(a * a + b * b), str(a - b), str(ans + b)]
    if ans < 0:
        return None
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="medium",
        skill="square",
        stem=stem,
        correct=str(ans),
        wrongs=wrongs,
        explanation=explain,
    )


@template("จำนวนและการดำเนินการ", "hard", "money-steps")
def t_money_steps():
    name = random.choice(NAMES_TH)
    books = random.randint(2, 5)
    book_price = random.choice([15, 18, 20, 25, 28, 32])
    pencils = random.randint(2, 6)
    pencil_price = random.choice([5, 6, 7, 8, 9])
    ans = books * book_price + pencils * pencil_price
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="hard",
        skill="money-steps",
        stem=(
            f"{name}ซื้อสมุด {books} เล่ม เล่มละ {book_price} บาท "
            f"และดินสอ {pencils} แท่ง แท่งละ {pencil_price} บาท ต้องจ่ายทั้งหมดกี่บาท"
        ),
        correct=str(ans),
        wrongs=[
            str(books * book_price + pencil_price),
            str(book_price + pencils * pencil_price),
            str(books * pencils * book_price),
            str((books + pencils) * book_price),
            str(ans + book_price),
        ],
        explanation=(
            f"สมุด {books} × {book_price} = {books * book_price} บาท "
            f"ดินสอ {pencils} × {pencil_price} = {pencils * pencil_price} บาท "
            f"รวม {books * book_price} + {pencils * pencil_price} = {ans} บาท"
        ),
    )


@template("จำนวนและการดำเนินการ", "hard", "change")
def t_change():
    name = random.choice(NAMES_TH)
    paid = random.choice([100, 200, 500, 1000])
    cost = random.randint(paid // 5, paid - 15)
    ans = paid - cost
    return mcq(
        subject="math",
        topic="จำนวนและการดำเนินการ",
        difficulty="hard",
        skill="change",
        stem=f"{name}จ่ายแบงก์ {num(paid)} บาท เพื่อซื้อของราคา {num(cost)} บาท จะได้รับเงินทอนกี่บาท",
        correct=num(ans),
        wrongs=[num(paid + cost), num(ans + 10), num(max(0, ans - 10)), num(cost), num(paid // 2)],
        explanation=f"เงินทอน = เงินที่จ่าย − ราคาสินค้า = {num(paid)} − {num(cost)} = {num(ans)} บาท",
    )


# ---------------------------------------------------------------------------
# Math — ทศนิยมเศษส่วน
# ---------------------------------------------------------------------------

_TERM = [
    Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5),
    Fraction(3, 5), Fraction(4, 5), Fraction(1, 8), Fraction(3, 8), Fraction(5, 8),
    Fraction(7, 8), Fraction(1, 20), Fraction(3, 20), Fraction(1, 25), Fraction(3, 25),
]


@template("ทศนิยมเศษส่วน", "easy", "frac-to-dec")
def t_frac_dec():
    fr = random.choice(_TERM)
    correct = show_dec(fr)
    wrongs = [show_dec(fr + Fraction(1, 10)), show_dec(Fraction(fr.numerator, fr.denominator + 1)), show_dec(1 - fr), "0." + str(fr.numerator)]
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="easy",
        skill="frac-to-dec",
        stem=f"เศษส่วน {show_frac(fr)} เขียนเป็นทศนิยมได้เท่าใด",
        correct=correct,
        wrongs=wrongs,
        explanation=f"{fr.numerator} ÷ {fr.denominator} = {correct}",
    )


@template("ทศนิยมเศษส่วน", "easy", "dec-to-frac")
def t_dec_frac():
    fr = random.choice(_TERM)
    dec = show_dec(fr)
    unsimplified = f"{fr.numerator * 2}/{fr.denominator * 2}"
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="easy",
        skill="dec-to-frac",
        stem=f"{dec} เขียนเป็นเศษส่วนอย่างต่ำได้เท่าใด",
        correct=show_frac(fr),
        wrongs=[
            unsimplified,
            show_frac(Fraction(fr.denominator, fr.numerator)) if fr.numerator != 1 else show_frac(fr + Fraction(1, 5)),
            show_frac(fr + Fraction(1, 10)),
            show_frac(Fraction(fr.numerator, 10)),
            show_frac(1 - fr) if fr != Fraction(1, 2) else "2/5",
        ],
        explanation=f"{dec} = {show_frac(fr)} เมื่อทำให้เป็นเศษส่วนอย่างต่ำแล้ว",
    )


@template("ทศนิยมเศษส่วน", "medium", "add-frac")
def t_add_frac():
    a = Fraction(random.randint(1, 5), random.randint(2, 9))
    b = Fraction(random.randint(1, 5), random.randint(2, 9))
    if a.denominator == b.denominator:
        b = Fraction(b.numerator, b.denominator + 1)
    ans = a + b
    if ans >= 2:
        return None
    wrong_add_den = Fraction(a.numerator + b.numerator, a.denominator + b.denominator)
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="medium",
        skill="add-frac",
        stem=f"ผลบวกของ {show_frac(a)} + {show_frac(b)} เท่ากับเท่าใด",
        correct=show_frac(ans),
        wrongs=[
            show_frac(wrong_add_den),
            f"{a.numerator + b.numerator}/{a.denominator * b.denominator}",
            show_frac(abs(a - b)) if a != b else show_frac(ans + Fraction(1, 15)),
            show_frac(a * b),
            show_frac(ans + Fraction(1, a.denominator * b.denominator)),
        ],
        explanation=(
            f"ทำส่วนให้เท่ากัน: {show_frac(a)} + {show_frac(b)} "
            f"= {a.numerator * b.denominator}/{a.denominator * b.denominator} + {b.numerator * a.denominator}/{a.denominator * b.denominator} "
            f"= {show_frac(ans)}"
        ),
    )


@template("ทศนิยมเศษส่วน", "medium", "sub-frac")
def t_sub_frac():
    a = Fraction(random.randint(2, 8), random.randint(3, 9))
    b = Fraction(random.randint(1, 4), random.randint(3, 9))
    if b >= a:
        a, b = a + 1, b
    if b >= a:
        return None
    ans = a - b
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="medium",
        skill="sub-frac",
        stem=f"ผลลบของ {show_frac(a)} − {show_frac(b)} เท่ากับเท่าใด",
        correct=show_frac(ans),
        wrongs=[
            show_frac(Fraction(abs(a.numerator - b.numerator), a.denominator + b.denominator)),
            show_frac(a + b),
            show_frac(Fraction(a.numerator * b.denominator - b.numerator * a.denominator, a.denominator + b.denominator)),
            show_frac(ans + Fraction(1, 12)),
            f"{abs(a.numerator - b.numerator)}/{a.denominator * b.denominator}",
        ],
        explanation=f"ทำส่วนให้เท่ากันก่อนลบ แล้วทำเป็นอย่างต่ำ ได้ {show_frac(ans)}",
    )


@template("ทศนิยมเศษส่วน", "medium", "mul-frac")
def t_mul_frac():
    a = Fraction(random.randint(1, 5), random.randint(2, 8))
    b = Fraction(random.randint(1, 5), random.randint(2, 8))
    ans = a * b
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="medium",
        skill="mul-frac",
        stem=f"ผลคูณของ {show_frac(a)} × {show_frac(b)} เท่ากับเท่าใด",
        correct=show_frac(ans),
        wrongs=[
            f"{a.numerator * b.numerator}/{a.denominator + b.denominator}",
            show_frac(a + b),
            show_frac(Fraction(a.numerator * b.denominator, a.denominator * b.numerator)) if b.numerator else "1/2",
            show_frac(ans + Fraction(1, 8)),
            f"{a.numerator + b.numerator}/{a.denominator * b.denominator}",
        ],
        explanation=f"คูณเศษกับเศษ และส่วนกับส่วน แล้วทำอย่างต่ำ: {show_frac(a)} × {show_frac(b)} = {show_frac(ans)}",
    )


@template("ทศนิยมเศษส่วน", "hard", "div-frac")
def t_div_frac():
    a = Fraction(random.randint(1, 5), random.randint(2, 7))
    b = Fraction(random.randint(1, 4), random.randint(2, 7))
    ans = a / b
    if ans > 4:
        return None
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="hard",
        skill="div-frac",
        stem=f"ผลหารของ {show_frac(a)} ÷ {show_frac(b)} เท่ากับเท่าใด",
        correct=show_frac(ans),
        wrongs=[
            show_frac(a * b),
            show_frac(b / a) if a != b else show_frac(ans + 1),
            f"{a.numerator * b.numerator}/{a.denominator * b.denominator}",
            show_frac(ans + Fraction(1, 2)),
            show_frac(Fraction(a.numerator, b.numerator)),
        ],
        explanation=f"การหารเศษส่วนคือคูณด้วยส่วนกลับ: {show_frac(a)} × {show_frac(Fraction(b.denominator, b.numerator))} = {show_frac(ans)}",
    )


@template("ทศนิยมเศษส่วน", "medium", "frac-of-whole")
def t_frac_of():
    den = random.choice([2, 4, 5, 8, 10])
    nume = random.randint(1, den - 1)
    whole = den * random.randint(3, 12)
    ans = whole * nume // den
    fr = Fraction(nume, den)
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="medium",
        skill="frac-of-whole",
        stem=f"{show_frac(fr)} ของ {whole} เท่ากับเท่าใด",
        correct=str(ans),
        wrongs=[str(whole // den), str(whole - ans), str(ans + den), str(nume * den), str(whole // nume if whole % nume == 0 and whole // nume != ans else ans + 2)],
        explanation=f"{show_frac(fr)} ของ {whole} = {whole} ÷ {den} × {nume} = {whole // den} × {nume} = {ans}",
    )


@template("ทศนิยมเศษส่วน", "hard", "greatest-frac")
def t_greatest_frac():
    fracs = []
    guard = 0
    while len(fracs) < 4 and guard < 40:
        guard += 1
        fr = Fraction(random.randint(1, 8), random.randint(3, 12))
        if fr >= 1 or fr in fracs:
            continue
        fracs.append(fr)
    if len(fracs) < 4 or len(set(fracs)) < 4:
        return None
    best = max(fracs)
    listed = ", ".join(show_frac(fr) for fr in sorted(fracs, key=lambda f: (f.numerator, f.denominator)))
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="hard",
        skill="greatest-frac",
        stem=f"เศษส่วนใดมีค่ามากที่สุด จาก {listed}",
        correct=show_frac(best),
        wrongs=[show_frac(fr) for fr in fracs if fr != best],
        explanation=(
            "เทียบโดยคูณไขว้หรือทำส่วนให้เท่ากัน จะได้ "
            + " < ".join(show_frac(fr) for fr in sorted(fracs))
            + f" ดังนั้นค่ามากที่สุดคือ {show_frac(best)}"
        ),
    )


@template("ทศนิยมเศษส่วน", "medium", "mixed-to-improper")
def t_mixed():
    whole = random.randint(2, 8)
    den = random.randint(3, 9)
    nume = random.randint(1, den - 1)
    ans = Fraction(whole * den + nume, den)
    return mcq(
        subject="math",
        topic="ทศนิยมเศษส่วน",
        difficulty="medium",
        skill="mixed-to-improper",
        stem=f"จำนวนคละ {whole} {nume}/{den} เขียนเป็นเศษเกินได้เท่าใด",
        correct=show_frac(ans),
        wrongs=[
            f"{whole * nume}/{den}",
            f"{whole + nume}/{den}",
            f"{whole * den}/{nume}",
            f"{whole * den + nume}/{nume}",
            show_frac(Fraction(whole * den - nume, den)),
        ],
        explanation=f"เศษเกิน = (จำนวนเต็ม × ส่วน + เศษ) / ส่วน = ({whole} × {den} + {nume})/{den} = {show_frac(ans)}",
    )


# ---------------------------------------------------------------------------
# Math — อัตราส่วนร้อยละ
# ---------------------------------------------------------------------------

@template("อัตราส่วนร้อยละ", "easy", "simplify-ratio")
def t_ratio():
    g = random.choice([2, 3, 4, 5, 6])
    x = random.randint(1, 7)
    y = random.randint(1, 7)
    if x == y:
        y += 1
    from math import gcd as math_gcd

    left, right = g * x, g * y
    gg = math_gcd(left, right)
    ans = f"{left // gg}:{right // gg}"
    return mcq(
        subject="math",
        topic="อัตราส่วนร้อยละ",
        difficulty="easy",
        skill="simplify-ratio",
        stem=f"อัตราส่วน {left}:{right} ทำเป็นอัตราส่วนอย่างต่ำได้เท่าใด",
        correct=ans,
        wrongs=[
            f"{left}:{right}",
            f"{right // gg}:{left // gg}",
            f"{left // gg + 1}:{right // gg}",
            f"{x}:{y + 1}",
            f"{left // g}:{right}",
        ],
        explanation=f"หารทั้งสองจำนวนด้วย ห.ร.ม. {gg} ได้ {ans}",
    )


@template("อัตราส่วนร้อยละ", "medium", "share-ratio")
def t_share():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    if a == b:
        b += 1
    parts = a + b
    unit = random.randint(4, 18)
    total = parts * unit
    ask_first = random.choice([True, False])
    ans = unit * (a if ask_first else b)
    other = total - ans
    name = random.choice(NAMES_TH)
    who = "คนแรก" if ask_first else "คนที่สอง"
    return mcq(
        subject="math",
        topic="อัตราส่วนร้อยละ",
        difficulty="medium",
        skill="share-ratio",
        stem=f"แบ่งเงิน {total} บาท ในอัตราส่วน {a}:{b} {who}จะได้กี่บาท",
        correct=str(ans),
        wrongs=[str(other), str(unit), str(total // max(a, 1)), str(ans + unit), str(a * b * unit)],
        explanation=(
            f"ส่วนรวม {a}+{b} = {parts} ส่วน ส่วนละ {total}÷{parts} = {unit} บาท "
            f"{who}ได้ {a if ask_first else b} ส่วน = {ans} บาท"
        ),
    )


@template("อัตราส่วนร้อยละ", "easy", "percent-of")
def t_percent_of():
    percent = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
    base = random.choice([40, 60, 80, 100, 120, 150, 200, 240, 400])
    ans = base * percent // 100
    return mcq(
        subject="math",
        topic="อัตราส่วนร้อยละ",
        difficulty="easy",
        skill="percent-of",
        stem=f"{percent}% ของ {base} เท่ากับเท่าใด",
        correct=str(ans),
        wrongs=[str(base // percent if percent and base % percent == 0 else ans + 5), str(percent), str(ans + base // 10), str(base - ans), str(ans * 2)],
        explanation=f"{percent}% = {percent}/100 ดังนั้น {base} × {percent}/100 = {ans}",
    )


@template("อัตราส่วนร้อยละ", "medium", "what-percent")
def t_what_percent():
    percent = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
    base = random.choice([20, 40, 50, 80, 100, 120, 200])
    part = base * percent // 100
    return mcq(
        subject="math",
        topic="อัตราส่วนร้อยละ",
        difficulty="medium",
        skill="what-percent",
        stem=f"{part} เป็นกี่เปอร์เซ็นต์ของ {base}",
        correct=f"{percent}%",
        wrongs=[f"{percent + 5}%", f"{percent // 2 or 5}%", f"{part}%", f"{100 - percent}%", f"{percent + 10}%"],
        explanation=f"({part} ÷ {base}) × 100 = {percent}%",
    )


@template("อัตราส่วนร้อยละ", "medium", "discount")
def t_discount():
    price = random.choice([200, 250, 400, 500, 800, 1000, 1200, 1500])
    percent = random.choice([10, 15, 20, 25, 30])
    off = price * percent // 100
    ans = price - off
    return mcq(
        subject="math",
        topic="อัตราส่วนร้อยละ",
        difficulty="medium",
        skill="discount",
        stem=f"สินค้าราคา {num(price)} บาท ลดราคา {percent}% จะขายในราคาเท่าใด",
        correct=num(ans),
        wrongs=[num(off), num(price + off), num(ans - off if ans > off else ans + 10), num(price - percent), num(ans + 10)],
        explanation=f"ส่วนลด = {num(price)} × {percent}% = {num(off)} บาท ราคาขาย = {num(price)} − {num(off)} = {num(ans)} บาท",
    )


@template("อัตราส่วนร้อยละ", "hard", "profit")
def t_profit():
    cost = random.choice([400, 500, 600, 800, 1000, 1200, 1600, 2000])
    percent = random.choice([10, 15, 20, 25, 30])
    gain = cost * percent // 100
    ans = cost + gain
    return mcq(
        subject="math",
        topic="อัตราส่วนร้อยละ",
        difficulty="hard",
        skill="profit",
        stem=f"ร้านค้าได้กำไร {percent}% จากราคาทุน {num(cost)} บาท ต้องขายในราคาเท่าใด",
        correct=num(ans),
        wrongs=[num(gain), num(cost - gain), num(ans + gain), num(cost + percent), num(cost)],
        explanation=f"กำไร = {num(cost)} × {percent}% = {num(gain)} บาท ราคาขาย = ทุน + กำไร = {num(cost)} + {num(gain)} = {num(ans)} บาท",
    )


# ---------------------------------------------------------------------------
# Math — สมการ
# ---------------------------------------------------------------------------

@template("สมการ", "easy", "eq-add")
def t_eq_add():
    x = random.randint(5, 40)
    a = random.randint(3, 30)
    b = x + a
    return mcq(
        subject="math",
        topic="สมการ",
        difficulty="easy",
        skill="eq-add",
        stem=f"ถ้า x + {a} = {b} แล้ว x เท่ากับเท่าใด",
        correct=str(x),
        wrongs=[str(b + a), str(b), str(a), str(x + 1), str(abs(a - b))],
        explanation=f"ย้าย {a} ไปลบ: x = {b} − {a} = {x}",
    )


@template("สมการ", "easy", "eq-mul")
def t_eq_mul():
    a = random.randint(2, 12)
    x = random.randint(3, 15)
    b = a * x
    return mcq(
        subject="math",
        topic="สมการ",
        difficulty="easy",
        skill="eq-mul",
        stem=f"ถ้า {a}x = {b} แล้ว x เท่ากับเท่าใด",
        correct=str(x),
        wrongs=[str(b), str(a), str(x + 1), str(b - a), str(a + x)],
        explanation=f"หารทั้งสองข้างด้วย {a}: x = {b} ÷ {a} = {x}",
    )


@template("สมการ", "medium", "eq-two-step")
def t_eq_two():
    a = random.randint(2, 9)
    x = random.randint(2, 12)
    b = random.randint(1, 15)
    kind = random.choice(["plus", "minus"])
    if kind == "plus":
        c = a * x + b
        stem = f"ถ้า {a}x + {b} = {c} แล้ว x เท่ากับเท่าใด"
        explain = f"ย้าย {b} ก่อน: {a}x = {c} − {b} = {a * x} แล้วหารด้วย {a} ได้ x = {x}"
        wrongs = [str(c - b), str(x + 1), str(b), str((c + b) // a if (c + b) % a == 0 else x + 2)]
    else:
        if a * x <= b:
            return None
        c = a * x - b
        stem = f"ถ้า {a}x − {b} = {c} แล้ว x เท่ากับเท่าใด"
        explain = f"ย้าย {b}: {a}x = {c} + {b} = {a * x} แล้วหารด้วย {a} ได้ x = {x}"
        wrongs = [str(c + b), str(x + 1), str(max(1, x - 1)), str(b)]
    return mcq(
        subject="math",
        topic="สมการ",
        difficulty="medium",
        skill="eq-two-step",
        stem=stem,
        correct=str(x),
        wrongs=wrongs + [str(a), str(c)],
        explanation=explain,
    )


@template("สมการ", "hard", "eq-word")
def t_eq_word():
    name = random.choice(NAMES_TH)
    price = random.choice([8, 12, 15, 18, 20, 25])
    count = random.randint(3, 8)
    left = random.choice([10, 15, 20, 25, 30, 40])
    ans = price * count + left
    return mcq(
        subject="math",
        topic="สมการ",
        difficulty="hard",
        skill="eq-word",
        stem=(
            f"{name}มีเงินอยู่จำนวนหนึ่ง ซื้อของชิ้นละ {price} บาท จำนวน {count} ชิ้น แล้วเหลือเงิน {left} บาท "
            f"เดิมมีเงินกี่บาท"
        ),
        correct=str(ans),
        wrongs=[str(price * count), str(left), str(price * count - left), str(ans + price), str(count * left)],
        explanation=f"เงินเดิม = เงินที่ใช้ + เงินที่เหลือ = ({price} × {count}) + {left} = {price * count} + {left} = {ans} บาท",
    )


@template("สมการ", "hard", "eq-age")
def t_eq_age():
    child = random.randint(8, 12)
    gap = random.randint(18, 32)
    parent = child + gap
    years = random.randint(2, 6)
    ans = parent + years
    return mcq(
        subject="math",
        topic="สมการ",
        difficulty="hard",
        skill="eq-age",
        stem=f"ตอนนี้ลูกอายุ {child} ปี พ่ออายุมากกว่าลูก {gap} ปี อีก {years} ปีพ่อจะอายุกี่ปี",
        correct=str(ans),
        wrongs=[str(parent), str(child + years), str(gap + years), str(parent - years), str(ans + gap)],
        explanation=f"ตอนนี้พ่ออายุ {child} + {gap} = {parent} ปี อีก {years} ปีจะอายุ {parent} + {years} = {ans} ปี",
    )


# ---------------------------------------------------------------------------
# Math — เรขาคณิต
# ---------------------------------------------------------------------------

@template("เรขาคณิตพื้นที่ปริมาตร", "easy", "rect-area")
def t_rect_area():
    w = random.randint(4, 24)
    h = random.randint(3, 18)
    if w == h:
        h += 1
    ans = w * h
    return mcq(
        subject="math",
        topic="เรขาคณิตพื้นที่ปริมาตร",
        difficulty="easy",
        skill="rect-area",
        stem=f"รูปสี่เหลี่ยมผืนผ้ากว้าง {w} เซนติเมตร ยาว {h} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร",
        correct=str(ans),
        wrongs=[str(2 * (w + h)), str((w + h) * 2 // 2), str(w + h), str(ans + w), str(w * (h + 1))],
        explanation=f"พื้นที่สี่เหลี่ยมผืนผ้า = กว้าง × ยาว = {w} × {h} = {ans} ตารางเซนติเมตร",
    )


@template("เรขาคณิตพื้นที่ปริมาตร", "easy", "rect-perim")
def t_rect_perim():
    w = random.randint(4, 30)
    h = random.randint(3, 20)
    ans = 2 * (w + h)
    return mcq(
        subject="math",
        topic="เรขาคณิตพื้นที่ปริมาตร",
        difficulty="easy",
        skill="rect-perim",
        stem=f"รูปสี่เหลี่ยมผืนผ้ากว้าง {w} เซนติเมตร ยาว {h} เซนติเมตร มีความยาวรอบรูปกี่เซนติเมตร",
        correct=str(ans),
        wrongs=[str(w * h), str(w + h), str(2 * w + h), str(ans + 2), str(4 * (w + h))],
        explanation=f"ความยาวรอบรูป = 2 × (กว้าง + ยาว) = 2 × ({w} + {h}) = {ans} เซนติเมตร",
    )


@template("เรขาคณิตพื้นที่ปริมาตร", "medium", "tri-area")
def t_tri_area():
    base = random.randrange(6, 30, 2)
    height = random.randint(4, 18)
    ans = base * height // 2
    return mcq(
        subject="math",
        topic="เรขาคณิตพื้นที่ปริมาตร",
        difficulty="medium",
        skill="tri-area",
        stem=f"รูปสามเหลี่ยมมีฐาน {base} เซนติเมตร และสูง {height} เซนติเมตร พื้นที่เป็นเท่าใด",
        correct=str(ans),
        wrongs=[str(base * height), str(base + height), str(ans + base), str(base * height // 4), str((base + height) // 2)],
        explanation=f"พื้นที่สามเหลี่ยม = 1/2 × ฐาน × สูง = 1/2 × {base} × {height} = {ans} ตารางเซนติเมตร",
    )


@template("เรขาคณิตพื้นที่ปริมาตร", "medium", "tri-angle")
def t_tri_angle():
    a = random.randint(25, 80)
    b = random.randint(25, 80)
    c = 180 - a - b
    if c < 20 or c > 120:
        return None
    return mcq(
        subject="math",
        topic="เรขาคณิตพื้นที่ปริมาตร",
        difficulty="medium",
        skill="tri-angle",
        stem=f"รูปสามเหลี่ยมมุมหนึ่งขนาด {a} องศา อีกมุมหนึ่งขนาด {b} องศา มุมที่เหลือขนาดเท่าใด",
        correct=f"{c}°",
        wrongs=[f"{a + b}°", f"{180 - a}°", f"{90 - (a % 90)}°", f"{c + 10}°", f"{abs(a - b)}°"],
        explanation=f"ผลบวกมุมภายในสามเหลี่ยมเท่ากับ 180° ดังนั้นมุมที่เหลือ = 180 − {a} − {b} = {c}°",
    )


@template("เรขาคณิตพื้นที่ปริมาตร", "medium", "box-volume")
def t_volume():
    l = random.randint(3, 12)
    w = random.randint(3, 10)
    h = random.randint(2, 8)
    ans = l * w * h
    return mcq(
        subject="math",
        topic="เรขาคณิตพื้นที่ปริมาตร",
        difficulty="medium",
        skill="box-volume",
        stem=f"กล่องสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {l} ซม. สูง {h} ซม. มีปริมาตรกี่ลูกบาศก์เซนติเมตร",
        correct=str(ans),
        wrongs=[str(2 * (l * w + l * h + w * h)), str(l * w), str(l + w + h), str(l * w * (h + 1)), str(ans + l)],
        explanation=f"ปริมาตร = กว้าง × ยาว × สูง = {w} × {l} × {h} = {ans} ลูกบาศก์เซนติเมตร",
    )


@template("เรขาคณิตพื้นที่ปริมาตร", "hard", "circle-22-7")
def t_circle():
    radius = random.choice([7, 14, 21])
    thing = random.choice(["สนาม", "สระน้ำ", "แปลงดอกไม้", "ลานกีฬา", "หน้าปัดนาฬิกา", "ลานวงกลม"])
    kind = random.choice(["area", "circum"])
    if kind == "area":
        ans = 22 * radius * radius // 7
        stem = f"{thing}รูปวงกลมมีรัศมี {radius} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร กำหนด π = 22/7"
        explain = f"พื้นที่ = πr² = 22/7 × {radius} × {radius} = {ans}"
        wrongs = [str(2 * 22 * radius // 7), str(22 * radius // 7), str(ans // 2), str(radius * radius)]
    else:
        ans = 2 * 22 * radius // 7
        stem = f"{thing}รูปวงกลมมีรัศมี {radius} เซนติเมตร มีเส้นรอบวงยาวกี่เซนติเมตร กำหนด π = 22/7"
        explain = f"เส้นรอบวง = 2πr = 2 × 22/7 × {radius} = {ans}"
        wrongs = [str(22 * radius * radius // 7), str(22 * radius // 7), str(ans // 2), str(2 * radius)]
    return mcq(
        subject="math",
        topic="เรขาคณิตพื้นที่ปริมาตร",
        difficulty="hard",
        skill="circle-22-7",
        stem=stem,
        correct=str(ans),
        wrongs=wrongs,
        explanation=explain,
    )


@template("เรขาคณิตพื้นที่ปริมาตร", "hard", "composite-area")
def t_composite():
    w = random.randint(8, 16)
    h = random.randint(6, 12)
    side = random.randint(2, min(4, w - 2, h - 2))
    big = w * h
    hole = side * side
    ans = big - hole
    return mcq(
        subject="math",
        topic="เรขาคณิตพื้นที่ปริมาตร",
        difficulty="hard",
        skill="composite-area",
        stem=(
            f"แผ่นสี่เหลี่ยมกว้าง {w} ซม. ยาว {h} ซม. ถูกตัดสี่เหลี่ยมจัตุรัสด้านละ {side} ซม. ออกหนึ่งรูป "
            f"พื้นที่ส่วนที่เหลือเป็นเท่าใด"
        ),
        correct=str(ans),
        wrongs=[str(big), str(big + hole), str(big - side), str(hole), str(2 * (w + h) - hole)],
        explanation=f"พื้นที่แผ่นเดิม {w} × {h} = {big} ลบช่องที่ตัด {side} × {side} = {hole} เหลือ {ans} ตารางเซนติเมตร",
    )


# ---------------------------------------------------------------------------
# Math — สถิติและโจทย์ปัญหา
# ---------------------------------------------------------------------------

@template("สถิติโจทย์ปัญหา", "easy", "mean")
def t_mean():
    target = random.randint(8, 20)
    nums = [random.randint(3, 25) for _ in range(4)]
    fifth = target * 5 - sum(nums)
    if not 1 <= fifth <= 40:
        return None
    nums.append(fifth)
    if sum(nums) != target * 5:
        return None
    shown = ", ".join(str(n) for n in nums)
    return mcq(
        subject="math",
        topic="สถิติโจทย์ปัญหา",
        difficulty="easy",
        skill="mean",
        stem=f"ค่าเฉลี่ยของ {shown} เท่ากับเท่าใด",
        correct=str(target),
        wrongs=[str(target + 1), str(max(1, target - 1)), str(sum(nums)), str(max(nums)), str(target + 2)],
        explanation=f"ผลรวม = {sum(nums)} มี 5 จำนวน ค่าเฉลี่ย = {sum(nums)} ÷ 5 = {target}",
    )


@template("สถิติโจทย์ปัญหา", "medium", "median")
def t_median():
    nums = random.sample(range(2, 30), 5)
    ordered = sorted(nums)
    ans = ordered[2]
    shown = ", ".join(str(n) for n in nums)
    return mcq(
        subject="math",
        topic="สถิติโจทย์ปัญหา",
        difficulty="medium",
        skill="median",
        stem=f"มัธยฐานของข้อมูล {shown} เท่ากับเท่าใด",
        correct=str(ans),
        wrongs=[str(ordered[0]), str(ordered[1]), str(ordered[3]), str(ordered[4]), str(round(sum(nums) / 5))],
        explanation=f"เรียงจากน้อยไปมากได้ {', '.join(map(str, ordered))} ตัวกลางคือ {ans}",
    )


@template("สถิติโจทย์ปัญหา", "easy", "mode")
def t_mode():
    mode = random.randint(2, 12)
    others = random.sample([n for n in range(1, 16) if n != mode], 3)
    data = [mode, mode, mode, *others]
    random.shuffle(data)
    if data.count(mode) < 3 or any(data.count(n) >= 3 for n in others):
        return None
    shown = ", ".join(str(n) for n in data)
    return mcq(
        subject="math",
        topic="สถิติโจทย์ปัญหา",
        difficulty="easy",
        skill="mode",
        stem=f"ฐานนิยมของข้อมูล {shown} เท่ากับเท่าใด",
        correct=str(mode),
        wrongs=[str(n) for n in others] + [str(mode + 1)],
        explanation=f"{mode} ปรากฏ {data.count(mode)} ครั้ง ซึ่งบ่อยที่สุด จึงเป็นฐานนิยม",
    )


@template("สถิติโจทย์ปัญหา", "hard", "missing-mean")
def t_missing_mean():
    target = random.randint(10, 18)
    known = [random.randint(6, 20) for _ in range(4)]
    ans = target * 5 - sum(known)
    if not 1 <= ans <= 30 or ans in known:
        return None
    shown = ", ".join(str(n) for n in known)
    return mcq(
        subject="math",
        topic="สถิติโจทย์ปัญหา",
        difficulty="hard",
        skill="missing-mean",
        stem=f"ข้อมูล {shown} และอีกหนึ่งจำนวน มีค่าเฉลี่ยเท่ากับ {target} จำนวนที่หายไปคือเท่าใด",
        correct=str(ans),
        wrongs=[str(target), str(sum(known) // 4), str(ans + 5), str(max(1, ans - 5)), str(target * 2)],
        explanation=f"ผลรวมทั้ง 5 จำนวนต้องเป็น {target} × 5 = {target * 5} จำนวนที่หายไป = {target * 5} − {sum(known)} = {ans}",
    )


@template("สถิติโจทย์ปัญหา", "medium", "speed")
def t_speed():
    speed = random.choice([40, 45, 48, 50, 60, 72, 80])
    hours = random.choice([2, 3, 4, 5])
    distance = speed * hours
    ask = random.choice(["speed", "distance", "time"])
    if ask == "speed":
        stem = f"รถยนต์วิ่งได้ระยะทาง {distance} กิโลเมตร ในเวลา {hours} ชั่วโมง ความเร็วเฉลี่ยเป็นกี่กิโลเมตรต่อชั่วโมง"
        correct = str(speed)
        explain = f"ความเร็ว = ระยะทาง ÷ เวลา = {distance} ÷ {hours} = {speed} กิโลเมตรต่อชั่วโมง"
        wrongs = [str(distance), str(hours), str(speed + 10), str(distance * hours)]
    elif ask == "distance":
        stem = f"รถยนต์วิ่งด้วยความเร็วเฉลี่ย {speed} กิโลเมตรต่อชั่วโมง เป็นเวลา {hours} ชั่วโมง จะได้ระยะทางกี่กิโลเมตร"
        correct = str(distance)
        explain = f"ระยะทาง = ความเร็ว × เวลา = {speed} × {hours} = {distance} กิโลเมตร"
        wrongs = [str(speed), str(speed + hours), str(distance + speed), str(speed * (hours + 1))]
    else:
        stem = f"ถ้าระยะทาง {distance} กิโลเมตร และความเร็วเฉลี่ย {speed} กิโลเมตรต่อชั่วโมง ต้องใช้เวลากี่ชั่วโมง"
        correct = str(hours)
        explain = f"เวลา = ระยะทาง ÷ ความเร็ว = {distance} ÷ {speed} = {hours} ชั่วโมง"
        wrongs = [str(speed), str(distance), str(hours + 1), str(max(1, hours - 1))]
    return mcq(
        subject="math",
        topic="สถิติโจทย์ปัญหา",
        difficulty="medium",
        skill="speed",
        stem=stem,
        correct=correct,
        wrongs=wrongs,
        explanation=explain,
    )


@template("สถิติโจทย์ปัญหา", "medium", "table-max")
def t_table():
    names = random.sample(NAMES_TH, 4)
    scores = random.sample(range(8, 30), 4)
    best_i = max(range(4), key=lambda i: scores[i])
    rows = " ".join(f"{names[i]} {scores[i]} คะแนน" for i in range(4))
    return mcq(
        subject="math",
        topic="สถิติโจทย์ปัญหา",
        difficulty="medium",
        skill="table-max",
        stem=f"จากคะแนนสอบ {rows} ใครได้คะแนนสูงสุด",
        correct=names[best_i],
        wrongs=[names[i] for i in range(4) if i != best_i],
        explanation=(
            "เทียบจำนวนโดยตรง: "
            + ", ".join(f"{names[i]}={scores[i]}" for i in range(4))
            + f" ค่าสูงสุดคือ {names[best_i]} ได้ {scores[best_i]} คะแนน"
        ),
    )


# ---------------------------------------------------------------------------
# English — grammar
# ---------------------------------------------------------------------------

_VERBS_3RD = [
    ("go to school", "goes to school", "going to school", "went to school"),
    ("play football", "plays football", "playing football", "played football"),
    ("read a book", "reads a book", "reading a book", "read a book yesterday"),
    ("watch the news", "watches the news", "watching the news", "watched the news"),
    ("study English", "studies English", "studying English", "studied English"),
]


@template("Grammar/Tenses", "easy", "present-simple-3rd")
def t_present_simple():
    person = _pick_person()
    base, third, ing, past = random.choice(_VERBS_3RD)
    days = random.choice(["every Monday", "on weekdays", "every morning", "after dinner"])
    name, _pronoun, _poss = person
    explain = (
        f"ประธานเอกพจน์บุรุษที่สาม ({name}) ใน present simple ใช้กริยาเติม -s "
        f"และ {days} บอกนิสัย จึงตอบ {third}"
    )
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="easy",
        skill="present-simple-3rd",
        stem=f'{name} ___ {days}. Use the present simple of "{base}".',
        correct=third,
        wrongs=[base, ing, past],
        explanation=explain,
    )


@template("Grammar/Tenses", "medium", "present-continuous")
def t_present_cont():
    name, pronoun, _poss = _pick_person()
    pairs = [
        ("is reading a story", "reads a story", "read a story", "has read"),
        ("is cooking dinner", "cooks dinner", "cook dinner", "cooked dinner"),
        ("is drawing a map", "draws a map", "draw a map", "drew a map"),
        ("are playing football", "play football", "plays football", "played football"),
    ]
    marker = random.choice(["Listen!", "Look!", "Be quiet!"])
    correct, *fixed_wrongs = random.choice(pairs[:3])
    lemma = correct.split()[1]
    place = random.choice(["in the living room", "at the library", "in the kitchen", "under the tree"])
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="medium",
        skill="present-continuous",
        stem=f'{marker} {name} ___ {place}. Use "{lemma}".',
        correct=correct,
        wrongs=list(fixed_wrongs),
        explanation=(
            f"{marker} บอกว่ากำลังเกิดอยู่ตอนนี้ ใช้ present continuous: {name} {correct} {place}."
        ),
    )


@template("Grammar/Tenses", "medium", "past-simple")
def t_past():
    name, _pronoun, _poss = _pick_person()
    rows = [
        ("go", "went to the museum", "goes to the museum", "go to the museum", "going to the museum"),
        ("buy", "bought a new bag", "buys a new bag", "buy a new bag", "buying a new bag"),
        ("see", "saw a rainbow", "sees a rainbow", "see a rainbow", "seeing a rainbow"),
        ("eat", "ate rice for lunch", "eats rice for lunch", "eat rice for lunch", "eating rice for lunch"),
        ("write", "wrote a letter", "writes a letter", "write a letter", "writing a letter"),
    ]
    lemma, correct, w1, w2, w3 = random.choice(rows)
    when = random.choice(["yesterday", "last Sunday", "last night", "two days ago"])
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="medium",
        skill="past-simple",
        stem=f'{name} ___ {when}. Use the past simple of "{lemma}".',
        correct=correct,
        wrongs=[w1, w2, w3],
        explanation=f"{when} เป็นเวลาในอดีตที่จบแล้ว ใช้ past simple ของ {lemma}: {correct}",
    )


@template("Grammar/Tenses", "medium", "future-will")
def t_future():
    name, _pronoun, _poss = _pick_person()
    actions = [
        "help her mother",
        "visit Chiang Mai",
        "join the science club",
        "finish the project",
        "call his friend",
    ]
    action = random.choice(actions)
    when = random.choice(["tomorrow", "next Monday", "this weekend", "next month"])
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="medium",
        skill="future-will",
        stem=f"{name} ___ {action} {when}.",
        correct="will",
        wrongs=["was", "did", "is"],
        explanation=f"{when} เป็นอนาคต ใช้ will + กริยาช่องที่ 1: {name} will {action} {when}.",
    )


@template("Grammar/Tenses", "easy", "there-is-are")
def t_there():
    place = random.choice(["on the desk", "in the garden", "in my bag", "near the door"])
    singular = random.choice([True, False])
    if singular:
        noun = random.choice(["an orange", "a ruler", "a cat", "an umbrella"])
        correct, wrongs = "is", ["are", "were", "be"]
        stem = f"There ___ {noun} {place}."
        explain = f"{noun} เป็นเอกพจน์ ใช้ There is"
    else:
        noun = random.choice(["two cats", "three books", "some flowers", "many chairs"])
        correct, wrongs = "are", ["is", "was", "be"]
        stem = f"There ___ {noun} {place}."
        explain = f"{noun} เป็นพหูพจน์ ใช้ There are"
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="easy",
        skill="there-is-are",
        stem=stem,
        correct=correct,
        wrongs=wrongs,
        explanation=explain + f": There {correct} {noun} {place}.",
    )


@template("Grammar/Tenses", "medium", "article")
def t_article():
    name, _p, _pos = _pick_person()
    rows = [
        ("an", "elephant at the zoo", "a", "the", "—", "elephant ขึ้นต้นด้วยเสียงสระ"),
        ("an", "hour to finish the quiz", "a", "the", "—", "hour ออกเสียงขึ้นต้นด้วยสระ แม้สะกดด้วย h"),
        ("a", "university tour", "an", "the", "—", "university ออกเสียงขึ้นต้นด้วย /j/ ซึ่งเป็นเสียงพยัญชนะ"),
        ("an", "apple from the market", "a", "the", "—", "apple ขึ้นต้นด้วยเสียงสระ"),
        ("a", "uniform for the concert", "an", "the", "—", "uniform ออกเสียงขึ้นต้นด้วย /j/ จึงใช้ a"),
    ]
    correct, tail, w1, w2, w3, why = random.choice(rows)
    verb = "waited" if tail.startswith("hour") else "saw"
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="medium",
        skill="article",
        stem=f"{name} {verb} ___ {tail}.",
        correct=correct,
        wrongs=[w1, w2, w3],
        explanation=f"เลือก a/an จากเสียงต้นคำ ไม่ใช่ตัวสะกด: {why} จึงใช้ {correct}",
    )


@template("Grammar/Tenses", "medium", "preposition-time")
def t_prep_time():
    name, _p, _pos = _pick_person()
    rows = [
        ("on", "Monday morning", "in", "at", "by"),
        ("at", "7 o'clock", "on", "in", "to"),
        ("in", "2014", "on", "at", "by"),
        ("in", "July", "on", "at", "to"),
        ("on", "New Year's Day", "in", "at", "by"),
    ]
    correct, when, w1, w2, w3 = random.choice(rows)
    verb = random.choice(["was born", "has a test", "arrives", "met Mina"])
    if verb == "was born" and correct == "at":
        verb = "arrives"
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="medium",
        skill="preposition-time",
        stem=f"{name} {verb} ___ {when}.",
        correct=correct,
        wrongs=[w1, w2, w3],
        explanation=f"วันใช้ on, เวลาเป็นนาฬิกาใช้ at, เดือน ปี และฤดูใช้ in ดังนั้นหน้า {when} ใช้ {correct}",
    )


@template("Grammar/Tenses", "hard", "comparative")
def t_comparative():
    pairs = [
        ("tall", "taller", "more tall", "tallest", "talled"),
        ("big", "bigger", "more big", "biggest", "bigest"),
        ("happy", "happier", "more happy", "happyest", "happyer"),
        ("good", "better", "gooder", "more good", "best"),
        ("beautiful", "more beautiful", "beautifuler", "most beautiful", "beautifulest"),
    ]
    adj, correct, w1, w2, w3 = random.choice(pairs)
    a = random.choice(["This box", "My bag", "The red car", "Room 2", "The morning train"])
    b = random.choice(["that one", "yours", "the blue car", "Room 5", "the evening train"])
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="hard",
        skill="comparative",
        stem=f'{a} is ___ than {b}. Use "{adj}".',
        correct=correct,
        wrongs=[w1, w2, w3, adj],
        explanation=f"มี than จึงเป็นขั้นกว่า ไม่ใช่ขั้นสุด สูตรของ {adj} คือ {correct}",
    )


@template("Grammar/Tenses", "medium", "modal-must")
def t_modal():
    place = random.choice(["in the library", "in the hospital", "during the test", "in class"])
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="medium",
        skill="modal-must",
        stem=f"Students ___ talk loudly {place}.",
        correct="must not",
        wrongs=["can to", "must", "are"],
        explanation=f"{place} เป็นที่ที่ห้ามส่งเสียงดัง ใช้ must not เพื่อบอกข้อห้าม",
    )


@template("Grammar/Tenses", "hard", "past-when")
def t_past_when():
    name, pronoun, _poss = _pick_person()
    backgrounds = [
        ("was walking home", "walked home", "walks home", "is walking home"),
        ("was doing homework", "did homework", "does homework", "is doing homework"),
        ("was cooking", "cooked", "cooks", "is cooking"),
    ]
    correct, w1, w2, w3 = random.choice(backgrounds)
    lemma = {"was walking home": "walk", "was doing homework": "do", "was cooking": "cook"}[correct]
    event = random.choice(["the rain started", "the phone rang", "a friend arrived", "the lights went out"])
    return mcq(
        subject="english",
        topic="Grammar/Tenses",
        difficulty="hard",
        skill="past-when",
        stem=f'{name} ___ when {event}. Use "{lemma}".',
        correct=correct,
        wrongs=[w1, w2, w3],
        explanation=(
            "เหตุการณ์สั้นที่ขัดจังหวะใช้ past simple (when ...) "
            f"ส่วนสิ่งที่กำลังทำอยู่ใช้อดีตต่อเนื่อง: {name} {correct} when {event}."
        ),
    )


# ---------------------------------------------------------------------------
# English — vocabulary
# ---------------------------------------------------------------------------

VOCAB = [
    ("ancient", "very old", "modern", "The ___ temple was built 800 years ago.", ["modern", "tiny", "loud"]),
    ("brave", "not afraid", "cowardly", "The ___ firefighter ran into the smoky house.", ["scared", "sleepy", "rude"]),
    ("polite", "showing good manners", "rude", "{name} says please and thank you. {name} is ___.", ["rude", "hungry", "late"]),
    ("huge", "very big", "tiny", "An elephant is ___ next to a mouse.", ["tiny", "quiet", "sour"]),
    ("scarce", "hard to find", "plentiful", "Water is ___ in the dry season.", ["cheap", "wet", "easy"]),
    ("delicious", "very tasty", "awful", "The mango sticky rice was ___.", ["awful", "empty", "noisy"]),
    ("patient", "able to wait calmly", "impatient", "A ___ teacher listens when students need more time.", ["angry", "loud", "late"]),
    ("careful", "paying attention to avoid mistakes", "careless", "Be ___ when you cross the busy road.", ["careless", "hungry", "funny"]),
    ("generous", "happy to give", "selfish", "She shared her lunch. She is ___.", ["selfish", "sleepy", "tiny"]),
    ("exhausted", "very tired", "energetic", "After the long race, Ben felt ___.", ["hungry only", "energetic", "ancient"]),
    ("borrow", "take for a short time and return", "lend", "May I ___ your ruler? I will give it back.", ["keep forever", "sell", "break"]),
    ("lend", "give for a short time", "borrow", "Could you ___ me a pencil until lunch?", ["steal", "hide", "eat"]),
    ("arrive", "reach a place", "leave", "The train will ___ at 7 o'clock.", ["leave", "sleep", "draw"]),
    ("protect", "keep safe", "harm", "Helmets ___ cyclists.", ["hurt", "sell", "wake"]),
    ("predict", "say what will happen", "forget", "The weather report can ___ rain.", ["forget", "paint", "borrow"]),
    ("rare", "not common", "common", "Snow is ___ in Bangkok.", ["usual", "hot", "near"]),
    ("silent", "making no sound", "noisy", "Please stay ___ during the test.", ["noisy", "late", "sweet"]),
    ("honest", "always telling the truth", "dishonest", "An ___ student does not copy answers.", ["lazy", "loud", "rude"]),
    ("repair", "fix something broken", "break", "Dad will ___ the broken chair.", ["break", "sell", "hide"]),
    ("wander", "walk without a clear plan", "rush", "They ___ around the old market.", ["sleep", "shout", "fly"]),
    ("brief", "short in time", "long", "The teacher gave a ___ talk before lunch.", ["long", "angry", "wet"]),
    ("fragile", "easy to break", "strong", "Glass cups are ___. Carry them with two hands.", ["heavy always", "strong", "sweet"]),
    ("eager", "wanting to do something very much", "unwilling", "The pupils are ___ to visit the museum.", ["asleep", "late", "rude"]),
    ("plenty", "more than enough", "lack", "There is ___ of fruit on the table.", ["none", "one only", "a hole"]),
]


def _vocab_cloze():
    word, meaning, opposite, frame, wrongs = random.choice(VOCAB)
    name, _pronoun, _poss = _pick_person()
    place = random.choice(["in Chiang Mai", "at school", "in the story", "on the worksheet"])
    sentence = frame.format(name=name)
    stem = f"{place.capitalize()}, {name} reads this sentence: {sentence}"
    return mcq(
        subject="english",
        topic="Vocabulary",
        difficulty="medium",
        skill=f"cloze-{word}",
        stem=stem,
        correct=word,
        wrongs=wrongs + [opposite],
        explanation=f"{word} หมายถึง {meaning} ซึ่งเข้ากับประโยคนี้ คำตรงข้ามคร่าว ๆ คือ {opposite}",
    )


def _vocab_meaning():
    word, meaning, opposite, _frame, _wrongs = random.choice(VOCAB)
    name, _pronoun, _poss = _pick_person()
    others = [row[1] for row in VOCAB if row[0] != word]
    random.shuffle(others)
    return mcq(
        subject="english",
        topic="Vocabulary",
        difficulty="easy",
        skill=f"meaning-{word}",
        stem=f"{name} looks up the word \"{word}\". Which meaning is correct?",
        correct=meaning,
        wrongs=others[:4],
        explanation=f"{word} แปลว่า {meaning}",
    )


def _vocab_opposite():
    word, meaning, opposite, _frame, _wrongs = random.choice(VOCAB)
    name, _pronoun, _poss = _pick_person()
    others = [row[2] for row in VOCAB if row[2] != opposite]
    random.shuffle(others)
    return mcq(
        subject="english",
        topic="Vocabulary",
        difficulty="medium",
        skill=f"opposite-{word}",
        stem=f"{name} asks: what is the opposite of \"{word}\"?",
        correct=opposite,
        wrongs=others[:4] + [meaning],
        explanation=f"คำตรงข้ามของ {word} ({meaning}) ในชุดนี้คือ {opposite}",
    )


@template("Vocabulary", "medium", "vocab-cloze")
def t_vocab_cloze():
    return _vocab_cloze()


@template("Vocabulary", "easy", "vocab-meaning")
def t_vocab_meaning():
    return _vocab_meaning()


@template("Vocabulary", "medium", "vocab-opposite")
def t_vocab_opposite():
    return _vocab_opposite()


# ---------------------------------------------------------------------------
# English — conversation
# ---------------------------------------------------------------------------

CONVERSATIONS = [
    ("apology-late", "You arrive late to class. What should you say to the teacher?", "I'm sorry I'm late.", ["Good night.", "How old are you?", "Give me your bag."], "เมื่อมาสายให้ขอโทษ I'm sorry I'm late."),
    ("asking-way", "You are lost near the palace. What do you ask?", "Excuse me, how can I get to the museum?", ["What is your salary?", "I hate this city.", "Close the window."], "การถามทางขึ้นต้นอย่างสุภาพด้วย Excuse me แล้วบอกจุดหมาย"),
    ("shopping-price", "You want to know the price of a notebook. What do you say?", "How much is this notebook?", ["How old is the shop?", "I am a notebook.", "Sit down, please."], "ถามราคาใช้ How much is ...?"),
    ("offer-help", "Your friend drops a pile of books. What do you say?", "Let me help you.", ["Go away.", "What is the date?", "I can't hear the books."], "เมื่อเพื่อนลำบาก การเสนอความช่วยเหลือที่เหมาะคือ Let me help you."),
    ("suggestion", "Your team must choose a place for lunch. What is a polite suggestion?", "Shall we eat at the canteen?", ["You must pay for me.", "Don't talk.", "I am the canteen."], "Shall we ...? ใช้ชวนอย่างสุภาพ"),
    ("permission", "You want to open the window in class. What do you ask the teacher?", "May I open the window?", ["Open it yourself.", "I opened yesterday.", "Windows are glass."], "ขออนุญาตใช้ May I ...?"),
    ("doctor", "You have a sore throat at the clinic. What do you tell the doctor?", "I have a sore throat.", ["I need a new bicycle.", "The clinic is blue.", "See you next year only."], "บอกอาการตรง ๆ: I have a sore throat."),
    ("phone", "You call and the person you want is not there. What do you say?", "May I leave a message?", ["Put the phone in the fridge.", "How much is your house?", "I am a message."], "ขอฝากข้อความใช้ May I leave a message?"),
    ("restaurant", "A waiter asks what you would like. What do you answer?", "I'd like fried rice, please.", ["I like your hat yesterday.", "The kitchen is behind you.", "No, I am a waiter."], "สั่งอาหารใช้ I'd like ..., please."),
    ("thanks", "Someone holds the door for you. What do you say?", "Thank you.", ["Excuse my door.", "How much is the door?", "Go to bed."], "เมื่อมีคนช่วยเหลือเล็กน้อย ตอบ Thank you."),
    ("weather-plan", "It is raining and a friend suggests football outside. What do you say?", "Let's stay inside until the rain stops.", ["Let's swim in the classroom.", "Rain is a person.", "I ate the rain."], "แผนที่สมเหตุผลเมื่อฝนตกคือรอข้างในก่อน"),
    ("birthday", "It is your friend's birthday. What do you say?", "Happy birthday!", ["Good night forever.", "How much are you?", "Close your books."], "อวยพรวันเกิดใช้ Happy birthday!"),
    ("classroom-repeat", "You did not hear the teacher's question. What do you say?", "Could you say that again, please?", ["You are wrong always.", "I know your password.", "Stop teaching."], "ขอให้พูดซ้ำอย่างสุภาพใช้ Could you say that again, please?"),
    ("library", "You are in the library and your phone rings. What should you do?", "I should turn off the sound and go outside to talk.", ["I should sing loudly.", "I should hide the books.", "I should eat noodles there."], "ห้องสมุดต้องเงียบ ปิดเสียงแล้วออกไปคุยข้างนอก"),
    ("agree", "Your friend says, \"This math problem is hard.\" How can you agree?", "Yes, it is. Let's try it step by step.", ["No, you are a problem.", "The desk is hard wood only.", "I disagree that numbers exist."], "เห็นด้วยแล้วชวนคิดเป็นขั้นเป็นวิธีที่สุภาพและเป็นประโยชน์"),
    ("introduction", "A new student joins the class. What do you say first?", "Hello, I'm {name}. Nice to meet you.", ["Give me your homework.", "How much is your name?", "Go home now."], "แนะนำตัวสั้น ๆ แล้วทักทาย Nice to meet you."),
]


@template("Conversation", "medium", "conversation-situation")
def t_conversation():
    skill, prompt, correct, wrongs, explain = random.choice(CONVERSATIONS)
    name, _pronoun, _poss = _pick_person()
    place = random.choice(["at school", "in Bangkok", "at the weekend market", "during lunch"])
    correct = correct.format(name=name)
    stem = f"{name} is {place}. {prompt}"
    return mcq(
        subject="english",
        topic="Conversation",
        difficulty="medium",
        skill=skill,
        stem=stem,
        correct=correct,
        wrongs=wrongs,
        explanation=explain,
    )


# ---------------------------------------------------------------------------
# English — reading groups
# ---------------------------------------------------------------------------

CITIES = ["Bangkok", "Chiang Mai", "Phuket", "Khon Kaen", "Ayutthaya", "Nakhon Pathom"]
PLACES = ["the national museum", "a floating market", "the city library", "a hilltop temple", "the science park"]
CLUBS = ["the science club", "the art club", "the music club", "the football club", "the reading club"]
ACTIVITIES = [
    "visits the school library",
    "practices the piano at home",
    "helps at the family shop",
    "plays football in the park",
    "draws animals in a notebook",
]
MONTHS = ["June", "July", "August", "September", "October"]
DAYS = ["Monday", "Friday", "Saturday", "Sunday"]


def make_reading_group():
    name, pronoun, poss = _pick_person()
    kind = random.choice(["routine", "trip"])
    group_key = uuid.uuid4().hex[:12]
    if kind == "routine":
        city = random.choice(CITIES)
        day = random.choice(DAYS)
        activity = random.choice(ACTIVITIES)
        books = random.choice([2, 3, 4, 5])
        subject = random.choice(["science", "math", "history", "art"])
        club = random.choice(CLUBS)
        month = random.choice(MONTHS)
        passage = (
            f"{name} is a Grade 6 student in {city}. "
            f"Every {day}, {pronoun.lower()} {activity}. "
            f"{pronoun} reads {books} books every week and likes {subject} the most. "
            f"Next {month}, {name} will join {club}."
        )
        other_cities = [c for c in CITIES if c != city]
        other_acts = [a for a in ACTIVITIES if a != activity]
        other_clubs = [c for c in CLUBS if c != club]
        book_choices = [f"{n} books" for n in (2, 3, 4, 5) if n != books]
        specs = [
            (
                "reading-place",
                f"In which city is {name} a student?",
                city,
                other_cities,
                f"ย่อหน้าแรกบอกว่า {name} is a Grade 6 student in {city}",
            ),
            (
                "reading-habit",
                f"What does {name} do every {day}?",
                activity,
                other_acts,
                f"ประโยค Every {day} บอกกิจกรรมว่า {activity}",
            ),
            (
                "reading-number",
                f"How many books does {name} read every week?",
                f"{books} books",
                book_choices,
                f"ประโยคระบุตรง ๆ ว่า reads {books} books every week",
            ),
            (
                "reading-plan",
                f"What will {name} join next {month}?",
                club,
                other_clubs,
                f"ประโยคท้ายบอกอนาคตว่า will join {club}",
            ),
        ]
    else:
        city = random.choice(CITIES)
        day = random.choice(DAYS)
        place = random.choice(PLACES)
        count = random.choice([2, 3, 4, 6])
        month = random.choice(MONTHS)
        passage = (
            f"Last {day}, {name} went to {city} with {poss} family. "
            f"They visited {place} and took photos. "
            f"{name} bought {count} souvenirs for classmates. "
            f"{pronoun} wants to go there again next {month}."
        )
        other_cities = [c for c in CITIES if c != city]
        other_places = [p for p in PLACES if p != place]
        count_choices = [f"{n} souvenirs" for n in (2, 3, 4, 6) if n != count]
        specs = [
            (
                "reading-place",
                f"Which city did {name} go to?",
                city,
                other_cities,
                f"ประโยคแรกบอกว่า went to {city}",
            ),
            (
                "reading-detail",
                f"Which place did {name}'s family visit?",
                place,
                other_places,
                f"ประโยคถัดไปบอกว่า visited {place}",
            ),
            (
                "reading-number",
                f"How many souvenirs did {name} buy?",
                f"{count} souvenirs",
                count_choices,
                f"ตัวเลขในเรื่องคือ bought {count} souvenirs",
            ),
        ]
    chosen = random.sample(specs, 3)
    items = []
    for skill, stem, correct, wrongs, explain in chosen:
        item = mcq(
            subject="english",
            topic="Reading",
            difficulty="medium",
            skill=skill,
            stem=stem,
            correct=correct,
            wrongs=wrongs,
            explanation=explain + " ตอบจากข้อความเท่านั้น ไม่เดาจากความรู้ทั่วไป",
            passage=passage,
            group_key=group_key,
        )
        if item is None:
            return None
        items.append(item)
    try:
        for item in items:
            validate_item(item)
    except ValueError:
        return None
    return items


def _take_reading(conn, batch, groups):
    items = []
    for _ in range(groups):
        got = None
        for _try in range(40):
            group = make_reading_group()
            if not group:
                continue
            if all(_fresh(conn, item, batch) for item in group):
                got = group
                break
        if not got:
            raise RuntimeError("could not build a new reading set")
        for item in got:
            batch.add(item["fingerprint"])
            items.append(item)
    return items


def build_math_items(conn, batch=None, used_skills=None):
    batch = batch if batch is not None else set()
    used_skills = used_skills if used_skills is not None else set()
    plan = [
        ("จำนวนและการดำเนินการ", 6),
        ("ทศนิยมเศษส่วน", 5),
        ("อัตราส่วนร้อยละ", 5),
        ("สมการ", 5),
        ("เรขาคณิตพื้นที่ปริมาตร", 5),
        ("สถิติโจทย์ปัญหา", 4),
    ]
    items = []
    for topic, count in plan:
        for difficulty in difficulties(count):
            items.append(generate_one(conn, topic, difficulty, used_skills, batch))
    random.shuffle(items)
    return items


def build_english_items(conn, batch=None, used_skills=None):
    batch = batch if batch is not None else set()
    used_skills = used_skills if used_skills is not None else set()
    plan = [
        ("Grammar/Tenses", 10),
        ("Vocabulary", 8),
        ("Conversation", 6),
    ]
    items = []
    for topic, count in plan:
        for difficulty in difficulties(count):
            items.append(generate_one(conn, topic, difficulty, used_skills, batch))
    random.shuffle(items)
    items.extend(_take_reading(conn, batch, 2))
    return items


def build_practice_items(conn, subject, topic):
    batch = set()
    used = set()
    if topic not in TOPICS.get(subject, []):
        raise ValueError("unknown topic")
    if topic == "Reading":
        return _take_reading(conn, batch, 2)
    count = 8
    items = []
    for difficulty in difficulties(count):
        items.append(generate_one(conn, topic, difficulty, used, batch))
    random.shuffle(items)
    return items
