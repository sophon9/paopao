"""Statistics, charts, and probability question bank for topic m.data (สถิติ กราฟ และความน่าจะเป็น)."""

from fractions import Fraction
import math
import random

from backend.bank import svg
from backend.bank.core import W, dec, frac, mcq, name_th, num, pick, skill, template


# ===========================================================================
# Skill 1: m.data.central — ค่าเฉลี่ยเลขคณิต มัธยฐาน ฐานนิยม และพิสัย
# ===========================================================================
skill(
    "m.data.central",
    "m.data",
    "ค่าเฉลี่ยเลขคณิต มัธยฐาน ฐานนิยม และพิสัย",
    lesson={
        "concept": (
            "ค่าเฉลี่ยเลขคณิต = ผลรวมของข้อมูลทั้งหมด ÷ จำนวนข้อมูลทั้งหมด, "
            "มัธยฐาน = ค่าที่อยู่ตรงกลางเมื่อเรียงข้อมูลจากน้อยไปมาก (ถ้ามีจำนวนคู่ให้นำสองตัวกลางบวกกันหารด้วย 2), "
            "ฐานนิยม = ข้อมูลที่มีความถี่สูงสุด (ซ้ำกันมากที่สุด) และ พิสัย = ค่าสูงสุด − ค่าต่ำสุด"
        ),
        "steps": [
            "เรียงลำดับข้อมูลจากน้อยไปมากก่อนเสมอ เพื่อป้องกันการหามัธยฐานและพิสัยผิดพลาด",
            "ตรวจสอบจำนวนข้อมูล (N) ว่ามีกี่จำนวน",
            "เลือกคำนวณค่าสถิติตามที่โจทย์ถาม",
        ],
        "example": {
            "q": "ข้อมูลชุดหนึ่งคือ 12, 8, 15, 8, 17 จงหาค่าเฉลี่ย มัธยฐาน และฐานนิยม",
            "steps": [
                "เรียงจากน้อยไปมาก: 8, 8, 12, 15, 17",
                "ค่าเฉลี่ย = (8 + 8 + 12 + 15 + 17) ÷ 5 = 60 ÷ 5 = 12",
                "มัธยฐาน (ตัวกลาง) = 12 และฐานนิยม (ซ้ำมากสุด) = 8",
            ],
            "a": "ค่าเฉลี่ย = 12, มัธยฐาน = 12, ฐานนิยม = 8",
        },
        "mistakes": [
            "หยิบตัวเลขที่อยู่ตรงกลางของโจทย์มาตอบเป็นมัธยฐานเลย โดยลืมเรียงข้อมูลจากน้อยไปมากก่อน",
            "เมื่อข้อมูลมีจำนวนคู่ เผลอหยิบตัวใดตัวหนึ่งแทนที่จะหาค่าเฉลี่ยของ 2 ตัวกลาง",
        ],
        "tips": [
            "ก่อนทำโจทย์สถิติชุดตัวเลข ให้ขีดฆ่าพร้อมเขียนเรียงจากน้อยไปมากทุกครั้ง จะเห็นทั้งค่าต่ำสุด ค่าสูงสุด มัธยฐาน และฐานนิยมทันที!",
        ],
    },
    weight=1.4,
)


@template("m.data.central", "easy")
def _basic_mean_mode_range():
    base = random.randint(10, 35)
    # 5 numbers with a unique mode and integer mean
    # Let's pick mode m = base, two copies of m, and 3 other distinct numbers summing to 3*base + 5*k
    offsets = pick([(-4, -1, 5), (-5, 1, 4), (-6, 2, 4), (-3, -2, 5), (-7, 2, 5), (-8, 3, 5)])
    data = [base, base, base + offsets[0], base + offsets[1], base + offsets[2]]
    random.shuffle(data)
    ordered = sorted(data)
    mean_val = sum(data) // 5
    mode_val = base
    range_val = ordered[-1] - ordered[0]
    ask = random.choice(["mean", "range", "sum_mode_range"])
    data_str = ", ".join(str(x) for x in data)
    if ask == "mean":
        return mcq(
            stem=f"ข้อมูลชุดหนึ่งประกอบด้วย {data_str} ค่าเฉลี่ยเลขคณิตของข้อมูลชุดนี้เท่ากับเท่าใด",
            correct=str(mean_val),
            wrongs=[
                W(str(sum(data)), "หาเฉพาะผลรวมของข้อมูล ลืมหารด้วยจำนวนข้อมูล (5 จำนวน)", "partial"),
                W(str(range_val), "ตอบค่าพิสัย (ค่าสูงสุด − ค่าต่ำสุด) แทนค่าเฉลี่ย", "concept"),
                W(str(mean_val + 2), "บวกเลขหรือหารเลขผิดพลาด", "calc"),
                W(str(mean_val - 2), "บวกเลขหรือหารเลขผิดพลาด", "calc"),
            ],
            hint="ค่าเฉลี่ยเลขคณิต = ผลรวมของข้อมูลทั้งหมด ÷ จำนวนข้อมูลทั้งหมด",
            steps=[
                f"ผลรวมของข้อมูล = {' + '.join(str(x) for x in data)} = {sum(data)}",
                f"มีข้อมูลทั้งหมด 5 จำนวน ค่าเฉลี่ย = {sum(data)} ÷ 5 = {mean_val}",
            ],
        )
    if ask == "range":
        return mcq(
            stem=f"กำหนดข้อมูลชุดหนึ่งคือ {data_str} พิสัยของข้อมูลชุดนี้มีค่าเท่าใด",
            correct=str(range_val),
            wrongs=[
                W(str(abs(data[-1] - data[0]) if abs(data[-1] - data[0]) != range_val else range_val + 3),
                  "นำตัวสุดท้ายลบตัวแรกโดยไม่ได้หาค่าสูงสุดและค่าต่ำสุด", "concept"),
                W(str(mode_val), "ตอบค่าฐานนิยมแทนค่าพิสัย", "concept"),
                W(str(ordered[-1] + ordered[0]), "นำค่าสูงสุดบวกค่าต่ำสุด แทนที่จะนำมาลบกัน", "formula"),
            ],
            hint="พิสัย = ค่าสูงสุด − ค่าต่ำสุด",
            steps=[
                f"เรียงข้อมูลจากน้อยไปมาก: {', '.join(str(x) for x in ordered)}",
                f"ค่าสูงสุดคือ {ordered[-1]} และค่าต่ำสุดคือ {ordered[0]}",
                f"พิสัย = {ordered[-1]} − {ordered[0]} = {range_val}",
            ],
        )
    ans = mode_val + range_val
    return mcq(
        stem=f"จากข้อมูล {data_str} ผลบวกของ **ฐานนิยม** และ **พิสัย** ของข้อมูลชุดนี้มีค่าเท่าใด",
        correct=str(ans),
        wrongs=[
            W(str(mode_val), "ตอบเฉพาะฐานนิยม ลืมบวกค่าพิสัย", "partial"),
            W(str(range_val), "ตอบเฉพาะค่าพิสัย ลืมบวกค่าฐานนิยม", "partial"),
            W(str(abs(mode_val - range_val)), "นำฐานนิยมและพิสัยมาลบกันแทนที่จะบวกกัน", "misread"),
        ],
        hint="ฐานนิยมคือตัวที่ซ้ำมากที่สุด และพิสัยคือ ค่าสูงสุด − ค่าต่ำสุด",
        steps=[
            f"เรียงข้อมูลจากน้อยไปมาก: {', '.join(str(x) for x in ordered)}",
            f"ฐานนิยม (ซ้ำมากที่สุด) = {mode_val}",
            f"พิสัย = {ordered[-1]} − {ordered[0]} = {range_val}",
            f"ผลบวกของฐานนิยมและพิสัย = {mode_val} + {range_val} = {ans}",
        ],
    )


@template("m.data.central", "medium")
def _median_unsorted_trap():
    is_even = random.choice([True, False])
    start = random.randint(12, 45)
    if is_even:
        steps = [0, random.randint(2, 4), random.randint(5, 8), random.randint(10, 14), random.randint(15, 19), random.randint(20, 25)]
        ordered = [start + s for s in steps]
        # Arrange unsorted so that the middle two in raw order do NOT match the sorted middle two
        raw = [ordered[4], ordered[0], ordered[5], ordered[1], ordered[3], ordered[2]]
        med = (ordered[2] + ordered[3]) / 2
        med_str = dec(med, 1)
        trap_raw_mid = dec((raw[2] + raw[3]) / 2, 1)
        return mcq(
            stem=f"คะแนนสอบของนักเรียน 6 คน เป็นดังนี้: {', '.join(str(x) for x in raw)} มัธยฐานของคะแนนสอบชุดนี้เท่ากับเท่าใด",
            correct=med_str,
            wrongs=[
                W(trap_raw_mid, "หาค่าเฉลี่ยของ 2 ตัวกลางทันทีโดยลืมเรียงข้อมูลจากน้อยไปมากก่อน", "trap"),
                W(str(ordered[2]), "ตอบเฉพาะตัวที่ 3 หลังเรียงลำดับ ลืมเฉลี่ยกับตัวที่ 4", "partial"),
                W(str(ordered[3]), "ตอบเฉพาะตัวที่ 4 หลังเรียงลำดับ ลืมเฉลี่ยกับตัวที่ 3", "partial"),
            ],
            hint="ต้องเรียงข้อมูลจากน้อยไปมากก่อน แล้วนำข้อมูลคู่กลาง (ตัวที่ 3 และ 4) มาบวกกันหารด้วย 2",
            steps=[
                f"เรียงข้อมูลจากน้อยไปมาก: {', '.join(str(x) for x in ordered)}",
                f"ข้อมูลมี 6 จำนวน คู่กลางคือตัวที่ 3 ({ordered[2]}) และตัวที่ 4 ({ordered[3]})",
                f"มัธยฐาน = ({ordered[2]} + {ordered[3]}) ÷ 2 = {med_str}",
            ],
        )
    steps = [0, random.randint(2, 5), random.randint(6, 9), random.randint(10, 14),
             random.randint(15, 18), random.randint(19, 22), random.randint(23, 27)]
    ordered = [start + s for s in steps]
    raw = [ordered[5], ordered[1], ordered[6], ordered[0], ordered[4], ordered[2], ordered[3]]
    med = ordered[3]
    trap_raw = raw[3]
    return mcq(
        stem=f"ข้อมูลชุดหนึ่งมี 7 จำนวน คือ {', '.join(str(x) for x in raw)} มัธยฐานของข้อมูลชุดนี้คือข้อใด",
        correct=str(med),
        wrongs=[
            W(str(trap_raw), "หยิบตัวที่ 4 จากโจทย์มาตอบเลยโดยลืมเรียงลำดับจากน้อยไปมากก่อน", "trap"),
            W(str(ordered[2]), "เรียงลำดับแล้วหยิบตัวที่ 3 แทนที่จะเป็นตัวที่ 4 (ตรงกลาง)", "calc"),
            W(str(ordered[4]), "เรียงลำดับแล้วหยิบตัวที่ 5 แทนที่จะเป็นตัวที่ 4 (ตรงกลาง)", "calc"),
        ],
        hint="เรียงข้อมูลจากน้อยไปมากก่อน ตัวที่อยู่ตรงกลาง (ตัวที่ 4 จาก 7 ตัว) คือมัธยฐาน",
        steps=[
            f"เรียงข้อมูลจากน้อยไปมาก: {', '.join(str(x) for x in ordered)}",
            f"ข้อมูลมี 7 จำนวน ตัวที่อยู่ตรงกลางคือตัวที่ 4 ซึ่งมีค่าเท่ากับ {med}",
        ],
    )


