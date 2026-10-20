"""Fraction and decimal question templates for topic ``m.frac`` (เศษส่วนและทศนิยม).

Covers equivalent/simplifying fractions (with fraction bar/grid figures),
comparing & ordering fractions/decimals, adding & subtracting fractions/mixed
numbers, multiplying & dividing fractions (incl. complex fractions & cancelling
products), decimal operations, repeating decimals & cyclic digit patterns,
fraction of a quantity (with visual models), multi-step "of the remainder"
word problems, and top-school telescoping fraction series.
"""

from fractions import Fraction
import math
import random

from backend.bank import svg
from backend.bank.core import W, dec, frac, mcq, name_th, num, pick, skill, template


# ===========================================================================
# Skill 1: m.frac.equiv — เศษส่วนที่เท่ากัน เศษส่วนอย่างต่ำ และจำนวนคละ
# ===========================================================================

skill(
    "m.frac.equiv",
    "m.frac",
    "เศษส่วนที่เท่ากัน เศษส่วนอย่างต่ำ และจำนวนคละ",
    lesson={
        "concept": (
            "เศษส่วนที่มีค่าเท่ากันเกิดจากการนำจำนวนนับตัวเดียวกันมาคูณหรือหารทั้งตัวเศษและตัวส่วน "
            "เศษส่วนอย่างต่ำคือเศษส่วนที่ ห.ร.ม. ของตัวเศษและตัวส่วนเป็น 1 ส่วนจำนวนคละเขียนในรูปเศษเกินได้โดย (จำนวนเต็ม × ตัวส่วน + ตัวเศษ) / ตัวส่วน"
        ),
        "steps": [
            "ทำเป็นเศษส่วนอย่างต่ำ: หา ห.ร.ม. ของตัวเศษและตัวส่วน แล้วนำมาหารทั้งบนและล่าง",
            "เปลี่ยนจำนวนคละ a b/c เป็นเศษเกิน: ตัวเศษใหม่ = (a × c) + b โดยตัวส่วนคงเดิมคือ c",
            "หาค่าตัวไม่ทราบค่าในเศษส่วนที่เท่ากัน: ย่อเป็นเศษส่วนอย่างต่ำก่อน แล้วดูว่าตัวเศษหรือตัวส่วนคูณเพิ่มกี่เท่า",
        ],
        "example": {
            "q": "ถ้า [[12/18]] = [[x/27]] = [[20/y]] แล้ว x + y มีค่าเท่าใด",
            "steps": [
                "ทอน [[12/18]] เป็นเศษส่วนอย่างต่ำโดยหารด้วย 6 ทั้งเศษและส่วน ได้ [[2/3]]",
                "จาก [[2/3]] = [[x/27]] ตัวส่วนคูณ 9 ดังนั้น x = 2 × 9 = 18",
                "จาก [[2/3]] = [[20/y]] ตัวเศษคูณ 10 ดังนั้น y = 3 × 10 = 30 รวม x + y = 48",
            ],
            "a": "48",
        },
        "mistakes": [
            "นำจำนวนเดียวกันไปบวกทั้งเศษและส่วน แล้วเข้าใจผิดว่าเศษส่วนยังมีค่าเท่าเดิม",
            "เปลี่ยนจำนวนคละเป็นเศษเกินโดยนำ จำนวนเต็ม + ตัวเศษ แทนที่จะคูณตัวส่วนก่อน",
        ],
        "tips": [
            "เวลาเจอสมการเศษส่วนเท่ากันที่เลขไม่ลงตัว ให้ทอนตัวที่รู้ค่าเป็นเศษส่วนอย่างต่ำก่อนเสมอ!",
        ],
    },
    weight=1.1,
)


@template("m.frac.equiv", "easy")
def _fraction_bar_simplify_fig():
    # Show a fraction bar with k*p shaded out of k*q parts, ask for simplified fraction or unshaded fraction
    base_pairs = [(1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 6), (5, 6)]
    p, q = pick(base_pairs)
    k = random.choice([2, 3, 4])
    total_parts = q * k
    if total_parts > 18:
        k = 2
        total_parts = q * k
    shaded = p * k
    fig = svg.fraction_bar(total_parts, shaded, width=320, height=38)
    ask = random.choice(["shaded", "unshaded"])
    if ask == "shaded":
        ans_f = Fraction(p, q)
        other_f = Fraction(q - p, q)
        raw_str = f"[[{shaded}/{total_parts}]]"
        return mcq(
            stem="จากรูปแถบเศษส่วน ส่วนที่แรเงาคิดเป็น **เศษส่วนอย่างต่ำ** เท่าใดของรูปทั้งหมด",
            figure=fig,
            correct=frac(ans_f),
            wrongs=[
                W(frac(other_f), "นี่คือเศษส่วนของส่วนที่ไม่แรเงา โจทย์ถามส่วนที่แรเงา", "misread"),
                W(f"[[{shaded}/{total_parts - shaded}]]", "ใช้จำนวนช่องที่ไม่แรเงาเป็นตัวส่วน แทนที่จะใช้จำนวนช่องทั้งหมด", "concept"),
                W(f"[[{p}/{q + 1}]]", "นับจำนวนช่องทั้งหมดหรือทอนเป็นเศษส่วนอย่างต่ำคลาดเคลื่อน", "calc"),
            ],
            hint="นับจำนวนช่องที่แรเงาเป็นตัวเศษ และจำนวนช่องทั้งหมดเป็นตัวส่วน แล้วหารด้วย ห.ร.ม.",
            steps=[
                f"มีช่องที่แรเงา {shaded} ช่อง จากทั้งหมด {total_parts} ช่อง เขียนเป็น {raw_str}",
                f"ทอนเป็นเศษส่วนอย่างต่ำโดยหารด้วย {k} ทั้งเศษและส่วน ได้ {frac(ans_f)}",
            ],
        )
    else:
        ans_f = Fraction(q - p, q)
        shaded_f = Fraction(p, q)
        unshaded = total_parts - shaded
        return mcq(
            stem="จากรูปแถบเศษส่วน ส่วนที่ **ไม่แรเงา** คิดเป็น **เศษส่วนอย่างต่ำ** เท่าใดของรูปทั้งหมด",
            figure=fig,
            correct=frac(ans_f),
            wrongs=[
                W(frac(shaded_f), "นี่คือเศษส่วนของส่วนที่แรเงา โจทย์ถามส่วนที่ไม่แรเงา", "misread"),
                W(f"[[{unshaded}/{shaded}]]", "นำส่วนที่ไม่แรเงาเทียบกับส่วนที่แรเงา แทนที่จะเทียบกับช่องทั้งหมด", "concept"),
                W(f"[[{q - p}/{q + 1}]]", "ทอนเศษส่วนเป็นเศษส่วนอย่างต่ำคลาดเคลื่อน", "calc"),
            ],
            hint="นับช่องสีขาว (ไม่แรเงา) ส่วนด้วยช่องทั้งหมด แล้วทอนเป็นเศษส่วนอย่างต่ำ",
            steps=[
                f"ช่องที่ไม่แรเงามี {total_parts} − {shaded} = {unshaded} ช่อง จากทั้งหมด {total_parts} ช่อง",
                f"เขียนเป็นเศษส่วน [[{unshaded}/{total_parts}]] ทอนอย่างต่ำโดยหารด้วย {k} ได้ {frac(ans_f)}",
            ],
        )


@template("m.frac.equiv", "medium")
def _equivalent_fraction_chain():
    coprimes = [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (3, 7), (4, 7), (5, 6), (5, 8), (7, 9)]
    p, q = pick(coprimes)
    m1, m2, m3 = random.sample(range(2, 12), 3)
    a, b = p * m1, q * m1
    x = p * m2
    b2 = q * m2
    a3 = p * m3
    y = q * m3
    ans = x + y
    w_swap = q * m2 + p * m3
    if w_swap == ans:
        w_swap = ans + p + q
    w_diff = abs(y - x)
    if w_diff in (ans, w_swap) or w_diff == 0:
        w_diff = ans - p
    w_unreduced = p * m1 * m2 + q * m3
    if w_unreduced in (ans, w_swap, w_diff):
        w_unreduced = ans + m2 + m3
    return mcq(
        stem=f"ถ้า **[[{a}/{b}]] = [[x/{b2}]] = [[{a3}/y]]** แล้วค่าของ **x + y** เท่ากับเท่าใด",
        correct=num(ans),
        wrongs=[
            W(num(w_swap), "สลับคูณตัวเศษกับตัวส่วนตอนเทียบเศษส่วนที่เท่ากัน", "formula"),
            W(num(w_diff), "นำค่า x และ y มาลบกันแทนที่จะบวกกัน", "misread"),
            W(num(w_unreduced), f"ลืมทอน {a}/{b} เป็นเศษส่วนอย่างต่ำก่อนเทียบหาค่า x", "concept"),
        ],
        hint=f"ทอน [[{a}/{b}]] เป็นเศษส่วนอย่างต่ำก่อน จะได้ [[{p}/{q}]] แล้วเทียบหาค่า x และ y",
        steps=[
            f"ทอน [[{a}/{b}]] เป็นเศษส่วนอย่างต่ำ โดยหารด้วย {m1} ได้ [[{p}/{q}]]",
            f"จาก [[{p}/{q}]] = [[x/{b2}]] ตัวส่วนคูณด้วย {m2} ดังนั้น x = {p} × {m2} = {x}",
            f"จาก [[{p}/{q}]] = [[{a3}/y]] ตัวเศษคูณด้วย {m3} ดังนั้น y = {q} × {m3} = {y}",
            f"ดังนั้น x + y = {x} + {y} = {num(ans)}",
        ],
    )


@template("m.frac.equiv", "hard")
def _fraction_sum_num_den_puzzle():
    # A fraction is equivalent to p/q, and the sum (or difference) of its numerator and denominator is S.
    coprimes = [(3, 5), (3, 7), (4, 7), (4, 9), (5, 8), (5, 9), (7, 11), (5, 12)]
    p, q = pick(coprimes)
    k = random.randint(4, 15)
    num_val, den_val = p * k, q * k
    s = num_val + den_val
    diff = den_val - num_val
    return mcq(
        stem=(
            f"เศษส่วนจำนวนหนึ่งเมื่อทอนเป็นเศษส่วนอย่างต่ำแล้วได้ **[[{p}/{q}]]** "
            f"ถ้าผลบวกของตัวเศษและตัวส่วนของเศษส่วนเดิมเท่ากับ **{s}** "
            f"แล้วตัวส่วนมากกว่าตัวเศษของเศษส่วนเดิมอยู่เท่าใด"
        ),
        correct=num(diff),
        wrongs=[
            W(num(q - p), f"ตอบผลต่างของเศษส่วนอย่างต่ำ ({q} − {p} = {q - p}) โดยลืมคูณด้วย {k}", "partial"),
            W(num(num_val), f"{num_val} คือค่าของตัวเศษเดิม ไม่ใช่ผลต่างระหว่างตัวส่วนกับตัวเศษ", "misread"),
            W(num(den_val), f"{den_val} คือค่าของตัวส่วนเดิม ไม่ใช่ผลต่างระหว่างตัวส่วนกับตัวเศษ", "misread"),
        ],
        hint=f"ให้เศษส่วนเดิมคือ [[{p}k/{q}k]] ดังนั้น {p}k + {q}k = {s} แก้หาค่า k ก่อน",
        steps=[
            f"ให้เศษส่วนเดิมมีตัวเศษ = {p}k และตัวส่วน = {q}k",
            f"ผลบวกของตัวเศษและตัวส่วน = {p}k + {q}k = {p + q}k = {s} จะได้ k = {s} ÷ {p + q} = {k}",
            f"ตัวส่วนมากกว่าตัวเศษอยู่ = ({q} − {p}) × {k} = {q - p} × {k} = {num(diff)}",
        ],
    )


# ===========================================================================
# Skill 2: m.frac.compare — การเปรียบเทียบและเรียงลำดับเศษส่วนและทศนิยม
# ===========================================================================

