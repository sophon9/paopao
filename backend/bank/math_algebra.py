"""Patterns and linear equations question templates for topic ``m.alg`` (แบบรูปและสมการ).

Covers number patterns (arithmetic, second-difference, Fibonacci-like,
alternating), nth term & Gauss series sums, geometric/matchstick/table patterns
(with SVG figures), algebraic expression evaluation, one/two-step & fractional
linear equations, equations with brackets & variables on both sides, balance
scales (with SVG figures), consecutive integers/evens/odds, and classic
top-school equation word problems (coins, surplus-and-deficit).
"""

from fractions import Fraction
import math
import random

from backend.bank import svg
from backend.bank.core import W, frac, mcq, name_th, num, pick, skill, template


# ---------------------------------------------------------------------------
# Private SVG figure helpers for patterns and balance scales
# ---------------------------------------------------------------------------

def _svg_matchstick_squares(counts=(1, 2, 3)):
    """Draw 1, 2, 3 joined squares made of matchsticks side-by-side."""
    s = 26
    y0 = 18
    parts = []
    cur_x = 18
    for idx, k in enumerate(counts, start=1):
        w_group = k * s
        for i in range(k):
            x = cur_x + i * s
            parts.append(svg.rect(x, y0, s, s, shade=(i % 2 == 0)))
        parts.append(svg.label((cur_x + w_group / 2, y0 + s + 18), f"รูปที่ {idx}", size=11, cls="fig-axis"))
        parts.append(svg.label((cur_x + w_group / 2, y0 + s + 32), f"({3 * k + 1} ก้าน)", size=10, cls="fig-dim"))
        cur_x += w_group + 28
    return svg.canvas(cur_x - 10, y0 + s + 44, parts)


def _svg_matchstick_triangles(counts=(1, 2, 3)):
    """Draw 1, 2, 3 joined triangles (alternating up/down or row of upright triangles) made of matchsticks."""
    s = 28
    h = 24
    y_bot = 42
    parts = []
    cur_x = 16
    for idx, k in enumerate(counts, start=1):
        w_group = k * s
        for i in range(k):
            x = cur_x + i * s
            pts = [(x, y_bot), (x + s, y_bot), (x + s / 2, y_bot - h)]
            parts.append(svg.polygon(pts, shade=True))
        parts.append(svg.label((cur_x + w_group / 2, y_bot + 16), f"รูปที่ {idx}", size=11, cls="fig-axis"))
        parts.append(svg.label((cur_x + w_group / 2, y_bot + 30), f"({3 * k} ก้าน)" if False else f"({k} รูปสามเหลี่ยม)", size=10, cls="fig-dim"))
        cur_x += w_group + 26
    return svg.canvas(cur_x - 8, y_bot + 42, parts)


def _svg_tables_and_chairs(per_side=2):
    """Draw 1, 2, 3 joined rectangular tables with chairs (dots) along top, bottom, and left/right ends."""
    tw, th = 32, 24
    y0 = 22
    parts = []
    cur_x = 28
    for k in (1, 2, 3):
        w_group = k * tw
        for i in range(k):
            x = cur_x + i * tw
            parts.append(svg.rect(x, y0, tw, th, shade=True))
            # Chairs on top and bottom of each table
            for c_idx in range(per_side):
                cx = x + tw * (c_idx + 0.5) / per_side
                parts.append(svg.dot((cx, y0 - 7), 3.5))
                parts.append(svg.dot((cx, y0 + th + 7), 3.5))
        # Chairs at left end and right end (1 each)
        parts.append(svg.dot((cur_x - 7, y0 + th / 2), 3.5))
        parts.append(svg.dot((cur_x + w_group + 7, y0 + th / 2), 3.5))
        seats = 2 * per_side * k + 2
        parts.append(svg.label((cur_x + w_group / 2, y0 + th + 22), f"โต๊ะ {k} ตัว", size=11, cls="fig-axis"))
        parts.append(svg.label((cur_x + w_group / 2, y0 + th + 36), f"({seats} ที่นั่ง)", size=10, cls="fig-dim"))
        cur_x += max(w_group, 48) + 36
    return svg.canvas(cur_x - 10, y0 + th + 48, parts)


def _svg_step_blocks(counts=(1, 2, 3)):
    """Draw staircase / L-shape block patterns for figures 1, 2, 3."""
    cell = 16
    y_bot = 64
    parts = []
    cur_x = 26
    for n in counts:
        # Staircase of 1 + 2 + ... + n blocks
        w_group = n * cell
        x_draw = cur_x + max(0, (44 - w_group) / 2)
        for col in range(n):
            col_h = col + 1
            for row in range(col_h):
                parts.append(svg.rect(x_draw + col * cell, y_bot - (row + 1) * cell, cell, cell, shade=True))
        total_b = n * (n + 1) // 2
        cx = x_draw + w_group / 2
        parts.append(svg.label((cx, y_bot + 16), f"รูปที่ {n}", size=11, cls="fig-axis"))
        parts.append(svg.label((cx, y_bot + 30), f"({total_b} ช่อง)", size=10, cls="fig-dim"))
        cur_x += max(w_group, 44) + 32
    return svg.canvas(cur_x - 10, y_bot + 42, parts)


def _svg_balance_scale(left_x_count, left_wt, right_x_count, right_wt):
    """Draw a balanced two-pan scale with ``x`` boxes and weight blocks on each pan."""
    w, h = 340, 128
    cx = w / 2
    beam_y = 74
    pan_w = 116
    lx, rx = 76, w - 76
    parts = [
        # Base & fulcrum triangle
        svg.polygon([(cx - 22, 108), (cx + 22, 108), (cx, beam_y)], cls="fig-face3"),
        svg.line((lx, beam_y), (rx, beam_y), cls="fig-line"),
        svg.dot((cx, beam_y), 4),
        # Left and right pan supports + pans
        svg.line((lx, beam_y), (lx, beam_y - 12), cls="fig-line"),
        svg.line((lx - pan_w / 2, beam_y - 12), (lx + pan_w / 2, beam_y - 12), cls="fig-line"),
        svg.line((rx, beam_y), (rx, beam_y - 12), cls="fig-line"),
        svg.line((rx - pan_w / 2, beam_y - 12), (rx + pan_w / 2, beam_y - 12), cls="fig-line"),
    ]

    def _draw_pan_items(pan_cx, x_cnt, wt):
        pan_top = beam_y - 12
        items = [("x", "x") for _ in range(x_cnt)]
        if wt > 0:
            items.append(("w", f"{wt}"))
        n_it = len(items)
        bw, bh = (24 if n_it <= 4 else 20), 26
        gap = 4
        total_w = n_it * bw + max(0, n_it - 1) * gap
        start_x = pan_cx - total_w / 2
        for i, (kind, txt) in enumerate(items):
            bx = start_x + i * (bw + gap)
            by = pan_top - bh
            if kind == "x":
                parts.append(svg.rect(bx, by, bw, bh, shade=True))
                parts.append(svg.label((bx + bw / 2, by + bh / 2), txt, size=12, bold=True))
            else:
                parts.append(svg.rect(bx, by - 4, bw + 6, bh + 4, cls="fig-face2"))
                parts.append(svg.label((bx + (bw + 6) / 2, by - 2 + bh / 2), f"{txt}", size=11, cls="fig-dim"))

    _draw_pan_items(lx, left_x_count, left_wt)
    _draw_pan_items(rx, right_x_count, right_wt)
    parts.append(svg.label((cx, 118), "สมดุล", size=11, cls="fig-axis"))
    return svg.canvas(w, h, parts)


# ===========================================================================
# Skill 1: m.alg.pattern_num — แบบรูปของจำนวน
# ===========================================================================

skill(
    "m.alg.pattern_num",
    "m.alg",
    "แบบรูปของจำนวนและการหาความสัมพันธ์",
    lesson={
        "concept": (
            "การหาจำนวนที่หายไปในแบบรูป ให้เริ่มจากเขียน 'ผลต่างระหว่างพจน์ที่ติดกัน' เสมอ "
            "ถ้าผลต่างยังไม่คงที่ ให้ดูผลต่างของผลต่าง (ชั้นที่ 2) หรือสังเกตการบวกสองพจน์หน้า (แบบฟีโบนัชชี) หรือแบบรูปสลับชุด"
        ),
        "steps": [
            "เขียนผลต่าง (+ หรือ −) ระหว่างตัวเลขที่อยู่ติดกันทุกคู่",
            "ถ้าเลขขึ้น-ลงสลับกัน หรือกระโดดแปลก ๆ ให้แยกดู 'ชุดตำแหน่งคี่ (ตัวที่ 1, 3, 5, ...)' กับ 'ชุดตำแหน่งคู่ (ตัวที่ 2, 4, 6, ...)'",
            "ถ้าผลต่างไม่เป็นระเบียบ ลองเช็กว่าแต่ละพจน์เกิดจาก 2 พจน์ข้างหน้าบวกกันหรือไม่ (เช่น 2, 3, 5, 8, 13, ...)",
        ],
        "example": {
            "q": "จงหาจำนวนถัดไปของแบบรูป 3, 5, 9, 15, 23, ___",
            "steps": [
                "หาผลต่างระหว่างพจน์ติดกัน: +2, +4, +6, +8",
                "จะเห็นว่าผลต่างเพิ่มขึ้นทีละ 2 ดังนั้นครั้งถัดไปต้องบวกเพิ่ม 10",
                "จำนวนถัดไป = 23 + 10 = 33",
            ],
            "a": "33",
        },
        "mistakes": [
            "บวกด้วยผลต่างตัวเดิมซ้ำ (เช่น เอา 23 + 8 = 31 แทนที่จะเพิ่มผลต่างเป็น +10)",
            "ในแบบรูปสลับชุด เผลอนำกฎของชุดตำแหน่งคี่ไปใช้กับตำแหน่งคู่",
        ],
        "tips": [
            "ถ้าเจอแบบรูปยาว 7–8 ตัวขึ้นไป มักเป็น 'แบบรูป 2 ชุดซ้อนกัน (สลับฟันปลา)' ให้ขีดเส้นโยงข้ามทีละตัวทันที!",
        ],
    },
    weight=1.3,
)


@template("m.alg.pattern_num", "easy")
def _second_diff_pattern():
    start = random.randint(2, 20)
    d0 = random.randint(2, 6)
    step = random.choice([2, 3, 4, 5])
    # Terms: t_0 = start, diffs are d0, d0+step, d0+2*step, d0+3*step, d0+4*step
    terms = [start]
    for i in range(5):
        terms.append(terms[-1] + d0 + i * step)
    ans = terms[-1]
    visible = terms[:-1]
    last_diff = d0 + 3 * step
    next_diff = d0 + 4 * step
    seq_str = ", ".join(str(x) for x in visible)
    return mcq(
        stem=f"จงหาจำนวนถัดไปของแบบรูป **{seq_str}, ____**",
        correct=num(ans),
        wrongs=[
            W(num(visible[-1] + last_diff), f"บวกด้วยผลต่างเดิมคือ +{last_diff} ซ้ำอีกครั้ง โดยไม่ได้เพิ่มผลต่างอีก {step}", "trap"),
            W(num(ans + step), f"เพิ่มผลต่างเกินไปอีกหนึ่งขั้น (+{next_diff + step} แทนที่จะเป็น +{next_diff})", "calc"),
            W(num(ans - 1), "บวกเลขในขั้นสุดท้ายคลาดเคลื่อนไป 1", "calc"),
        ],
        hint=f"หาผลต่างระหว่างพจน์ที่ติดกัน จะพบว่าผลต่างเพิ่มขึ้นทีละ {step}",
        steps=[
            f"ผลต่างระหว่างพจน์ที่ติดกันคือ +{d0}, +{d0 + step}, +{d0 + 2 * step}, +{last_diff}",
            f"ผลต่างเพิ่มขึ้นทีละ {step} ดังนั้นพจน์ถัดไปต้องบวกเพิ่ม {last_diff} + {step} = {next_diff}",
            f"จำนวนถัดไป = {visible[-1]} + {next_diff} = {num(ans)}",
        ],
    )