@template("m.data.central", "hard")
def _ordered_data_find_unknowns():
    # 5 positive integers in ascending order: a, b, c, d, d (so mode is d, median is c)
    # Given: mode, median, range, and mean -> find b!
    a = random.randint(8, 22)
    c = a + random.randint(5, 10)
    d = c + random.randint(3, 8)
    # Choose b between a+1 and c-1 such that a+b+c+2d is divisible by 5
    rem = (a + c + 2 * d) % 5
    b_candidates = [x for x in range(a + 1, c) if (x + rem) % 5 == 0]
    if not b_candidates:
        return None
    b = b_candidates[0]
    total = a + b + c + 2 * d
    mean_val = total // 5
    rng = d - a
    return mcq(
        stem=f"ข้อมูลชุดหนึ่งมี 5 จำนวน เรียงจากน้อยไปมากได้เป็น a, b, {c}, d, d ถ้าข้อมูลชุดนี้มีฐานนิยมเท่ากับ {d} พิสัยเท่ากับ {rng} และค่าเฉลี่ยเลขคณิตเท่ากับ {mean_val} แล้ว b มีค่าเท่าใด",
        correct=str(b),
        wrongs=[
            W(str(a), "ตอบค่าต่ำสุด a แทนที่จะตอบค่า b", "misread"),
            W(str(total - (c + 2 * d)), "หาผลบวก a + b ได้แล้วลืมลบค่า a ออก", "partial"),
            W(str(b + 5), "คำนวณผลรวมทั้งหมดจากค่าเฉลี่ยผิดพลาด", "calc"),
            W(str(c - 1 if c - 1 != b else b - 1), "เดาว่า b มีค่าน้อยกว่ามัธยฐานอยู่ 1 โดยไม่ได้ใช้ค่าเฉลี่ย", "concept"),
        ],
        hint="หาค่า a จากพิสัย (d − a = พิสัย) และหาผลรวมทั้ง 5 จำนวนจาก ค่าเฉลี่ย × 5",
        steps=[
            f"ฐานนิยมคือ {d} ดังนั้น d = {d}",
            f"พิสัย = ค่าสูงสุด − ค่าต่ำสุด จะได้ {d} − a = {rng} ดังนั้น a = {a}",
            f"ผลรวมของข้อมูลทั้ง 5 จำนวน = {mean_val} × 5 = {total}",
            f"จะได้ {a} + b + {c} + {d} + {d} = {total} ดังนั้น b = {total} − {a + c + 2 * d} = {b}",
        ],
    )


# ===========================================================================
# Skill 2: m.data.mean_adv — โจทย์ปัญหาค่าเฉลี่ยและการเปลี่ยนแปลงข้อมูล
# ===========================================================================
skill(
    "m.data.mean_adv",
    "m.data",
    "โจทย์ปัญหาค่าเฉลี่ยและการเปลี่ยนแปลงข้อมูล",
    lesson={
        "concept": (
            "หัวใจของโจทย์ค่าเฉลี่ยคือการเปลี่ยนกลับเป็น **ผลรวม**: ผลรวมของข้อมูล = ค่าเฉลี่ย × จำนวนข้อมูล "
            "เมื่อมีการเพิ่ม ลด หรือแก้ไขข้อมูล ให้คำนวณผ่านผลรวมเดิมและผลรวมใหม่เสมอ"
        ),
        "steps": [
            "ขั้นที่ 1: หา 'ผลรวมเดิม' = ค่าเฉลี่ยเดิม × จำนวนข้อมูลเดิม",
            "ขั้นที่ 2: ปรับผลรวมตามเงื่อนไขโจทย์ (บวกคนเข้า / ลบคนออก / ลบค่าที่อ่านผิดแล้วบวกค่าที่ถูก)",
            "ขั้นที่ 3: หาค่าเฉลี่ยใหม่หรือค่าของข้อมูลที่ต้องการ",
        ],
        "example": {
            "q": "นักเรียน 4 คนมีน้ำหนักเฉลี่ย 38 กก. เมื่อรวมกับครูอีก 1 คน ทำให้น้ำหนักเฉลี่ยของทั้ง 5 คนเป็น 42 กก. ครูหนักกี่กิโลกรัม",
            "steps": [
                "น้ำหนักรวมของนักเรียน 4 คน = 38 × 4 = 152 กก.",
                "น้ำหนักรวมของ 5 คน (รวมครู) = 42 × 5 = 210 กก.",
                "น้ำหนักของครู = 210 − 152 = 58 กก.",
            ],
            "a": "58 กก.",
        },
        "mistakes": [
            "นำค่าเฉลี่ยของสองกลุ่มที่มีจำนวนคนไม่เท่ากันมาบวกกันแล้วหารด้วย 2 โดยตรง",
            "เมื่ออ่านข้อมูลผิดตัวหนึ่ง เผลอนำผลต่างไปบวกลบกับค่าเฉลี่ยโดยตรงโดยลืมหารด้วยจำนวนข้อมูล",
        ],
        "tips": [
            "เจอคำว่า 'ค่าเฉลี่ย' เมื่อไร ให้เขียน 'ผลรวม = ค่าเฉลี่ย × จำนวน' ทันที!",
        ],
    },
    weight=1.6,
)


@template("m.data.mean_adv", "medium")
def _mean_find_next_score():
    n = random.randint(3, 6)
    old_mean = random.randint(65, 82)
    target_mean = old_mean + random.randint(2, 4)
    old_sum = n * old_mean
    new_sum = (n + 1) * target_mean
    needed = new_sum - old_sum
    if needed > 100:
        return None
    person = name_th()
    return mcq(
        stem=f"{person}สอบวิชาคณิตศาสตร์ไปแล้ว {n} ครั้ง ได้คะแนนเฉลี่ย {old_mean} คะแนน ถ้าต้องการให้คะแนนเฉลี่ยของการสอบทั้ง {n + 1} ครั้ง เพิ่มขึ้นเป็น {target_mean} คะแนน ในการสอบครั้งที่ {n + 1} {person}ต้องทำคะแนนให้ได้กี่คะแนน",
        correct=f"{needed} คะแนน",
        wrongs=[
            W(f"{target_mean} คะแนน", "คิดว่าสอบครั้งต่อไปได้เท่ากับค่าเฉลี่ยเป้าหมายก็พอ ลืมชดเชยครั้งก่อน ๆ", "concept"),
            W(f"{target_mean + (target_mean - old_mean)} คะแนน", "บวกชดเชยให้เพียงครั้งเดียว ลืมว่าต้องชดเชยให้ทั้ง " + str(n) + " ครั้งก่อนหน้า", "partial"),
            W(f"{new_sum - old_mean} คะแนน", "นำผลรวมใหม่ลบด้วยค่าเฉลี่ยเดิมแทนที่จะลบด้วยผลรวมเดิม", "formula"),
        ],
        hint=f"หาคะแนนรวมของการสอบ {n + 1} ครั้ง ลบด้วยคะแนนรวมของการสอบ {n} ครั้งแรก",
        steps=[
            f"คะแนนรวม {n} ครั้งแรก = {old_mean} × {n} = {old_sum} คะแนน",
            f"คะแนนรวมที่ต้องการเมื่อครบ {n + 1} ครั้ง = {target_mean} × {n + 1} = {new_sum} คะแนน",
            f"ดังนั้นครั้งที่ {n + 1} ต้องทำได้ = {new_sum} − {old_sum} = {needed} คะแนน",
        ],
    )


@template("m.data.mean_adv", "hard")
def _weighted_mean_two_groups():
    n1 = random.choice([10, 12, 15, 18, 20, 24])
    n2 = random.choice([15, 20, 25, 30, 32])
    if n1 == n2:
        n2 += 10
    total_n = n1 + n2
    # Choose m1, m2 so (n1*m1 + n2*m2) is divisible by total_n
    m1 = random.randint(60, 85)
    step = total_n // math.gcd(n2, total_n)
    k = random.randint(1, 3)
    m2 = m1 + k * step
    if m2 > 98:
        m2 = m1 - k * step
    total_sum = n1 * m1 + n2 * m2
    combined_mean = total_sum // total_n
    simple_avg = dec((m1 + m2) / 2, 1)
    return mcq(
        stem=f"นักเรียนห้อง ก มี {n1} คน สอบได้คะแนนเฉลี่ย {m1} คะแนน และนักเรียนห้อง ข มี {n2} คน สอบได้คะแนนเฉลี่ย {m2} คะแนน ถ้านำนักเรียนทั้งสองห้องมารวมกัน คะแนนเฉลี่ยของนักเรียนทั้งหมดเท่ากับกี่คะแนน",
        correct=f"{combined_mean} คะแนน",
        wrongs=[
            W(f"{simple_avg} คะแนน", "นำค่าเฉลี่ยของสองห้องมาบวกกันแล้วหารด้วย 2 โดยไม่ได้ถ่วงน้ำหนักตามจำนวนนักเรียน", "trap"),
            W(f"{dec(total_sum / n1, 1)} คะแนน", "หารด้วยจำนวนนักเรียนเพียงห้องเดียว", "partial"),
            W(f"{combined_mean + 2} คะแนน", "คำนวณการหารคะแนนรวมผิดพลาด", "calc"),
        ],
        hint="ต้องหาคะแนนรวมของห้อง ก และคะแนนรวมของห้อง ข มาบวกกัน แล้วหารด้วยจำนวนนักเรียนทั้งหมด",
        steps=[
            f"คะแนนรวมของห้อง ก = {n1} × {m1} = {num(n1 * m1)} คะแนน",
            f"คะแนนรวมของห้อง ข = {n2} × {m2} = {num(n2 * m2)} คะแนน",
            f"คะแนนรวมทั้งสองห้อง = {num(n1 * m1)} + {num(n2 * m2)} = {num(total_sum)} คะแนน",
            f"จำนวนนักเรียนทั้งหมด = {n1} + {n2} = {total_n} คน",
            f"ดังนั้นคะแนนเฉลี่ยรวม = {num(total_sum)} ÷ {total_n} = {combined_mean} คะแนน",
        ],
    )


