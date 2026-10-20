"""Ratio, proportion and percentage question templates for topic ``m.ratio`` (อัตราส่วนและร้อยละ).

Covers simplifying ratios (incl. unit conversion), proportions & best-buy unit
rates (with tables), sharing in a ratio & ratio chains (a:b and b:c -> a:b:c),
map scales (length & area trap), percentages (with pie charts), percent
increase/decrease (incl. rectangle area change), discounts & successive
discounts, profit/loss & reverse cost price / marked-price-with-discount,
simple interest & VAT, and top-school percentage mixture problems.
"""

from fractions import Fraction
import math
import random

from backend.bank import svg
from backend.bank.core import W, dec, mcq, name_th, num, pick, skill, template


# ===========================================================================
# Skill 1: m.ratio.basic — อัตราส่วนอย่างต่ำ สัดส่วน และราคาต่อหน่วย
# ===========================================================================

skill(
    "m.ratio.basic",
    "m.ratio",
    "อัตราส่วนอย่างต่ำ สัดส่วน และราคาต่อหน่วย",
    lesson={
        "concept": (
            "อัตราส่วน a : b ใช้เปรียบเทียบปริมาณสองปริมาณ ถ้ามีหน่วยต่างกันควรแปลงให้เป็นหน่วยเดียวกันก่อนทำเป็นอัตราส่วนอย่างต่ำ "
            "ส่วนสัดส่วนคือประโยคที่แสดงการเท่ากันของสองอัตราส่วน แก้ได้ด้วยการคูณไขว้หรือดูตัวคูณขยาย"
        ),
        "steps": [
            "ถ้าหน่วยต่างกัน (เช่น เมตรกับเซนติเมตร หรือ ชั่วโมงกับนาที) ให้แปลงเป็นหน่วยเล็กตัวเดียวกันก่อน",
            "นำ ห.ร.ม. ของจำนวนทั้งหมดมาหารทุกตัวเพื่อทำเป็นอัตราส่วนอย่างต่ำ",
            "การเปรียบเทียบความคุ้มค่า (Best buy): หาราคาต่อ 1 หน่วย (หรือเทียบปริมาณที่เท่ากัน เช่น ต่อ 100 กรัม)",
        ],
        "example": {
            "q": "อัตราส่วนของ 45 นาที ต่อ 1 ชั่วโมงครึ่ง ทำเป็นอัตราส่วนอย่างต่ำได้เท่าใด",
            "steps": [
                "แปลง 1 ชั่วโมงครึ่ง เป็นนาที: 60 + 30 = 90 นาที",
                "เขียนอัตราส่วน 45 : 90 แล้วหารด้วย 45 ทั้งสองข้าง ได้ 1 : 2",
            ],
            "a": "1 : 2",
        },
        "mistakes": [
            "ไม่แปลงหน่วยให้เหมือนกันก่อนทอนเป็นอัตราส่วนอย่างต่ำ เช่น นำ 45 นาที : 1.5 ชั่วโมง มาทอนเลย",
            "สลับลำดับหน้า-หลังของอัตราส่วน เช่น โจทย์ถาม A : B แต่ตอบ B : A",
        ],
        "tips": [
            "ในการเปรียบเทียบราคาสินค้าหลายขนาด ให้ปรับน้ำหนักเป็นจำนวนที่หารง่ายร่วมกัน เช่น 100 กรัม หรือ 1,000 กรัม จะไม่ต้องหารทศนิยมยาก ๆ",
        ],
    },
    weight=1.1,
)


@template("m.ratio.basic", "easy")
def _simplify_ratio_with_units():
    conv_type = pick([
        ("ซม.", "เมตร", 100),
        ("กรัม", "กิโลกรัม", 1000),
        ("นาที", "ชั่วโมง", 60),
        ("มล.", "ลิตร", 1000),
    ])
    u_small, u_big, factor = conv_type
    big_n = random.choice([1, 2, 3])
    total_big_in_small = big_n * factor
    # Pick small_n that shares a nice GCD with total_big_in_small
    divisors = [d for d in (10, 12, 15, 20, 25, 30, 40, 50, 75, 100, 120, 150, 200, 250) if total_big_in_small % d == 0]
    g = random.choice(divisors)
    q_big = total_big_in_small // g
    coprimes = [x for x in range(1, q_big + 5) if math.gcd(x, q_big) == 1 and x != q_big]
    q_small = random.choice(coprimes)
    small_n = q_small * g
    ans = f"{q_small} : {q_big}"
    rev_ans = f"{q_big} : {q_small}"
    g_raw = math.gcd(small_n, big_n)
    wrong_no_unit = f"{small_n // g_raw} : {big_n // g_raw}"
    wrong_unreduced = f"{q_small * 2} : {q_big * 2}"
    return mcq(
        stem=f"อัตราส่วนของ **{num(small_n)} {u_small} ต่อ {big_n} {u_big}** เมื่อทำเป็นอัตราส่วนอย่างต่ำในหน่วยเดียวกันตรงกับข้อใด",
        correct=ans,
        wrongs=[
            W(wrong_no_unit, f"ไม่ได้แปลง {big_n} {u_big} ให้เป็น{u_small}ก่อนทำเป็นอัตราส่วนอย่างต่ำ", "unit"),
            W(rev_ans, "สลับลำดับหน้า-หลังของอัตราส่วนที่โจทย์ถาม", "misread"),
            W(wrong_unreduced, "ยังทอนเป็นอัตราส่วนอย่างต่ำไม่สุด (ยังหารด้วย 2 ต่อได้อีก)", "partial"),
        ],
        hint=f"แปลง {big_n} {u_big} เป็น{u_small}ก่อน (1 {u_big} = {num(factor)} {u_small}) แล้วหารด้วย ห.ร.ม.",
        steps=[
            f"แปลงหน่วยให้เป็น{u_small}: {big_n} {u_big} = {big_n} × {num(factor)} = {num(total_big_in_small)} {u_small}",
            f"ได้อัตราส่วน {num(small_n)} : {num(total_big_in_small)}",
            f"หารด้วย ห.ร.ม. คือ {g} ทั้งสองจำนวน ได้อัตราส่วนอย่างต่ำ = {ans}",
        ],
    )