@template("m.alg.pattern_num", "medium")
def _interleaved_or_fibonacci_pattern():
    mode = random.choice(["interleaved", "fibonacci"])
    if mode == "interleaved":
        a0 = random.randint(3, 15)
        da = random.randint(3, 7)
        b0 = random.randint(25, 45)
        db = random.randint(2, 5)
        # 7 visible terms: a0, b0, a1, b1, a2, b2, a3 -> ask for 8th term (b3) or sum of 7th & 8th
        seq = [
            a0,
            b0,
            a0 + da,
            b0 - db,
            a0 + 2 * da,
            b0 - 2 * db,
            a0 + 3 * da,
        ]
        ans = b0 - 3 * db
        wrong_use_a_rule = seq[-1] + da
        wrong_sign_b = b0 - db
        seq_str = ", ".join(str(x) for x in seq)
        return mcq(
            stem=f"จากแบบรูป **{seq_str}, A** จงหาค่าของ **A**",
            correct=str(ans),
            wrongs=[
                W(str(wrong_use_a_rule), f"นำพจน์ที่ 7 ({seq[-1]}) ไปบวก {da} ตามกฎของพจน์ลำดับคี่ ทั้งที่ A เป็นพจน์ลำดับคู่", "trap"),
                W(str(b0 - 2 * db + db), f"พจน์ลำดับคู่ลดลงทีละ {db} แต่เผลอบวกเพิ่ม {db}", "sign"),
                W(str(seq[-1] - db if seq[-1] - db != ans else ans - 2), f"นำ {db} ไปลบออกจากพจน์ที่ 7 แทนที่จะลบออกจากพจน์ที่ 6 ({b0 - 2 * db})", "concept"),
            ],
            hint="สังเกตแยกเป็น 2 ชุดสลับกัน: ชุดตำแหน่งคี่ (ตัวที่ 1, 3, 5, 7) และชุดตำแหน่งคู่ (ตัวที่ 2, 4, 6, 8)",
            steps=[
                f"แยกเป็น 2 ชุดสลับกัน: ชุดตำแหน่งคี่คือ {a0}, {a0 + da}, {a0 + 2 * da}, {a0 + 3 * da} (เพิ่มทีละ {da})",
                f"ชุดตำแหน่งคู่คือ {b0}, {b0 - db}, {b0 - 2 * db}, A (ลดลงทีละ {db})",
                f"ดังนั้น A = {b0 - 2 * db} − {db} = {ans}",
            ],
        )
    else:
        # Fibonacci-like sequence: t1, t2, t1+t2, ...
        t1 = random.randint(1, 7)
        t2 = random.randint(t1 + 1, 11)
        terms = [t1, t2]
        for _ in range(5):
            terms.append(terms[-1] + terms[-2])
        ans = terms[6]
        visible = terms[:6]
        last_diff = visible[-1] - visible[-2]
        seq_str = ", ".join(str(x) for x in visible)
        return mcq(
            stem=f"กำหนดแบบรูป **{seq_str}, ____** จำนวนถัดไปมีค่าเท่าใด",
            correct=num(ans),
            wrongs=[
                W(num(visible[-1] + last_diff),
                  f"นำผลต่างครั้งก่อน (+{last_diff}) มาบวกซ้ำแทนที่จะนำสองพจน์ข้างหน้ามาบวกกัน", "trap"),
                W(num(visible[-1] * 2), "นำพจน์สุดท้ายคูณ 2 แทนที่จะบวกกับพจน์ก่อนหน้า", "concept"),
                W(num(ans - 2 if ans - 2 != visible[-1] + last_diff else ans + 2), "บวกเลขสองพจน์สุดท้ายคลาดเคลื่อน", "calc"),
            ],
            hint="สังเกตความสัมพันธ์ของ 3 พจน์ที่ติดกัน: พจน์ที่ 3 เกิดจากพจน์ที่ 1 บวกพจน์ที่ 2",
            steps=[
                f"แบบรูปนี้แต่ละพจน์เกิดจาก 2 พจน์ข้างหน้าบวกกัน เช่น {t1} + {t2} = {terms[2]}, {t2} + {terms[2]} = {terms[3]}",
                f"ดังนั้นจำนวนถัดไป = {visible[-2]} + {visible[-1]} = {num(ans)}",
            ],
        )


@template("m.alg.pattern_num", "hard")
def _fraction_pattern_next():
    # Fraction sequence where numerators and denominators follow distinct patterns (without simplifying intermediate display)
    n0 = random.randint(1, 5)
    dn = random.randint(2, 5)
    d0 = random.randint(2, 6)
    # Denominators grow by second-difference or multiplication
    step_d = random.randint(2, 4)
    nums = [n0 + i * dn for i in range(5)]
    dens = [d0]
    for i in range(4):
        dens.append(dens[-1] + (i + 1) * step_d)
    # Ask for sum of numerator and denominator of the 5th term
    ans = nums[4] + dens[4]
    seq_str = ",  ".join(f"[[{nums[i]}/{dens[i]}]]" for i in range(4))
    prev_d_diff = 3 * step_d
    next_d_diff = 4 * step_d
    return mcq(
        stem=(
            f"พิจารณาแบบรูปของเศษส่วน **{seq_str},  [[A/B]]** "
            f"(โดยไม่ต้องทอนเป็นเศษส่วนอย่างต่ำตามแบบรูป) จงหาค่าของ **A + B**"
        ),
        correct=num(ans),
        wrongs=[
            W(num(nums[4] + dens[3] + prev_d_diff),
              f"บวกตัวส่วนด้วยผลต่างเดิม (+{prev_d_diff}) แทนที่จะเพิ่มผลต่างเป็น +{next_d_diff}", "trap"),
            W(num(dens[4] - nums[4]), "นำ B กับ A มาลบกันแทนที่จะบวกกัน", "misread"),
            W(num(nums[4]), f"{nums[4]} คือค่าของตัวเศษ A อย่างเดียว ลืมบวกค่าตัวส่วน B", "partial"),
        ],
        hint="แยกคิดแบบรูปของตัวเศษ (ข้างบน) และแบบรูปของตัวส่วน (ข้างล่าง) คนละชุดกัน",
        steps=[
            f"ตัวเศษ: {nums[0]}, {nums[1]}, {nums[2]}, {nums[3]} เพิ่มขึ้นทีละ {dn} ดังนั้น A = {nums[3]} + {dn} = {nums[4]}",
            f"ตัวส่วน: {dens[0]}, {dens[1]}, {dens[2]}, {dens[3]} เพิ่มขึ้น +{step_d}, +{2 * step_d}, +{3 * step_d} ครั้งถัดไปจึงบวก +{4 * step_d} ได้ B = {dens[3]} + {4 * step_d} = {dens[4]}",
            f"ดังนั้น A + B = {nums[4]} + {dens[4]} = {num(ans)}",
        ],
    )


# ===========================================================================
# Skill 2: m.alg.nth_term — การหาพจน์ที่ n และผลบวกของลำดับ
# ===========================================================================

skill(
    "m.alg.nth_term",
    "m.alg",
    "การหาพจน์ที่ n และผลบวกของลำดับเลขคณิต",
    lesson={
        "concept": (
            "ลำดับเลขคณิตที่เพิ่มขึ้นทีละ d คงที่ พจน์ที่ n หาได้จากสูตร พจน์ที่ n = พจน์แรก + (n − 1) × d "
            "จำนวนพจน์ทั้งหมด = ((ปลาย − ต้น) ÷ ระยะห่าง) + 1 และผลบวกทั้งหมด = ((ต้น + ปลาย) × จำนวนพจน์) ÷ 2"
        ),
        "steps": [
            "หาพจน์ที่ n: เริ่มจากพจน์ที่ 1 แล้วบวกเพิ่มอีก (n − 1) ช่วง ช่วงละ d",
            "หาจำนวนพจน์: นำ (ตัวสุดท้าย − ตัวแรก) ÷ ระยะห่าง แล้วอย่าลืม + 1 เสมอ!",
            "หาผลบวก: จับคู่หัวท้าย (ต้น + ปลาย) คูณจำนวนพจน์ แล้วหารด้วย 2",
        ],
        "example": {
            "q": "ลำดับ 7, 11, 15, 19, ... พจน์ที่ 30 มีค่าเท่าใด",
            "steps": [
                "พจน์แรก = 7 และเพิ่มขึ้นทีละ d = 4",
                "จากพจน์ที่ 1 ไปพจน์ที่ 30 ห่างกัน 30 − 1 = 29 ช่วง",
                "พจน์ที่ 30 = 7 + (29 × 4) = 7 + 116 = 123",
            ],
            "a": "123",
        },
        "mistakes": [
            "หาพจน์ที่ n โดยเอา พจน์แรก + (n × d) เพราะลืมว่าจากพจน์ที่ 1 ไปพจน์ที่ n มีแค่ (n − 1) ช่วง",
            "นับจำนวนพจน์โดยเอา (ปลาย − ต้น) ÷ ห่าง แล้วลืมบวก 1",
        ],
        "tips": [
            "ผลบวกของจำนวนคี่เรียงกันตั้งแต่ 1 จำนวน n ตัวแรก มีค่าเท่ากับ n² เสมอ! เช่น 1+3+5+7+9 (5 ตัว) = 5² = 25",
        ],
    },
    weight=1.6,
)


@template("m.alg.nth_term", "easy")
def _arithmetic_nth_term():
    a1 = random.randint(3, 19)
    d = random.randint(3, 9)
    n = random.randint(25, 65)
    ans = a1 + (n - 1) * d
    wrong_nd = a1 + n * d
    wrong_mul_a1 = n * a1 + d
    t2, t3, t4 = a1 + d, a1 + 2 * d, a1 + 3 * d
    return mcq(
        stem=f"กำหนดแบบรูป **{a1}, {t2}, {t3}, {t4}, ...** จงหาว่า **จำนวนที่ {n}** ในแบบรูปนี้มีค่าเท่าใด",
        correct=num(ans),
        wrongs=[
            W(num(wrong_nd), f"นำ {a1} + ({n} × {d}) โดยลืมว่าจากพจน์ที่ 1 ไปพจน์ที่ {n} มีระยะห่างเพียง {n - 1} ช่วง", "formula"),
            W(num(n * d), f"คำนวณเฉพาะ {n} × {d} ลืมดูค่าพจน์เริ่มต้น ({a1})", "partial"),
            W(num(wrong_mul_a1), f"สลับนำ {n} ไปคูณกับพจน์แรก ({a1}) แทนที่จะคูณกับระยะห่าง ({d})", "formula"),
        ],
        hint=f"แต่ละพจน์เพิ่มขึ้นทีละ {d} จากพจน์ที่ 1 ไปถึงพจน์ที่ {n} ต้องบวกเพิ่มอีก {n - 1} ครั้ง",
        steps=[
            f"พจน์ที่ 1 คือ {a1} และเพิ่มขึ้นครั้งละ {d}",
            f"พจน์ที่ {n} = พจน์ที่ 1 + ({n} − 1) × {d} = {a1} + ({n - 1} × {d})",
            f"= {a1} + {num((n - 1) * d)} = {num(ans)}",
        ],
    )