@template("m.data.mean_adv", "challenge")
def _mean_misread_correction():
    n = random.choice([8, 10, 12, 15, 20, 25])
    wrong_mean = random.randint(45, 82)
    diff_mult = random.choice([1, 2, 3, -1, -2, -3])
    delta = diff_mult * n
    true_val = random.randint(40, 90)
    read_val = true_val - delta
    if read_val < 10 or read_val > 99:
        return None
    wrong_sum = n * wrong_mean
    true_sum = wrong_sum - read_val + true_val
    true_mean = true_sum // n
    return mcq(
        stem=f"ในการหาค่าเฉลี่ยเลขคณิตของข้อมูล {n} จำนวน คำนวณได้ค่าเฉลี่ยเท่ากับ {wrong_mean} แต่ภายหลังพบว่าอ่านข้อมูลผิดไป 1 จำนวน คือข้อมูลจริงเป็น {true_val} แต่อ่านผิดเป็น {read_val} ค่าเฉลี่ยเลขคณิตที่ถูกต้องมีค่าเท่าใด",
        correct=str(true_mean),
        wrongs=[
            W(str(wrong_mean - diff_mult), "บวกลบค่าที่อ่านผิดกับค่าที่ถูกสลับทิศทางกัน", "sign"),
            W(str(wrong_mean + delta), f"นำผลต่าง ({abs(delta)}) ไปปรับที่ค่าเฉลี่ยโดยตรง ลืมหารด้วยจำนวนข้อมูล {n} จำนวน", "trap"),
            W(str(true_sum), "ตอบผลรวมที่ถูกต้องแทนที่จะหารด้วยจำนวนข้อมูลเพื่อหาค่าเฉลี่ย", "partial"),
        ],
        hint="ผลรวมที่ถูกต้อง = ผลรวมเดิม − ค่าที่อ่านผิด + ค่าที่ถูกต้อง แล้วจึงหารด้วยจำนวนข้อมูล",
        steps=[
            f"ผลรวมเดิมที่คำนวณไว้ = {wrong_mean} × {n} = {num(wrong_sum)}",
            f"ผลรวมที่ถูกต้อง = {num(wrong_sum)} − {read_val} + {true_val} = {num(true_sum)}",
            f"ดังนั้นค่าเฉลี่ยที่ถูกต้อง = {num(true_sum)} ÷ {n} = {true_mean}",
        ],
    )


# ===========================================================================
# Skill 3: m.data.bar — การอ่านและวิเคราะห์แผนภูมิแท่ง
# ===========================================================================
skill(
    "m.data.bar",
    "m.data",
    "การอ่านและวิเคราะห์แผนภูมิแท่ง",
    lesson={
        "concept": (
            "แผนภูมิแท่งแสดงข้อมูลด้วยความสูงของแท่งเทียบกับแกนตัวเลข "
            "ในการทำข้อสอบต้องอ่านค่าของแต่ละแท่งให้แม่นยำ แล้วนำมาหาผลรวม ผลต่าง ค่าเฉลี่ย หรือร้อยละตามที่โจทย์ถาม"
        ),
        "steps": [
            "ดูชื่อแผนภูมิ หน่วยบนแกนตั้ง และสเกลของเส้นตาราง",
            "เขียนตัวเลขกำกับบนยอดแท่งแต่ละแท่งก่อนเริ่มคำนวณ",
            "คำนวณตามสิ่งที่โจทย์ถาม (เช่น มากกว่ากี่ชิ้น คิดเป็นร้อยละเท่าใด หรือค่าเฉลี่ยเป็นเท่าใด)",
        ],
        "example": {
            "q": "ยอดขายหนังสือวันจันทร์–พุธ เป็น 30, 45 และ 60 เล่ม ยอดขายเฉลี่ยต่อวันเป็นกี่เล่ม",
            "steps": [
                "ยอดขายรวม 3 วัน = 30 + 45 + 60 = 135 เล่ม",
                "ยอดขายเฉลี่ย = 135 ÷ 3 = 45 เล่ม",
            ],
            "a": "45 เล่ม",
        },
        "mistakes": [
            "อ่านสเกลแกนตั้งผิดเมื่อ 1 ช่องไม่ได้แทน 1 หน่วย",
            "เมื่อโจทย์ถามว่า A มากกว่า B คิดเป็นร้อยละเท่าใดของ B เผลอไปเทียบส่วนด้วย A หรือผลรวมทั้งหมด",
        ],
        "tips": [
            "เขียนตัวเลขไว้เหนือแท่งทุกแท่งตั้งแต่ครั้งแรกที่อ่านรูป จะช่วยประหยัดเวลาเมื่อมีคำถามต่อเนื่องหลายข้อ",
        ],
    },
    weight=1.4,
)


@template("m.data.bar", "easy")
def _bar_chart_read_compare():
    cats = pick([
        (["จันทร์", "อังคาร", "พุธ", "พฤหัสฯ", "ศุกร์"], "จำนวนหนังสือที่ยืมในห้องสมุด", "เล่ม"),
        (["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค."], "ยอดขายจักรยานของร้านค้า", "คัน"),
        (["ป.2", "ป.3", "ป.4", "ป.5", "ป.6"], "จำนวนนักเรียนที่เข้าร่วมชมรมดนตรี", "คน"),
    ])
    labels, title, unit = cats
    step = random.choice([10, 20])
    vals = [step * random.randint(2, 9) for _ in range(5)]
    if len(set(vals)) < 4:
        vals[0] += step
        vals[1] = max(step, vals[1] - step)
    fig = svg.bar_chart(labels, vals, title=title, unit=unit, step=step)
    hi = max(vals)
    lo = min(vals)
    diff = hi - lo
    total = sum(vals)
    ask_total = random.choice([True, False])
    if ask_total:
        return mcq(
            stem=f"จากแผนภูมิแท่ง {title}รวมทั้ง 5 รายการเป็นเท่าใด",
            figure=fig,
            correct=f"{num(total)} {unit}",
            wrongs=[
                W(f"{num(total - lo)} {unit}", "บวกข้อมูลตกหล่นไป 1 แท่ง", "partial"),
                W(f"{num(total + step)} {unit}", "อ่านค่าจากเส้นตารางคลาดเคลื่อนไป 1 ช่องสเกล", "detail"),
                W(f"{num(diff)} {unit}", "ตอบผลต่างระหว่างค่าสูงสุดกับค่าต่ำสุดแทนผลรวม", "misread"),
            ],
            hint="อ่านค่าความสูงของทั้ง 5 แท่งจากแกนตั้ง แล้วนำมาบวกกันทั้งหมด",
            steps=[
                f"อ่านค่าแต่ละแท่งได้ดังนี้: {', '.join(f'{l} = {v}' for l, v in zip(labels, vals))} {unit}",
                f"รวมทั้งหมด = {' + '.join(str(v) for v in vals)} = {num(total)} {unit}",
            ],
        )
    return mcq(
        stem=f"จากแผนภูมิแท่ง รายการที่มีจำนวนมากที่สุดมากกว่าน้อยที่สุดอยู่กี่{unit}",
        figure=fig,
        correct=f"{num(diff)} {unit}",
        wrongs=[
            W(f"{num(hi)} {unit}", "ตอบเฉพาะค่าที่มากที่สุด ลืมลบด้วยค่าที่น้อยที่สุด", "partial"),
            W(f"{num(hi + lo)} {unit}", "นำค่าสูงสุดและต่ำสุดมาบวกกันแทนที่จะลบกัน", "sign"),
            W(f"{num(abs(vals[-1] - vals[0]) or step)} {unit}", "นำแท่งแรกกับแท่งสุดท้ายมาลบกันโดยไม่ได้ดูแท่งที่สูงที่สุดและต่ำที่สุด", "detail"),
        ],
        hint="หาแท่งที่สูงที่สุดและแท่งที่เตี้ยที่สุด แล้วนำค่ามาลบกัน",
        steps=[
            f"แท่งที่มากที่สุดมีค่า {hi} {unit} และแท่งที่น้อยที่สุดมีค่า {lo} {unit}",
            f"ต่างกันอยู่ = {hi} − {lo} = {num(diff)} {unit}",
        ],
    )