@template("m.ratio.basic", "medium")
def _best_buy_table():
    product = pick(["ผงซักฟอก", "นมสด", "ข้าวสาร", "น้ำผลไม้", "อาหารสุนัข", "เมล็ดกาแฟ"])
    # 4 sizes in grams: 200, 400, 500, 1000
    sizes = [200, 400, 500, 1000]
    # Price per 100g for each brand (in baht), all distinct integers
    rates_per_100 = random.sample(range(12, 28), 4)
    labels = ["ขนาด A", "ขนาด B", "ขนาด C", "ขนาด D"]
    prices = [int((sz // 100) * r) for sz, r in zip(sizes, rates_per_100)]
    min_idx = rates_per_100.index(min(rates_per_100))
    max_idx = rates_per_100.index(max(rates_per_100))
    cheapest_pack_idx = prices.index(min(prices))
    other_idxs = [i for i in range(4) if i != min_idx]
    tbl = {
        "head": ["ตัวเลือก", "ปริมาณ (กรัม)", "ราคา (บาท)"],
        "rows": [[labels[i], num(sizes[i]), num(prices[i])] for i in range(4)],
    }
    wrongs = []
    if cheapest_pack_idx != min_idx:
        wrongs.append(W(labels[cheapest_pack_idx], "ดูเฉพาะราคารวมที่จ่ายน้อยที่สุด โดยไม่ได้คิดเทียบราคาต่อปริมาณที่เท่ากัน", "trap"))
    if max_idx != min_idx:
        wrongs.append(W(labels[max_idx], f"นี่คือขนาดที่ราคาต่อ 100 กรัม แพงที่สุด ({rates_per_100[max_idx]} บาทต่อ 100 กรัม)", "misread"))
    for idx in other_idxs:
        wrongs.append(W(labels[idx], f"คิดเป็น {rates_per_100[idx]} บาทต่อ 100 กรัม ซึ่งยังไม่ใช่ตัวเลือกที่ถูกที่สุด", "calc"))
    return mcq(
        stem=f"ตารางแสดงปริมาณและราคาของ{product} 4 ขนาด ซื้อขนาดใด **คุ้มค่าที่สุด** (ราคาเฉลี่ยต่อกรัมถูกที่สุด)",
        table=tbl,
        correct=labels[min_idx],
        wrongs=wrongs,
        hint="เทียบราคาต่อปริมาณที่เท่ากัน เช่น คิดราคาต่อ 100 กรัม ของแต่ละขนาด",
        steps=[
            "คิดราคาต่อปริมาณ 100 กรัม ของแต่ละขนาด:",
            f"ขนาด A = {prices[0]} ÷ 2 = {rates_per_100[0]} บาท, ขนาด B = {prices[1]} ÷ 4 = {rates_per_100[1]} บาท",
            f"ขนาด C = {prices[2]} ÷ 5 = {rates_per_100[2]} บาท, ขนาด D = {prices[3]} ÷ 10 = {rates_per_100[3]} บาท",
            f"ดังนั้น {labels[min_idx]} ถูกที่สุด ({rates_per_100[min_idx]} บาทต่อ 100 กรัม)",
        ],
    )


@template("m.ratio.basic", "hard")
def _ratio_add_one_side():
    # Syrup : water = a : b. After adding k litres of water, ratio becomes a : c. Find initial syrup or total!
    a = random.choice([2, 3, 4, 5])
    b = random.randint(a + 1, a + 5)
    c = b + random.choice([2, 3, 4])
    unit_val = random.randint(3, 12)
    added_water = (c - b) * unit_val
    syrup_amt = a * unit_val
    init_total = (a + b) * unit_val
    final_total = (a + c) * unit_val
    return mcq(
        stem=(
            f"น้ำหวานในถังมีอัตราส่วนของ **น้ำเชื่อม ต่อ น้ำเปล่า เป็น {a} : {b}** "
            f"เมื่อเติมน้ำเปล่าเพิ่มลงไปอีก **{added_water} ลิตร** (โดยไม่เติมน้ำเชื่อม) "
            f"ทำให้อัตราส่วนของน้ำเชื่อมต่อน้ำเปล่ากลายเป็น **{a} : {c}** "
            f"อยากทราบว่า **เดิม** ในถังมีน้ำหวานรวมกันทั้งหมดกี่ลิตร"
        ),
        correct=f"{init_total} ลิตร",
        wrongs=[
            W(f"{final_total} ลิตร", "นี่คือปริมาณน้ำหวานทั้งหมดหลังจากเติมน้ำเปล่าเพิ่มแล้ว โจทย์ถามปริมาณเดิม", "misread"),
            W(f"{syrup_amt} ลิตร", "นี่คือปริมาณน้ำเชื่อมอย่างเดียว ไม่ใช่น้ำหวานเดิมทั้งหมดในถัง", "partial"),
            W(f"{b * unit_val} ลิตร", "นี่คือปริมาณน้ำเปล่าเดิมอย่างเดียว ลืมรวมปริมาณน้ำเชื่อม", "partial"),
        ],
        hint=f"ปริมาณน้ำเชื่อมคงเดิมคือ {a} ส่วน ส่วนน้ำเปล่าเพิ่มขึ้นจาก {b} ส่วน เป็น {c} ส่วน (เพิ่มขึ้น {c - b} ส่วน = {added_water} ลิตร)",
        steps=[
            f"ปริมาณน้ำเชื่อมเท่าเดิมคือ {a} ส่วน ส่วนน้ำเปล่าเพิ่มขึ้น {c} − {b} = {c - b} ส่วน",
            f"น้ำเปล่าที่เติมเพิ่ม {c - b} ส่วน คิดเป็น {added_water} ลิตร ดังนั้น 1 ส่วน = {added_water} ÷ {c - b} = {unit_val} ลิตร",
            f"เดิมมีน้ำหวานรวม {a} + {b} = {a + b} ส่วน คิดเป็น {a + b} × {unit_val} = {init_total} ลิตร",
        ],
    )


# ===========================================================================
# Skill 2: m.ratio.share — การแบ่งตามอัตราส่วนและอัตราส่วนต่อเนื่อง
# ===========================================================================

skill(
    "m.ratio.share",
    "m.ratio",
    "การแบ่งตามอัตราส่วนและอัตราส่วนต่อเนื่อง",
    lesson={
        "concept": (
            "การเชื่อมอัตราส่วนสองคู่ เช่น A : B และ B : C ให้ทำตัวร่วม (B) ให้เท่ากันโดยใช้ ค.ร.น. "
            "เมื่อได้อัตราส่วนรวม A : B : C แล้ว จึงเทียบจำนวนส่วนกับค่าจริงที่โจทย์กำหนด (ผลรวม หรือ ผลต่าง) เพื่อหาค่าของ 1 ส่วน"
        ),
        "steps": [
            "เขียนอัตราส่วนโดยให้ตัวร่วมอยู่ตรงกัน แล้วคูณแต่ละอัตราส่วนเพื่อให้ตัวร่วมเท่ากับ ค.ร.น.",
            "ดูว่าตัวเลขที่โจทย์ให้มาคือ 'ผลรวมทั้งหมด' หรือ 'ผลต่างของสองคน' หรือ 'ค่าของคนใดคนหนึ่ง'",
            "หาค่าของ 1 ส่วน = ค่าจริงที่รู้ ÷ จำนวนส่วนที่ตรงกัน แล้วคูณจำนวนส่วนของสิ่งที่โจทย์ถาม",
        ],
        "example": {
            "q": "ถ้า A : B = 2 : 3 และ B : C = 4 : 5 เมื่อทั้งสามคนมีเงินรวมกัน 140 บาท B มีเงินกี่บาท",
            "steps": [
                "ทำ B ให้เท่ากัน (ค.ร.น. ของ 3 และ 4 คือ 12): A : B = 8 : 12 และ B : C = 12 : 15",
                "ได้ A : B : C = 8 : 12 : 15 รวมทั้งหมด 8 + 12 + 15 = 35 ส่วน",
                "1 ส่วน = 140 ÷ 35 = 4 บาท ดังนั้น B มีเงิน 12 × 4 = 48 บาท",
            ],
            "a": "48 บาท",
        },
        "mistakes": [
            "นำอัตราส่วนมาบวกกันเลยโดยยังไม่ได้ทำตัวร่วม B ให้เท่ากันก่อน (เช่น เอา 2 + 3 + 5)",
            "โจทย์ให้ผลต่างของ A กับ C มา แต่เผลอเอาจำนวนส่วนทั้งหมดไปหาร",
        ],
        "tips": [
            "ตรวจคำตอบเร็ว ๆ: นำคำตอบที่ได้มาทอนอัตราส่วนย้อนกลับว่าตรงกับที่โจทย์กำหนดหรือไม่",
        ],
    },
    weight=1.7,
)


@template("m.ratio.share", "easy")
def _share_in_ratio_diff_or_total():
    triples = [(2, 3, 5), (2, 5, 7), (3, 4, 5), (3, 5, 7), (4, 5, 6), (2, 3, 4), (3, 5, 8)]
    a, b, c = pick(triples)
    unit_val = random.randint(15, 50)
    p1, p2, p3 = name_th(3)
    mode = random.choice(["given_total_ask_diff", "given_diff_ask_total"])
    total_parts = a + b + c
    diff_parts = c - a
    total_money = total_parts * unit_val
    diff_money = diff_parts * unit_val
    if mode == "given_total_ask_diff":
        return mcq(
            stem=(
                f"{p1}, {p2} และ{p3} แบ่งเงินกันในอัตราส่วน **{a} : {b} : {c}** "
                f"ถ้าทั้งสามคนได้รับเงินรวมกันทั้งหมด **{num(total_money)} บาท** "
                f"แล้ว{p3}ได้รับเงินมากกว่า{p1}กี่บาท"
            ),
            correct=f"{num(diff_money)} บาท",
            wrongs=[
                W(f"{num(c * unit_val)} บาท", f"นี่คือเงินของ{p3}ทั้งหมด ลืมลบเงินของ{p1}ออก", "partial"),
                W(f"{num(a * unit_val)} บาท", f"นี่คือเงินของ{p1} ไม่ใช่ผลต่างของ{p3}กับ{p1}", "misread"),
                W(f"{num((c - b) * unit_val)} บาท", f"นำส่วนของ{p3}ลบด้วยส่วนของ{p2} แทนที่จะลบด้วยส่วนของ{p1}", "misread"),
            ],
            hint=f"รวมจำนวนส่วนทั้งหมดได้ {a}+{b}+{c} = {total_parts} ส่วน หาค่าของ 1 ส่วน แล้วคูณผลต่างส่วนของ{p3}กับ{p1}",
            steps=[
                f"จำนวนส่วนทั้งหมด = {a} + {b} + {c} = {total_parts} ส่วน คิดเป็น {num(total_money)} บาท",
                f"ดังนั้น 1 ส่วน = {num(total_money)} ÷ {total_parts} = {unit_val} บาท",
                f"{p3}ได้มากกว่า{p1} = {c} − {a} = {diff_parts} ส่วน คิดเป็น {diff_parts} × {unit_val} = {num(diff_money)} บาท",
            ],
        )
    else:
        return mcq(
            stem=(
                f"แบ่งเงินจำนวนหนึ่งให้ {p1}, {p2} และ{p3} ในอัตราส่วน **{a} : {b} : {c}** ตามลำดับ "
                f"ถ้า{p3}ได้รับเงินมากกว่า{p1}อยู่ **{num(diff_money)} บาท** "
                f"เงินที่นำมาแบ่งทั้งหมดมีกี่บาท"
            ),
            correct=f"{num(total_money)} บาท",
            wrongs=[
                W(f"{num(c * unit_val)} บาท", f"นี่คือเงินของ{p3}คนเดียว ไม่ใช่เงินรวมของทั้งสามคน", "partial"),
                W(f"{num((a + c) * unit_val)} บาท", f"รวมเฉพาะเงินของ{p1}กับ{p3} ลืมบวกส่วนของ{p2}", "partial"),
                W(f"{num(diff_money * total_parts)} บาท", f"ลืมหารด้วยผลต่างของจำนวนส่วน ({c} − {a} = {diff_parts} ส่วน) ก่อนคูณจำนวนส่วนรวม", "concept"),
            ],
            hint=f"{p3}มากกว่า{p1}อยู่ {c} − {a} = {diff_parts} ส่วน ซึ่งเท่ากับ {num(diff_money)} บาท หาค่า 1 ส่วนก่อน",
            steps=[
                f"ส่วนของ{p3}มากกว่า{p1} = {c} − {a} = {diff_parts} ส่วน คิดเป็นเงิน {num(diff_money)} บาท",
                f"จะได้ 1 ส่วน = {num(diff_money)} ÷ {diff_parts} = {unit_val} บาท",
                f"เงินทั้งหมดมี {a} + {b} + {c} = {total_parts} ส่วน คิดเป็น {total_parts} × {unit_val} = {num(total_money)} บาท",
            ],
        )


@template("m.ratio.share", "medium")
def _ratio_chain_abc():
    # A : B = a1 : b1 and B : C = b2 : c2 where gcd(b1, b2) == 1
    ab_pairs = [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5)]
    bc_pairs = [(2, 3), (4, 5), (3, 5), (5, 6), (2, 5)]
    a1, b1 = pick(ab_pairs)
    b2, c2 = pick(bc_pairs)
    if b1 == b2:
        b2 += 1
    lcm_b = math.lcm(b1, b2)
    ra = a1 * (lcm_b // b1)
    rb = lcm_b
    rc = c2 * (lcm_b // b2)
    total_parts = ra + rb + rc
    unit_val = random.randint(4, 15)
    total_val = total_parts * unit_val
    ans_b = rb * unit_val
    ans_c = rc * unit_val
    naive_parts = a1 + b1 + c2
    return mcq(
        stem=(
            f"กำหนดอัตราส่วน **A : B = {a1} : {b1}** และ **B : C = {b2} : {c2}** "
            f"ถ้า **A + B + C = {num(total_val)}** แล้ว **C** มีค่าเท่าใด"
        ),
        correct=num(ans_c),
        wrongs=[
            W(num(ans_b), f"นี่คือค่าของ B ({rb} ส่วน) โจทย์ถามค่าของ C ({rc} ส่วน)", "misread"),
            W(num(ra * unit_val), f"นี่คือค่าของ A ({ra} ส่วน) โจทย์ถามค่าของ C", "misread"),
            W(num(c2 * unit_val), f"ลืมคูณขยายส่วนของ C ตอนทำตัวร่วม B ให้เท่ากับ {lcm_b}", "partial"),
        ],
        hint=f"ทำตัวร่วม B ให้เท่ากับ ค.ร.น. ของ {b1} และ {b2} คือ {lcm_b} เพื่อให้ได้อัตราส่วน A : B : C",
        steps=[
            f"ทำตัวร่วม B ให้เท่ากับ {lcm_b}: A : B = {ra} : {rb} และ B : C = {rb} : {rc}",
            f"จะได้ A : B : C = {ra} : {rb} : {rc} รวมทั้งหมด {ra} + {rb} + {rc} = {total_parts} ส่วน",
            f"1 ส่วน = {num(total_val)} ÷ {total_parts} = {unit_val} ดังนั้น C = {rc} × {unit_val} = {num(ans_c)}",
        ],
    )


@template("m.ratio.share", "hard")
def _ratio_internal_transfer():
    # Classic top-school invariant-total ratio problem:
    # Two people have money in ratio a1:b1. After first gives K baht to second, ratio becomes a2:b2.
    # Notice total money is UNCHANGED! Make a1+b1 and a2+b2 equal or scale to their LCM.
    configs = [
        (3, 2, 1, 1),   # sums 5 and 2 -> LCM 10: (6:4) -> (5:5), transfer 1 part
        (5, 3, 1, 1),   # sums 8 -> (5:3) -> (4:4), transfer 1 part
        (4, 3, 5, 9),   # sums 7 and 14 -> LCM 14: (8:6) -> (5:9), transfer 3 parts
        (5, 2, 3, 4),   # sums 7: (5:2) -> (3:4), transfer 2 parts
        (7, 5, 1, 1),   # sums 12 -> (7:5) -> (6:6), transfer 1 part
        (3, 1, 5, 3),   # sums 4 and 8 -> (6:2) -> (5:3), transfer 1 part
        (5, 4, 1, 2),   # sums 9 and 3 -> (5:4) -> (3:6), transfer 2 parts
    ]
    a1, b1, a2, b2 = pick(configs)
    s1, s2 = a1 + b1, a2 + b2
    lcm_s = math.lcm(s1, s2)
    p1_before = a1 * (lcm_s // s1)
    p2_before = b1 * (lcm_s // s1)
    p1_after = a2 * (lcm_s // s2)
    p2_after = b2 * (lcm_s // s2)
    diff_p = p1_before - p1_after
    unit_val = random.randint(20, 80)
    transfer = diff_p * unit_val
    total_money = lcm_s * unit_val
    n1, n2 = name_th(2)
    return mcq(
        stem=(
            f"เดิม{n1}และ{n2}มีเงินอยู่ในอัตราส่วน **{a1} : {b1}** "
            f"ต่อมา{n1}แบ่งเงินของตนให้{n2}ไป **{num(transfer)} บาท** "
            f"ทำให้อัตราส่วนเงินของ{n1}ต่อ{n2}เปลี่ยนเป็น **{a2} : {b2}** "
            f"อยากทราบว่าทั้งสองคนมีเงินรวมกันทั้งหมดกี่บาท"
        ),
        correct=f"{num(total_money)} บาท",
        wrongs=[
            W(f"{num(p1_before * unit_val)} บาท", f"นี่คือเงินเดิมของ{n1}คนเดียว ไม่ใช่เงินรวมของทั้งสองคน", "partial"),
            W(f"{num(p2_before * unit_val)} บาท", f"นี่คือเงินเดิมของ{n2}คนเดียว ไม่ใช่เงินรวมของทั้งสองคน", "partial"),
            W(f"{num((s1 + s2) * unit_val)} บาท", "ลืมปรับจำนวนส่วนรวมก่อนและหลังให้เท่ากันก่อนเทียบเงินที่โอนให้กัน", "concept"),
        ],
        hint=f"การแบ่งเงินให้กันเองทำให้ 'ผลรวมของเงินทั้งสองคนคงเดิม' จึงปรับผลบวกของอัตราส่วนทั้งสองให้เท่ากับ {lcm_s} ส่วนเท่ากัน",
        steps=[
            f"เนื่องจากเป็นการให้เงินกันเอง ผลรวมเงินของทั้งสองคนจึงเท่าเดิมเสมอ",
            f"ปรับผลรวมส่วนให้เท่ากับ {lcm_s} ส่วน: เดิม = {p1_before} : {p2_before} และหลังให้เงิน = {p1_after} : {p2_after}",
            f"ส่วนของ{n1}ลดลง {p1_before} − {p1_after} = {diff_p} ส่วน คิดเป็น {num(transfer)} บาท (1 ส่วน = {unit_val} บาท)",
            f"ดังนั้นทั้งสองคนมีเงินรวมกัน = {lcm_s} × {unit_val} = {num(total_money)} บาท",
        ],
    )


# ===========================================================================
# Skill 3: m.ratio.scale — มาตราส่วนและแผนผัง
# ===========================================================================

skill(
    "m.ratio.scale",
    "m.ratio",
    "มาตราส่วนและแผนผัง",
    lesson={
        "concept": (
            "มาตราส่วน = ความยาวในรูป (หรือแผนที่) : ความยาวจริง "
            "ถ้าไม่มีหน่วยกำกับ แปลว่าเป็นหน่วยเดียวกัน (เช่น 1 : 100,000 คือ 1 ซม. : 100,000 ซม. = 1 กม.) และระวังการหาพื้นที่จริงต้องแปลงความยาวแต่ละด้านเป็นความยาวจริงก่อนคูณกัน!"
        ),
        "steps": [
            "จำการแปลงหน่วยความยาว: 1 เมตร = 100 ซม. และ 1 กิโลเมตร = 1,000 เมตร = 100,000 ซม.",
            "หาความยาวจริง = ความยาวในแผนผัง × ตัวคูณมาตราส่วน แล้วแปลงเป็นเมตรหรือกิโลเมตร",
            "หากถาม 'พื้นที่จริง': แปลงความกว้างจริงและความยาวจริงแต่ละด้านก่อน แล้วจึงนำมาคูณกัน (ห้ามเอาพื้นที่ในรูปคูณมาตราส่วนแค่ครั้งเดียว!)",
        ],
        "example": {
            "q": "แผนผังใช้มาตราส่วน 1 : 500 ที่ดินรูปสี่เหลี่ยมผืนผ้าในแผนผังกว้าง 4 ซม. ยาว 6 ซม. ที่ดินจริงมีพื้นที่กี่ตารางเมตร",
            "steps": [
                "มาตราส่วน 1 : 500 แปลว่า 1 ซม. ในแผนผัง แทนความยาวจริง 500 ซม. = 5 เมตร",
                "ความกว้างจริง = 4 × 5 = 20 เมตร และความยาวจริง = 6 × 5 = 30 เมตร",
                "พื้นที่จริง = 20 × 30 = 600 ตารางเมตร",
            ],
            "a": "600 ตร.ม.",
        },
        "mistakes": [
            "แปลงเซนติเมตรเป็นกิโลเมตรผิด (1 กม. = 100,000 ซม. มีศูนย์ 5 ตัว ไม่ใช่ 3 หรือ 4 ตัว)",
            "หาพื้นที่จริงโดยนำพื้นที่ในแผนผัง (กว้าง × ยาว) คูณมาตราส่วนเพียงครั้งเดียว แทนที่จะคูณทั้งด้านกว้างและด้านยาว",
        ],
        "tips": [
            "สูตรลัดแปลงมาตราส่วน 1 : N (ซม.) เป็นกิโลเมตร: ตัดเลข 0 ออก 5 ตัว! เช่น 1 : 200,000 คือ 1 ซม. ต่อ 2 กม.",
        ],
    },
    weight=1.3,
)


@template("m.ratio.scale", "easy")
def _map_scale_distance():
    scale_km = random.choice([2, 3, 4, 5, 8, 10, 15, 20, 25])
    scale_cm = scale_km * 100_000
    map_cm = random.randint(3, 18)
    real_km = map_cm * scale_km
    return mcq(
        stem=(
            f"แผนที่ฉบับหนึ่งใช้มาตราส่วน **1 : {num(scale_cm)}** "
            f"ถ้าวัดระยะทางระหว่างเมืองสองเมืองในแผนที่ได้ **{map_cm} เซนติเมตร** "
            f"ระยะทางจริงระหว่างสองเมืองนี้เป็นกี่กิโลเมตร"
        ),
        correct=f"{num(real_km)} กิโลเมตร",
        wrongs=[
            W(f"{num(real_km * 10)} กิโลเมตร", "แปลงหน่วยเซนติเมตรเป็นกิโลเมตรโดยหารด้วย 10,000 แทนที่จะเป็น 100,000", "unit"),
            W(f"{num(real_km * 100)} กิโลเมตร", "แปลงเซนติเมตรเป็นเมตร (หารด้วย 100) หรือหารด้วย 1,000 เท่านั้น", "unit"),
            W(f"{num(scale_km + map_cm)} กิโลเมตร", "นำระยะในแผนที่ไปบวกกับมาตราส่วนแทนที่จะนำมาคูณกัน", "concept"),
        ],
        hint="1 กิโลเมตร = 1,000 เมตร = 100,000 เซนติเมตร (ตัดเลขศูนย์ออก 5 ตัว)",
        steps=[
            f"จากมาตราส่วน 1 : {num(scale_cm)} แปลว่า 1 ซม. แทนระยะจริง {num(scale_cm)} ซม. = {scale_km} กิโลเมตร",
            f"ระยะในแผนที่ {map_cm} ซม. คิดเป็นระยะทางจริง = {map_cm} × {scale_km} = {num(real_km)} กิโลเมตร",
        ],
    )


@template("m.ratio.scale", "medium")
def _map_scale_travel_time():
    scale_km = random.choice([5, 6, 8, 10, 12, 15])
    scale_cm = scale_km * 100_000
    speed = random.choice([60, 75, 80, 90])
    # Pick map_cm so that real_km / speed is a clean number of hours or hours + 30 min
    hours = random.randint(2, 5)
    real_km = speed * hours
    if real_km % scale_km != 0:
        scale_km = 5
        scale_cm = 500_000
        real_km = speed * hours
    map_cm = real_km // scale_km
    return mcq(
        stem=(
            f"แผนที่ใช้มาตราส่วน **1 : {num(scale_cm)}** เมือง ก และเมือง ข อยู่ห่างกันในแผนที่ **{map_cm} เซนติเมตร** "
            f"ถ้าขับรถจากเมือง ก ไปเมือง ข ด้วยอัตราเร็วเฉลี่ย **{speed} กิโลเมตรต่อชั่วโมง** จะใช้เวลาเดินทางกี่ชั่วโมง"
        ),
        correct=f"{hours} ชั่วโมง",
        wrongs=[
            W(f"{hours * 10} ชั่วโมง", "แปลงเซนติเมตรเป็นกิโลเมตรพลาดไป 1 หลัก (1 กม. = 100,000 ซม.)", "unit"),
            W(f"{real_km} ชั่วโมง", f"{real_km} คือระยะทางจริงเป็นกิโลเมตร ยังไม่ได้หารด้วยอัตราเร็ว {speed} กม./ชม.", "partial"),
            W(f"{max(1, hours - 1)} ชั่วโมง", "หารระยะทางด้วยอัตราเร็วคลาดเคลื่อน", "calc"),
        ],
        hint="หาระยะทางจริงเป็นกิโลเมตรก่อน แล้วใช้สูตร เวลา = ระยะทาง ÷ อัตราเร็ว",
        steps=[
            f"มาตราส่วน 1 : {num(scale_cm)} คือ 1 ซม. แทนระยะจริง {scale_km} กม.",
            f"ระยะทางจริง = {map_cm} × {scale_km} = {real_km} กิโลเมตร",
            f"เวลาที่ใช้ = {real_km} ÷ {speed} = {hours} ชั่วโมง",
        ],
    )


@template("m.ratio.scale", "hard")
def _map_scale_area_trap():
    # Classic top-school trap: scale 1 : (m * 100), so 1 cm = m metres.
    # Rectangle on plan is w cm by l cm. Find actual area in sq.m.!
    m_per_cm = random.choice([2, 3, 4, 5, 6, 8, 10])
    scale_n = m_per_cm * 100
    w_cm = random.randint(3, 9)
    l_cm = random.randint(w_cm + 2, 15)
    real_w = w_cm * m_per_cm
    real_l = l_cm * m_per_cm
    real_area = real_w * real_l
    plan_area = w_cm * l_cm
    wrong_once = plan_area * m_per_cm
    wrong_perim = 2 * (real_w + real_l)
    return mcq(
        stem=(
            f"แผนผังที่ดินใช้มาตราส่วน **1 : {num(scale_n)}** "
            f"ถ้าที่ดินแปลงหนึ่งในแผนผังเป็นรูปสี่เหลี่ยมผืนผ้ากว้าง **{w_cm} เซนติเมตร** ยาว **{l_cm} เซนติเมตร** "
            f"ที่ดินแปลงนี้มี **พื้นที่จริง** กี่ตารางเมตร"
        ),
        correct=f"{num(real_area)} ตารางเมตร",
        wrongs=[
            W(f"{num(wrong_once)} ตารางเมตร",
              f"นำพื้นที่ในแผนผัง ({w_cm}×{l_cm} = {plan_area}) คูณด้วย {m_per_cm} เพียงครั้งเดียว ลืมว่าต้องคูณทั้งด้านกว้างและด้านยาว", "trap"),
            W(f"{num(plan_area * scale_n)} ตารางเมตร",
              f"นำพื้นที่ในแผนผังไปคูณ {num(scale_n)} แล้วตอบเป็นตารางเมตรโดยไม่ได้แปลงหน่วยตารางเซนติเมตรเป็นตารางเมตร", "unit"),
            W(f"{num(wrong_perim)} ตารางเมตร", "คำนวณความยาวรอบรูปจริงแทนที่จะหาพื้นที่จริง", "formula"),
        ],
        hint=f"มาตราส่วน 1 : {num(scale_n)} แปลว่า 1 ซม. แทนความยาวจริง {num(scale_n)} ซม. = {m_per_cm} เมตร แปลงความกว้างและความยาวจริงก่อนนำมาคูณกัน",
        steps=[
            f"มาตราส่วน 1 : {num(scale_n)} คือ 1 ซม. ในแผนผัง แทนความยาวจริง {num(scale_n)} ซม. = {m_per_cm} เมตร",
            f"ความกว้างจริง = {w_cm} × {m_per_cm} = {real_w} เมตร และความยาวจริง = {l_cm} × {m_per_cm} = {real_l} เมตร",
            f"พื้นที่จริง = {real_w} × {real_l} = {num(real_area)} ตารางเมตร",
        ],
    )


# ===========================================================================
# Skill 4: m.ratio.pct_basic — ร้อยละของจำนวนและแผนภูมิวงกลมร้อยละ
# ===========================================================================

skill(
    "m.ratio.pct_basic",
    "m.ratio",
    "ร้อยละของจำนวนและการเทียบร้อยละย้อนกลับ",
    lesson={
        "concept": (
            "ร้อยละ p (หรือ p%) หมายถึง [[p/100]] คำว่า 'ของ' คือการคูณ "
            "หากต้องการหาว่า A คิดเป็นกี่เปอร์เซ็นต์ของ B ให้คำนวณ (A ÷ B) × 100%"
        ),
        "steps": [
            "หา p% ของ N: คำนวณ (p / 100) × N",
            "ถามว่า A คิดเป็นกี่เปอร์เซ็นต์ของ B: นำ A เป็นตัวตั้ง หารด้วย B (ตัวหลังคำว่า 'ของ') แล้วคูณ 100",
            "ถ้าโจทย์บอกค่าของ p% มาให้ แล้วถามหาค่าอื่น (q%): ใช้เทียบบัญญัติไตรยางศ์ ค่าที่ถาม = (ค่าที่รู้ ÷ p) × q",
        ],
        "example": {
            "q": "ถ้า 35% ของจำนวนหนึ่งเท่ากับ 140 แล้ว 60% ของจำนวนนั้นมีค่าเท่าใด",
            "steps": [
                "35% คิดเป็น 140 ดังนั้น 1% = 140 ÷ 35 = 4",
                "ต้องการหา 60% จึงมีค่า = 60 × 4 = 240",
            ],
            "a": "240",
        },
        "mistakes": [
            "สลับตัวตั้งกับตัวหารเวลาถามว่า A คิดเป็นกี่เปอร์เซ็นต์ของ B",
            "ในแผนภูมิวงกลม ลืมว่าผลรวมของทุกส่วนทั้งหมดต้องเท่ากับ 100% เสมอ",
        ],
        "tips": [
            "ถ้าโจทย์ให้ p% มา แล้วถาม q% ของจำนวนเดียวกัน ไม่ต้องเสียเวลาหา 100% ก่อน สามารถเทียบ (ค่าที่รู้ ÷ p) × q ได้เลยในขั้นเดียว!",
        ],
    },
    weight=1.4,
)


@template("m.ratio.pct_basic", "easy")
def _what_percent_or_pct_of():
    # If p% of N is V, what is q% of N?
    p = random.choice([15, 20, 25, 30, 35, 40, 45])
    q = random.choice([55, 60, 65, 70, 75, 80, 85])
    one_pct = random.randint(3, 18)
    total = one_pct * 100
    val_p = p * one_pct
    val_q = q * one_pct
    return mcq(
        stem=f"ถ้า **{p}%** ของจำนวนนับจำนวนหนึ่งเท่ากับ **{num(val_p)}** แล้ว **{q}%** ของจำนวนนับนั้นมีค่าเท่าใด",
        correct=num(val_q),
        wrongs=[
            W(num(total), f"นี่คือค่าของจำนวนนั้นทั้งหมด (100%) ยังไม่ได้คูณหา {q}%", "partial"),
            W(num(val_q - val_p), f"นำค่าของ {q}% ลบด้วย {p}% แทนที่จะตอบค่าของ {q}%", "misread"),
            W(num((val_p * p) // q if (val_p * p) // q != val_q else val_q + one_pct * 5),
              "ตั้งสัดส่วนบัญญัติไตรยางศ์สลับตัวคูณกับตัวหาร", "formula"),
        ],
        hint=f"หาค่าของ 1% ก่อนโดยนำ {num(val_p)} ÷ {p} แล้วคูณด้วย {q}",
        steps=[
            f"เนื่องจาก {p}% ของจำนวนนั้น = {num(val_p)} จะได้ 1% = {num(val_p)} ÷ {p} = {one_pct}",
            f"(หรือจำนวนทั้งหมด 100% = {num(total)})",
            f"ดังนั้น {q}% ของจำนวนนั้น = {q} × {one_pct} = {num(val_q)}",
        ],
    )


@template("m.ratio.pct_basic", "medium")
def _pie_chart_percent_fig():
    # Pie chart of 4 categories where 3 percentages are given and the 4th is computed from 100%
    p1 = random.choice([25, 30, 35])
    p2 = random.choice([20, 25])
    p3 = random.choice([15, 20])
    p4 = 100 - (p1 + p2 + p3)
    if len({p1, p2, p3, p4}) < 3 or p4 < 10:
        return None
    cats = ["คณิตศาสตร์", "วิทยาศาสตร์", "ภาษาอังกฤษ", "ภาษาไทย"]
    percents = [p1, p2, p3, p4]
    fig = svg.pie_chart(cats, percents, title="วิชาที่นักเรียนชั้น ป.6 ชอบมากที่สุด")
    one_pct = random.randint(2, 9)
    total = one_pct * 100
    # Given the difference between cat 0 and cat 2 (or given cat 1 count), ask for cat 3 count
    diff_0_2 = (p1 - p3) * one_pct
    ans = p4 * one_pct
    return mcq(
        stem=(
            f"จากแผนภูมิวงกลม ถ้านักเรียนที่ชอบ **{cats[0]}** มีมากกว่านักเรียนที่ชอบ **{cats[2]}** อยู่ **{diff_0_2} คน** "
            f"จะมีนักเรียนที่ชอบ **{cats[3]}** กี่คน"
        ),
        figure=fig,
        correct=f"{ans} คน",
        wrongs=[
            W(f"{total} คน", "นี่คือจำนวนนักเรียนทั้งหมด 100% โจทย์ถามเฉพาะคนที่ชอบภาษาไทย", "misread"),
            W(f"{p1 * one_pct} คน", f"นี่คือจำนวนนักเรียนที่ชอบ{cats[0]} ({p1}%)", "misread"),
            W(f"{p4 * (diff_0_2 // 5) if diff_0_2 % 5 == 0 and (diff_0_2 // 5) != one_pct else ans + p4} คน",
              f"ไม่ได้นำผลต่างของเปอร์เซ็นต์ ({p1}% − {p3}% = {p1 - p3}%) ไปหาร {diff_0_2} คนเพื่อหาค่าของ 1%", "concept"),
        ],
        hint=f"หาผลต่างเปอร์เซ็นต์ของวิชา{cats[0]}กับ{cats[2]} ({p1}% − {p3}% = {p1 - p3}%) แล้วเทียบกับ {diff_0_2} คน",
        steps=[
            f"นักเรียนที่ชอบ{cats[0]}มากกว่า{cats[2]} = {p1}% − {p3}% = {p1 - p3}% คิดเป็น {diff_0_2} คน",
            f"ดังนั้น 1% คิดเป็น {diff_0_2} ÷ {p1 - p3} = {one_pct} คน",
            f"นักเรียนที่ชอบ{cats[3]}มี {p4}% = {p4} × {one_pct} = {ans} คน",
        ],
    )


@template("m.ratio.pct_basic", "hard")
def _nested_percentage_students():
    # In a school, boys are p_boy% of all students. Of the boys, p_glass% wear glasses.
    # Given the number of boys who DO NOT wear glasses is K, find total students in the school!
    p_boy = random.choice([40, 45, 50, 55, 60])
    p_glass = random.choice([20, 25, 30, 40])
    p_no_glass = 100 - p_glass
    # Fraction of total who are boys without glasses: (p_boy/100) * (p_no_glass/100)
    f_target = Fraction(p_boy * p_no_glass, 10000)
    mult = random.randint(2, 8)
    total_students = f_target.denominator * mult
    boys_no_glass = f_target.numerator * mult
    total_boys = (total_students * p_boy) // 100
    total_girls = total_students - total_boys
    return mcq(
        stem=(
            f"โรงเรียนแห่งหนึ่งมีนักเรียนชายคิดเป็น **{p_boy}%** ของนักเรียนทั้งหมด "
            f"และในกลุ่มนักเรียนชายมีคนที่สวมแว่นตา **{p_glass}%** ของนักเรียนชายทั้งหมด "
            f"ถ้านักเรียนชายที่ **ไม่สวมแว่นตา** มี **{num(boys_no_glass)} คน** โรงเรียนนี้มีนักเรียนทั้งหมดกี่คน"
        ),
        correct=f"{num(total_students)} คน",
        wrongs=[
            W(f"{num(total_boys)} คน", "นี่คือจำนวนนักเรียนชายทั้งหมด ยังไม่ได้คิดย้อนกลับไปเป็นนักเรียนทั้งโรงเรียน", "partial"),
            W(f"{num(total_girls)} คน", "นี่คือจำนวนนักเรียนหญิง ไม่ใช่จำนวนนักเรียนทั้งหมด", "misread"),
            W(f"{num(int(boys_no_glass * 100 / (100 - p_boy - p_glass)) if 100 - p_boy - p_glass > 0 and (boys_no_glass * 100) % (100 - p_boy - p_glass) == 0 else total_students - total_boys // 2)} คน",
              f"นำ {p_boy}% และ {p_glass}% ไปลบออกจาก 100% พร้อมกัน ลืมว่า {p_glass}% คิดจากนักเรียนชายเท่านั้น", "trap"),
        ],
        hint=f"นักเรียนชายที่ไม่สวมแว่นคิดเป็น 100% − {p_glass}% = {p_no_glass}% ของนักเรียนชาย หาจำนวนนักเรียนชายทั้งหมดก่อน แล้วจึงหานักเรียนทั้งโรงเรียน",
        steps=[
            f"นักเรียนชายที่ไม่สวมแว่นคิดเป็น 100% − {p_glass}% = {p_no_glass}% ของนักเรียนชายทั้งหมด",
            f"จาก {p_no_glass}% ของนักเรียนชาย = {num(boys_no_glass)} คน จะได้นักเรียนชายทั้งหมด = {num(boys_no_glass)} × 100 ÷ {p_no_glass} = {num(total_boys)} คน",
            f"นักเรียนชายคิดเป็น {p_boy}% ของทั้งโรงเรียน ดังนั้นมีนักเรียนทั้งหมด = {num(total_boys)} × 100 ÷ {p_boy} = {num(total_students)} คน",
        ],
    )


# ===========================================================================
# Skill 5: m.ratio.pct_change — ร้อยละของการเพิ่มขึ้นและลดลง
# ===========================================================================

skill(
    "m.ratio.pct_change",
    "m.ratio",
    "ร้อยละของการเพิ่มขึ้นและลดลง",
    lesson={
        "concept": (
            "การเพิ่มขึ้นหรือลดลงกี่เปอร์เซ็นต์ ต้องคิดเทียบกับ 'ค่าเดิม (100%)' เสมอ "
            "ถ้าเพิ่มขึ้น p% ค่าใหม่จะคิดเป็น (100 + p)% ของค่าเดิม และถ้าลดลง p% ค่าใหม่จะคิดเป็น (100 − p)% ของค่าเดิม"
        ),
        "steps": [
            "หาเปอร์เซ็นต์การเปลี่ยนแปลง = ((ผลต่างระหว่างค่าใหม่กับค่าเดิม) ÷ ค่าเดิม) × 100%",
            "เมื่อรู้ค่าใหม่หลังเพิ่ม p% แล้วต้องการหาค่าเดิม: ค่าเดิม = ค่าใหม่ × 100 ÷ (100 + p)",
            "สำหรับพื้นที่รูปสี่เหลี่ยมเมื่อด้านเปลี่ยนเป็นเปอร์เซ็นต์: ให้สมมติเดิมกว้าง 10 ยาว 10 (พื้นที่เดิม = 100) แล้วคำนวณพื้นที่ใหม่เทียบกับ 100!",
        ],
        "example": {
            "q": "สี่เหลี่ยมผืนผ้ารูปหนึ่ง เมื่อเพิ่มความยาวขึ้น 20% และลดความกว้างลง 20% พื้นที่ใหม่จะเปลี่ยนไปจากเดิมอย่างไร",
            "steps": [
                "สมมติเดิมกว้าง 10 หน่วย ยาว 10 หน่วย มีพื้นที่เดิม = 10 × 10 = 100 ตารางหน่วย",
                "ยาวขึ้น 20% เป็น 12 หน่วย และกว้างลดลง 20% เหลือ 8 หน่วย",
                "พื้นที่ใหม่ = 12 × 8 = 96 ตารางหน่วย ลดลงจาก 100 อยู่ 4% (ลดลง 4%)",
            ],
            "a": "ลดลง 4%",
        },
        "mistakes": [
            "เมื่อรู้ค่าใหม่หลังจากเพิ่ม 20% แล้ว เผลอเอา 20% ของค่าใหม่ไปลบออก (จริง ๆ ต้องหารด้วย 120 แล้วคูณ 100)",
            "คิดว่าด้านหนึ่งเพิ่ม 20% อีกด้านลด 20% แล้วพื้นที่จะเท่าเดิม (ความจริงพื้นที่ลดลง 4%!)",
        ],
        "tips": [
            "โจทย์เรขาคณิตถามว่าพื้นที่เปลี่ยนไปกี่เปอร์เซ็นต์ ให้สมมติความยาวเดิมเป็น 10 × 10 = 100 เสมอ จะได้คำตอบเป็นเปอร์เซ็นต์ทันทีโดยไม่ต้องตั้งสมการ!",
        ],
    },
    weight=1.6,
)


@template("m.ratio.pct_change", "easy")
def _percent_change_find_pct():
    orig = random.choice([200, 250, 400, 500, 600, 800, 1200, 1500, 2000])
    pct = random.choice([12, 15, 18, 20, 24, 25, 30, 35, 40])
    change = (orig * pct) // 100
    direction = random.choice(["inc", "dec"])
    new_val = orig + change if direction == "inc" else orig - change
    word = "เพิ่มขึ้น" if direction == "inc" else "ลดลง"
    wrong_base_new = round((change / new_val) * 100, 1)
    return mcq(
        stem=(
            f"ราคาสินค้าชนิดหนึ่งเปลี่ยนจาก **{num(orig)} บาท** เป็น **{num(new_val)} บาท** "
            f"ราคาสินค้าชนิดนี้{word}จากเดิมคิดเป็นร้อยละเท่าใด"
        ),
        correct=f"ร้อยละ {pct}",
        wrongs=[
            W(f"ร้อยละ {change}", f"{num(change)} คือจำนวนเงินที่{word}เป็นบาท ยังไม่ได้คิดเทียบเป็นร้อยละของราคาเดิม", "partial"),
            W(f"ร้อยละ {dec(wrong_base_new, 1) if abs(wrong_base_new - pct) > 0.5 else pct + 5}",
              f"นำส่วนต่างไปหารด้วยราคาใหม่ ({num(new_val)}) แทนที่จะหารด้วยราคาเดิม ({num(orig)})", "formula"),
            W(f"ร้อยละ {100 - pct if 100 - pct != pct else pct + 10}",
              "นำค่าร้อยละที่ได้ไปลบออกจาก 100 อีกครั้ง", "concept"),
        ],
        hint=f"หาผลต่างของราคาก่อน ({num(change)} บาท) แล้วหารด้วย 'ราคาเดิม ({num(orig)} บาท)' คูณด้วย 100",
        steps=[
            f"ราคา{word} = {num(abs(new_val - orig))} บาท จากราคาเดิม {num(orig)} บาท",
            f"คิดเป็นร้อยละ = ({num(change)} ÷ {num(orig)}) × 100 = ร้อยละ {pct}",
        ],
    )


@template("m.ratio.pct_change", "medium")
def _reverse_percent_increase():
    pct = random.choice([10, 15, 20, 25, 30, 40, 50])
    orig_hundreds = random.randint(12, 45) * 2
    orig = orig_hundreds * 100
    new_val = (orig * (100 + pct)) // 100
    # Common trap: taking pct% of new_val and subtracting it from new_val!
    trap_val = new_val - (new_val * pct) // 100
    person = name_th()
    return mcq(
        stem=(
            f"ปีนี้{person}ได้รับเงินเดือนเพิ่มขึ้นจากปีที่แล้ว **{pct}%** "
            f"ทำให้ปัจจุบัน{person}ได้รับเงินเดือนเดือนละ **{num(new_val)} บาท** "
            f"อยากทราบว่าปีที่แล้ว{person}มีเงินเดือนกี่บาท"
        ),
        correct=f"{num(orig)} บาท",
        wrongs=[
            W(f"{num(trap_val)} บาท",
              f"นำ {pct}% ไปคิดจากเงินเดือนใหม่ ({num(new_val)} บาท) แล้วลบออก ทั้งที่ {pct}% ต้องคิดจากเงินเดือนปีที่แล้ว (100%)", "trap"),
            W(f"{num(new_val - orig)} บาท", "นี่คือจำนวนเงินเดือนที่เพิ่มขึ้น ไม่ใช่เงินเดือนปีที่แล้ว", "misread"),
            W(f"{num(new_val - pct * 100)} บาท", "หักออกด้วยตัวเลขเปอร์เซ็นต์คูณ 100 โดยไม่ได้เทียบบัญญัติไตรยางศ์กับ 100 + " + str(pct), "concept"),
        ],
        hint=f"ให้เงินเดือนปีที่แล้วเป็น 100% ดังนั้นเงินเดือนปีนี้คิดเป็น 100% + {pct}% = {100 + pct}% ของปีที่แล้ว",
        steps=[
            f"เงินเดือนปีนี้เพิ่มขึ้น {pct}% จึงคิดเป็น 100 + {pct} = {100 + pct}% ของเงินเดือนปีที่แล้ว",
            f"จะได้ {100 + pct}% คิดเป็นเงิน {num(new_val)} บาท",
            f"ดังนั้นปีที่แล้วมีเงินเดือน (100%) = {num(new_val)} × 100 ÷ {100 + pct} = {num(orig)} บาท",
        ],
    )


@template("m.ratio.pct_change", "challenge")
def _rectangle_area_percent_change():
    # Classic top-school challenge: length changes by a%, width changes by b% -> net % change in area
    a = random.choice([10, 20, 30, 40, 50])
    b = random.choice([-40, -30, -20, -10, 10, 20, 30, 40])
    new_area = ((100 + a) * (100 + b)) // 100
    diff = new_area - 100
    if diff > 0:
        ans = f"เพิ่มขึ้น {diff}%"
        opp = f"ลดลง {diff}%"
    elif diff < 0:
        ans = f"ลดลง {abs(diff)}%"
        opp = f"เพิ่มขึ้น {abs(diff)}%"
    else:
        ans = "เท่าเดิม (ไม่เปลี่ยนแปลง)"
        opp = f"ลดลง {max(1, (a * abs(b)) // 100)}%"

    naive_sum = a + b
    if naive_sum == 0:
        naive_str = "เท่าเดิม (ไม่เปลี่ยนแปลง)"
    elif naive_sum > 0:
        naive_str = f"เพิ่มขึ้น {naive_sum}%"
    else:
        naive_str = f"ลดลง {abs(naive_sum)}%"

    w_extra = f"เพิ่มขึ้น {abs(diff) + 2}%" if diff < 0 else f"ลดลง {abs(diff) + 2}%"
    w_calc = f"{'ลดลง' if diff < 0 else 'เพิ่มขึ้น'} {abs(diff) + 5}%"
    if w_calc in (ans, naive_str, opp, w_extra):
        w_calc = f"{'ลดลง' if diff < 0 else 'เพิ่มขึ้น'} {abs(diff) + 7}%"
    b_word = f"เพิ่มขึ้น {b}%" if b > 0 else f"ลดลง {abs(b)}%"
    shape_noun = pick([
        "รูปสี่เหลี่ยมผืนผ้ารูปหนึ่ง",
        "สนามหญ้ารูปสี่เหลี่ยมผืนผ้า",
        "แผ่นป้ายรูปสี่เหลี่ยมผืนผ้า",
        "แปลงผักรูปสี่เหลี่ยมผืนผ้า",
        "กระจกเงารูปสี่เหลี่ยมผืนผ้า",
        "สระว่ายน้ำรูปสี่เหลี่ยมผืนผ้า",
    ])
    return mcq(
        stem=(
            f"{shape_noun} ถ้าเพิ่มความยาวขึ้น **{a}%** และปรับความกว้างให้ **{b_word}** "
            f"พื้นที่ใหม่จะเปลี่ยนแปลงไปจากพื้นที่เดิมอย่างไร"
        ),
        correct=ans,
        wrongs=[
            W(naive_str if naive_str != ans else w_extra,
              f"นำเปอร์เซ็นต์ทั้งสองด้านมาบวกลบกันโดยตรง ({a}% กับ {b}%) โดยลืมว่าพื้นที่เกิดจาก กว้าง × ยาว", "trap"),
            W(opp, "คำนวณขนาดการเปลี่ยนแปลงถูกแล้ว แต่สรุปทิศทางเพิ่มขึ้น/ลดลงสลับกัน", "sign"),
            W(w_calc, "คำนวณผลคูณของด้านใหม่ผิดพลาด", "calc"),
        ],
        hint="สมมติให้เดิมกว้าง 10 หน่วย ยาว 10 หน่วย (พื้นที่เดิม = 100 ตารางหน่วย) แล้วคำนวณความกว้างและความยาวใหม่มาคูณกัน",
        steps=[
            "สมมติเดิมยาว 10 หน่วย กว้าง 10 หน่วย จะมีพื้นที่เดิม = 10 × 10 = 100 ตารางหน่วย",
            f"ความยาวใหม่เพิ่มขึ้น {a}% เป็น {dec(10 * (100 + a) / 100, 2)} หน่วย และความกว้างใหม่ ({b_word}) เป็น {dec(10 * (100 + b) / 100, 2)} หน่วย",
            f"พื้นที่ใหม่ = {dec(10 * (100 + a) / 100, 2)} × {dec(10 * (100 + b) / 100, 2)} = {new_area} ตารางหน่วย",
            f"เทียบกับพื้นที่เดิม 100 ตารางหน่วย พบว่าพื้นที่ {ans}",
        ],
    )


# ===========================================================================
# Skill 6: m.ratio.discount — การลดราคาและการลดราคาสองต่อ
# ===========================================================================

skill(
    "m.ratio.discount",
    "m.ratio",
    "การลดราคาและการลดราคาต่อเนื่อง",
    lesson={
        "concept": (
            "การลดราคา d% คิดจาก 'ราคาป้าย (100%)' ทำให้ราคาขายจริงคิดเป็น (100 − d)% ของราคาป้าย "
            "และหากมีการลดราคาสองต่อ (เช่น ลด a% แล้วลดเพิ่มอีก b%) ครั้งที่สองต้องคิดลดจากราคาที่ลดแล้วในครั้งแรก ไม่ใช่นำ (a + b)% ไปลดรวดเดียว!"
        ),
        "steps": [
            "รู้ราคาป้าย P ลด d%: ราคาขายจริง = P × (100 − d) ÷ 100",
            "รู้ราคาขายจริง S หลังลด d%: ราคาป้าย = S × 100 ÷ (100 − d)",
            "ลดสองต่อ (ลด a% แล้วลดเพิ่มอีก b%): ราคาสุทธิ = ราคาป้าย × [[100−a/100]] × [[100−b/100]]",
        ],
        "example": {
            "q": "รองเท้าติดป้ายราคา 2,000 บาท ร้านค้าลดราคา 20% และถ้าเป็นสมาชิกลดเพิ่มอีก 10% จากราคาที่ลดแล้ว สมาชิกต้องจ่ายเงินกี่บาท",
            "steps": [
                "ลดครั้งแรก 20% เหลือราคา = 2,000 × (80 ÷ 100) = 1,600 บาท",
                "สมาชิกลดเพิ่มอีก 10% ของ 1,600 บาท เหลือจ่ายจริง = 1,600 × (90 ÷ 100) = 1,440 บาท",
            ],
            "a": "1,440 บาท",
        },
        "mistakes": [
            "เห็นป้ายลด 20% แล้วลดเพิ่มอีก 10% เผลอรวมเป็นลด 30% (ความจริงลด 100% − (80% × 90%) = 28% เท่านั้น)",
            "ตอนหาราคาป้ายย้อนกลับจากราคาขาย เผลอนำเปอร์เซ็นต์ส่วนลดไปคูณราคาขายแล้วบวกกลับ",
        ],
        "tips": [
            "ลด a% ตามด้วยลด b% คิดเป็นราคาจ่ายจริง = (100 − a)% × (100 − b)% ของราคาป้ายเสมอ",
        ],
    },
    weight=1.6,
)


@template("m.ratio.discount", "easy")
def _discount_basic():
    marked = random.choice([450, 600, 750, 800, 900, 1200, 1500, 1800, 2400, 2500])
    disc_pct = random.choice([10, 15, 20, 25, 30, 40])
    disc_amt = (marked * disc_pct) // 100
    sell_price = marked - disc_amt
    item = pick(["กระเป๋านักเรียน", "รองเท้ากีฬา", "นาฬิกาข้อมือ", "เสื้อกันหนาว", "โคมไฟอ่านหนังสือ"])
    return mcq(
        stem=f"{item}ติดป้ายราคาไว้ **{num(marked)} บาท** ร้านค้าลดราคาให้ **{disc_pct}%** ผู้ซื้อต้องจ่ายเงินกี่บาท",
        correct=f"{num(sell_price)} บาท",
        wrongs=[
            W(f"{num(disc_amt)} บาท", f"{num(disc_amt)} บาท คือจำนวนเงินส่วนลด ไม่ใช่ราคาที่ต้องจ่ายจริง", "partial"),
            W(f"{num(marked - disc_pct)} บาท", f"นำตัวเลขเปอร์เซ็นต์ ({disc_pct}) ไปลบออกจากราคาป้ายโดยตรง", "concept"),
            W(f"{num(marked + disc_amt)} บาท", "นำส่วนลดไปบวกเพิ่มกับราคาป้ายแทนที่จะนำมาลบออก", "sign"),
        ],
        hint=f"ลดราคา {disc_pct}% แปลว่าจ่ายเงินจริง 100% − {disc_pct}% = {100 - disc_pct}% ของราคาป้าย",
        steps=[
            f"ลดราคา {disc_pct}% คิดเป็นส่วนลด = ({disc_pct} ÷ 100) × {num(marked)} = {num(disc_amt)} บาท",
            f"ผู้ซื้อต้องจ่ายเงิน = {num(marked)} − {num(disc_amt)} = {num(sell_price)} บาท",
        ],
    )


@template("m.ratio.discount", "medium")
def _reverse_discount_marked_price():
    disc_pct = random.choice([12, 15, 20, 25, 30, 35])
    pay_pct = 100 - disc_pct
    marked = random.randint(8, 35) * 100
    sell_price = (marked * pay_pct) // 100
    disc_amt = marked - sell_price
    trap_add_pct = sell_price + (sell_price * disc_pct) // 100
    item = pick(["จักรยาน", "เครื่องคิดเลขวิทยาศาสตร์", "ชุดเครื่องเขียน", "พจนานุกรม", "เตารีดไอน้ำ"])
    return mcq(
        stem=(
            f"ร้านค้าลดราคา{item} **{disc_pct}%** จากราคาป้าย "
            f"ทำให้ลูกค้าซื้อได้ในราคา **{num(sell_price)} บาท** "
            f"เดิมร้านค้าติดป้ายราคา{item}ไว้กี่บาท"
        ),
        correct=f"{num(marked)} บาท",
        wrongs=[
            W(f"{num(trap_add_pct if trap_add_pct != marked else marked - 50)} บาท",
              f"นำ {disc_pct}% ไปคิดจากราคาที่ลดแล้ว ({num(sell_price)} บาท) แล้วบวกกลับ ทั้งที่ {disc_pct}% ต้องคิดจากราคาป้าย (100%)", "trap"),
            W(f"{num(disc_amt)} บาท", "นี่คือจำนวนเงินที่ลดให้ลูกค้า ไม่ใช่ราคาป้ายเต็ม", "misread"),
            W(f"{num(sell_price + disc_pct * 10)} บาท", "บวกเพิ่มด้วยตัวเลขเปอร์เซ็นต์คูณ 10 แทนการเทียบบัญญัติไตรยางศ์", "concept"),
        ],
        hint=f"ลดราคา {disc_pct}% แสดงว่าราคาที่ลูกค้าจ่าย ({num(sell_price)} บาท) คิดเป็น {pay_pct}% ของราคาป้าย",
        steps=[
            f"เมื่อลดราคา {disc_pct}% ราคาขายจริงจะคิดเป็น 100 − {disc_pct} = {pay_pct}% ของราคาป้าย",
            f"จะได้ {pay_pct}% ของราคาป้าย = {num(sell_price)} บาท",
            f"ดังนั้นราคาป้าย (100%) = {num(sell_price)} × 100 ÷ {pay_pct} = {num(marked)} บาท",
        ],
    )


@template("m.ratio.discount", "hard")
def _successive_discounts_trap():
    # Classic top-school trap: discount d1% then extra d2% off discounted price
    d1, d2 = pick([
        (20, 10), (30, 10), (20, 20), (25, 20), (40, 10), (50, 20), (10, 10), (20, 15), (30, 20)
    ])
    marked = random.choice([1000, 1500, 2000, 2500, 3000, 4000, 5000])
    after1 = (marked * (100 - d1)) // 100
    final_price = (after1 * (100 - d2)) // 100
    naive_price = (marked * (100 - d1 - d2)) // 100
    total_disc_amt = marked - final_price
    return mcq(
        stem=(
            f"ห้างสรรพสินค้าติดป้ายราคาสินค้าชิ้นหนึ่งไว้ **{num(marked)} บาท** "
            f"ช่วงโปรโมชันลดราคา **{d1}%** และถ้าชำระด้วยเงินสดจะลดเพิ่มอีก **{d2}% ของราคาที่ลดแล้ว** "
            f"ถ้าลูกค้าชำระด้วยเงินสดจะต้องจ่ายเงินกี่บาท"
        ),
        correct=f"{num(final_price)} บาท",
        wrongs=[
            W(f"{num(naive_price)} บาท",
              f"นำเปอร์เซ็นต์ส่วนลดมาบวกกันเป็น {d1}+{d2} = {d1 + d2}% แล้วคิดจากราคาป้ายทีเดียว (จริง ๆ ครั้งที่สองคิดจากราคาที่ลดแล้ว)", "trap"),
            W(f"{num(after1)} บาท", f"คิดเฉพาะส่วนลดครั้งแรก ({d1}%) ลืมลดเพิ่มอีก {d2}% สำหรับเงินสด", "partial"),
            W(f"{num(total_disc_amt)} บาท", "นี่คือจำนวนเงินส่วนลดรวมทั้งหมด โจทย์ถามจำนวนเงินที่ต้องจ่ายจริง", "misread"),
        ],
        hint=f"คิดทีละขั้น: ขั้นแรกลด {d1}% เหลือกี่บาท แล้วจึงนำราคาที่เหลือนั้นมาหักออกอีก {d2}%",
        steps=[
            f"ลดราคาครั้งแรก {d1}% เหลือราคา = {num(marked)} × ({100 - d1} ÷ 100) = {num(after1)} บาท",
            f"ชำระเงินสดลดเพิ่มอีก {d2}% ของราคาที่ลดแล้ว จึงต้องจ่ายจริง = {num(after1)} × ({100 - d2} ÷ 100) = {num(final_price)} บาท",
        ],
    )


# ===========================================================================
# Skill 7: m.ratio.profit — กำไร ขาดทุน ราคาทุน และการตั้งราคาป้าย
# ===========================================================================

skill(
    "m.ratio.profit",
    "m.ratio",
    "กำไร ขาดทุน และการตั้งราคาป้าย",
    lesson={
        "concept": (
            "กำไรและขาดทุนคิดเป็นร้อยละเทียบกับ 'ราคาทุน (100%)' เสมอ "
            "ได้กำไร p% แปลว่า ราคาขาย = (100 + p)% ของทุน · ขาดทุน p% แปลว่า ราคาขาย = (100 − p)% ของทุน "
            "ส่วนการลดราคา d% จะคิดเทียบจาก 'ราคาป้าย'"
        ),
        "steps": [
            "ถ้ารู้ราคาขายและรู้ว่ากำไร/ขาดทุนกี่เปอร์เซ็นต์ ให้เทียบบัญญัติไตรยางศ์กับ (100 ± p)% เพื่อหาทุน (100%) ก่อน",
            "โจทย์เปลี่ยนเป้าหมาย (ขาย S1 ขาดทุน a% ถ้าอยากได้กำไร b% ต้องขายเท่าไร): ใช้สัดส่วน S2 = S1 × (100 + b) ÷ (100 − a)",
            "โจทย์ตั้งราคาป้าย P เพื่อให้ลด d% แล้วยังได้กำไร p% ของทุน C: ใช้สมการ ราคาขายจริงเท่ากัน คือ P × (100 − d)% = C × (100 + p)%",
        ],
        "example": {
            "q": "พ่อค้าซื้อเสื้อมาตัวละ 400 บาท ต้องติดป้ายราคาไว้กี่บาท เมื่อลดให้ลูกค้า 20% จากราคาป้ายแล้วยังได้กำไร 10%",
            "steps": [
                "ต้องการกำไร 10% จากทุน 400 บาท ดังนั้นราคาขายจริงต้องได้ = 400 × (110 ÷ 100) = 440 บาท",
                "ราคาขายจริง 440 บาท เกิดจากการลดราคาป้าย 20% (คิดเป็น 80% ของราคาป้าย)",
                "ดังนั้นต้องติดป้ายราคา = 440 × 100 ÷ 80 = 550 บาท",
            ],
            "a": "550 บาท",
        },
        "mistakes": [
            "โจทย์ต้องการกำไร 10% เมื่อลดราคา 20% เผลอคิดบวกเพิ่ม 30% จากทุนเป็น 400 × 1.3 = 520 บาท (ซึ่งพอลด 20% จะเหลือแค่ 416 บาท กำไรไม่ถึง 10%!)",
            "คิดเปอร์เซ็นต์กำไรเทียบกับราคาขาย แทนที่จะเทียบกับราคาทุน",
        ],
        "tips": [
            "จำสมการทองของเรื่องการค้า: ราคาป้าย × (100 − %ลด) = ราคาทุน × (100 + %กำไร) แทนค่าปุ๊บออกปั๊บ!",
        ],
    },
    weight=2.0,
)


@template("m.ratio.profit", "easy")
def _profit_loss_basic():
    cost = random.choice([300, 400, 500, 600, 800, 1200, 1500, 2000])
    pct = random.choice([12, 15, 20, 25, 30, 35])
    diff_amt = (cost * pct) // 100
    is_profit = random.choice([True, False])
    sell = cost + diff_amt if is_profit else cost - diff_amt
    word = "ได้กำไร" if is_profit else "ขาดทุน"
    return mcq(
        stem=(
            f"แม่ค้าลงทุนซื้อผลไม้มาเป็นเงิน **{num(cost)} บาท** นำไปขายทั้งหมดในราคา **{num(sell)} บาท** "
            f"แม่ค้าขายผลไม้{word}ร้อยละเท่าใด"
        ),
        correct=f"{word}ร้อยละ {pct}",
        wrongs=[
            W(f"{'ขาดทุน' if is_profit else 'ได้กำไร'}ร้อยละ {pct}",
              "สรุปผลกำไร/ขาดทุนสลับกัน (ราคาขายมากกว่าทุนคือกำไร ราคาขายน้อยกว่าทุนคือขาดทุน)", "misread"),
            W(f"{word}ร้อยละ {diff_amt}", f"{num(diff_amt)} คือจำนวนเงินเป็นบาท ยังไม่ได้คิดเทียบเป็นร้อยละของทุน", "partial"),
            W(f"{word}ร้อยละ {round(diff_amt * 100 / sell) if round(diff_amt * 100 / sell) != pct else pct + 4}",
              f"นำกำไร/ขาดทุนไปหารด้วยราคาขาย ({num(sell)}) แทนที่จะหารด้วยราคาทุน ({num(cost)})", "formula"),
        ],
        hint="หาผลต่างระหว่างราคาขายกับราคาทุน แล้วนำมาหารด้วย 'ราคาทุน' คูณ 100",
        steps=[
            f"ขายราคา {num(sell)} บาท จากทุน {num(cost)} บาท จึง{word} = {num(diff_amt)} บาท",
            f"คิดเป็นร้อยละ = ({num(diff_amt)} ÷ {num(cost)}) × 100 = ร้อยละ {pct}",
        ],
    )


@template("m.ratio.profit", "medium")
def _loss_to_target_profit():
    # Sold at S1 with a% loss. To make b% profit, what price S2 should it be sold at?
    loss_pct = random.choice([10, 15, 20, 25])
    prof_pct = random.choice([10, 15, 20, 25, 30])
    cost = random.randint(6, 25) * 100
    s1 = (cost * (100 - loss_pct)) // 100
    s2 = (cost * (100 + prof_pct)) // 100
    wrong_on_s1 = s1 + (s1 * (loss_pct + prof_pct)) // 100
    return mcq(
        stem=(
            f"ขายนาฬิกาเรือนหนึ่งไปในราคา **{num(s1)} บาท** ปรากฏว่า **ขาดทุน {loss_pct}%** "
            f"ถ้าต้องการขายให้ได้ **กำไร {prof_pct}%** จะต้องขายนาฬิกาเรือนนี้ในราคากี่บาท"
        ),
        correct=f"{num(s2)} บาท",
        wrongs=[
            W(f"{num(cost)} บาท", f"{num(cost)} บาท คือราคาทุน (เท่าทุน) ยังไม่ได้บวกกำไร {prof_pct}%", "partial"),
            W(f"{num(wrong_on_s1 if wrong_on_s1 != s2 else s2 - 40)} บาท",
              f"นำ {loss_pct + prof_pct}% ไปคิดจากราคาขายเดิม ({num(s1)} บาท) แทนที่จะหาทุน (100%) ก่อน", "trap"),
            W(f"{num(s1 + (cost * prof_pct) // 100)} บาท",
              f"นำกำไร {prof_pct}% ของทุนไปบวกต่อจากราคาที่ขาดทุน ({num(s1)} บาท) แทนที่จะบวกกับราคาทุน", "concept"),
        ],
        hint=f"ราคาขาย {num(s1)} บาท คิดเป็น {100 - loss_pct}% ของทุน ให้หาทุนก่อน หรือเทียบไปที่ {100 + prof_pct}% ของทุน",
        steps=[
            f"ขายขาดทุน {loss_pct}% แสดงว่าราคา {num(s1)} บาท คิดเป็น 100 − {loss_pct} = {100 - loss_pct}% ของทุน",
            f"ราคาทุน (100%) = {num(s1)} × 100 ÷ {100 - loss_pct} = {num(cost)} บาท",
            f"ต้องการกำไร {prof_pct}% ต้องขายในราคา ({100 + prof_pct}% ของทุน) = {num(cost)} × {100 + prof_pct} ÷ 100 = {num(s2)} บาท",
        ],
    )


@template("m.ratio.profit", "challenge")
def _marked_price_discount_and_profit():
    # Classic top-school: Cost C, want to allow discount d% off marked price M and still make profit p% on cost!
    # M * (100 - d) = C * (100 + p)
    configs = [
        (20, 10, 400),
        (20, 20, 500),
        (20, 24, 500),
        (25, 20, 450),
        (10, 20, 600),
        (10, 17, 500),
        (20, 16, 600),
        (25, 15, 600),
        (30, 5, 800),
    ]
    disc_pct, prof_pct, base_c = pick(configs)
    mult = random.randint(1, 5)
    cost = base_c * mult
    sell_price = (cost * (100 + prof_pct)) // 100
    marked_price = (sell_price * 100) // (100 - disc_pct)
    # Trap: adding (disc_pct + prof_pct)% directly to cost!
    naive_marked = (cost * (100 + disc_pct + prof_pct)) // 100
    return mcq(
        stem=(
            f"ร้านค้าซื้อสินค้าชิ้นหนึ่งมาในราคาทุน **{num(cost)} บาท** "
            f"จะต้อง **ติดป้ายราคา** สินค้าชิ้นนี้ไว้กี่บาท เพื่อว่าเมื่อลดราคาให้ลูกค้า **{disc_pct}%** จากราคาป้ายแล้ว "
            f"ร้านค้ายังคงได้ **กำไร {prof_pct}%** จากราคาทุน"
        ),
        correct=f"{num(marked_price)} บาท",
        wrongs=[
            W(f"{num(naive_marked if naive_marked != marked_price else marked_price - 30)} บาท",
              f"นำ {disc_pct}% + {prof_pct}% = {disc_pct + prof_pct}% ไปคิดบวกเพิ่มจากทุนเลย (ลืมว่าส่วนลด {disc_pct}% คิดจากราคาป้าย ไม่ใช่คิดจากทุน)", "trap"),
            W(f"{num(sell_price)} บาท",
              f"{num(sell_price)} บาท คือราคาขายจริงที่ได้กำไร {prof_pct}% ยังไม่ได้เผื่อส่วนลด {disc_pct}% สำหรับตั้งราคาป้าย", "partial"),
            W(f"{num((cost * 100) // (100 - disc_pct))} บาท",
              f"ตั้งราคาป้ายเผื่อส่วนลด {disc_pct}% อย่างเดียว (ขายเท่าทุน) ลืมบวกกำไร {prof_pct}%", "partial"),
        ],
        hint=f"หาราคาขายจริงที่ต้องการก่อน (ทุน + กำไร {prof_pct}%) ซึ่งราคาขายจริงนี้จะเท่ากับ {100 - disc_pct}% ของราคาป้าย",
        steps=[
            f"ต้องการกำไร {prof_pct}% จากทุน {num(cost)} บาท ดังนั้นต้องขายจริงในราคา = {num(cost)} × ({100 + prof_pct} ÷ 100) = {num(sell_price)} บาท",
            f"เนื่องจากลดจากป้าย {disc_pct}% แสดงว่าราคาขายจริง {num(sell_price)} บาท คิดเป็น {100 - disc_pct}% ของราคาป้าย",
            f"ดังนั้นต้องติดป้ายราคา = {num(sell_price)} × 100 ÷ {100 - disc_pct} = {num(marked_price)} บาท",
        ],
    )


# ===========================================================================
# Skill 8: m.ratio.interest_vat — ดอกเบี้ยเชิงเดียวและภาษีมูลค่าเพิ่ม
# ===========================================================================

skill(
    "m.ratio.interest_vat",
    "m.ratio",
    "ดอกเบี้ยเชิงเดียวและภาษีมูลค่าเพิ่ม",
    lesson={
        "concept": (
            "ดอกเบี้ยเชิงเดียวคำนวณจากสูตร ดอกเบี้ย (I) = เงินต้น (P) × อัตราดอกเบี้ยต่อปี (r/100) × เวลาเป็นปี (t) "
            "ถ้าเวลาเป็นเดือนให้หารด้วย 12 (เช่น 8 เดือน = [[8/12]] ปี) ส่วนเงินรวม = เงินต้น + ดอกเบี้ย"
        ),
        "steps": [
            "แปลงระยะเวลาฝากให้เป็นหน่วย 'ปี' เสมอ (จำนวนเดือน ÷ 12 หรือ จำนวนวัน ÷ 365)",
            "คำนวณดอกเบี้ย I = P × (r / 100) × t แล้วดูว่าโจทย์ถาม 'ดอกเบี้ย' หรือ 'เงินรวมทั้งหมด (P + I)'",
            "สำหรับภาษีมูลค่าเพิ่ม (VAT 7%): ราคารวมภาษี = ราคาสินค้า × [[107/100]] (ถ้าถอดภาษีย้อนกลับ ให้หารด้วย 107 แล้วคูณ 100)",
        ],
        "example": {
            "q": "ฝากเงิน 12,000 บาท ธนาคารคิดอัตราดอกเบี้ยร้อยละ 3 ต่อปี เมื่อฝากครบ 8 เดือน จะได้ดอกเบี้ยกี่บาท",
            "steps": [
                "เวลา 8 เดือน คิดเป็น [[8/12]] = [[2/3]] ปี",
                "ดอกเบี้ย = 12,000 × (3 ÷ 100) × (8 ÷ 12) = 240 บาท",
            ],
            "a": "240 บาท",
        },
        "mistakes": [
            "ฝากเงินเป็นเดือน (เช่น 8 เดือน) แต่แทนค่า t = 8 ลงในสูตรเหมือนฝาก 8 ปี โดยลืมหารด้วย 12",
            "โจทย์ถามเงินรวมเมื่อปิดบัญชี แต่ตอบเฉพาะดอกเบี้ย (ลืมบวกเงินต้น)",
        ],
        "tips": [
            "ถอด VAT 7% ย้อนกลับ: ถ้าราคารวม VAT 7% คือ X บาท ราคาสินค้าก่อนภาษีคือ (X ÷ 107) × 100 ไม่ใช่เอา 7% ของ X มาลบออก!",
        ],
    },
    weight=1.3,
)


@template("m.ratio.interest_vat", "easy")
def _simple_interest_years():
    principal = random.choice([5000, 8000, 10000, 12000, 15000, 20000, 25000, 30000])
    rate = random.choice([2, 3, 4, 5])
    years = random.choice([2, 3, 4])
    interest = (principal * rate * years) // 100
    total = principal + interest
    one_yr_interest = (principal * rate) // 100
    person = name_th()
    return mcq(
        stem=(
            f"{person}ฝากเงินกับธนาคาร **{num(principal)} บาท** ได้รับอัตราดอกเบี้ยเชิงเดียว **ร้อยละ {rate} ต่อปี** "
            f"เมื่อฝากครบ **{years} ปี** (โดยไม่ถอนเงินเลย) {person}จะมี **เงินรวมทั้งหมด** ในบัญชีกี่บาท"
        ),
        correct=f"{num(total)} บาท",
        wrongs=[
            W(f"{num(interest)} บาท", f"{num(interest)} บาท คือดอกเบี้ยอย่างเดียว โจทย์ถามเงินรวมทั้งหมด (ต้องบวกเงินต้นด้วย)", "misread"),
            W(f"{num(principal + one_yr_interest)} บาท", f"คิดดอกเบี้ยเพียง 1 ปี ลืมคูณจำนวนปี ({years} ปี)", "partial"),
            W(f"{num(principal + rate * years * 10)} บาท", "คำนวณดอกเบี้ยผิดหลักหน่วยร้อยละ", "calc"),
        ],
        hint="หาดอกเบี้ยจาก เงินต้น × (อัตราดอกเบี้ย ÷ 100) × จำนวนปี แล้วนำมาบวกกับเงินต้น",
        steps=[
            f"ดอกเบี้ย {years} ปี = {num(principal)} × ({rate} ÷ 100) × {years} = {num(interest)} บาท",
            f"เงินรวมทั้งหมด = เงินต้น + ดอกเบี้ย = {num(principal)} + {num(interest)} = {num(total)} บาท",
        ],
    )


@template("m.ratio.interest_vat", "medium")
def _simple_interest_months():
    months = random.choice([3, 4, 6, 8, 9, 10])
    rate = random.choice([3, 4, 6])
    principal = random.randint(2, 12) * 6000
    interest = (principal * rate * months) // (100 * 12)
    wrong_as_years = (principal * rate * months) // 100
    wrong_one_yr = (principal * rate) // 100
    return mcq(
        stem=(
            f"ฝากเงินธนาคาร **{num(principal)} บาท** อัตราดอกเบี้ย **ร้อยละ {rate} ต่อปี** "
            f"เมื่อฝากครบ **{months} เดือน** จะได้รับดอกเบี้ยกี่บาท"
        ),
        correct=f"{num(interest)} บาท",
        wrongs=[
            W(f"{num(wrong_as_years)} บาท", f"แทนเวลาเป็น {months} ปีโดยลืมหารด้วย 12 เดือนต่อปี", "unit"),
            W(f"{num(wrong_one_yr)} บาท", "นี่คือดอกเบี้ยเต็ม 1 ปี (12 เดือน) ยังไม่ได้คิดตามสัดส่วนจำนวนเดือนที่ฝาก", "partial"),
            W(f"{num(principal + interest)} บาท", "นี่คือเงินต้นรวมดอกเบี้ย โจทย์ถามเฉพาะดอกเบี้ย", "misread"),
        ],
        hint=f"เวลา {months} เดือน คิดเป็น [[{months}/12]] ปี แทนลงในสูตร ดอกเบี้ย = เงินต้น × (อัตรา ÷ 100) × เวลาเป็นปี",
        steps=[
            f"แปลงเวลา {months} เดือนเป็นปี ได้ [[{months}/12]] ปี",
            f"ดอกเบี้ย = {num(principal)} × ({rate} ÷ 100) × ({months} ÷ 12) = {num(interest)} บาท",
        ],
    )


@template("m.ratio.interest_vat", "hard")
def _vat_or_service_charge_reverse():
    mode = random.choice(["reverse_vat", "service_plus_vat"])
    if mode == "reverse_vat":
        # Price including 7% VAT is 107 * k. Find price before VAT or VAT amount!
        k = random.randint(12, 85) * 10
        pre_vat = k * 100
        vat_amt = k * 7
        total_inc = k * 107
        ask = random.choice(["pre", "vat"])
        if ask == "pre":
            trap = round(total_inc * 0.93)
            return mcq(
                stem=(
                    f"คุณแม่ซื้อเครื่องใช้ไฟฟ้าชิ้นหนึ่ง จ่ายเงินไปทั้งหมด **{num(total_inc)} บาท** "
                    f"ซึ่งราคานี้ **รวมภาษีมูลค่าเพิ่ม (VAT) 7%** เรียบร้อยแล้ว "
                    f"อยากทราบว่าราคาเครื่องใช้ไฟฟ้า **ก่อนรวมภาษีมูลค่าเพิ่ม** เป็นกี่บาท"
                ),
                correct=f"{num(pre_vat)} บาท",
                wrongs=[
                    W(f"{num(trap)} บาท",
                      f"นำ 7% ไปคิดจากราคารวมภาษี ({num(total_inc)} บาท) แล้วลบออก ทั้งที่ 7% คิดจากราคาก่อนภาษี (100%)", "trap"),
                    W(f"{num(vat_amt)} บาท", f"{num(vat_amt)} บาท คือค่าภาษีมูลค่าเพิ่ม 7% ไม่ใช่ราคาสินค้าก่อนรวมภาษี", "misread"),
                    W(f"{num(total_inc - 700)} บาท", "ลบออกด้วย 700 บาทโดยไม่ได้เทียบบัญญัติไตรยางศ์กับ 107%", "concept"),
                ],
                hint=f"ราคารวมภาษี {num(total_inc)} บาท คิดเป็น 100% + 7% = 107% ของราคาก่อนรวมภาษี",
                steps=[
                    "ให้ราคาสินค้าก่อนรวมภาษีเป็น 100% เมื่อรวมภาษี 7% จึงคิดเป็น 107%",
                    f"จะได้ 107% = {num(total_inc)} บาท",
                    f"ดังนั้นราคาก่อนรวมภาษี (100%) = ({num(total_inc)} ÷ 107) × 100 = {num(pre_vat)} บาท",
                ],
            )
        else:
            trap_vat = round(total_inc * 0.07)
            return mcq(
                stem=(
                    f"ใบเสร็จรับเงินแสดงราคาสินค้าที่ **รวมภาษีมูลค่าเพิ่ม 7% แล้ว** เป็นเงิน **{num(total_inc)} บาท** "
                    f"ในการซื้อครั้งนี้เป็น **ค่าภาษีมูลค่าเพิ่ม** กี่บาท"
                ),
                correct=f"{num(vat_amt)} บาท",
                wrongs=[
                    W(f"{num(trap_vat if trap_vat != vat_amt else vat_amt + 14)} บาท",
                      f"นำ 7% ไปคูณกับราคารวมภาษี ({num(total_inc)} บาท) โดยตรง แทนที่จะเทียบจาก 107 ส่วน", "trap"),
                    W(f"{num(pre_vat)} บาท", f"{num(pre_vat)} บาท คือราคาสินค้าก่อนรวมภาษี โจทย์ถามเฉพาะค่าภาษีมูลค่าเพิ่ม", "misread"),
                    W(f"{num(vat_amt * 2)} บาท", "คำนวณอัตราส่วน 7 ใน 107 คลาดเคลื่อน", "calc"),
                ],
                hint=f"ราคารวมภาษี {num(total_inc)} บาท คือ 107 ส่วน โดยที่เป็นค่าภาษีอยู่ 7 ส่วน",
                steps=[
                    f"ราคารวมภาษี 7% คิดเป็น 107% ของราคาสินค้า เท่ากับ {num(total_inc)} บาท",
                    f"ดังนั้นค่าภาษี 7% = ({num(total_inc)} ÷ 107) × 7 = {num(vat_amt)} บาท",
                ],
            )
    else:
        # Restaurant bill: food price F, discount disc_pct%, then service charge 10% on discounted food
        food = random.choice([1000, 1200, 1500, 2000, 2500, 3000, 3500, 4000])
        svc_pct = 10
        disc_pct = random.choice([15, 20, 25, 30])
        after_disc = (food * (100 - disc_pct)) // 100
        total_pay = (after_disc * (100 + svc_pct)) // 100
        naive_net = (food * (100 - disc_pct + svc_pct)) // 100
        wrong_sub_svc = (after_disc * (100 - svc_pct)) // 100
        return mcq(
            stem=(
                f"รับประทานอาหารที่ร้านแห่งหนึ่ง ค่าอาหารตามเมนูเป็นเงิน **{num(food)} บาท** "
                f"ใช้บัตรสมาชิกลดค่าอาหารได้ **{disc_pct}%** จากนั้นทางร้านคิดค่าบริการ (Service Charge) เพิ่มอีก **{svc_pct}%** ของค่าอาหารหลังหักส่วนลด "
                f"จะต้องจ่ายเงินทั้งหมดกี่บาท"
            ),
            correct=f"{num(total_pay)} บาท",
            wrongs=[
                W(f"{num(naive_net)} บาท",
                  f"นำส่วนลด {disc_pct}% กับค่าบริการ {svc_pct}% มาหักลบกันเป็นเปอร์เซ็นต์เดียวโดยไม่คิดเป็นลำดับขั้น", "trap"),
                W(f"{num(after_disc)} บาท", f"คิดเฉพาะค่าอาหารหลังลด {disc_pct}% ลืมบวกค่าบริการ {svc_pct}%", "partial"),
                W(f"{num(wrong_sub_svc)} บาท",
                  f"นำค่าบริการ {svc_pct}% ไปหักลดเพิ่มแทนที่จะบวกเพิ่ม", "sign"),
            ],
            hint=f"หาค่าอาหารหลังลด {disc_pct}% ก่อน แล้วจึงบวกเพิ่มอีก {svc_pct}% ของยอดนั้น",
            steps=[
                f"ค่าอาหารหลังหักส่วนลด {disc_pct}% = {num(food)} × ({100 - disc_pct} ÷ 100) = {num(after_disc)} บาท",
                f"บวกค่าบริการเพิ่ม {svc_pct}% = {num(after_disc)} × ({100 + svc_pct} ÷ 100) = {num(total_pay)} บาท",
            ],
        )


# ===========================================================================
# Skill 9: m.ratio.mixture — โจทย์ความเข้มข้นและของผสมร้อยละ
# ===========================================================================

skill(
    "m.ratio.mixture",
    "m.ratio",
    "โจทย์ความเข้มข้นและของผสมร้อยละ",
    lesson={
        "concept": (
            "ความเข้มข้นของสารละลาย (เช่น น้ำเกลือ หรือ น้ำเชื่อม) ร้อยละ p หมายถึง ในสารละลายทั้งหมด 100 ส่วน มีเนื้อสารแท้ (เกลือ/น้ำตาล) อยู่ p ส่วน "
            "เมื่อเติมน้ำเปล่าเพิ่ม ปริมาณเนื้อสารแท้จะคงเดิม! และเมื่อนำสองถังมาผสมกัน ปริมาณเนื้อสารรวม = เนื้อสารของถังที่ 1 + ถังที่ 2"
        ),
        "steps": [
            "หาปริมาณเนื้อสารแท้ = (เปอร์เซ็นต์ความเข้มข้น ÷ 100) × ปริมาณสารละลายทั้งหมด",
            "ถ้าเติมน้ำเปล่าหรือระเหยน้ำออก: ยึด 'ปริมาณเนื้อสารแท้คงเดิม' เพื่อหาความเข้มข้นใหม่หรือปริมาณสารละลายใหม่",
            "ถ้าผสมสองความเข้มข้นเข้าด้วยกัน: ความเข้มข้นใหม่ = (เนื้อสารรวม ÷ ปริมาณสารละลายรวม) × 100%",
        ],
        "example": {
            "q": "น้ำเชื่อมเข้มข้น 20% จำนวน 300 กรัม ถ้าเติมน้ำเปล่าลงไปอีก 100 กรัม จะได้น้ำเชื่อมที่มีความเข้มข้นกี่เปอร์เซ็นต์",
            "steps": [
                "หาปริมาณน้ำตาลในน้ำเชื่อมเดิม = (20 ÷ 100) × 300 = 60 กรัม",
                "เมื่อเติมน้ำเปล่า 100 กรัม น้ำหนักรวมใหม่ = 300 + 100 = 400 กรัม (แต่น้ำตาลยังมี 60 กรัมเท่าเดิม)",
                "ความเข้มข้นใหม่ = (60 ÷ 400) × 100 = 15%",
            ],
            "a": "15%",
        },
        "mistakes": [
            "เมื่อผสมน้ำเชื่อม 20% กับ 30% ในปริมาณที่ไม่เท่ากัน เผลอเอา (20 + 30) ÷ 2 = 25% ทันทีโดยไม่ถ่วงน้ำหนักตามปริมาณ",
            "เวลาเติมน้ำเปล่า เผลอบวกปริมาณน้ำเข้าไปในตัวเศษ (ปริมาณน้ำตาล) ด้วย",
        ],
        "tips": [
            "จำหลักการเดียวพิชิตทุกข้อ: 'ตามหาปริมาณเนื้อเกลือ/น้ำตาลกี่กรัมให้เจอ' เพราะเนื้อสารไม่หายไปไหน!",
        ],
    },
    weight=1.4,
)


@template("m.ratio.mixture", "hard")
def _mixture_two_solutions():
    # Mix W1 grams of C1% solution with W2 grams of C2% solution -> find resulting concentration %
    configs = [
        (200, 15, 300, 25),
        (300, 10, 200, 25),
        (150, 20, 250, 12),
        (400, 15, 100, 35),
        (200, 10, 600, 30),
        (300, 12, 500, 20),
        (250, 16, 150, 24),
        (100, 10, 300, 30),
    ]
    w1, c1, w2, c2 = pick(configs)
    scale = random.choice([1, 2, 3])
    w1, w2 = w1 * scale, w2 * scale
    solute1 = (w1 * c1) // 100
    solute2 = (w2 * c2) // 100
    total_solute = solute1 + solute2
    total_w = w1 + w2
    ans_pct = (total_solute * 100) // total_w
    avg_pct = (c1 + c2) / 2
    avg_str = dec(avg_pct, 1)
    substance, solute = pick([("น้ำเกลือ", "เกลือ"), ("น้ำเชื่อม", "น้ำตาล")])
    return mcq(
        stem=(
            f"นำ{substance}ความเข้มข้น **{c1}%** จำนวน **{num(w1)} กรัม** "
            f"มาผสมกับ{substance}ความเข้มข้น **{c2}%** จำนวน **{num(w2)} กรัม** "
            f"จะได้{substance}ผสมที่มีความเข้มข้นร้อยละเท่าใด"
        ),
        correct=f"ร้อยละ {ans_pct}",
        wrongs=[
            W(f"ร้อยละ {avg_str if avg_str != str(ans_pct) else ans_pct + 2}",
              f"นำ {c1}% กับ {c2}% มาหาค่าเฉลี่ยครึ่งหนึ่งโดยไม่คิดถ่วงน้ำหนักตามปริมาณที่ไม่เท่ากัน", "trap"),
            W(f"ร้อยละ {c1 + c2}", "นำเปอร์เซ็นต์ความเข้มข้นของทั้งสองส่วนมาบวกกันโดยตรง", "concept"),
            W(f"ร้อยละ {total_solute if total_solute != ans_pct else ans_pct + 4}",
              f"{num(total_solute)} กรัม คือปริมาณ{solute}รวม ยังไม่ได้หารด้วยน้ำหนักสารละลายรวม ({num(total_w)} กรัม)", "partial"),
        ],
        hint=f"หาปริมาณ{solute}ของแต่ละส่วนมารวมกัน แล้วหารด้วยน้ำหนักรวมทั้งหมด ({num(w1)} + {num(w2)} = {num(total_w)} กรัม) คูณ 100",
        steps=[
            f"ส่วนที่ 1 มี{solute} = ({c1} ÷ 100) × {num(w1)} = {solute1} กรัม",
            f"ส่วนที่ 2 มี{solute} = ({c2} ÷ 100) × {num(w2)} = {solute2} กรัม รวมมี{solute} = {total_solute} กรัม",
            f"น้ำหนักรวม = {num(w1)} + {num(w2)} = {num(total_w)} กรัม คิดเป็นความเข้มข้น = ({total_solute} ÷ {num(total_w)}) × 100 = ร้อยละ {ans_pct}",
        ],
    )


@template("m.ratio.mixture", "challenge")
def _dilution_add_water_or_solute():
    # How many grams of pure water must be added to W grams of C1% salt solution to dilute it to C2%?
    configs = [
        (300, 20, 12),
        (400, 25, 20),
        (200, 30, 15),
        (500, 24, 15),
        (300, 25, 15),
        (400, 18, 12),
        (600, 20, 15),
        (250, 24, 12),
    ]
    w_init, c1, c2 = pick(configs)
    scale = random.choice([1, 2, 3])
    w_init *= scale
    solute = (w_init * c1) // 100
    w_final = (solute * 100) // c2
    added_water = w_final - w_init
    return mcq(
        stem=(
            f"มีน้ำเชื่อมความเข้มข้น **{c1}%** อยู่ **{num(w_init)} กรัม** "
            f"จะต้อง **เติมน้ำเปล่า** ลงไปอีกกี่กรัม จึงจะได้น้ำเชื่อมที่มีความเข้มข้นลดลงเหลือ **{c2}%**"
        ),
        correct=f"{num(added_water)} กรัม",
        wrongs=[
            W(f"{num(w_final)} กรัม",
              f"{num(w_final)} กรัม คือน้ำหนักรวมของน้ำเชื่อมใหม่ทั้งหมด ลืมลบน้ำหนักน้ำเชื่อมเดิม ({num(w_init)} กรัม) ออก", "partial"),
            W(f"{num(solute)} กรัม", f"{num(solute)} กรัม คือปริมาณน้ำตาลที่อยู่ในน้ำเชื่อม ไม่ใช่ปริมาณน้ำที่ต้องเติมเพิ่ม", "misread"),
            W(f"{num((w_init * (c1 - c2)) // 100)} กรัม",
              f"นำผลต่างเปอร์เซ็นต์ ({c1}% − {c2}%) ไปคูณกับ {num(w_init)} กรัมโดยตรง", "concept"),
        ],
        hint=f"การเติมน้ำเปล่าทำให้ 'ปริมาณน้ำตาลคงเดิม' ให้หาน้ำตาลในน้ำเชื่อมเดิมก่อน ซึ่งจะคิดเป็น {c2}% ของน้ำเชื่อมใหม่",
        steps=[
            f"ปริมาณน้ำตาลในน้ำเชื่อมเดิม = ({c1} ÷ 100) × {num(w_init)} = {num(solute)} กรัม",
            f"เมื่อเติมน้ำเปล่า น้ำตาล {num(solute)} กรัมนี้จะคิดเป็น {c2}% ของน้ำเชื่อมใหม่",
            f"ดังนั้นน้ำหนักน้ำเชื่อมใหม่ทั้งหมด = ({num(solute)} ÷ {c2}) × 100 = {num(w_final)} กรัม",
            f"ต้องเติมน้ำเปล่าเพิ่ม = {num(w_final)} − {num(w_init)} = {num(added_water)} กรัม",
        ],
    )