skill(
    "m.frac.compare",
    "m.frac",
    "การเปรียบเทียบและเรียงลำดับเศษส่วนและทศนิยม",
    lesson={
        "concept": (
            "การเปรียบเทียบเศษส่วนทำได้หลายวิธี: 1) ทำตัวส่วนให้เท่ากัน 2) คูณไขว้ 3) เทียบกับค่ากลางเช่น [[1/2]] หรือ 1 "
            "โดยเฉพาะเศษส่วนแท้ที่ (ตัวส่วน − ตัวเศษ) เท่ากันทุกตัว ตัวที่มีเลขมากกว่าจะมีค่าใกล้ 1 มากกว่า (มีค่ามากกว่า)"
        ),
        "steps": [
            "ถ้าตัวส่วนหา ค.ร.น. ง่าย ให้ทำตัวส่วนให้เท่ากันแล้วเปรียบเทียบตัวเศษ",
            "ถ้าเป็นเศษส่วนแท้ที่ผลต่าง (ส่วน − เศษ = d) เท่ากัน เช่น [[7/9]], [[11/13]]: เขียนเป็น 1 − [[d/ส่วน]] ตัวส่วนยิ่งมาก ส่วนที่ลบออกยิ่งน้อย ค่าจึงยิ่งมาก",
            "ถ้ามีทั้งเศษส่วนและทศนิยม ให้แปลงเป็นทศนิยม (หรือเศษส่วน) รูปเดียวกันก่อนเรียงลำดับ",
        ],
        "example": {
            "q": "ข้อใดมีค่ามากที่สุด ระหว่าง [[5/7]], [[9/11]], [[13/15]], [[17/19]]",
            "steps": [
                "สังเกตว่าทุกตัวเป็นเศษส่วนแท้ที่ ตัวส่วนมากกว่าตัวเศษอยู่ 2 เท่ากัน",
                "เขียนในรูป 1 − [[2/7]], 1 − [[2/11]], 1 − [[2/15]], 1 − [[2/19]]",
                "เนื่องจาก [[2/19]] มีค่าน้อยที่สุด เมื่อลบออกจาก 1 จึงเหลือมากที่สุด ตอบ [[17/19]]",
            ],
            "a": "[[17/19]]",
        },
        "mistakes": [
            "เห็นตัวส่วนมากขึ้นแล้วคิดว่าเศษส่วนมีค่าน้อยลงเสมอ โดยลืมดูว่าตัวเศษก็เพิ่มขึ้นด้วย",
            "เรียงลำดับจากมากไปน้อย แต่เผลอตอบจากน้อยไปมาก",
        ],
        "tips": [
            "จำสั้น ๆ: เศษส่วนแท้ (เศษ < ส่วน) ถ้าผลต่างเศษกับส่วนเท่ากัน → 'เลขยิ่งมาก ค่ายิ่งมาก'!",
        ],
    },
    weight=1.3,
)


@template("m.frac.compare", "easy")
def _order_fractions_lcm():
    lcm_d = random.choice([12, 20, 24, 30, 36])
    divs = [d for d in range(2, lcm_d + 1) if lcm_d % d == 0 and d <= 18]
    chosen_ds = random.sample(divs, 4)
    fracs = []
    seen_vals = set()
    for d in chosen_ds:
        candidates = [n for n in range(1, d) if Fraction(n, d) not in seen_vals]
        if not candidates:
            return None
        n = random.choice(candidates)
        f = Fraction(n, d)
        seen_vals.add(f)
        fracs.append((n, d, f))
    ask = random.choice(["max", "min"])
    fracs_sorted = sorted(fracs, key=lambda x: x[2])
    if ask == "max":
        best = fracs_sorted[-1]
        worst = fracs_sorted[0]
        second = fracs_sorted[-2]
        third = fracs_sorted[1]
        q_word = "มากที่สุด"
    else:
        best = fracs_sorted[0]
        worst = fracs_sorted[-1]
        second = fracs_sorted[1]
        third = fracs_sorted[-2]
        q_word = "น้อยที่สุด"
    items_str = ",  ".join(f"[[{n}/{d}]]" for n, d, _ in fracs)
    conv_str = ", ".join(f"[[{n}/{d}]] = [[{n * (lcm_d // d)}/{lcm_d}]]" for n, d, _ in fracs)
    return mcq(
        stem=f"จากเศษส่วน **{items_str}** เศษส่วนในข้อใดมีค่า **{q_word}**",
        correct=f"[[{best[0]}/{best[1]}]]",
        wrongs=[
            W(f"[[{worst[0]}/{worst[1]}]]", f"นี่คือเศษส่วนที่มีค่า{'น้อยที่สุด' if ask == 'max' else 'มากที่สุด'} ตรงกันข้ามกับที่โจทย์ถาม", "misread"),
            W(f"[[{second[0]}/{second[1]}]]", "เปรียบเทียบเฉพาะตัวเศษหรือตัวส่วนโดยยังไม่ได้ทำตัวส่วนให้เท่ากัน", "concept"),
            W(f"[[{third[0]}/{third[1]}]]", "คูณขยายตัวเศษคลาดเคลื่อนตอนทำตัวส่วนให้เท่ากัน", "calc"),
        ],
        hint=f"ทำตัวส่วนของทุกจำนวนให้เท่ากับ ค.ร.น. คือ {lcm_d} แล้วเปรียบเทียบตัวเศษ",
        steps=[
            f"ทำตัวส่วนให้เท่ากับ {lcm_d}: {conv_str}",
            f"ดังนั้นเศษส่วนที่มีค่า{q_word}คือ [[{best[0]}/{best[1]}]]",
        ],
    )


@template("m.frac.compare", "medium")
def _compare_complement_to_one():
    diff = random.choice([1, 2, 3, 4])
    dens = sorted(random.sample(range(diff + 3, diff + 25), 4))
    nums = [d - diff for d in dens]
    ask = random.choice(["max", "min"])
    items = [f"[[{n}/{d}]]" for n, d in zip(nums, dens)]
    shuffled_items = items[:]
    random.shuffle(shuffled_items)
    if ask == "max":
        ans = items[-1]
        opp = items[0]
        w1, w2 = items[1], items[2]
        q_word = "มากที่สุด"
        explain = f"เมื่อลบออกจาก 1 ตัวลบ [[{diff}/{dens[-1]}]] มีค่าน้อยที่สุด จึงทำให้ {ans} มีค่ามากที่สุด"
    else:
        ans = items[0]
        opp = items[-1]
        w1, w2 = items[1], items[2]
        q_word = "น้อยที่สุด"
        explain = f"เมื่อลบออกจาก 1 ตัวลบ [[{diff}/{dens[0]}]] มีค่ามากที่สุด จึงทำให้ {ans} มีค่าน้อยที่สุด"
    return mcq(
        stem=f"ในบรรดาเศษส่วน **{',  '.join(shuffled_items)}** ข้อใดมีค่า **{q_word}**",
        correct=ans,
        wrongs=[
            W(opp, f"เข้าใจสลับกันว่าตัวส่วนมากแล้วค่าจะน้อยลง แต่กรณีผลต่างเท่ากัน เศษส่วนแท้ที่เลขมากกว่าจะมีค่าเข้าใกล้ 1 มากกว่า", "trap"),
            W(w1, "เปรียบเทียบโดยยังไม่ได้เขียนในรูป 1 ลบด้วยเศษส่วนที่เหลือ", "concept"),
            W(w2, "เลือกค่ากลางแทนค่าปลายสุด", "calc"),
        ],
        hint=f"สังเกตว่าทุกจำนวนมีตัวส่วนมากกว่าตัวเศษอยู่ {diff} เท่ากัน จึงเขียนในรูป 1 − [[{diff}/ตัวส่วน]] ได้",
        steps=[
            f"ทุกจำนวนขาดอีก [[{diff}/ตัวส่วน]] จะครบ 1",
            explain,
        ],
    )


@template("m.frac.compare", "hard")
def _fractions_between_bounds():
    # How many integers x satisfy a/b < x/d < c/e (or sum of such integers x)
    b, e = pick([(3, 4), (3, 5), (4, 5), (2, 3), (5, 6), (2, 5)])
    m = random.choice([1, 2])
    d = b * e * m
    f_lo = Fraction(1, b)
    f_hi = Fraction(e - 1, e)
    lo_num = int(f_lo * d)
    hi_num = int(f_hi * d)
    valid_x = list(range(lo_num + 1, hi_num))
    if len(valid_x) < 2:
        return None
    ask = random.choice(["count", "sum"])
    if ask == "count":
        ans = len(valid_x)
        return mcq(
            stem=(
                f"มีจำนวนเต็ม **x** ทั้งหมดกี่จำนวนที่ทำให้ "
                f"**{frac(f_lo)} < [[x/{d}]] < {frac(f_hi)}**"
            ),
            correct=f"{ans} จำนวน",
            wrongs=[
                W(f"{ans + 2} จำนวน", f"เผลอนับขอบ {lo_num} และ {hi_num} รวมเข้าไปด้วย ทั้งที่เครื่องหมายเป็น < ไม่ใช่ ≤", "trap"),
                W(f"{ans + 1} จำนวน", f"นำ {hi_num} − {lo_num} เลยโดยลืมลบ 1 สำหรับจำนวนที่อยู่ระหว่างกลางแท้ ๆ", "concept"),
                W(f"{max(1, ans - 1)} จำนวน", "คูณขยายตัวเศษตอนทำส่วนให้เท่ากันคลาดเคลื่อนไป 1", "calc"),
            ],
            hint=f"ทำตัวส่วนของ {frac(f_lo)} และ {frac(f_hi)} ให้เป็น {d} เท่ากัน แล้วดูว่า x เป็นจำนวนเต็มใดได้บ้าง",
            steps=[
                f"ทำตัวส่วนให้เป็น {d}: {frac(f_lo)} = [[{lo_num}/{d}]] และ {frac(f_hi)} = [[{hi_num}/{d}]]",
                f"อสมการกลายเป็น {lo_num} < x < {hi_num} ดังนั้น x ได้แก่ {', '.join(str(v) for v in valid_x)}",
                f"มีทั้งหมด {ans} จำนวน",
            ],
        )
    else:
        ans = sum(valid_x)
        return mcq(
            stem=(
                f"จงหา **ผลบวกของจำนวนเต็ม x ทั้งหมด** ที่สอดคล้องกับอสมการ "
                f"**{frac(f_lo)} < [[x/{d}]] < {frac(f_hi)}**"
            ),
            correct=num(ans),
            wrongs=[
                W(num(ans + lo_num + hi_num), f"เผลอบวกค่าขอบ {lo_num} และ {hi_num} เข้าไปด้วย", "trap"),
                W(num(len(valid_x)), "ตอบเป็นจำนวนตัวของค่า x แทนผลบวกของค่า x", "misread"),
                W(num(ans - valid_x[0]), f"ลืมบวกค่า x ตัวแรกคือ {valid_x[0]}", "partial"),
            ],
            hint=f"ทำตัวส่วนของทุกพจน์ให้เป็น {d} ก่อน แล้วหาค่าจำนวนเต็ม x ที่อยู่ระหว่างตัวเศษทั้งสอง",
            steps=[
                f"แปลงตัวส่วนเป็น {d}: [[{lo_num}/{d}]] < [[x/{d}]] < [[{hi_num}/{d}]]",
                f"จำนวนเต็ม x ที่เป็นไปได้คือ {', '.join(str(v) for v in valid_x)}",
                f"ผลบวก = {' + '.join(str(v) for v in valid_x)} = {num(ans)}",
            ],
        )


# ===========================================================================
# Skill 3: m.frac.addsub — การบวกและการลบเศษส่วนและจำนวนคละ
# ===========================================================================