@template("m.data.bar", "hard", group=True)
def _bar_chart_group_set():
    labels = ["ชมรมวิทย์", "ชมรมคณิต", "ชมรมศิลปะ", "ชมรมกีฬา", "ชมรมดนตรี"]
    # Choose values summing to 200 or 250 so percentage is clean, and divisible by 5 for mean
    mult = random.randint(2, 5)
    raw = [4, 6, 3, 7, 5]  # sum = 25
    random.shuffle(raw)
    vals = [r * mult * 2 for r in raw]  # sum = 50 * mult, divisible by 5
    total = sum(vals)
    mean_val = total // 5
    fig = svg.bar_chart(labels, vals, title="จำนวนสมาชิกชมรมต่าง ๆ ของโรงเรียนแห่งหนึ่ง", unit="คน", show_values=True)

    # Q1: How many clubs have membership strictly above average, or difference between top 2 and bottom 2
    above = [l for l, v in zip(labels, vals) if v > mean_val]
    top2_idx = sorted(range(5), key=lambda i: vals[i], reverse=True)
    i_max, i_min = top2_idx[0], top2_idx[-1]
    pct_max = dec(vals[i_max] * 100 / total, 1)

    q1 = mcq(
        stem="จากแผนภูมิแท่ง ค่าเฉลี่ยของจำนวนสมาชิกต่อชมรมเป็นกี่คน และมีกี่ชมรมที่มีสมาชิกมากกว่าค่าเฉลี่ย",
        figure=fig,
        correct=f"ค่าเฉลี่ย {mean_val} คน และมี {len(above)} ชมรม",
        wrongs=[
            W(f"ค่าเฉลี่ย {mean_val} คน และมี {len(above) + 1} ชมรม",
              f"นับรวมชมรมที่มีสมาชิกเท่ากับค่าเฉลี่ย ({mean_val} คน) เข้าไปด้วย ทั้งที่โจทย์ถามว่า 'มากกว่าค่าเฉลี่ย'", "trap"),
            W(f"ค่าเฉลี่ย {total} คน และมี {len(above)} ชมรม", "ใช้ผลรวมทั้งหมดแทนค่าเฉลี่ย", "concept"),
            W(f"ค่าเฉลี่ย {mean_val + 4} คน และมี {len(above)} ชมรม", "บวกเลขหรือหารค่าเฉลี่ยผิดพลาด", "calc"),
        ],
        hint="หาค่าเฉลี่ยจาก ผลรวมทั้งหมด ÷ 5 แล้วนับเฉพาะชมรมที่ได้มากกว่าค่าเฉลี่ย (ไม่รวมชมรมที่เท่ากับค่าเฉลี่ย)",
        steps=[
            f"จำนวนสมาชิกรวมทั้งหมด = {' + '.join(str(v) for v in vals)} = {total} คน",
            f"ค่าเฉลี่ยต่อชมรม = {total} ÷ 5 = {mean_val} คน",
            f"ชมรมที่มีสมาชิกมากกว่า {mean_val} คน ได้แก่ {', '.join(above)} รวม {len(above)} ชมรม",
        ],
    )
    q2 = mcq(
        stem=f"จากแผนภูมิแท่ง สมาชิกของ **{labels[i_max]}** คิดเป็นร้อยละเท่าใดของจำนวนสมาชิกชมรมทั้งหมด",
        figure=fig,
        correct=f"ร้อยละ {pct_max}",
        wrongs=[
            W(f"ร้อยละ {vals[i_max]}", "นำจำนวนคนมาตอบเป็นร้อยละโดยตรงโดยไม่ได้เทียบกับจำนวนทั้งหมด " + str(total) + " คน", "concept"),
            W(f"ร้อยละ {dec(vals[i_max] * 100 / (total - vals[i_max]), 1)}", "นำไปเทียบกับจำนวนสมาชิกที่เหลือแทนที่จะเทียบกับทั้งหมด", "formula"),
            W(f"ร้อยละ {dec((vals[i_max] - vals[i_min]) * 100 / total, 1)}", "นำผลต่างไปคิดร้อยละแทนที่จะใช้จำนวนสมาชิกของชมรมนั้น", "misread"),
        ],
        hint="ร้อยละของชมรม = (จำนวนสมาชิกของชมรม ÷ จำนวนสมาชิกทั้งหมด) × 100",
        steps=[
            f"{labels[i_max]}มีสมาชิก {vals[i_max]} คน จากทั้งหมด {total} คน",
            f"คิดเป็นร้อยละ = ({vals[i_max]} ÷ {total}) × 100 = ร้อยละ {pct_max}",
        ],
    )
    return [q1, q2]


# ===========================================================================
# Skill 4: m.data.pie — การอ่านและคำนวณแผนภูมิรูปวงกลม
# ===========================================================================
skill(
    "m.data.pie",
    "m.data",
    "การอ่านและคำนวณแผนภูมิรูปวงกลม",
    lesson={
        "concept": (
            "แผนภูมิรูปวงกลมแสดงสัดส่วนของข้อมูลเทียบกับทั้งหมด โดยผลรวมของร้อยละทั้งหมดเท่ากับ 100% "
            "และผลรวมของมุมที่จุดศูนย์กลางทั้งหมดเท่ากับ 360° "
            "(ความสัมพันธ์: ร้อยละ ÷ 100 = มุมที่จุดศูนย์กลาง ÷ 360 = จำนวนย่อย ÷ จำนวนทั้งหมด)"
        ),
        "steps": [
            "ถ้าร้อยละของส่วนใดหายไป ให้หาจาก 100% − ผลรวมของส่วนที่ทราบค่า",
            "แปลงร้อยละเป็นปริมาณจริง: (ร้อยละ ÷ 100) × จำนวนทั้งหมด",
            "แปลงร้อยละเป็นมุมที่จุดศูนย์กลาง: (ร้อยละ ÷ 100) × 360° (เช่น 25% = 90°, 10% = 36°, 5% = 18°)",
        ],
        "example": {
            "q": "นักเรียน 400 คน ชอบฟุตบอล 35% ชอบบาสเกตบอล 25% ที่เหลือชอบว่ายน้ำ มีคนชอบว่ายน้ำกี่คน และคิดเป็นมุมที่จุดศูนย์กลางกี่องศา",
            "steps": [
                "ชอบว่ายน้ำ = 100% − (35% + 25%) = 40%",
                "จำนวนคนชอบว่ายน้ำ = (40 ÷ 100) × 400 = 160 คน",
                "มุมที่จุดศูนย์กลาง = (40 ÷ 100) × 360° = 144°",
            ],
            "a": "160 คน, มุม 144°",
        },
        "mistakes": [
            "คิดมุมที่จุดศูนย์กลางเป็น 100° หรือ 180° แทนที่จะเป็น 360°",
            "เมื่อโจทย์ให้จำนวนของส่วนย่อยส่วนหนึ่งมา เผลอนำไปคูณร้อยละเลยแทนที่จะหาจำนวนทั้งหมดก่อน",
        ],
        "tips": [
            "จำเทียบเร็ว: 10% = 36°, 5% = 18°, 15% = 54°, 20% = 72°, 25% = 90°, 30% = 108°",
        ],
    },
    weight=1.6,
)


@template("m.data.pie", "easy")
def _pie_chart_percent_to_value():
    total = random.choice([200, 300, 400, 500, 600, 800, 1200])
    p1 = random.choice([20, 25, 30, 35])
    p2 = random.choice([15, 20, 25, 30])
    p3 = random.choice([10, 15, 20])
    p4 = 100 - (p1 + p2 + p3)
    if p4 <= 5:
        return None
    percents = [p1, p2, p3, p4]
    labels = ["อาหาร", "ค่าเดินทาง", "ออมเงิน", "อื่น ๆ"]
    fig = svg.pie_chart(labels, percents, title="สัดส่วนค่าใช้จ่ายและเงินออมรายเดือน")
    idx = random.randint(0, 3)
    ans = total * percents[idx] // 100
    return mcq(
        stem=f"จากแผนภูมิรูปวงกลม ถ้ามีรายรับทั้งหมด {num(total)} บาท จะแบ่งเป็นส่วนของ **{labels[idx]}** กี่บาท",
        figure=fig,
        correct=f"{num(ans)} บาท",
        wrongs=[
            W(f"{num(percents[idx])} บาท", "ตอบค่าร้อยละเป็นจำนวนเงินโดยตรง ลืมคูณกับรายรับทั้งหมด", "partial"),
            W(f"{num(total * (100 - percents[idx]) // 100)} บาท", "คำนวณส่วนที่เหลือแทนส่วนที่โจทย์ถาม", "misread"),
            W(f"{num(total * percents[(idx + 1) % 4] // 100)} บาท", f"อ่านสีในแผนภูมิสลับกับหมวด{labels[(idx + 1) % 4]}", "detail"),
        ],
        hint=f"นำร้อยละของหมวด{labels[idx]} คูณด้วยรายรับทั้งหมด แล้วหารด้วย 100",
        steps=[
            f"สัดส่วนของ{labels[idx]} คิดเป็น {percents[idx]}% ของรายรับทั้งหมด",
            f"คิดเป็นเงิน = ({percents[idx]} ÷ 100) × {num(total)} = {num(ans)} บาท",
        ],
    )


@template("m.data.pie", "medium")
def _pie_chart_given_one_slice_find_another():
    # Given the actual count of slice A, find the count or difference of slice B!
    percents = random.choice([
        [35, 25, 25, 15],
        [40, 30, 20, 10],
        [30, 25, 25, 20],
        [45, 25, 20, 10],
        [35, 30, 20, 15],
    ])
    random.shuffle(percents)
    labels = ["ฟุตบอล", "บาสเกตบอล", "แบดมินตัน", "ว่ายน้ำ"]
    unit_per_pct = random.randint(3, 12)  # total is 100 * unit_per_pct
    total = 100 * unit_per_pct
    i_given, i_ask = pick(range(4), 2)
    given_val = percents[i_given] * unit_per_pct
    ask_val = percents[i_ask] * unit_per_pct
    fig = svg.pie_chart(
        [f"{l} ({p}%)" if k != i_ask else f"{l} (ยังไม่ระบุ %)" for k, (l, p) in enumerate(zip(labels, percents))],
        percents,
        title="กีฬาที่นักเรียนชั้น ป.6 ชอบเล่น",
        show_percent=False,
    )
    other_sum = 100 - percents[i_ask]
    return mcq(
        stem=f"จากแผนภูมิรูปวงกลม ถ้านักเรียนที่ชอบเล่น **{labels[i_given]}** มีจำนวน {given_val} คน แล้วนักเรียนที่ชอบเล่น **{labels[i_ask]}** มีกี่คน",
        figure=fig,
        correct=f"{ask_val} คน",
        wrongs=[
            W(f"{percents[i_ask]} คน", "หาค่าร้อยละของกีฬาที่ถามได้แล้วตอบเลย ลืมแปลงเป็นจำนวนคน", "partial"),
            W(f"{total} คน", "ตอบจำนวนนักเรียนทั้งหมดแทนที่จะตอบเฉพาะคนที่ชอบ " + labels[i_ask], "partial"),
            W(f"{abs(ask_val - given_val) or unit_per_pct * 5} คน", "ตอบผลต่างของจำนวนคนแทนจำนวนคนของกีฬาที่ถาม", "misread"),
        ],
        hint="หาร้อยละที่หายไปจาก 100% ก่อน แล้วเทียบว่า 1% คิดเป็นกี่คนจากข้อมูลที่โจทย์กำหนดให้",
        steps=[
            f"ร้อยละของคนที่ชอบ{labels[i_ask]} = 100% − {other_sum}% = {percents[i_ask]}%",
            f"เนื่องจาก {labels[i_given]} ({percents[i_given]}%) คิดเป็น {given_val} คน ดังนั้น 1% = {given_val} ÷ {percents[i_given]} = {unit_per_pct} คน",
            f"ดังนั้นคนที่ชอบ{labels[i_ask]} ({percents[i_ask]}%) มีจำนวน = {percents[i_ask]} × {unit_per_pct} = {ask_val} คน",
        ],
    )