@template("m.alg.nth_term", "medium")
def _how_many_terms_in_seq():
    a1 = random.randint(4, 25)
    d = random.randint(3, 8)
    n = random.randint(18, 48)
    an = a1 + (n - 1) * d
    t2, t3 = a1 + d, a1 + 2 * d
    return mcq(
        stem=f"ลำดับของจำนวน **{a1}, {t2}, {t3}, ..., {num(an)}** มีจำนวนทั้งหมดกี่จำนวน",
        correct=f"{n} จำนวน",
        wrongs=[
            W(f"{n - 1} จำนวน", f"นำ ({num(an)} − {a1}) ÷ {d} = {n - 1} แล้วลืมบวก 1 สำหรับพจน์เริ่มต้น", "trap"),
            W(f"{n + 1} จำนวน", "บวก 1 ซ้ำเกินไป 1 จำนวน", "calc"),
            W(f"{an // d if an // d not in (n, n - 1, n + 1) else n + 2} จำนวน",
              f"นำพจน์สุดท้าย ({num(an)}) หารด้วย {d} เลยโดยไม่ได้ลบพจน์แรกออกก่อน", "formula"),
        ],
        hint=f"ใช้สูตร จำนวนพจน์ = ((พจน์สุดท้าย − พจน์แรก) ÷ ระยะห่าง) + 1",
        steps=[
            f"พจน์แรก = {a1}, พจน์สุดท้าย = {num(an)} และระยะห่าง = {d}",
            f"จำนวนช่องว่าง = ({num(an)} − {a1}) ÷ {d} = {n - 1} ช่วง",
            f"ดังนั้นมีจำนวนทั้งหมด = {n - 1} + 1 = {n} จำนวน",
        ],
    )


@template("m.alg.nth_term", "hard")
def _gauss_arithmetic_sum():
    # Sum of arithmetic progression a1 + a2 + ... + an
    d = random.choice([1, 2, 3, 4])
    a1 = random.randint(1, 15)
    n = random.choice([20, 24, 25, 30, 36, 40, 50])
    an = a1 + (n - 1) * d
    ans = (a1 + an) * n // 2
    wrong_no_plus1 = (a1 + an) * (n - 1) // 2
    wrong_no_div2 = (a1 + an) * n
    wrong_only_an = (1 + an) * an // 2 if (1 + an) * an // 2 != ans else ans + a1 * 5
    t2, t3 = a1 + d, a1 + 2 * d
    return mcq(
        stem=f"จงหาผลบวกของ **{a1} + {t2} + {t3} + ... + {num(an)}**",
        correct=num(ans),
        wrongs=[
            W(num(wrong_no_plus1), f"นับจำนวนพจน์ได้ {n - 1} พจน์ (ลืมบวก 1) ตอนแทนสูตรผลบวก", "trap"),
            W(num(wrong_no_div2), "ลืมหารด้วย 2 ในสูตรผลบวก ((ต้น + ปลาย) × จำนวนพจน์) ÷ 2", "formula"),
            W(num(wrong_only_an), f"ใช้สูตรผลบวกตั้งแต่ 1 ถึง {num(an)} โดยไม่ได้ดูระยะห่างและพจน์เริ่มต้น", "formula"),
        ],
        hint="หาจำนวนพจน์ก่อน แล้วใช้สูตรผลบวก = ((ต้น + ปลาย) × จำนวนพจน์) ÷ 2",
        steps=[
            f"ลำดับเพิ่มขึ้นทีละ {d} มีจำนวนพจน์ = (({num(an)} − {a1}) ÷ {d}) + 1 = {n} พจน์",
            f"ผลบวก = (({a1} + {num(an)}) × {n}) ÷ 2 = ({num(a1 + an)} × {n}) ÷ 2 = {num(ans)}",
        ],
    )


# ===========================================================================
# Skill 3: m.alg.pattern_fig — แบบรูปเรขาคณิตและก้านไม้ขีดไฟ (มีรูปประกอบ)
# ===========================================================================

skill(
    "m.alg.pattern_fig",
    "m.alg",
    "แบบรูปเรขาคณิต ก้านไม้ขีดไฟ และการจัดโต๊ะ",
    lesson={
        "concept": (
            "แบบรูปของรูปเรขาคณิตที่วางเรียงต่อกัน (เช่น ก้านไม้ขีดไฟต่อเป็นรูปสี่เหลี่ยม หรือจัดโต๊ะต่อกัน) "
            "ต้องสังเกตว่า 'รูปแรกใช้กี่ชิ้น' และ 'เมื่อเพิ่มรูปถัดไป 1 รูป ต้องใช้เพิ่มรูปละกี่ชิ้น' (เพราะด้านที่ชนกันใช้ร่วมกัน!)"
        ),
        "steps": [
            "นับจำนวนชิ้นในรูปที่ 1, รูปที่ 2 และรูปที่ 3 เขียนเป็นลำดับตัวเลขออกมา",
            "หาว่าแต่ละรูปเพิ่มขึ้นทีละกี่ชิ้น (สมมติเพิ่มทีละ d) จะได้สูตรรูปที่ n = รูปที่ 1 + (n − 1) × d",
            "ถ้าโจทย์บอกจำนวนชิ้นทั้งหมดมาให้ แล้วถามว่าเป็นรูปที่เท่าใด ให้ตั้งสมการย้อนกลับ!",
        ],
        "example": {
            "q": "วางก้านไม้ขีดเป็นรูปสี่เหลี่ยมจัตุรัสเรียงต่อกันในแนวนอน รูปที่ 1 ใช้ 4 ก้าน รูปที่ 2 ใช้ 7 ก้าน รูปที่ 3 ใช้ 10 ก้าน รูปที่ 15 ต้องใช้ก้านไม้ขีดกี่ก้าน",
            "steps": [
                "จำนวนก้านไม้ขีดเรียงเป็น 4, 7, 10, ... (เพิ่มขึ้นรูปละ 3 ก้าน เพราะด้านข้างใช้ร่วมกัน)",
                "สูตรรูปที่ n คือ 3n + 1 (หรือ 4 + (n − 1) × 3)",
                "รูปที่ 15 ใช้ = 3(15) + 1 = 46 ก้าน",
            ],
            "a": "46 ก้าน",
        },
        "mistakes": [
            "นำจำนวนด้านของ 1 รูปคูณด้วย n โดยตรง (เช่น สี่เหลี่ยม 15 รูป เอา 4 × 15 = 60 ก้าน โดยลืมหักด้านที่ใช้ร่วมกัน)",
            "ในการจัดโต๊ะต่อกัน ลืมนับเก้าอี้หัว-ท้าย 2 ตัวที่คงที่เสมอ",
        ],
        "tips": [
            "จำสูตรลัดก้านไม้ขีดเรียงติดกัน: สามเหลี่ยมต่อกันใช้ 2n + 1 ก้าน · สี่เหลี่ยมต่อกันใช้ 3n + 1 ก้าน · ห้าเหลี่ยมต่อกันใช้ 4n + 1 ก้าน!",
        ],
    },
    weight=1.7,
)


@template("m.alg.pattern_fig", "easy")
def _staircase_blocks_fig():
    fig = _svg_step_blocks((1, 2, 3))
    n = random.randint(6, 25)
    ans = n * (n + 1) // 2
    wrong_prev = (n - 1) * n // 2
    wrong_linear = 2 * n + 1
    wrong_no_div2 = n * (n + 1)
    return mcq(
        stem=f"จากแบบรูปการเรียงบล็อกสี่เหลี่ยมเป็นขั้นบันไดดังรูป **รูปที่ {n}** จะมีบล็อกสี่เหลี่ยมทั้งหมดกี่ช่อง",
        figure=fig,
        correct=f"{ans} ช่อง",
        wrongs=[
            W(f"{wrong_prev} ช่อง", f"คำนวณผลบวกถึงแค่ {n - 1} (ได้รูปที่ {n - 1} แทนที่จะเป็นรูปที่ {n})", "calc"),
            W(f"{wrong_no_div2} ช่อง", f"นำ {n} × {n + 1} โดยลืมหารด้วย 2", "formula"),
            W(f"{wrong_linear if wrong_linear not in (ans, wrong_prev) else ans + 4} ช่อง",
              "เข้าใจผิดว่าจำนวนช่องเพิ่มขึ้นคงที่เท่ากันทุกขั้น", "concept"),
        ],
        hint=f"รูปที่ n เกิดจากบล็อกเรียงซ้อนกัน 1 + 2 + 3 + ... + n ช่อง ใช้สูตร n × (n + 1) ÷ 2",
        steps=[
            "สังเกตจำนวนบล็อก: รูปที่ 1 มี 1 ช่อง, รูปที่ 2 มี 1+2 = 3 ช่อง, รูปที่ 3 มี 1+2+3 = 6 ช่อง",
            f"ดังนั้นรูปที่ {n} มีบล็อก = 1 + 2 + 3 + ... + {n}",
            f"= ({n} × {n + 1}) ÷ 2 = {ans} ช่อง",
        ],
    )


@template("m.alg.pattern_fig", "medium")
def _matchstick_squares_fig():
    fig = _svg_matchstick_squares((1, 2, 3))
    n = random.randint(12, 35)
    ans = 3 * n + 1
    wrong_4n = 4 * n
    wrong_3n = 3 * n
    wrong_prev = 3 * (n - 1) + 1
    return mcq(
        stem=(
            f"นำก้านไม้ขีดไฟมาวางเรียงเป็นรูปสี่เหลี่ยมจัตุรัสติดต่อกันดังรูป "
            f"ถ้าต้องการสร้าง **รูปที่ {n}** (มีสี่เหลี่ยมจัตุรัสเรียงต่อกัน {n} รูป) จะต้องใช้ก้านไม้ขีดไฟทั้งหมดกี่ก้าน"
        ),
        figure=fig,
        correct=f"{ans} ก้าน",
        wrongs=[
            W(f"{wrong_4n} ก้าน", f"นำ 4 × {n} โดยลืมว่าด้านแนวตั้งตรงกลางใช้ก้านไม้ขีดร่วมกันระหว่างรูปติดกัน", "trap"),
            W(f"{wrong_3n} ก้าน", f"คิดรูปละ 3 ก้าน แต่ลืมบวกก้านปิดท้ายอีก 1 ก้าน", "partial"),
            W(f"{wrong_prev} ก้าน", f"คำนวณจำนวนช่วงคลาดเคลื่อนไป 1 รูป (ได้รูปที่ {n - 1})", "calc"),
        ],
        hint="รูปที่ 1 ใช้ 4 ก้าน และเมื่อต่อเพิ่มอีก 1 รูปจะใช้ไม้ขีดเพิ่มเพียงรูปละ 3 ก้าน (สูตรคือ 3n + 1)",
        steps=[
            "จำนวนก้านไม้ขีดของรูปที่ 1, 2, 3 คือ 4, 7, 10 ก้าน ตามลำดับ (เพิ่มขึ้นรูปละ 3 ก้าน)",
            f"ดังนั้นรูปที่ {n} ใช้ก้านไม้ขีด = 4 + ({n} − 1) × 3 = 3({n}) + 1 = {ans} ก้าน",
        ],
    )