skill(
    "m.frac.addsub",
    "m.frac",
    "การบวกและการลบเศษส่วนและจำนวนคละ",
    lesson={
        "concept": (
            "การบวกและลบเศษส่วนต้องทำตัวส่วนให้เท่ากันก่อนเสมอ (โดยใช้ ค.ร.น. ของตัวส่วน) "
            "แล้วจึงนำตัวเศษมาบวกลบกัน ส่วนตัวส่วนคงเดิม"
        ),
        "steps": [
            "หา ค.ร.น. ของตัวส่วนทุกตัว แล้วคูณขยายทั้งเศษและส่วนให้มีตัวส่วนเท่ากับ ค.ร.น.",
            "สำหรับจำนวนคละ สามารถแยกส่วนจำนวนเต็มบวกลบกัน และส่วนเศษส่วนบวกลบกันได้ (ถ้าตัวเศษตัวตั้งน้อยกว่าตัวลบ ให้ยืมจำนวนเต็มมา 1 ซึ่งเท่ากับ ตัวส่วน/ตัวส่วน)",
            "ตรวจสอบคำตอบสุดท้ายให้เป็นเศษส่วนอย่างต่ำหรือจำนวนคละ",
        ],
        "example": {
            "q": "จงหาค่าของ [[3 1/4]] − [[1 2/3]]",
            "steps": [
                "ทำส่วนให้เป็น 12: [[3 3/12]] − [[1 8/12]]",
                "เนื่องจาก 3 < 8 จึงกระจายจำนวนเต็ม 3 มา 1 กลายเป็น [[2 15/12]] − [[1 8/12]]",
                "= [[1 7/12]]",
            ],
            "a": "[[1 7/12]]",
        },
        "mistakes": [
            "นำตัวเศษบวกตัวเศษ และตัวส่วนบวกตัวส่วนโดยตรง เช่น [[1/2]] + [[1/3]] = [[2/5]]",
            "ตอนลบจำนวนคละที่ตัวเศษตัวตั้งน้อยกว่าตัวลบ เผลอสลับเอาตัวมากตั้งลบตัวน้อยโดยไม่ยืมจำนวนเต็ม",
        ],
        "tips": [
            "การบวกลบจำนวนคละที่เลขจำนวนเต็มเยอะ ๆ ห้ามแปลงเป็นเศษเกินเพราะเลขจะใหญ่มาก ให้แยกคิดส่วนจำนวนเต็มกับเศษส่วน!",
        ],
    },
    weight=1.3,
)


@template("m.frac.addsub", "easy")
def _add_sub_unlike_fractions():
    pairs = [(3, 4), (2, 5), (3, 5), (4, 5), (3, 7), (4, 6), (6, 8), (4, 10), (6, 9)]
    b, d = pick(pairs)
    a = random.randint(1, b - 1)
    c = random.randint(1, d - 1)
    op_choice = random.choice(["+", "-"])
    f1, f2 = Fraction(a, b), Fraction(c, d)
    if f1 == f2:
        f1 = Fraction(b - 1, b)
        f2 = Fraction(1, d)
        a, c = f1.numerator, f2.numerator
    if op_choice == "-" and f1 < f2:
        f1, f2 = f2, f1
        a, b, c, d = f1.numerator, f1.denominator, f2.numerator, f2.denominator
    ans = f1 + f2 if op_choice == "+" else f1 - f2
    lcm_bd = math.lcm(b, d)
    naive_num = a + c if op_choice == "+" else max(1, abs(a - c))
    naive_den = b + d if op_choice == "+" else max(2, abs(b - d))
    naive_f = Fraction(naive_num, naive_den)
    if naive_f == ans:
        naive_f = ans + Fraction(1, lcm_bd)
    wrong_no_scale = Fraction(max(1, a + c if op_choice == "+" else abs(a - c)), lcm_bd)
    if wrong_no_scale in (ans, naive_f):
        wrong_no_scale = ans + Fraction(2, lcm_bd)
    wrong_op = f1 - f2 if op_choice == "+" and f1 > f2 else f1 + f2
    if wrong_op in (ans, naive_f, wrong_no_scale) or wrong_op <= 0:
        wrong_op = ans + Fraction(3, lcm_bd)
    return mcq(
        stem=f"จงหาผลลัพธ์ของ **[[{a}/{b}]] {op_choice} [[{c}/{d}]]** ในรูปเศษส่วนอย่างต่ำหรือจำนวนคละ",
        correct=frac(ans, mixed=True),
        wrongs=[
            W(frac(naive_f, mixed=True), "นำตัวเศษกระทำกันและตัวส่วนกระทำกันโดยตรง ซึ่งผิดหลักการบวกลบเศษส่วน", "concept"),
            W(frac(wrong_no_scale, mixed=True), f"เปลี่ยนตัวส่วนเป็น {lcm_bd} แล้วแต่ลืมคูณขยายตัวเศษให้สอดคล้องกัน", "partial"),
            W(frac(wrong_op, mixed=True), "ใช้เครื่องหมายบวก/ลบสลับกับที่โจทย์กำหนดหรือคำนวณตัวเศษผิด", "sign"),
        ],
        hint=f"หา ค.ร.น. ของ {b} และ {d} คือ {lcm_bd} แล้วทำตัวส่วนให้เท่ากันก่อน",
        steps=[
            f"ค.ร.น. ของ {b} และ {d} คือ {lcm_bd}",
            f"แปลงตัวส่วน: [[{a}/{b}]] = [[{a * (lcm_bd // b)}/{lcm_bd}]] และ [[{c}/{d}]] = [[{c * (lcm_bd // d)}/{lcm_bd}]]",
            f"คำนวณได้ = {frac(ans, mixed=True)}",
        ],
    )