@template("m.data.pie", "hard")
def _pie_chart_central_angle():
    p_list = random.choice([
        [30, 25, 25, 20],
        [35, 25, 25, 15],
        [40, 25, 20, 15],
        [45, 25, 20, 10],
    ])
    random.shuffle(p_list)
    labels = ["นิยาย", "การ์ตูน", "วิทยาศาสตร์", "ประวัติศาสตร์"]
    fig = svg.pie_chart(labels, p_list, title="สัดส่วนหนังสือในห้องสมุด")
    idx = random.randint(0, 3)
    pct = p_list[idx]
    deg = dec(pct * 360 / 100, 1)
    return mcq(
        stem=f"จากแผนภูมิรูปวงกลม ส่วนของหนังสือ **{labels[idx]}** ({pct}%) มีขนาดของมุมที่จุดศูนย์กลางของวงกลมกางกี่องศา",
        figure=fig,
        correct=f"{deg}°",
        wrongs=[
            W(f"{dec(pct * 180 / 100, 1)}°", "คูณด้วย 180° แทนที่จะคูณด้วยมุมรอบจุดศูนย์กลาง 360°", "formula"),
            W(f"{pct}°", "นำค่าร้อยละมาตอบเป็นองศาโดยตรง", "concept"),
            W(f"{dec((100 - pct) * 360 / 100, 1)}°", "คำนวณมุมของส่วนที่เหลือทั้งหมดแทนส่วนที่โจทย์ถาม", "misread"),
        ],
        hint="มุมรอบจุดศูนย์กลางของวงกลมคือ 360° ดังนั้น มุมที่จุดศูนย์กลาง = (ร้อยละ ÷ 100) × 360°",
        steps=[
            f"หนังสือ{labels[idx]}คิดเป็น {pct}% ของทั้งหมด",
            f"มุมที่จุดศูนย์กลาง = ({pct} ÷ 100) × 360° = {deg}°",
        ],
    )


# ===========================================================================
# Skill 5: m.data.line — การอ่านและวิเคราะห์กราฟเส้น
# ===========================================================================
skill(
    "m.data.line",
    "m.data",
    "การอ่านและวิเคราะห์กราฟเส้น",
    lesson={
        "concept": (
            "กราฟเส้นเหมาะสำหรับแสดงการเปลี่ยนแปลงของข้อมูลตามเวลา "
            "ความชันของเส้นกราฟบอกอัตราการเปลี่ยนแปลง: เส้นชันมากแปลว่าเปลี่ยนมาก เส้นแนวนอนแปลว่าคงที่"
        ),
        "steps": [
            "อ่านค่าของแต่ละจุดบนกราฟเทียบกับแกนตั้ง",
            "หากถามช่วงที่เพิ่มขึ้นหรือลดลงมากที่สุด ให้ดูความต่างของจุดสองจุดที่อยู่ติดกัน (ความชันของส่วนของเส้นตรง)",
        ],
        "example": {
            "q": "จำนวนผู้เข้าชมพิพิธภัณฑ์วันจันทร์–พฤหัสฯ เป็น 120, 150, 210, 190 คน ช่วงวันใดมีผู้เข้าชมเพิ่มขึ้นมากที่สุด",
            "steps": [
                "จันทร์→อังคาร เพิ่ม 150 − 120 = 30 คน",
                "อังคาร→พุธ เพิ่ม 210 − 150 = 60 คน (มากที่สุด)",
            ],
            "a": "วันอังคารไปวันพุธ (เพิ่มขึ้น 60 คน)",
        },
        "mistakes": [
            "สับสนระหว่าง 'จุดที่มีค่าสูงสุด' กับ 'ช่วงที่มีการเพิ่มขึ้นมากที่สุด'",
        ],
        "tips": [
            "ช่วงที่เส้นกราฟพุ่งขึ้นชันที่สุด คือช่วงที่มีค่าเพิ่มขึ้นมากที่สุด",
        ],
    },
    weight=1.2,
)


@template("m.data.line", "easy")
def _line_chart_biggest_change():
    days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสฯ", "ศุกร์"]
    base = random.randint(2, 5) * 10
    # Create unique positive jumps and one drop
    deltas = random.sample([10, 20, 30, 40], 3) + [-20]
    random.shuffle(deltas)
    vals = [base]
    for d in deltas:
        vals.append(max(10, vals[-1] + d))
    # Ensure a unique maximum increase between consecutive days
    inc = [vals[i + 1] - vals[i] for i in range(4)]
    max_inc = max(inc)
    if inc.count(max_inc) > 1 or max_inc <= 0:
        return None
    best_i = inc.index(max_inc)
    fig = svg.line_chart(days, vals, title="ยอดขายน้ำผลไม้ปั่นรายวัน (แก้ว)", unit="แก้ว", step=20)
    ans = f"{days[best_i]} ไป {days[best_i + 1]}"
    others = [f"{days[i]} ไป {days[i + 1]}" for i in range(4) if i != best_i]
    return mcq(
        stem="จากกราฟเส้น ยอดขายน้ำผลไม้ปั่น **เพิ่มขึ้นมากที่สุด** ในช่วงวันใด",
        figure=fig,
        correct=ans,
        wrongs=[
            W(others[0], "ช่วงนี้มียอดขายเปลี่ยนแปลงน้อยกว่าช่วงที่กราฟชันที่สุด", "detail"),
            W(others[1], "ดูเฉพาะความสูงของจุดยอดกราฟ แทนที่จะดูผลต่างที่เพิ่มขึ้นระหว่างสองวันติดกัน", "trap"),
            W(others[2], "อ่านผลต่างระหว่างวันผิดพลาด", "detail"),
        ],
        hint="หาผลต่างของยอดขายระหว่างสองวันที่อยู่ติดกัน หรือดูช่วงที่เส้นกราฟพุ่งขึ้นชันที่สุด",
        steps=[
            f"อ่านค่ายอดขายแต่ละวัน: {', '.join(f'{d} = {v}' for d, v in zip(days, vals))} แก้ว",
            f"ช่วง {ans} เพิ่มขึ้น {vals[best_i + 1]} − {vals[best_i]} = {max_inc} แก้ว ซึ่งเพิ่มขึ้นมากที่สุด",
        ],
    )


@template("m.data.line", "medium")
def _line_chart_mean_and_diff():
    months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย."]
    vals = [random.randint(2, 9) * 10 for _ in range(6)]
    # Adjust last value so sum is divisible by 6
    rem = sum(vals[:-1]) % 60
    vals[-1] = 60 - rem if 60 - rem >= 20 else 120 - rem
    mean_v = sum(vals) // 6
    fig = svg.line_chart(months, vals, title="ปริมาณการใช้ไฟฟ้าของบ้านหลังหนึ่ง (หน่วย)", unit="หน่วย", step=20)
    return mcq(
        stem="จากกราฟเส้น ปริมาณการใช้ไฟฟ้าเฉลี่ยต่อเดือนในช่วง 6 เดือนนี้เป็นกี่หน่วย",
        figure=fig,
        correct=f"{mean_v} หน่วย",
        wrongs=[
            W(f"{sum(vals)} หน่วย", "ตอบผลรวมของทั้ง 6 เดือน ลืมหารด้วย 6", "partial"),
            W(f"{(max(vals) + min(vals)) // 2} หน่วย", "นำค่าสูงสุดบวกค่าต่ำสุดแล้วหารด้วย 2 แทนที่จะรวมทุกเดือน", "formula"),
            W(f"{mean_v + 10} หน่วย", "อ่านค่าจากกราฟหรือบวกเลขคลาดเคลื่อน", "calc"),
        ],
        hint="อ่านค่าทั้ง 6 เดือนจากจุดบนกราฟ นำมาบวกกันทั้งหมดแล้วหารด้วย 6",
        steps=[
            f"ค่าของแต่ละเดือนคือ {', '.join(str(v) for v in vals)} หน่วย",
            f"ผลรวมทั้ง 6 เดือน = {sum(vals)} หน่วย",
            f"ค่าเฉลี่ยต่อเดือน = {sum(vals)} ÷ 6 = {mean_v} หน่วย",
        ],
    )