@template("m.alg.pattern_fig", "challenge")
def _tables_and_chairs_reverse_fig():
    per_side = random.choice([1, 2, 3])
    fig = _svg_tables_and_chairs(per_side=per_side)
    # Each table adds 2 * per_side seats, plus 2 end seats -> Total seats = (2 * per_side) * n + 2
    step = 2 * per_side
    n_tables = random.randint(10, 28)
    total_seats = step * n_tables + 2
    first_seats = step + 2
    wrong_div_first = total_seats // first_seats if total_seats % first_seats == 0 else n_tables - 2
    wrong_add_2 = (total_seats + 2) // step
    return mcq(
        stem=(
            f"จัดโต๊ะอาหารรูปสี่เหลี่ยมผืนผ้าเรียงต่อกันเป็นแถวยาวดังรูป "
            f"(ด้านบนและด้านล่างของโต๊ะแต่ละตัวนั่งได้ด้านละ {per_side} คน และหัวท้ายสุดของแถวนั่งได้ข้างละ 1 คน) "
            f"ถ้ามีผู้ร่วมงานทั้งหมด **{total_seats} คน** นั่งเต็มทุกที่นั่งพอดี จะต้องใช้โต๊ะเรียงต่อกันกี่ตัว"
        ),
        figure=fig,
        correct=f"{n_tables} ตัว",
        wrongs=[
            W(f"{n_tables + 1} ตัว", "ลืมหักที่นั่งหัว-ท้าย 2 ที่นั่งออกก่อนนำจำนวนที่นั่งด้านข้างไปหาร", "partial"),
            W(f"{wrong_add_2 if wrong_add_2 not in (n_tables, n_tables + 1) else n_tables + 2} ตัว",
              "นำ 2 ที่นั่งหัว-ท้ายไปบวกเพิ่มแทนที่จะลบออกก่อนหาร", "sign"),
            W(f"{wrong_div_first if wrong_div_first != n_tables else n_tables - 3} ตัว",
              f"คิดว่าโต๊ะทุกตัวนั่งได้ตัวละ {first_seats} คนเหมือนตอนวางแยกเดี่ยว ๆ", "trap"),
        ],
        hint=f"หักที่นั่งหัว-ท้ายสุดของแถวออก 2 คนก่อน ที่เหลือคือคนที่นั่งขนาบข้างโต๊ะ ตัวละ {step} คน",
        steps=[
            f"เมื่อนำโต๊ะมาเรียงต่อกัน โต๊ะ n ตัว จะนั่งด้านข้างได้ตัวละ {step} คน และหัว-ท้ายสุดอีก 2 คน",
            f"เขียนเป็นสมการ: {step}n + 2 = {total_seats}",
            f"จะได้ {step}n = {total_seats - 2} ดังนั้นต้องใช้โต๊ะ n = {total_seats - 2} ÷ {step} = {n_tables} ตัว",
        ],
    )


# ===========================================================================
# Skill 4: m.alg.eval — นิพจน์พีชคณิตและการแทนค่าตัวแปร
# ===========================================================================

skill(
    "m.alg.eval",
    "m.alg",
    "นิพจน์พีชคณิตและการแทนค่าตัวแปร",
    lesson={
        "concept": (
            "นิพจน์พีชคณิตคือประโยคที่มีตัวแปร เช่น 3x + 2y − 5 โดยที่ 3x หมายถึง 3 × x "
            "การหาค่าของนิพจน์ทำได้โดยแทนค่าตัวแปรด้วยตัวเลขที่กำหนด แล้วคำนวณตามลำดับการดำเนินการ (ยกกำลัง → คูณ/หาร → บวก/ลบ)"
        ),
        "steps": [
            "เขียนวงเล็บครอบค่าตัวแปรทุกครั้งที่แทนค่า เพื่อป้องกันการสับสนเครื่องหมาย",
            "คำนวณเลขยกกำลังและการคูณติดตัวแปรก่อน แล้วจึงบวกลบ",
            "สำหรับโจทย์แนวข้อสอบแข่งขันที่ให้ค่าของก้อน เช่น 2x + 3y = 11 แล้วถาม 6x + 9y − 5 ให้สังเกตว่า 6x + 9y = 3(2x + 3y) แทนค่าทั้งก้อนได้เลย!",
        ],
        "example": {
            "q": "ถ้า a = 4 และ b = 3 แล้วค่าของ 2a² − 3ab มีค่าเท่าใด",
            "steps": [
                "แทนค่า a = 4 และ b = 3: ได้ 2(4²) − 3(4)(3)",
                "คิดเลขยกกำลังก่อน: 2(16) − 36 = 32 − 36 = −4",
            ],
            "a": "−4",
        },
        "mistakes": [
            "เห็น 2a² แล้วเอา (2 × a) ไปยกกำลังสอง ทั้งที่ต้องยกกำลังสองเฉพาะ a ก่อนแล้วค่อยคูณ 2",
            "เห็น 3x เมื่อ x = 5 แล้วเขียนต่อกันเป็น 35 แทนที่จะคูณกันเป็น 3 × 5 = 15",
        ],
        "tips": [
            "ถ้าโจทย์ให้ 1 สมการ แต่มี 2 ตัวแปร (เช่น ให้ค่า 3a − 2b มา) แปลว่าโจทย์ไม่ได้ให้หา a, b แยกตัว แต่ต้องจัดรูปสิ่งที่ถามให้อยู่ในรูปพหุคูณของ (3a − 2b)!",
        ],
    },
    weight=1.2,
)


@template("m.alg.eval", "easy")
def _eval_linear_expression():
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    x = random.randint(3, 9)
    y = random.randint(2, 8)
    c = random.randint(4, 15)
    ans = a * x + b * y - c
    # Mistake: concatenating digits ax as 10a+x
    concat_val = (10 * a + x) + (10 * b + y) - c
    wrong_add_c = a * x + b * y + c
    wrong_swap = a * y + b * x - c
    if wrong_swap == ans:
        wrong_swap = ans + a
    return mcq(
        stem=f"ถ้า **x = {x}** และ **y = {y}** แล้วค่าของ **{a}x + {b}y − {c}** เท่ากับเท่าใด",
        correct=num(ans),
        wrongs=[
            W(num(wrong_swap), "แทนค่าตัวแปร x กับ y สลับตำแหน่งกัน", "misread"),
            W(num(wrong_add_c), f"นำ {c} มาบวกแทนที่จะลบออก", "sign"),
            W(num(concat_val), f"เข้าใจว่า {a}x คือการนำตัวเลขมาเขียนต่อกัน แทนที่จะเป็น {a} × {x}", "concept"),
        ],
        hint=f"{a}x หมายถึง {a} × x และ {b}y หมายถึง {b} × y แทนค่าแล้วคูณก่อนบวกลบ",
        steps=[
            f"แทนค่า x = {x} และ y = {y}: ({a} × {x}) + ({b} × {y}) − {c}",
            f"= {a * x} + {b * y} − {c} = {num(ans)}",
        ],
    )


@template("m.alg.eval", "medium")
def _eval_square_and_fraction_expr():
    a = random.randint(3, 7)
    b = random.randint(1, a - 1)
    k = random.choice([2, 3])
    # Evaluate (k * a^2 - b^2)
    ans = k * (a ** 2) - (b ** 2)
    # Trap: (k*a)^2 - b^2
    trap_ka_sq = ((k * a) ** 2) - (b ** 2)
    # Trap: k*(2*a) - (2*b)
    trap_mult2 = k * (2 * a) - (2 * b)
    return mcq(
        stem=f"เมื่อกำหนดให้ **a = {a}** และ **b = {b}** ค่าของ **{k}a² − b²** มีค่าเท่าใด",
        correct=num(ans),
        wrongs=[
            W(num(trap_ka_sq),
              f"นำ {k} × {a} = {k * a} ไปยกกำลังสอง ทั้งที่ {k}a² ต้องยกกำลังสองเฉพาะ a ก่อนแล้วจึงคูณด้วย {k}", "trap"),
            W(num(trap_mult2), "คำนวณยกกำลังสองโดยนำตัวแปรไปคูณ 2 แทนที่จะคูณตัวเอง", "concept"),
            W(num(k * (a ** 2) + (b ** 2)), "นำ b² มาบวกแทนที่จะลบออก", "sign"),
        ],
        hint=f"คำนวณ a² = {a}×{a} ก่อน แล้วค่อยคูณด้วย {k} จากนั้นลบด้วย b² = {b}×{b}",
        steps=[
            f"หาค่า a² = {a} × {a} = {a ** 2} และ b² = {b} × {b} = {b ** 2}",
            f"แทนค่าในนิพจน์: {k}({a ** 2}) − {b ** 2} = {k * (a ** 2)} − {b ** 2} = {num(ans)}",
        ],
    )


@template("m.alg.eval", "hard")
def _block_substitution_trick():
    # Classic top-school trick: Given p*x + q*y = V, find m*p*x + m*q*y + c
    p = random.randint(2, 5)
    q = random.randint(2, 6)
    val = random.randint(7, 25)
    m = random.randint(2, 5)
    c = random.randint(5, 30)
    sign_c = random.choice(["+", "-"])
    mp, mq = m * p, m * q
    ans = m * val + c if sign_c == "+" else m * val - c
    wrong_no_m = val + c if sign_c == "+" else val - c
    wrong_c_mult = m * (val + c) if sign_c == "+" else m * (val - c)
    return mcq(
        stem=(
            f"ถ้า **{p}x + {q}y = {val}** แล้วค่าของ **{mp}x + {mq}y {sign_c} {c}** เท่ากับข้อใด"
        ),
        correct=num(ans),
        wrongs=[
            W(num(wrong_c_mult), f"นำ {m} ไปคูณกับ {c} ด้วย ทั้งที่ {m} เป็นตัวประกอบร่วมของ {mp}x + {mq}y เท่านั้น", "trap"),
            W(num(wrong_no_m), f"แทนค่า {mp}x + {mq}y ด้วย {val} เลยโดยลืมคูณ {m} เท่า", "partial"),
            W(num(m * val - c if sign_c == "+" else m * val + c), f"ใช้เครื่องหมายของ {c} สลับตรงกันข้าม", "sign"),
        ],
        hint=f"สังเกตว่า {mp}x + {mq}y = {m}({p}x + {q}y) จึงแทนค่าก้อน ({p}x + {q}y) = {val} ลงไปได้ทันที",
        steps=[
            f"ดึงตัวร่วม {m} ออกจากสองพจน์แรก: {mp}x + {mq}y = {m}({p}x + {q}y)",
            f"แทนค่า {p}x + {q}y = {val} จะได้ {m}({val}) {sign_c} {c} = {m * val} {sign_c} {c} = {num(ans)}",
        ],
    )


# ===========================================================================
# Skill 5: m.alg.eq_basic — การแก้สมการเชิงเส้น (หนึ่งถึงสองขั้นตอนและเศษส่วน)
# ===========================================================================

skill(
    "m.alg.eq_basic",
    "m.alg",
    "การแก้สมการเชิงเส้นและสมการเศษส่วน",
    lesson={
        "concept": (
            "การแก้สมการคือการหาค่าของตัวแปรที่ทำให้สมการเป็นจริง โดยใช้สมบัติการเท่ากัน "
            "(ทำสิ่งตรงข้ามทั้งสองข้างของสมการ) โดยให้กำจัดตัวเลขที่อยู่ไกลตัวแปรออกไปก่อน!"
        ),
        "steps": [
            "สมการรูป ax + b = c: กำจัด +b ด้วยการลบ b ทั้งสองข้างก่อน แล้วจึงหารด้วย a",
            "สมการรูป [[x + b/a]] = c: ตัวส่วน a หารอยู่ทั้งก้อน ต้องคูณด้วย a ทั้งสองข้างก่อน แล้วจึงลบด้วย b",
            "สมการเศษส่วนหลายตัวส่วน เช่น [[x/a]] + [[x/b]] = c: นำ ค.ร.น. ของตัวส่วนมาคูณตลอดทั้งสมการเพื่อทำให้ตัวส่วนหายไป",
        ],
        "example": {
            "q": "จงแก้สมการ [[x/3]] + [[x/4]] = 14",
            "steps": [
                "ค.ร.น. ของ 3 และ 4 คือ 12 นำ 12 คูณตลอดทั้งสมการ",
                "จะได้ 4x + 3x = 14 × 12 → 7x = 168",
                "ดังนั้น x = 168 ÷ 7 = 24",
            ],
            "a": "24",
        },
        "mistakes": [
            "ย้ายข้างโดยลืมเปลี่ยนเป็นเครื่องหมายตรงข้าม (เช่น + ย้ายไปเป็น + เหมือนเดิม)",
            "ตอนนำ ค.ร.น. คูณตลอดสมการเศษส่วน เผลอคูณเฉพาะฝั่งซ้ายแต่ลืมคูณตัวเลขฝั่งขวา!",
        ],
        "tips": [
            "ได้คำตอบแล้ว ลองแทนค่า x กลับเข้าไปในสมการตั้งต้นในใจ ใช้เวลาแค่ 3 วินาทีแต่รู้ทันทีว่าถูก 100%!",
        ],
    },
    weight=1.6,
)


