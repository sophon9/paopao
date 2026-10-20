"""Number theory and arithmetic question templates for topic ``m.num`` (จำนวนและตัวประกอบ).

Covers place value & rounding, order of operations, divisibility & remainders,
primes & prime factorisation, factors & factor counting, GCD/LCM & classic word
problems, integers & number lines (with SVG figures), exponents & powers of 10,
and top-school digit puzzles.
"""

import math
import random

from backend.bank import svg
from backend.bank.core import W, mcq, name_th, num, pick, skill, template


# ===========================================================================
# Skill 1: m.num.place — ค่าประจำหลักและการประมาณค่า
# ===========================================================================

skill(
    "m.num.place",
    "m.num",
    "ค่าประจำหลักและการประมาณค่า",
    lesson={
        "concept": (
            "เลขโดดตัวเดียวกันเมื่ออยู่ในหลักต่างกันจะมีค่าต่างกันตามค่าประจำหลัก "
            "ส่วนการประมาณค่าให้ดูเลขโดดในหลักถัดไปทางขวา ถ้าตั้งแต่ 5 ขึ้นไปให้ปัดขึ้น ถ้าน้อยกว่า 5 ให้ปัดทิ้ง"
        ),
        "steps": [
            "ระบุหลักของเลขโดดที่โจทย์ถาม แล้วคูณด้วยค่าประจำหลัก (เช่น หลักหมื่น = × 10,000)",
            "หากเป็นการประมาณค่าเป็นจำนวนเต็มหลักใด ให้ดูเลขโดดทางขวาติดกัน 1 หลัก",
            "หากโจทย์ถามย้อนกลับ (จำนวนน้อยสุด/มากสุดที่ปัดแล้วได้ X) ให้คิดช่วงครึ่งหลัก คือ [X − ครึ่งหลัก, X + ครึ่งหลัก − 1]",
        ],
        "example": {
            "q": "จำนวนเต็มที่น้อยที่สุดเมื่อปัดเป็นจำนวนเต็มพันแล้วได้ 14,000 คือจำนวนใด",
            "steps": [
                "การปัดเป็นจำนวนเต็มพัน ดูที่หลักร้อย (ครึ่งหนึ่งของ 1,000 คือ 500)",
                "จำนวนที่น้อยที่สุดต้องปัดขึ้นจาก 13,500",
                "ดังนั้นคำตอบคือ 13,500",
            ],
            "a": "13,500",
        },
        "mistakes": [
            "สับสนระหว่าง 'ค่าประจำหลัก' กับ 'ค่าของเลขโดด' (เช่น เลข 7 ในหลักพันมีค่า 7,000 ไม่ใช่ 1,000)",
            "เวลาหาจำนวนมากที่สุดที่ปัดได้ X เผลอตอบ X + 500 แทนที่จะเป็น X + 499",
        ],
        "tips": [
            "จำง่าย ๆ: ปัดเป็นเต็มสิบ ช่วงคือ [−5, +4] · เต็มร้อย [−50, +49] · เต็มพัน [−500, +499]",
        ],
    },
    weight=1.0,
)


