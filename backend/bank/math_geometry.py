"""Geometry question bank for topic m.geo (เรขาคณิต)."""

import math
import random

from backend.bank import svg
from backend.bank.core import W, mcq, num, pick, skill, template


def _arrow_parallel(p, q, count=1):
    """Draw small arrow chevron(s) on segment pq to indicate parallel lines."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    nx, ny = -uy, ux
    out = []
    for i in range(count):
        off = (i - (count - 1) / 2) * 6
        cx, cy = mx + ux * off, my + uy * off
        p1 = (cx - ux * 5 + nx * 4, cy - uy * 5 + ny * 4)
        p2 = (cx + ux * 2, cy + uy * 2)
        p3 = (cx - ux * 5 - nx * 4, cy - uy * 5 - ny * 4)
        out.append(svg.polyline([p1, p2, p3], cls="fig-mark"))
    return "".join(out)


# ===========================================================================
# Skill 1: m.geo.line_angles — มุมบนเส้นตรง มุมรอบจุด และมุมตรงข้าม
# ===========================================================================
skill(
    "m.geo.line_angles",
    "m.geo",
    "มุมบนเส้นตรง มุมรอบจุด และมุมตรงข้าม",
    lesson={
        "concept": (
            "มุมบนเส้นตรงเดียวกันรวมกันได้ 180° มุมรอบจุดศูนย์กลางรวมกันได้ 360° "
            "และเมื่อเส้นตรงสองเส้นตัดกัน มุมตรงข้ามจะมีขนาดเท่ากันเสมอ"
        ),
        "steps": [
            "สังเกตว่ามุมที่กำหนดให้อยู่บนเส้นตรงเดียวกัน (รวม 180°) รอบจุดเดียวกัน (รวม 360°) หรือเป็นมุมตรงข้าม",
            "ตั้งสมการจากความสัมพันธ์ของมุม",
            "แก้สมการหาค่ามุมหรือค่าตัวแปรที่โจทย์ถาม",
        ],
        "example": {
            "q": "เส้นตรง AB มีจุด O อยู่บนเส้นตรง ถ้ามีรังสี OC และ OD แบ่งมุมด้านหนึ่งออกเป็น 3 มุม ขนาด 45°, x° และ 65° จงหาค่า x",
            "steps": [
                "มุมบนเส้นตรงเดียวกันรวมกันได้ 180°",
                "จะได้ 45 + x + 65 = 180",
                "x = 180 − 110 = 70°",
            ],
            "a": "70°",
        },
        "mistakes": [
            "จำสับสนระหว่างมุมบนเส้นตรง (180°) กับมุมฉาก (90°) หรือมุมรอบจุด (360°)",
            "เมื่อโจทย์ให้มุมในรูปตัวแปร เช่น 2x + 10 หาค่า x ได้แล้วลืมแทนค่ากลับเพื่อหามุมที่โจทย์ถาม",
        ],
        "tips": [
            "ถ้ามีสัญลักษณ์สี่เหลี่ยมเล็กที่มุม แปลว่ามุมนั้นมีขนาด 90° ทันที",
            "เส้นตรงสองเส้นตัดกัน มุมประชิดรวมได้ 180° ส่วนมุมตรงข้ามเท่ากัน",
        ],
    },
    weight=1.2,
)


@template("m.geo.line_angles", "easy")
def _angles_on_straight_line():
    a = random.randint(32, 78)
    b = random.randint(32, 78)
    x = 180 - a - b
    if x <= 20:
        return None
    o = (130, 115)
    p_left, p_right = (25, 115), (235, 115)
    p1 = (130 - 80 * math.cos(math.radians(52)), 115 - 80 * math.sin(math.radians(52)))
    p2 = (130 + 80 * math.cos(math.radians(56)), 115 - 80 * math.sin(math.radians(56)))
    fig = svg.canvas(260, 145, [
        svg.line(p_left, p_right),
        svg.line(o, p1),
        svg.line(o, p2),
        svg.dot(o, 3),
        svg.point_label(p_left, "A", dy=16),
        svg.point_label(o, "O", dy=16),
        svg.point_label(p_right, "B", dy=16),
        svg.point_label(p1, "C", dx=-8, dy=-6),
        svg.point_label(p2, "D", dx=8, dy=-6),
        svg.angle_arc(o, p_left, p1, f"{a}°", r=26),
        svg.angle_arc(o, p1, p2, "x°", r=32),
        svg.angle_arc(o, p2, p_right, f"{b}°", r=26),
    ])
    return mcq(
        stem="จากรูป AOB เป็นเส้นตรง จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{x}°",
        wrongs=[
            W(f"{360 - a - b}°", "ใช้ผลรวมมุมรอบจุด 360° แทนที่จะเป็นมุมบนเส้นตรง 180°", "concept"),
            W(f"{a + b}°", "นำมุมที่กำหนดให้มาบวกกันแล้วตอบเลย ลืมนำไปลบออกจาก 180°", "partial"),
            W(f"{abs(90 - (a + b)) or 15}°", "ใช้ 90° แทนที่จะใช้มุมตรง 180°", "concept"),
            W(f"{x + 10}°", "ลบเลขหลักสิบผิดพลาด", "calc"),
        ],
        hint="มุมที่อยู่บนข้างเดียวกันของเส้นตรง AOB รวมกันได้ 180°",
        steps=[
            "มุมบนเส้นตรง AOB รวมกันได้ 180°",
            f"จะได้ {a}° + x° + {b}° = 180°",
            f"x = 180 − ({a} + {b}) = 180 − {a + b} = {x}°",
        ],
    )


@template("m.geo.line_angles", "medium")
def _vertically_opposite_algebra():
    k = random.choice([2, 3, 4])
    x = random.randint(18, 36)
    c = random.randint(8, 28)
    ang = k * x + c
    if ang >= 160 or ang <= 45:
        return None
    supp = 180 - ang
    ask_supp = random.choice([True, False])
    o = (130, 75)
    p_a, p_b = (30, 120), (230, 30)
    p_c, p_d = (30, 30), (230, 120)
    fig = svg.canvas(260, 150, [
        svg.line(p_a, p_b),
        svg.line(p_c, p_d),
        svg.dot(o, 3),
        svg.point_label(p_a, "A", dx=-10, dy=4),
        svg.point_label(p_b, "B", dx=10, dy=-2),
        svg.point_label(p_c, "C", dx=-10, dy=-2),
        svg.point_label(p_d, "D", dx=10, dy=4),
        svg.point_label(o, "O", dy=-18),
        svg.angle_arc(o, p_a, p_c, f"{ang}°", r=28),
        svg.angle_arc(o, p_b, p_d, r=28),
        svg.label((164, 75), f"({k}x+{c})°", size=12, anchor="start", cls="fig-dim"),
        svg.angle_arc(o, p_a, p_d, "y°", r=24) if ask_supp else "",
    ])
    if ask_supp:
        ans = x + supp
        return mcq(
            stem=f"จากรูป เส้นตรง AB ตัดกับ CD ที่จุด O จงหาค่าของ x + y (รูปไม่ได้วาดตามสัดส่วน)",
            figure=fig,
            correct=str(ans),
            wrongs=[
                W(str(x + ang), "คิดว่ามุมประชิด y เท่ากับมุมตรงข้าม แทนที่จะรวมกันได้ 180°", "concept"),
                W(str(x), "ตอบเฉพาะค่า x ลืมบวกค่า y ตามที่โจทย์ถาม", "partial"),
                W(str((ang + c) // k + supp), f"แก้สมการหา x ผิดโดยนำ {c} ไปบวกแทนที่จะลบ", "sign"),
                W(str(supp), "ตอบเฉพาะค่า y ลืมบวกค่า x", "partial"),
            ],
            hint="หามุมตรงข้ามเพื่อแก้สมการหา x และใช้มุมประชิดบนเส้นตรงรวมกันได้ 180° เพื่อหา y",
            steps=[
                f"มุมตรงข้ามมีขนาดเท่ากัน จะได้ {k}x + {c} = {ang}",
                f"{k}x = {ang - c} ดังนั้น x = {x}",
                f"มุม y เป็นมุมประชิดบนเส้นตรงเดียวกับมุม {ang}° ดังนั้น y = 180 − {ang} = {supp}",
                f"ดังนั้น x + y = {x} + {supp} = {ans}",
            ],
        )
    return mcq(
        stem="จากรูป เส้นตรง AB ตัดกับเส้นตรง CD ที่จุด O จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=str(x),
        wrongs=[
            W(str((ang + c) // k if (ang + c) % k == 0 else x + 6), f"ย้ายข้างสมการผิดโดยนำ {c} ไปบวกกับ {ang}", "sign"),
            W(str(180 - ang), "นำมุมไปลบจาก 180° เพราะสับสนกับมุมประชิดบนเส้นตรง", "concept"),
            W(str(ang - c), f"ลบ {c} แล้วลืมหารด้วย {k}", "partial"),
            W(str(x + 4), "คำนวณการหารผิดพลาด", "calc"),
        ],
        hint="เส้นตรงสองเส้นตัดกัน มุมตรงข้ามย่อมมีขนาดเท่ากัน",
        steps=[
            "เนื่องจากมุม AOC และมุม BOD เป็นมุมตรงข้าม จึงมีขนาดเท่ากัน",
            f"ตั้งสมการ: {k}x + {c} = {ang}",
            f"{k}x = {ang} − {c} = {ang - c}",
            f"x = {ang - c} ÷ {k} = {x}",
        ],
    )


@template("m.geo.line_angles", "hard")
def _angles_around_point_ratio():
    a = random.randint(100, 145)
    rem = 360 - 90 - a
    r1, r2 = pick([(1, 2), (2, 3), (1, 3), (3, 5), (1, 4)])
    if rem % (r1 + r2) != 0:
        a = 270 - (rem // (r1 + r2)) * (r1 + r2)
        rem = 270 - a
    if a < 95 or a > 155:
        return None
    unit_deg = rem // (r1 + r2)
    ang_x = r1 * unit_deg
    ang_y = r2 * unit_deg
    o = (130, 85)
    p_up = (130, 15)
    p_right = (215, 85)
    p_down = (165, 155)
    p_left = (45, 115)
    fig = svg.canvas(260, 175, [
        svg.line(o, p_up),
        svg.line(o, p_right),
        svg.line(o, p_down),
        svg.line(o, p_left),
        svg.right_angle(o, p_up, p_right, size=11),
        svg.angle_arc(o, p_right, p_down, "x°", r=24),
        svg.angle_arc(o, p_down, p_left, "y°", r=28),
        svg.angle_arc(o, p_left, p_up, f"{a}°", r=26),
        svg.dot(o, 3),
    ])
    ask_diff = random.choice([True, False])
    if ask_diff:
        ans = ang_y - ang_x
        stem = f"จากรูป มุมรอบจุดมีอัตราส่วน x : y = {r1} : {r2} จงหาว่ามุม y มีขนาดมากกว่ามุม x กี่องศา (รูปไม่ได้วาดตามสัดส่วน)"
        w1 = W(f"{ang_y}°", "ตอบขนาดของมุม y แทนที่จะตอบผลต่าง y − x", "misread")
        w2 = W(f"{ang_x}°", "ตอบขนาดของมุม x แทนที่จะตอบผลต่าง y − x", "misread")
        w3 = W(f"{rem}°", "ตอบผลรวม x + y แทนที่จะตอบผลต่าง", "partial")
        last_step = f"ดังนั้น y − x = {ang_y}° − {ang_x}° = {ans}°"
    else:
        ans = ang_y
        stem = f"จากรูป มุมรอบจุดมีอัตราส่วน x : y = {r1} : {r2} จงหาขนาดของมุม y (รูปไม่ได้วาดตามสัดส่วน)"
        w1 = W(f"{ang_x}°", "ตอบขนาดของมุม x แทนที่จะเป็นมุม y", "misread")
        w2 = W(f"{rem}°", "หาผลรวม x + y ได้แล้วแต่ยังไม่ได้แบ่งตามอัตราส่วน", "partial")
        w3 = W(f"{(360 - a) * r2 // (r1 + r2)}°", "ลืมหักมุมฉาก 90° ออกจาก 360°", "misread")
        last_step = f"ดังนั้น มุม y = {r2} × {unit_deg}° = {ang_y}°"
    return mcq(
        stem=stem,
        figure=fig,
        correct=f"{ans}°",
        wrongs=[w1, w2, w3, W(f"{ans + unit_deg}°", "คำนวณสัดส่วนของมุมผิดไป 1 ส่วน", "calc")],
        hint="มุมรอบจุดรวมกันได้ 360° และสัญลักษณ์มุมฉากคือ 90°",
        steps=[
            "มุมรอบจุดรวมกันได้ 360°",
            f"จะได้ x + y = 360° − 90° − {a}° = {rem}°",
            f"แบ่ง {rem}° ออกเป็น {r1} + {r2} = {r1 + r2} ส่วน ส่วนละ {rem} ÷ {r1 + r2} = {unit_deg}°",
            f"จะได้ x = {ang_x}° และ y = {ang_y}°",
            last_step,
        ],
    )


# ===========================================================================
# Skill 2: m.geo.parallel — เส้นขนานและเส้นตัดขวาง
# ===========================================================================
skill(
    "m.geo.parallel",
    "m.geo",
    "เส้นขนานและเส้นตัดขวาง",
    lesson={
        "concept": (
            "เมื่อเส้นตรงเส้นหนึ่งตัดเส้นขนานคู่หนึ่ง จะเกิด (1) มุมแย้งมีขนาดเท่ากัน (รูปตัว Z) "
            "(2) มุมภายนอกและมุมภายในที่อยู่ตรงข้ามบนข้างเดียวกันของเส้นตัดมีขนาดเท่ากัน (รูปตัว F) "
            "และ (3) มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัดรวมกันได้ 180° (รูปตัว C หรือ U)"
        ),
        "steps": [
            "หาคู่เส้นขนานและเส้นตัดขวางในรูป",
            "ระบุความสัมพันธ์ของมุมว่าเป็นมุมแย้ง (Z) มุมสมนัย (F) หรือมุมภายในข้างเดียวกัน (C)",
            "หากมีจุดหักมุมระหว่างเส้นขนาน ให้ลากเส้นช่วยขนานกับเส้นเดิมผ่านจุดยอดมุม",
        ],
        "example": {
            "q": "เส้นขนานคู่หนึ่งมีเส้นตัดทำมุมภายในข้างหนึ่ง 65° มุมภายในที่อยู่ข้างเดียวกันของเส้นตัดอีกมุมมีขนาดเท่าใด",
            "steps": [
                "มุมภายในข้างเดียวกันของเส้นตัดรวมกันได้ 180°",
                "ขนาดของมุมที่ต้องการ = 180° − 65° = 115°",
            ],
            "a": "115°",
        },
        "mistakes": [
            "คิดว่ามุมภายในข้างเดียวกันของเส้นตัดมีขนาดเท่ากัน (จริง ๆ ต้องรวมกันได้ 180°)",
            "เจอรูปเส้นหยัก (ตัว M หรือซิกแซก) แล้วนำมุมมาลบกันแทนที่จะบวกกัน",
        ],
        "tips": [
            "เทคนิครูปตัว M (มุมหยักระหว่างเส้นขนาน): มุมแหลมที่ชี้ไปทางซ้ายรวมกัน = มุมแหลมที่ชี้ไปทางขวารวมกัน",
        ],
    },
    weight=1.6,
)


@template("m.geo.parallel", "easy")
def _parallel_transversal_basic():
    ang = random.randint(42, 138)
    if abs(ang - 90) < 8:
        ang += 12
    supp = 180 - ang
    mode = random.choice(["alt", "co_int"])
    p1, q1 = (25, 45), (235, 45)
    p2, q2 = (25, 125), (235, 125)
    t_top, t_bot = (165, 15), (95, 155)
    # intersections at y=45 and y=125 along line from (165,15) to (95,155)
    # x(y) = 165 - (y-15)*70/140 = 165 - 0.5*(y-15)
    u = (150, 45)
    v = (110, 125)
    parts = [
        svg.line(p1, q1),
        svg.line(p2, q2),
        svg.line(t_top, t_bot),
        _arrow_parallel((55, 45), (85, 45), 1),
        _arrow_parallel((55, 125), (85, 125), 1),
        svg.point_label(p1, "A", dx=-10),
        svg.point_label(q1, "B", dx=10),
        svg.point_label(p2, "C", dx=-10),
        svg.point_label(q2, "D", dx=10),
        svg.angle_arc(u, p1, v, f"{ang}°", r=26),
    ]
    if mode == "alt":
        parts.append(svg.angle_arc(v, u, q2, "x°", r=26))
        ans = ang
        wrong_main = W(f"{supp}°", "นำ 180° ไปลบ เพราะสับสนมุมแย้งกับมุมภายในข้างเดียวกัน", "concept")
        steps = [
            "เนื่องจาก AB ขนานกับ CD มุมแย้งภายในจะมีขนาดเท่ากัน",
            f"ดังนั้น x = {ang}°",
        ]
        hint = "สังเกตมุมรูปตัว Z (มุมแย้งภายใน)"
    else:
        parts.append(svg.angle_arc(v, u, p2, "x°", r=26))
        ans = supp
        wrong_main = W(f"{ang}°", "ตอบเท่ากับมุมที่โจทย์ให้มา เพราะสับสนมุมภายในข้างเดียวกันกับมุมแย้ง", "concept")
        steps = [
            "เนื่องจาก AB ขนานกับ CD มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัดรวมกันได้ 180°",
            f"จะได้ {ang}° + x° = 180°",
            f"ดังนั้น x = 180° − {ang}° = {supp}°",
        ]
        hint = "มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัด (รูปตัว C) รวมกันได้ 180°"
    fig = svg.canvas(265, 165, parts)
    return mcq(
        stem="จากรูป เส้นตรง AB ขนานกับเส้นตรง CD จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{ans}°",
        wrongs=[
            wrong_main,
            W(f"{abs(90 - ang) + 20}°", "ใช้ความสัมพันธ์ของมุมผิด", "concept"),
            W(f"{ans + 10}°", "ลบเลขผิดพลาด", "calc"),
            W(f"{ans - 10}°", "ลบเลขผิดพลาด", "calc"),
        ],
        hint=hint,
        steps=steps,
    )


@template("m.geo.parallel", "medium")
def _parallel_zigzag_m():
    a = random.randint(25, 62)
    b = random.randint(28, 65)
    m_ang = a + b
    ask_vertex = random.choice([True, False])
    p1, q1 = (25, 35), (235, 35)
    p2, q2 = (25, 145), (235, 145)
    u = (75, 35)
    m = (155, 90)
    v = (85, 145)
    fig = svg.canvas(260, 175, [
        svg.line(p1, q1),
        svg.line(p2, q2),
        svg.polyline([u, m, v]),
        _arrow_parallel((185, 35), (215, 35), 1),
        _arrow_parallel((185, 145), (215, 145), 1),
        svg.point_label(p1, "A", dx=-10),
        svg.point_label(q1, "B", dx=10),
        svg.point_label(p2, "C", dx=-10),
        svg.point_label(q2, "D", dx=10),
        svg.point_label(m, "P", dx=12),
        svg.angle_arc(u, m, q1, f"{a}°", r=28),
        svg.angle_arc(m, u, v, "x°" if ask_vertex else f"{m_ang}°", r=24),
        svg.angle_arc(v, m, q2, f"{b}°" if ask_vertex else "x°", r=28),
    ])
    if ask_vertex:
        return mcq(
            stem="จากรูป AB ขนานกับ CD จงหาขนาดของมุม x ที่จุด P (รูปไม่ได้วาดตามสัดส่วน)",
            figure=fig,
            correct=f"{m_ang}°",
            wrongs=[
                W(f"{180 - m_ang}°", "นำผลบวกไปลบออกจาก 180° โดยไม่จำเป็น", "concept"),
                W(f"{abs(a - b) or 15}°", "นำมุมทั้งสองมาลบกันแทนที่จะบวกกัน", "sign"),
                W(f"{m_ang + 10}°", "บวกเลขผิดพลาด", "calc"),
            ],
            hint="ลากเส้นตรงผ่านจุด P ให้ขนานกับ AB และ CD แล้วใช้สมบัติมุมแย้ง",
            steps=[
                "ลากเส้นตรงผ่านจุด P ให้ขนานกับ AB และ CD",
                f"มุม x ถูกแบ่งเป็น 2 ส่วน ซึ่งแย้งกับมุม {a}° และมุม {b}° ตามลำดับ",
                f"ดังนั้น x = {a}° + {b}° = {m_ang}°",
            ],
        )
    return mcq(
        stem=f"จากรูป AB ขนานกับ CD และมุมที่จุด P มีขนาด {m_ang}° จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{b}°",
        wrongs=[
            W(f"{m_ang + a}°", f"นำ {m_ang}° ไปบวกกับ {a}° แทนที่จะลบออก", "sign"),
            W(f"{180 - m_ang}°", f"นำ {m_ang}° ไปลบออกจาก 180°", "concept"),
            W(f"{a}°", "คิดว่ามุมด้านล่างต้องเท่ากับมุมด้านบนเสมอ", "concept"),
        ],
        hint="มุมแหลมที่จุด P เท่ากับผลบวกของมุมแหลมทั้งสองที่เส้นขนาน",
        steps=[
            "ลากเส้นตรงผ่านจุด P ให้ขนานกับ AB และ CD จะได้มุมที่จุด P เท่ากับผลบวกของมุมแย้งทั้งสอง",
            f"จะได้ {a}° + x° = {m_ang}°",
            f"ดังนั้น x = {m_ang}° − {a}° = {b}°",
        ],
    )


@template("m.geo.parallel", "hard")
def _parallel_reflex_zigzag():
    a = random.randint(115, 150)
    b = random.randint(110, 148)
    # Two interior reflex-side bends (pencil / bullet shape between parallel lines):
    # A + P + C = 360° => P = 360 - a - b, OR obtuse angles facing left sum to 360°
    p_ang = (180 - a) + (180 - b)
    obtuse_p = 360 - p_ang  # if measured on the wide side, or acute p_ang
    p1, q1 = (25, 35), (235, 35)
    p2, q2 = (25, 145), (235, 145)
    u = (110, 35)
    m = (65, 90)
    v = (115, 145)
    fig = svg.canvas(260, 175, [
        svg.line(p1, q1),
        svg.line(p2, q2),
        svg.polyline([u, m, v]),
        _arrow_parallel((185, 35), (215, 35), 1),
        _arrow_parallel((185, 145), (215, 145), 1),
        svg.point_label(p1, "A", dx=-10),
        svg.point_label(q1, "B", dx=10),
        svg.point_label(p2, "C", dx=-10),
        svg.point_label(q2, "D", dx=10),
        svg.point_label(m, "E", dx=-14),
        svg.angle_arc(u, m, q1, f"{a}°", r=24),
        svg.angle_arc(m, u, v, "x°", r=24),
        svg.angle_arc(v, m, q2, f"{b}°", r=24),
    ])
    return mcq(
        stem="จากรูป AB ขนานกับ CD จงหาค่าของ x ที่จุด E (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{p_ang}°",
        wrongs=[
            W(f"{a + b - 180}°", "นำมุมป้านสองมุมบวกกันแล้วลบ 180° ซึ่งสลับทิศทางของมุม", "formula"),
            W(f"{180 - p_ang}°", "หาค่ามุม x ได้แล้วเผลอนำไปลบออกจาก 180°", "concept"),
            W(f"{360 - a}°", "ใช้เพียงมุมด้านบนมุมเดียวในการคำนวณ", "partial"),
            W(f"{p_ang + 10}°", "ลบเลขจาก 360° ผิดพลาด", "calc"),
        ],
        hint="ลากเส้นขนานผ่านจุด E จะเกิดมุมภายในข้างเดียวกันของเส้นตัด 2 คู่ (รวมคู่ละ 180°)",
        steps=[
            "ลากเส้นตรงผ่านจุด E ไปทางขวาให้ขนานกับ AB และ CD",
            f"มุมส่วนบนที่จุด E = 180° − {a}° = {180 - a}° (มุมภายในข้างเดียวกัน)",
            f"มุมส่วนล่างที่จุด E = 180° − {b}° = {180 - b}° (มุมภายในข้างเดียวกัน)",
            f"ดังนั้น x = {180 - a}° + {180 - b}° = {p_ang}°",
        ],
    )


# ===========================================================================
# Skill 3: m.geo.tri_angles — มุมภายในและมุมภายนอกของรูปสามเหลี่ยมและสี่เหลี่ยม
# ===========================================================================
skill(
    "m.geo.tri_angles",
    "m.geo",
    "มุมภายในและมุมภายนอกของรูปสามเหลี่ยมและสี่เหลี่ยม",
    lesson={
        "concept": (
            "ผลรวมมุมภายในของรูปสามเหลี่ยมเท่ากับ 180° และของรูปสี่เหลี่ยมเท่ากับ 360° "
            "นอกจากนี้ มุมภายนอกของรูปสามเหลี่ยมที่เกิดจากการต่อด้านออกไป จะมีขนาดเท่ากับผลบวกของมุมภายในที่ไม่ใช่มุมประชิด"
        ),
        "steps": [
            "ดูว่ารูปที่กำหนดเป็นสามเหลี่ยม (รวม 180°) หรือสี่เหลี่ยม (รวม 360°)",
            "หากมีเส้นต่อออกไปเป็นมุมภายนอก ใช้สมบัติ มุมภายนอก = ผลบวกของมุมภายในที่อยู่ไกลออกไปสองมุม",
            "แก้สมการหาขนาดของมุมที่ต้องการ",
        ],
        "example": {
            "q": "สามเหลี่ยม ABC มีมุม A = 50° และมุม B = 65° ถ้าต่อด้าน BC ออกไปทาง C ถึงจุด D มุมภายนอก ACD มีขนาดเท่าใด",
            "steps": [
                "มุมภายนอกของรูปสามเหลี่ยม = ผลบวกของมุมภายในที่ไม่ใช่มุมประชิด",
                "มุม ACD = มุม A + มุม B = 50° + 65° = 115°",
            ],
            "a": "115°",
        },
        "mistakes": [
            "ใช้มุมภายนอกเท่ากับมุมภายในที่อยู่ติดกัน (จริง ๆ มุมที่ติดกันรวมกันได้ 180°)",
            "ลืมว่าผลรวมมุมภายในสี่เหลี่ยมคือ 360° ไม่ใช่ 180°",
        ],
        "tips": [
            "สมบัติมุมภายนอกช่วยลดขั้นตอน ไม่ต้องหามุมภายในที่เหลือแล้วลบจาก 180° ซ้ำอีกครั้ง",
        ],
    },
    weight=1.5,
)


@template("m.geo.tri_angles", "easy")
def _triangle_exterior_angle():
    a = random.randint(38, 78)
    b = random.randint(42, 78)
    ext = a + b
    c_int = 180 - ext
    if c_int < 25:
        return None
    ask_ext = random.choice([True, False])
    pa, pb, pc, pd = (95, 25), (30, 130), (175, 130), (240, 130)
    fig = svg.canvas(265, 155, [
        svg.polygon([pa, pb, pc]),
        svg.line(pc, pd),
        svg.point_label(pa, "A", dy=-10),
        svg.point_label(pb, "B", dx=-10, dy=6),
        svg.point_label(pc, "C", dy=16),
        svg.point_label(pd, "D", dy=16),
        svg.angle_arc(pa, pb, pc, f"{a}°" if ask_ext else "x°", r=24),
        svg.angle_arc(pb, pa, pc, f"{b}°", r=24),
        svg.angle_arc(pc, pa, pd, "x°" if ask_ext else f"{ext}°", r=26),
    ])
    if ask_ext:
        return mcq(
            stem="จากรูป ส่วนของเส้นตรง BCD เป็นเส้นตรง จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
            figure=fig,
            correct=f"{ext}°",
            wrongs=[
                W(f"{c_int}°", "หามุมภายใน ACB แทนที่จะตอบมุมภายนอก x", "misread"),
                W(f"{180 - a}°", f"นำมุม {a}° มุมเดียวไปลบออกจาก 180°", "partial"),
                W(f"{abs(a - b) + 90}°", "ใช้ความสัมพันธ์ของมุมภายนอกผิด", "formula"),
            ],
            hint="มุมภายนอกของรูปสามเหลี่ยมเท่ากับผลบวกของมุมภายในสองมุมที่ไม่ใช่มุมประชิด",
            steps=[
                "จากสมบัติมุมภายนอกของรูปสามเหลี่ยม ABC",
                f"จะได้ x = มุม A + มุม B = {a}° + {b}° = {ext}°",
            ],
        )
    return mcq(
        stem="จากรูป ส่วนของเส้นตรง BCD เป็นเส้นตรง จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{a}°",
        wrongs=[
            W(f"{180 - ext}°", f"หาขนาดของมุมภายใน ACB (180° − {ext}°) แล้วตอบเลยโดยยังไม่ได้หามุม x", "partial"),
            W(f"{ext + b}°", f"นำ {ext}° ไปบวกกับ {b}° แทนที่จะลบออก", "sign"),
            W(f"{180 - b}°", f"นำ 180° ลบด้วย {b}° เพียงมุมเดียว", "partial"),
        ],
        hint="มุมภายนอก ACD มีขนาดเท่ากับผลบวกของมุม A และมุม B",
        steps=[
            "จากสมบัติมุมภายนอกของรูปสามเหลี่ยม: มุม ACD = มุม A + มุม B",
            f"จะได้ {ext}° = x° + {b}°",
            f"ดังนั้น x = {ext}° − {b}° = {a}°",
        ],
    )


@template("m.geo.tri_angles", "medium")
def _quadrilateral_angles():
    a = random.randint(65, 105)
    b = random.randint(75, 115)
    c = random.randint(60, 100)
    d = 360 - (a + b + c)
    if d < 50 or d > 140:
        return None
    pa, pb, pc, pd = (45, 35), (30, 130), (195, 135), (215, 45)
    fig = svg.canvas(250, 160, [
        svg.polygon([pa, pb, pc, pd]),
        svg.point_label(pa, "A", dx=-10, dy=-6),
        svg.point_label(pb, "B", dx=-10, dy=8),
        svg.point_label(pc, "C", dx=10, dy=8),
        svg.point_label(pd, "D", dx=10, dy=-6),
        svg.angle_arc(pa, pb, pd, f"{a}°", r=22),
        svg.angle_arc(pb, pa, pc, f"{b}°", r=22),
        svg.angle_arc(pc, pb, pd, f"{c}°", r=22),
        svg.angle_arc(pd, pa, pc, "x°", r=22),
    ])
    return mcq(
        stem="จากรูปสี่เหลี่ยม ABCD จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{d}°",
        wrongs=[
            W(f"{abs(180 - d)}°", "คำนวณผลรวมมุมผิดหรือเผลอไปเทียบกับ 180°", "concept"),
            W(f"{a + b + c}°", "ตอบผลบวกของสามมุมที่กำหนดให้ ลืมนำไปลบออกจาก 360°", "partial"),
            W(f"{d + 10}°", "ลบเลขจาก 360° ผิดในหลักสิบ", "calc"),
            W(f"{d - 10}°", "ลบเลขจาก 360° ผิดในหลักสิบ", "calc"),
        ],
        hint="มุมภายในของรูปสี่เหลี่ยมรวมกันได้ 360°",
        steps=[
            "ผลรวมของมุมภายในของรูปสี่เหลี่ยมเท่ากับ 360°",
            f"ผลบวกของ 3 มุมที่ทราบค่า = {a}° + {b}° + {c}° = {a + b + c}°",
            f"ดังนั้น x = 360° − {a + b + c}° = {d}°",
        ],
    )


@template("m.geo.tri_angles", "hard")
def _crossed_triangles_bowtie():
    a = random.randint(35, 70)
    b = random.randint(35, 70)
    c = random.randint(30, 65)
    # In bowtie AB and CD intersecting at O: a + b = c + x => x = a + b - c
    x = a + b - c
    if x < 25 or x > 85 or x == a or x == b:
        return None
    o = (130, 80)
    pa, pb = (35, 25), (35, 135)
    pc, pd = (225, 25), (225, 135)
    fig = svg.canvas(260, 160, [
        svg.polygon([pa, pb, o]),
        svg.polygon([pc, pd, o]),
        svg.point_label(pa, "A", dx=-12, dy=-2),
        svg.point_label(pb, "B", dx=-12, dy=4),
        svg.point_label(pc, "C", dx=12, dy=-2),
        svg.point_label(pd, "D", dx=12, dy=4),
        svg.point_label(o, "O", dy=-18),
        svg.angle_arc(pa, pb, o, f"{a}°", r=24),
        svg.angle_arc(pb, pa, o, f"{b}°", r=24),
        svg.angle_arc(pc, pd, o, f"{c}°", r=24),
        svg.angle_arc(pd, pc, o, "x°", r=24),
    ])
    return mcq(
        stem="จากรูป ส่วนของเส้นตรง AD และ BC ตัดกันที่จุด O จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{x}°",
        wrongs=[
            W(f"{180 - (a + b)}°", "หาขนาดของมุม AOB แล้วตอบเลย ลืมคำนวณต่อในรูปสามเหลี่ยม COD", "partial"),
            W(f"{a + b + c - 90 if a + b + c > 90 else 45}°", "นำมุมไปบวกลบผิดความสัมพันธ์", "concept"),
            W(f"{180 - c - a}°", "สมมติว่าด้านขนานกันและจับมุมแย้งเท่ากัน ทั้งที่โจทย์ไม่ได้กำหนดว่าขนานกัน", "trap"),
            W(f"{x + 10}°", "บวกลบเลขผิดพลาด", "calc"),
        ],
        hint="มุม AOB กับมุม COD เป็นมุมตรงข้ามจึงมีขนาดเท่ากัน ดังนั้น มุม A + มุม B = มุม C + มุม D",
        steps=[
            f"ในสามเหลี่ยม AOB: มุม AOB = 180° − ({a}° + {b}°) = {180 - a - b}°",
            f"เนื่องจากมุม COD เป็นมุมตรงข้ามกับมุม AOB จึงมีขนาด {180 - a - b}° เท่ากัน",
            f"ในสามเหลี่ยม COD: x = 180° − ({180 - a - b}° + {c}°) = {a + b}° − {c}° = {x}°",
        ],
    )


# ===========================================================================
# Skill 4: m.geo.iso_equi — รูปสามเหลี่ยมหน้าจั่วและสามเหลี่ยมด้านเท่า
# ===========================================================================
skill(
    "m.geo.iso_equi",
    "m.geo",
    "รูปสามเหลี่ยมหน้าจั่วและสามเหลี่ยมด้านเท่า",
    lesson={
        "concept": (
            "สามเหลี่ยมหน้าจั่วมีด้านยาวเท่ากัน 2 ด้าน และมุมที่ฐานซึ่งอยู่ตรงข้ามด้านที่เท่ากันจะมีขนาดเท่ากัน "
            "ส่วนสามเหลี่ยมด้านเท่ามีด้านยาวเท่ากันทั้ง 3 ด้าน และมุมภายในทุกมุมมีขนาด 60° เท่ากัน"
        ),
        "steps": [
            "ดูขีดสัญลักษณ์ด้านที่ยาวเท่ากัน เพื่อระบุว่ามุมคู่ใดเป็นมุมที่ฐานที่เท่ากัน",
            "ถ้าทราบมุมยอด: มุมที่ฐานแต่ละมุม = (180° − มุมยอด) ÷ 2",
            "ถ้าทราบมุมที่ฐาน: มุมยอด = 180° − 2 × มุมที่ฐาน",
        ],
        "example": {
            "q": "สามเหลี่ยมหน้าจั่ว ABC มี AB = AC และมุมยอด A = 40° มุมที่ฐาน B มีขนาดเท่าใด",
            "steps": [
                "เนื่องจาก AB = AC ดังนั้น มุม B = มุม C",
                "มุม B = (180° − 40°) ÷ 2 = 140° ÷ 2 = 70°",
            ],
            "a": "70°",
        },
        "mistakes": [
            "ลบมุมยอดออกจาก 180° แล้วลืมหารด้วย 2",
            "ดูขีดด้านเท่ากันไม่ตรงคู่ ทำให้ระบุมุมยอดและมุมที่ฐานสลับกัน",
        ],
        "tips": [
            "มุมที่อยู่ตรงข้ามด้านที่ยาวเท่ากัน จะมีขนาดเท่ากันเสมอ",
        ],
    },
    weight=1.4,
)


@template("m.geo.iso_equi", "easy")
def _isosceles_basic():
    base_ang = random.randint(35, 76)
    apex_ang = 180 - 2 * base_ang
    given_apex = random.choice([True, False])
    pa, pb, pc = (120, 20), (40, 140), (200, 140)
    fig = svg.canvas(240, 165, [
        svg.polygon([pa, pb, pc]),
        svg.tick(pa, pb, 1),
        svg.tick(pa, pc, 1),
        svg.point_label(pa, "A", dy=-10),
        svg.point_label(pb, "B", dx=-12, dy=4),
        svg.point_label(pc, "C", dx=12, dy=4),
        svg.angle_arc(pa, pb, pc, f"{apex_ang}°" if given_apex else "x°", r=26),
        svg.angle_arc(pb, pa, pc, "x°" if given_apex else f"{base_ang}°", r=24),
    ])
    if given_apex:
        return mcq(
            stem="จากรูป สามเหลี่ยม ABC มีด้าน AB = AC จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
            figure=fig,
            correct=f"{base_ang}°",
            wrongs=[
                W(f"{180 - apex_ang}°", "นำมุมยอดลบออกจาก 180° แล้วลืมหารด้วย 2", "partial"),
                W(f"{apex_ang}°", "คิดว่ามุมที่ฐานเท่ากับมุมยอด", "concept"),
                W(f"{180 - 2 * apex_ang if 180 - 2 * apex_ang > 0 else base_ang + 15}°", "คำนวณโดยเอามุมยอดคูณ 2 แล้วลบจาก 180° (สลับกับมุมที่ฐาน)", "formula"),
            ],
            hint="ด้าน AB = AC ทำให้มุม B และมุม C มีขนาดเท่ากัน",
            steps=[
                "เนื่องจาก AB = AC รูปสามเหลี่ยม ABC จึงเป็นสามเหลี่ยมหน้าจั่วที่มีมุม B = มุม C = x°",
                f"จะได้ x + x + {apex_ang}° = 180°",
                f"2x = {180 - apex_ang}° ดังนั้น x = {base_ang}°",
            ],
        )
    return mcq(
        stem="จากรูป สามเหลี่ยม ABC มีด้าน AB = AC จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{apex_ang}°",
        wrongs=[
            W(f"{180 - base_ang}°", "ลบมุมที่ฐานออกเพียงมุมเดียว ลืมว่ามีมุมที่ฐาน 2 มุมที่เท่ากัน", "partial"),
            W(f"{(180 - base_ang) // 2}°", "สับสนคิดว่าเป็นมุมยอด จึงนำไปลบ 180° แล้วหารด้วย 2", "formula"),
            W(f"{base_ang}°", "คิดว่ามุมยอดเท่ากับมุมที่ฐาน", "concept"),
        ],
        hint="มุมที่ฐาน B และ C มีขนาดเท่ากัน",
        steps=[
            f"เนื่องจาก AB = AC ดังนั้น มุม C = มุม B = {base_ang}°",
            f"มุมยอด x = 180° − ({base_ang}° + {base_ang}°) = 180° − {2 * base_ang}° = {apex_ang}°",
        ],
    )


@template("m.geo.iso_equi", "medium")
def _two_isosceles_chain():
    # Triangle ABC with point D on BC such that AB = AD and AD = DC (or BD = AD)
    # Wait: let's make D on BC with AD = DC and AB = BD? Or let's use exterior angle chain:
    # In ΔABC, D is on BC. AD = DC, ∠C = c => ∠DAC = c, exterior ∠ADB = 2c.
    # Also AB = BD (or AB = AD). If AB = AD, then ∠B = ∠ADB = 2c, and ∠BAD = 180 - 4c.
    c = random.randint(22, 40)
    adb = 2 * c
    b_ang = adb  # since AB = AD
    bad = 180 - 4 * c
    bac = bad + c
    pa, pb, pd, pc = (95, 25), (25, 135), (125, 135), (230, 135)
    fig = svg.canvas(255, 160, [
        svg.polygon([pa, pb, pc]),
        svg.line(pa, pd),
        svg.tick(pa, pb, 2),
        svg.tick(pa, pd, 2),
        svg.tick(pd, pc, 1),
        svg.point_label(pa, "A", dy=-10),
        svg.point_label(pb, "B", dx=-10, dy=6),
        svg.point_label(pd, "D", dy=16),
        svg.point_label(pc, "C", dx=10, dy=6),
        svg.angle_arc(pc, pa, pd, f"{c}°", r=28),
        svg.angle_arc(pb, pa, pd, "x°", r=24),
    ])
    return mcq(
        stem="จากรูป จุด D อยู่บนส่วนของเส้นตรง BC โดยที่ AB = AD และ AD = DC จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{b_ang}°",
        wrongs=[
            W(f"{c}°", "คิดว่ามุม B เท่ากับมุม C โดยตรง", "concept"),
            W(f"{180 - 2 * c}°", "ตอบขนาดของมุม ADC แทนที่จะหามุม B", "partial"),
            W(f"{bac}°", "ตอบขนาดของมุม BAC แทนที่จะตอบมุม B", "misread"),
            W(f"{3 * c}°", "คูณขนาดมุมผิดขั้นตอน", "calc"),
        ],
        hint="เริ่มจากสามเหลี่ยมหน้าจั่ว ADC เพื่อหามุมภายนอก ADB ก่อน แล้วจึงดูสามเหลี่ยมหน้าจั่ว ABD",
        steps=[
            f"ในสามเหลี่ยม ADC มี AD = DC ดังนั้น มุม DAC = มุม C = {c}°",
            f"มุม ADB เป็นมุมภายนอกของสามเหลี่ยม ADC จึงมีขนาด = {c}° + {c}° = {adb}°",
            f"ในสามเหลี่ยม ABD มี AB = AD ดังนั้น มุม B (x) = มุม ADB = {b_ang}°",
        ],
    )


@template("m.geo.iso_equi", "challenge")
def _square_equilateral_combo():
    # Classic top-school problem: Square ABCD with Equilateral triangle ABE inside or outside,
    # or Equilateral triangle ABC attached to isosceles triangle ACD where AC = CD.
    mode = random.choice(["inside_sq", "outside_sq", "equi_iso"])
    if mode == "inside_sq":
        # Square ABCD, equilateral ΔABE inside (or ΔCDE inside).
        # Let's vary by adding an extra angle question or rotating, or let's parameterize with a rectangle/rhombus!
        # Better yet: Rhombus ABCD with ∠B = b_ang (even), and equilateral ΔABE inside or outside!
        # That makes it fully parametric with huge variety!
        b_ang = random.randrange(64, 116, 2)
        if b_ang == 60:
            b_ang = 76
        # In rhombus ABCD, AB = BC = CD = DA.
        # ΔABE is equilateral inside/on AB, or let's do: ΔABC is equilateral (all 60°), and ΔACD is isosceles with AC = AD and ∠CAD = top_ang!
        pass
    # Parametric combo: Equilateral triangle ABC (AB=BC=CA) and isosceles triangle ACD (AC=AD) sharing side AC.
    # Let ∠CAD = alpha (even). Then in ΔACD (AC=AD), ∠ACD = ∠ADC = (180 - alpha)/2.
    # Ask for ∠BCD = 60 + (180 - alpha)/2 or ∠ABD etc.
    alpha = random.randrange(24, 96, 2)
    acd = (180 - alpha) // 2
    bcd = 60 + acd
    pb, pa, pc, pd = (30, 130), (95, 25), (140, 130), (225, 65)
    fig = svg.canvas(255, 160, [
        svg.polygon([pa, pb, pc]),
        svg.polygon([pa, pc, pd]),
        svg.tick(pa, pb, 1),
        svg.tick(pb, pc, 1),
        svg.tick(pa, pc, 1),
        svg.tick(pa, pd, 1),
        svg.point_label(pa, "A", dy=-10),
        svg.point_label(pb, "B", dx=-12, dy=4),
        svg.point_label(pc, "C", dy=16),
        svg.point_label(pd, "D", dx=12, dy=-2),
        svg.angle_arc(pa, pc, pd, f"{alpha}°", r=24),
        svg.angle_arc(pc, pb, pd, "x°", r=20),
    ])
    return mcq(
        stem="จากรูป สามเหลี่ยม ABC เป็นรูปสามเหลี่ยมด้านเท่า และมีด้าน AD = AC จงหาขนาดของมุม BCD (ค่า x) (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{bcd}°",
        wrongs=[
            W(f"{acd}°", "หามุม ACD ได้แล้วแต่ลืมบวกมุม ACB (60°) ของสามเหลี่ยมด้านเท่า", "partial"),
            W(f"{60 + alpha}°", f"คิดว่ามุม ACD มีขนาดเท่ากับมุมยอด {alpha}°", "concept"),
            W(f"{60 + (180 - alpha)}°", "ลืมหารด้วย 2 ตอนหามุมที่ฐานของสามเหลี่ยมหน้าจั่ว ACD", "partial"),
            W(f"{bcd - 10}°", "คำนวณมุมของสามเหลี่ยมด้านเท่าหรือหน้าจั่วผิดพลาด", "calc"),
        ],
        hint="ด้านที่มีขีด 1 ขีดยาวเท่ากันทั้งหมด ดังนั้นสามเหลี่ยม ACD เป็นสามเหลี่ยมหน้าจั่วที่มี AC = AD",
        steps=[
            "เนื่องจากสามเหลี่ยม ABC เป็นสามเหลี่ยมด้านเท่า ดังนั้น มุม ACB = 60°",
            f"เนื่องจาก AD = AC สามเหลี่ยม ACD จึงเป็นสามเหลี่ยมหน้าจั่วที่มีมุม ACD = มุม ADC",
            f"จะได้ มุม ACD = (180° − {alpha}°) ÷ 2 = {acd}°",
            f"ดังนั้น มุม BCD (x) = มุม ACB + มุม ACD = 60° + {acd}° = {bcd}°",
        ],
    )


# ===========================================================================
# Skill 5: m.geo.polygon — มุมภายในและมุมภายนอกของรูปหลายเหลี่ยม
# ===========================================================================
skill(
    "m.geo.polygon",
    "m.geo",
    "มุมภายในและมุมภายนอกของรูปหลายเหลี่ยม",
    lesson={
        "concept": (
            "รูป n เหลี่ยมใด ๆ สามารถแบ่งเป็นรูปสามเหลี่ยมได้ n − 2 รูป จึงมีผลรวมมุมภายในเท่ากับ (n − 2) × 180° "
            "และผลรวมของมุมภายนอกของรูปหลายเหลี่ยมใด ๆ เท่ากับ 360° เสมอ "
            "ถ้ารูป n เหลี่ยมเป็นรูปหลายเหลี่ยมด้านเท่ามุมเท่า มุมภายในแต่ละมุม = [(n − 2) × 180°] ÷ n = 180° − (360° ÷ n)"
        ),
        "steps": [
            "ดูจำนวนด้าน (n) ของรูปหลายเหลี่ยม",
            "ใช้สูตรผลรวมมุมภายใน = (n − 2) × 180°",
            "ถ้าเป็นรูปหลายเหลี่ยมด้านเท่ามุมเท่า ให้หารด้วย n หรือใช้ มุมภายนอก = 360° ÷ n แล้วนำไปลบออกจาก 180°",
        ],
        "example": {
            "q": "รูปหกเหลี่ยมด้านเท่ามุมเท่ามีมุมภายในแต่ละมุมกางกี่องศา",
            "steps": [
                "ผลรวมมุมภายในของรูป 6 เหลี่ยม = (6 − 2) × 180° = 720°",
                "มุมภายในแต่ละมุม = 720° ÷ 6 = 120°",
            ],
            "a": "120°",
        },
        "mistakes": [
            "ใช้สูตร n × 180° แทนที่จะเป็น (n − 2) × 180°",
            "สับสนระหว่างผลรวมมุมภายในทั้งหมด กับขนาดของมุมภายใน 1 มุม",
        ],
        "tips": [
            "การหามุมภายใน 1 มุมของรูป n เหลี่ยมด้านเท่ามุมเท่า คิดจาก 180° − (360° ÷ n) จะคิดเลขเร็วกว่ามาก",
        ],
    },
    weight=1.3,
)

_POLY_NAMES = {
    5: "ห้าเหลี่ยม",
    6: "หกเหลี่ยม",
    8: "แปดเหลี่ยม",
    9: "เก้าเหลี่ยม",
    10: "สิบเหลี่ยม",
    12: "สิบสองเหลี่ยม",
    15: "สิบห้าเหลี่ยม",
    18: "สิบแปดเหลี่ยม",
    20: "ยี่สิบเหลี่ยม",
}


def _reg_poly_points(cx, cy, r, n):
    pts = []
    for i in range(n):
        a = math.radians(-90 + i * 360 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@template("m.geo.polygon", "easy")
def _polygon_regular_angle():
    n = random.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    name = _POLY_NAMES[n]
    total = (n - 2) * 180
    one_int = total // n
    one_ext = 360 // n
    ask_total = random.choice([True, False])
    draw_n = min(n, 8)
    pts = _reg_poly_points(110, 80, 62, draw_n)
    fig = svg.canvas(220, 160, [
        svg.polygon(pts, shade=True),
        svg.label((110, 80), f"{n} เหลี่ยม", size=13, bold=True),
    ])
    if ask_total:
        return mcq(
            stem=f"ผลรวมของมุมภายในทั้งหมดของรูป{name}เท่ากับกี่องศา",
            figure=fig,
            correct=f"{num(total)}°",
            wrongs=[
                W(f"{num(n * 180)}°", f"นำจำนวนด้าน {n} คูณ 180° เลย ลืมลบ 2 ออกก่อน", "formula"),
                W(f"{num((n - 1) * 180)}°", "ใช้ (n − 1) × 180° แทนที่จะเป็น (n − 2) × 180°", "formula"),
                W(f"{one_int}°", "ตอบขนาดของมุมภายในเพียง 1 มุม แทนที่จะตอบผลรวมทุกมุม", "misread"),
            ],
            hint="ผลรวมมุมภายในของรูป n เหลี่ยม = (n − 2) × 180°",
            steps=[
                f"รูป{name}มีจำนวนด้าน n = {n}",
                f"ผลรวมมุมภายใน = ({n} − 2) × 180° = {n - 2} × 180° = {num(total)}°",
            ],
        )
    return mcq(
        stem=f"มุมภายในแต่ละมุมของรูป{name}ด้านเท่ามุมเท่ามีขนาดกี่องศา",
        figure=fig,
        correct=f"{one_int}°",
        wrongs=[
            W(f"{one_ext}°", "ตอบขนาดของมุมภายนอก (360° ÷ n) ลืมนำไปลบออกจาก 180°", "partial"),
            W(f"{num(total)}°", "ตอบผลรวมของมุมภายในทั้งหมด ลืมหารด้วยจำนวนมุม", "partial"),
            W(f"{180 - (180 // n if 180 % n == 0 else one_ext - 6)}°", "ใช้ 180° ÷ n แทนที่จะเป็น 360° ÷ n", "formula"),
        ],
        hint="หามุมภายนอกแต่ละมุมจาก 360° ÷ n แล้วนำไปลบออกจาก 180°",
        steps=[
            f"รูป{name}ด้านเท่ามุมเท่ามี n = {n} ด้าน",
            f"มุมภายนอกแต่ละมุม = 360° ÷ {n} = {one_ext}°",
            f"มุมภายในแต่ละมุม = 180° − {one_ext}° = {one_int}°",
        ],
    )


@template("m.geo.polygon", "medium")
def _pentagon_missing_angle():
    # Irregular pentagon with 4 known angles (one can be 90°) and 1 unknown x
    a = random.randint(95, 130)
    b = random.randint(95, 130)
    c = random.randint(100, 135)
    d = random.choice([90, random.randint(95, 125)])
    x = 540 - (a + b + c + d)
    if x < 70 or x > 155:
        return None
    pts = [(40, 135), (185, 135), (210, 70), (115, 20), (25, 70)]
    parts = [
        svg.polygon(pts),
        svg.angle_arc(pts[1], pts[0], pts[2], f"{a}°", r=22),
        svg.angle_arc(pts[2], pts[1], pts[3], f"{b}°", r=22),
        svg.angle_arc(pts[3], pts[2], pts[4], "x°", r=24),
        svg.angle_arc(pts[4], pts[3], pts[0], f"{c}°", r=22),
    ]
    if d == 90:
        parts.append(svg.right_angle(pts[0], pts[1], pts[4], size=11))
    else:
        parts.append(svg.angle_arc(pts[0], pts[1], pts[4], f"{d}°", r=22))
    fig = svg.canvas(240, 160, parts)
    return mcq(
        stem="จากรูปห้าเหลี่ยมที่กำหนดให้ จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{x}°",
        wrongs=[
            W(f"{x + 90 if d == 90 else abs(360 - (a + b + c + d)) or 80}°",
              "ลืมหักมุมฉาก 90° ออกด้วย" if d == 90 else "ใช้ผลรวมมุมภายใน 360° แทนที่จะเป็น 540°",
              "misread" if d == 90 else "formula"),
            W(f"{720 - (a + b + c + d)}°", "ใช้ผลรวมมุมภายในของรูปหกเหลี่ยม (720°) แทนรูปห้าเหลี่ยม (540°)", "formula"),
            W(f"{x + 10}°", "บวกลบเลขผิดในหลักสิบ", "calc"),
            W(f"{x - 10}°", "บวกลบเลขผิดในหลักสิบ", "calc"),
        ],
        hint="ผลรวมมุมภายในของรูปห้าเหลี่ยม = (5 − 2) × 180° = 540°",
        steps=[
            "ผลรวมมุมภายในของรูปห้าเหลี่ยม = (5 − 2) × 180° = 540°",
            f"ผลบวกของมุมที่ทราบค่า 4 มุม = {a}° + {b}° + {c}° + {d}° = {a + b + c + d}°",
            f"ดังนั้น x = 540° − {a + b + c + d}° = {x}°",
        ],
    )


@template("m.geo.polygon", "hard")
def _polygon_find_sides_or_diagonals():
    n = random.choice([6, 8, 9, 10, 12, 15, 18, 20, 24])
    ext = 360 // n
    interior = 180 - ext
    diags = n * (n - 3) // 2
    mode = random.choice(["from_int_to_n", "from_ratio_to_n", "from_int_to_diag"])
    if mode == "from_int_to_diag":
        return mcq(
            stem=f"รูปหลายเหลี่ยมด้านเท่ามุมเท่ารูปหนึ่งมีมุมภายในแต่ละมุมกาง {interior}° รูปหลายเหลี่ยมนี้มีเส้นทแยงมุมทั้งหมดกี่เส้น",
            correct=f"{diags} เส้น",
            wrongs=[
                W(f"{n} เส้น", "ตอบเป็นจำนวนด้านของรูปหลายเหลี่ยม แทนที่จะหาจำนวนเส้นทแยงมุม", "partial"),
                W(f"{n * (n - 3)} เส้น", "ใช้สูตร n(n − 3) โดยลืมหารด้วย 2 จึงนับเส้นทแยงมุมซ้ำไป-กลับ", "formula"),
                W(f"{n - 3} เส้น", "ตอบเฉพาะจำนวนเส้นทแยงมุมที่ลากจากจุดยอดเพียง 1 จุด", "partial"),
            ],
            hint="หาจำนวนด้าน n จากมุมภายนอก 360° ÷ (180° − มุมภายใน) ก่อน แล้วใช้สูตรจำนวนเส้นทแยงมุม = n(n − 3) ÷ 2",
            steps=[
                f"มุมภายนอกแต่ละมุม = 180° − {interior}° = {ext}°",
                f"จำนวนด้าน n = 360° ÷ {ext}° = {n} ด้าน",
                f"จำนวนเส้นทแยงมุมทั้งหมด = {n} × ({n} − 3) ÷ 2 = {diags} เส้น",
            ],
        )
    if mode == "from_ratio_to_n":
        from math import gcd
        g = gcd(interior, ext)
        r_in, r_ex = interior // g, ext // g
        return mcq(
            stem=f"รูปหลายเหลี่ยมด้านเท่ามุมเท่ารูปหนึ่ง มีอัตราส่วนของมุมภายในต่อมุมภายนอกแต่ละมุมเป็น {r_in} : {r_ex} รูปหลายเหลี่ยมนี้มีทั้งหมดกี่ด้าน",
            correct=f"{n} ด้าน",
            wrongs=[
                W(f"{r_in + r_ex} ด้าน", "นำตัวเลขอัตราส่วนมาบวกกันแล้วตอบเลย", "concept"),
                W(f"{n + 2} ด้าน", "ลืมบวก 2 หรือคำนวณจำนวนด้านคลาดเคลื่อน", "formula"),
                W(f"{ext} ด้าน", "ตอบขนาดของมุมภายนอกแทนจำนวนด้าน", "partial"),
            ],
            hint="มุมภายใน + มุมภายนอกที่จุดยอดเดียวกันรวมกันได้ 180° และจำนวนด้าน n = 360° ÷ มุมภายนอก",
            steps=[
                f"มุมภายใน + มุมภายนอก = 180° แบ่งเป็น {r_in} + {r_ex} = {r_in + r_ex} ส่วน",
                f"จะได้มุมภายนอกแต่ละมุม = 180° × {r_ex} ÷ {r_in + r_ex} = {ext}°",
                f"จำนวนด้าน n = 360° ÷ {ext}° = {n} ด้าน",
            ],
        )
    total = (n - 2) * 180
    return mcq(
        stem=f"รูปหลายเหลี่ยมรูปหนึ่งมีผลรวมของมุมภายในทั้งหมดเท่ากับ {num(total)}° รูปหลายเหลี่ยมนี้มีกี่ด้าน",
        correct=f"{n} ด้าน",
        wrongs=[
            W(f"{n - 2} ด้าน", "หารด้วย 180° แล้วตอบเลย ลืมบวก 2 จากสูตร (n − 2) × 180°", "partial"),
            W(f"{n + 2} ด้าน", "นำ 2 ไปบวกซ้ำเกินอีกครั้ง", "formula"),
            W(f"{total // 90} ด้าน", "หารด้วย 90° แทนที่จะหารด้วย 180°", "formula"),
        ],
        hint="จากสูตร ผลรวมมุมภายใน = (n − 2) × 180° ให้หารด้วย 180° แล้วบวก 2",
        steps=[
            f"จากสูตร (n − 2) × 180° = {num(total)}°",
            f"n − 2 = {num(total)} ÷ 180 = {n - 2}",
            f"ดังนั้น n = {n - 2} + 2 = {n} ด้าน",
        ],
    )


# ===========================================================================
# Skill 6: m.geo.quad_props — สมบัติของรูปสี่เหลี่ยมและแกนสมมาตร
# ===========================================================================
skill(
    "m.geo.quad_props",
    "m.geo",
    "สมบัติของรูปสี่เหลี่ยมและแกนสมมาตร",
    lesson={
        "concept": (
            "รูปสี่เหลี่ยมแต่ละชนิดมีสมบัติของด้าน มุม เส้นทแยงมุม และแกนสมมาตรต่างกัน เช่น "
            "เส้นทแยงมุมตัดกันเป็นมุมฉากได้แก่ จัตุรัส ขนมเปียกปูน รูปว่าว (และสี่เหลี่ยมที่เส้นทแยงมุมตั้งฉากกัน) "
            "ส่วนสี่เหลี่ยมด้านขนานและผืนผ้า เส้นทแยงมุมแบ่งครึ่งซึ่งกันและกันแต่ไม่จำเป็นต้องตัดกันเป็นมุมฉาก"
        ),
        "steps": [
            "พิจารณาสมบัติ 4 ด้าน: ความยาวด้าน การขนานกัน เส้นทแยงมุม (ยาวเท่ากัน/แบ่งครึ่ง/ตั้งฉาก) และจำนวนแกนสมมาตร",
            "ระวังรูปที่มักจำผิด: สี่เหลี่ยมผืนผ้ามีแกนสมมาตร 2 แกน (ไม่ใช่ 4 แกน) และสี่เหลี่ยมด้านขนานไม่มีแกนสมมาตร",
        ],
        "example": {
            "q": "รูปสี่เหลี่ยมชนิดใดที่เส้นทแยงมุมยาวเท่ากัน แบ่งครึ่งซึ่งกันและกัน และตัดกันเป็นมุมฉาก",
            "steps": [
                "เส้นทแยงมุมยาวเท่ากัน → จัตุรัส หรือ ผืนผ้า",
                "ตัดกันเป็นมุมฉากด้วย → รูปสี่เหลี่ยมจัตุรัสเท่านั้น",
            ],
            "a": "รูปสี่เหลี่ยมจัตุรัส",
        },
        "mistakes": [
            "คิดว่าสี่เหลี่ยมผืนผ้าพับตามแนวเส้นทแยงมุมแล้วทับกันสนิท (จริง ๆ ไม่ทับกันสนิท จึงมีแกนสมมาตรแค่ 2 แกน)",
            "คิดว่าสี่เหลี่ยมด้านขนานมีแกนสมมาตร 2 แกน (จริง ๆ มี 0 แกน)",
        ],
        "tips": [
            "จำแม่น ๆ: แกนสมมาตร จัตุรัส=4, ผืนผ้า=2, ขนมเปียกปูน=2, รูปว่าว=1, คางหมูหน้าจั่ว=1, ด้านขนาน=0",
        ],
    },
    weight=1.1,
)


@template("m.geo.quad_props", "easy")
def _symmetry_axes_count():
    shapes = [
        ("รูปสี่เหลี่ยมจัตุรัส", 4, svg.rect(50, 20, 90, 90, shade=True)),
        ("รูปสี่เหลี่ยมผืนผ้า (ที่กว้างไม่เท่ากับยาว)", 2, svg.rect(35, 30, 120, 70, shade=True)),
        ("รูปสี่เหลี่ยมขนมเปียกปูน (ที่ไม่ใช่จัตุรัส)", 2, svg.polygon([(95, 15), (160, 65), (95, 115), (30, 65)], shade=True)),
        ("รูปสี่เหลี่ยมด้านขนาน (ที่ไม่ใช่ผืนผ้าและขนมเปียกปูน)", 0, svg.polygon([(55, 25), (165, 25), (135, 105), (25, 105)], shade=True)),
        ("รูปสี่เหลี่ยมรูปว่าว", 1, svg.polygon([(95, 15), (145, 55), (95, 120), (45, 55)], shade=True)),
        ("รูปสามเหลี่ยมด้านเท่า", 3, svg.polygon([(95, 15), (155, 115), (35, 115)], shade=True)),
        ("รูปสามเหลี่ยมหน้าจั่ว (ที่ไม่ใช่ด้านเท่า)", 1, svg.polygon([(95, 15), (140, 115), (50, 115)], shade=True)),
        ("รูปห้าเหลี่ยมด้านเท่ามุมเท่า", 5, svg.polygon(_reg_poly_points(95, 68, 52, 5), shade=True)),
        ("รูปหกเหลี่ยมด้านเท่ามุมเท่า", 6, svg.polygon(_reg_poly_points(95, 68, 52, 6), shade=True)),
    ]
    a, b = pick(shapes, 2)
    ask_mode = random.choice(["single", "sum", "diff"])
    if ask_mode == "single":
        name, ans, elem = a
        fig = svg.canvas(190, 130, [elem])
        wrongs = [
            W(f"{4 if ans != 4 else 2} แกน", "เผลอนับแนวเส้นทแยงมุมซึ่งเมื่อพับแล้วไม่ทับกันสนิท", "trap"),
            W(f"{2 if ans not in (2, 4) else 0} แกน", "จำจำนวนแกนสมมาตรของรูปสี่เหลี่ยมสลับชนิดกัน", "concept"),
            W(f"{1 if ans != 1 else 3} แกน", "นับแกนสมมาตรไม่ครบทุกแนว", "partial"),
            W(f"{ans + 2} แกน", "นับแกนซ้ำหัวท้ายเป็นคนละแกน", "concept"),
        ]
        return mcq(
            stem=f"{name} มีแกนสมมาตรทั้งหมดกี่แกน",
            figure=fig,
            correct=f"{ans} แกน",
            wrongs=wrongs,
            hint="แกนสมมาตรคือเส้นที่เมื่อพับรูปตามแนวเส้นนั้นแล้ว สองข้างจะทับกันสนิทพอดี",
            steps=[
                f"พิจารณาการพับครึ่งของ{name}",
                f"มีแนวพับที่ทับกันสนิททั้งหมด {ans} แกน",
            ],
        )
    n1, c1, _ = a
    n2, c2, _ = b
    total = c1 + c2
    return mcq(
        stem=f"ผลรวมของจำนวนแกนสมมาตรของ{n1} และ{n2} เท่ากับกี่แกน",
        correct=f"{total} แกน",
        wrongs=[
            W(f"{total + 2} แกน", "คิดว่าสี่เหลี่ยมผืนผ้ามี 4 แกน หรือสี่เหลี่ยมด้านขนานมี 2 แกน", "trap"),
            W(f"{abs(c1 - c2)} แกน", "นำจำนวนแกนสมมาตรมาลบกันแทนที่จะบวกกัน", "misread"),
            W(f"{max(1, total - 1)} แกน", "นับแกนสมมาตรของรูปใดรูปหนึ่งขาดไป 1 แกน", "concept"),
            W(f"{total + 1} แกน", "นับแกนสมมาตรเกินมา 1 แกน", "concept"),
        ],
        hint="หาจำนวนแกนสมมาตรของแต่ละรูปก่อน แล้วนำมาบวกกัน (ระวังผืนผ้ามี 2 แกน ด้านขนานมี 0 แกน)",
        steps=[
            f"{n1} มีแกนสมมาตร {c1} แกน",
            f"{n2} มีแกนสมมาตร {c2} แกน",
            f"รวมมีแกนสมมาตรทั้งหมด {c1} + {c2} = {total} แกน",
        ],
    )


@template("m.geo.quad_props", "medium")
def _quad_diagonal_properties():
    questions = [
        (
            "ข้อใดเป็นสมบัติของรูปสี่เหลี่ยมขนมเปียกปูนที่ถูกต้องเสมอ",
            "เส้นทแยงมุมแบ่งครึ่งซึ่งกันและกันและตัดกันเป็นมุมฉาก",
            [
                W("เส้นทแยงมุมสองเส้นยาวเท่ากันเสมอ", "เส้นทแยงมุมของขนมเปียกปูนไม่จำเป็นต้องยาวเท่ากัน (จะเท่ากันเฉพาะเมื่อเป็นจัตุรัส)", "concept"),
                W("มุมภายในทุกมุมเป็นมุมฉาก", "ขนมเปียกปูนมีมุมตรงข้ามเท่ากัน แต่ไม่จำเป็นต้องเป็นมุมฉาก", "concept"),
                W("มีแกนสมมาตรทั้งหมด 4 แกน", "ขนมเปียกปูนทั่วไปมีแกนสมมาตรเพียง 2 แกนตามแนวเส้นทแยงมุม", "trap"),
            ],
            "สี่เหลี่ยมขนมเปียกปูนมีด้านทั้งสี่ยาวเท่ากัน เส้นทแยงมุมจึงตัดกันเป็นมุมฉากและแบ่งครึ่งซึ่งกันและกัน",
        ),
        (
            "รูปสี่เหลี่ยมในข้อใดที่เส้นทแยงมุมตัดกันเป็นมุมฉาก แต่แบ่งครึ่งเพียงเส้นเดียว",
            "รูปสี่เหลี่ยมรูปว่าว",
            [
                W("รูปสี่เหลี่ยมขนมเปียกปูน", "ขนมเปียกปูนมีเส้นทแยงมุมแบ่งครึ่งซึ่งกันและกันทั้งสองเส้น", "concept"),
                W("รูปสี่เหลี่ยมผืนผ้า", "ผืนผ้ามีเส้นทแยงมุมแบ่งครึ่งกันทั้งสองเส้นแต่ไม่ตัดกันเป็นมุมฉาก", "concept"),
                W("รูปสี่เหลี่ยมคางหมูหน้าจั่ว", "คางหมูหน้าจั่วมีเส้นทแยงมุมยาวเท่ากันแต่ไม่จำเป็นต้องตัดกันเป็นมุมฉาก", "concept"),
            ],
            "สี่เหลี่ยมรูปว่าวมีแกนสมมาตร 1 แกน เส้นทแยงมุมเส้นหลักจึงแบ่งครึ่งและตั้งฉากกับเส้นทแยงมุมอีกเส้นหนึ่ง",
        ),
        (
            "รูปสี่เหลี่ยมชนิดใดที่เส้นทแยงมุมยาวเท่ากันและแบ่งครึ่งซึ่งกันและกัน แต่ไม่จำเป็นต้องตัดกันเป็นมุมฉาก",
            "รูปสี่เหลี่ยมผืนผ้า",
            [
                W("รูปสี่เหลี่ยมขนมเปียกปูน", "ขนมเปียกปูนมีเส้นทแยงมุมตัดกันเป็นมุมฉากแต่ยาวไม่เท่ากัน", "concept"),
                W("รูปสี่เหลี่ยมด้านขนาน", "สี่เหลี่ยมด้านขนานทั่วไปมีเส้นทแยงมุมยาวไม่เท่ากัน", "concept"),
                W("รูปสี่เหลี่ยมรูปว่าว", "รูปว่าวมีเส้นทแยงมุมตัดกันเป็นมุมฉากและยาวไม่เท่ากัน", "concept"),
            ],
            "สี่เหลี่ยมผืนผ้ามีมุมทั้งสี่เป็นมุมฉาก เส้นทแยงมุมจึงยาวเท่ากันและแบ่งครึ่งกัน",
        ),
        (
            "ข้อใดกล่าวถึงแกนสมมาตรของรูปสี่เหลี่ยมได้ถูกต้อง",
            "รูปสี่เหลี่ยมด้านขนานที่ด้านประชิดยาวไม่เท่ากันและมุมไม่เป็นมุมฉาก ไม่มีแกนสมมาตร",
            [
                W("รูปสี่เหลี่ยมผืนผ้ามีแกนสมมาตร 4 แกน", "ผืนผ้าพับตามแนวเส้นทแยงมุมไม่ทับกันสนิท จึงมีแกนสมมาตรเพียง 2 แกน", "trap"),
                W("รูปสี่เหลี่ยมคางหมูทุกรูปมีแกนสมมาตร 1 แกน", "เฉพาะสี่เหลี่ยมคางหมูหน้าจั่วเท่านั้นที่มีแกนสมมาตร 1 แกน", "trap"),
                W("รูปสี่เหลี่ยมรูปว่าวมีแกนสมมาตร 2 แกนตามแนวเส้นทแยงมุม", "รูปว่าวมีแกนสมมาตรเพียง 1 แกนตามแนวเส้นทแยงมุมเส้นที่เชื่อมมุมยอด", "concept"),
            ],
            "ระวังกับดักเรื่องการพับสี่เหลี่ยมผืนผ้าและสี่เหลี่ยมด้านขนาน",
        ),
    ]
    # Add a rhombus/kite angle calculation variant for variety!
    if random.random() < 0.7:
        # Rhombus ABCD with diagonal AC and BD intersecting at O, given ∠BAC = a, find ∠ABC
        a = random.randint(22, 68)
        abc = 180 - 2 * a
        pts = [(120, 20), (210, 80), (120, 140), (30, 80)]
        o = (120, 80)
        fig = svg.canvas(240, 160, [
            svg.polygon(pts),
            svg.line(pts[0], pts[2]),
            svg.line(pts[1], pts[3]),
            svg.point_label(pts[0], "A", dy=-10),
            svg.point_label(pts[1], "B", dx=12),
            svg.point_label(pts[2], "C", dy=15),
            svg.point_label(pts[3], "D", dx=-12),
            svg.point_label(o, "O", dx=10, dy=-10),
            svg.angle_arc(pts[3], pts[0], o, f"{a}°", r=28),
            svg.angle_arc(pts[0], pts[3], pts[1], r=22),
            svg.label((106, 52), "x°", size=12, cls="fig-dim"),
        ])
        return mcq(
            stem="จากรูป สี่เหลี่ยม ABCD เป็นรูปสี่เหลี่ยมขนมเปียกปูน มีเส้นทแยงมุมตัดกันที่จุด O ถ้ามุม ADO = "
                 f"{a}° แล้วมุม DAB (ค่า x) มีขนาดกี่องศา (รูปไม่ได้วาดตามสัดส่วน)",
            figure=fig,
            correct=f"{abc}°",
            wrongs=[
                W(f"{90 - a}°", "ตอบขนาดของมุม DAO เพียงครึ่งเดียว ลืมคูณ 2 เพื่อเป็นมุม DAB เต็มมุม", "partial"),
                W(f"{2 * a}°", "ตอบขนาดของมุม ADC แทนที่จะเป็นมุม DAB", "misread"),
                W(f"{180 - a}°", f"นำ {a}° ไปลบออกจาก 180° โดยลืมคูณ 2 ก่อน", "partial"),
            ],
            hint="เส้นทแยงมุมของสี่เหลี่ยมขนมเปียกปูนตัดกันเป็นมุมฉากและแบ่งครึ่งมุมยอด",
            steps=[
                "เส้นทแยงมุมของสี่เหลี่ยมขนมเปียกปูนตัดกันเป็นมุมฉากที่จุด O (มุม AOD = 90°)",
                f"ในสามเหลี่ยมมุมฉาก AOD: มุม DAO = 90° − {a}° = {90 - a}°",
                f"เส้นทแยงมุม AC แบ่งครึ่งมุม DAB ดังนั้น x = 2 × {90 - a}° = {abc}°",
            ],
        )
    stem, corr, wrongs, explanation = pick(questions)
    return mcq(
        stem=stem,
        correct=corr,
        wrongs=wrongs,
        hint="ทบทวนสมบัติเส้นทแยงมุมและแกนสมมาตรของรูปสี่เหลี่ยมแต่ละชนิด",
        steps=[explanation, f"ดังนั้นคำตอบที่ถูกต้องคือ “{corr}”"],
    )


# ===========================================================================
# Skill 7: m.geo.circle — ส่วนประกอบและสมบัติของวงกลม
# ===========================================================================
skill(
    "m.geo.circle",
    "m.geo",
    "ส่วนประกอบและสมบัติของวงกลม",
    lesson={
        "concept": (
            "รัศมีทุกเส้นของวงกลมเดียวกันมีความยาวเท่ากัน เส้นผ่านศูนย์กลางยาวเป็น 2 เท่าของรัศมีและเป็นคอร์ดที่ยาวที่สุด "
            "เมื่อลากรัศมีสองเส้นไปยังปลายคอร์ด จะเกิดรูปสามเหลี่ยมหน้าจั่วที่มีจุดศูนย์กลางเป็นจุดยอดเสมอ"
        ),
        "steps": [
            "สังเกตส่วนของเส้นตรงที่ลากจากจุดศูนย์กลางไปยังเส้นรอบวง ว่าเป็นรัศมีซึ่งยาวเท่ากันทั้งหมด",
            "ใช้สมบัติของรูปสามเหลี่ยมหน้าจั่ว (OA = OB) เพื่อหามุมที่ต้องการ",
            "จำว่ามุมในครึ่งวงกลม (ที่มีเส้นผ่านศูนย์กลางเป็นฐาน) มีขนาด 90° เสมอ",
        ],
        "example": {
            "q": "วงกลมมีจุดศูนย์กลาง O ถ้าคอร์ด AB ทำให้มุม AOB = 80° มุม OAB มีขนาดเท่าใด",
            "steps": [
                "เนื่องจาก OA และ OB เป็นรัศมีของวงกลม จึงยาวเท่ากัน",
                "สามเหลี่ยม OAB เป็นสามเหลี่ยมหน้าจั่ว: มุม OAB = (180° − 80°) ÷ 2 = 50°",
            ],
            "a": "50°",
        },
        "mistakes": [
            "ลืมว่ารัศมี OA และ OB ยาวเท่ากันแม้โจทย์จะไม่ได้ขีดสัญลักษณ์ด้านเท่ากันไว้ให้",
            "สับสนระหว่างรัศมี (r) กับเส้นผ่านศูนย์กลาง (2r)",
        ],
        "tips": [
            "เจอจุดศูนย์กลางวงกลมเมื่อไร ให้ขีดสัญลักษณ์เท่ากันบนรัศมีทุกเส้นทันที!",
        ],
    },
    weight=1.1,
)


@template("m.geo.circle", "easy")
def _circle_chord_isosceles():
    base = random.randint(25, 72)
    center_ang = 180 - 2 * base
    given_center = random.choice([True, False])
    c = (115, 80)
    r = 62
    pa = (c[0] - r * math.cos(math.radians(35)), c[1] + r * math.sin(math.radians(35)))
    pb = (c[0] + r * math.cos(math.radians(35)), c[1] + r * math.sin(math.radians(35)))
    fig = svg.canvas(230, 165, [
        svg.circle(c, r),
        svg.polygon([c, pa, pb], shade=True),
        svg.dot(c, 3),
        svg.point_label(c, "O", dy=-12),
        svg.point_label(pa, "A", dx=-12, dy=6),
        svg.point_label(pb, "B", dx=12, dy=6),
        svg.angle_arc(c, pa, pb, f"{center_ang}°" if given_center else "x°", r=20),
        svg.angle_arc(pa, c, pb, "x°" if given_center else f"{base}°", r=22),
    ])
    if given_center:
        return mcq(
            stem="จากรูป จุด O เป็นจุดศูนย์กลางของวงกลม จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
            figure=fig,
            correct=f"{base}°",
            wrongs=[
                W(f"{180 - center_ang}°", "ลบมุมที่จุดศูนย์กลางออกจาก 180° แล้วลืมหารด้วย 2", "partial"),
                W(f"{center_ang // 2}°", "นำมุมที่จุดศูนย์กลางไปหารด้วย 2 โดยตรง", "concept"),
                W(f"{center_ang}°", "คิดว่ามุมที่ฐานเท่ากับมุมที่จุดศูนย์กลาง", "concept"),
            ],
            hint="OA และ OB เป็นรัศมีของวงกลมเดียวกัน จึงยาวเท่ากัน",
            steps=[
                "เนื่องจาก OA = OB (รัศมีของวงกลมเดียวกัน) สามเหลี่ยม OAB จึงเป็นสามเหลี่ยมหน้าจั่ว",
                f"จะได้ มุม OAB = มุม OBA = x°",
                f"x = (180° − {center_ang}°) ÷ 2 = {base}°",
            ],
        )
    return mcq(
        stem="จากรูป จุด O เป็นจุดศูนย์กลางของวงกลม จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{center_ang}°",
        wrongs=[
            W(f"{180 - base}°", "ลบมุมที่ฐานออกจาก 180° เพียงมุมเดียว", "partial"),
            W(f"{2 * base}°", "นำมุมที่ฐานคูณ 2 แล้วตอบเลย ลืมลบออกจาก 180°", "partial"),
            W(f"{90 - base if 90 > base else base}°", "ใช้ 90° แทนผลรวมมุมภายในสามเหลี่ยม 180°", "concept"),
        ],
        hint="สามเหลี่ยม OAB มี OA = OB เป็นรัศมีของวงกลม",
        steps=[
            f"เนื่องจาก OA = OB (รัศมีของวงกลม) ดังนั้น มุม OBA = มุม OAB = {base}°",
            f"มุม AOB (x) = 180° − ({base}° + {base}°) = {center_ang}°",
        ],
    )


@template("m.geo.circle", "medium")
def _semicircle_triangle():
    # AB is diameter through O, C is on circle. Given ∠CAB = a, find ∠ABC or ∠BOC
    a = random.randint(24, 66)
    b = 90 - a
    boc = 2 * a
    ask_boc = random.choice([True, False])
    c = (115, 85)
    r = 65
    pa = (c[0] - r, c[1])
    pb = (c[0] + r, c[1])
    pc = (c[0] + r * math.cos(math.radians(115)), c[1] - r * math.sin(math.radians(115)))
    fig = svg.canvas(230, 165, [
        svg.circle(c, r),
        svg.polygon([pa, pb, pc], shade=True),
        svg.line(c, pc),
        svg.dot(c, 3),
        svg.point_label(c, "O", dy=15),
        svg.point_label(pa, "A", dx=-12),
        svg.point_label(pb, "B", dx=12),
        svg.point_label(pc, "C", dy=-12),
        svg.angle_arc(pa, pb, pc, f"{a}°", r=24),
        svg.angle_arc(c, pb, pc, "x°", r=20) if ask_boc else svg.angle_arc(pb, pa, pc, "x°", r=24),
    ])
    if ask_boc:
        return mcq(
            stem="จากรูป AB เป็นเส้นผ่านศูนย์กลางของวงกลมที่มีจุด O เป็นจุดศูนย์กลาง จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
            figure=fig,
            correct=f"{boc}°",
            wrongs=[
                W(f"{180 - 2 * a}°", "ตอบขนาดของมุม AOC แทนที่จะตอบมุม BOC (x)", "misread"),
                W(f"{a}°", "คิดว่ามุมที่จุดศูนย์กลางเท่ากับมุมที่เส้นรอบวง", "concept"),
                W(f"{90 - a}°", "ตอบขนาดของมุม ABC แทนมุม BOC", "misread"),
            ],
            hint="OA = OC เป็นรัศมีของวงกลม ทำให้สามเหลี่ยม OAC เป็นสามเหลี่ยมหน้าจั่ว และมุม BOC เป็นมุมภายนอกของสามเหลี่ยม OAC",
            steps=[
                f"เนื่องจาก OA = OC (รัศมี) ดังนั้น มุม OCA = มุม OAC = {a}°",
                f"มุม BOC (x) เป็นมุมภายนอกของสามเหลี่ยม OAC จึงมีขนาด = {a}° + {a}° = {boc}°",
            ],
        )
    return mcq(
        stem="จากรูป AB เป็นเส้นผ่านศูนย์กลางของวงกลมที่มีจุด O เป็นจุดศูนย์กลาง จงหาค่าของ x (รูปไม่ได้วาดตามสัดส่วน)",
        figure=fig,
        correct=f"{b}°",
        wrongs=[
            W(f"{180 - 2 * a}°", "คิดว่าสามเหลี่ยม ABC เป็นสามเหลี่ยมหน้าจั่วที่มี AC = BC", "trap"),
            W(f"{a}°", "คิดว่ามุม B เท่ากับมุม A เสมอ", "concept"),
            W(f"{180 - a}°", "ลืมหักมุม ACB ซึ่งมีขนาด 90° (มุมในครึ่งวงกลม)", "concept"),
        ],
        hint="มุมในครึ่งวงกลม (มุม ACB) มีขนาด 90° เสมอ หรือแยกคิดจากสามเหลี่ยมหน้าจั่ว OAC และ OBC",
        steps=[
            f"เนื่องจาก OA = OC = OB (รัศมี) ทำให้มุม ACB เป็นมุมในครึ่งวงกลมซึ่งมีขนาด 90°",
            f"ในสามเหลี่ยมมุมฉาก ABC: x = 180° − 90° − {a}° = {b}°",
        ],
    )


# ===========================================================================
# Skill 8: m.geo.solid3d — รูปเรขาคณิตสามมิติและรูปคลี่
# ===========================================================================
skill(
    "m.geo.solid3d",
    "m.geo",
    "รูปเรขาคณิตสามมิติและรูปคลี่",
    lesson={
        "concept": (
            "ปริซึม n เหลี่ยม มีหน้าตัดเป็นรูป n เหลี่ยม 2 หน้า และหน้าข้างเป็นสี่เหลี่ยมมุมฉาก n หน้า "
            "(รวม F = n+2 หน้า, เส้นขอบ E = 3n เส้น, จุดยอด V = 2n จุด) "
            "ส่วนพีระมิดฐาน n เหลี่ยม มีฐาน 1 หน้า และหน้าข้างเป็นรูปสามเหลี่ยม n หน้า "
            "(รวม F = n+1 หน้า, เส้นขอบ E = 2n เส้น, จุดยอด V = n+1 จุด)"
        ),
        "steps": [
            "แยกให้ชัดเจนว่าเป็นปริซึม (มี 2 ฐาน หน้าข้างเป็นสี่เหลี่ยม) หรือพีระมิด (มี 1 ฐาน หน้าข้างเป็นสามเหลี่ยม)",
            "ใช้สูตรตามจำนวนเหลี่ยมของฐาน (n) เพื่อหาจำนวนหน้า (F) เส้นขอบ/สัน (E) และจุดยอด (V)",
            "สำหรับรูปคลี่ของลูกบาศก์ หน้าตรงข้ามจะเว้น 1 ช่องเสมอเมื่อเรียงต่อกันในแนวเดียวกัน",
        ],
        "example": {
            "q": "ปริซึมฐานหกเหลี่ยม มีจำนวนหน้า เส้นขอบ และจุดยอดรวมกันเท่าใด",
            "steps": [
                "ปริซึมฐาน 6 เหลี่ยม (n = 6): จำนวนหน้า F = 6 + 2 = 8 หน้า",
                "จำนวนเส้นขอบ E = 3 × 6 = 18 เส้น, จุดยอด V = 2 × 6 = 12 จุด",
                "รวมทั้งหมด = 8 + 18 + 12 = 38",
            ],
            "a": "38",
        },
        "mistakes": [
            "สลับสูตรของปริซึมกับพีระมิด",
            "ลืมนับหน้าฐาน (2 หน้าสำหรับปริซึม, 1 หน้าสำหรับพีระมิด) เมื่อหาจำนวนหน้าทั้งหมด",
        ],
        "tips": [
            "ความสัมพันธ์ของออยเลอร์ (Euler): สำหรับรูปทรงหลายหน้าทุกชนิด จะได้ หน้า + จุดยอด − เส้นขอบ = 2 เสมอ (F + V − E = 2)",
        ],
    },
    weight=1.2,
)


@template("m.geo.solid3d", "easy")
def _prism_pyramid_fev():
    n = random.choice([3, 4, 5, 6, 7, 8, 10])
    names = {
        3: "สามเหลี่ยม", 4: "สี่เหลี่ยม", 5: "ห้าเหลี่ยม", 6: "หกเหลี่ยม",
        7: "เจ็ดเหลี่ยม", 8: "แปดเหลี่ยม", 10: "สิบเหลี่ยม",
    }
    solid_type = random.choice(["prism", "pyramid"])
    ask_what = random.choice(["edges", "faces_plus_vertices", "sum_all"])
    if solid_type == "prism":
        sname = f"ปริซึมฐาน{names[n]}"
        F, E, V = n + 2, 3 * n, 2 * n
        wrong_other_E = 2 * n
    else:
        sname = f"พีระมิดฐาน{names[n]}"
        F, E, V = n + 1, 2 * n, n + 1
        wrong_other_E = 3 * n

    if ask_what == "edges":
        return mcq(
            stem=f"{sname} มีจำนวนเส้นขอบ (สัน) ทั้งหมดกี่เส้น",
            correct=f"{E} เส้น",
            wrongs=[
                W(f"{wrong_other_E} เส้น", "สับสนสูตรระหว่างปริซึม (3n) กับพีระมิด (2n)", "formula"),
                W(f"{F} เส้น", "ตอบจำนวนหน้าแทนจำนวนเส้นขอบ", "misread"),
                W(f"{V} เส้น", "ตอบจำนวนจุดยอดแทนจำนวนเส้นขอบ", "misread"),
                W(f"{E + n} เส้น", "นับเส้นขอบฐานซ้ำอีกหนึ่งรอบ", "concept"),
            ],
            hint="ปริซึมฐาน n เหลี่ยมมีเส้นขอบ 3n เส้น ส่วนพีระมิดฐาน n เหลี่ยมมีเส้นขอบ 2n เส้น",
            steps=[
                f"ฐานเป็นรูป{names[n]} ดังนั้น n = {n}",
                f"{sname} มีเส้นขอบทั้งหมด = {'3 × ' if solid_type == 'prism' else '2 × '}{n} = {E} เส้น",
            ],
        )
    if ask_what == "faces_plus_vertices":
        ans = F + V
        return mcq(
            stem=f"{sname} มีจำนวนหน้าและจำนวนจุดยอดรวมกันเท่ากับข้อใด",
            correct=str(ans),
            wrongs=[
                W(str(ans - (2 if solid_type == "prism" else 1)), "ลืมนับหน้าฐานเข้าไปในจำนวนหน้าทั้งหมด", "partial"),
                W(str(E), "ตอบเฉพาะจำนวนเส้นขอบแทนผลบวกของหน้ากับจุดยอด", "misread"),
                W(str((n + 1) + (n + 1) if solid_type == "prism" else (n + 2) + 2 * n),
                  "จำสูตรของปริซึมและพีระมิดสลับกัน", "formula"),
            ],
            hint="นับจำนวนหน้า (รวมฐาน) และจำนวนจุดยอด แล้วนำมาบวกกัน",
            steps=[
                f"สำหรับ{sname} (n = {n}): จำนวนหน้า = {F} หน้า, จำนวนจุดยอด = {V} จุด",
                f"ผลรวมของจำนวนหน้าและจุดยอด = {F} + {V} = {ans}",
            ],
        )
    ans = F + E + V
    return mcq(
        stem=f"ผลรวมของจำนวนหน้า จำนวนเส้นขอบ และจำนวนจุดยอดของ{sname} เท่ากับเท่าใด",
        correct=str(ans),
        wrongs=[
            W(str(ans - (2 if solid_type == "prism" else 1)), "นับเฉพาะหน้าข้าง ลืมนับหน้าฐาน", "partial"),
            W(str((n + 1) + 2 * n + (n + 1) if solid_type == "prism" else (n + 2) + 3 * n + 2 * n),
              "ใช้สูตรของปริซึมและพีระมิดสลับกัน", "formula"),
            W(str(E + V), "บวกเฉพาะเส้นขอบกับจุดยอด ลืมบวกจำนวนหน้า", "partial"),
        ],
        hint="หาจำนวนหน้า (F) เส้นขอบ (E) และจุดยอด (V) ทีละค่าแล้วนำมาบวกกัน",
        steps=[
            f"สำหรับ{sname} (n = {n}):",
            f"จำนวนหน้า (F) = {F} หน้า, เส้นขอบ (E) = {E} เส้น, จุดยอด (V) = {V} จุด",
            f"รวมทั้งหมด = {F} + {E} + {V} = {ans}",
        ],
    )


@template("m.geo.solid3d", "medium")
def _cube_net_opposite():
    # 4 classic cube net layouts with 6 numbered/lettered squares
    layouts = [
        # Cross net: row 1 has (0,1), (1,1), (2,1), (3,1); top (1,0); bottom (1,2)
        # Opposites: idx 0 <-> 2, 1 <-> 3, 4 <-> 5
        ([(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)], [(0, 2), (1, 3), (4, 5)]),
        # T-like net: (0,1),(1,1),(2,1),(3,1),(0,0),(2,2)
        ([(0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (2, 2)], [(0, 2), (1, 3), (4, 5)]),
        # Z-like staircase: (0,0),(1,0),(1,1),(2,1),(2,2),(3,2)
        ([(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)], [(0, 3), (1, 4), (2, 5)]),
        # 1-4-1 shifted: (0,1),(1,1),(2,1),(3,1),(2,0),(0,2)
        ([(0, 1), (1, 1), (2, 1), (3, 1), (2, 0), (0, 2)], [(0, 2), (1, 3), (4, 5)]),
    ]
    cells, pairs = pick(layouts)
    symbols = random.choice([
        ["A", "B", "C", "D", "E", "F"],
        ["ก", "ข", "ค", "ง", "จ", "ฉ"],
        ["1", "2", "3", "4", "5", "6"],
        ["P", "Q", "R", "S", "T", "U"],
    ])
    labels = symbols[:]
    random.shuffle(labels)
    pair_idx = random.randint(0, 2)
    i1, i2 = pairs[pair_idx]
    if random.random() < 0.5:
        i1, i2 = i2, i1
    ask_face = labels[i1]
    ans_face = labels[i2]
    other_faces = [labels[k] for k in range(6) if k not in (i1, i2)]

    s = 38
    parts = []
    for (cx, cy), lab in zip(cells, labels):
        x, y = 25 + cx * s, 15 + cy * s
        parts.append(svg.rect(x, y, s, s, shade=(lab == ask_face)))
        parts.append(svg.label((x + s / 2, y + s / 2), lab, size=14, bold=True))
    fig = svg.canvas(210, 145, parts)
    return mcq(
        stem=f"จากรูปคลี่ของลูกบาศก์ที่กำหนดให้ เมื่อพับเป็นลูกบาศก์แล้ว หน้าใดจะอยู่ตรงข้ามกับหน้า “{ask_face}”",
        figure=fig,
        correct=f"หน้า {ans_face}",
        wrongs=[
            W(f"หน้า {other_faces[0]}", "เมื่อพับขึ้นแล้วหน้านี้จะอยู่ติดกับหน้าที่ถาม ไม่ได้อยู่ตรงข้ามกัน", "concept"),
            W(f"หน้า {other_faces[1]}", "เมื่อพับขึ้นแล้วหน้านี้มีสันร่วมกับหน้าที่ถาม จึงเป็นหน้าประชิด", "concept"),
            W(f"หน้า {other_faces[2]}", "พับทบผิดทิศทาง หน้านี้จะตั้งฉากกับหน้าที่ถาม", "concept"),
        ],
        hint="เลือกหน้าหนึ่งเป็นฐาน แล้วจินตนาการพับหน้าข้างขึ้นมาตั้งฉากทีละด้าน (หน้าที่เรียงติดกันจะเว้น 1 ช่องจึงจะตรงข้ามกัน)",
        steps=[
            f"ยึดหน้าตรงกลางเป็นฐานแล้วพับหน้ารอบข้างตั้งฉากขึ้นมา 90°",
            f"หน้าที่อยู่เว้น 1 ช่องในแนวเดียวกันหรือพับมาปิดด้านตรงข้ามกับหน้า “{ask_face}” คือหน้า “{ans_face}”",
        ],
    )


@template("m.geo.solid3d", "hard")
def _opposite_dice_sum():
    # Standard die rule: opposite faces sum to 7, or custom rule on a net where opposite faces sum to K
    target_sum = random.choice([10, 12, 15, 20])
    a = random.randint(1, target_sum - 2)
    b = random.randint(1, target_sum - 2)
    c = random.randint(1, target_sum - 2)
    if len({a, b, c}) < 3:
        b += 1
        c += 2
    opp_a, opp_b, opp_c = target_sum - a, target_sum - b, target_sum - c
    cells = [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (2, 2)]
    # In this net: 0 <-> 2, 1 <-> 3, 4 <-> 5
    vals = [str(a), str(b), "x", "y", str(c), "z"]
    s = 38
    parts = []
    for (cx, cy), lab in zip(cells, vals):
        x, y_pos = 25 + cx * s, 15 + cy * s
        parts.append(svg.rect(x, y_pos, s, s, shade=(lab in ("x", "y", "z"))))
        parts.append(svg.label((x + s / 2, y_pos + s / 2), lab, size=14, bold=True))
    fig = svg.canvas(210, 145, parts)
    # Ask for 2x + y - z or x + 2y + z so student must identify which variable is opposite which number!
    ans = 2 * opp_a + opp_b - opp_c
    return mcq(
        stem=f"จากรูปคลี่ของลูกบาศก์ กำหนดให้ผลบวกของจำนวนบนหน้าที่อยู่ตรงข้ามกันทุกคู่เท่ากับ {target_sum} เท่ากันเสมอ จงหาค่าของ 2x + y − z",
        figure=fig,
        correct=str(ans),
        wrongs=[
            W(str(2 * opp_b + opp_a - opp_c), "จับคู่หน้าตรงข้ามของ x และ y สลับกัน", "concept"),
            W(str(2 * opp_a + opp_c - opp_b), "จับคู่หน้าตรงข้ามของ y และ z สลับกัน", "concept"),
            W(str(opp_a + opp_b + opp_c), "หาค่า x, y, z ถูกแต่แทนค่าเป็น x + y + z แทนที่จะเป็น 2x + y − z", "misread"),
            W(str(2 * opp_a + opp_b + opp_c), "นำค่า z ไปบวกแทนที่จะลบออก", "sign"),
        ],
        hint="ในแถวเรียง 4 ช่อง หน้าที่อยู่ห่างกัน 1 ช่องจะพับมาอยู่ตรงข้ามกัน",
        steps=[
            f"จากรูปคลี่ หน้า x อยู่ตรงข้ามกับ {a} ดังนั้น x = {target_sum} − {a} = {opp_a}",
            f"หน้า y อยู่ตรงข้ามกับ {b} ดังนั้น y = {target_sum} − {b} = {opp_b}",
            f"หน้า z อยู่ตรงข้ามกับ {c} ดังนั้น z = {target_sum} − {c} = {opp_c}",
            f"ดังนั้น 2x + y − z = 2({opp_a}) + {opp_b} − {opp_c} = {ans}",
        ],
    )


# ===========================================================================
# Skill 9: m.geo.counting — การนับรูปเรขาคณิต
# ===========================================================================
skill(
    "m.geo.counting",
    "m.geo",
    "การนับรูปเรขาคณิตในรูปซ้อน",
    lesson={
        "concept": (
            "การนับรูปเรขาคณิตที่ซ้อนกันต้องนับอย่างเป็นระบบโดยแยกตามขนาด (1 ช่อง, 2 ช่อง, ...) หรือใช้สูตรลัด "
            "เช่น สามเหลี่ยมที่แบ่งจากจุดยอดเป็น n ช่องและมีเส้นคั่นแนวนอน m ชั้น จะมีสามเหลี่ยมทั้งหมด m × [n(n + 1) ÷ 2] รูป "
            "และตารางขนาด c × r ช่อง จะมีรูปสี่เหลี่ยมมุมฉากทั้งหมด [c(c + 1)/2] × [r(r + 1)/2] รูป"
        ),
        "steps": [
            "แบ่งกรณีตามขนาดจากเล็กไปใหญ่ หรือใช้สูตรการนับตามโครงสร้างรูป",
            "สำหรับรูปสี่เหลี่ยมจัตุรัสในตาราง n × n: นับแยกขนาด 1×1, 2×2, ..., n×n แล้วบวกกัน (n² + (n−1)² + ... + 1²)",
            "ตรวจสอบว่าโจทย์ถาม 'รูปสี่เหลี่ยมจัตุรัส' หรือ 'รูปสี่เหลี่ยมมุมฉากทั้งหมด'",
        ],
        "example": {
            "q": "รูปสามเหลี่ยมที่มีเส้นลากจากจุดยอดลงมาแบ่งฐานออกเป็น 4 ช่อง มีรูปสามเหลี่ยมทั้งหมดกี่รูป",
            "steps": [
                "นับสามเหลี่ยมขนาด 1 ช่อง = 4 รูป, 2 ช่องติดกัน = 3 รูป, 3 ช่อง = 2 รูป, 4 ช่อง = 1 รูป",
                "รวมทั้งหมด = 4 + 3 + 2 + 1 = 10 รูป",
            ],
            "a": "10 รูป",
        },
        "mistakes": [
            "นับเฉพาะรูปย่อยช่องเล็กที่สุด ลืมนับรูปที่เกิดจากการรวมหลายช่องเข้าด้วยกัน",
            "สับสนระหว่างการนับรูปสี่เหลี่ยมจัตุรัส กับรูปสี่เหลี่ยมมุมฉาก (ซึ่งรวมสี่เหลี่ยมผืนผ้าด้วย)",
        ],
        "tips": [
            "จำสูตรลัด: เส้นแบ่งฐานสามเหลี่ยมเป็น n ช่อง มีสามเหลี่ยม 1 + 2 + ... + n = n(n+1)/2 รูป ถ้ามีเส้นขวาง m ชั้น ให้คูณด้วย m",
        ],
    },
    weight=1.0,
)


@template("m.geo.counting", "challenge")
def _count_subdivided_triangles():
    n = random.randint(3, 7)  # base subdivisions
    m = random.randint(1, 5)  # horizontal layers
    v_names = pick([("A", "B", "C"), ("P", "Q", "R"), ("X", "Y", "Z"), ("ก", "ข", "ค")])
    per_layer = n * (n + 1) // 2
    total = m * per_layer

    apex = (120, 18)
    y_base = 140
    x_left, x_right = 25, 215
    parts = [
        svg.polygon([apex, (x_left, y_base), (x_right, y_base)]),
        svg.point_label(apex, v_names[0], dy=-10),
        svg.point_label((x_left, y_base), v_names[1], dx=-10, dy=6),
        svg.point_label((x_right, y_base), v_names[2], dx=10, dy=6),
    ]
    for i in range(1, n):
        bx = x_left + (x_right - x_left) * i / n
        parts.append(svg.line(apex, (bx, y_base)))
    for j in range(1, m):
        t = j / m
        lx = apex[0] + (x_left - apex[0]) * t
        rx = apex[0] + (x_right - apex[0]) * t
        ly = apex[1] + (y_base - apex[1]) * t
        parts.append(svg.line((lx, ly), (rx, ly)))
    fig = svg.canvas(240, 160, parts)
    seq_str = " + ".join(str(k) for k in range(1, n + 1))
    return mcq(
        stem=f"จากรูปสามเหลี่ยม {v_names[0]}{v_names[1]}{v_names[2]} ที่กำหนดให้ มีรูปสามเหลี่ยมทั้งหมดกี่รูป (นับทุกขนาด)",
        figure=fig,
        correct=f"{total} รูป",
        wrongs=[
            W(f"{per_layer if m > 1 else n} รูป",
              "นับเฉพาะชั้นเดียว ลืมคูณจำนวนชั้นของเส้นขนานฐาน" if m > 1 else "นับเฉพาะรูปสามเหลี่ยมช่องเล็กที่สุด",
              "partial"),
            W(f"{n * m} รูป", "นับเฉพาะจำนวนช่องย่อย ไม่ได้นับรูปสามเหลี่ยมที่เกิดจากการรวมหลายช่อง", "partial"),
            W(f"{total + n} รูป", "นับซ้ำในชั้นเดียวกัน", "calc"),
            W(f"{total - m} รูป", "ลืมนับรูปสามเหลี่ยมใหญ่สุดของแต่ละชั้น", "partial"),
        ],
        hint="ในแต่ละชั้นของเส้นแนวนอนที่มีฐานแบ่งเป็น n ช่อง จะมีรูปสามเหลี่ยม 1 + 2 + ... + n รูป",
        steps=[
            f"ฐานถูกแบ่งออกเป็น {n} ช่อง ใน 1 ชั้นจึงมีสามเหลี่ยม = {seq_str} = {per_layer} รูป",
            f"มีเส้นแนวนอนรองรับฐานทั้งหมด {m} ชั้น",
            f"ดังนั้นมีรูปสามเหลี่ยมทั้งหมด = {per_layer} × {m} = {total} รูป",
        ],
    )


@template("m.geo.counting", "challenge")
def _count_squares_or_rects_in_grid():
    cols = random.randint(2, 6)
    rows = random.randint(2, 5)
    mode = random.choice(["squares", "rects", "non_square_rects"])
    cell_sz = 28 if max(cols, rows) >= 5 else 32
    fig = svg.canvas(20 + cols * cell_sz, 20 + rows * cell_sz, [
        svg.grid(10, 10, cols, rows, cell_sz),
    ])
    sq_terms = [(cols - k) * (rows - k) for k in range(min(cols, rows))]
    total_sq = sum(sq_terms)
    c_ways = cols * (cols + 1) // 2
    r_ways = rows * (rows + 1) // 2
    total_rect = c_ways * r_ways
    only_oblong = total_rect - total_sq

    if mode == "squares":
        breakdown = " + ".join(f"({cols - k}×{rows - k})" for k in range(min(cols, rows)))
        sums = " + ".join(str(v) for v in sq_terms)
        return mcq(
            stem=f"จากตารางขนาด {cols} × {rows} ช่อง (ทุกช่องเป็นรูปสี่เหลี่ยมจัตุรัสขนาดเท่ากัน) มี **รูปสี่เหลี่ยมจัตุรัส** ทั้งหมดกี่รูป",
            figure=fig,
            correct=f"{total_sq} รูป",
            wrongs=[
                W(f"{cols * rows} รูป", "นับเฉพาะรูปสี่เหลี่ยมจัตุรัสขนาด 1×1 ช่อง ลืมนับขนาด 2×2 ขึ้นไป", "partial"),
                W(f"{total_rect} รูป", "เผลอนับรูปสี่เหลี่ยมมุมฉากทั้งหมด (รวมสี่เหลี่ยมผืนผ้าด้วย)", "misread"),
                W(f"{total_sq - 1} รูป", "นับขนาดใหญ่สุดตกหล่นไป 1 รูป", "partial"),
                W(f"{total_sq + 2} รูป", "บวกจำนวนรูปในแต่ละขนาดผิดพลาด", "calc"),
            ],
            hint="แยกนับตามขนาดของจัตุรัส: ขนาด 1×1, ขนาด 2×2, ... แล้วนำมารวมกัน",
            steps=[
                f"นับแยกตามขนาดของรูปสี่เหลี่ยมจัตุรัสตั้งแต่ 1×1 ไปจนถึง {min(cols, rows)}×{min(cols, rows)}:",
                f"จำนวนรูป = {breakdown} = {sums}",
                f"รวมมีรูปสี่เหลี่ยมจัตุรัสทั้งหมด {total_sq} รูป",
            ],
        )
    if mode == "non_square_rects":
        return mcq(
            stem=f"จากตารางขนาด {cols} × {rows} ช่อง (ทุกช่องเป็นจัตุรัสขนาด 1×1) มี **รูปสี่เหลี่ยมผืนผ้าที่ไม่ใช่รูปสี่เหลี่ยมจัตุรัส** ทั้งหมดกี่รูป",
            figure=fig,
            correct=f"{only_oblong} รูป",
            wrongs=[
                W(f"{total_rect} รูป", "ตอบจำนวนรูปสี่เหลี่ยมมุมฉากทั้งหมด ลืมหักรูปสี่เหลี่ยมจัตุรัสออก", "partial"),
                W(f"{total_sq} รูป", "ตอบจำนวนรูปสี่เหลี่ยมจัตุรัส แทนที่จะตอบรูปสี่เหลี่ยมผืนผ้าที่ไม่ใช่จัตุรัส", "misread"),
                W(f"{total_rect - cols * rows} รูป", "หักออกเฉพาะช่องจัตุรัสขนาด 1×1 ลืมหักจัตุรัสขนาด 2×2 ขึ้นไป", "partial"),
                W(f"{only_oblong + 2} รูป", "ลบจำนวนรูปสี่เหลี่ยมจัตุรัสผิดพลาด", "calc"),
            ],
            hint="หาจำนวนรูปสี่เหลี่ยมมุมฉากทั้งหมดก่อน แล้วลบด้วยจำนวนรูปสี่เหลี่ยมจัตุรัสทุกขนาด",
            steps=[
                f"จำนวนรูปสี่เหลี่ยมมุมฉากทั้งหมด = {c_ways} × {r_ways} = {total_rect} รูป",
                f"จำนวนรูปสี่เหลี่ยมจัตุรัสทุกขนาด = {' + '.join(str(v) for v in sq_terms)} = {total_sq} รูป",
                f"ดังนั้นมีสี่เหลี่ยมผืนผ้าที่ไม่ใช่จัตุรัส = {total_rect} − {total_sq} = {only_oblong} รูป",
            ],
        )
    return mcq(
        stem=f"จากตารางขนาด {cols} × {rows} ช่อง มี **รูปสี่เหลี่ยมมุมฉาก** (รวมทั้งจัตุรัสและผืนผ้า) ทั้งหมดกี่รูป",
        figure=fig,
        correct=f"{total_rect} รูป",
        wrongs=[
            W(f"{total_sq} รูป", "นับเฉพาะรูปสี่เหลี่ยมจัตุรัส ลืมนับรูปสี่เหลี่ยมผืนผ้า", "misread"),
            W(f"{cols * rows} รูป", "นับเฉพาะช่องเล็กขนาด 1×1 ช่อง", "partial"),
            W(f"{c_ways + r_ways} รูป", "นำจำนวนวิธีเลือกแนวนอนและแนวตั้งมาบวกกันแทนที่จะคูณกัน", "formula"),
            W(f"{only_oblong} รูป", "นับเฉพาะสี่เหลี่ยมผืนผ้า ลืมรวมรูปสี่เหลี่ยมจัตุรัส", "partial"),
        ],
        hint="จำนวนสี่เหลี่ยมมุมฉากในตาราง c × r ช่อง = (1 + 2 + ... + c) × (1 + 2 + ... + r)",
        steps=[
            f"จำนวนวิธีเลือกความกว้างแนวนอน ({cols} ช่อง) = 1 + ... + {cols} = {c_ways} วิธี",
            f"จำนวนวิธีเลือกความสูงแนวตั้ง ({rows} ช่อง) = 1 + ... + {rows} = {r_ways} วิธี",
            f"มีรูปสี่เหลี่ยมมุมฉากทั้งหมด = {c_ways} × {r_ways} = {total_rect} รูป",
        ],
    )