@template("m.alg.eq_basic", "easy")
def _two_step_linear_eq():
    a = random.randint(3, 9)
    x = random.randint(4, 22)
    b = random.randint(5, 35)
    mode = random.choice(["plus", "minus"])
    if mode == "plus":
        rhs = a * x + b
        wrong_sign = (rhs + b) // a if (rhs + b) % a == 0 else x + b
        stem = f"ถ้า **{a}x + {b} = {rhs}** แล้ว **x** มีค่าเท่าใด"
        steps = [
            f"นำ {b} ลบออกทั้งสองข้าง: {a}x = {rhs} − {b} = {a * x}",
            f"นำ {a} ไปหาร: x = {a * x} ÷ {a} = {x}",
        ]
    else:
        rhs = a * x - b
        if rhs <= 0:
            return None
        wrong_sign = (rhs - b) // a if rhs > b and (rhs - b) % a == 0 else max(1, x - b)
        stem = f"ถ้า **{a}x − {b} = {rhs}** แล้ว **x** มีค่าเท่าใด"
        steps = [
            f"นำ {b} บวกทั้งสองข้าง: {a}x = {rhs} + {b} = {a * x}",
            f"นำ {a} ไปหาร: x = {a * x} ÷ {a} = {x}",
        ]
    return mcq(
        stem=stem,
        correct=str(x),
        wrongs=[
            W(str(wrong_sign if wrong_sign != x else x + 3), "ย้ายข้างพจน์ค่าคงที่โดยไม่ได้เปลี่ยนเครื่องหมายบวก/ลบ", "sign"),
            W(str(a * x), f"หาได้ {a}x = {a * x} แล้วลืมหารด้วยสัมประสิทธิ์ {a}", "partial"),
            W(str(x + 2 if x + 2 != wrong_sign else x + 4), "หารตัวเลขในขั้นสุดท้ายคลาดเคลื่อน", "calc"),
        ],
        hint=f"กำจัดพจน์ {b} ก่อน แล้วจึงนำ {a} ไปหาร",
        steps=steps,
    )


@template("m.alg.eq_basic", "medium")
def _fractional_group_eq():
    # Solve (a*x - b) / c = d
    a = random.randint(2, 6)
    x = random.randint(5, 18)
    c = random.randint(3, 7)
    d = random.randint(4, 15)
    # We need a*x - b = c*d -> b = a*x - c*d
    # Pick x large enough so b > 0
    while a * x <= c * d + 2:
        x += 3
    b = a * x - c * d
    # Trap: adding b to d BEFORE multiplying by c -> a*x = d + b
    trap_order = c * (d + b) // a if (c * (d + b)) % a == 0 else x - c
    wrong_sign_b = (c * d - b) // a if c * d > b and (c * d - b) % a == 0 else x - 2
    return mcq(
        stem=f"จงหาค่าของ **x** จากสมการ **[[{a}x − {b}/{c}]] = {d}**",
        correct=str(x),
        wrongs=[
            W(str(wrong_sign_b if wrong_sign_b != x else x - 3),
              f"หลังจากคูณ {c} แล้ว เผลอนำ {b} ไปลบออกจาก {c * d} แทนที่จะบวกเข้า", "sign"),
            W(str(trap_order if trap_order not in (x, wrong_sign_b) else x + 4),
              f"นำ {b} ไปบวกกับ {d} ก่อนที่จะคูณด้วยตัวส่วน {c}", "concept"),
            W(str(a * x), f"หาค่า {a}x = {a * x} ได้แล้ว แต่ลืมหารด้วย {a}", "partial"),
        ],
        hint=f"คูณด้วยตัวส่วน {c} ทั้งสองข้างก่อน จะได้ {a}x − {b} = {c * d}",
        steps=[
            f"นำ {c} คูณทั้งสองข้างของสมการ: {a}x − {b} = {d} × {c} = {c * d}",
            f"บวกด้วย {b} ทั้งสองข้าง: {a}x = {c * d} + {b} = {a * x}",
            f"หารด้วย {a}: x = {a * x} ÷ {a} = {x}",
        ],
    )


@template("m.alg.eq_basic", "hard")
def _equation_two_denominators():
    # Solve x/a + x/b = c  or  x/a - x/b = c
    pairs = [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (3, 6), (4, 6), (5, 6)]
    a, b = pick(pairs)
    op = random.choice(["+", "-"])
    coeff_f = Fraction(1, a) + Fraction(1, b) if op == "+" else Fraction(1, a) - Fraction(1, b)
    lcm_ab = coeff_f.denominator
    num_coeff = coeff_f.numerator
    k = random.randint(2, 9)
    x = lcm_ab * k
    c = num_coeff * k
    trap_add_den = c * (a + b)
    trap_no_rhs = c
    trap_3 = num_coeff * x if num_coeff > 1 else c * (b - a)
    if trap_3 in (x, trap_add_den, trap_no_rhs):
        trap_3 = x + a + b
    return mcq(
        stem=f"ถ้า **[[x/{a}]] {op} [[x/{b}]] = {c}** แล้ว **x** มีค่าเท่าใด",
        correct=num(x),
        wrongs=[
            W(num(trap_add_den if trap_add_den != x else x + lcm_ab),
              f"นำตัวส่วนมาบวกกันเป็น x/{a + b} = {c} ซึ่งผิดหลักการบวกลบเศษส่วน", "concept"),
            W(num(trap_no_rhs if trap_no_rhs != x else x - lcm_ab),
              f"ทำส่วนฝั่งซ้ายให้เป็น {lcm_ab} แล้ว แต่ลืมคูณฝั่งขวา ({c}) ด้วย {lcm_ab}", "partial"),
            W(num(trap_3),
              f"คูณด้วย {lcm_ab} แล้วลืมหารด้วยสัมประสิทธิ์ {num_coeff}" if num_coeff > 1 else "ใช้ผลต่างของตัวส่วนแทน ค.ร.น. ของตัวส่วน",
              "partial" if num_coeff > 1 else "concept"),
        ],
        hint=f"นำ ค.ร.น. ของ {a} และ {b} คือ {lcm_ab} คูณตลอดทั้งสมการเพื่อกำจัดตัวส่วน",
        steps=[
            f"ค.ร.น. ของ {a} และ {b} คือ {lcm_ab} นำ {lcm_ab} คูณตลอดทั้งสมการ",
            f"จะได้ {lcm_ab // a}x {op} {lcm_ab // b}x = {c} × {lcm_ab}",
            f"{num_coeff}x = {c * lcm_ab} ดังนั้น x = {c * lcm_ab} ÷ {num_coeff} = {num(x)}",
        ],
    )


# ===========================================================================
# Skill 6: m.alg.eq_adv — สมการที่มีวงเล็บและตัวแปรอยู่ทั้งสองข้าง
# ===========================================================================

skill(
    "m.alg.eq_adv",
    "m.alg",
    "สมการที่มีวงเล็บและตัวแปรอยู่ทั้งสองข้าง",
    lesson={
        "concept": (
            "เมื่อสมการมีตัวแปรอยู่ทั้งสองข้าง ให้ย้ายพจน์ที่มีตัวแปรไปรวมกันข้างเดียว และย้ายตัวเลขไปอยู่อีกข้าง "
            "หากมีวงเล็บให้ใช้สมบัติการแจกแจง a(x + b) = ax + ab โดยระวังเครื่องหมายลบหน้าวงเล็บต้องเปลี่ยนเครื่องหมายทุกพจน์ในวงเล็บ!"
        ),
        "steps": [
            "กระจายตัวเลขหน้าวงเล็บเข้าไปคูณทุกตัวในวงเล็บ (ระวัง: −a(x − b) = −ax + ab)",
            "ย้ายพจน์ตัวแปรไปฝั่งที่มีสัมประสิทธิ์มากกว่า เพื่อไม่ให้สัมประสิทธิ์ติดลบ",
            "ย้ายตัวเลขคงที่ไปอีกฝั่ง แล้วหารด้วยสัมประสิทธิ์หน้าตัวแปร",
        ],
        "example": {
            "q": "จงแก้สมการ 5(x − 2) − 2(x − 3) = 14",
            "steps": [
                "กระจายวงเล็บ (ระวัง −2 คูณ −3 ได้ +6): 5x − 10 − 2x + 6 = 14",
                "รวมพจน์ที่คล้ายกัน: 3x − 4 = 14",
                "จะได้ 3x = 18 ดังนั้น x = 6",
            ],
            "a": "6",
        },
        "mistakes": [
            "กระจายเฉพาะตัวหน้าในวงเล็บ เช่น 3(x + 4) เขียนเป็น 3x + 4 (ลืมเอา 3 × 4)",
            "เจอเครื่องหมายลบหน้าวงเล็บ เช่น −2(x − 3) แล้วกระจายเป็น −2x − 6 แทนที่จะเป็น −2x + 6",
        ],
        "tips": [
            "ขีดเส้นใต้เครื่องหมายหน้าตัวเลขก่อนกระจายวงเล็บทุกครั้ง เช่น '−2' คูณกับ '−3' ได้ '+6'",
        ],
    },
    weight=1.7,
)


@template("m.alg.eq_adv", "medium")
def _eq_variables_both_sides():
    c_right = random.randint(2, 5)
    diff_coeff = random.randint(2, 5)
    a_left = c_right + diff_coeff
    x = random.randint(3, 16)
    b_left = random.randint(4, 25)
    d_right = (a_left - c_right) * x + b_left
    # Equation: a_left * x - b_left = c_right * x + (d_right - 2*b_left)? Let's make: a_left*x - b_left = c_right*x + k_right
    # Wait: a_left*x - b_left = c_right*x + k_right -> (a_left - c_right)*x = k_right + b_left
    k_right = diff_coeff * x - b_left
    if k_right <= 0:
        b_left = random.randint(2, diff_coeff * x - 2)
        k_right = diff_coeff * x - b_left
    # Mistakes:
    # 1) Adding a_left + c_right instead of subtracting
    # 2) Subtracting k_right - b_left instead of adding k_right + b_left
    wrong_sub_const = abs(k_right - b_left) // diff_coeff if abs(k_right - b_left) % diff_coeff == 0 and abs(k_right - b_left) // diff_coeff != x else x - 2
    wrong_no_div = diff_coeff * x
    return mcq(
        stem=f"จงหาคำตอบของสมการ **{a_left}x − {b_left} = {c_right}x + {k_right}**",
        correct=str(x),
        wrongs=[
            W(str(wrong_sub_const), f"ย้าย −{b_left} ไปฝั่งขวาแต่ไม่ได้เปลี่ยนเป็น +{b_left}", "sign"),
            W(str(wrong_no_div), f"ยุบรวมได้ {diff_coeff}x = {diff_coeff * x} แล้วลืมหารด้วย {diff_coeff}", "partial"),
            W(str(x + 2 if x + 2 != wrong_sub_const else x + 3),
              f"นำสัมประสิทธิ์ {a_left}x กับ {c_right}x มาบวกกันแทนที่จะลบกันเมื่อย้ายข้าง", "sign"),
        ],
        hint=f"ย้าย {c_right}x มาลบฝั่งซ้าย และย้าย −{b_left} ไปบวกฝั่งขวา",
        steps=[
            f"ย้ายตัวแปรมาฝั่งซ้ายและย้ายตัวเลขไปฝั่งขวา: {a_left}x − {c_right}x = {k_right} + {b_left}",
            f"จะได้ {diff_coeff}x = {diff_coeff * x}",
            f"ดังนั้น x = {diff_coeff * x} ÷ {diff_coeff} = {x}",
        ],
    )