@template("m.frac.addsub", "medium")
def _mixed_number_borrow_sub():
    w1 = random.randint(4, 9)
    w2 = random.randint(1, w1 - 2)
    b, d = pick([(3, 4), (4, 5), (3, 5), (4, 6), (6, 8), (5, 6)])
    # Ensure fractional part of first is SMALLER than fractional part of second so borrowing is needed!
    f1_part = Fraction(1, b)
    f2_part = Fraction(d - 1, d)
    if f1_part >= f2_part:
        return None
    val1 = w1 + f1_part
    val2 = w2 + f2_part
    ans = val1 - val2
    # Common mistake: subtracting whole numbers (w1 - w2) and subtracting fractions backwards (f2_part - f1_part)
    wrong_no_borrow = (w1 - w2) + (f2_part - f1_part)
    wrong_borrow_10 = (w1 - 1 - w2) + Fraction(10 + f1_part.numerator * (math.lcm(b, d) // b) - f2_part.numerator * (math.lcm(b, d) // d), math.lcm(b, d))
    lcm_bd = math.lcm(b, d)
    n1 = f1_part.numerator * (lcm_bd // b)
    n2 = f2_part.numerator * (lcm_bd // d)
    return mcq(
        stem=f"จงหาค่าของ **{frac(val1, mixed=True)} − {frac(val2, mixed=True)}**",
        correct=frac(ans, mixed=True),
        wrongs=[
            W(frac(wrong_no_borrow, mixed=True),
              f"นำจำนวนเต็ม {w1}−{w2} = {w1 - w2} แล้วสลับเอาเศษส่วน {n2}/{lcm_bd} − {n1}/{lcm_bd} โดยไม่ยืมจำนวนเต็ม", "trap"),
            W(frac(ans + 1, mixed=True), "กระจายจำนวนเต็มมาบวกตัวเศษแล้ว แต่ลืมลดค่าจำนวนเต็มลง 1", "calc"),
            W(frac(wrong_borrow_10, mixed=True), f"เวลากระจายจำนวนเต็ม 1 มาเป็นเศษส่วน เผลอบวกตัวเศษด้วย 10 แทนที่จะบวกด้วยตัวส่วน ({lcm_bd})", "concept"),
        ],
        hint=f"ทำส่วนให้เท่ากันเป็น {lcm_bd} จะเห็นว่าตัวเศษหน้า ({n1}) น้อยกว่าตัวเศษหลัง ({n2}) ต้องกระจายจำนวนเต็ม {w1} มา 1 (คือ [[{lcm_bd}/{lcm_bd}]])",
        steps=[
            f"ทำตัวส่วนให้เท่ากับ {lcm_bd}: [[{w1} {n1}/{lcm_bd}]] − [[{w2} {n2}/{lcm_bd}]]",
            f"กระจายจำนวนเต็ม {w1} มา 1 ได้ [[{w1 - 1} {n1 + lcm_bd}/{lcm_bd}]] − [[{w2} {n2}/{lcm_bd}]]",
            f"ลบส่วนจำนวนเต็มและเศษส่วน ได้ = {frac(ans, mixed=True)}",
        ],
    )


@template("m.frac.addsub", "hard")
def _solve_missing_fraction_mixed():
    # Find X in: A - (X - B) = C  or  (A - X) + B = C
    den = random.choice([12, 15, 18, 20, 24])
    f_a = Fraction(random.randint(2 * den + 1, 4 * den - 1), den)
    f_b = Fraction(random.randint(den + 1, 2 * den - 1), den)
    f_x = Fraction(random.randint(den + 2, 3 * den - 1), den)
    if f_a.denominator == 1 or f_b.denominator == 1 or f_x.denominator == 1:
        return None
    # Equation: f_a - X + f_b = f_c
    f_c = f_a - f_x + f_b
    if f_c <= 0 or f_c.denominator == 1:
        return None
    wrong_sign1 = f_a + f_c - f_b
    wrong_sign2 = abs(f_a - f_b - f_c)
    return mcq(
        stem=(
            f"ถ้า **{frac(f_a, mixed=True)} − A + {frac(f_b, mixed=True)} = {frac(f_c, mixed=True)}** "
            f"แล้ว **A** มีค่าเท่าใด"
        ),
        correct=frac(f_x, mixed=True),
        wrongs=[
            W(frac(wrong_sign1, mixed=True), "ย้ายข้างสมการผิด โดยนำค่าฝั่งขวามาบวกแทนที่จะนำมาลบ", "sign"),
            W(frac(wrong_sign2, mixed=True), "นำพจน์ที่สามไปลบออกจากพจน์แรกแทนที่จะบวกกันก่อน", "sign"),
            W(frac(f_x + Fraction(1, den), mixed=True), "คำนวณตัวเศษเมื่อทำตัวส่วนให้เท่ากันคลาดเคลื่อนไป 1", "calc"),
        ],
        hint=f"จัดรูปสมการให้ A อยู่ฝั่งเดียว: A = {frac(f_a, mixed=True)} + {frac(f_b, mixed=True)} − {frac(f_c, mixed=True)}",
        steps=[
            f"จากสมการ จะได้ A = {frac(f_a, mixed=True)} + {frac(f_b, mixed=True)} − {frac(f_c, mixed=True)}",
            f"ทำตัวส่วนให้เท่ากันแล้วคำนวณ ได้ A = {frac(f_x, mixed=True)}",
        ],
    )


# ===========================================================================
# Skill 4: m.frac.muldiv — การคูณและการหารเศษส่วนและเศษส่วนซ้อน
# ===========================================================================

skill(
    "m.frac.muldiv",
    "m.frac",
    "การคูณ การหารเศษส่วน และเศษส่วนซ้อน",
    lesson={
        "concept": (
            "การคูณเศษส่วนให้นำเศษคูณเศษและส่วนคูณส่วน (ตัดทอนก่อนคูณจะคิดง่ายขึ้น) "
            "การหารเศษส่วนให้เปลี่ยนเครื่องหมาย ÷ เป็น × แล้วกลับเศษเป็นส่วนของตัวหาร ส่วนเศษส่วนซ้อนให้คิดไล่จากชั้นล่างสุดขึ้นบน"
        ),
        "steps": [
            "ถ้ามีจำนวนคละในการคูณหรือหาร ต้องแปลงเป็นเศษเกินทุกตัวก่อนเสมอ!",
            "เปลี่ยน ÷ เป็น × กับส่วนกลับของตัวหาร แล้วตัดทอนตัวเศษกับตัวส่วนเป็นคู่ ๆ",
            "สำหรับเศษส่วนซ้อน (มีเศษส่วนอยู่ในตัวส่วน) ให้บวกลบชั้นล่างสุดให้เป็นเศษส่วนเดี่ยวก่อน แล้วใช้หลัก 'ตัวตั้ง ÷ ตัวหาร = ตัวตั้ง × ส่วนกลับ'",
        ],
        "example": {
            "q": "จงหาค่าของ 1 + 1 / (1 + [[1/3]])",
            "steps": [
                "คิดชั้นล่างสุดก่อน: 1 + [[1/3]] = [[4/3]]",
                "กลับเศษเป็นส่วนของ 1 ÷ [[4/3]] ได้ [[3/4]]",
                "บวกกับ 1 ข้างหน้า: 1 + [[3/4]] = [[1 3/4]]",
            ],
            "a": "[[1 3/4]]",
        },
        "mistakes": [
            "คูณจำนวนคละโดยเอาจำนวนเต็มคูณจำนวนเต็ม และเศษส่วนคูณเศษส่วน ซึ่งผิด! ต้องทำเป็นเศษเกินก่อน",
            "ตอนหารเศษส่วน เผลอกลับเศษเป็นส่วนของ 'ตัวตั้ง' แทนที่จะกลับเฉพาะ 'ตัวหาร'",
        ],
        "tips": [
            "โจทย์ผลคูณเรียงกัน เช่น (1 + [[1/2]])(1 + [[1/3]])...(1 + [[1/n]]) ให้แปลงแต่ละวงเล็บเป็นเศษเกิน จะตัดทอนแนวทแยงได้หมด!",
        ],
    },
    weight=1.6,
)


@template("m.frac.muldiv", "easy")
def _mul_div_mixed_numbers():
    w1 = random.randint(1, 4)
    w2 = random.randint(1, 3)
    d1, d2 = pick([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (3, 6), (4, 6)])
    r1 = Fraction(random.randint(1, d1 - 1), d1)
    r2 = Fraction(random.randint(1, d2 - 1), d2)
    f1 = w1 + r1
    f2 = w2 + r2
    op = random.choice(["×", "÷"])
    ans = f1 * f2 if op == "×" else f1 / f2
    # Mistake 1: multiplying/dividing whole parts and fraction parts separately
    wrong_sep = (w1 * w2 + r1 * r2) if op == "×" else Fraction(w1, w2) + (r1 / r2)
    # Mistake 2: forgetting to invert divisor or inverting when multiplying
    wrong_inv = f1 / f2 if op == "×" else f1 * f2
    # Mistake 3: inverting dividend instead of divisor
    wrong_inv_first = (1 / f1) * f2 if op == "÷" else ans + Fraction(1, f1.denominator)
    return mcq(
        stem=f"จงหาผลลัพธ์ของ **{frac(f1, mixed=True)} {op} {frac(f2, mixed=True)}**",
        correct=frac(ans, mixed=True),
        wrongs=[
            W(frac(wrong_sep, mixed=True), "นำจำนวนเต็มกระทำกันและเศษส่วนกระทำกันแยกส่วน ต้องแปลงจำนวนคละเป็นเศษเกินก่อนเสมอ", "concept"),
            W(frac(wrong_inv, mixed=True),
              "ไม่ได้กลับเศษเป็นส่วนของตัวหาร" if op == "÷" else "เผลอกลับเศษเป็นส่วนเหมือนการหาร", "formula"),
            W(frac(wrong_inv_first, mixed=True), "กลับเศษเป็นส่วนของตัวตั้งหรือคูณตัวเศษผิดพลาด", "calc"),
        ],
        hint="แปลงจำนวนคละทั้งสองจำนวนให้เป็นเศษเกินก่อน แล้วจึงคูณหรือหาร",
        steps=[
            f"แปลงจำนวนคละเป็นเศษเกิน: {frac(f1, mixed=True)} = {frac(f1)} และ {frac(f2, mixed=True)} = {frac(f2)}",
            f"คำนวณ {frac(f1)} {op} {frac(f2)} = {frac(ans, mixed=True)}",
        ],
    )


@template("m.frac.muldiv", "medium")
def _cancelling_product_chain():
    # Classic telescoping product: (1 + 1/a)(1 + 1/(a+1))...(1 + 1/b) or (1 - 1/a)(1 - 1/(a+1))...(1 - 1/b)
    a = random.randint(2, 6)
    b = random.randint(a + 4, a + 15)
    mode = random.choice(["plus", "minus"])
    if mode == "plus":
        # (a+1)/a * (a+2)/(a+1) * ... * (b+1)/b = (b+1)/a
        ans = Fraction(b + 1, a)
        wrong_no_plus1 = Fraction(b, a)
        wrong_inv = Fraction(a, b + 1)
        wrong_first_last = Fraction(a + 1, b)
        stem = (
            f"จงหาค่าของ **(1 + [[1/{a}]]) × (1 + [[1/{a + 1}]]) × (1 + [[1/{a + 2}]]) × ... × (1 + [[1/{b}]])**"
        )
        steps = [
            f"แปลงแต่ละวงเล็บเป็นเศษเกิน: [[{a + 1}/{a}]] × [[{a + 2}/{a + 1}]] × [[{a + 3}/{a + 2}]] × ... × [[{b + 1}/{b}]]",
            f"ตัวเศษและตัวส่วนตัดทอนกันแนวทแยง เหลือตัวเศษตัวสุดท้ายคือ {b + 1} และตัวส่วนตัวยืนต้นคือ {a}",
            f"ดังนั้นผลลัพธ์ = [[{b + 1}/{a}]] = {frac(ans, mixed=True)}",
        ]
    else:
        # (a-1)/a * a/(a+1) * ... * (b-1)/b = (a-1)/b
        ans = Fraction(a - 1, b)
        wrong_no_plus1 = Fraction(a, b)
        wrong_inv = Fraction(b, a - 1)
        wrong_first_last = Fraction(1, b) if a > 2 else Fraction(2, b)
        stem = (
            f"จงหาค่าของ **(1 − [[1/{a}]]) × (1 − [[1/{a + 1}]]) × (1 − [[1/{a + 2}]]) × ... × (1 − [[1/{b}]])**"
        )
        steps = [
            f"คำนวณในแต่ละวงเล็บ: [[{a - 1}/{a}]] × [[{a}/{a + 1}]] × [[{a + 1}/{a + 2}]] × ... × [[{b - 1}/{b}]]",
            f"ตัดทอนตัวเศษกับตัวส่วนที่เหมือนกัน เหลือตัวเศษตัวแรกคือ {a - 1} และตัวส่วนตัวสุดท้ายคือ {b}",
            f"ดังนั้นผลลัพธ์ = {frac(ans, mixed=True)}",
        ]
    return mcq(
        stem=stem,
        correct=frac(ans, mixed=True),
        wrongs=[
            W(frac(wrong_no_plus1, mixed=True), "ตัดทอนพจน์หัวหรือพจน์ท้ายผิดตำแหน่ง", "calc"),
            W(frac(wrong_inv, mixed=True), "สลับตัวเศษที่เหลือกับตัวส่วนที่เหลือ", "concept"),
            W(frac(wrong_first_last, mixed=True), "ลืมบวกหรือลบ 1 ในวงเล็บสุดท้ายก่อนตัดทอน", "partial"),
        ],
        hint="ทำในแต่ละวงเล็บให้เป็นเศษส่วนเดี่ยวก่อน แล้วสังเกตการตัดทอนแนวทแยงระหว่างวงเล็บติดกัน",
        steps=steps,
    )


@template("m.frac.muldiv", "hard")
def _continued_fraction_eval():
    # Evaluate a + 1 / (b + 1 / c) or a + 1 / (b - 1 / c)
    a = random.randint(1, 3)
    b = random.randint(1, 4)
    c = random.randint(2, 6)
    inner = b + Fraction(1, c)
    recip = Fraction(1, 1) / inner
    ans = a + recip
    wrong_no_recip = a + inner
    wrong_partial = recip
    wrong_add_wrong = a + Fraction(1, b) + Fraction(1, c)
    return mcq(
        stem=(
            f"จงหาค่าของ **{a} + [[1/{b} + [[1/{c}]]]]** "
            f"(หมายถึง {a} บวกด้วย 1 ส่วนด้วย ({b} + [[1/{c}]]))"
        ),
        correct=frac(ans, mixed=True),
        wrongs=[
            W(frac(wrong_partial, mixed=True), f"คำนวณเฉพาะส่วน 1 ÷ ({b} + 1/{c}) แล้วลืมบวก {a} ข้างหน้า", "partial"),
            W(frac(wrong_no_recip, mixed=True), f"หาค่า {b} + 1/{c} แล้วนำมาบวก {a} เลยโดยลืมกลับเศษเป็นส่วน", "concept"),
            W(frac(wrong_add_wrong, mixed=True), f"กระจายตัวส่วนเป็น 1/{b} + 1/{c} ซึ่งทำไม่ได้", "concept"),
        ],
        hint=f"เริ่มคิดจากชั้นล่างสุดก่อน คือหาค่า {b} + [[1/{c}]] เป็นเศษเกิน แล้วกลับเศษเป็นส่วนก่อนนำไปบวกกับ {a}",
        steps=[
            f"ขั้นที่ 1 คิดตัวส่วนชั้นล่างสุด: {b} + [[1/{c}]] = {frac(inner)}",
            f"ขั้นที่ 2 หาค่า 1 ÷ {frac(inner)} = {frac(recip)}",
            f"ขั้นที่ 3 นำไปบวกกับ {a}: {a} + {frac(recip)} = {frac(ans, mixed=True)}",
        ],
    )


# ===========================================================================
# Skill 5: m.frac.dec_ops — การบวก ลบ คูณ หาร ทศนิยมระคน
# ===========================================================================

skill(
    "m.frac.dec_ops",
    "m.frac",
    "การบวก ลบ คูณ หาร ทศนิยมระคน",
    lesson={
        "concept": (
            "การบวกลบทศนิยมต้องตั้งจุดทศนิยมให้ตรงกัน การคูณทศนิยมจำนวนตำแหน่งทศนิยมของผลลัพธ์จะเท่ากับผลรวมตำแหน่งทศนิยมของตัวตั้งและตัวคูณ "
            "ส่วนการหารทศนิยมต้องเลื่อนจุดตัวหารให้เป็นจำนวนเต็มก่อน โดยเลื่อนจุดตัวตั้งไปทางขวาเท่ากัน"
        ),
        "steps": [
            "การบวก/ลบ: เติม 0 ท้ายทศนิยมให้มีจำนวนตำแหน่งเท่ากันแล้วตั้งจุดให้ตรงกัน",
            "การคูณ: คูณเหมือนจำนวนเต็มก่อน แล้วนับตำแหน่งทศนิยมรวม (เช่น 2 ตำแหน่ง × 1 ตำแหน่ง = 3 ตำแหน่ง)",
            "การหาร: เลื่อนจุดทศนิยมของตัวหารและตัวตั้งไปทางขวาจำนวนตำแหน่งเท่ากัน จนตัวหารเป็นจำนวนเต็ม",
        ],
        "example": {
            "q": "จงหาค่าของ 3.6 ÷ 0.09 + 1.2 × 0.5",
            "steps": [
                "คิดส่วนหาร: 3.6 ÷ 0.09 เลื่อนจุด 2 ตำแหน่ง เป็น 360 ÷ 9 = 40",
                "คิดส่วนคูณ: 1.2 × 0.5 = 0.60 = 0.6",
                "นำมาบวกกัน: 40 + 0.6 = 40.6",
            ],
            "a": "40.6",
        },
        "mistakes": [
            "เลื่อนจุดทศนิยมตอนหาร เช่น 3.6 ÷ 0.09 เผลอคิดเป็น 36 ÷ 9 = 4 แทนที่จะเป็น 360 ÷ 9 = 40",
            "คูณทศนิยม 1 ตำแหน่งกับ 1 ตำแหน่ง แล้วใส่จุดทศนิยมแค่ 1 ตำแหน่ง (เช่น 0.4 × 0.3 = 1.2 แทนที่จะเป็น 0.12)",
        ],
        "tips": [
            "การหารด้วย 0.1, 0.01, 0.001 มีค่าเท่ากับการคูณด้วย 10, 100, 1,000 ตามลำดับ (ผลลัพธ์จะมากขึ้น!)",
        ],
    },
    weight=1.2,
)


@template("m.frac.dec_ops", "easy")
def _decimal_mult_place_trap():
    a = random.choice([2, 3, 4, 6, 7, 8, 9, 11, 12, 13])
    b = random.choice([3, 4, 6, 7, 8, 9])
    if (a * b) % 10 == 0:
        b = 7
    # Compute 0.a * 0.0b or (a/10) * (b/10)
    prod = a * b
    ans_val = Fraction(prod, 1000)  # e.g. 0.a * 0.0b (1 place * 2 places = 3 places)
    da = dec(Fraction(a, 10), 2)
    db = dec(Fraction(b, 100), 3)
    ans = dec(ans_val, 4)
    w_2places = dec(Fraction(prod, 100), 3)
    w_4places = dec(Fraction(prod, 10000), 4)
    w_add = dec(Fraction(a, 10) + Fraction(b, 100), 3)
    return mcq(
        stem=f"ผลคูณของ **{da} × {db}** มีค่าเท่าใด",
        correct=ans,
        wrongs=[
            W(w_2places, "ใส่ทศนิยมเพียง 2 ตำแหน่ง ลืมรวมตำแหน่งทศนิยมของตัวตั้ง (1 ตำแหน่ง) กับตัวคูณ (2 ตำแหน่ง) เป็น 3 ตำแหน่ง", "unit"),
            W(w_4places, "นับตำแหน่งทศนิยมของผลคูณเกินไป 1 ตำแหน่ง", "unit"),
            W(w_add, "นำทศนิยมทั้งสองมาบวกกันแทนที่จะคูณกัน", "misread"),
        ],
        hint="คูณตัวเลขเหมือนจำนวนเต็มก่อน แล้วนับจำนวนตำแหน่งทศนิยมรวมกัน (1 ตำแหน่ง + 2 ตำแหน่ง = 3 ตำแหน่ง)",
        steps=[
            f"นำตัวเลขมาคูณกัน: {a} × {b} = {prod}",
            f"{da} เป็นทศนิยม 1 ตำแหน่ง และ {db} เป็นทศนิยม 2 ตำแหน่ง รวมเป็น 1 + 2 = 3 ตำแหน่ง",
            f"ดังนั้นผลลัพธ์คือ {ans}",
        ],
    )


@template("m.frac.dec_ops", "medium")
def _decimal_div_and_mul_mixed():
    divisor_int = random.choice([4, 6, 7, 8, 9, 12, 15])
    q_int = random.choice([20, 30, 40, 50, 60, 70, 80])
    # dividend / divisor = q_int, where divisor = divisor_int / 100, dividend = (divisor_int * q_int) / 100
    dividend = Fraction(divisor_int * q_int, 100)
    divisor = Fraction(divisor_int, 100)
    m1 = Fraction(random.choice([12, 14, 15, 16, 18, 24, 25]), 10)
    m2 = Fraction(random.choice([2, 3, 4, 5, 6]), 10)
    prod_part = m1 * m2
    ans = Fraction(q_int) + prod_part
    wrong_shift = Fraction(q_int, 10) + prod_part
    wrong_prod_shift = Fraction(q_int) + prod_part * 10
    wrong_sub = Fraction(q_int) - prod_part
    return mcq(
        stem=f"จงหาค่าของ **{dec(dividend, 2)} ÷ {dec(divisor, 2)} + {dec(m1, 2)} × {dec(m2, 2)}**",
        correct=dec(ans, 3),
        wrongs=[
            W(dec(wrong_shift, 3), f"เลื่อนจุดทศนิยมตอนหาร {dec(dividend, 2)} ÷ {dec(divisor, 2)} พลาดไป 1 ตำแหน่ง จึงได้ {q_int // 10} แทนที่จะเป็น {q_int}", "unit"),
            W(dec(wrong_prod_shift, 3), f"นับตำแหน่งทศนิยมของ {dec(m1, 2)} × {dec(m2, 2)} เป็น 1 ตำแหน่ง แทนที่จะเป็น 2 ตำแหน่ง", "unit"),
            W(dec(wrong_sub, 3), "นำผลหารกับผลคูณมาลบกันแทนที่จะบวกกัน", "sign"),
        ],
        hint=f"เลื่อนจุดทศนิยมของ {dec(dividend, 2)} ÷ {dec(divisor, 2)} ไปทางขวา 2 ตำแหน่งทั้งคู่ก่อนหาร",
        steps=[
            f"ส่วนหาร: {dec(dividend, 2)} ÷ {dec(divisor, 2)} = {divisor_int * q_int} ÷ {divisor_int} = {q_int}",
            f"ส่วนคูณ: {dec(m1, 2)} × {dec(m2, 2)} = {dec(prod_part, 3)}",
            f"รวมกันได้: {q_int} + {dec(prod_part, 3)} = {dec(ans, 3)}",
        ],
    )


@template("m.frac.dec_ops", "hard")
def _decimal_scaling_given_product():
    # Given A * B = P (integers), find (A/10^x * B/10^y) / (C/10^z) or similar
    a = random.randint(23, 89)
    b = random.randint(14, 67)
    if (a * b) % 10 == 0:
        b += 1
    p = a * b
    # Ask for (a/10) * (b/100) + (p/10) ÷ (a/100)
    # Wait: (p/10) ÷ (a/100) = (p/a) * 10 = 10*b! Super neat!
    a_dec1 = dec(Fraction(a, 10), 2)
    b_dec2 = dec(Fraction(b, 100), 3)
    p_dec1 = dec(Fraction(p, 10), 2)
    a_dec2 = dec(Fraction(a, 100), 3)
    part1 = Fraction(p, 1000)
    part2 = Fraction(b * 10, 1)
    ans = part1 + part2
    w1 = part1 + Fraction(b, 1)
    w2 = Fraction(p, 100) + part2
    w3 = part1 + Fraction(b, 10)
    return mcq(
        stem=(
            f"กำหนดให้ **{a} × {b} = {num(p)}** "
            f"จงหาค่าของ **({a_dec1} × {b_dec2}) + ({p_dec1} ÷ {a_dec2})**"
        ),
        correct=dec(ans, 3),
        wrongs=[
            W(dec(w1, 3), f"คำนวณ {p_dec1} ÷ {a_dec2} ได้ {b} แทนที่จะเป็น {b * 10} เพราะเลื่อนจุดทศนิยมไม่ครบ", "unit"),
            W(dec(w2, 3), f"คำนวณ {a_dec1} × {b_dec2} เป็นทศนิยม 2 ตำแหน่ง แทนที่จะเป็น 3 ตำแหน่ง", "unit"),
            W(dec(w3, 3), f"เลื่อนจุดทศนิยมของตัวตั้งและตัวหารไปคนละทิศทาง", "concept"),
        ],
        hint=f"ใช้ความสัมพันธ์ {a} × {b} = {num(p)} และ {num(p)} ÷ {a} = {b} แล้วนับตำแหน่งทศนิยมของแต่ละวงเล็บ",
        steps=[
            f"วงเล็บแรก: {a_dec1} × {b_dec2} มีทศนิยม 1 + 2 = 3 ตำแหน่ง จึงได้ = {dec(part1, 3)}",
            f"วงเล็บหลัง: {p_dec1} ÷ {a_dec2} เลื่อนจุด 2 ตำแหน่ง เป็น {p}0 ÷ {a} = {b * 10}",
            f"บวกกันได้: {dec(part1, 3)} + {b * 10} = {dec(ans, 3)}",
        ],
    )


# ===========================================================================
# Skill 6: m.frac.dec_rep — การแปลงเศษส่วนเป็นทศนิยมและทศนิยมซ้ำ
# ===========================================================================

skill(
    "m.frac.dec_rep",
    "m.frac",
    "เศษส่วนกับทศนิยมและแบบรูปทศนิยมซ้ำ",
    lesson={
        "concept": (
            "เศษส่วนที่ตัวส่วนแยกตัวประกอบแล้วมีเฉพาะ 2 กับ 5 จะเขียนเป็นทศนิยมซ้ำศูนย์ (ทศนิยมรู้จบ) ได้เสมอ "
            "ส่วนตัวส่วนอื่น ๆ จะเกิดทศนิยมซ้ำเป็นชุด (คาบ) ซึ่งสามารถหาเลขโดดในตำแหน่งที่ต้องการได้จากการหารเอาเศษด้วยความยาวชุดที่ซ้ำ"
        ),
        "steps": [
            "แปลงเป็นทศนิยมรู้จบ: คูณทั้งเศษและส่วนให้ตัวส่วนเป็น 10, 100 หรือ 1,000 (จำคู่คูณ: 2×5=10, 4×25=100, 8×125=1,000)",
            "แปลงทศนิยมซ้ำเป็นเศษส่วน: ทศนิยมซ้ำตั้งแต่ตำแหน่งแรก ใส่ตัวส่วนเป็นเลข 9 ตามจำนวนตำแหน่งที่ซ้ำ เช่น 0.777... = [[7/9]]",
            "หาทศนิยมตำแหน่งที่ N ของเศษส่วน: หาชุดตัวเลขที่ซ้ำ (ความยาว k ตัว) แล้วนำ N หารด้วย k ดูเศษเหลือ",
        ],
        "example": {
            "q": "เมื่อเขียน [[2/7]] ในรูปทศนิยม จะได้ 0.285714285714... เลขโดดหลังจุดทศนิยมตำแหน่งที่ 50 คือเลขใด",
            "steps": [
                "ชุดตัวเลขหลังจุดทศนิยมซ้ำทีละ 6 ตัว คือ 2, 8, 5, 7, 1, 4",
                "นำ 50 หารด้วย 6 ได้ 8 เศษ 2",
                "เศษ 2 ตรงกับตัวที่ 2 ของชุด คือเลข 8",
            ],
            "a": "8",
        },
        "mistakes": [
            "ลืมคู่คูณ 8 × 125 = 1,000 เลยตั้งหารยาวจนเสียเวลาหรือคิดเลขผิด",
            "เวลานับตำแหน่งทศนิยมที่หารลงตัว (เศษ 0) เผลอตอบตัวที่ 1 แทนที่จะตอบตัวสุดท้ายของชุดซ้ำ",
        ],
        "tips": [
            "จำให้ขึ้นใจ: [[1/8]] = 0.125, [[3/8]] = 0.375, [[5/8]] = 0.625, [[7/8]] = 0.875 และ [[1/9]] = 0.111..., [[1/99]] = 0.0101...",
        ],
    },
    weight=1.3,
)


@template("m.frac.dec_rep", "easy")
def _frac_to_terminating_dec():
    den, mult, target_pow = pick([
        (8, 125, 1000),
        (25, 4, 100),
        (40, 25, 1000),
        (125, 8, 1000),
        (20, 5, 100),
        (50, 2, 100),
    ])
    whole = random.randint(0, 5)
    num_part = random.choice([x for x in range(1, den) if math.gcd(x, den) == 1])
    f = whole + Fraction(num_part, den)
    ans = dec(f, 3)
    wrong_no_scale = f"{whole}.{num_part}"
    wrong_shift = dec(whole + Fraction(num_part * mult, target_pow * 10), 4)
    wrong_calc = dec(f + Fraction(1, target_pow), 3)
    return mcq(
        stem=f"เมื่อเขียน **{frac(f, mixed=True)}** ในรูปทศนิยม จะตรงกับข้อใด",
        correct=ans,
        wrongs=[
            W(wrong_no_scale, f"นำตัวเศษ {num_part} มาเขียนหลังจุดทศนิยมเลยโดยยังไม่ได้ทำตัวส่วนให้เป็น {num(target_pow)}", "concept"),
            W(wrong_shift, "วางตำแหน่งจุดทศนิยมคลาดเคลื่อนไป 1 ตำแหน่ง", "unit"),
            W(wrong_calc, f"คูณขยายตัวเศษด้วย {mult} คลาดเคลื่อนไป 1", "calc"),
        ],
        hint=f"คูณทั้งตัวเศษและตัวส่วนของ [[{num_part}/{den}]] ด้วย {mult} เพื่อให้ตัวส่วนเป็น {num(target_pow)}",
        steps=[
            f"ทำตัวส่วนให้เป็น {num(target_pow)}: [[{num_part}/{den}]] = [[{num_part} × {mult}/{den} × {mult}]] = [[{num_part * mult}/{num(target_pow)}]]",
            f"รวมกับจำนวนเต็มข้างหน้า ได้ทศนิยม = {ans}",
        ],
    )


@template("m.frac.dec_rep", "medium")
def _repeating_dec_to_frac():
    # Sum of two repeating decimals 0.a... + 0.bc... or converting 0.ab(rep) to simplified fraction
    a = random.randint(1, 8)
    b = random.randint(10, 89)
    if b % 11 == 0:
        b += 1
    f1 = Fraction(a, 9)
    f2 = Fraction(b, 99)
    ans = f1 + f2
    wrong_10_100 = Fraction(a, 10) + Fraction(b, 100)
    wrong_99_both = Fraction(a + b, 99)
    b_str = f"{b:02d}"
    return mcq(
        stem=(
            f"จงหาผลบวกของทศนิยมซ้ำ **0.{a}{a}{a}... + 0.{b_str}{b_str}{b_str}...** "
            f"ในรูปเศษส่วนอย่างต่ำหรือจำนวนคละ"
        ),
        correct=frac(ans, mixed=True),
        wrongs=[
            W(frac(wrong_10_100, mixed=True), "แปลงเป็นส่วน 10 และส่วน 100 เหมือนทศนิยมรู้จบ แทนที่จะใช้ส่วน 9 และ 99", "concept"),
            W(frac(wrong_99_both, mixed=True), f"เปลี่ยนตัวส่วนของ 0.{a}{a}{a}... เป็น 99 แต่ลืมคูณตัวเศษด้วย 11", "partial"),
            W(frac(ans + Fraction(1, 99), mixed=True), "บวกตัวเศษหรือทอนเป็นเศษส่วนอย่างต่ำคลาดเคลื่อน", "calc"),
        ],
        hint=f"0.{a}{a}{a}... = [[{a}/9]] และ 0.{b_str}{b_str}{b_str}... = [[{b}/99]] ทำส่วนให้เป็น 99 เท่ากันแล้วบวกกัน",
        steps=[
            f"แปลงทศนิยมซ้ำเป็นเศษส่วน: 0.{a}{a}{a}... = [[{a}/9]] = [[{a * 11}/99]]",
            f"และ 0.{b_str}{b_str}{b_str}... = [[{b}/99]]",
            f"นำมาบวกกัน: [[{a * 11}/99]] + [[{b}/99]] = [[{a * 11 + b}/99]] = {frac(ans, mixed=True)}",
        ],
    )


@template("m.frac.dec_rep", "challenge")
def _cyclic_decimal_nth_digit():
    # Classic top-school: nth digit after decimal point of k/7 (cycle of 6) or k/37 (cycle of 3) or k/11 (cycle of 2)
    choice = pick([
        (1, 7, "142857"),
        (2, 7, "285714"),
        (3, 7, "428571"),
        (4, 7, "571428"),
        (5, 7, "714285"),
        (6, 7, "857142"),
        (3, 13, "230769"),
        (4, 13, "307692"),
    ])
    num_val, den_val, cycle = choice
    k = len(cycle)  # 6
    n_pos = random.randint(65, 250)
    rem = n_pos % k
    ans_digit = cycle[rem - 1]
    w1 = cycle[rem % k]
    w2 = cycle[(rem - 2) % k]
    w3 = cycle[(rem + 1) % k]
    return mcq(
        stem=(
            f"เมื่อเขียนเศษส่วน **[[{num_val}/{den_val}]]** ในรูปทศนิยม "
            f"เลขโดดหลังจุดทศนิยมใน **ตำแหน่งที่ {n_pos}** คือเลขใด"
        ),
        correct=ans_digit,
        wrongs=[
            W(w1, "นับลำดับเศษจากการหารด้วย 6 คลาดเคลื่อนไป 1 ตำแหน่ง", "calc"),
            W(w2, "นับตำแหน่งเริ่มต้นผิด หรือถ้าหารลงตัวต้องตอบตัวที่ 6 ของชุดซ้ำ", "concept"),
            W(w3, f"หารตำแหน่งด้วย {den_val} แทนที่จะหารด้วยจำนวนตัวเลขในชุดที่ซ้ำ (6 ตัว)", "concept"),
        ],
        hint=f"ตั้งหารยาว [[{num_val}/{den_val}]] จะพบว่าทศนิยมซ้ำกันทีละ {k} ตัว คือ 0.{cycle}{cycle}... แล้วนำ {n_pos} หารด้วย {k} ดูเศษ",
        steps=[
            f"เมื่อนำ {num_val} ÷ {den_val} จะได้ทศนิยมซ้ำทีละ {k} ตัว คือ 0.{cycle}{cycle}...",
            f"นำตำแหน่งที่ {n_pos} หารด้วย {k} ได้ {n_pos // k} เศษ {rem if rem != 0 else '0 (ตรงกับตัวที่ 6)'}",
            f"ดังนั้นเลขโดดในตำแหน่งที่ {n_pos} คือ {ans_digit}",
        ],
    )


# ===========================================================================
# Skill 7: m.frac.of_qty — เศษส่วนของจำนวนและแผนภาพเศษส่วน
# ===========================================================================

skill(
    "m.frac.of_qty",
    "m.frac",
    "เศษส่วนของจำนวนและแผนภาพเศษส่วน",
    lesson={
        "concept": (
            "คำว่า 'ของ' ในเรื่องเศษส่วนหมายถึงการคูณ เช่น [[3/5]] ของ 40 คือ [[3/5]] × 40 "
            "แต่ถ้าโจทย์บอกค่าของส่วนย่อยมาให้แล้วถามหา 'จำนวนทั้งหมด' ต้องนำค่าที่รู้ไปหารด้วยเศษส่วนนั้น (หรือคิดหาค่าของ 1 ส่วนก่อน)"
        ),
        "steps": [
            "ถ้าโจทย์ให้จำนวนทั้งหมด N มา แล้วถาม [[a/b]] ของ N: คำนวณ (a/b) × N",
            "ถ้าโจทย์บอกว่า [[a/b]] ของทั้งหมดเท่ากับ K: ดังนั้น 1 ส่วน = K ÷ a และทั้งหมด (b ส่วน) = (K ÷ a) × b",
            "ถ้าใช้แผนภาพแท่ง (Bar Model): แบ่งแท่งออกเป็น b ช่องเท่า ๆ กัน เขียนค่าลงในช่องที่ทราบ จะเห็นคำตอบทันที",
        ],
        "example": {
            "q": "น้ำในถังมีอยู่ [[3/7]] ของถัง ถ้าน้ำที่มีอยู่คิดเป็น 24 ลิตร ถังใบนี้จุน้ำได้เต็มที่กี่ลิตร",
            "steps": [
                "น้ำ 3 ส่วน คิดเป็น 24 ลิตร ดังนั้น 1 ส่วน = 24 ÷ 3 = 8 ลิตร",
                "ความจุถังทั้งหมด 7 ส่วน = 7 × 8 = 56 ลิตร",
            ],
            "a": "56 ลิตร",
        },
        "mistakes": [
            "เมื่อโจทย์ให้ส่วนย่อยมาและถามหาทั้งหมด เผลอนำเศษส่วนไปคูณแทนที่จะหาร (เช่น เอา [[3/7]] × 24)",
            "โจทย์ถาม 'ต้องเติมอีกเท่าไรจึงจะเต็ม' แต่เผลอตอบความจุทั้งหมดของถัง",
        ],
        "tips": [
            "วาดแถบแบ่งช่อง (Bar Model) ทุกครั้งที่เจอโจทย์เศษส่วน จะไม่สับสนเลยว่าต้องคูณหรือหาร!",
        ],
    },
    weight=1.5,
)


@template("m.frac.of_qty", "easy")
def _frac_of_qty_compare():
    d1, d2 = pick([(3, 4), (4, 5), (3, 5), (5, 6), (4, 7), (5, 8)])
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    q1 = d1 * random.randint(6, 18)
    q2 = d2 * random.randint(6, 18)
    val1 = (n1 * q1) // d1
    val2 = (n2 * q2) // d2
    if val1 == val2:
        return None
    if val1 < val2:
        n1, d1, q1, val1, n2, d2, q2, val2 = n2, d2, q2, val2, n1, d1, q1, val1
    ans = val1 - val2
    return mcq(
        stem=f"**[[{n1}/{d1}]] ของ {q1}** มีค่ามากกว่า **[[{n2}/{d2}]] ของ {q2}** อยู่เท่าใด",
        correct=num(ans),
        wrongs=[
            W(num(val1 + val2), "นำค่าทั้งสองมาบวกกัน โจทย์ถามว่ามากกว่ากันอยู่เท่าใดจึงต้องลบกัน", "misread"),
            W(num(val1), f"ตอบเฉพาะค่าของ {n1}/{d1} ของ {q1} ลืมลบด้วยค่าที่สอง", "partial"),
            W(num(abs(q1 - q2)), "นำจำนวนเต็มหลังคำว่า 'ของ' มาลบกันโดยตรงโดยไม่ได้คูณเศษส่วนก่อน", "concept"),
        ],
        hint="คำว่า 'ของ' คือการคูณ หาค่าแต่ละก้อนก่อนแล้วนำมาลบกัน",
        steps=[
            f"ก้อนแรก: [[{n1}/{d1}]] × {q1} = {val1}",
            f"ก้อนหลัง: [[{n2}/{d2}]] × {q2} = {val2}",
            f"ต่างกันอยู่ = {val1} − {val2} = {num(ans)}",
        ],
    )


@template("m.frac.of_qty", "medium")
def _bar_model_find_whole_fig():
    # Visual fraction bar showing shaded parts and unshaded parts with a dimension/label for the unshaded (or shaded) part
    parts_total = random.choice([5, 6, 7, 8, 9])
    shaded = random.randint(2, parts_total - 2)
    unshaded = parts_total - shaded
    if shaded == unshaded:
        shaded -= 1
        unshaded += 1
    unit_val = random.randint(12, 35)
    shaded_val = shaded * unit_val
    unshaded_val = unshaded * unit_val
    total_val = parts_total * unit_val

    # Draw custom SVG bar with bracket label for the unshaded part
    w_bar, h_bar = 300, 34
    pw = w_bar / parts_total
    x0, y0 = 20, 14
    svg_parts = []
    for i in range(parts_total):
        svg_parts.append(svg.rect(x0 + i * pw, y0, pw, h_bar, shade=i < shaded))
    # Bracket under unshaded region
    ux1 = x0 + shaded * pw
    ux2 = x0 + parts_total * pw
    by = y0 + h_bar + 8
    svg_parts.append(svg.polyline([(ux1, by - 4), (ux1, by + 4), (ux2, by + 4), (ux2, by - 4)], cls="fig-mark"))
    svg_parts.append(svg.label(((ux1 + ux2) / 2, by + 18), f"ส่วนที่ไม่แรเงา = {num(unshaded_val)}", size=12, cls="fig-dim"))
    fig = svg.canvas(w_bar + 40, 82, svg_parts)

    ask = random.choice(["total", "shaded"])
    if ask == "total":
        return mcq(
            stem="จากแผนภาพแท่งที่แบ่งเป็นส่วนเท่า ๆ กันทุกช่อง จงหาว่า **ทั้งแท่งทั้งหมด** มีค่าเท่าใด",
            figure=fig,
            correct=num(total_val),
            wrongs=[
                W(num(shaded_val), f"นี่คือค่าของส่วนที่แรเงา ({shaded} ช่อง) โจทย์ถามทั้งแท่ง ({parts_total} ช่อง)", "partial"),
                W(num(unshaded_val * parts_total), f"นำ {num(unshaded_val)} ไปคูณ {parts_total} เลยโดยลืมหารด้วยจำนวนช่องที่ไม่แรเงา ({unshaded} ช่อง) ก่อน", "concept"),
                W(num(total_val - unit_val), "นับจำนวนช่องทั้งหมดของแผนภาพขาดไป 1 ช่อง", "detail"),
            ],
            hint=f"ดูว่าส่วนที่ไม่แรเงามีกี่ช่อง เพื่อหาค่าของ 1 ช่องก่อน แล้วคูณด้วยจำนวนช่องทั้งหมด ({parts_total} ช่อง)",
            steps=[
                f"ส่วนที่ไม่แรเงามี {unshaded} ช่อง มีค่ารวม {num(unshaded_val)} ดังนั้น 1 ช่อง = {num(unshaded_val)} ÷ {unshaded} = {unit_val}",
                f"ทั้งแท่งมีทั้งหมด {parts_total} ช่อง จึงมีค่า = {parts_total} × {unit_val} = {num(total_val)}",
            ],
        )
    else:
        return mcq(
            stem="จากแผนภาพแท่งที่แบ่งเป็นช่องเท่า ๆ กัน จงหาว่า **ส่วนที่แรเงา** มีค่าเท่าใด",
            figure=fig,
            correct=num(shaded_val),
            wrongs=[
                W(num(total_val), f"นี่คือค่าของทั้งแท่งรวมกัน ({parts_total} ช่อง) โจทย์ถามเฉพาะส่วนที่แรเงา ({shaded} ช่อง)", "misread"),
                W(num(unit_val), f"{unit_val} คือค่าของ 1 ช่อง ยังไม่ได้คูณจำนวนช่องที่แรเงา ({shaded} ช่อง)", "partial"),
                W(num((shaded + 1) * unit_val), "นับจำนวนช่องที่แรเงาเกินไป 1 ช่อง", "detail"),
            ],
            hint=f"ส่วนที่ไม่แรเงา {unshaded} ช่อง มีค่า {num(unshaded_val)} หาค่า 1 ช่องแล้วคูณด้วย {shaded} ช่องที่แรเงา",
            steps=[
                f"ส่วนที่ไม่แรเงา {unshaded} ช่อง = {num(unshaded_val)} จะได้ 1 ช่อง = {num(unshaded_val)} ÷ {unshaded} = {unit_val}",
                f"ส่วนที่แรเงามี {shaded} ช่อง จึงมีค่า = {shaded} × {unit_val} = {num(shaded_val)}",
            ],
        )


@template("m.frac.of_qty", "hard")
def _difference_of_two_fractions_word():
    person = name_th()
    pairs = [
        (Fraction(2, 5), Fraction(1, 4)),
        (Fraction(3, 5), Fraction(1, 3)),
        (Fraction(3, 7), Fraction(2, 7)),
        (Fraction(4, 7), Fraction(1, 3)),
        (Fraction(3, 8), Fraction(1, 4)),
        (Fraction(5, 8), Fraction(1, 3)),
        (Fraction(4, 9), Fraction(1, 3)),
        (Fraction(3, 5), Fraction(3, 10)),
    ]
    f1, f2 = pick(pairs)
    diff_f = f1 - f2
    lcm_bd = diff_f.denominator
    mult = random.randint(4, 15)
    total_pages = lcm_bd * mult
    diff_pages = int(diff_f * total_pages)
    read_total = int((f1 + f2) * total_pages)
    w_no_num = lcm_bd * diff_pages
    if w_no_num in (total_pages, read_total):
        w_no_num = total_pages + lcm_bd * 2
    w_unread = int(total_pages - read_total) if total_pages > read_total and int(total_pages - read_total) not in (total_pages, read_total, w_no_num) else total_pages - lcm_bd
    return mcq(
        stem=(
            f"{person}อ่านหนังสือวันแรกได้ **{frac(f1)}** ของเล่ม วันที่สองอ่านได้อีก **{frac(f2)}** ของเล่ม "
            f"ปรากฏว่าวันแรกอ่านได้มากกว่าวันที่สองอยู่ **{diff_pages} หน้า** หนังสือเล่มนี้มีทั้งหมดกี่หน้า"
        ),
        correct=f"{num(total_pages)} หน้า",
        wrongs=[
            W(f"{num(read_total)} หน้า", "นี่คือจำนวนหน้าที่อ่านไปสองวันรวมกัน ไม่ใช่จำนวนหน้าทั้งหมดของหนังสือ", "misread"),
            W(f"{num(w_no_num)} หน้า", "คูณด้วยตัวส่วนของผลต่างโดยลืมหารด้วยตัวเศษของผลต่าง", "partial"),
            W(f"{num(w_unread)} หน้า", "ตอบจำนวนหน้าที่ยังไม่ได้อ่านแทนจำนวนหน้าทั้งหมด", "misread"),
        ],
        hint=f"หาผลต่างของเศษส่วนที่อ่านในสองวัน คือ {frac(f1)} − {frac(f2)} ก่อน แล้วเทียบกับ {diff_pages} หน้า",
        steps=[
            f"วันแรกอ่านมากกว่าวันที่สองคิดเป็นเศษส่วน = {frac(f1)} − {frac(f2)} = {frac(diff_f)} ของเล่ม",
            f"ดังนั้น {frac(diff_f)} ของเล่ม คิดเป็น {diff_pages} หน้า",
            f"หนังสือทั้งเล่มมี = {diff_pages} × {diff_f.denominator} ÷ {diff_f.numerator} = {num(total_pages)} หน้า",
        ],
    )


# ===========================================================================
# Skill 8: m.frac.word_rem — โจทย์ปัญหาเศษส่วนหลายขั้นตอน ("ของที่เหลือ")
# ===========================================================================

skill(
    "m.frac.word_rem",
    "m.frac",
    "โจทย์ปัญหาเศษส่วนหลายขั้นตอน (ของที่เหลือ)",
    lesson={
        "concept": (
            "โจทย์ที่มีคำว่า 'ของที่เหลือ' ต้องระวังว่าฐานของเศษส่วนเปลี่ยนไป! "
            "ถ้าขั้นแรกใช้ไป [[a/b]] ของทั้งหมด จะเหลือ (1 − [[a/b]]) ของทั้งหมด แล้วขั้นต่อไปต้องนำเศษส่วนใหม่ไปคูณกับ 'ส่วนที่เหลือ' นี้"
        ),
        "steps": [
            "ขั้นที่ 1: ใช้ไป f1 ของทั้งหมด → เหลือครั้งแรก = (1 − f1) ของทั้งหมด",
            "ขั้นที่ 2: ใช้ไป f2 'ของที่เหลือ' → เหลือครั้งที่สอง = (1 − f2) × (1 − f1) ของทั้งหมด",
            "นำเศษส่วนที่เหลือสุทธิไปเทียบกับจำนวนเงิน/สิ่งของที่โจทย์บอก เพื่อหาค่าทั้งหมด",
        ],
        "example": {
            "q": "มีเงินอยู่จำนวนหนึ่ง ซื้อหนังสือไป [[1/3]] ของเงินที่มี และซื้อขนมไป [[1/4]] ของเงินที่เหลือ แล้วเหลือเงิน 150 บาท เดิมมีเงินกี่บาท",
            "steps": [
                "ซื้อหนังสือ [[1/3]] เหลือเงิน = 1 − [[1/3]] = [[2/3]] ของเงินเดิม",
                "ซื้อขนม [[1/4]] ของที่เหลือ จึงเหลือเงินสุทธิ = (1 − [[1/4]]) × [[2/3]] = [[3/4]] × [[2/3]] = [[1/2]] ของเงินเดิม",
                "เนื่องจาก [[1/2]] ของเงินเดิม = 150 บาท ดังนั้นเดิมมีเงิน = 150 × 2 = 300 บาท",
            ],
            "a": "300 บาท",
        },
        "mistakes": [
            "นำเศษส่วนทั้งสองครั้งมาบวกกันเลย เช่น [[1/3]] + [[1/4]] โดยลืมว่าครั้งที่สองคิดจาก 'ของที่เหลือ' ไม่ใช่ของทั้งหมด",
            "หาเศษส่วนที่ใช้ไปในขั้นที่สองแล้วลืมหักออกจากส่วนที่เหลือ",
        ],
        "tips": [
            "เทคนิคคิดเร็วสำหรับโจทย์ 'ของที่เหลือ': เศษส่วนที่เหลือสุทธิ = (1 − เศษส่วนขั้นที่ 1) × (1 − เศษส่วนขั้นที่ 2) ตัดทอนกันได้ง่ายมาก!",
        ],
    },
    weight=2.0,
)


@template("m.frac.word_rem", "medium")
def _remainder_word_forward():
    person = name_th()
    # Clean telescoping remainders: step 1 uses 1/b (leaves (b-1)/b), step 2 uses c/(b-1) of remainder
    b = random.choice([3, 4, 5, 6, 7])
    f1 = Fraction(random.randint(1, b - 2) if b > 3 else 1, b)
    rem1 = 1 - f1
    d2 = random.choice([3, 4, 5, 6])
    f2 = Fraction(random.randint(1, d2 - 1), d2)
    rem_final = rem1 * (1 - f2)
    denom = rem_final.denominator
    total = denom * random.randint(15, 45)
    ans = int(rem_final * total)
    # Mistake: subtracting (f1 + f2) from 1 directly
    wrong_direct_f = 1 - (f1 + f2)
    wrong_direct = int( abs(wrong_direct_f) * total) if wrong_direct_f != 0 else ans + 20
    spent_total = total - ans
    return mcq(
        stem=(
            f"{person}มีเงิน **{num(total)} บาท** นำไปซื้ออุปกรณ์การเรียน **{frac(f1)}** ของเงินที่มีทั้งหมด "
            f"จากนั้นนำเงินไปซื้อของขวัญอีก **{frac(f2)} ของเงินที่เหลือ** "
            f"{person}จะเหลือเงินกี่บาท"
        ),
        correct=f"{num(ans)} บาท",
        wrongs=[
            W(f"{num(wrong_direct if wrong_direct != ans else ans + 30)} บาท",
              "นำเศษส่วนทั้งสองครั้งมาบวกกันเป็นเศษส่วนของเงินทั้งหมด โดยลืมว่าครั้งที่สองคิดจาก 'ของที่เหลือ'", "trap"),
            W(f"{num(spent_total)} บาท", "นี่คือจำนวนเงินที่ใช้ไปทั้งหมด โจทย์ถามจำนวนเงินที่เหลือ", "misread"),
            W(f"{num(int(rem1 * f2 * total))} บาท", "นี่คือราคาของขวัญที่ซื้อในครั้งที่สอง ไม่ใช่เงินที่เหลือ", "partial"),
        ],
        hint=f"หาเงินที่เหลือหลังจากซื้ออุปกรณ์การเรียนก่อน แล้วจึงหักออกอีก {frac(f2)} ของเงินที่เหลือนั้น",
        steps=[
            f"หลังซื้ออุปกรณ์การเรียน {frac(f1)} จะเหลือเงิน = (1 − {frac(f1)}) × {num(total)} = {frac(rem1)} × {num(total)} = {num(int(rem1 * total))} บาท",
            f"ซื้อของขวัญไป {frac(f2)} ของที่เหลือ จึงเหลือเงินสุทธิ = (1 − {frac(f2)}) × {num(int(rem1 * total))} = {frac(1 - f2)} × {num(int(rem1 * total))} = {num(ans)} บาท",
        ],
    )


@template("m.frac.word_rem", "hard")
def _remainder_word_reverse():
    person = name_th()
    # Reverse "of the remainder": given final amount left, find initial total!
    pairs = [
        (Fraction(1, 3), Fraction(1, 4)),
        (Fraction(1, 4), Fraction(1, 3)),
        (Fraction(2, 5), Fraction(1, 3)),
        (Fraction(1, 5), Fraction(3, 8)),
        (Fraction(1, 3), Fraction(2, 5)),
        (Fraction(3, 7), Fraction(1, 4)),
        (Fraction(2, 7), Fraction(2, 5)),
        (Fraction(1, 6), Fraction(2, 5)),
    ]
    f1, f2 = pick(pairs)
    rem1 = 1 - f1
    rem_final = rem1 * (1 - f2)
    mult = random.randint(15, 60)
    left_money = rem_final.numerator * mult
    total_money = rem_final.denominator * mult
    rem1_money = int(rem1 * total_money)
    # Wrong 1: 1 - (f1 + f2)
    naive_rem = 1 - f1 - f2
    wrong_naive = int(left_money / naive_rem) if naive_rem > 0 and (left_money * naive_rem.denominator) % naive_rem.numerator == 0 else total_money + mult * 2
    return mcq(
        stem=(
            f"{person}มีเงินอยู่จำนวนหนึ่ง วันแรกใช้ไป **{frac(f1)}** ของเงินทั้งหมด "
            f"วันที่สองใช้ไปอีก **{frac(f2)} ของเงินที่เหลือ** แล้วปรากฏว่ายังเหลือเงินอยู่อีก **{num(left_money)} บาท** "
            f"เดิม{person}มีเงินทั้งหมดกี่บาท"
        ),
        correct=f"{num(total_money)} บาท",
        wrongs=[
            W(f"{num(rem1_money)} บาท", "คิดย้อนกลับเพียงขั้นเดียว (นี่คือเงินที่เหลือหลังจบวันแรก ไม่ใช่เงินเริ่มต้นทั้งหมด)", "partial"),
            W(f"{num(wrong_naive if wrong_naive != total_money else total_money + 120)} บาท",
              "นำเศษส่วนทั้งสองวันบวกกันโดยตรง ลืมว่าวันที่สองคิดจากเงินที่เหลือ", "trap"),
            W(f"{num(total_money - left_money)} บาท", "นี่คือจำนวนเงินที่ใช้ไปทั้งสองวันรวมกัน ไม่ใช่เงินเดิมทั้งหมด", "misread"),
        ],
        hint=f"เศษส่วนของเงินที่เหลือสุดท้าย = (1 − {frac(f1)}) × (1 − {frac(f2)}) ของเงินเดิมทั้งหมด",
        steps=[
            f"จบวันแรกเหลือเงิน = 1 − {frac(f1)} = {frac(rem1)} ของเงินเดิม",
            f"วันที่สองใช้ไป {frac(f2)} ของที่เหลือ จึงเหลือเงินสุทธิ = (1 − {frac(f2)}) × {frac(rem1)} = {frac(1 - f2)} × {frac(rem1)} = {frac(rem_final)} ของเงินเดิม",
            f"จะได้ {frac(rem_final)} ของเงินเดิม = {num(left_money)} บาท ดังนั้นเดิมมีเงิน = {num(left_money)} × {rem_final.denominator} ÷ {rem_final.numerator} = {num(total_money)} บาท",
        ],
    )


@template("m.frac.word_rem", "challenge")
def _two_stage_with_addition_between():
    # Classic top-school working-backwards fraction puzzle:
    # A basket of oranges: first sold 1/a of all oranges AND another k1 oranges.
    # Then sold 1/b of the remaining oranges, leaving final_rem oranges. How many originally?
    person = name_th()
    a = random.choice([2, 3, 4, 5])
    b = random.choice([2, 3, 4])
    # Work backwards cleanly:
    # After stage 1, let rem1 be a multiple of b:
    u = random.randint(6, 20)
    rem1 = b * u
    final_rem = (b - 1) * u  # since 1/b of rem1 is sold in stage 2
    # Before extra k1 oranges were sold in stage 1, (a - 1)/a of total = rem1 + k1
    # Pick k1 such that (rem1 + k1) is divisible by (a - 1)
    k1 = random.randint(2, 12)
    while (rem1 + k1) % (a - 1) != 0:
        k1 += 1
    total = ((rem1 + k1) // (a - 1)) * a
    wrong_add_k1_late = (((rem1 - k1) // (a - 1)) * a) if (rem1 > k1 and (rem1 - k1) % (a - 1) == 0) else total - a * 2
    return mcq(
        stem=(
            f"แม่ค้ามีส้มอยู่ตะกร้าหนึ่ง เช้าขายไปได้ **[[1/{a}]] ของส้มทั้งหมด กับอีก {k1} ผล** "
            f"ตอนบ่ายขายไปได้อีก **[[1/{b}]] ของส้มที่เหลือจากตอนเช้า** แล้วเหลือส้มในตะกร้า **{final_rem} ผล** "
            f"เดิมแม่ค้ามีส้มทั้งหมดกี่ผล"
        ),
        correct=f"{num(total)} ผล",
        wrongs=[
            W(f"{num(rem1 + k1)} ผล", f"นี่คือจำนวนส้ม {a - 1}/{a} ของทั้งหมด ยังไม่ได้คิดย้อนกลับไปเป็นส้มเต็มตะกร้า", "partial"),
            W(f"{num(wrong_add_k1_late if wrong_add_k1_late != total else total - a)} ผล",
              f"ตอนคิดย้อนกลับจากส้มที่เหลือตอนเช้า เผลอนำ {k1} ผลไปลบแทนที่จะบวกคืน", "sign"),
            W(f"{num((rem1 * a) // (a - 1) + k1 if (rem1 * a) % (a - 1) == 0 else total + k1)} ผล",
              f"คูณย้อนกลับด้วย {a}/{a - 1} ก่อนแล้วค่อยบวก {k1} ผล ทั้งที่ต้องบวก {k1} ผลคืนก่อน", "concept"),
        ],
        hint="คิดย้อนกลับจากข้างหลังมาข้างหน้า: หาจำนวนส้มที่เหลือหลังจบตอนเช้าก่อน แล้วบวกคืนอีก "
             f"{k1} ผล จะเท่ากับ [[{a - 1}/{a}]] ของส้มทั้งหมด",
        steps=[
            f"ตอนบ่ายขายไป [[1/{b}]] ของที่เหลือ จึงเหลือ [[{b - 1}/{b}]] ของตอนเช้า = {final_rem} ผล",
            f"ดังนั้นหลังจบตอนเช้าเหลือส้ม = {final_rem} × {b} ÷ {b - 1} = {rem1} ผล",
            f"ตอนเช้าขายไป [[1/{a}]] ของทั้งหมด กับอีก {k1} ผล แสดงว่า [[{a - 1}/{a}]] ของทั้งหมด = {rem1} + {k1} = {rem1 + k1} ผล",
            f"เดิมมีส้มทั้งหมด = {rem1 + k1} × {a} ÷ {a - 1} = {num(total)} ผล",
        ],
    )


# ===========================================================================
# Skill 9: m.frac.series — โจทย์ท้าทายอนุกรมเศษส่วนและเศษส่วนต่อเนื่อง
# ===========================================================================

skill(
    "m.frac.series",
    "m.frac",
    "อนุกรมเศษส่วนแยกเศษส่วนย่อยและโจทย์ท้าทาย",
    lesson={
        "concept": (
            "ผลบวกของเศษส่วนที่ตัวส่วนอยู่ในรูปผลคูณเรียงกัน เช่น [[1/1×2]] + [[1/2×3]] + ... + [[1/n(n+1)]] "
            "สามารถแยกแต่ละพจน์เป็นผลต่าง [[1/k(k+1)]] = [[1/k]] − [[1/k+1]] ทำให้พจน์กลางหักล้างกันหมด เหลือเพียงพจน์แรกสุดลบพจน์สุดท้าย!"
        ),
        "steps": [
            "สังเกตตัวส่วน: เช่น 2 = 1×2, 6 = 2×3, 12 = 3×4, 20 = 4×5, 30 = 5×6, 42 = 6×7, 56 = 7×8, 72 = 8×9, 90 = 9×10",
            "แยกแต่ละพจน์เป็น ([[1/ตัวหน้า]] − [[1/ตัวหลัง]])",
            "เมื่อพจน์กลางตัดกันหมด คำตอบจะเท่ากับ [[1/ตัวแรกสุด]] − [[1/ตัวท้ายสุด]]",
        ],
        "example": {
            "q": "จงหาค่าของ [[1/2]] + [[1/6]] + [[1/12]] + [[1/20]] + [[1/30]]",
            "steps": [
                "เขียนตัวส่วนในรูปผลคูณ: [[1/1×2]] + [[1/2×3]] + [[1/3×4]] + [[1/4×5]] + [[1/5×6]]",
                "แยกเป็น (1 − [[1/2]]) + ([[1/2]] − [[1/3]]) + ... + ([[1/5]] − [[1/6]])",
                "ตัดพจน์กลางหมด เหลือ 1 − [[1/6]] = [[5/6]]",
            ],
            "a": "[[5/6]]",
        },
        "mistakes": [
            "พยายามหา ค.ร.น. ของตัวส่วนทุกตัวซึ่งมีค่าใหญ่มากจนคำนวณผิด",
            "ตอนแยกพจน์สุดท้าย [[1/n(n+1)]] เผลอใช้ [[1/n]] แทนที่จะเป็น [[1/n+1]]",
        ],
        "tips": [
            "ถ้าจาก [[1/1×2]] บวกไปจนถึง [[1/n(n+1)]] คำตอบคือ [[n/n+1]] เสมอ!",
        ],
    },
    weight=1.4,
)


@template("m.frac.series", "hard")
def _telescoping_sum_from_one():
    n = random.randint(6, 25)
    k = random.choice([1, 2, 3, 5])
    last_den = n * (n + 1)
    ans = Fraction(k * n, n + 1)
    wrong_no_k = Fraction(n, n + 1) if k > 1 else Fraction(n - 1, n)
    wrong_next = Fraction(k * (n + 1), n + 2)
    wrong_one_over = Fraction(k * n, last_den)
    return mcq(
        stem=(
            f"จงหาผลบวกของ **[[{k}/2]] + [[{k}/6]] + [[{k}/12]] + [[{k}/20]] + ... + [[{k}/{last_den}]]**"
        ),
        correct=frac(ans, mixed=True),
        wrongs=[
            W(frac(wrong_no_k, mixed=True),
              f"ลืมคูณด้วยตัวเศษร่วม {k}" if k > 1 else f"แยกตัวประกอบของ {last_den} เป็น {n - 1} × {n} แทนที่จะเป็น {n} × {n + 1}",
              "partial" if k > 1 else "calc"),
            W(frac(wrong_next, mixed=True), "นับจำนวนพจน์เกินไป 1 พจน์", "calc"),
            W(frac(wrong_one_over, mixed=True), "นำจำนวนพจน์ไปส่วนด้วยตัวส่วนของพจน์สุดท้ายโดยตรง", "concept"),
        ],
        hint=f"ดึงตัวร่วม {k} ออกมา (ถ้ามี) แล้วสังเกตว่า 2 = 1×2, 6 = 2×3, ..., {last_den} = {n}×{n + 1} แยกเป็นผลต่าง",
        steps=[
            f"เขียนแต่ละพจน์ในรูป {k} × ([[1/m]] − [[1/m+1]]) โดยพจน์สุดท้ายคือ {k} × ([[1/{n}]] − [[1/{n + 1}]])",
            f"เมื่อนำมาบวกกัน พจน์ตรงกลางจะหักล้างกันหมด เหลือ {k} × (1 − [[1/{n + 1}]])",
            f"= {k} × [[{n}/{n + 1}]] = {frac(ans, mixed=True)}",
        ],
    )


@template("m.frac.series", "challenge")
def _telescoping_sum_arbitrary_start_or_continued_eq():
    mode = random.choice(["start_k", "continued_abc"])
    if mode == "start_k":
        a = random.randint(2, 5)
        n = random.randint(a + 4, a + 10)
        first_den = a * (a + 1)
        second_den = (a + 1) * (a + 2)
        third_den = (a + 2) * (a + 3)
        last_den = n * (n + 1)
        ans = Fraction(1, a) - Fraction(1, n + 1)
        wrong_from_1 = Fraction(n, n + 1)
        wrong_plus = Fraction(1, a) + Fraction(1, n + 1)
        wrong_last_n = Fraction(1, a) - Fraction(1, n)
        return mcq(
            stem=(
                f"จงหาค่าของ **[[1/{first_den}]] + [[1/{second_den}]] + [[1/{third_den}]] + ... + [[1/{last_den}]]**"
            ),
            correct=frac(ans),
            wrongs=[
                W(frac(wrong_from_1), f"ใช้สูตร 1 − 1/{n + 1} โดยลืมว่าพจน์แรกเริ่มที่ 1/({a}×{a + 1}) ไม่ใช่ 1/(1×2)", "trap"),
                W(frac(wrong_last_n), f"พจน์สุดท้ายแยกเป็น 1/{n} − 1/{n + 1} แต่เผลอลบด้วย 1/{n}", "calc"),
                W(frac(wrong_plus), f"นำ 1/{a} ไปบวกกับ 1/{n + 1} แทนที่จะลบกัน", "sign"),
            ],
            hint=f"พจน์แรกคือ [[1/{a}×{a + 1}]] = [[1/{a}]] − [[1/{a + 1}]] และพจน์สุดท้ายคือ [[1/{n}×{n + 1}]] = [[1/{n}]] − [[1/{n + 1}]]",
            steps=[
                f"แยกแต่ละพจน์: ([[1/{a}]] − [[1/{a + 1}]]) + ([[1/{a + 1}]] − [[1/{a + 2}]]) + ... + ([[1/{n}]] − [[1/{n + 1}]])",
                f"พจน์กลางหักล้างกันหมด เหลือ [[1/{a}]] − [[1/{n + 1}]]",
                f"ทำส่วนให้เท่ากัน ได้ = {frac(ans)}",
            ],
        )
    else:
        # Continued fraction decomposition: p/q = a + 1/(b + 1/c), find a + b + c
        a = random.randint(1, 4)
        b = random.randint(2, 5)
        c = random.randint(2, 6)
        val = a + Fraction(1, b + Fraction(1, c))
        p, q = val.numerator, val.denominator
        ans = a + b + c
        return mcq(
            stem=(
                f"ถ้า **[[{p}/{q}]] = a + [[1/b + [[1/c]]]]** "
                f"(เมื่อ a, b, c เป็นจำนวนนับ และ c > 1) จงหาค่าของ **a + b + c**"
            ),
            correct=str(ans),
            wrongs=[
                W(str(a * b * c if a * b * c != ans else ans + 3), "นำค่า a, b, c มาคูณกันแทนที่จะบวกกัน", "misread"),
                W(str(ans - a), f"คิดเฉพาะส่วนเศษส่วนแท้ ลืมบวกจำนวนเต็ม a = {a}", "partial"),
                W(str(ans + 1), "เปลี่ยนเศษเกินเป็นจำนวนคละในชั้นที่สองคลาดเคลื่อนไป 1", "calc"),
            ],
            hint=f"เปลี่ยน [[{p}/{q}]] เป็นจำนวนคละจะได้ค่า a ทันที จากนั้นกลับเศษเป็นส่วนของเศษส่วนที่เหลือแล้วทำเป็นจำนวนคละอีกครั้ง",
            steps=[
                f"เขียนเป็นจำนวนคละ: [[{p}/{q}]] = {a} + [[{p - a * q}/{q}]] จะได้ a = {a}",
                f"กลับเศษเป็นส่วน: [[1/{q}/{p - a * q}]] = 1 / ({b} + [[1/{c}]]) จะได้ b = {b} และ c = {c}",
                f"ดังนั้น a + b + c = {a} + {b} + {c} = {ans}",
            ],
        )