# ===========================================================================
# Skill 6: m.data.picto_table — แผนภูมิรูปภาพและตารางข้อมูล
# ===========================================================================
skill(
    "m.data.picto_table",
    "m.data",
    "แผนภูมิรูปภาพและตารางข้อมูล",
    lesson={
        "concept": (
            "แผนภูมิรูปภาพใช้สัญลักษณ์ 1 รูปแทนจำนวนที่กำหนดไว้ในข้อตกลง (เช่น 1 รูป แทน 20 ชิ้น ครึ่งรูปจึงแทน 10 ชิ้น) "
            "ส่วนตารางทางเดียวและตารางสองทางต้องตรวจสอบผลรวมตามแนวแถวและแนวคอลัมน์ให้สอดคล้องกัน"
        ),
        "steps": [
            "อ่านข้อตกลงด้านล่างแผนภูมิรูปภาพก่อนเสมอว่า 1 รูปแทนเท่าไร",
            "สำหรับตารางสองทาง ให้หาช่องที่หายไปจากการลบออกจากผลรวมของแถวหรือคอลัมน์",
        ],
        "example": {
            "q": "ถ้า ● 1 รูป แทนเค้ก 12 ชิ้น แถววันเสาร์มีรูปเต็ม 3 รูป กับครึ่งรูป 1 รูป ขายเค้กได้กี่ชิ้น",
            "steps": [
                "3.5 รูป × 12 ชิ้น = 42 ชิ้น",
            ],
            "a": "42 ชิ้น",
        },
        "mistakes": [
            "นับจำนวนรูปภาพมาตอบเลยโดยลืมคูณค่าที่ 1 รูปแทนตามข้อตกลง",
            "ลืมคิดรูปครึ่งดวงเป็นครึ่งหนึ่งของค่าที่กำหนด",
        ],
        "tips": [
            "ถ้าถามผลต่างระหว่างสองแถวในแผนภูมิรูปภาพ ให้นำ 'ผลต่างของจำนวนรูป' มาคูณค่าของ 1 รูปได้เลย จะเร็วกว่าคูณแยกทีละแถว!",
        ],
    },
    weight=1.2,
)


@template("m.data.picto_table", "easy")
def _pictogram_half_symbol():
    per_val = random.choice([8, 10, 12, 16, 20, 24, 30])
    labels = ["ชั้น ป.4", "ชั้น ป.5", "ชั้น ป.6"]
    counts = [
        random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        random.choice([2, 2.5, 3, 3.5, 4, 4.5, 5]),
        random.choice([2.5, 3.5, 4.5, 5.5]),
    ]
    total_syms = sum(counts)
    total_val = int(round(total_syms * per_val))
    fig = svg.pictogram(labels, counts, symbol="★", per=f"กำหนดให้ ★ 1 รูป แทนนักเรียน {per_val} คน")
    return mcq(
        stem="จากแผนภูมิรูปภาพ นักเรียนทั้ง 3 ชั้นมีจำนวนรวมกันทั้งหมดกี่คน",
        figure=fig,
        correct=f"{num(total_val)} คน",
        wrongs=[
            W(f"{dec(total_syms, 1)} คน", "นับเฉพาะจำนวนรูปดาวทั้งหมด ลืมคูณจำนวนคนที่ดาว 1 รูปแทน", "partial"),
            W(f"{num(int(sum(int(c) for c in counts) * per_val))} คน", "นับเฉพาะรูปดาวเต็มดวง ลืมรวมรูปดาวครึ่งดวง", "detail"),
            W(f"{num(int(sum(math.ceil(c) for c in counts) * per_val))} คน", "คิดรูปดาวครึ่งดวงเป็นเต็มดวง", "detail"),
        ],
        hint=f"รวมจำนวนรูปดาวทั้งหมด (ครึ่งรูป = 0.5) แล้วคูณด้วย {per_val}",
        steps=[
            f"จำนวนรูปดาวรวม = {' + '.join(dec(c, 1) for c in counts)} = {dec(total_syms, 1)} รูป",
            f"เนื่องจากดาว 1 รูป แทน {per_val} คน จึงมีนักเรียนทั้งหมด = {dec(total_syms, 1)} × {per_val} = {num(total_val)} คน",
        ],
    )


@template("m.data.picto_table", "medium")
def _two_way_table_missing():
    g1_m = random.randint(12, 25)
    g1_f = random.randint(14, 26)
    g2_m = random.randint(13, 25)
    g2_f = random.randint(15, 27)
    tot_m = g1_m + g2_m
    tot_f = g1_f + g2_f
    tot_1 = g1_m + g1_f
    tot_2 = g2_m + g2_f
    grand = tot_1 + tot_2
    tbl = {
        "caption": "ตารางแสดงจำนวนนักเรียนที่เลือกเรียนวิชาเลือก",
        "head": ["วิชาเลือก", "ชาย (คน)", "หญิง (คน)", "รวม (คน)"],
        "rows": [
            ["คอมพิวเตอร์", str(g1_m), "A", str(tot_1)],
            ["ภาษาจีน", "B", str(g2_f), "C"],
            ["รวม", str(tot_m), str(tot_f), str(grand)],
        ],
    }
    ans = g1_f + g2_m
    return mcq(
        stem="จากตารางที่กำหนดให้ ค่าของ **A + B** เท่ากับข้อใด",
        table=tbl,
        correct=f"{ans} คน",
        wrongs=[
            W(f"{g1_f + tot_2} คน", "หาค่า C แทนที่จะเป็นค่า B แล้วนำมาบวกกับ A", "misread"),
            W(f"{g1_f} คน", "ตอบเฉพาะค่า A ลืมบวกค่า B", "partial"),
            W(f"{tot_1 - g1_m + tot_m} คน", "ใช้ผลรวมชายทั้งหมดเป็นค่า B โดยไม่ได้ลบวิชาคอมพิวเตอร์ออก", "partial"),
        ],
        hint="หา A จากแถวคอมพิวเตอร์ (รวม − ชาย) และหา B จากคอลัมน์ชาย (รวมชาย − ชายคอมพิวเตอร์)",
        steps=[
            f"จากแถวคอมพิวเตอร์: A = {tot_1} − {g1_m} = {g1_f} คน",
            f"จากคอลัมน์นักเรียนชาย: B = {tot_m} − {g1_m} = {g2_m} คน",
            f"ดังนั้น A + B = {g1_f} + {g2_m} = {ans} คน",
        ],
    )


@template("m.data.picto_table", "hard")
def _frequency_table_weighted_mean():
    # Frequency table of scores or children per family -> find weighted mean!
    scores = [1, 2, 3, 4, 5]
    # Pick frequencies summing to 10 or 20 with clean weighted sum
    f1, f2, f3, f4 = random.randint(1, 5), random.randint(2, 6), random.randint(2, 6), random.randint(1, 5)
    target_total_f = 20
    f5 = target_total_f - (f1 + f2 + f3 + f4)
    if f5 < 1:
        return None
    freqs = [f1, f2, f3, f4, f5]
    weighted_sum = sum(s * f for s, f in zip(scores, freqs))
    mean_val = weighted_sum / target_total_f
    mean_str = dec(mean_val, 2)
    tbl = {
        "caption": "ตารางความถี่แสดงจำนวนหนังสือที่นักเรียนอ่านใน 1 เดือน",
        "head": ["จำนวนหนังสือ (เล่ม)", "จำนวนนักเรียน (คน)"],
        "rows": [[str(s), str(f)] for s, f in zip(scores, freqs)],
    }
    return mcq(
        stem=f"จากตารางความถี่ของนักเรียน {target_total_f} คน นักเรียนกลุ่มนี้อ่านหนังสือเฉลี่ยคนละกี่เล่มต่อเดือน",
        table=tbl,
        correct=f"{mean_str} เล่ม",
        wrongs=[
            W("3 เล่ม" if mean_str != "3" else "2.5 เล่ม",
              "นำจำนวนหนังสือ (1 ถึง 5) มาเฉลี่ยกันโดยไม่คูณจำนวนคนในแต่ละกลุ่ม", "trap"),
            W(f"{dec(weighted_sum / 5, 1)} เล่ม",
              f"หาผลรวมจำนวนหนังสือทั้งหมดถูก ({weighted_sum} เล่ม) แต่หารด้วย 5 แถว แทนที่จะหารด้วยจำนวนนักเรียน {target_total_f} คน",
              "trap"),
            W(f"{dec(target_total_f / 5, 1)} เล่ม", "นำจำนวนนักเรียนไปหารด้วย 5 แถว", "concept"),
        ],
        hint="ต้องหาจำนวนหนังสือรวมทั้งหมดโดยนำ (จำนวนเล่ม × จำนวนคน) ของทุกแถวมาบวกกัน แล้วหารด้วยจำนวนนักเรียนทั้งหมด",
        steps=[
            "หาผลรวมของหนังสือทั้งหมด = " + " + ".join(f"({s}×{f})" for s, f in zip(scores, freqs)) + f" = {weighted_sum} เล่ม",
            f"จำนวนนักเรียนทั้งหมด = {' + '.join(str(f) for f in freqs)} = {target_total_f} คน",
            f"ค่าเฉลี่ย = {weighted_sum} ÷ {target_total_f} = {mean_str} เล่ม",
        ],
    )


# ===========================================================================
# Skill 7: m.data.prob_basic — ความน่าจะเป็นเบื้องต้น (ลูกเต๋า ลูกบอล เหรียญ)
# ===========================================================================
skill(
    "m.data.prob_basic",
    "m.data",
    "ความน่าจะเป็นเบื้องต้น",
    lesson={
        "concept": (
            "ความน่าจะเป็นของเหตุการณ์ = (จำนวนผลลัพธ์ของเหตุการณ์ที่สนใจ) ÷ (จำนวนผลลัพธ์ทั้งหมดที่อาจจะเกิดขึ้นได้) "
            "โดยค่าความน่าจะเป็นจะอยู่ระหว่าง 0 ถึง 1 เสมอ และมักตอบในรูปเศษส่วนอย่างต่ำ"
        ),
        "steps": [
            "ขั้นที่ 1: นับจำนวนผลลัพธ์ทั้งหมดที่เป็นไปได้ (n(S))",
            "ขั้นที่ 2: นับจำนวนผลลัพธ์ที่ตรงตามเงื่อนไขที่โจทย์ถาม (n(E))",
            "ขั้นที่ 3: เขียนเป็นเศษส่วน n(E)/n(S) แล้วทอนเป็นเศษส่วนอย่างต่ำ",
        ],
        "example": {
            "q": "ทอดลูกเต๋าเที่ยงตรง 1 ลูก 1 ครั้ง ความน่าจะเป็นที่จะได้แต้มเป็นจำนวนเฉพาะเป็นเท่าใด",
            "steps": [
                "แต้มทั้งหมดที่เป็นไปได้คือ 1, 2, 3, 4, 5, 6 (6 แบบ)",
                "แต้มที่เป็นจำนวนเฉพาะคือ 2, 3, 5 (3 แบบ — ระวัง 1 ไม่ใช่จำนวนเฉพาะ)",
                "ความน่าจะเป็น = [[3/6]] = [[1/2]]",
            ],
            "a": "[[1/2]]",
        },
        "mistakes": [
            "นับ 1 เป็นจำนวนเฉพาะเมื่อโจทย์ถามความน่าจะเป็นของการได้จำนวนเฉพาะ",
            "นำจำนวนที่สนใจไปเทียบกับจำนวนที่เหลือ แทนที่จะเทียบกับจำนวนทั้งหมด",
        ],
        "tips": [
            "ถ้าโจทย์ถามความน่าจะเป็นของคำว่า 'ไม่...' ให้คิดจาก 1 − ความน่าจะเป็นที่เกิดเหตุการณ์นั้น",
        ],
    },
    weight=1.5,
)