@template("m.alg.eq_adv", "hard")
def _eq_brackets_negative_sign_trap():
    # Classic trap: a(x + b) - c(x - d) = rhs
    c = random.randint(2, 4)
    diff = random.choice([2, 3, 4])
    a = c + diff
    b = random.randint(1, 5)
    d = random.randint(2, 6)
    x = random.randint(3, 14)
    # True expansion: (a - c)x + a*b + c*d = rhs
    rhs = diff * x + a * b + c * d
    # Trap: writing -c(x - d) = -cx - cd -> (a - c)x + ab - cd = rhs -> (a-c)x = rhs - ab + cd = diff*x + 2*c*d
    # Pick c*d divisible by diff so the trap gives an integer!
    while (2 * c * d) % diff != 0:
        d += 1
        rhs = diff * x + a * b + c * d
    trap_neg_sign = x + (2 * c * d) // diff
    trap_no_dist = x + ((a - 1) * b + (c - 1) * d) // diff if ((a - 1) * b + (c - 1) * d) % diff == 0 else x + 3
    return mcq(
        stem=f"จงหาค่าของ **x** จากสมการ **{a}(x + {b}) − {c}(x − {d}) = {rhs}**",
        correct=str(x),
        wrongs=[
            W(str(trap_neg_sign),
              f"ตอนกระจาย −{c}(x − {d}) เผลอเขียนเป็น −{c}x − {c * d} แทนที่จะเป็น −{c}x + {c * d} (ลบคูณลบต้องได้บวก)", "trap"),
            W(str(trap_no_dist if trap_no_dist not in (x, trap_neg_sign) else x - 2),
              "กระจายตัวเลขหน้าวงเล็บคูณเฉพาะ x แต่ลืมคูณตัวเลขตัวหลังในวงเล็บ", "concept"),
            W(str(diff * x), f"หาค่า {diff}x = {diff * x} ได้แล้ว แต่ลืมหารด้วย {diff}", "partial"),
        ],
        hint=f"กระจายวงเล็บให้ครบทุกพจน์ และระวัง −{c} คูณกับ (−{d}) ต้องได้ +{c * d}",
        steps=[
            f"กระจายวงเล็บ: {a}x + {a * b} − {c}x + {c * d} = {rhs}",
            f"รวมพจน์ที่คล้ายกัน: {diff}x + {a * b + c * d} = {rhs}",
            f"จะได้ {diff}x = {rhs} − {a * b + c * d} = {diff * x} ดังนั้น x = {x}",
        ],
    )