@template("m.num.place", "easy")
def _place_value_diff():
    digits = random.sample([2, 3, 4, 5, 6, 7, 8, 9], 5)
    d_target = random.choice([3, 4, 5, 6, 7, 8, 9])
    # Place d_target in two distinct positions among 6-digit or 7-digit number
    length = random.choice([6, 7])
    pos_hi = random.randint(3, length - 1)  # 10^pos_hi
    pos_lo = random.randint(0, pos_hi - 2)
    other_pool = [d for d in range(1, 10) if d != d_target]
    arr = [0] * length
    for idx in range(length):
        if idx in (pos_hi, pos_lo):
            arr[idx] = d_target
        else:
            arr[idx] = other_pool.pop(random.randrange(len(other_pool)))
    # Build integer (arr[0] is units)
    n_val = sum(arr[i] * (10 ** i) for i in range(length))
    val_hi = d_target * (10 ** pos_hi)
    val_lo = d_target * (10 ** pos_lo)
    diff = val_hi - val_lo
    total = val_hi + val_lo
    place_names = ["หน่วย", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    return mcq(
        stem=(
            f"จากจำนวน **{num(n_val)}** ค่าของเลขโดด **{d_target}** ที่อยู่ในหลัก{place_names[pos_hi]} "
            f"มากกว่าค่าของเลขโดด **{d_target}** ที่อยู่ในหลัก{place_names[pos_lo]} อยู่เท่าใด"
        ),
        correct=num(diff),
        wrongs=[
            W(num(total), "นำค่าของเลขโดดทั้งสองหลักมาบวกกัน โจทย์ถามว่ามากกว่ากันเท่าใดจึงต้องนำมาลบ", "misread"),
            W(num((10 ** pos_hi) - (10 ** pos_lo)), "นำค่าประจำหลักมาลบกันโดยลืมคูณด้วยตัวเลขโดด", "concept"),
            W(num(val_hi - val_lo * 10) if pos_lo + 1 < pos_hi else num(diff - 9 * (10 ** pos_lo)),
              "ระบุหลักของเลขโดดตัวหลังคลาดเคลื่อนไป 1 หลัก", "calc"),
        ],
        hint=f"หาค่าของเลข {d_target} ในแต่ละหลักก่อน แล้วนำมาลบกัน",
        steps=[
            f"เลข {d_target} ในหลัก{place_names[pos_hi]} มีค่า = {num(val_hi)}",
            f"เลข {d_target} ในหลัก{place_names[pos_lo]} มีค่า = {num(val_lo)}",
            f"ผลต่าง = {num(val_hi)} − {num(val_lo)} = {num(diff)}",
        ],
    )


@template("m.num.place", "medium")
def _rounding_reverse_range():
    place_exp, place_name, half = pick([
        (2, "เต็มร้อย", 50),
        (3, "เต็มพัน", 500),
        (4, "เต็มหมื่น", 5000),
    ])
    base_mult = random.randint(12, 98)
    target = base_mult * (10 ** place_exp)
    min_val = target - half
    max_val = target + half - 1
    mode = random.choice(["min", "max", "sum", "diff_count"])
    if mode == "min":
        return mcq(
            stem=f"จำนวนนับที่ **น้อยที่สุด** เมื่อประมาณค่าเป็นจำนวน{place_name}แล้วได้ **{num(target)}** คือจำนวนใด",
            correct=num(min_val),
            wrongs=[
                W(num(max_val), f"นี่คือจำนวนที่มากที่สุดที่ปัดแล้วได้ {num(target)}", "misread"),
                W(num(target - half + 1), f"เลข {num(min_val)} มีหลักถัดไปเป็นเลข 5 ซึ่งปัดขึ้นได้ {num(target)} อยู่แล้ว", "concept"),
                W(num(target - (10 ** (place_exp - 1))), "ลดลงเพียง 1 หลักถัดไป ยังไม่ใช่ค่าที่น้อยที่สุดที่ปัดขึ้นได้", "concept"),
            ],
            hint=f"การปัดขึ้นเป็น {num(target)} ต้องเริ่มตั้งแต่ครึ่งหนึ่งของหลัก{place_name[4:]} คือ {num(half)}",
            steps=[
                f"การประมาณค่าเป็นจำนวน{place_name} จะปัดขึ้นเมื่อเศษตั้งแต่ {num(half)} ขึ้นไป",
                f"จำนวนนับที่น้อยที่สุดจึงเท่ากับ {num(target)} − {num(half)} = {num(min_val)}",
            ],
        )
    if mode == "max":
        return mcq(
            stem=f"จำนวนนับที่ **มากที่สุด** เมื่อประมาณค่าเป็นจำนวน{place_name}แล้วได้ **{num(target)}** คือจำนวนใด",
            correct=num(max_val),
            wrongs=[
                W(num(target + half), f"ถ้าเป็น {num(target + half)} จะต้องปัดขึ้นเป็น {num(target + 2 * half)} ไม่ใช่ {num(target)}", "trap"),
                W(num(min_val), f"นี่คือจำนวนที่น้อยที่สุดที่ปัดแล้วได้ {num(target)}", "misread"),
                W(num(target + half - 10), "ยังไม่มากที่สุด เพราะหลักหน่วยและหลักอื่น ๆ ทางขวาเป็นเลข 9 ได้ทั้งหมด", "partial"),
            ],
            hint=f"ถ้าเกิน {num(target)} ไปถึง {num(target + half)} จะถูกปัดขึ้น ต้องน้อยกว่านั้นอยู่ 1",
            steps=[
                f"จำนวนที่ปัดลงมาเป็น {num(target)} ต้องน้อยกว่า {num(target + half)}",
                f"ดังนั้นจำนวนนับที่มากที่สุดคือ {num(target + half)} − 1 = {num(max_val)}",
            ],
        )
    # mode in ("sum", "diff_count")
    s = min_val + max_val
    return mcq(
        stem=(
            f"ให้ A เป็นจำนวนนับที่มากที่สุด และ B เป็นจำนวนนับที่น้อยที่สุด "
            f"ที่เมื่อประมาณค่าเป็นจำนวน{place_name}แล้วได้ **{num(target)}** เท่ากัน จงหาค่าของ **A + B**"
        ),
        correct=num(s),
        wrongs=[
            W(num(2 * target), f"คิดเป็น 2 × {num(target)} โดยลืมว่า A = {num(max_val)} และ B = {num(min_val)} รวมกันน้อยกว่าอยู่ 1", "trap"),
            W(num(max_val - min_val), "นำ A กับ B มาลบกันแทนที่จะบวกกัน", "misread"),
            W(num(s + 2), f"หาค่า A เป็น {num(target + half)} ซึ่งเกินช่วงที่ปัดลง", "concept"),
        ],
        hint=f"หาค่า A (มากสุด) และ B (น้อยสุด) ก่อน โดยช่วงคือ [{num(min_val)}, {num(max_val)}]",
        steps=[
            f"จำนวนน้อยที่สุด B = {num(target)} − {num(half)} = {num(min_val)}",
            f"จำนวนมากที่สุด A = {num(target)} + {num(half - 1)} = {num(max_val)}",
            f"ดังนั้น A + B = {num(max_val)} + {num(min_val)} = {num(s)}",
        ],
    )


@template("m.num.place", "hard")
def _digit_formation_even_odd():
    # Form 4-digit numbers from 4 given digits (including 0) without repetition
    nonzero = sorted(random.sample(range(1, 10), 3))
    digits = [0] + nonzero
    # Largest 4-digit number and smallest 4-digit odd/even number
    cond = random.choice(["even_diff", "odd_diff"])
    all_nums = []
    for a in digits:
        if a == 0:
            continue
        for b in digits:
            if b == a:
                continue
            for c in digits:
                if c in (a, b):
                    continue
                for d in digits:
                    if d in (a, b, c):
                        continue
                    all_nums.append(a * 1000 + b * 100 + c * 10 + d)
    if cond == "even_diff":
        evens = [x for x in all_nums if x % 2 == 0]
        hi, lo = max(evens), min(evens)
        cond_text = "จำนวนคู่สี่หลัก"
    else:
        odds = [x for x in all_nums if x % 2 == 1]
        if not odds:
            return None
        hi, lo = max(odds), min(odds)
        cond_text = "จำนวนคี่สี่หลัก"
    ans = hi - lo
    # Common mistake: putting 0 in thousands place for smallest
    fake_lo_zero = nonzero[0] * 100 + nonzero[1] * 10 + nonzero[2]
    # Or forgetting the even/odd condition on smallest/largest
    overall_hi, overall_lo = max(all_nums), min(all_nums)
    d_str = ", ".join(str(d) for d in digits)
    wrongs = []
    if overall_hi - overall_lo != ans:
        wrongs.append(W(num(overall_hi - overall_lo), f"ลืมเงื่อนไขว่าต้องเป็น{cond_text} จึงใช้ค่ามากสุดหรือน้อยสุดทั่วไป", "misread"))
    wrongs.append(W(num(hi + lo), "นำจำนวนที่มากที่สุดและน้อยที่สุดมาบวกกันแทนที่จะหาผลต่าง", "misread"))
    wrongs.append(W(num(hi - fake_lo_zero), "วางเลข 0 ไว้หลักพันทำให้ได้จำนวนสามหลัก ไม่ใช่สี่หลัก", "concept"))
    wrongs.append(W(num(ans + 90), "สลับหลักสิบกับหลักร้อยตอนเรียงเลขให้น้อยที่สุด", "calc"))
    return mcq(
        stem=(
            f"นำบัตรตัวเลข **{d_str}** มาสร้างเป็น **{cond_text}** โดยไม่ใช้เลขซ้ำกันในแต่ละจำนวน "
            f"ผลต่างของจำนวนที่มากที่สุดกับจำนวนที่น้อยที่สุดที่สร้างได้มีค่าเท่าใด"
        ),
        correct=num(ans),
        wrongs=wrongs,
        hint=f"หลักพันห้ามเป็น 0 และหลักหน่วยต้องสอดคล้องกับเงื่อนไข{cond_text}",
        steps=[
            f"สร้าง{cond_text}ที่มากที่สุด ได้ {num(hi)}",
            f"สร้าง{cond_text}ที่น้อยที่สุด (หลักพันห้ามเป็น 0) ได้ {num(lo)}",
            f"ผลต่าง = {num(hi)} − {num(lo)} = {num(ans)}",
        ],
    )


# ===========================================================================
# Skill 2: m.num.order — ลำดับการคำนวณและการดำเนินการระคน
# ===========================================================================

skill(
    "m.num.order",
    "m.num",
    "ลำดับการคำนวณและการดำเนินการระคน",
    lesson={
        "concept": (
            "การคำนวณที่มีหลายเครื่องหมายต้องทำตามลำดับ: 1) ทำในวงเล็บก่อน "
            "2) คูณและหารจากซ้ายไปขวา 3) บวกและลบจากซ้ายไปขวา"
        ),
        "steps": [
            "หาค่าในวงเล็บเล็ก (...) ก่อน แล้วตามด้วยวงเล็บใหญ่",
            "ทำเครื่องหมาย × และ ÷ เรียงจากซ้ายไปขวา",
            "ทำเครื่องหมาย + และ − เรียงจากซ้ายไปขวา (สังเกตตัวร่วมเพื่อดึงตัวร่วมช่วยให้คิดเร็วขึ้น)",
        ],
        "example": {
            "q": "จงหาค่าของ 48 − 18 ÷ 3 × 2 + 5",
            "steps": [
                "ทำหารและคูณจากซ้ายไปขวา: 18 ÷ 3 = 6 แล้ว 6 × 2 = 12",
                "แทนค่ากลับ: 48 − 12 + 5",
                "ทำจากซ้ายไปขวา: 36 + 5 = 41",
            ],
            "a": "41",
        },
        "mistakes": [
            "ทำบวกหรือลบก่อนคูณหาร เช่น เอา 48 − 18 ก่อน",
            "ทำคูณก่อนหารเสมอโดยไม่เรียงซ้ายไปขวา เช่น เอา 3 × 2 = 6 แล้วค่อยเอา 18 ÷ 6",
        ],
        "tips": [
            "ถ้าเจอ a × b + a × c ให้ดึงตัวร่วมเป็น a × (b + c) จะคิดในใจได้ทันที",
        ],
    },
    weight=1.3,
)


@template("m.num.order", "easy")
def _order_ops_basic():
    b = random.randint(2, 6)
    c = random.randint(2, 5)
    q = random.randint(3, 9)
    a = b * q  # so a ÷ b = q
    start = random.randint(a + 15, a + 60)
    add_end = random.randint(4, 19)
    # Expression: start - a ÷ b × c + add_end
    ans = start - q * c + add_end
    if ans <= 0:
        return None
    wrong_left_to_right = ((start - a) // b) * c + add_end if (start - a) % b == 0 else (start - a) * c + add_end
    wrong_mult_first = start - (a // (b * c)) + add_end if a % (b * c) == 0 else start - q - c + add_end
    wrong_add_before_sub = start - (q * c + add_end)
    return mcq(
        stem=f"จงหาผลลัพธ์ของ **{start} − {a} ÷ {b} × {c} + {add_end}**",
        correct=num(ans),
        wrongs=[
            W(num(wrong_add_before_sub), f"นำ {q * c} ไปบวกกับ {add_end} ก่อนแล้วค่อยนำไปลบออกจาก {start} ทั้งที่ต้องทำซ้ายไปขวา", "concept"),
            W(num(wrong_mult_first), f"ทำ {b} × {c} ก่อนหาร ทั้งที่ ÷ กับ × มีลำดับเท่ากันต้องทำจากซ้ายไปขวา", "concept"),
            W(num(wrong_left_to_right), f"นำ {start} − {a} ก่อน ทั้งที่ต้องทำหารและคูณก่อนบวกลบ", "concept"),
        ],
        hint="ทำ ÷ และ × เรียงจากซ้ายไปขวาก่อน แล้วจึงทำ − และ + เรียงจากซ้ายไปขวา",
        steps=[
            f"ขั้นที่ 1 คิดส่วนหารและคูณจากซ้ายไปขวา: {a} ÷ {b} = {q} แล้ว {q} × {c} = {q * c}",
            f"ขั้นที่ 2 แทนค่าในประโยค: {start} − {q * c} + {add_end}",
            f"ขั้นที่ 3 คำนวณจากซ้ายไปขวา: {start - q * c} + {add_end} = {num(ans)}",
        ],
    )


@template("m.num.order", "medium")
def _distributive_shortcut():
    common = random.randint(14, 48)
    p = random.randint(62, 145)
    use_sub = random.choice([True, False])
    if use_sub:
        target_round = random.choice([100, 200])
        q = p + target_round
        # common × q − common × p = common × target_round
        ans = common * target_round
        stem = f"จงหาค่าของ **{common} × {q} − {common} × {p}**"
        steps = [
            f"ดึงตัวร่วม {common} ออกมา: {common} × ({q} − {p})",
            f"= {common} × {target_round} = {num(ans)}",
        ]
        wrongs = [
            W(num(common * (q + p)), "ดึงตัวร่วมแล้วนำตัวเลขในวงเล็บมาบวกกันแทนที่จะลบกัน", "sign"),
            W(num(common * common * target_round), f"นำ {common} คูณซ้ำสองครั้งตอนดึงตัวร่วม", "concept"),
            W(num(ans - common * 10), "คำนวณผลลบในวงเล็บคลาดเคลื่อนไป 10", "calc"),
        ]
    else:
        target_round = random.choice([100, 200, 300])
        q = target_round - p
        if q <= 10 or q == p:
            return None
        ans = common * target_round
        stem = f"จงหาค่าของ **{common} × {p} + {common} × {q}**"
        steps = [
            f"ดึงตัวร่วม {common} ออกมา: {common} × ({p} + {q})",
            f"= {common} × {target_round} = {num(ans)}",
        ]
        wrongs = [
            W(num(2 * common * target_round), f"บวกตัวร่วม {common} + {common} เป็น {2 * common} แล้วคูณกับ {target_round}", "concept"),
            W(num(common * (target_round - 10)), "บวกเลขในวงเล็บพลาด ลืมทดหลักสิบ", "calc"),
            W(num(common + target_round), "นำตัวร่วมไปบวกกับผลรวมแทนที่จะคูณ", "concept"),
        ]
    return mcq(
        stem=stem,
        correct=num(ans),
        wrongs=wrongs,
        hint=f"สังเกตตัวคูณร่วม {common} แล้วใช้สมบัติการแจกแจง a × b ± a × c = a × (b ± c)",
        steps=steps,
    )


@template("m.num.order", "hard")
def _custom_operation():
    # Top-school classic: defined binary operation a ★ b
    sym = pick(["★", "⊕", "⊗", "◆"])
    k1 = random.randint(2, 5)
    k2 = random.randint(1, 4)
    # Define a sym b = k1 * a + k2 * b  or  a * b - (a + b)
    style = random.choice(["linear", "prod_diff"])
    a, b, c = random.sample(range(3, 10), 3)
    if style == "linear":
        def op(x, y):
            return k1 * x + k2 * y
        rule_str = f"{k1}a + {k2}b" if k2 > 1 else f"{k1}a + b"
        step1_val = op(a, b)
        ans = op(step1_val, c)
        wrong_swap = op(b, a)
        wrong_swap_ans = op(wrong_swap, c)
        wrong_no_chain = step1_val + c
        return mcq(
            stem=(
                f"กำหนดให้ a {sym} b = **{rule_str}** เมื่อ a และ b เป็นจำนวนนับ "
                f"จงหาค่าของ **({a} {sym} {b}) {sym} {c}**"
            ),
            correct=num(ans),
            wrongs=[
                W(num(wrong_swap_ans), "สลับตำแหน่ง a กับ b ตอนแทนค่าในสูตร", "formula"),
                W(num(step1_val), f"คำนวณเฉพาะในวงเล็บ ({a} {sym} {b}) = {step1_val} แล้วลืมทำ {sym} {c} ต่อ", "partial"),
                W(num(wrong_no_chain), f"ขั้นที่สองนำ {step1_val} ไปบวก {c} เฉย ๆ แทนที่จะใช้สูตร {sym}", "concept"),
            ],
            hint=f"หาค่าในวงเล็บ ({a} {sym} {b}) ก่อน แล้วนำผลลัพธ์ที่ได้เป็นตัวหน้าทำ {sym} กับ {c} อีกครั้ง",
            steps=[
                f"หาค่าในวงเล็บ: {a} {sym} {b} = {k1}({a}) + {k2}({b}) = {k1 * a} + {k2 * b} = {step1_val}",
                f"นำผลลัพธ์มาทำต่อ: {step1_val} {sym} {c} = {k1}({step1_val}) + {k2}({c}) = {k1 * step1_val} + {k2 * c} = {num(ans)}",
            ],
        )
    else:
        def op(x, y):
            return x * y - (x + y)
        step1_val = op(a, b)
        if step1_val <= 1:
            return None
        ans = op(step1_val, c)
        return mcq(
            stem=(
                f"กำหนดให้ a {sym} b = **(a × b) − (a + b)** "
                f"จงหาค่าของ **({a} {sym} {b}) {sym} {c}**"
            ),
            correct=num(ans),
            wrongs=[
                W(num(step1_val * c - step1_val + c), "ลืมใส่วงเล็บตอนลบ (a + b) จึงกลายเป็น − a + b", "sign"),
                W(num(step1_val), f"คิดเฉพาะ ({a} {sym} {b}) = {step1_val} ยังไม่ได้ทำกับ {c}", "partial"),
                W(num((a * b * c) - (a + b + c)), "รวบสูตรเป็น (a×b×c) − (a+b+c) ซึ่งไม่เท่ากับการทำทีละขั้นตามวงเล็บ", "concept"),
            ],
            hint=f"แทนค่า a = {a}, b = {b} เพื่อหาค่าในวงเล็บก่อน แล้วนำผลลัพธ์ที่ได้ไปแทนเป็นตัวหน้า",
            steps=[
                f"ขั้นที่ 1: {a} {sym} {b} = ({a} × {b}) − ({a} + {b}) = {a * b} − {a + b} = {step1_val}",
                f"ขั้นที่ 2: {step1_val} {sym} {c} = ({step1_val} × {c}) − ({step1_val} + {c}) = {step1_val * c} − {step1_val + c} = {num(ans)}",
            ],
        )


# ===========================================================================
# Skill 3: m.num.div — การหารลงตัวและเศษเหลือ
# ===========================================================================

skill(
    "m.num.div",
    "m.num",
    "การหารลงตัวและเศษเหลือ",
    lesson={
        "concept": (
            "ความสัมพันธ์ของการหารคือ ตัวตั้ง = (ตัวหาร × ผลหาร) + เศษ โดยที่ 0 ≤ เศษ < ตัวหารเสมอ "
            "และสามารถตรวจการหารลงตัวด้วยกฎของเลขโดด เช่น หารด้วย 3 หรือ 9 ลงตัวเมื่อผลบวกเลขโดดหารด้วย 3 หรือ 9 ลงตัว"
        ),
        "steps": [
            "ถ้าโจทย์บอกตัวหาร ผลหาร และเศษ ให้ใช้ ตัวตั้ง = (ตัวหาร × ผลหาร) + เศษ (เศษมากที่สุดคือ ตัวหาร − 1)",
            "หารด้วย 4 ลงตัว: ดูเลข 2 หลักสุดท้าย · หารด้วย 8 ลงตัว: ดูเลข 3 หลักสุดท้าย",
            "หารด้วย 3 หรือ 9 ลงตัว: นำเลขโดดทุกหลักมาบวกกัน แล้วดูว่าหารด้วย 3 หรือ 9 ลงตัวหรือไม่",
        ],
        "example": {
            "q": "จำนวนห้าหลัก 42,A36 หารด้วย 9 ลงตัว เลขโดด A มีค่าเท่าใด",
            "steps": [
                "ผลบวกของเลขโดด = 4 + 2 + A + 3 + 6 = 15 + A",
                "จำนวนที่มากกว่าหรือเท่ากับ 15 และหารด้วย 9 ลงตัวคือ 18",
                "ดังนั้น A = 18 − 15 = 3",
            ],
            "a": "3",
        },
        "mistakes": [
            "คิดว่าเศษของการหารด้วย d มีค่าเท่ากับ d ได้ (จริง ๆ เศษต้องน้อยกว่า d เสมอ)",
            "ตรวจการหารด้วย 4 โดยดูแค่หลักหน่วยว่าเป็นเลขคู่ (เช่น 14 เป็นเลขคู่แต่หารด้วย 4 ไม่ลงตัว)",
        ],
        "tips": [
            "หารด้วย 6 ลงตัว = ต้องเป็นเลขคู่ (หารด้วย 2 ลงตัว) และผลบวกเลขโดดหารด้วย 3 ลงตัวพร้อมกัน",
        ],
    },
    weight=1.4,
)


@template("m.num.div", "easy")
def _division_max_remainder():
    divisor = random.randint(12, 35)
    quotient = random.randint(11, 29)
    max_rem = divisor - 1
    dividend = divisor * quotient + max_rem
    return mcq(
        stem=(
            f"จำนวนนับจำนวนหนึ่งเมื่อหารด้วย **{divisor}** ได้ผลหารเป็น **{quotient}** และมีเศษเหลือมากที่สุดเท่าที่เป็นไปได้ "
            f"จำนวนนับนั้นคือจำนวนใด"
        ),
        correct=num(dividend),
        wrongs=[
            W(num(divisor * quotient + divisor), f"ใช้เศษเท่ากับตัวหาร ({divisor}) แต่เศษต้องน้อยกว่าตัวหารเสมอ", "concept"),
            W(num(divisor * quotient + 1), "ใช้เศษน้อยที่สุด (1) แทนที่จะใช้เศษมากที่สุด", "misread"),
            W(num(divisor * quotient), "ลืมบวกเศษเหลือ คิดเฉพาะ ตัวหาร × ผลหาร", "partial"),
        ],
        hint="เศษที่มากที่สุดเมื่อหารด้วย d คือ d − 1 จากนั้นใช้ ตัวตั้ง = (ตัวหาร × ผลหาร) + เศษ",
        steps=[
            f"เมื่อตัวหารคือ {divisor} เศษเหลือที่มากที่สุดที่เป็นไปได้คือ {divisor} − 1 = {max_rem}",
            f"ตัวตั้ง = (ตัวหาร × ผลหาร) + เศษ = ({divisor} × {quotient}) + {max_rem}",
            f"= {num(divisor * quotient)} + {max_rem} = {num(dividend)}",
        ],
    )


@template("m.num.div", "medium")
def _divisibility_by_9_or_6():
    d1, d2, d3, d4 = [random.randint(1, 9) for _ in range(4)]
    mode = random.choice(["div9", "div6_max"])
    if mode == "div9":
        s = d1 + d2 + d3 + d4
        # find A in 0..9 such that (s + A) % 9 == 0; avoid s % 9 == 0 so 0 and 9 aren't both valid
        if s % 9 == 0:
            d4 = (d4 % 8) + 1
            s = d1 + d2 + d3 + d4
        a_val = (9 - (s % 9)) % 9
        wrong_div3 = (a_val + 3) % 10
        return mcq(
            stem=f"ถ้าจำนวนห้าหลัก **{d1}{d2},A{d3}{d4}** หารด้วย **9** ลงตัว แล้วเลขโดด **A** มีค่าเท่าใด",
            correct=str(a_val),
            wrongs=[
                W(str(wrong_div3), "ค่านี้ทำให้ผลบวกเลขโดดหารด้วย 3 ลงตัว แต่หารด้วย 9 ไม่ลงตัว", "concept"),
                W(str((a_val + 1) % 10), f"บวกเลขโดด {d1}+{d2}+{d3}+{d4} ได้คลาดเคลื่อนไป 1", "calc"),
                W(str(9 - a_val if 9 - a_val != a_val else (a_val + 2) % 10), "นำเศษจากการหารด้วย 9 มาตอบโดยไม่ได้ลบออกจาก 9", "partial"),
            ],
            hint="จำนวนที่หารด้วย 9 ลงตัว ผลบวกของเลขโดดทุกหลักต้องหารด้วย 9 ลงตัว",
            steps=[
                f"ผลบวกของเลขโดดที่ทราบค่า = {d1} + {d2} + {d3} + {d4} = {s}",
                f"ต้องการให้ {s} + A หารด้วย 9 ลงตัว ซึ่งจำนวนถัดไปที่หารด้วย 9 ลงตัวคือ {s + a_val}",
                f"ดังนั้น A = {s + a_val} − {s} = {a_val}",
            ],
        )
    else:
        # 5-digit number d1 d2 d3 d4 B divisible by 6, find largest digit B
        s = d1 + d2 + d3 + d4
        valid_b = [b for b in (0, 2, 4, 6, 8) if (s + b) % 3 == 0]
        ans = max(valid_b)
        min_b = min(valid_b)
        odd_div3 = max([b for b in (1, 3, 5, 7, 9) if (s + b) % 3 == 0])
        even_not3 = max([b for b in (0, 2, 4, 6, 8) if (s + b) % 3 != 0])
        if len({ans, min_b, odd_div3, even_not3}) < 4:
            return None
        return mcq(
            stem=(
                f"จำนวนห้าหลัก **{d1}{d2},{d3}{d4}B** หารด้วย **6** ลงตัว "
                f"เลขโดด **B ที่มากที่สุด** ที่เป็นไปได้คือข้อใด"
            ),
            correct=str(ans),
            wrongs=[
                W(str(odd_div3), f"ถ้า B = {odd_div3} จะหารด้วย 3 ลงตัว แต่เป็นจำนวนคี่จึงหารด้วย 6 ไม่ลงตัว", "concept"),
                W(str(even_not3), f"ถ้า B = {even_not3} เป็นจำนวนคู่แต่ผลบวกเลขโดดเท่ากับ {s + even_not3} ซึ่งหารด้วย 3 ไม่ลงตัว", "concept"),
                W(str(min_b), f"B = {min_b} หารด้วย 6 ลงตัวจริง แต่ยังไม่ใช่ค่าที่มากที่สุด", "misread"),
            ],
            hint="หารด้วย 6 ลงตัว ต้องเป็นจำนวนคู่ (B เป็น 0, 2, 4, 6, 8) และผลบวกเลขโดดหารด้วย 3 ลงตัว",
            steps=[
                "จำนวนที่หารด้วย 6 ลงตัว ต้องหารด้วย 2 และ 3 ลงตัว ดังนั้น B ต้องเป็นเลขคู่ (0, 2, 4, 6, 8)",
                f"ผลบวกเลขโดด 4 หลักแรก = {d1} + {d2} + {d3} + {d4} = {s}",
                f"ค่า B ที่เป็นเลขคู่และทำให้ {s} + B หารด้วย 3 ลงตัว ได้แก่ {', '.join(str(x) for x in valid_b)} ค่าที่มากที่สุดคือ {ans}",
            ],
        )


@template("m.num.div", "hard")
def _divisibility_by_36_or_45():
    # 5-digit number d1 d2 A d3 B divisible by 36 (4 and 9) or 45 (5 and 9)
    d1, d2, d3 = [random.randint(1, 8) for _ in range(3)]
    mode = random.choice(["45", "36_max"])
    if mode == "45":
        # Ask for largest A + B when d1 d2 A d3 B is divisible by 45
        # Since divisible by 45 -> divisible by 5 and 9 -> B in {0, 5}
        s = d1 + d2 + d3
        a_when_0 = 9 if s % 9 == 0 else 9 - (s % 9)
        a_when_5 = 9 if (s + 5) % 9 == 0 else 9 - ((s + 5) % 9)
        sum0 = a_when_0 + 0
        sum5 = a_when_5 + 5
        ans = max(sum0, sum5)
        other_sum = min(sum0, sum5) if sum0 != sum5 else max(1, ans - 5)
        trap_95 = 14 if ans != 14 else 13
        calc_off = ans + 1 if ans + 1 not in (other_sum, trap_95) else ans - 1
        return mcq(
            stem=(
                f"จำนวนห้าหลัก **{d1}{d2},A{d3}B** หารด้วย **45** ลงตัว "
                f"ค่าของ **A + B ที่มากที่สุด** ที่เป็นไปได้คือเท่าใด"
            ),
            correct=str(ans),
            wrongs=[
                W(str(other_sum), "คิดเฉพาะกรณีเดียวของหลักหน่วย B (ลืมเทียบระหว่าง B = 0 กับ B = 5)", "partial"),
                W(str(calc_off), "คำนวณผลบวกเลขโดดเพื่อให้หารด้วย 9 ลงตัวคลาดเคลื่อนไป 1", "calc"),
                W(str(trap_95), "สมมติให้ A = 9 และ B = 5 ทันทีโดยไม่ได้ตรวจว่าผลบวกเลขโดดหารด้วย 9 ลงตัวหรือไม่", "trap"),
            ],
            hint="หารด้วย 45 ลงตัว แปลว่าต้องหารด้วย 5 และ 9 ลงตัว ดังนั้น B เป็นได้แค่ 0 หรือ 5",
            steps=[
                "เนื่องจากหารด้วย 45 ลงตัว ต้องหารด้วย 5 และ 9 ลงตัว ทำให้ B เป็นได้คือ 0 หรือ 5",
                f"กรณี B = 0: ผลบวกเลขโดดคือ {s} + A + 0 ต้องหารด้วย 9 ลงตัว จะได้ A สูงสุด = {a_when_0} (A + B = {sum0})",
                f"กรณี B = 5: ผลบวกเลขโดดคือ {s} + A + 5 = {s + 5} + A ต้องหารด้วย 9 ลงตัว จะได้ A สูงสุด = {a_when_5} (A + B = {sum5})",
                f"ดังนั้นค่า A + B ที่มากที่สุดคือ {ans}",
            ],
        )
    else:
        # Divisible by 36 -> divisible by 4 and 9, with B fixed by two-digit d3 B divisible by 4
        d3 = random.choice([1, 3, 5, 7, 9])
        s = d1 + d2 + d3
        a_for_6 = 9 if (s + 6) % 9 == 0 else 9 - ((s + 6) % 9)
        a_for_2 = 9 if (s + 2) % 9 == 0 else 9 - ((s + 2) % 9)
        sum6 = a_for_6 + 6
        sum2 = a_for_2 + 2
        ans = max(sum6, sum2)
        other = min(sum6, sum2) if sum6 != sum2 else max(2, ans - 4)
        a_for_8 = 9 if (s + 8) % 9 == 0 else 9 - ((s + 8) % 9)
        wrong_b8 = a_for_8 + 8
        if wrong_b8 in (ans, other):
            wrong_b8 = ans + 2
        calc_off = ans - 1 if ans - 1 not in (other, wrong_b8) else ans + 1
        return mcq(
            stem=(
                f"ถ้าจำนวนห้าหลัก **{d1}{d2},A{d3}B** หารด้วย **36** ลงตัว "
                f"แล้วค่าของ **A + B ที่มากที่สุด** เท่ากับเท่าใด"
            ),
            correct=str(ans),
            wrongs=[
                W(str(other), "ตรวจสอบค่า B ที่หารด้วย 4 ลงตัวไม่ครบทุกกรณี", "partial"),
                W(str(wrong_b8), f"ให้ B = 8 เพราะเป็นเลขคู่ที่มากที่สุด แต่ {d3}8 หารด้วย 4 ไม่ลงตัว", "concept"),
                W(str(calc_off), "บวกเลขโดดผิดพลาดตอนตรวจการหารด้วย 9", "calc"),
            ],
            hint=f"36 = 4 × 9 ดังนั้นเลขสองหลักท้าย ({d3}B) ต้องหารด้วย 4 ลงตัว และผลบวกเลขโดดทั้งห้าหลักต้องหารด้วย 9 ลงตัว",
            steps=[
                f"หารด้วย 4 ลงตัว ดู 2 หลักท้ายคือ {d3}B จะได้ B เป็นได้คือ 2 หรือ 6 (เพราะ {d3}2 และ {d3}6 หารด้วย 4 ลงตัว)",
                f"ถ้า B = 6: {s} + A + 6 = {s + 6} + A หารด้วย 9 ลงตัว ได้ A = {a_for_6} รวม A + B = {sum6}",
                f"ถ้า B = 2: {s} + A + 2 = {s + 2} + A หารด้วย 9 ลงตัว ได้ A = {a_for_2} รวม A + B = {sum2}",
                f"ดังนั้นค่า A + B ที่มากที่สุดคือ {ans}",
            ],
        )


# ===========================================================================
# Skill 4: m.num.prime — จำนวนเฉพาะและการแยกตัวประกอบ
# ===========================================================================

skill(
    "m.num.prime",
    "m.num",
    "จำนวนเฉพาะและการแยกตัวประกอบ",
    lesson={
        "concept": (
            "จำนวนเฉพาะ (Prime Number) คือจำนวนนับที่มากกว่า 1 และมีตัวประกอบเพียง 2 ตัว คือ 1 กับตัวมันเอง "
            "โดย 2 เป็นจำนวนเฉพาะเพียงตัวเดียวที่เป็นจำนวนคู่ (1 ไม่ใช่จำนวนเฉพาะ)"
        ),
        "steps": [
            "จำจำนวนเฉพาะไม่เกิน 50 ให้แม่น: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47",
            "การแยกตัวประกอบ คือการเขียนจำนวนนับในรูปการคูณของตัวประกอบเฉพาะเท่านั้น",
            "ถ้าผลบวกของจำนวนเฉพาะ 2 จำนวนเป็นจำนวนคี่ แสดงว่าต้องมีเลข 2 อยู่ด้วยเสมอ (เพราะ คู่ + คี่ = คี่)",
        ],
        "example": {
            "q": "ผลบวกของจำนวนเฉพาะสองจำนวนเท่ากับ 39 ผลคูณของสองจำนวนนี้มีค่าเท่าใด",
            "steps": [
                "ผลบวกเป็น 39 (จำนวนคี่) แสดงว่าต้องเกิดจาก จำนวนคู่ + จำนวนคี่",
                "จำนวนเฉพาะที่เป็นจำนวนคู่มีเพียงตัวเดียวคือ 2 ดังนั้นอีกจำนวนคือ 39 − 2 = 37 (ซึ่งเป็นจำนวนเฉพาะ)",
                "ผลคูณ = 2 × 37 = 74",
            ],
            "a": "74",
        },
        "mistakes": [
            "นับ 1 เป็นจำนวนเฉพาะ หรือคิดว่าเลขคี่ทุกตัว (เช่น 9, 15, 21, 27, 51, 57, 91) เป็นจำนวนเฉพาะ (ระวัง 51 = 3×17, 91 = 7×13)",
            "แยกตัวประกอบแล้วยังมีจำนวนประกอบปนอยู่ เช่น 24 = 4 × 6",
        ],
        "tips": [
            "ระวังตัวลวงยอดฮิตในห้องสอบ: 51 (3×17), 57 (3×19), 87 (3×29), 91 (7×13) ไม่ใช่จำนวนเฉพาะ!",
        ],
    },
    weight=1.4,
)

_PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


@template("m.num.prime", "easy")
def _prime_range_count_or_sum():
    lo, hi = pick([
        (1, 20), (10, 30), (20, 40), (30, 50), (40, 60), (50, 75), (1, 15), (15, 35)
    ])
    ps = [p for p in _PRIMES_100 if lo <= p <= hi]
    ask = random.choice(["count", "sum"])
    if ask == "count":
        ans = len(ps)
        return mcq(
            stem=f"ตั้งแต่ **{lo} ถึง {hi}** มีจำนวนเฉพาะทั้งหมดกี่จำนวน",
            correct=f"{ans} จำนวน",
            wrongs=[
                W(f"{ans + 1} จำนวน", "เผลอนับ 1 หรือจำนวนคี่ที่ไม่ใช่จำนวนเฉพาะ (เช่น 9, 15, 21, 27, 33, 39, 49, 51, 57) รวมเข้าไปด้วย", "trap"),
                W(f"{ans - 1} จำนวน", "นับจำนวนเฉพาะตกหล่นไป 1 ตัว (เช่น ลืม 2 หรือจำนวนเฉพาะช่วงท้าย)", "calc"),
                W(f"{ans + 2} จำนวน", "นับจำนวนคี่ที่หารด้วย 3 หรือ 7 ลงตัวเป็นจำนวนเฉพาะ", "concept"),
            ],
            hint="ระวัง! 1 ไม่ใช่จำนวนเฉพาะ และเช็กเลขคี่ที่หารด้วย 3, 7 ลงตัวออกให้หมด",
            steps=[
                f"จำนวนเฉพาะตั้งแต่ {lo} ถึง {hi} ได้แก่ {', '.join(str(p) for p in ps)}",
                f"นับรวมได้ทั้งหมด {ans} จำนวน",
            ],
        )
    else:
        ans = sum(ps)
        return mcq(
            stem=f"ผลบวกของจำนวนเฉพาะทั้งหมดที่อยู่ระหว่าง **{lo} ถึง {hi}** มีค่าเท่าใด",
            correct=num(ans),
            wrongs=[
                W(num(ans + (1 if lo == 1 else lo + 1)), "เผลอบวกเลขที่ไม่ใช่จำนวนเฉพาะ (เช่น 1 หรือจำนวนประกอบคี่) เข้าไปด้วย", "trap"),
                W(num(ans - ps[-1]), f"ลืมบวกจำนวนเฉพาะตัวสุดท้ายในช่วงคือ {ps[-1]}", "partial"),
                W(num(ans + 2), "บวกเลขในใจผิดพลาดไป 2", "calc"),
            ],
            hint=f"เขียนจำนวนเฉพาะในช่วง {lo} ถึง {hi} ออกมาทุกตัวก่อนแล้วค่อยนำมาบวกกัน",
            steps=[
                f"จำนวนเฉพาะในช่วง {lo} ถึง {hi} คือ {', '.join(str(p) for p in ps)}",
                f"ผลบวก = {' + '.join(str(p) for p in ps)} = {num(ans)}",
            ],
        )


@template("m.num.prime", "medium")
def _prime_factorisation_exponents():
    a = random.randint(1, 4)
    b = random.randint(1, 3)
    c = random.randint(1, 2)
    p3 = random.choice([5, 7, 11])
    n_val = (2 ** a) * (3 ** b) * (p3 ** c)
    if n_val > 5000:
        return None
    ask = random.choice(["sum_exp", "sum_distinct_primes"])
    if ask == "sum_exp":
        ans = a + b + c
        return mcq(
            stem=(
                f"เมื่อแยกตัวประกอบของ **{num(n_val)}** ในรูปเลขยกกำลังจะได้ "
                f"**{num(n_val)} = 2^a × 3^b × {p3}^c** จงหาค่าของ **a + b + c**"
            ),
            correct=str(ans),
            wrongs=[
                W(str(a * b * c if a * b * c != ans else ans + 2), "นำเลขชี้กำลังมาคูณกันแทนที่จะบวกกัน", "misread"),
                W(str(2 + 3 + p3), f"นำฐานของตัวประกอบเฉพาะ (2 + 3 + {p3}) มาบวกกันแทนเลขชี้กำลัง", "misread"),
                W(str(ans - 1), f"หารแยกตัวประกอบของ 2 หรือ 3 ไม่สุด ขาดไป 1 ตัว", "calc"),
            ],
            hint=f"นำ {num(n_val)} มาตั้งหารสั้นด้วยจำนวนเฉพาะ 2, 3, {p3} แล้วนับว่ามีแต่ละตัวกี่ตัว",
            steps=[
                f"แยกตัวประกอบของ {num(n_val)} ได้ = (2^{a}) × (3^{b}) × ({p3}^{c})",
                f"ดังนั้น a = {a}, b = {b}, c = {c}",
                f"จะได้ a + b + c = {a} + {b} + {c} = {ans}",
            ],
        )
    else:
        ans = 2 + 3 + p3
        total_with_mult = 2 * a + 3 * b + p3 * c
        return mcq(
            stem=f"ผลบวกของ **ตัวประกอบเฉพาะที่แตกต่างกันทั้งหมด** ของ **{num(n_val)}** มีค่าเท่าใด",
            correct=str(ans),
            wrongs=[
                W(str(total_with_mult), "นำตัวประกอบเฉพาะที่ซ้ำกันมาบวกทั้งหมด โจทย์ถามเฉพาะตัวประกอบเฉพาะที่แตกต่างกัน", "misread"),
                W(str(ans + 1), "เผลอนับ 1 เป็นตัวประกอบเฉพาะด้วย (1 ไม่ใช่จำนวนเฉพาะ)", "concept"),
                W(str(a + b + c), "ตอบเป็นจำนวนตัวประกอบเฉพาะแทนผลบวกของตัวประกอบเฉพาะ", "misread"),
            ],
            hint="แยกตัวประกอบของจำนวนนี้ แล้วดูว่ามีจำนวนเฉพาะตัวใดบ้างที่เป็นตัวประกอบ (ไม่ต้องบวกซ้ำ)",
            steps=[
                f"แยกตัวประกอบ: {num(n_val)} = (2^{a}) × (3^{b}) × ({p3}^{c})",
                f"ตัวประกอบเฉพาะที่แตกต่างกัน ได้แก่ 2, 3 และ {p3}",
                f"ผลบวก = 2 + 3 + {p3} = {ans}",
            ],
        )


@template("m.num.prime", "hard")
def _prime_even_odd_trap():
    # Sum of two primes is an odd number (2 + odd_prime) -> find product!
    odd_primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    p = random.choice(odd_primes)
    s = 2 + p
    ans = 2 * p
    # Tempting wrong: splitting s into two numbers that aren't both prime, e.g. 9 + (s-9) or 1 + (s-1)
    fake1 = 1 * (s - 1)
    fake2 = 9 * (s - 9) if s > 15 else 3 * (s - 3)
    return mcq(
        stem=(
            f"จำนวนเฉพาะสองจำนวนมีผลบวกเท่ากับ **{s}** "
            f"จงหาว่า **ผลคูณ** ของจำนวนเฉพาะทั้งสองจำนวนนี้มีค่าเท่าใด"
        ),
        correct=num(ans),
        wrongs=[
            W(num(fake1), f"ใช้ 1 กับ {s - 1} แต่ 1 ไม่ใช่จำนวนเฉพาะ", "concept"),
            W(num(fake2), "แยกผลบวกเป็นจำนวนคี่ที่ไม่ใช่จำนวนเฉพาะ (เช่น 9 หรือ 15 หรือ 21)", "trap"),
            W(num(s * 2), "นำผลบวกไปคูณ 2 โดยไม่ได้แยกหาจำนวนเฉพาะแต่ละตัวก่อน", "calc"),
        ],
        hint=f"ผลบวกเป็นจำนวนคี่ ({s}) แสดงว่าต้องเกิดจาก จำนวนคู่ + จำนวนคี่ และจำนวนเฉพาะที่เป็นเลขคู่มีเพียงตัวเดียว!",
        steps=[
            f"เนื่องจาก {s} เป็นจำนวนคี่ การบวกกันของจำนวนนับ 2 จำนวนที่ได้ผลลัพธ์เป็นคี่ ต้องเกิดจาก คู่ + คี่",
            f"จำนวนเฉพาะที่เป็นจำนวนคู่มีเพียงตัวเดียวคือ 2 ดังนั้นอีกจำนวนคือ {s} − 2 = {p}",
            f"ผลคูณของทั้งสองจำนวน = 2 × {p} = {num(ans)}",
        ],
    )


# ===========================================================================
# Skill 5: m.num.factors — ตัวประกอบและจำนวนตัวประกอบ
# ===========================================================================

skill(
    "m.num.factors",
    "m.num",
    "ตัวประกอบและจำนวนตัวประกอบ",
    lesson={
        "concept": (
            "ตัวประกอบของ N คือจำนวนนับที่หาร N ลงตัว หากเขียน N ในรูปแยกตัวประกอบเฉพาะ "
            "N = p^a × q^b × ... จำนวนตัวประกอบทั้งหมดจะหาได้จากสูตร (a + 1)(b + 1)..."
        ),
        "steps": [
            "แยกตัวประกอบของ N ให้อยู่ในรูปเลขยกกำลังของจำนวนเฉพาะ",
            "นำเลขชี้กำลังของแต่ละตัวมาบวก 1 แล้วนำมาคูณกัน จะได้จำนวนตัวประกอบบวกทั้งหมด",
            "ถ้าต้องการคูณให้เป็นกำลังสองสมบูรณ์ ให้หาจำนวนมาคูณเพื่อให้เลขชี้กำลังทุกตัวเป็นจำนวนคู่",
        ],
        "example": {
            "q": "72 มีตัวประกอบทั้งหมดกี่จำนวน",
            "steps": [
                "แยกตัวประกอบ: 72 = 8 × 9 = 2^3 × 3^2",
                "นำเลขชี้กำลังบวก 1 แล้วคูณกัน: (3 + 1) × (2 + 1) = 4 × 3 = 12",
            ],
            "a": "12 จำนวน",
        },
        "mistakes": [
            "นำเลขชี้กำลังมาคูณกันเลยโดยลืมบวก 1 ก่อน (เช่น 3 × 2 = 6 แทนที่จะเป็น 4 × 3 = 12)",
            "เวลาไล่ตัวประกอบเป็นคู่ ๆ ของจำนวนกำลังสองสมบูรณ์ (เช่น 36) เผลอนับ 6 ซ้ำสองครั้ง",
        ],
        "tips": [
            "จำนวนที่มีตัวประกอบเป็นจำนวนคี่ตัว คือ 'จำนวนกำลังสองสมบูรณ์' เสมอ (และจำนวนที่มีตัวประกอบ 3 ตัว คือกำลังสองของจำนวนเฉพาะ)",
        ],
    },
    weight=1.3,
)


@template("m.num.factors", "easy")
def _factor_count_medium_num():
    a = random.randint(2, 4)
    b = random.randint(1, 3)
    c = random.choice([0, 1])
    p3 = random.choice([5, 7])
    n_val = (2 ** a) * (3 ** b) * (p3 ** c)
    ans = (a + 1) * (b + 1) * (c + 1)
    wrong_no_plus1 = a * b * (c if c > 0 else 1)
    wrong_sum = (a + 1) + (b + 1) + (c + 1 if c > 0 else 0)
    if wrong_sum in (ans, wrong_no_plus1, ans - 2):
        wrong_sum = ans + 2
    exp_str = f"2^{a} × 3^{b}" + (f" × {p3}^{c}" if c > 0 else "")
    formula_str = f"({a}+1)({b}+1)" + (f"({c}+1)" if c > 0 else "")
    return mcq(
        stem=f"จำนวนนับ **{num(n_val)}** มีตัวประกอบทั้งหมดกี่จำนวน",
        correct=f"{ans} จำนวน",
        wrongs=[
            W(f"{wrong_no_plus1} จำนวน", "นำเลขชี้กำลังมาคูณกันโดยลืมบวก 1 ที่เลขชี้กำลังแต่ละตัว", "formula"),
            W(f"{ans - 2} จำนวน", "ลืมนับ 1 และตัวมันเองว่าเป็นตัวประกอบด้วย", "partial"),
            W(f"{wrong_sum} จำนวน", "นำ (เลขชี้กำลัง + 1) มาบวกกันแทนที่จะคูณกัน", "formula"),
        ],
        hint="แยกตัวประกอบให้อยู่ในรูปเลขยกกำลัง แล้วนำ (เลขชี้กำลัง + 1) ของแต่ละฐานมาคูณกัน",
        steps=[
            f"แยกตัวประกอบของ {num(n_val)} ได้ = {exp_str}",
            f"จำนวนตัวประกอบทั้งหมด = {formula_str} = {ans} จำนวน",
        ],
    )


@template("m.num.factors", "medium")
def _make_perfect_square():
    # Smallest positive integer k such that N * k is a perfect square
    odd_primes = random.sample([2, 3, 5, 7, 11], random.choice([1, 2]))
    k = 1
    for p in odd_primes:
        k *= p
    sq_root = random.randint(3, 8)
    n_val = k * (sq_root ** 2)
    if n_val > 1200:
        return None
    resulting_root = k * sq_root
    return mcq(
        stem=(
            f"จำนวนนับที่ **น้อยที่สุด** ที่นำมาคูณกับ **{num(n_val)}** "
            f"แล้วทำให้ผลคูณเป็น **กำลังสองสมบูรณ์** คือจำนวนใด"
        ),
        correct=str(k),
        wrongs=[
            W(str(resulting_root), f"นี่คือรากที่สองของผลคูณ ({resulting_root} × {resulting_root} = {num(n_val * k)}) ไม่ใช่ตัวที่นำมาคูณเพิ่ม", "misread"),
            W(str(sq_root), f"{sq_root} มีคู่กำลังสองอยู่แล้ว ({sq_root}^2 = {sq_root ** 2}) ไม่ต้องคูณซ้ำ", "concept"),
            W(str(k * 2 if k != 2 else 6), "แยกตัวประกอบแล้วยังจัดกลุ่มคู่ได้ไม่ครบ", "calc"),
        ],
        hint="แยกตัวประกอบของจำนวนนี้ แล้วดูว่าตัวประกอบเฉพาะตัวใดที่มีจำนวนตัวเป็นเลขคี่ (ยังจับคู่ได้ไม่ครบ)",
        steps=[
            f"แยกตัวประกอบ: {num(n_val)} = {k} × {sq_root}^2",
            f"จะเห็นว่าส่วนที่เป็นกำลังสองสมบูรณ์แล้วคือ {sq_root}^2 เหลือ {k} ที่ยังไม่มีคู่",
            f"ดังนั้นต้องคูณด้วย {k} เป็นอย่างน้อย เพื่อให้เป็นกำลังสองสมบูรณ์",
        ],
    )


@template("m.num.factors", "challenge")
def _even_factors_or_3_factors():
    mode = random.choice(["even_factors", "three_factors"])
    if mode == "even_factors":
        a = random.randint(2, 4)
        b = random.randint(1, 3)
        c = random.choice([1, 2])
        n_val = (2 ** a) * (3 ** b) * (5 ** c)
        total_factors = (a + 1) * (b + 1) * (c + 1)
        odd_factors = (b + 1) * (c + 1)
        even_factors = a * (b + 1) * (c + 1)
        return mcq(
            stem=f"จำนวนนับ **{num(n_val)}** มีตัวประกอบที่เป็น **จำนวนคู่** ทั้งหมดกี่จำนวน",
            correct=f"{even_factors} จำนวน",
            wrongs=[
                W(f"{total_factors} จำนวน", "นี่คือจำนวนตัวประกอบทั้งหมด (รวมทั้งตัวประกอบที่เป็นจำนวนคี่ด้วย)", "partial"),
                W(f"{odd_factors} จำนวน", "นี่คือจำนวนตัวประกอบที่เป็นจำนวนคี่ ไม่ใช่จำนวนคู่", "misread"),
                W(f"{total_factors // 2 if total_factors // 2 != even_factors else even_factors - 2} จำนวน",
                  "เข้าใจผิดว่าตัวประกอบคู่กับคี่จะมีจำนวนเท่ากันครึ่งต่อครึ่งเสมอ", "concept"),
            ],
            hint="หาจำนวนตัวประกอบทั้งหมดก่อน แล้วลบออกด้วยจำนวนตัวประกอบที่เป็นจำนวนคี่ (ตัวที่ไม่มี 2 เป็นตัวประกอบ)",
            steps=[
                f"แยกตัวประกอบ: {num(n_val)} = 2^{a} × 3^{b} × 5^{c}",
                f"ตัวประกอบทั้งหมดมี ({a}+1)({b}+1)({c}+1) = {total_factors} จำนวน",
                f"ตัวประกอบที่เป็นจำนวนคี่ (ไม่ใช้เลข 2 เลย) มี ({b}+1)({c}+1) = {odd_factors} จำนวน",
                f"ดังนั้นตัวประกอบที่เป็นจำนวนคู่มี {total_factors} − {odd_factors} = {even_factors} จำนวน",
            ],
        )
    else:
        # How many integers from lo to hi have EXACTLY 3 positive factors? (Squares of primes: 4, 9, 25, 49, 121, 169, 289...)
        hi = random.choice([60, 100, 150, 200, 300, 400])
        p_squares = [p * p for p in _PRIMES_100 if p * p <= hi]
        ans = len(p_squares)
        all_squares = int(math.isqrt(hi)) - 1  # excluding 1
        return mcq(
            stem=f"จำนวนนับตั้งแต่ **1 ถึง {hi}** มีกี่จำนวนที่มีตัวประกอบบวก **เพียง 3 ตัวเท่านั้น**",
            correct=f"{ans} จำนวน",
            wrongs=[
                W(f"{all_squares} จำนวน", "นับจำนวนกำลังสองสมบูรณ์ทุกตัว (เช่น 16, 36, 64 มีตัวประกอบมากกว่า 3 ตัว)", "trap"),
                W(f"{ans + 1} จำนวน", "เผลอนับ 1 หรือ 81 (3^4 มีตัวประกอบ 5 ตัว) รวมเข้าไปด้วย", "trap"),
                W(f"{ans - 1} จำนวน", "ลืมนับเลข 4 (2^2) เพราะลืมว่า 2 เป็นจำนวนเฉพาะ", "partial"),
            ],
            hint="จำนวนที่มีตัวประกอบ 3 ตัว ต้องอยู่ในรูป p^2 เมื่อ p เป็นจำนวนเฉพาะเท่านั้น",
            steps=[
                "จากสูตรจำนวนตัวประกอบ (a + 1) = 3 จะได้ a = 2 นั่นคือต้องเป็นกำลังสองของจำนวนเฉพาะ (p^2)",
                f"กำลังสองของจำนวนเฉพาะที่ไม่เกิน {hi} ได้แก่ {', '.join(str(x) for x in p_squares)}",
                f"จึงมีทั้งหมด {ans} จำนวน",
            ],
        )


# ===========================================================================
# Skill 6: m.num.gcd_lcm — ห.ร.ม. และ ค.ร.น. (สมบัติและการคำนวณ)
# ===========================================================================

skill(
    "m.num.gcd_lcm",
    "m.num",
    "ห.ร.ม. และ ค.ร.น. (สมบัติและเศษเหลือ)",
    lesson={
        "concept": (
            "ห.ร.ม. คือจำนวนที่มากที่สุดที่หารทุกจำนวนลงตัว ส่วน ค.ร.น. คือจำนวนที่น้อยที่สุดที่ทุกจำนวนหารลงตัว "
            "สำหรับจำนวนนับสองจำนวน A และ B จะมีสมบัติสำคัญคือ A × B = ห.ร.ม. × ค.ร.น."
        ),
        "steps": [
            "ถ้ารู้ ห.ร.ม. = g และ ค.ร.น. = L ของสองจำนวน สามารถเขียนสองจำนวนในรูป g×x และ g×y โดยที่ ห.ร.ม.(x, y) = 1 และ g×x×y = L",
            "โจทย์ 'จำนวนที่น้อยที่สุดที่หารด้วย a, b, c แล้วเหลือเศษ r เท่ากัน' ให้หา ค.ร.น.(a, b, c) + r",
            "โจทย์ 'จำนวนที่มากที่สุดที่นำไปหาร x, y, z แล้วเหลือเศษ r1, r2, r3' ให้หา ห.ร.ม. ของ (x − r1), (y − r2), (z − r3)",
        ],
        "example": {
            "q": "จำนวนนับที่น้อยที่สุดที่หารด้วย 6, 8 และ 12 แล้วเหลือเศษ 5 เท่ากันคือจำนวนใด",
            "steps": [
                "หา ค.ร.น. ของ 6, 8 และ 12 ได้เท่ากับ 24",
                "ต้องการให้เหลือเศษ 5 จึงนำ ค.ร.น. บวกเศษ: 24 + 5 = 29",
            ],
            "a": "29",
        },
        "mistakes": [
            "สลับวิธีทำระหว่างโจทย์ 'หารด้วย ... เหลือเศษ' (ใช้ ค.ร.น.) กับ 'นำไปหาร ... เหลือเศษ' (ใช้ ห.ร.ม.)",
            "ลืมบวกเศษหลังจากหา ค.ร.น. เสร็จ หรือเผลอนำเศษไปลบก่อนหา ค.ร.น.",
        ],
        "tips": [
            "จำคำสำคัญ: 'หารด้วย...' = เราเป็นตัวตั้ง (ตัวใหญ่ → ใช้ ค.ร.น.) · 'นำไปหาร...' = เราเป็นตัวหาร (ตัวเล็ก → ใช้ ห.ร.ม.)",
        ],
    },
    weight=1.8,
)


@template("m.num.gcd_lcm", "easy")
def _gcd_lcm_three_numbers():
    g = random.randint(2, 9)
    triples = [(2, 3, 4), (2, 3, 5), (2, 4, 6), (3, 4, 6), (2, 5, 6), (3, 5, 6)]
    t1, t2, t3 = pick(triples)
    a, b, c = g * t1, g * t2, g * t3
    gcd_val = math.gcd(math.gcd(a, b), c)
    lcm_val = math.lcm(math.lcm(a, b), c)
    ans = lcm_val - gcd_val
    return mcq(
        stem=f"ผลต่างของ **ค.ร.น.** และ **ห.ร.ม.** ของ **{a}, {b}** และ **{c}** มีค่าเท่าใด",
        correct=num(ans),
        wrongs=[
            W(num(lcm_val + gcd_val), "นำ ค.ร.น. กับ ห.ร.ม. มาบวกกัน โจทย์ถามผลต่างจึงต้องลบกัน", "misread"),
            W(num(lcm_val), "ตอบเฉพาะค่า ค.ร.น. ลืมลบออกด้วย ห.ร.ม.", "partial"),
            W(num(a * b * c // (gcd_val ** 2) - gcd_val if a * b * c // (gcd_val ** 2) != lcm_val else ans + g),
              "หา ค.ร.น. ของ 3 จำนวนโดยหารเฉพาะตัวที่หารลงตัวทั้ง 3 จำนวนเท่านั้น ไม่ได้หารต่อทีละ 2 จำนวน", "concept"),
        ],
        hint="ตั้งหารสั้นหา ห.ร.ม. (ต้องหารลงตัวทั้ง 3 จำนวน) และหา ค.ร.น. (หารลงตัวตั้งแต่ 2 จำนวนขึ้นไป) แล้วนำมาลบกัน",
        steps=[
            f"ห.ร.ม. ของ {a}, {b} และ {c} คือ {gcd_val}",
            f"ค.ร.น. ของ {a}, {b} และ {c} คือ {lcm_val}",
            f"ผลต่าง = {lcm_val} − {gcd_val} = {num(ans)}",
        ],
    )


@template("m.num.gcd_lcm", "medium")
def _gcd_lcm_product_relation():
    g = random.randint(3, 12)
    coprime_pairs = [(2, 3), (2, 5), (3, 4), (3, 5), (4, 5), (2, 7), (3, 7), (5, 6)]
    x, y = pick(coprime_pairs)
    a, b = g * x, g * y
    lcm_val = g * x * y
    mode = random.choice(["find_other", "min_sum"])
    if mode == "find_other":
        return mcq(
            stem=(
                f"จำนวนนับสองจำนวนมี **ห.ร.ม. เท่ากับ {g}** และ **ค.ร.น. เท่ากับ {num(lcm_val)}** "
                f"ถ้าจำนวนหนึ่งคือ **{a}** อีกจำนวนหนึ่งคือข้อใด"
            ),
            correct=num(b),
            wrongs=[
                W(num(lcm_val // a), "นำ ค.ร.น. หารด้วยจำนวนที่รู้ค่าเลย โดยลืมคูณด้วย ห.ร.ม.", "formula"),
                W(num(lcm_val - a), "นำ ค.ร.น. ลบด้วยจำนวนที่รู้ค่า แทนที่จะใช้สูตรความสัมพันธ์ของการคูณ", "concept"),
                W(num(b * g), f"คูณด้วย ห.ร.ม. ({g}) ซ้ำสองครั้ง", "calc"),
            ],
            hint="ใช้ความสัมพันธ์: จำนวนที่หนึ่ง × จำนวนที่สอง = ห.ร.ม. × ค.ร.น.",
            steps=[
                "จากสูตร จำนวนที่หนึ่ง × จำนวนที่สอง = ห.ร.ม. × ค.ร.น.",
                f"จะได้ {a} × จำนวนที่สอง = {g} × {num(lcm_val)}",
                f"จำนวนที่สอง = ({g} × {num(lcm_val)}) ÷ {a} = {num(b)}",
            ],
        )
    else:
        # Given GCD = g and LCM = lcm_val (with x*y having two coprime factorisations: (1, x*y) and (x, y)), find minimum A + B
        ans = a + b
        max_sum = g * (1 + x * y)
        diff_ab = abs(b - a)
        if diff_ab in (ans, max_sum, x + y):
            diff_ab = ans - g
        return mcq(
            stem=(
                f"จำนวนนับสองจำนวนมี **ห.ร.ม. เท่ากับ {g}** และ **ค.ร.น. เท่ากับ {num(lcm_val)}** "
                f"ผลบวกที่ **น้อยที่สุด** ของจำนวนทั้งสองมีค่าเท่าใด"
            ),
            correct=num(ans),
            wrongs=[
                W(num(max_sum), f"นี่คือผลบวกกรณีที่จำนวนหนึ่งเป็น {g} และอีกจำนวนเป็น {num(lcm_val)} ซึ่งให้ผลบวกมากที่สุด ไม่ใช่น้อยที่สุด", "trap"),
                W(num(x + y), f"ลืมคูณด้วย ห.ร.ม. ({g}) กลับเข้าไปในตัวประกอบ", "partial"),
                W(num(diff_ab), "นำจำนวนทั้งสองมาลบกันแทนที่จะบวกกัน", "misread"),
            ],
            hint=f"ให้สองจำนวนคือ {g}x และ {g}y จะได้ x × y = {num(lcm_val)} ÷ {g} = {x * y} แล้วเลือกคู่ (x, y) ที่ใกล้กันที่สุด",
            steps=[
                f"ให้สองจำนวนคือ {g}x และ {g}y โดยที่ ห.ร.ม.(x, y) = 1",
                f"จาก ค.ร.น. = {g} × x × y = {num(lcm_val)} จะได้ x × y = {x * y}",
                f"เพื่อให้ผลบวกน้อยที่สุด เลือก x = {x}, y = {y} ได้สองจำนวนคือ {a} และ {b}",
                f"ผลบวกที่น้อยที่สุด = {a} + {b} = {num(ans)}",
            ],
        )


@template("m.num.gcd_lcm", "hard")
def _lcm_remainder_patterns():
    # Classic top-school: either same remainder r, or constant difference (divisor - remainder) = d
    triples = [(4, 6, 8), (6, 8, 9), (6, 9, 12), (8, 10, 12), (5, 6, 8), (6, 8, 10), (9, 12, 15)]
    a, b, c = pick(triples)
    lcm_val = math.lcm(math.lcm(a, b), c)
    mode = random.choice(["same_rem", "const_diff"])
    if mode == "same_rem":
        r = random.randint(1, a - 1)
        ans = lcm_val + r
        return mcq(
            stem=(
                f"จำนวนนับที่มากกว่า {r} และมีค่า **น้อยที่สุด** ที่เมื่อนำ **{a}, {b}** และ **{c}** ไปหารแล้ว "
                f"เหลือเศษ **{r}** เท่ากันทุกครั้ง คือจำนวนใด"
            ),
            correct=num(ans),
            wrongs=[
                W(num(lcm_val), f"หาแต่ ค.ร.น. ({lcm_val}) แล้วลืมบวกเศษ {r}", "partial"),
                W(num(lcm_val - r), f"นำเศษ {r} ไปลบออกจาก ค.ร.น. แทนที่จะบวกเข้า", "sign"),
                W(num(a * b * c + r if a * b * c != lcm_val else ans + lcm_val), "นำตัวหารทั้งสามมาคูณกันเฉย ๆ แทนที่จะหา ค.ร.น. ที่น้อยที่สุด", "concept"),
            ],
            hint=f"หา ค.ร.น. ของ {a}, {b}, {c} เพื่อให้หารลงตัวก่อน แล้วบวกด้วยเศษ {r}",
            steps=[
                f"หา ค.ร.น. ของ {a}, {b} และ {c} ได้เท่ากับ {lcm_val}",
                f"ต้องการให้หารแล้วเหลือเศษ {r} เท่ากัน จึงนำ ค.ร.น. บวกเศษ",
                f"จำนวนที่น้อยที่สุด = {lcm_val} + {r} = {num(ans)}",
            ],
        )
    else:
        diff = random.randint(1, a - 1)
        r1, r2, r3 = a - diff, b - diff, c - diff
        ans = lcm_val - diff
        return mcq(
            stem=(
                f"จำนวนนับที่ **น้อยที่สุด** ซึ่งเมื่อหารด้วย **{a}, {b}** และ **{c}** "
                f"จะเหลือเศษ **{r1}, {r2}** และ **{r3}** ตามลำดับ คือจำนวนใด"
            ),
            correct=num(ans),
            wrongs=[
                W(num(lcm_val + diff), f"นำผลต่าง {diff} ไปบวกกับ ค.ร.น. แทนที่จะลบออก", "sign"),
                W(num(lcm_val), f"ตอบเป็น ค.ร.น. ({lcm_val}) โดยยังไม่ได้หักส่วนที่ขาดอีก {diff}", "partial"),
                W(num(lcm_val - r1), f"นำเศษตัวแรก ({r1}) ไปลบออกจาก ค.ร.น. แทนที่จะลบด้วยผลต่างคงที่ ({diff})", "concept"),
            ],
            hint=f"สังเกตว่า ตัวหาร ลบ เศษ มีค่าเท่ากันทุกตัว คือ {a}−{r1} = {b}−{r2} = {c}−{r3} = {diff} (ขาดอีก {diff} จะหารลงตัว)",
            steps=[
                f"สังเกตผลต่างระหว่างตัวหารกับเศษ: {a} − {r1} = {diff}, {b} − {r2} = {diff} และ {c} − {r3} = {diff}",
                f"แสดงว่าถ้าบวกจำนวนนั้นเพิ่มอีก {diff} จะหารด้วย {a}, {b}, {c} ลงตัวพอดี",
                f"ค.ร.น. ของ {a}, {b}, {c} คือ {lcm_val} ดังนั้นจำนวนนั้นคือ {lcm_val} − {diff} = {num(ans)}",
            ],
        )


@template("m.num.gcd_lcm", "challenge")
def _gcd_with_remainders():
    # Largest number that divides X, Y, Z leaving remainders r1, r2, r3
    d = random.choice([12, 14, 15, 16, 18, 21, 24, 28, 32, 36])
    mults = random.sample([3, 4, 5, 7, 8, 9, 11], 3)
    mults.sort()
    m1, m2, m3 = mults
    if math.gcd(math.gcd(m1, m2), m3) != 1:
        return None
    r1 = random.randint(1, d - 3)
    r2 = random.randint(1, d - 2)
    r3 = random.randint(1, d - 1)
    x, y, z = d * m1 + r1, d * m2 + r2, d * m3 + r3
    return mcq(
        stem=(
            f"จำนวนนับที่ **มากที่สุด** ที่นำไปหาร **{num(x)}, {num(y)}** และ **{num(z)}** "
            f"แล้วเหลือเศษ **{r1}, {r2}** และ **{r3}** ตามลำดับ คือจำนวนใด"
        ),
        correct=str(d),
        wrongs=[
            W(str(d // 2 if d % 2 == 0 else d // 3), "เป็นตัวหารร่วมจริง แต่ยังไม่ใช่จำนวนที่มากที่สุด (ยังหารต่อได้อีก)", "partial"),
            W(str(d + r1), "นำเศษไปบวกกับ ห.ร.ม. หลังจากคำนวณเสร็จ", "concept"),
            W(str(math.gcd(d * m1, d * m2) if math.gcd(m1, m2) > 1 else d * 2),
              "หา ห.ร.ม. จากสองจำนวนแรกเท่านั้น หรือลืมลบเศษออกก่อนหา ห.ร.ม.", "partial"),
        ],
        hint="ลบเศษของแต่ละจำนวนออกก่อน เพื่อให้หารลงตัวพอดี แล้วจึงหา ห.ร.ม. ของทั้งสามจำนวน",
        steps=[
            f"หักเศษออกจากตัวตั้งแต่ละตัว: {num(x)} − {r1} = {num(d * m1)}, {num(y)} − {r2} = {num(d * m2)} และ {num(z)} − {r3} = {num(d * m3)}",
            f"หา ห.ร.ม. ของ {num(d * m1)}, {num(d * m2)} และ {num(d * m3)}",
            f"จะได้ ห.ร.ม. เท่ากับ {d}",
        ],
    )


# ===========================================================================
# Skill 7: m.num.gcd_word — โจทย์ปัญหา ห.ร.ม. และ ค.ร.น.
# ===========================================================================

skill(
    "m.num.gcd_word",
    "m.num",
    "โจทย์ปัญหา ห.ร.ม. และ ค.ร.น.",
    lesson={
        "concept": (
            "โจทย์แบ่งของ/ตัดเชือก/ปูกระเบื้อง/ปักเสาให้ได้ขนาดใหญ่ที่สุดและเท่ากัน ใช้ ห.ร.ม. "
            "ส่วนโจทย์เหตุการณ์ที่เกิดขึ้นพร้อมกันอีกครั้ง (ระฆังตี ไฟกะพริบ รถออกพร้อมกัน) ใช้ ค.ร.น."
        ),
        "steps": [
            "อ่านโจทย์ให้ชัดว่าถาม 'ขนาดที่ใหญ่ที่สุดของแต่ละชิ้น' (คือค่า ห.ร.ม.) หรือถาม 'จำนวนชิ้นทั้งหมดที่แบ่งได้'",
            "ถ้าถามจำนวนท่อนเชือก/จำนวนกอง: นำความยาวแต่ละเส้นหารด้วย ห.ร.ม. แล้วนำผลหารมาบวกกัน",
            "ถ้าถามปูกระเบื้องจัตุรัสในห้องผืนผ้า: จำนวนแผ่น = (กว้าง ÷ ห.ร.ม.) × (ยาว ÷ ห.ร.ม.) ต้องคูณกัน ไม่ใช่บวกกัน!",
        ],
        "example": {
            "q": "เชือก 3 เส้นยาว 24, 36 และ 60 เมตร ตัดเป็นท่อนสั้นยาวเท่ากันให้ยาวที่สุดโดยไม่เหลือเศษ จะได้เชือกทั้งหมดกี่ท่อน",
            "steps": [
                "หาความยาวแต่ละท่อน = ห.ร.ม. ของ 24, 36, 60 = 12 เมตร",
                "จำนวนท่อน = (24 ÷ 12) + (36 ÷ 12) + (60 ÷ 12) = 2 + 3 + 5 = 10 ท่อน",
            ],
            "a": "10 ท่อน",
        },
        "mistakes": [
            "โจทย์ถาม 'ได้ทั้งหมดกี่ท่อน' แต่เผลอตอบค่า ห.ร.ม. (ความยาวของแต่ละท่อน)",
            "โจทย์ปูกระเบื้อง เอาจำนวนแถวด้านกว้างบวกด้านยาว แทนที่จะนำมาคูณกัน",
        ],
        "tips": [
            "เวลาตั้งหารสั้นหา ห.ร.ม. เสร็จ ตัวเลขบรรทัดสุดท้ายข้างล่างสุดคือจำนวนชิ้นของแต่ละกอง สามารถนำมาบวกกัน (หรือคูณกันกรณีพื้นที่) ได้ทันที!",
        ],
    },
    weight=1.8,
)


@template("m.num.gcd_word", "medium")
def _rope_cutting_total_pieces():
    g = random.choice([6, 8, 9, 12, 14, 15, 16, 18, 20, 24])
    triples = [(2, 3, 4), (2, 3, 5), (2, 5, 7), (3, 4, 5), (3, 5, 7), (2, 4, 5), (3, 5, 8)]
    q1, q2, q3 = pick(triples)
    l1, l2, l3 = g * q1, g * q2, g * q3
    total_pieces = q1 + q2 + q3
    item_noun, unit_piece = pick([
        ("เชือก 3 เส้น", "ท่อน"),
        ("ริบบิ้น 3 ม้วน", "เส้น"),
        ("ท่อนไม้ 3 ท่อน", "ท่อน"),
        ("ลวด 3 เส้น", "เส้น"),
    ])
    if g == total_pieces:
        return None
    return mcq(
        stem=(
            f"มี{item_noun}ยาว **{l1}, {l2}** และ **{l3}** เซนติเมตร ต้องการตัดแบ่งให้ยาวเท่า ๆ กัน "
            f"โดยแต่ละ{unit_piece}ยาวที่สุดเท่าที่จะทำได้และไม่เหลือเศษ จะตัดได้ทั้งหมดกี่{unit_piece}"
        ),
        correct=f"{total_pieces} {unit_piece}",
        wrongs=[
            W(f"{g} {unit_piece}", f"{g} คือความยาวของแต่ละ{unit_piece} (ค่า ห.ร.ม.) ไม่ใช่จำนวน{unit_piece}ทั้งหมด", "misread"),
            W(f"{q1 * q2 * q3} {unit_piece}", f"นำจำนวน{unit_piece}ของแต่ละเส้นมาคูณกันแทนที่จะบวกกัน", "concept"),
            W(f"{total_pieces - 3} {unit_piece}", f"สับสนระหว่างจำนวน{unit_piece}กับจำนวนรอยตัด", "trap"),
        ],
        hint=f"หา ห.ร.ม. เพื่อหาความยาวของแต่ละ{unit_piece}ก่อน แล้วนำความยาวแต่ละเส้นหารด้วย ห.ร.ม. มาบวกกัน",
        steps=[
            f"ความยาวที่มากที่สุดของแต่ละ{unit_piece} = ห.ร.ม. ของ {l1}, {l2}, {l3} = {g} ซม.",
            f"จำนวน{unit_piece}ที่ได้ = ({l1} ÷ {g}) + ({l2} ÷ {g}) + ({l3} ÷ {g}) = {q1} + {q2} + {q3} = {total_pieces} {unit_piece}",
        ],
    )


@template("m.num.gcd_word", "hard")
def _tiling_or_bells_clock():
    mode = random.choice(["tiles", "bells"])
    if mode == "tiles":
        g = random.choice([15, 20, 24, 25, 30, 35, 40, 45, 50, 60])
        coprimes = [(3, 4), (3, 5), (4, 5), (4, 7), (5, 6), (5, 7), (5, 8), (6, 7), (7, 9)]
        nx, ny = pick(coprimes)
        w, l = g * nx, g * ny
        tiles = nx * ny
        if tiles == g:
            return None
        return mcq(
            stem=(
                f"ห้องรูปสี่เหลี่ยมผืนผ้ากว้าง **{num(w)} เซนติเมตร** ยาว **{num(l)} เซนติเมตร** "
                f"ต้องการปูกระเบื้องรูปสี่เหลี่ยมจัตุรัสขนาดใหญ่ที่สุดเท่าที่เป็นไปได้โดยไม่ตัดกระเบื้องเลย "
                f"จะต้องใช้กระเบื้องทั้งหมดกี่แผ่น"
            ),
            correct=f"{tiles} แผ่น",
            wrongs=[
                W(f"{g} แผ่น", f"{g} ซม. คือความยาวด้านของกระเบื้องแต่ละแผ่น (ห.ร.ม.) ไม่ใช่จำนวนแผ่น", "misread"),
                W(f"{nx + ny} แผ่น", "นำจำนวนแผ่นด้านกว้างบวกกับด้านยาว แทนที่จะนำมาคูณกัน", "formula"),
                W(f"{2 * (nx + ny)} แผ่น", "คิดเฉพาะแนวขอบรอบห้องแทนพื้นที่เต็มห้อง", "formula"),
            ],
            hint="ความยาวด้านของกระเบื้องคือ ห.ร.ม. ของความกว้างและความยาว แล้วนำจำนวนแผ่นด้านกว้างคูณจำนวนแผ่นด้านยาว",
            steps=[
                f"ขนาดกระเบื้องจัตุรัสที่ใหญ่ที่สุด = ห.ร.ม. ของ {num(w)} และ {num(l)} = {g} เซนติเมตร",
                f"ด้านกว้างปูได้ {num(w)} ÷ {g} = {nx} แผ่น และด้านยาวปูได้ {num(l)} ÷ {g} = {ny} แผ่น",
                f"จำนวนกระเบื้องทั้งหมด = {nx} × {ny} = {tiles} แผ่น",
            ],
        )
    else:
        # Bells ringing together with clock time
        triples = [(12, 15, 20), (15, 20, 30), (18, 24, 36), (10, 15, 25), (16, 24, 48), (12, 18, 24), (20, 30, 45)]
        t1, t2, t3 = pick(triples)
        lcm_min = math.lcm(math.lcm(t1, t2), t3)
        start_h = random.randint(6, 10)
        start_m = random.choice([0, 15, 30, 45])
        total_m = start_h * 60 + start_m + lcm_min
        end_h, end_m = divmod(total_m, 60)
        ans = f"{end_h:02d}:{end_m:02d} น."
        # Distractors: treating minutes as base-100, or using GCD, or forgetting start_m
        wrong_100_h = start_h + (start_m + lcm_min) // 100
        wrong_100_m = (start_m + lcm_min) % 100
        wrong_100 = f"{wrong_100_h:02d}:{wrong_100_m:02d} น."
        wrong_plus1h = f"{end_h + 1:02d}:{end_m:02d} น."
        wrong_sum_m = start_h * 60 + start_m + (t1 + t2 + t3)
        wh2, wm2 = divmod(wrong_sum_m, 60)
        wrong_sum = f"{wh2:02d}:{wm2:02d} น."
        return mcq(
            stem=(
                f"ระฆัง 3 ใบ ตีทุก ๆ **{t1} นาที, {t2} นาที** และ **{t3} นาที** ตามลำดับ "
                f"ถ้าระฆังทั้งสามใบตีพร้อมกันครั้งแรกเวลา **{start_h:02d}:{start_m:02d} น.** "
                f"ระฆังทั้งสามจะตีพร้อมกันครั้งต่อไปเวลาใด"
            ),
            correct=ans,
            wrongs=[
                W(wrong_sum, f"นำเวลา {t1}+{t2}+{t3} = {t1 + t2 + t3} นาที มาบวกแทนการหา ค.ร.น.", "concept"),
                W(wrong_plus1h, "แปลงนาทีเป็นชั่วโมงเกินไป 1 ชั่วโมง", "unit"),
                W(wrong_100 if wrong_100 != ans else f"{end_h:02d}:{(end_m + 20) % 60:02d} น.",
                  "ทดเวลา 1 ชั่วโมงเป็น 100 นาที แทนที่จะเป็น 60 นาที", "unit"),
            ],
            hint="หา ค.ร.น. ของเวลาทั้งสาม (เป็นนาที) แล้วแปลงเป็นชั่วโมงและนาทีไปบวกต่อจากเวลาเริ่มต้น",
            steps=[
                f"ค.ร.น. ของ {t1}, {t2} และ {t3} คือ {lcm_min} นาที",
                f"คิดเป็น {lcm_min // 60} ชั่วโมง {lcm_min % 60} นาที",
                f"นับต่อจาก {start_h:02d}:{start_m:02d} น. ไปอีก {lcm_min} นาที เป็นเวลา {ans}",
            ],
        )


@template("m.num.gcd_word", "challenge")
def _fence_posts_with_gate():
    # Fencing around a rectangular plot with max equal spacing, minus gate!
    g = random.choice([4, 5, 6, 8, 10, 12])
    coprimes = [(4, 7), (5, 7), (5, 8), (5, 9), (6, 11), (7, 9), (7, 10)]
    nx, ny = pick(coprimes)
    w, l = g * nx, g * ny
    perim = 2 * (w + l)
    total_posts = perim // g
    gate_spans = random.choice([1, 2])
    gate_w = gate_spans * g
    # If a gate of width gate_spans * g is left open between existing posts, (gate_spans - 1) interior posts are removed;
    # simpler & clearer standard exam phrasing: cost of posts around the whole perimeter
    cost_per_post = random.choice([120, 150, 180, 200, 250])
    total_cost = total_posts * cost_per_post
    return mcq(
        stem=(
            f"ที่ดินรูปสี่เหลี่ยมผืนผ้ากว้าง **{w} เมตร** ยาว **{l} เมตร** ต้องการปักเสาล้อมรอบที่ดิน "
            f"โดยปักที่มุมทั้งสี่และให้เสาแต่ละต้นห่างเท่า ๆ กันมากที่สุดเท่าที่เป็นไปได้ "
            f"ถ้าเสาราคาต้นละ **{num(cost_per_post)} บาท** จะต้องจ่ายค่าเสาทั้งหมดกี่บาท"
        ),
        correct=f"{num(total_cost)} บาท",
        wrongs=[
            W(f"{num((total_posts + 4) * cost_per_post)} บาท", "บวกเสาที่มุมซ้ำอีก 4 ต้น (การปักเสารอบรูปปิด จำนวนเสา = ความยาวรอบรูป ÷ ระยะห่าง พอดี)", "trap"),
            W(f"{num((nx + ny) * cost_per_post)} บาท", "คิดเฉพาะด้านกว้าง 1 ด้านและด้านยาว 1 ด้าน ลืมคูณ 2 ให้ครบรอบรูป", "partial"),
            W(f"{num((nx * ny) * cost_per_post)} บาท", "นำจำนวนช่องด้านกว้างคูณด้านยาวเหมือนหาพื้นที่ แทนที่จะคิดตามความยาวรอบรูป", "formula"),
        ],
        hint="ระยะห่างระหว่างเสาที่มากที่สุดคือ ห.ร.ม. ของความกว้างและความยาว และรูปปิดจะมีจำนวนเสา = ความยาวรอบรูป ÷ ระยะห่าง",
        steps=[
            f"ระยะห่างระหว่างเสาที่มากที่สุด = ห.ร.ม. ของ {w} และ {l} = {g} เมตร",
            f"ความยาวรอบรูปที่ดิน = 2 × ({w} + {l}) = {perim} เมตร",
            f"จำนวนเสาที่ใช้ปักรอบรูปปิด = {perim} ÷ {g} = {total_posts} ต้น",
            f"คิดเป็นเงินค่าเสา = {total_posts} × {num(cost_per_post)} = {num(total_cost)} บาท",
        ],
    )


# ===========================================================================
# Skill 8: m.num.int — จำนวนเต็มและเส้นจำนวน
# ===========================================================================

skill(
    "m.num.int",
    "m.num",
    "จำนวนเต็มและเส้นจำนวน",
    lesson={
        "concept": (
            "บนเส้นจำนวน จำนวนที่อยู่ทางขวาจะมีค่ามากกว่าทางซ้ายเสมอ "
            "ระยะห่างระหว่างจุดสองจุดหาได้จาก (ค่ามาก − ค่าน้อย) และการลบด้วยจำนวนเต็มลบคือการบวกด้วยจำนวนตรงข้าม"
        ),
        "steps": [
            "การบวกจำนวนเครื่องหมายต่างกัน ให้นำค่าสัมบูรณ์มาลบกัน แล้วตอบตามเครื่องหมายของตัวที่มีค่าสัมบูรณ์มากกว่า",
            "การลบ: ตัวตั้ง − ตัวลบ = ตัวตั้ง + (จำนวนตรงข้ามของตัวลบ) เช่น 5 − (−3) = 5 + 3 = 8",
            "การคูณและหาร: เครื่องหมายเหมือนกันได้บวก เครื่องหมายต่างกันได้ลบ",
        ],
        "example": {
            "q": "อุณหภูมิบนยอดดอยตอนเช้ามืดวัดได้ −4 °C ตอนบ่ายสูงขึ้น 11 °C ตอนบ่ายอุณหภูมิกี่องศาเซลเซียส",
            "steps": [
                "อุณหภูมิสูงขึ้นคือการบวก: (−4) + 11",
                "= 7 °C",
            ],
            "a": "7 °C",
        },
        "mistakes": [
            "เห็นเครื่องหมายลบซ้อนกัน เช่น −8 − (−5) แล้วนำ 8 + 5 เป็น −13 แทนที่จะเป็น −8 + 5 = −3",
            "หาระยะห่างระหว่าง −4 กับ 7 แล้วตอบ 7 − 4 = 3 แทนที่จะเป็น 7 − (−4) = 11",
        ],
        "tips": [
            "เวลานับระยะบนเส้นจำนวนข้ามเลข 0 ให้คิดแยกเป็น 'ระยะทางซ้ายของ 0' บวกกับ 'ระยะทางขวาของ 0'",
        ],
    },
    weight=1.1,
)


@template("m.num.int", "easy")
def _number_line_distance_fig():
    lo, hi = -6, 6
    a = random.randint(-6, -1)
    b = random.randint(1, 6)
    fig = svg.number_line(
        lo, hi,
        marks={a: "A", b: "B"},
        labels_at=[-6, -4, -2, 0, 2, 4, 6],
        highlight=(a, b),
    )
    dist = b - a
    sum_ab = a + b
    ask = random.choice(["dist", "sub"])
    if ask == "dist":
        return mcq(
            stem="จากเส้นจำนวนที่กำหนด จุด **A** และจุด **B** อยู่ห่างกันกี่หน่วย",
            figure=fig,
            correct=f"{dist} หน่วย",
            wrongs=[
                W(f"{abs(sum_ab) if abs(sum_ab) != dist else dist - 2} หน่วย",
                  f"นำ {b} กับ {abs(a)} มาลบกันแทนที่จะรวมระยะทางทั้งสองฝั่งของ 0", "sign"),
                W(f"{dist + 1} หน่วย", "นับจำนวนขีดแทนที่จะนับจำนวนช่องว่าง", "concept"),
                W(f"{dist - 1} หน่วย", "อ่านค่าของจุด A หรือจุด B คลาดเคลื่อนไป 1 ช่อง", "detail"),
            ],
            hint="อ่านค่าของจุด A และจุด B บนเส้นจำนวน แล้วนำ (ค่ามาก − ค่าน้อย)",
            steps=[
                f"จากเส้นจำนวน จุด A แทน {a} และจุด B แทน {b}",
                f"ระยะห่าง = {b} − ({a}) = {b} + {abs(a)} = {dist} หน่วย",
            ],
        )
    else:
        ans = a - b
        return mcq(
            stem="จากเส้นจำนวนที่กำหนดให้ จงหาค่าของ **A − B**",
            figure=fig,
            correct=str(ans),
            wrongs=[
                W(str(dist), "สลับเอา B − A จึงได้ค่าบวกแทนที่จะเป็นค่าลบ", "sign"),
                W(str(sum_ab), f"นำ A กับ B มาบวกกัน ({a} + {b}) แทนที่จะลบกัน", "sign"),
                W(str(-sum_ab if -sum_ab != ans else ans - 2), "เปลี่ยนเครื่องหมายของทั้งสองจำนวนผิดพลาด", "sign"),
            ],
            hint="อ่านค่า A (ฝั่งลบ) และ B (ฝั่งบวก) แล้วคำนวณ A − B",
            steps=[
                f"จากเส้นจำนวน A = {a} และ B = {b}",
                f"ดังนั้น A − B = {a} − {b} = {ans}",
            ],
        )


@template("m.num.int", "medium")
def _integer_mixed_ops():
    a = random.randint(-18, -6)
    b = random.randint(-12, -3)
    c = random.randint(2, 5)
    d = random.randint(-8, -2)
    # Compute (a - b) * c + d
    diff = a - b  # a + |b|
    ans = diff * c + d
    wrong_no_flip = (a + b) * c + d
    wrong_sign_d = diff * c - d
    return mcq(
        stem=f"จงหาค่าของ **[({a}) − ({b})] × {c} + ({d})**",
        correct=str(ans),
        wrongs=[
            W(str(wrong_no_flip), f"คำนวณ ({a}) − ({b}) เป็น {a + b} เพราะลืมเปลี่ยนลบของจำนวนลบเป็นบวก", "sign"),
            W(str(wrong_sign_d), f"ตอนท้ายนำ {diff * c} ไปบวก {abs(d)} แทนที่จะบวกด้วย ({d})", "sign"),
            W(str(-ans if ans != 0 else ans + 4), "ใส่เครื่องหมายบวก/ลบของผลคูณสลับตรงกันข้าม", "sign"),
        ],
        hint="ระวังเครื่องหมายลบชนลบในวงเล็บ: (−x) − (−y) = −x + y",
        steps=[
            f"คำนวณในวงเล็บใหญ่: ({a}) − ({b}) = {a} + {abs(b)} = {diff}",
            f"นำไปคูณกับ {c}: {diff} × {c} = {diff * c}",
            f"บวกด้วย ({d}): {diff * c} + ({d}) = {ans}",
        ],
    )


@template("m.num.int", "hard")
def _number_line_step_scale_fig():
    # A number line with 8 ticks (0..8 on svg), where only 2 ticks are labelled with integer values spaced by step * gap
    step = random.choice([3, 4, 5, 6, 7])
    start_val = -step * random.randint(3, 5)
    # Build custom SVG number line with 9 ticks (indices 0..8)
    n_ticks = 8
    idx_known1 = random.choice([1, 2])
    idx_known2 = random.choice([5, 6])
    idx_a = 0
    idx_b = random.choice([3, 4, 7])
    val_at = lambda idx: start_val + idx * step
    val_a = val_at(idx_a)
    val_b = val_at(idx_b)
    ans = val_a + val_b

    width = 360
    left, right, y = 24, 24, 42
    pw = width - left - right
    X = lambda idx: left + pw * idx / n_ticks
    parts = [svg.line((left - 10, y), (left + pw + 10, y), cls="fig-axisline")]
    for idx in range(n_ticks + 1):
        parts.append(svg.line((X(idx), y - 5), (X(idx), y + 5), cls="fig-axisline"))
    for idx in (idx_known1, idx_known2):
        parts.append(svg.label((X(idx), y + 18), str(val_at(idx)), size=12, cls="fig-axis", bold=True))
    for idx, name in ((idx_a, "A"), (idx_b, "B")):
        parts.append(svg.dot((X(idx), y), 5))
        parts.append(svg.label((X(idx), y - 16), name, size=13, cls="fig-vertex", bold=True))
    fig = svg.canvas(width, 74, parts)

    gap_ticks = idx_known2 - idx_known1
    gap_val = val_at(idx_known2) - val_at(idx_known1)
    return mcq(
        stem="เส้นจำนวนต่อไปนี้แบ่งช่องห่างเท่า ๆ กันทุกช่อง จงหาค่าของ **A + B**",
        figure=fig,
        correct=str(ans),
        wrongs=[
            W(str(val_b - val_a), "นำค่า B ลบด้วย A แทนที่จะหาผลบวก A + B", "misread"),
            W(str((val_a + step) + val_b), f"นับจำนวนช่องไปหาจุด A ขาดไป 1 ช่อง (แต่ละช่องเท่ากับ {step})", "detail"),
            W(str(val_at(idx_known1) - idx_known1 + val_at(idx_known1) + (idx_b - idx_known1)),
              "คิดแต่ละช่องห่างกันช่องละ 1 หน่วย โดยไม่ได้คำนวณความกว้างต่อช่อง", "concept"),
        ],
        hint=f"หาว่า {gap_ticks} ช่องระหว่าง {val_at(idx_known1)} กับ {val_at(idx_known2)} ห่างกันเท่าไร เพื่อหาว่า 1 ช่องมีค่ากี่หน่วย",
        steps=[
            f"จากจุด {val_at(idx_known1)} ไปถึง {val_at(idx_known2)} ห่างกัน {gap_ticks} ช่อง คิดเป็นระยะ {val_at(idx_known2)} − ({val_at(idx_known1)}) = {gap_val}",
            f"ดังนั้น 1 ช่องมีค่าเท่ากับ {gap_val} ÷ {gap_ticks} = {step} หน่วย",
            f"จะได้ A = {val_a} และ B = {val_b} ดังนั้น A + B = ({val_a}) + ({val_b}) = {ans}",
        ],
    )


# ===========================================================================
# Skill 9: m.num.exp — เลขยกกำลังและปริศนาตัวเลข
# ===========================================================================

skill(
    "m.num.exp",
    "m.num",
    "เลขยกกำลังและปริศนาตัวเลข",
    lesson={
        "concept": (
            "เลขยกกำลัง a^n หมายถึง a คูณกัน n ตัว สมบัติฐานเดียวกัน: (a^m) × (a^n) = a^(m+n) และ (a^m) ÷ (a^n) = a^(m−n) "
            "รวมถึงการสังเกตวัฏจักรเลขโดดหลักหน่วยของเลขยกกำลังและจำนวนศูนย์ลงท้ายที่เกิดจากคู่ 2 × 5 = 10"
        ),
        "steps": [
            "ถ้าฐานยังไม่เท่ากัน (เช่น 4, 8, 16) ให้แปลงเป็นฐาน 2 ก่อน: 4 = 2^2, 8 = 2^3, 16 = 2^4",
            "หาเลขหลักหน่วยของ a^n: ลองคูณดูเลขหลักหน่วย 1-4 ตัวแรก จะพบวัฏจักรซ้ำทุก ๆ 4 ตัว (หรือ 2 ตัว)",
            "หาจำนวนเลข 0 ลงท้ายของผลคูณ: นับจำนวนคู่ของ 2 × 5 (ดูเลขชี้กำลังที่น้อยกว่าระหว่าง 2 กับ 5)",
        ],
        "example": {
            "q": "ถ้า 2^x = 8^4 แล้ว x มีค่าเท่าใด",
            "steps": [
                "เปลี่ยนฐาน 8 ให้เป็นฐาน 2: เนื่องจาก 8 = 2^3",
                "จะได้ 8^4 = (2^3)^4 = 2^(3×4) = 2^12",
                "ดังนั้น x = 12",
            ],
            "a": "12",
        },
        "mistakes": [
            "เข้าใจผิดว่า a^n = a × n เช่น คิดว่า 2^5 = 10 แทนที่จะเป็น 32",
            "เปลี่ยน 8^4 เป็น 2^(3+4) = 2^7 แทนที่จะนำเลขชี้กำลังมาคูณกันเป็น 2^12",
        ],
        "tips": [
            "จำค่ากำลังสองและกำลังสามที่ใช้บ่อย: 2^5=32, 2^6=64, 2^10=1,024, 3^4=81, 5^3=125, 11^2=121, 12^2=144, 13^2=169, 15^2=225",
        ],
    },
    weight=1.5,
)


@template("m.num.exp", "easy")
def _squares_and_cubes_eval():
    a = random.randint(4, 15)
    b = random.randint(2, 5)
    c = random.randint(2, 9)
    # Evaluate a^2 + b^3 - c^2
    val = (a ** 2) + (b ** 3) - (c ** 2)
    if val <= 0:
        return None
    wrong_mult = (2 * a) + (3 * b) - (2 * c)
    return mcq(
        stem=f"จงหาค่าของ **{a}² + {b}³ − {c}²**",
        correct=num(val),
        wrongs=[
            W(num(wrong_mult), "นำฐานไปคูณกับเลขชี้กำลัง (เช่น a×2) แทนที่จะคูณตัวเองซ้ำ", "concept"),
            W(num((a ** 2) + (b ** 2) - (c ** 2)), f"คำนวณ {b}³ เป็น {b}² = {b ** 2} แทนที่จะเป็น {b ** 3}", "calc"),
            W(num((a ** 2) + (b ** 3) + (c ** 2)), f"นำ {c}² มาบวกแทนที่จะลบออก", "sign"),
        ],
        hint=f"{a}² = {a}×{a} และ {b}³ = {b}×{b}×{b} คำนวณแต่ละพจน์ก่อนแล้วนำมาบวกลบกัน",
        steps=[
            f"หาค่าแต่ละพจน์: {a}² = {a ** 2}, {b}³ = {b ** 3} และ {c}² = {c ** 2}",
            f"แทนค่า: {a ** 2} + {b ** 3} − {c ** 2} = {num(val)}",
        ],
    )


@template("m.num.exp", "medium")
def _exponent_same_base_equation():
    base = random.choice([2, 3])
    if base == 2:
        p1, m1 = pick([(4, 2), (8, 3), (16, 4)])
        p2, m2 = pick([(4, 2), (8, 3), (16, 4)])
    else:
        p1, m1 = pick([(9, 2), (27, 3)])
        p2, m2 = pick([(9, 2), (27, 3)])
    e1 = random.randint(2, 6)
    e2 = random.randint(2, 5)
    ans = m1 * e1 + m2 * e2
    wrong_add_exp = (m1 + e1) + (m2 + e2)
    wrong_no_convert = e1 + e2
    return mcq(
        stem=f"ถ้า **{p1}^{e1} × {p2}^{e2} = {base}^n** แล้ว **n** มีค่าเท่าใด",
        correct=str(ans),
        wrongs=[
            W(str(wrong_no_convert), f"นำเลขชี้กำลัง {e1} + {e2} มาบวกกันเลยโดยยังไม่ได้แปลงฐานเป็นฐาน {base}", "concept"),
            W(str(wrong_add_exp if wrong_add_exp != ans else ans + 2),
              "ตอนแปลงฐานนำเลขชี้กำลังมาบวกกันแทนที่จะคูณกัน", "formula"),
            W(str((m1 * e1) * (m2 * e2)), "นำเลขชี้กำลังของสองพจน์มาคูณกันแทนที่จะบวกกันเมื่อคูณเลขยกกำลังฐานเดียวกัน", "formula"),
        ],
        hint=f"แปลง {p1} และ {p2} ให้อยู่ในรูปเลขยกกำลังฐาน {base} ก่อน แล้วใช้สมบัติ (a^m) × (a^n) = a^(m+n)",
        steps=[
            f"เนื่องจาก {p1} = {base}^{m1} จะได้ {p1}^{e1} = ({base}^{m1})^{e1} = {base}^{m1 * e1}",
            f"และ {p2} = {base}^{m2} จะได้ {p2}^{e2} = ({base}^{m2})^{e2} = {base}^{m2 * e2}",
            f"ดังนั้น {base}^{m1 * e1} × {base}^{m2 * e2} = {base}^({m1 * e1} + {m2 * e2}) = {base}^{ans} นั่นคือ n = {ans}",
        ],
    )


@template("m.num.exp", "hard")
def _last_digit_or_trailing_zeros():
    mode = random.choice(["last_digit", "zeros"])
    if mode == "last_digit":
        base, cycle = pick([
            (2, [2, 4, 8, 6]),
            (3, [3, 9, 7, 1]),
            (7, [7, 9, 3, 1]),
            (8, [8, 4, 2, 6]),
        ])
        exp = random.randint(25, 199)
        rem = exp % 4
        ans = cycle[rem - 1]  # rem=1->0, 2->1, 3->2, 0->3
        wrong1 = cycle[rem % 4]
        wrong2 = cycle[(rem - 2) % 4]
        wrong3 = cycle[(rem + 1) % 4]
        return mcq(
            stem=f"เลขโดดใน **หลักหน่วย** ของ **{base}^{exp}** คือเลขใด",
            correct=str(ans),
            wrongs=[
                W(str(wrong1), "นับลำดับเศษจากการหารด้วย 4 คลาดเคลื่อนไป 1 ตำแหน่ง", "calc"),
                W(str(wrong2), "ถ้าหารด้วย 4 ลงตัว ต้องใช้ตัวที่ 4 ของรอบ ไม่ใช่ตัวที่ 1", "concept"),
                W(str(wrong3), f"หารเลขชี้กำลังด้วย {base} แทนที่จะหารด้วยขนาดรอบวัฏจักรคือ 4", "concept"),
            ],
            hint=f"สังเกตหลักหน่วยของ {base}^1, {base}^2, {base}^3, {base}^4 จะซ้ำกันทุก ๆ 4 ตัว จึงนำเลขชี้กำลังหารด้วย 4 ดูเศษ",
            steps=[
                f"หลักหน่วยของ {base}^n จะวนซ้ำทุก ๆ 4 ตัวตามลำดับคือ {', '.join(str(x) for x in cycle)}",
                f"นำเลขชี้กำลัง {exp} หารด้วย 4 ได้เศษ {rem if rem != 0 else '0 (ตรงกับลำดับที่ 4)'}",
                f"ดังนั้นหลักหน่วยของ {base}^{exp} คือ {ans}",
            ],
        )
    else:
        # Number of digits or trailing zeros of 2^a * 5^b
        b = random.randint(8, 22)
        diff = random.choice([2, 3, 4])
        a = b + diff
        # 2^a * 5^b = (2^diff) * 10^b -> value is (2^diff) followed by b zeros
        head = str(2 ** diff)
        ask = random.choice(["zeros", "digits"])
        if ask == "zeros":
            return mcq(
                stem=f"ผลลัพธ์ของ **2^{a} × 5^{b}** เมื่อเขียนในรูปจำนวนเต็มจะมี **เลข 0 ลงท้าย** ทั้งหมดกี่ตัว",
                correct=f"{b} ตัว",
                wrongs=[
                    W(f"{a} ตัว", "เลือกเลขชี้กำลังที่มากกว่า แต่การจับคู่ 2 × 5 = 10 ต้องดูตัวที่น้อยกว่า", "concept"),
                    W(f"{a + b} ตัว", "นำเลขชี้กำลังของ 2 และ 5 มาบวกกัน", "formula"),
                    W(f"{b + len(head)} ตัว", "สับสนระหว่างจำนวนเลข 0 ลงท้าย กับจำนวนหลักทั้งหมดของผลลัพธ์", "misread"),
                ],
                hint="เลข 0 ลงท้าย 1 ตัว เกิดจาก 2 × 5 = 10 หนึ่งคู่ ให้ดูว่าจับคู่ได้ทั้งหมดกี่คู่",
                steps=[
                    f"จัดรูปการคูณ: 2^{a} × 5^{b} = 2^{diff} × (2^{b} × 5^{b}) = {2 ** diff} × 10^{b}",
                    f"เนื่องจาก {2 ** diff} ไม่มีเลข 0 ลงท้าย ดังนั้นผลลัพธ์จะมีเลข 0 ลงท้ายทั้งหมด {b} ตัว",
                ],
            )
        else:
            total_digits = len(head) + b
            return mcq(
                stem=f"ผลลัพธ์ของ **2^{a} × 5^{b}** เป็นจำนวนเต็มที่มีทั้งหมด **กี่หลัก**",
                correct=f"{total_digits} หลัก",
                wrongs=[
                    W(f"{b} หลัก", f"นับเฉพาะจำนวนเลข 0 ลงท้าย ({b} ตัว) ลืมนับเลขข้างหน้าคือ {head}", "partial"),
                    W(f"{a} หลัก", "ตอบตามเลขชี้กำลังของ 2 โดยไม่ได้จัดรูปเป็นฐาน 10", "concept"),
                    W(f"{total_digits + 1} หลัก", f"คิดว่า 10^{b} มี {b + 1} หลักแล้วบวกซ้ำกับหลักของ {head}", "calc"),
                ],
                hint="จัดรูปให้อยู่ในรูป k × 10^n แล้วดูจำนวนหลักของ k บวกกับจำนวนเลขศูนย์ n ตัว",
                steps=[
                    f"จัดรูป: 2^{a} × 5^{b} = 2^{diff} × (2^{b} × 5^{b}) = {head} × 10^{b}",
                    f"ตัวเลข {head} มี {len(head)} หลัก และตามด้วยเลข 0 อีก {b} ตัว",
                    f"ดังนั้นมีจำนวนหลักทั้งหมด = {len(head)} + {b} = {total_digits} หลัก",
                ],
            )


@template("m.num.exp", "challenge")
def _two_digit_swap_puzzle():
    # Classic top-school number theory puzzle:
    # A two-digit number has sum of digits S. When its digits are reversed, the new number differs by 9*k.
    x = random.randint(1, 7)
    y = random.randint(x + 1, 9)
    orig = 10 * x + y
    rev = 10 * y + x
    s = x + y
    diff = rev - orig  # 9 * (y - x)
    variant = random.choice(["find_orig", "find_rev", "find_prod"])
    if variant == "find_orig":
        w_other_pair = 10 * (x - 1) + (y + 1) if x > 1 and y < 9 else 10 * (x + 1) + (y - 1)
        if w_other_pair in (orig, rev):
            w_other_pair = orig + 11
        w_no_div9 = orig + 10 if orig + 10 not in (orig, rev, w_other_pair) else orig - 10
        return mcq(
            stem=(
                f"จำนวนนับสองหลักจำนวนหนึ่งมีผลบวกของเลขโดดทั้งสองหลักเท่ากับ **{s}** "
                f"ถ้าสลับที่เลขโดดหลักสิบกับหลักหน่วย จะได้จำนวนใหม่ที่ **มากกว่า** จำนวนเดิมอยู่ **{diff}** "
                f"จำนวนเดิมคือจำนวนใด"
            ),
            correct=str(orig),
            wrongs=[
                W(str(rev), f"{rev} คือจำนวนใหม่หลังสลับหลัก โจทย์ถามจำนวนเดิมซึ่งต้องน้อยกว่า", "misread"),
                W(str(w_other_pair), f"ผลบวกเลขโดดเท่ากับ {s} จริง แต่เมื่อสลับหลักแล้วผลต่างไม่ใช่ {diff}", "calc"),
                W(str(w_no_div9), "แก้สมการหาหลักสิบและหลักหน่วยคลาดเคลื่อนไป 1", "calc"),
            ],
            hint="เมื่อสลับหลักของจำนวนสองหลัก ผลต่างของจำนวนใหม่กับจำนวนเดิมจะเท่ากับ 9 × (ผลต่างของเลขโดดสองหลัก) เสมอ",
            steps=[
                "ให้จำนวนเดิมมีหลักสิบเป็น a และหลักหน่วยเป็น b (จำนวนใหม่มากกว่าเดิม แปลว่า b > a)",
                f"ผลต่างเมื่อสลับหลัก = (10b + a) − (10a + b) = 9(b − a) = {diff} จะได้ b − a = {diff // 9}",
                f"จาก b + a = {s} และ b − a = {diff // 9} แก้หาค่าได้ a = {x} และ b = {y}",
                f"ดังนั้นจำนวนเดิมคือ {orig}",
            ],
        )
    elif variant == "find_rev":
        w_other_pair = 10 * (y + 1) + (x - 1) if x > 1 and y < 9 else 10 * (y - 1) + (x + 1)
        if w_other_pair in (orig, rev):
            w_other_pair = rev - 11
        w_off = rev - 10 if rev - 10 not in (orig, rev, w_other_pair) else rev + 10
        return mcq(
            stem=(
                f"จำนวนนับสองหลักจำนวนหนึ่งมีผลบวกของเลขโดดทั้งสองหลักเท่ากับ **{s}** "
                f"เมื่อสลับที่เลขโดดหลักสิบกับหลักหน่วย จะได้จำนวนใหม่ที่ **น้อยกว่า** จำนวนเดิมอยู่ **{diff}** "
                f"จำนวนเดิมคือจำนวนใด"
            ),
            correct=str(rev),
            wrongs=[
                W(str(orig), f"{orig} คือจำนวนใหม่หลังสลับหลัก โจทย์บอกว่าจำนวนเดิมต้องมากกว่าจำนวนใหม่", "misread"),
                W(str(w_other_pair), f"ผลบวกเลขโดดได้ {s} จริง แต่ผลต่างเมื่อสลับหลักไม่เท่ากับ {diff}", "calc"),
                W(str(w_off), "หาค่าเลขโดดหลักสิบคลาดเคลื่อนไป 1", "calc"),
            ],
            hint="จำนวนใหม่น้อยกว่าจำนวนเดิม แสดงว่าหลักสิบของจำนวนเดิมมากกว่าหลักหน่วย และผลต่างเท่ากับ 9 × (หลักสิบ − หลักหน่วย)",
            steps=[
                "ให้จำนวนเดิมมีหลักสิบเป็น a และหลักหน่วยเป็น b (จำนวนใหม่น้อยกว่าเดิม แปลว่า a > b)",
                f"ผลต่างเมื่อสลับหลัก = 9(a − b) = {diff} จะได้ a − b = {diff // 9}",
                f"จาก a + b = {s} และ a − b = {diff // 9} จะได้ a = {y} และ b = {x}",
                f"ดังนั้นจำนวนเดิมคือ {rev}",
            ],
        )
    else:
        prod = x * y
        w1 = (x - 1) * (y + 1) if x > 1 else (x + 1) * (y - 1)
        if w1 == prod or w1 <= 0:
            w1 = prod + 4
        w2 = s * (y - x)
        if w2 in (prod, w1):
            w2 = prod + 6
        w3 = prod + 2 if prod + 2 not in (w1, w2) else prod + 8
        return mcq(
            stem=(
                f"จำนวนนับสองหลักจำนวนหนึ่งมีผลบวกของเลขโดดทั้งสองหลักเท่ากับ **{s}** "
                f"ถ้าสลับที่เลขโดดทั้งสองหลักจะได้จำนวนที่ต่างจากเดิมอยู่ **{diff}** "
                f"ผลคูณของเลขโดดทั้งสองหลักของจำนวนนี้มีค่าเท่าใด"
            ),
            correct=str(prod),
            wrongs=[
                W(str(w1), f"เลือกคู่เลขโดดที่บวกกันได้ {s} แต่ผลต่างไม่ใช่ {diff // 9}", "calc"),
                W(str(w2), f"นำผลบวกเลขโดด ({s}) ไปคูณกับผลต่างเลขโดด ({y - x}) แทนที่จะหาเลขโดดแต่ละตัวก่อน", "concept"),
                W(str(w3), "คำนวณผลคูณของเลขโดดคลาดเคลื่อน", "calc"),
            ],
            hint=f"ผลต่างเมื่อสลับหลักคือ {diff} ดังนั้นผลต่างของเลขโดดสองหลักเท่ากับ {diff} ÷ 9 = {diff // 9}",
            steps=[
                f"ผลต่างของเลขโดดทั้งสองหลัก = {diff} ÷ 9 = {diff // 9}",
                f"ผลบวกของเลขโดดเท่ากับ {s} และผลต่างเท่ากับ {diff // 9} จึงได้เลขโดดสองตัวคือ {x} และ {y}",
                f"ผลคูณของเลขโดดทั้งสองหลัก = {x} × {y} = {prod}",
            ],
        )