@template("m.data.prob_basic", "easy")
def _prob_balls_in_bag():
    r = random.randint(2, 7)
    b = random.randint(2, 7)
    y = random.randint(2, 7)
    total = r + b + y
    mode = random.choice(["red", "not_yellow", "red_or_blue"])
    if mode == "red":
        fav = r
        cond_txt = "ได้ลูกบอล **สีแดง**"
        step_fav = f"มีลูกบอลสีแดง {r} ลูก"
        trap_comp = total - r
    elif mode == "not_yellow":
        fav = r + b
        cond_txt = "ได้ลูกบอลที่ **ไม่ใช่สีเหลือง**"
        step_fav = f"ลูกบอลที่ไม่ใช่สีเหลือง (สีแดงหรือสีน้ำเงิน) มี {r} + {b} = {fav} ลูก"
        trap_comp = y
    else:
        fav = r + y
        cond_txt = "ได้ลูกบอล **สีแดงหรือสีเหลือง**"
        step_fav = f"ลูกบอลสีแดงหรือสีเหลืองมี {r} + {y} = {fav} ลูก"
        trap_comp = b

    ans_fr = Fraction(fav, total)
    if ans_fr.denominator == 1:
        return None
    wrong1 = Fraction(trap_comp, total)
    wrong2 = Fraction(fav, total - fav) if total - fav > 0 and fav < total - fav else Fraction(1, total)
    wrong3 = Fraction(min(total - 1, fav + 1), total)
    return mcq(
        stem=f"ในกล่องทึบใบหนึ่งมีลูกบอลขนาดเท่ากัน เป็นสีแดง {r} ลูก สีน้ำเงิน {b} ลูก และสีเหลือง {y} ลูก สุ่มหยิบลูกบอลขึ้นมา 1 ลูก ความน่าจะเป็นที่จะ{cond_txt}เท่ากับข้อใด",
        correct=frac(ans_fr),
        wrongs=[
            W(frac(wrong1), "คิดความน่าจะเป็นของเหตุการณ์ตรงกันข้ามกับที่โจทย์ถาม", "misread"),
            W(frac(wrong2), "ใช้ตัวส่วนเป็นจำนวนลูกบอลที่เหลือ แทนที่จะเป็นจำนวนลูกบอลทั้งหมดในกล่อง", "formula"),
            W(frac(wrong3), "นับจำนวนลูกบอลหรือทอนเศษส่วนอย่างต่ำผิดพลาด", "calc"),
        ],
        hint="ความน่าจะเป็น = จำนวนลูกบอลที่ตรงเงื่อนไข ÷ จำนวนลูกบอลทั้งหมดในกล่อง (ทอนเป็นเศษส่วนอย่างต่ำ)",
        steps=[
            f"จำนวนลูกบอลทั้งหมดในกล่อง = {r} + {b} + {y} = {total} ลูก",
            step_fav,
            f"ความน่าจะเป็น = [[{fav}/{total}]]" + (f" = {frac(ans_fr)}" if ans_fr.denominator != total else ""),
        ],
    )