@template("m.alg.eq_adv", "challenge")
def _coupled_two_equations():
    # Given equation 1 in x, find x and substitute into equation 2 to find k!
    x = random.randint(3, 10)
    a1 = random.randint(3, 6)
    b1 = random.randint(2, 9)
    rhs1 = a1 * (x + b1)
    # Second equation: k*x - m = c*x + n -> (k - c)x = m + n
    k = random.randint(3, 8)
    m = random.randint(4, 15)
    rhs2 = k * x - m
    return mcq(
        stem=(
            f"ถ้า **x** เป็นคำตอบของสมการ **{a1}(x + {b1}) = {rhs1}** "
            f"และทำให้สมการ **kx − {m} = {rhs2}** เป็นจริงด้วย แล้วค่าของ **k** เท่ากับเท่าใด"
        ),
        correct=str(k),
        wrongs=[
            W(str(x), f"{x} คือค่าของ x จากสมการแรก โจทย์ถามค่าของ k ในสมการที่สอง", "misread"),
            W(str((rhs2 - m) // x if rhs2 > m and (rhs2 - m) % x == 0 and (rhs2 - m) // x != k else k - 1),
              f"ตอนแก้หา k เผลอนำ {m} ไปลบออกจาก {rhs2} แทนที่จะบวกเข้า", "sign"),
            W(str(k * x), f"หาค่า kx = {k * x} ได้แล้ว แต่ลืมหารด้วย x ({x})", "partial"),
        ],
        hint="แก้สมการแรกเพื่อหาค่า x ก่อน แล้วนำค่า x ที่ได้ไปแทนในสมการที่สองเพื่อหาค่า k",
        steps=[
            f"จากสมการแรก: x + {b1} = {rhs1} ÷ {a1} = {x + b1} จะได้ x = {x}",
            f"แทนค่า x = {x} ลงในสมการที่สอง: {x}k − {m} = {rhs2}",
            f"จะได้ {x}k = {rhs2} + {m} = {k * x} ดังนั้น k = {k * x} ÷ {x} = {k}",
        ],
    )


# ===========================================================================
# Skill 7: m.alg.balance — สมการตาชั่งสองแขนสมดุล (มีรูปประกอบ)
# ===========================================================================

skill(
    "m.alg.balance",
    "m.alg",
    "สมการตาชั่งสองแขนสมดุล",
    lesson={
        "concept": (
            "ตาชั่งสองแขนที่อยู่ในแนวสมดุล แสดงว่าน้ำหนักรวมทางถาดซ้ายเท่ากับน้ำหนักรวมทางถาดขวา "
            "เราสามารถหยิบวัตถุชนิดเดียวกันและน้ำหนักเท่ากันออกจากทั้งสองถาดพร้อมกันได้โดยตาชั่งยังสมดุลเหมือนเดิม"
        ),
        "steps": [
            "เขียนสมการแทนน้ำหนักบนถาดซ้าย = น้ำหนักบนถาดขวา",
            "หยิบกล่อง x ออกจากทั้งสองฝั่งจำนวนเท่ากับฝั่งที่มีน้อยกว่า",
            "หักน้ำหนักลูกตุ้มตัวเลขออกจากทั้งสองฝั่ง แล้วหารเพื่อหาน้ำหนักของกล่อง x 1 ใบ",
        ],
        "example": {
            "q": "ถาดซ้ายมีกล่อง x จำนวน 3 ใบ กับลูกตุ้ม 4 กก. สมดุลกับถาดขวาที่มีกล่อง x จำนวน 1 ใบ กับลูกตุ้ม 16 กก. กล่อง x หนักใบละกี่กิโลกรัม",
            "steps": [
                "ตั้งสมการ: 3x + 4 = x + 16",
                "หยิบกล่อง x ออกข้างละ 1 ใบ และเอาลูกตุ้มออกข้างละ 4 กก.: เหลือ 2x = 12",
                "ดังนั้นกล่อง x หนักใบละ 12 ÷ 2 = 6 กิโลกรัม",
            ],
            "a": "6 กิโลกรัม",
        },
        "mistakes": [
            "นำจำนวนกล่อง x ทั้งสองฝั่งมาบวกกันแทนที่จะหยิบออกเท่า ๆ กัน",
            "ลืมหารด้วยจำนวนกล่อง x ที่เหลือในขั้นสุดท้าย",
        ],
        "tips": [
            "ขีดฆ่ากล่อง x ที่ซ้ำกันทั้งซ้ายและขวาในรูปออกคู่ต่อคู่ได้เลย จะเห็นสมการสั้น ๆ ทันที!",
        ],
    },
    weight=1.2,
)


@template("m.alg.balance", "easy")
def _balance_scale_one_side_x_fig():
    x_cnt = random.choice([2, 3, 4])
    x_val = random.randint(4, 18)
    left_wt = random.randint(3, 15)
    right_wt = x_cnt * x_val + left_wt
    fig = _svg_balance_scale(x_cnt, left_wt, 0, right_wt)
    return mcq(
        stem=(
            f"จากรูปตาชั่งสองแขนอยู่ในภาวะสมดุล กล่อง **x** แต่ละใบมีน้ำหนักเท่ากัน "
            f"และตัวเลขบนแท่งน้ำหนักมีหน่วยเป็นกิโลกรัม กล่อง **x** หนึ่งใบหนักกี่กิโลกรัม"
        ),
        figure=fig,
        correct=f"{x_val} กิโลกรัม",
        wrongs=[
            W(f"{x_cnt * x_val} กิโลกรัม", f"นี่คือน้ำหนักรวมของกล่อง x ทั้ง {x_cnt} ใบ ลืมหารด้วย {x_cnt}", "partial"),
            W(f"{(right_wt + left_wt) // x_cnt if (right_wt + left_wt) % x_cnt == 0 else x_val + left_wt} กิโลกรัม",
              f"นำน้ำหนัก {left_wt} กก. ไปบวกกับ {right_wt} กก. แทนที่จะหักออก", "sign"),
            W(f"{right_wt // x_cnt if right_wt // x_cnt != x_val else x_val + 2} กิโลกรัม",
              f"นำ {right_wt} หารด้วย {x_cnt} เลยโดยลืมหักน้ำหนัก {left_wt} กก. ทางฝั่งซ้ายออกก่อน", "partial"),
        ],
        hint=f"หักน้ำหนัก {left_wt} กก. ออกจากทั้งสองข้างก่อน แล้วแบ่งน้ำหนักที่เหลือให้กล่อง x ทั้ง {x_cnt} ใบเท่า ๆ กัน",
        steps=[
            f"จากรูปเขียนสมการได้: {x_cnt}x + {left_wt} = {right_wt}",
            f"หักออกข้างละ {left_wt} กก.: {x_cnt}x = {right_wt} − {left_wt} = {x_cnt * x_val}",
            f"ดังนั้น x = {x_cnt * x_val} ÷ {x_cnt} = {x_val} กิโลกรัม",
        ],
    )


@template("m.alg.balance", "medium")
def _balance_scale_both_sides_x_fig():
    right_x = random.choice([1, 2])
    diff_x = random.choice([2, 3])
    left_x = right_x + diff_x
    x_val = random.randint(5, 16)
    left_wt = random.randint(4, 18)
    right_wt = diff_x * x_val + left_wt
    fig = _svg_balance_scale(left_x, left_wt, right_x, right_wt)
    sum_x = left_x + right_x
    return mcq(
        stem=(
            f"ตาชั่งในรูปอยู่ในภาวะสมดุล กล่อง **x** ทุกใบมีน้ำหนักเท่ากัน (หน่วยเป็นกรัม) "
            f"จงหาว่ากล่อง **x** ใบเดียวมีน้ำหนักกี่กรัม"
        ),
        figure=fig,
        correct=f"{x_val} กรัม",
        wrongs=[
            W(f"{diff_x * x_val} กรัม", f"นี่คือน้ำหนักของกล่อง x จำนวน {diff_x} ใบ ลืมหารด้วย {diff_x}", "partial"),
            W(f"{(right_wt + left_wt) // diff_x if (right_wt + left_wt) % diff_x == 0 else x_val + 4} กรัม",
              f"นำน้ำหนัก {left_wt} กรัม ไปบวกกับ {right_wt} กรัม แทนที่จะนำมาลบกัน", "sign"),
            W(f"{(right_wt - left_wt) // sum_x if (right_wt - left_wt) % sum_x == 0 and (right_wt - left_wt) // sum_x != x_val else x_val - 2} กรัม",
              f"นำจำนวนกล่อง x ทั้งสองฝั่งมาบวกกัน ({left_x} + {right_x}) แทนที่จะลบกัน", "concept"),
        ],
        hint=f"หยิบกล่อง x ออกข้างละ {right_x} ใบ และหักน้ำหนักออกข้างละ {left_wt} กรัม",
        steps=[
            f"เขียนสมการจากตาชั่ง: {left_x}x + {left_wt} = {right_x}x + {right_wt}",
            f"หยิบกล่อง x ออกข้างละ {right_x} ใบ และเอาตุ้มน้ำหนักออกข้างละ {left_wt} กรัม: เหลือ {diff_x}x = {right_wt - left_wt}",
            f"ดังนั้นกล่อง x หนักใบละ = {right_wt - left_wt} ÷ {diff_x} = {x_val} กรัม",
        ],
    )


# ===========================================================================
# Skill 8: m.alg.consec — โจทย์สมการจำนวนเรียงกัน (จำนวนเต็ม คู่ คี่)
# ===========================================================================

skill(
    "m.alg.consec",
    "m.alg",
    "โจทย์สมการจำนวนเรียงกัน (จำนวนเต็ม คู่ คี่)",
    lesson={
        "concept": (
            "จำนวนเต็มที่เรียงติดกันจะห่างกันทีละ 1 (เช่น x, x+1, x+2) "
            "ส่วนจำนวนคู่ที่เรียงติดกัน หรือจำนวนคี่ที่เรียงติดกัน จะห่างกันทีละ 2 เสมอ! (เช่น x, x+2, x+4)"
        ),
        "steps": [
            "ถ้ามีจำนวนคี่ตัว (เช่น 3 หรือ 5 จำนวนเรียงกัน): ค่าเฉลี่ย (ผลบวก ÷ จำนวนตัว) คือ 'ตัวตรงกลาง' ทันที!",
            "ระวัง! ทั้งจำนวนคู่เรียงติดกัน และจำนวนคี่เรียงติดกัน ต่างก็เพิ่มขึ้นทีละ 2 เหมือนกัน (ไม่ใช่คี่บวก 1 หรือบวก 3)",
            "ตรวจสอบว่าโจทย์ถาม 'จำนวนที่น้อยที่สุด' 'จำนวนที่มากที่สุด' หรือ 'ผลบวกของตัวแรกกับตัวสุดท้าย'",
        ],
        "example": {
            "q": "ผลบวกของจำนวนคี่ 3 จำนวนที่เรียงติดกันเท่ากับ 81 จำนวนที่มากที่สุดคือจำนวนใด",
            "steps": [
                "หาจำนวนตรงกลาง (ตัวที่ 2) = 81 ÷ 3 = 27",
                "จำนวนคี่เรียงติดกันห่างกันทีละ 2 จึงได้ 25, 27, 29",
                "ดังนั้นจำนวนที่มากที่สุดคือ 29",
            ],
            "a": "29",
        },
        "mistakes": [
            "เห็นคำว่า 'จำนวนคี่เรียงติดกัน' แล้วสมมติเป็น x, x+1, x+3 หรือ x, x+3, x+5 (จริง ๆ ต้องห่างกันทีละ 2 คือ x, x+2, x+4)",
            "หาค่า x (ตัวน้อยสุด) ได้แล้วรีบตอบเลย โดยลืมดูว่าโจทย์ถามตัวมากที่สุด",
        ],
        "tips": [
            "สูตรลัด: ผลบวกของจำนวนเรียงกัน N ตัว → เอาผลบวกหารด้วย N จะได้ 'ค่ากึ่งกลาง' ทันที ไม่ต้องตั้งสมการย้ายข้างเลย!",
        ],
    },
    weight=1.5,
)


@template("m.alg.consec", "easy")
def _three_consecutive_integers():
    mid = random.randint(18, 65)
    n_count = random.choice([3, 5])
    total = mid * n_count
    half = n_count // 2
    smallest = mid - half
    largest = mid + half
    ask = random.choice(["max", "min"])
    ans = largest if ask == "max" else smallest
    opp = smallest if ask == "max" else largest
    q_word = "มากที่สุด" if ask == "max" else "น้อยที่สุด"
    return mcq(
        stem=f"ผลบวกของจำนวนนับที่เรียงติดกัน **{n_count} จำนวน** เท่ากับ **{num(total)}** จำนวนที่ **{q_word}** ในกลุ่มนี้คือจำนวนใด",
        correct=str(ans),
        wrongs=[
            W(str(mid), f"{mid} คือจำนวนที่อยู่ตรงกลาง ยังไม่ใช่จำนวนที่{q_word}", "partial"),
            W(str(opp), f"นี่คือจำนวนที่{'น้อยที่สุด' if ask == 'max' else 'มากที่สุด'} ตรงข้ามกับที่โจทย์ถาม", "misread"),
            W(str(ans + 1 if ask == "max" else ans - 1), "นับลำดับจากตัวกลางคลาดเคลื่อนไป 1", "calc"),
        ],
        hint=f"นำผลบวก {num(total)} หารด้วย {n_count} จะได้ 'จำนวนที่อยู่ตรงกลาง' ทันที",
        steps=[
            f"จำนวนที่อยู่ตรงกลาง = {num(total)} ÷ {n_count} = {mid}",
            f"จำนวนนับเรียงติดกัน {n_count} จำนวน คือ {', '.join(str(mid + i) for i in range(-half, half + 1))}",
            f"ดังนั้นจำนวนที่{q_word}คือ {ans}",
        ],
    )


@template("m.alg.consec", "medium")
def _consecutive_even_or_odd_four():
    # Sum of 4 consecutive even (or odd) numbers is S -> find largest or smallest
    is_odd = random.choice([True, False])
    first = random.randint(11, 55)
    if is_odd and first % 2 == 0:
        first += 1
    elif not is_odd and first % 2 == 1:
        first += 1
    nums = [first, first + 2, first + 4, first + 6]
    total = sum(nums)
    kind_word = "จำนวนคี่" if is_odd else "จำนวนคู่"
    ask = random.choice(["max", "min"])
    ans = nums[-1] if ask == "max" else nums[0]
    opp = nums[0] if ask == "max" else nums[-1]
    q_word = "มากที่สุด" if ask == "max" else "น้อยที่สุด"
    return mcq(
        stem=(
            f"ผลบวกของ **{kind_word}ที่เรียงติดกัน 4 จำนวน** เท่ากับ **{num(total)}** "
            f"จงหาว่า{kind_word}ที่ **{q_word}** ในสี่จำนวนนี้มีค่าเท่าใด"
        ),
        correct=str(ans),
        wrongs=[
            W(str(opp), f"นี่คือจำนวนที่{'น้อยที่สุด' if ask == 'max' else 'มากที่สุด'} โจทย์ถามจำนวนที่{q_word}", "misread"),
            W(str(total // 4), f"{total // 4} คือค่าเฉลี่ยกึ่งกลางระหว่างตัวที่ 2 กับตัวที่ 3 ไม่ใช่จำนวนในกลุ่ม", "partial"),
            W(str(nums[2] if ask == "max" else nums[1]), "ตอบตัวลำดับกลางแทนตัวริมสุด", "partial"),
        ],
        hint=f"ให้ 4 จำนวนคือ x, x+2, x+4, x+6 รวมกันได้ 4x + 12 = {num(total)}",
        steps=[
            f"{kind_word}เรียงติดกันห่างกันทีละ 2 ให้ทั้งสี่จำนวนคือ x, x + 2, x + 4 และ x + 6",
            f"ผลบวก: 4x + 12 = {num(total)} จะได้ 4x = {num(total - 12)} ดังนั้นตัวน้อยสุด x = {first}",
            f"จำนวนทั้งสี่คือ {nums[0]}, {nums[1]}, {nums[2]}, {nums[3]} จำนวนที่{q_word}คือ {ans}",
        ],
    )


@template("m.alg.consec", "hard")
def _consecutive_sum_comparison():
    # 5 consecutive odd/even numbers: sum of first 3 exceeds sum of last 2 by K. Find the largest number!
    # Let middle be m: numbers are m-4, m-2, m, m+2, m+4.
    # Sum of first 3 = 3m - 6. Sum of last 2 = 2m + 6.
    # Difference = (3m - 6) - (2m + 6) = m - 12 = K -> m = K + 12!
    is_odd = random.choice([True, False])
    m = random.randint(19, 65)
    if is_odd and m % 2 == 0:
        m += 1
    elif not is_odd and m % 2 == 1:
        m += 1
    k_diff = m - 12
    largest = m + 4
    smallest = m - 4
    kind_word = "จำนวนคี่" if is_odd else "จำนวนคู่"
    return mcq(
        stem=(
            f"กำหนด **{kind_word}ที่เรียงติดกัน 5 จำนวน** จากน้อยไปมาก "
            f"ถ้าผลบวกของ 3 จำนวนแรก มีค่ามากกว่าผลบวกของ 2 จำนวนหลังอยู่ **{k_diff}** "
            f"แล้วจำนวนที่ **มากที่สุด** ในห้าจำนวนนี้คือจำนวนใด"
        ),
        correct=str(largest),
        wrongs=[
            W(str(m), f"{m} คือจำนวนที่อยู่ตรงกลาง (ตัวที่ 3) โจทย์ถามจำนวนที่มากที่สุด (ตัวที่ 5)", "partial"),
            W(str(smallest), f"{smallest} คือจำนวนที่น้อยที่สุด (ตัวที่ 1) โจทย์ถามจำนวนที่มากที่สุด", "misread"),
            W(str(largest - 6), "สมมติให้จำนวนเรียงกันห่างกันทีละ 1 แทนที่จะห่างกันทีละ 2", "concept"),
        ],
        hint=f"ให้ 5 จำนวนคือ x, x+2, x+4, x+6, x+8 แล้วตั้งสมการ (ผลบวก 3 ตัวแรก) − (ผลบวก 2 ตัวหลัง) = {k_diff}",
        steps=[
            f"ให้{kind_word} 5 จำนวนคือ x, x+2, x+4, x+6 และ x+8",
            "ผลบวก 3 จำนวนแรก = 3x + 6 และผลบวก 2 จำนวนหลัง = 2x + 14",
            f"จากโจทย์: (3x + 6) − (2x + 14) = {k_diff} จะได้ x − 8 = {k_diff} ดังนั้น x = {smallest}",
            f"จำนวนที่มากที่สุดคือ x + 8 = {smallest} + 8 = {largest}",
        ],
    )


# ===========================================================================
# Skill 9: m.alg.word_eq — การเขียนและแก้สมการจากโจทย์ปัญหา
# ===========================================================================

skill(
    "m.alg.word_eq",
    "m.alg",
    "การเขียนและแก้สมการจากโจทย์ปัญหา",
    lesson={
        "concept": (
            "การแก้โจทย์ปัญหาด้วยสมการ ให้สมมติสิ่งที่โจทย์ถาม (หรือสิ่งที่เป็นฐาน) เป็นตัวแปร x "
            "เขียนปริมาณอื่น ๆ ในรูปของ x แล้วหาความสัมพันธ์ที่เท่ากันเพื่อตั้งสมการ"
        ),
        "steps": [
            "กำหนดตัวแปร x แทนสิ่งที่ต้องการหา แล้วเขียนเงื่อนไขอื่นในรูปของ x",
            "โจทย์เหรียญสองชนิดรวมกัน N เหรียญ: ถ้าชนิดแรกมี x เหรียญ อีกชนิดจะมี (N − x) เหรียญ แล้วคูณมูลค่าของแต่ละชนิด",
            "โจทย์แบ่งของให้เด็ก x คน: ตั้งสมการให้ 'จำนวนของทั้งหมด' จากเงื่อนไขที่ 1 เท่ากับเงื่อนไขที่ 2 (เช่น ax + เหลือ = bx − ขาด)",
        ],
        "example": {
            "q": "แบ่งลูกอมให้เด็กกลุ่มหนึ่ง ถ้าให้คนละ 5 เม็ด จะเหลือลูกอม 8 เม็ด แต่ถ้าให้คนละ 7 เม็ด จะขาดลูกอม 6 เม็ด มีเด็กกี่คน",
            "steps": [
                "ให้มีเด็ก x คน จำนวนลูกอมคิดจากเงื่อนไขแรกคือ 5x + 8 เม็ด",
                "จำนวนลูกอมคิดจากเงื่อนไขหลังคือ 7x − 6 เม็ด",
                "ตั้งสมการ: 5x + 8 = 7x − 6 → 2x = 14 → x = 7 คน",
            ],
            "a": "7 คน",
        },
        "mistakes": [
            "ในโจทย์แบ่งของแล้ว 'เหลือ' กับ 'ขาด' เผลอใส่เครื่องหมายเหมือนกันทั้งสองฝั่ง (เหลือต้อง + ขาดต้อง −)",
            "โจทย์เหรียญสองชนิด นำจำนวนเหรียญมาบวกกันเป็นจำนวนเงินโดยลืมคูณมูลค่าของเหรียญแต่ละชนิด",
        ],
        "tips": [
            "สูตรลัดโจทย์แบ่งของ (เหลือ/ขาด): จำนวนคน = (จำนวนที่เหลือ + จำนวนที่ขาด) ÷ (ผลต่างของที่แจกต่อคน)!",
        ],
    },
    weight=1.9,
)


@template("m.alg.word_eq", "medium")
def _word_to_equation_number():
    k = random.choice([3, 4, 5, 6])
    x = random.randint(8, 25)
    diff = random.randint(5, 29)
    # "k times a number is greater than twice the number by V" or "k times a number minus diff equals twice the number plus ..."
    m = random.choice([1, 2])
    if m >= k:
        m = 1
    # k*x - diff = m*x + extra
    extra = (k - m) * x - diff
    if extra <= 0:
        extra = 10
        diff = (k - m) * x - extra
        if diff <= 0:
            return None
    m_word = "เท่าของจำนวนนั้น" if m > 1 else "จำนวนนั้น"
    m_prefix = f"{m} " if m > 1 else ""
    wrong_sub = abs(extra - diff) // (k - m) if abs(extra - diff) % (k - m) == 0 and abs(extra - diff) // (k - m) != x else x - 3
    return mcq(
        stem=(
            f"เมื่อนำ **{diff}** ไปลบออกจาก **{k} เท่าของจำนวนนับจำนวนหนึ่ง** "
            f"จะมีค่าเท่ากับ **{m_prefix}{m_word}บวกกับ {extra}** จำนวนนับนั้นคือข้อใด"
        ),
        correct=str(x),
        wrongs=[
            W(str(wrong_sub), f"ย้าย −{diff} ไปอีกข้างแต่ไม่ได้เปลี่ยนเครื่องหมายเป็นบวก", "sign"),
            W(str((extra + diff) // (k + m) if (extra + diff) % (k + m) == 0 else x + 2),
              f"นำสัมประสิทธิ์ {k}x กับ {m}x มาบวกกันแทนที่จะลบกัน", "sign"),
            W(str((k - m) * x), f"หาค่า {k - m}x = {(k - m) * x} ได้แล้ว แต่ลืมหารด้วย {k - m}", "partial"),
        ],
        hint=f"ให้จำนวนนั้นคือ x จะได้สมการ {k}x − {diff} = {m if m > 1 else ''}x + {extra}",
        steps=[
            f"ให้จำนวนนับนั้นคือ x เขียนเป็นสมการได้: {k}x − {diff} = {m if m > 1 else ''}x + {extra}",
            f"ย้ายข้างจัดรูป: ({k} − {m})x = {extra} + {diff} → {k - m}x = {extra + diff}",
            f"ดังนั้น x = {extra + diff} ÷ {k - m} = {x}",
        ],
    )


@template("m.alg.word_eq", "hard")
def _coins_two_types_equation():
    person = name_th()
    v1, v2 = pick([(2, 5), (5, 10), (1, 5), (1, 10)])
    total_coins = random.randint(20, 45)
    c2 = random.randint(6, total_coins - 6)
    c1 = total_coins - c2
    if c1 == c2:
        c2 += 1
        c1 -= 1
    total_val = v1 * c1 + v2 * c2
    ask = random.choice(["c2", "c1"])
    ans = c2 if ask == "c2" else c1
    other = c1 if ask == "c2" else c2
    target_v = v2 if ask == "c2" else v1
    other_v = v1 if ask == "c2" else v2
    return mcq(
        stem=(
            f"{person}มีเหรียญ **{v1} บาท** และเหรียญ **{v2} บาท** รวมกันทั้งหมด **{total_coins} เหรียญ** "
            f"คิดเป็นเงินรวมกัน **{num(total_val)} บาท** อยากทราบว่า{person}มี **เหรียญ {target_v} บาท** กี่เหรียญ"
        ),
        correct=f"{ans} เหรียญ",
        wrongs=[
            W(f"{other} เหรียญ", f"นี่คือจำนวนเหรียญ {other_v} บาท โจทย์ถามจำนวนเหรียญ {target_v} บาท", "misread"),
            W(f"{ans * target_v} เหรียญ", f"ตอบเป็นมูลค่าเงินของเหรียญ {target_v} บาท ({ans * target_v} บาท) แทนจำนวนเหรียญ", "misread"),
            W(f"{abs(c2 - c1) if abs(c2 - c1) not in (ans, other) else ans + 3} เหรียญ",
              "แก้สมการหาจำนวนเหรียญคลาดเคลื่อนตอนกระจายวงเล็บ", "calc"),
        ],
        hint=f"ให้มีเหรียญ {target_v} บาท จำนวน x เหรียญ จะมีเหรียญ {other_v} บาท จำนวน ({total_coins} − x) เหรียญ แล้วตั้งสมการมูลค่ารวม",
        steps=[
            f"ให้มีเหรียญ {target_v} บาท จำนวน x เหรียญ ดังนั้นมีเหรียญ {other_v} บาท จำนวน {total_coins} − x เหรียญ",
            f"ตั้งสมการมูลค่าเงินรวม: {target_v}x + {other_v}({total_coins} − x) = {num(total_val)}",
            f"กระจายและแก้สมการ ได้ x = {ans} เหรียญ",
        ],
    )


@template("m.alg.word_eq", "challenge")
def _surplus_and_deficit_equation():
    # Classic top-school surplus & deficit problem:
    # Giving a items per child leaves surplus r1; giving b items per child is short by r2.
    # Ask either for number of children OR total number of items!
    a = random.randint(3, 7)
    diff_rate = random.choice([2, 3, 4])
    b = a + diff_rate
    children = random.randint(8, 22)
    r1 = random.randint(3, 14)
    r2 = random.randint(3, 14)
    total_items = a * children + r1
    # Notice: b * children - total_items = (a + diff_rate)*children - (a*children + r1) = diff_rate * children - r1 = r2
    r2 = diff_rate * children - r1
    if r2 <= 0:
        children += 5
        total_items = a * children + r1
        r2 = diff_rate * children - r1
    ask = random.choice(["children", "items"])
    item_noun = pick(["ลูกอม", "ดินสอ", "สมุด", "ขนมปัง", "ส้ม"])
    unit_item = "ผล" if item_noun == "ส้ม" else ("เล่ม" if item_noun == "สมุด" else ("แท่ง" if item_noun == "ดินสอ" else "ชิ้น"))
    wrong_sub_children = abs(r2 - r1) // diff_rate if abs(r2 - r1) % diff_rate == 0 and abs(r2 - r1) // diff_rate > 0 else children - 2
    if ask == "children":
        return mcq(
            stem=(
                f"คุณครูแจก{item_noun}ให้นักเรียนกลุ่มหนึ่ง ถ้าแจกให้คนละ **{a} {unit_item}** จะเหลือ{item_noun}อยู่ **{r1} {unit_item}** "
                f"แต่ถ้าแจกให้คนละ **{b} {unit_item}** จะขาด{item_noun}อีก **{r2} {unit_item}** จึงจะแจกครบทุกคน "
                f"นักเรียนกลุ่มนี้มีทั้งหมดกี่คน"
            ),
            correct=f"{children} คน",
            wrongs=[
                W(f"{total_items} คน", f"{total_items} คือจำนวน{item_noun}ทั้งหมด ไม่ใช่จำนวนนักเรียน", "misread"),
                W(f"{wrong_sub_children} คน",
                  f"นำจำนวนที่เหลือ ({r1}) กับจำนวนที่ขาด ({r2}) มาลบกันแทนที่จะบวกกันตอนย้ายข้างสมการ", "sign"),
                W(f"{r1 + r2} คน", f"หาผลบวก {r1} + {r2} = {r1 + r2} แล้วลืมหารด้วยผลต่างของการแจก ({b} − {a} = {diff_rate})", "partial"),
            ],
            hint=f"ให้นักเรียนมี x คน จำนวน{item_noun}ทั้งหมดเขียนได้ 2 แบบที่เท่ากันคือ {a}x + {r1} = {b}x − {r2}",
            steps=[
                f"ให้นักเรียนมี x คน แจกคนละ {a} {unit_item} เหลือ {r1} {unit_item} แสดงว่ามี{item_noun} = {a}x + {r1} {unit_item}",
                f"แจกคนละ {b} {unit_item} ขาด {r2} {unit_item} แสดงว่ามี{item_noun} = {b}x − {r2} {unit_item}",
                f"ตั้งสมการ: {a}x + {r1} = {b}x − {r2} จะได้ {diff_rate}x = {r1 + r2} ดังนั้นมีนักเรียน x = {children} คน",
            ],
        )
    else:
        wrong_items_sub = a * children - r1
        return mcq(
            stem=(
                f"คุณครูแจก{item_noun}ให้นักเรียนกลุ่มหนึ่ง ถ้าแจกให้คนละ **{a} {unit_item}** จะเหลือ{item_noun} **{r1} {unit_item}** "
                f"แต่ถ้าแจกให้คนละ **{b} {unit_item}** จะขาด{item_noun}อีก **{r2} {unit_item}** "
                f"คุณครูมี{item_noun}ทั้งหมดกี่{unit_item}"
            ),
            correct=f"{total_items} {unit_item}",
            wrongs=[
                W(f"{children} {unit_item}", f"{children} คือจำนวนนักเรียน (คน) ยังไม่ได้แทนค่าเพื่อหาจำนวน{item_noun}", "partial"),
                W(f"{wrong_items_sub} {unit_item}", f"แทนค่าหาจำนวน{item_noun}โดยนำ {a}({children}) − {r1} แทนที่จะบวกด้วย {r1}", "sign"),
                W(f"{a * wrong_sub_children + r1 if a * wrong_sub_children + r1 != total_items else total_items - a} {unit_item}",
                  "ย้ายข้างสมการหาจำนวนนักเรียนผิดเครื่องหมายก่อนนำมาคำนวณจำนวนของ", "calc"),
            ],
            hint=f"ให้นักเรียนมี x คน ตั้งสมการ {a}x + {r1} = {b}x − {r2} เพื่อหาจำนวนนักเรียนก่อน แล้วแทนค่าหาจำนวน{item_noun}",
            steps=[
                f"ให้นักเรียนมี x คน ตั้งสมการจำนวน{item_noun}เท่ากัน: {a}x + {r1} = {b}x − {r2}",
                f"แก้สมการได้ {diff_rate}x = {r1 + r2} ดังนั้นมีนักเรียน x = {children} คน",
                f"มี{item_noun}ทั้งหมด = ({a} × {children}) + {r1} = {total_items} {unit_item}",
            ],
        )