@template("m.data.prob_basic", "medium")
def _prob_number_cards():
    n = random.choice([10, 12, 15, 18, 20, 24, 25, 30])
    cond_type = random.choice(["prime", "div3", "multiple_or", "perfect_sq"])
    primes = [x for x in range(2, n + 1) if all(x % d != 0 for d in range(2, int(x ** 0.5) + 1))]
    if cond_type == "prime":
        fav_list = primes
        cond_desc = "เป็น **จำนวนเฉพาะ**"
        trap_count = len(primes) + 1  # counting 1 as prime!
        trap_reason = "เผลอนับ 1 เป็นจำนวนเฉพาะด้วย (1 ไม่ใช่จำนวนเฉพาะ)"
    elif cond_type == "div3":
        k = random.choice([3, 4, 6])
        fav_list = [x for x in range(1, n + 1) if x % k == 0]
        cond_desc = f"เป็นจำนวนที่ **หารด้วย {k} ลงตัว**"
        trap_count = len(fav_list) + 1
        trap_reason = f"นับจำนวนที่หารด้วย {k} ลงตัวเกินมา 1 จำนวน"
    elif cond_type == "multiple_or":
        fav_list = [x for x in range(1, n + 1) if x % 3 == 0 or x % 5 == 0]
        cond_desc = "เป็นจำนวนที่ **หารด้วย 3 หรือ 5 ลงตัว**"
        trap_count = (n // 3) + (n // 5)  # forgetting to subtract multiples of 15!
        if trap_count == len(fav_list):
            trap_count += 1
        trap_reason = "บวกจำนวนที่หารด้วย 3 ลงตัว กับหารด้วย 5 ลงตัวเข้าด้วยกันโดยลืมหักตัวที่หารด้วย 15 ลงตัวที่ซ้ำกัน"
    else:
        fav_list = [x for x in range(1, n + 1) if int(x ** 0.5) ** 2 == x]
        cond_desc = "เป็น **จำนวนกำลังสองสมบูรณ์** (เช่น 1, 4, 9, ...)"
        trap_count = len(fav_list) - 1
        trap_reason = "ลืมนับ 1 ซึ่งเป็นกำลังสองสมบูรณ์ (1² = 1)"

    fav = len(fav_list)
    ans = Fraction(fav, n)
    w_trap = Fraction(trap_count, n)
    w_comp = Fraction(n - fav, n)
    w_off = Fraction(max(1, fav - 1 if trap_count > fav else fav + 1), n)
    return mcq(
        stem=f"มีบัตรตัวเลขตั้งแต่ 1 ถึง {n} บัตรละ 1 หมายเลข สุ่มหยิบบัตรขึ้นมา 1 ใบ ความน่าจะเป็นที่จะได้บัตรหมายเลขที่{cond_desc}เท่ากับข้อใด",
        correct=frac(ans),
        wrongs=[
            W(frac(w_trap), trap_reason, "trap"),
            W(frac(w_comp), "ตอบความน่าจะเป็นของจำนวนที่ไม่ตรงเงื่อนไข", "misread"),
            W(frac(w_off), "นับจำนวนที่เข้าเงื่อนไขตกหล่นหรือทอนเศษส่วนผิด", "calc"),
        ],
        hint=f"เขียนรายการจำนวนตั้งแต่ 1 ถึง {n} ที่{cond_desc}ออกมาให้ครบ แล้วหารด้วย {n}",
        steps=[
            f"จำนวนบัตรทั้งหมดมี {n} ใบ",
            f"หมายเลขที่เข้าเงื่อนไข ได้แก่ {', '.join(str(x) for x in fav_list)} รวม {fav} ใบ",
            f"ความน่าจะเป็น = [[{fav}/{n}]]" + (f" = {frac(ans)}" if ans.denominator != n else ""),
        ],
    )


@template("m.data.prob_basic", "hard")
def _prob_two_dice():
    person = name_th()
    mode = random.choice(["sum_eq", "sum_ge", "diff_eq", "prod_eq"])
    if mode == "sum_eq":
        s = random.choice([4, 5, 6, 7, 8, 9, 10, 11])
        pairs = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s]
        desc = f"ผลรวมของแต้มทั้งสองลูกเท่ากับ **{s}**"
        trap_fr = Fraction(max(1, (len(pairs) + 1) // 2), 36)
        trap_why = "นับคู่สลับลำดับ เช่น (a, b) กับ (b, a) เป็นวิธีเดียวกัน"
    elif mode == "sum_ge":
        s = random.choice([9, 10, 11])
        pairs = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b >= s]
        desc = f"ผลรวมของแต้ม **ตั้งแต่ {s} ขึ้นไป**"
        strict = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b > s]
        trap_fr = Fraction(len(strict), 36)
        trap_why = f"นับเฉพาะผลรวมที่มากกว่า {s} ลืมรวมกรณีที่ผลรวมเท่ากับ {s} พอดี"
    elif mode == "diff_eq":
        d = random.choice([1, 2, 3, 4])
        pairs = [(a, b) for a in range(1, 7) for b in range(1, 7) if abs(a - b) == d]
        desc = f"ผลต่างของแต้มทั้งสองลูกเท่ากับ **{d}**"
        trap_fr = Fraction(len(pairs) // 2, 36)
        trap_why = "นับเฉพาะกรณีที่ลูกแรกมากกว่าลูกที่สอง ลืมคูณ 2 สำหรับกรณีสลับลูกเต๋า"
    else:
        p = random.choice([4, 6, 8, 10, 12, 15, 18, 20, 24])
        pairs = [(a, b) for a in range(1, 7) for b in range(1, 7) if a * b == p]
        desc = f"ผลคูณของแต้มทั้งสองลูกเท่ากับ **{p}**"
        trap_fr = Fraction(max(1, len(pairs) // 2), 12)
        trap_why = "คิดจำนวนผลลัพธ์ทั้งหมดเป็น 12 แทนที่จะเป็น 6 × 6 = 36"

    fav = len(pairs)
    ans = Fraction(fav, 36)
    return mcq(
        stem=f"{person}ทอดลูกเต๋าเที่ยงตรง 2 ลูกพร้อมกัน 1 ครั้ง ความน่าจะเป็นที่จะได้{desc}เท่ากับเท่าใด",
        correct=frac(ans),
        wrongs=[
            W(frac(trap_fr), trap_why, "trap"),
            W(frac(Fraction(fav + 1, 36)), "นับจำนวนคู่อันดับเกินมา 1 กรณี", "calc"),
            W(frac(Fraction(36 - fav, 36)), "ตอบความน่าจะเป็นของเหตุการณ์ตรงกันข้าม", "misread"),
            W(frac(Fraction(max(1, fav - 1), 36)), "นับจำนวนคู่อันดับตกหล่นไป 1 กรณี", "calc"),
        ],
        hint="ทอดลูกเต๋า 2 ลูก มีผลลัพธ์ทั้งหมด 6 × 6 = 36 แบบ โดย (a, b) และ (b, a) เมื่อ a ≠ b นับเป็นคนละแบบ",
        steps=[
            "จำนวนผลลัพธ์ทั้งหมดของการทอดลูกเต๋า 2 ลูก = 6 × 6 = 36 แบบ",
            f"ผลลัพธ์ที่ตรงเงื่อนไข มี {fav} แบบ ได้แก่ {', '.join(f'({a},{b})' for a, b in pairs)}",
            f"ดังนั้นความน่าจะเป็น = [[{fav}/36]]" + (f" = {frac(ans)}" if ans.denominator != 36 else ""),
        ],
    )


# ===========================================================================
# Skill 8: m.data.prob_fig — ความน่าจะเป็นเชิงเรขาคณิตและวงล้อเสี่ยงโชค
# ===========================================================================
skill(
    "m.data.prob_fig",
    "m.data",
    "ความน่าจะเป็นจากรูปเรขาคณิตและวงล้อเสี่ยงโชค",
    lesson={
        "concept": (
            "สำหรับการสุ่มหมุนวงล้อหรือสุ่มจุดในพื้นที่ ความน่าจะเป็นคำนวณจากสัดส่วนของจำนวนช่องที่เท่ากัน "
            "ขนาดของมุมที่จุดศูนย์กลาง (เทียบกับ 360°) หรือพื้นที่ส่วนที่สนใจเทียบกับพื้นที่ทั้งหมด"
        ),
        "steps": [
            "ดูว่าวงล้อหรือตารางถูกแบ่งออกเป็นช่องที่มีขนาดเท่ากันทั้งหมดกี่ช่อง",
            "นับจำนวนช่องที่ตรงกับเงื่อนไขที่โจทย์ถาม",
            "นำจำนวนช่องที่สนใจหารด้วยจำนวนช่องทั้งหมด แล้วทอนเป็นเศษส่วนอย่างต่ำ",
        ],
        "example": {
            "q": "วงล้อแบ่งเป็น 8 ช่องเท่ากัน มีเลข 1, 2, 2, 3, 3, 3, 4, 5 หมุนวงล้อ 1 ครั้ง ความน่าจะเป็นที่ได้เลข 3 เป็นเท่าใด",
            "steps": [
                "มีช่องทั้งหมด 8 ช่อง และมีช่องที่เป็นเลข 3 อยู่ 3 ช่อง",
                "ความน่าจะเป็น = [[3/8]]",
            ],
            "a": "[[3/8]]",
        },
        "mistakes": [
            "นับจำนวนชนิดของตัวเลข แทนที่จะนับจำนวนช่องที่มีตัวเลขนั้น",
        ],
        "tips": [
            "ถ้าแต่ละช่องมีขนาดไม่เท่ากัน ต้องเปลี่ยนเป็นหน่วยย่อยที่เท่ากันหรือคิดจากมุมที่จุดศูนย์กลาง ÷ 360°",
        ],
    },
    weight=1.1,
)


@template("m.data.prob_fig", "medium")
def _spinner_probability():
    n_sectors = random.choice([8, 10, 12])
    pool = ["A", "B", "C", "D"]
    if n_sectors == 8:
        counts = random.choice([[3, 2, 2, 1], [4, 2, 1, 1], [3, 3, 1, 1]])
    elif n_sectors == 10:
        counts = random.choice([[4, 3, 2, 1], [5, 2, 2, 1], [3, 3, 3, 1]])
    else:
        counts = random.choice([[5, 3, 3, 1], [4, 4, 3, 1], [5, 4, 2, 1]])
    random.shuffle(counts)
    seq = []
    for sym, cnt in zip(pool, counts):
        seq.extend([sym] * cnt)
    random.shuffle(seq)
    c = (100, 80)
    r = 62
    parts = [svg.circle(c, r)]
    step_deg = 360 / n_sectors
    for i in range(n_sectors):
        a0 = i * step_deg
        rad0 = math.radians(a0)
        parts.append(svg.line(c, (c[0] + r * math.cos(rad0), c[1] - r * math.sin(rad0))))
        mid = math.radians(a0 + step_deg / 2)
        parts.append(svg.label((c[0] + r * 0.65 * math.cos(mid), c[1] - r * 0.65 * math.sin(mid)),
                               seq[i], size=12, bold=True))
    parts.append(svg.dot(c, 3))
    fig = svg.canvas(200, 160, parts)

    i1, i2 = pick(range(4), 2)
    ask_or = random.choice([True, False])
    if ask_or:
        fav = counts[i1] + counts[i2]
        stem = f"จากรูปวงล้อที่แบ่งออกเป็น {n_sectors} ช่องเท่า ๆ กัน ถ้าหมุนวงล้อ 1 ครั้ง ความน่าจะเป็นที่ลูกศรจะชี้ช่องตัวอักษร **{pool[i1]} หรือ {pool[i2]}** เท่ากับเท่าใด"
        step2 = f"ช่องที่เป็น {pool[i1]} มี {counts[i1]} ช่อง และ {pool[i2]} มี {counts[i2]} ช่อง รวมเป็น {fav} ช่อง"
    else:
        fav = n_sectors - counts[i1]
        stem = f"จากรูปวงล้อที่แบ่งออกเป็น {n_sectors} ช่องเท่า ๆ กัน ถ้าหมุนวงล้อ 1 ครั้ง ความน่าจะเป็นที่ลูกศรจะ **ไม่ชี้** ช่องตัวอักษร **{pool[i1]}** เท่ากับเท่าใด"
        step2 = f"ช่องที่เป็น {pool[i1]} มี {counts[i1]} ช่อง ดังนั้นช่องที่ไม่ใช่ {pool[i1]} มี {n_sectors} − {counts[i1]} = {fav} ช่อง"
    ans = Fraction(fav, n_sectors)
    return mcq(
        stem=stem,
        figure=fig,
        correct=frac(ans),
        wrongs=[
            W(frac(Fraction(n_sectors - fav, n_sectors)), "ตอบความน่าจะเป็นของเหตุการณ์ตรงกันข้าม", "misread"),
            W(frac(Fraction(min(n_sectors - 1, fav + 1), n_sectors)), "นับจำนวนช่องบนวงล้อเกินมา 1 ช่อง", "detail"),
            W(frac(Fraction(max(1, fav - 1), n_sectors)), "นับจำนวนช่องบนวงล้อตกหล่นไป 1 ช่อง", "detail"),
            W(frac(Fraction(2 if ask_or else 3, 4)), "นับจำนวนชนิดของตัวอักษรแทนที่จะนับจำนวนช่องบนวงล้อ", "trap"),
        ],
        hint=f"นับจำนวนช่องที่ตรงกับเงื่อนไขจากทั้งหมด {n_sectors} ช่อง แล้วทอนเป็นเศษส่วนอย่างต่ำ",
        steps=[
            f"วงล้อแบ่งออกเป็น {n_sectors} ช่องที่มีขนาดเท่ากัน",
            step2,
            f"ความน่าจะเป็น = [[{fav}/{n_sectors}]]" + (f" = {frac(ans)}" if ans.denominator != n_sectors else ""),
        ],
    )


@template("m.data.prob_fig", "challenge")
def _without_replacement_or_grid_dart():
    digits = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    digits.sort()
    all_nums = [10 * a + b for a in digits for b in digits if a != b]
    evens = [x for x in all_nums if x % 2 == 0]
    gt_50 = [x for x in all_nums if x > 50]
    div_3 = [x for x in all_nums if x % 3 == 0]
    choices_cond = []
    if 0 < len(evens) < 12:
        choices_cond.append(("เป็น **จำนวนคู่**", evens))
    if 0 < len(gt_50) < 12:
        choices_cond.append(("มีค่า **มากกว่า 50**", gt_50))
    if 0 < len(div_3) < 12:
        choices_cond.append(("**หารด้วย 3 ลงตัว**", div_3))
    if not choices_cond:
        return None
    cond_txt, fav_list = pick(choices_cond)
    fav = len(fav_list)
    ans = Fraction(fav, 12)
    d_str = ", ".join(str(d) for d in digits)
    return mcq(
        stem=f"มีบัตรตัวเลข 4 ใบ คือ {d_str} สุ่มหยิบบัตรขึ้นมา 2 ใบเพื่อวางเรียงเป็นจำนวนสองหลัก (ไม่ใช้เลขซ้ำหลักกัน) ความน่าจะเป็นที่จะได้จำนวนสองหลักที่{cond_txt}เท่ากับเท่าใด",
        correct=frac(ans),
        wrongs=[
            W(frac(Fraction(fav, 16)), "คิดจำนวนผลลัพธ์ทั้งหมดเป็น 4 × 4 = 16 แบบ (รวมกรณีใช้เลขซ้ำกัน)", "trap"),
            W(frac(Fraction(12 - fav, 12)), "ตอบความน่าจะเป็นของจำนวนที่ไม่ตรงเงื่อนไข", "misread"),
            W(frac(Fraction(min(11, fav + 1), 12)), "นับจำนวนสองหลักที่เข้าเงื่อนไขเกินมา 1 จำนวน", "calc"),
            W(frac(Fraction(max(1, fav - 1), 12)), "นับจำนวนสองหลักที่เข้าเงื่อนไขตกหล่นไป 1 จำนวน", "calc"),
        ],
        hint="การสร้างจำนวนสองหลักจากบัตร 4 ใบโดยไม่ซ้ำกัน หลักสิบเลือกได้ 4 วิธี และหลักหน่วยเลือกได้ 3 วิธี รวม 12 จำนวน",
        steps=[
            "จำนวนสองหลักทั้งหมดที่สร้างได้ (หลักสิบ 4 วิธี × หลักหน่วย 3 วิธี) = 12 จำนวน",
            f"จำนวนที่{cond_txt} มี {fav} จำนวน ได้แก่ {', '.join(str(x) for x in fav_list)}",
            f"ดังนั้นความน่าจะเป็น = [[{fav}/12]]" + (f" = {frac(ans)}" if ans.denominator != 12 else ""),
        ],
    )
