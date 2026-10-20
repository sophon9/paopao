"""English grammar question bank (topic ``e.gram``) for M.1 entrance prep."""

import random

from backend.bank.core import W, mcq, name_en, pick, skill, template

# ---------------------------------------------------------------------------
# 1. Present Simple & Present Continuous
# ---------------------------------------------------------------------------

skill(
    "e.gram.present", "e.gram", "Present Simple & Present Continuous",
    lesson={
        "concept": "Present Simple (V.1 / V.s,es) ใช้กับกิจวัตร ความจริงทั่วไป ตารางเวลา ส่วน Present Continuous (is/am/are + V.ing) ใช้กับสิ่งที่กำลังเกิดขึ้นตอนนี้ และกริยาบอกความรู้สึก/ความคิด (stative verbs) มักไม่เติม -ing",
        "steps": [
            "หาคำบอกเวลาในประโยค เช่น every day, usually (Simple) หรือ now, Look!, right now (Continuous)",
            "เช็กประธานว่าเป็นเอกพจน์หรือพหูพจน์ เพื่อเลือกกริยาให้ตรงรูป",
            "ระวังกริยาที่ไม่ใช้รูป -ing เช่น know, believe, belong, prefer, need",
        ],
        "example": {
            "q": "Look! The children ____ in the playground right now.",
            "steps": [
                "มีคำว่า Look! และ right now บอกเหตุการณ์ที่กำลังทำอยู่",
                "ประธาน The children เป็นพหูพจน์ ใช้ are + V.ing",
            ],
            "a": "are running",
        },
        "mistakes": [
            "ลืมเติม -s/-es เมื่อประธานเป็นเอกพจน์บุรุษที่ 3 ใน Present Simple",
            "ใส่ V.ing โดยไม่มี is/am/are นำหน้า",
            "นำ stative verbs (เช่น know, want, belong) ไปเติม -ing",
        ],
        "tips": ["เจอ Look! / Listen! / at the moment ให้มองหา is/am/are + V.ing ก่อน แต่ถ้ากริยาเป็นตระกูลความรู้สึก/ครอบครอง ให้ใช้ V.1"],
    },
    weight=1.3,
)

_HABITS = [
    ("walk", "walks", "walking", "walked", "to school"),
    ("practice", "practices", "practicing", "practiced", "the piano"),
    ("review", "reviews", "reviewing", "reviewed", "English vocabulary"),
    ("drink", "drinks", "drinking", "drank", "a glass of milk"),
    ("feed", "feeds", "feeding", "fed", "the pet rabbit"),
    ("water", "waters", "watering", "watered", "the garden plants"),
    ("check", "checks", "checking", "checked", "the class schedule"),
    ("clean", "cleans", "cleaning", "cleaned", "the study desk"),
    ("ride", "rides", "riding", "rode", "a bicycle in the park"),
    ("borrow", "borrows", "borrowing", "borrowed", "a science magazine"),
]
_FREQ_ADV = ["every morning", "every evening", "on weekdays", "after dinner", "before class", "twice a week", "every Sunday"]
_NOW_CUES = [
    ("Look!", "right now"),
    ("Listen!", "at the moment"),
    ("Be quiet!", "right now"),
    ("Shh!", "at this moment"),
    ("Look over there!", "now"),
]
_CONT_ACTIONS = [
    ("prepare", "preparing", "prepares", "prepared", "for the science fair"),
    ("paint", "painting", "paints", "painted", "a big poster in the art room"),
    ("rehearse", "rehearsing", "rehearses", "rehearsed", "a school play on the stage"),
    ("solve", "solving", "solves", "solved", "a tough math puzzle"),
    ("build", "building", "builds", "built", "a model bridge together"),
    ("decorate", "decorating", "decorates", "decorated", "the classroom board"),
    ("discuss", "discussing", "discusses", "discussed", "the group project"),
    ("search", "searching", "searches", "searched", "for reference books"),
]


@template("e.gram.present", "easy")
def _present_habit_vs_now():
    name, _ = name_en()
    mode = pick(["habit_sing", "habit_plur", "now_sing", "now_plur"])
    if mode.startswith("habit"):
        v1, vs, ving, v2, obj = pick(_HABITS)
        adv = pick(_FREQ_ADV)
        if mode == "habit_sing":
            subj = name
            correct = vs
            wrongs = [
                W(v1, f"ประธาน {name} เป็นเอกพจน์ กริยาช่อง 1 ต้องเติม -s/-es", "agreement"),
                W(f"is {ving}", f"มีคำบอกความถี่ '{adv}' ต้องใช้ Present Simple ไม่ใช่กำลังกระทำ", "context"),
                W(v2, f"'{adv}' บอกกิจวัตรปัจจุบัน ไม่ใช่เหตุการณ์ในอดีต", "form"),
            ]
            step_s = f"ประธาน {name} เป็นเอกพจน์บุรุษที่ 3 กริยาต้องเติม -s เป็น {vs}"
        else:
            name2, _ = name_en()
            while name2 == name:
                name2, _ = name_en()
            subj = f"{name} and {name2}"
            correct = v1
            wrongs = [
                W(vs, f"ประธาน '{subj}' เป็นพหูพจน์ กริยาไม่ต้องเติม -s", "agreement"),
                W(f"are {ving}", f"'{adv}' บอกกิจวัตรประจำ ใช้ Present Simple รูปกริยาช่อง 1", "context"),
                W(ving, "กริยาเติม -ing อยู่เดี่ยว ๆ เป็นกริยาแท้ของประโยคไม่ได้", "form"),
            ]
            step_s = f"ประธาน '{subj}' เป็นพหูพจน์ ใช้กริยาช่อง 1 รูปเดิมคือ {v1}"
        return mcq(
            stem=f"Choose the best answer to complete the sentence:\n{subj} ____ {obj} {adv}.",
            correct=correct,
            wrongs=wrongs,
            hint="ดูคำบอกเวลาท้ายประโยค แล้วเช็กว่าประธานเป็นเอกพจน์หรือพหูพจน์",
            steps=[f"คำว่า '{adv}' บอกกิจวัตรประจำวัน จึงใช้ Present Simple", step_s],
        )
    cue, tail = pick(_NOW_CUES)
    v1, ving, vs, v2, obj = pick(_CONT_ACTIONS)
    if mode == "now_sing":
        subj = name
        correct = f"is {ving}"
        wrongs = [
            W(vs, f"มี '{cue}' และ '{tail}' แปลว่ากำลังทำอยู่ตอนนี้ ต้องใช้ is + V.ing", "context"),
            W(f"are {ving}", f"ประธาน {name} เป็นเอกพจน์ ต้องใช้ is ไม่ใช่ are", "agreement"),
            W(ving, "ขาด Verb to be (is) หน้ากริยาเติม -ing", "form"),
        ]
    else:
        subj = pick(["The students", "The children", f"{name} and her friends", "Our teammates"])
        correct = f"are {ving}"
        wrongs = [
            W(f"is {ving}", f"ประธาน '{subj}' เป็นพหูพจน์ ต้องใช้ are ไม่ใช่ is", "agreement"),
            W(v1, f"มี '{cue}' และ '{tail}' บอกว่ากำลังเกิดขึ้น ต้องใช้ are + V.ing", "context"),
            W(v2, "เหตุการณ์กำลังเกิดขึ้นตอนนี้ ไม่ใช่เหตุการณ์ในอดีต", "form"),
        ]
    return mcq(
        stem=f"Choose the best answer:\n{cue} {subj} ____ {obj} {tail}.",
        correct=correct,
        wrongs=wrongs,
        hint=f"คำขึ้นต้น '{cue}' และ '{tail}' บอกว่าเหตุการณ์กำลังเกิดขึ้นในขณะพูด",
        steps=[
            f"'{cue}' และ '{tail}' เป็นตัวบอกเวลาของ Present Continuous (is/am/are + V.ing)",
            f"ประธาน '{subj}' จึงใช้ '{correct}'",
        ],
    )


_STATIVE_ITEMS = [
    ("belong", "belongs", "belonging", "belonged", "this blue umbrella", "to", "แสดงความเป็นเจ้าของ"),
    ("know", "knows", "knowing", "knew", "our homeroom teacher", "the answer to this riddle", "บอกความรู้/ความเข้าใจ"),
    ("prefer", "prefers", "preferring", "preferred", "my older brother", "hot cocoa to iced tea", "บอกความชอบ"),
    ("contain", "contains", "containing", "contained", "this wooden box", "old family photos", "บอกส่วนประกอบภายใน"),
    ("need", "needs", "needing", "needed", "the injured puppy", "clean water and rest", "บอกความต้องการ"),
    ("believe", "believes", "believing", "believed", "everyone in our class", "his honest explanation", "บอกความเชื่อ"),
    ("remember", "remembers", "remembering", "remembered", "my grandmother", "every grandchild's birthday", "บอกความทรงจำ"),
    ("own", "owns", "owning", "owned", "my uncle", "a small bakery near the station", "บอกการครอบครอง"),
]


@template("e.gram.present", "medium")
def _present_contrast_and_stative():
    name, pron = name_en()
    if random.random() < 0.55:
        v_hab = pick([
            ("takes the bus", "is riding a bike", "rides a bike", "rode a bike"),
            ("studies in the library", "is studying in the garden", "studies in the garden", "studied in the garden"),
            ("wears sneakers", "is wearing boots", "wears boots", "wearing boots"),
            ("cooks dinner at home", "is eating out with friends", "eats out with friends", "ate out with friends"),
            ("practices badminton", "is swimming at the pool", "swims at the pool", "swam at the pool"),
            ("drinks orange juice", "is having warm soy milk", "has warm soy milk", "had warm soy milk"),
        ])
        hab, now_c, simple_w, past_w = v_hab
        time_now = pick(["today", "right now", "this afternoon", "at the moment"])
        return mcq(
            stem=f"{name} usually {hab}, but {time_now} {pron} ____ instead.",
            correct=now_c,
            wrongs=[
                W(simple_w, f"ครึ่งหลังมี '{time_now}' บอกสิ่งที่กำลังทำต่างจากปกติ ต้องใช้ is + V.ing", "context"),
                W(past_w, f"'{time_now}' เป็นเวลาปัจจุบัน ไม่ใช้กริยาช่อง 2", "form"),
                W(now_c.replace("is ", "are "), f"ประธาน '{pron}' เป็นเอกพจน์ ต้องใช้ is ไม่ใช่ are", "agreement"),
            ],
            hint="สังเกตคำเชื่อม 'but' ที่ตัดระหว่างกิจวัตรปกติ (usually) กับสิ่งที่กำลังทำอยู่ตอนนี้",
            steps=[
                "ประโยคหน้ามี usually ใช้ Present Simple บอกกิจวัตร",
                f"หลัง but มี '{time_now}' บอกการกระทำชั่วคราวในตอนนี้ จึงใช้ Present Continuous: {now_c}",
            ],
        )
    v1, vs, ving, v2, subj_raw, tail, meaning_th = pick(_STATIVE_ITEMS)
    subj = f"{name}'s sister" if subj_raw == "my older brother" and random.random() < 0.5 else subj_raw.capitalize()
    now_phrase = pick(["right now", "at the moment", "even now", "currently"])
    tail_full = f"{tail} {name}" if tail == "to" else tail
    return mcq(
        stem=f"{subj} ____ {tail_full} {now_phrase}.",
        correct=vs,
        wrongs=[
            W(f"is {ving}", f"กริยา '{v1}' ({meaning_th}) เป็น Stative Verb ไม่ใช้รูป Continuous แม้มี '{now_phrase}'", "trap"),
            W(v1, f"ประธาน '{subj}' เป็นเอกพจน์ กริยาต้องเติม -s เป็น '{vs}'", "agreement"),
            W(f"are {ving}", f"ทั้งผิดรูป Stative Verb และผิดพจน์ของประธานเอกพจน์", "agreement"),
        ],
        hint=f"ระวัง! กริยา '{v1}' เป็นกริยาบอกภาวะ/ความรู้สึก (Stative Verb) ไม่เติม -ing",
        steps=[
            f"กริยา '{v1}' ({meaning_th}) เป็น Stative Verb จึงใช้ Present Simple แม้มี '{now_phrase}'",
            f"ประธาน '{subj}' เป็นเอกพจน์บุรุษที่ 3 จึงตอบ '{vs}'",
        ],
    )


# ---------------------------------------------------------------------------
# 2. Past Simple & Past Continuous
# ---------------------------------------------------------------------------

skill(
    "e.gram.past", "e.gram", "Past Simple & Past Continuous",
    lesson={
        "concept": "Past Simple (V.2) ใช้กับเหตุการณ์ที่จบแล้วในอดีต หรือเหตุการณ์ที่แทรกเข้ามาสั้น ๆ (หลัง when) ส่วน Past Continuous (was/were + V.ing) ใช้กับเหตุการณ์ที่กำลังดำเนินอยู่ในอดีต (มักตามหลัง while/as)",
        "steps": [
            "หาคำบอกเวลาอดีต เช่น yesterday, last night, two days ago หรือโครงสร้าง when / while",
            "เหตุการณ์ที่กำลังทำอยู่ต่อเนื่องใช้ was/were + V.ing ส่วนเหตุการณ์ที่เข้ามาแทรกใช้ V.2",
            "ประโยคคำถามและปฏิเสธที่มี did/didn't ต้องตามด้วยกริยาช่อง 1 (V.infinitive) เสมอ",
        ],
        "example": {
            "q": "While Mali ____ her homework, the lights suddenly went out.",
            "steps": [
                "หลัง While เป็นเหตุการณ์ที่กำลังดำเนินอยู่ต่อเนื่องในอดีต",
                "ประธาน Mali เป็นเอกพจน์ ใช้ was + V.ing",
            ],
            "a": "was doing",
        },
        "mistakes": [
            "ใช้ V.2 ซ้อนหลัง didn't เช่น didn't went (ที่ถูกคือ didn't go)",
            "สลับคู่ when/while โดยใช้ V.ing กับเหตุการณ์สั้นที่แทรกเข้ามา",
        ],
        "tips": ["จำสั้น ๆ: กำลังทำอยู่ยาว ๆ = was/were + V.ing | แทรกปุ๊บปั๊บ = V.2 | มี did/didn't = กลับเป็น V.1"],
    },
    weight=1.3,
)

_PAST_PAIRS = [
    ("cross", "crossed", "was crossing", "were crossing", "the street", "the traffic light turned red"),
    ("wait", "waited", "was waiting", "were waiting", "at the bus stop", "it started to pour heavily"),
    ("carry", "carried", "was carrying", "were carrying", "a tray of soup", "he slipped on the wet floor"),
    ("cycle", "cycled", "was cycling", "were cycling", "through the park", "a squirrel jumped onto the path"),
    ("bake", "baked", "was baking", "were baking", "cookies in the kitchen", "the smoke alarm rang"),
    ("pack", "packed", "was packing", "were packing", "her schoolbag", "her phone rang loudly"),
    ("sketch", "sketched", "was sketching", "were sketching", "a portrait", "the pencil tip broke"),
    ("wash", "washed", "was washing", "were washing", "the dishes", "a plate slipped from her hand"),
]


@template("e.gram.past", "easy")
def _past_simple_irregular_and_did():
    name, _ = name_en()
    ago = pick(["yesterday afternoon", "last night", "two days ago", "last Saturday", "three hours ago", "yesterday morning"])
    irreg = pick([
        ("go", "went", "gone", "goes", "to the planetarium"),
        ("buy", "bought", "buyed", "buys", "a new dictionary"),
        ("find", "found", "founded", "finds", "a lost kitten near the gate"),
        ("write", "wrote", "written", "writes", "a thank-you card to the teacher"),
        ("take", "took", "taken", "takes", "photos of the science exhibition"),
        ("leave", "left", "leaved", "leaves", "the umbrella on the school bus"),
        ("break", "broke", "broken", "breaks", "his eyeglasses during PE class"),
        ("catch", "caught", "catched", "catches", "the early train to Chiang Mai"),
    ])
    v1, v2, v3, vs, obj = irreg
    if random.random() < 0.5:
        return mcq(
            stem=f"{name} ____ {obj} {ago}.",
            correct=v2,
            wrongs=[
                W(vs, f"มี '{ago}' บอกอดีตที่จบไปแล้ว ต้องใช้ V.2 ไม่ใช่ V.1 เติม -s", "context"),
                W(v3, f"'{v3}' เป็นกริยาช่อง 3 (V.3) หรือรูปที่ผิด จะวางเดี่ยว ๆ โดยไม่มี have/has/had ไม่ได้", "form"),
                W(f"is {v1}ing" if not v1.endswith("e") else f"is {v1[:-1]}ing", f"'{ago}' เป็นเวลาในอดีต ไม่ใช้ Present Continuous", "context"),
            ],
            hint=f"สังเกตคำบอกเวลา '{ago}' ซึ่งบอกเหตุการณ์ที่จบไปแล้วในอดีต",
            steps=[
                f"คำว่า '{ago}' บอกเวลาในอดีต จึงต้องใช้ Past Simple (กริยาช่อง 2)",
                f"กริยาช่อง 2 ของ '{v1}' คือ '{v2}'",
            ],
        )
    return mcq(
        stem=f"{name} didn't ____ {obj} {ago} because of the heavy rain.",
        correct=v1,
        wrongs=[
            W(v2, "มีกริยาช่วย didn't อยู่แล้ว กริยาแท้ข้างหลังต้องกลับเป็นรูปเดิม (V.1) ห้ามใช้ V.2 ซ้ำ", "form"),
            W(vs, "หลัง didn't ต้องตามด้วย V.infinitive ไม่เติม -s/-es", "form"),
            W(v3, f"หลัง didn't ต้องใช้ V.1 ('{v1}') ไม่ใช่ '{v3}'", "form"),
        ],
        hint="หลัง did หรือ didn't กริยาแท้ต้องอยู่ในรูปใดเสมอ?",
        steps=[
            "โครงสร้างปฏิเสธใน Past Simple คือ didn't + V.infinitive (กริยาช่อง 1 ไม่ผัน)",
            f"ดังนั้นหลัง didn't จึงต้องใช้ '{v1}'",
        ],
    )


@template("e.gram.past", "medium")
def _past_while_when():
    name, _ = name_en()
    v1, v2, was_ing, were_ing, phrase_long, clause_short = pick(_PAST_PAIRS)
    ask_long = random.random() < 0.6
    is_plur = random.random() < 0.4
    subj = f"{name} and her brother" if is_plur else name
    cont_correct = were_ing if is_plur else was_ing
    cont_wrong_agr = was_ing if is_plur else were_ing

    if ask_long:
        return mcq(
            stem=f"While {subj} ____ {phrase_long}, {clause_short}.",
            correct=cont_correct,
            wrongs=[
                W(v2, "หลัง While เป็นเหตุการณ์ที่กำลังดำเนินอยู่ต่อเนื่อง ต้องใช้ was/were + V.ing", "concept"),
                W(cont_wrong_agr, f"ประธาน '{subj}' ไม่สอดคล้องกับ was/were ที่เลือก", "agreement"),
                W(f"are {v1}ing", "ประโยคหลังเป็นอดีต (V.2) เหตุการณ์เกิดในอดีตจึงใช้ are ไม่ได้", "context"),
            ],
            hint="หลัง While บอกเหตุการณ์ที่กำลังดำเนินอยู่ในอดีต ก่อนอีกเหตุการณ์จะแทรกเข้ามา",
            steps=[
                "โครงสร้าง While + Past Continuous, Past Simple ใช้กับเหตุการณ์ที่กำลังทำอยู่แล้วมีอีกเหตุการณ์แทรก",
                f"ประธาน '{subj}' จึงใช้ '{cont_correct}'",
            ],
        )
    interrupt = pick([
        ("ring", "rang", "was ringing", "rings", "the school bell", "loudly"),
        ("drop", "dropped", "was dropping", "drops", f"{name}", "the notebook on the stairs"),
        ("knock", "knocked", "was knocking", "knocks", "someone", "on the classroom door"),
        ("go", "went", "was going", "goes", "the power", "out across the building"),
        ("arrive", "arrived", "was arriving", "arrives", "the principal", "at the hall"),
    ])
    iv1, iv2, iwas, ivs, isubj, itail = interrupt
    return mcq(
        stem=f"{subj} {cont_correct} {phrase_long} when {isubj} suddenly ____ {itail}.",
        correct=iv2,
        wrongs=[
            W(iwas, "เหตุการณ์หลัง when ที่มี suddenly เป็นเหตุการณ์สั้นที่แทรกเข้ามา ต้องใช้ Past Simple (V.2)", "concept"),
            W(ivs, "เหตุการณ์หลักเป็นอดีต (was/were + V.ing) จะใช้ Present Simple ไม่ได้", "context"),
            W(iv1, "ต้องผันเป็นกริยาช่อง 2 เพื่อให้สอดคล้องกับเหตุการณ์ในอดีต", "form"),
        ],
        hint="เหตุการณ์หลัง when ที่เกิดขึ้นฉับพลัน (suddenly) แทรกเข้ามา ใช้ Tense ใด?",
        steps=[
            f"ประโยคหน้า ({cont_correct}) เป็นเหตุการณ์ที่กำลังดำเนินอยู่ในอดีต",
            f"ส่วนที่ตามหลัง when ... suddenly เป็นเหตุการณ์ที่แทรกเข้ามาสั้น ๆ จึงใช้ Past Simple (V.2) คือ '{iv2}'",
        ],
    )


# ---------------------------------------------------------------------------
# 3. Present Perfect & Future Forms
# ---------------------------------------------------------------------------

skill(
    "e.gram.perfect_future", "e.gram", "Present Perfect & Future Forms",
    lesson={
        "concept": "Present Perfect (have/has + V.3) ใช้กับเหตุการณ์ที่เริ่มในอดีตและต่อเนื่องถึงปัจจุบัน (since + จุดเริ่ม, for + ระยะเวลา) หรือเพิ่งจบ/บอกประสบการณ์ (already, yet, ever, never) ส่วนอนาคตใช้ will + V.1 หรือ be going to + V.1",
        "steps": [
            "ถ้าเจอ since, for, already, just, yet, ever, never, so far ให้มองหา have/has + V.3",
            "แยก since (ตามด้วยจุดเวลา เช่น 2020, last week) กับ for (ตามด้วยจำนวนเวลา เช่น three years)",
            "ถ้าเป็นประโยคเวลาในอนาคตหลัง when / before / after / as soon as ห้ามใช้ will ในอนุประโยค ให้ใช้ Present Simple แทน",
        ],
        "example": {
            "q": "Mr. Henry ____ at this school since 2018.",
            "steps": [
                "มีคำว่า since 2018 บอกจุดเริ่มต้นในอดีตที่ต่อเนื่องมาถึงปัจจุบัน ใช้ Present Perfect",
                "ประธาน Mr. Henry เป็นเอกพจน์ ใช้ has + V.3 (taught)",
            ],
            "a": "has taught",
        },
        "mistakes": [
            "ใช้ Past Simple (V.2) ทั้งที่มี since หรือ for บอกความต่อเนื่องถึงปัจจุบัน",
            "ใส่ will หลังคำเชื่อมเวลา when / as soon as / before",
        ],
        "tips": ["เจอ since/for/yet/so far → have/has + V.3 | เจอ when/before/as soon as ในเรื่องอนาคต → หลังคำเชื่อมใช้ V.1/V.s"],
    },
    weight=1.4,
)

_PERF_VERBS = [
    ("live", "has lived", "have lived", "lived", "is living", "in this neighborhood"),
    ("study", "has studied", "have studied", "studied", "is studying", "Japanese and English"),
    ("collect", "has collected", "have collected", "collected", "is collecting", "rare postage stamps"),
    ("work", "has worked", "have worked", "worked", "is working", "as a volunteer librarian"),
    ("play", "has played", "have played", "played", "is playing", "the violin in the youth orchestra"),
    ("know", "has known", "have known", "knew", "is knowing", "each other very well"),
]
_SINCE_POINTS = ["2019", "last October", "she was seven years old", "the beginning of this semester", "January"]
_FOR_SPANS = ["more than five years", "three months", "almost a decade", "six weeks", "over two years"]


@template("e.gram.perfect_future", "medium")
def _present_perfect_since_for_yet():
    name, _ = name_en()
    v1, has_v3, have_v3, v2, is_ing, obj = pick(_PERF_VERBS)
    use_since = random.random() < 0.5
    time_marker = f"since {pick(_SINCE_POINTS)}" if use_since else f"for {pick(_FOR_SPANS)}"
    is_plur = random.random() < 0.35 or v1 == "know"
    subj = f"{name} and her cousin" if is_plur else name
    correct = have_v3 if is_plur else has_v3
    wrong_agr = has_v3 if is_plur else have_v3
    return mcq(
        stem=f"{subj} ____ {obj} {time_marker}.",
        correct=correct,
        wrongs=[
            W(v2, f"มี '{time_marker}' บอกเหตุการณ์ที่ต่อเนื่องมาถึงปัจจุบัน ต้องใช้ Present Perfect (have/has + V.3) ไม่ใช่ Past Simple", "context"),
            W(wrong_agr, f"ประธาน '{subj}' ไม่สอดคล้องกับ have/has ที่เลือก", "agreement"),
            W(is_ing, f"มี '{time_marker}' บอกระยะเวลาสะสมถึงปัจจุบัน ไม่ใช้ Present Continuous", "form"),
        ],
        hint=f"คำบอกเวลา '{time_marker}' ใช้คู่กับโครงสร้าง have/has + V.3",
        steps=[
            f"'{time_marker}' แสดงการกระทำตั้งแต่ในอดีตต่อเนื่องถึงปัจจุบัน จึงใช้ Present Perfect",
            f"ประธาน '{subj}' ใช้คู่กับ '{correct}'",
        ],
    )


@template("e.gram.perfect_future", "hard")
def _future_time_clause_and_since_for():
    name, pron = name_en()
    if random.random() < 0.55:
        conj = pick(["as soon as", "when", "after", "before"])
        act = pick([
            ("finish", "finishes", "will finish", "finished", "the science report", "will send it to the teacher"),
            ("arrive", "arrives", "will arrive", "arrived", "at the station", "will call her parents"),
            ("get", "gets", "will get", "got", "the exam results", "will let you know immediately"),
            ("return", "returns", "will return", "returned", "home this evening", "will feed the kittens"),
            ("check", "checks", "will check", "checked", "the flight schedule", "will book the tickets"),
        ])
        v1, vs, will_v, v2, obj, main_cl = act
        return mcq(
            stem=f"{name} {main_cl} {conj} {pron} ____ {obj}.",
            correct=vs,
            wrongs=[
                W(will_v, f"ในอนุประโยคบอกเวลาหลัง '{conj}' ห้ามใช้ will ให้ใช้ Present Simple แทน", "trap"),
                W(v1, f"ประธาน '{pron}' เป็นเอกพจน์ กริยาใน Present Simple ต้องเติม -s เป็น '{vs}'", "agreement"),
                W(v2, "ประโยคหลักเป็นเรื่องในอนาคต (will) จึงไม่ใช้กริยาช่อง 2 ในอนุประโยค", "context"),
            ],
            hint=f"หลังคำเชื่อมบอกเวลา ({conj}) ที่พูดถึงอนาคต ต้องใช้ Present Simple แทน Future Simple",
            steps=[
                f"ประโยคหลักมี will บอกอนาคต ส่วนที่ตามหลังคำเชื่อมเวลา '{conj}' ต้องใช้ Present Simple",
                f"ประธาน '{pron}' เป็นเอกพจน์ กริยาจึงต้องเติม -s เป็น '{vs}'",
            ],
        )
    # since vs for vs ago vs yet
    mode = pick(["since", "for", "yet"])
    if mode == "since":
        pt = pick(["last April", "2021", "he moved to Bangkok", "Monday morning", "nine o'clock"])
        return mcq(
            stem=f"{name} has been in the computer lab ____ {pt}.",
            correct="since",
            wrongs=[
                W("for", f"'{pt}' เป็นจุดเริ่มต้นของเวลา ต้องใช้ since ไม่ใช่ for (for ใช้กับจำนวนระยะเวลา)", "concept"),
                W("during", "during ใช้ตามด้วยคำนามช่วงเหตุการณ์ และไม่ใช้คู่กับ Present Perfect แบบบอกจุดเริ่ม", "context"),
                W("ago", "ago ใช้กับ Past Simple (V.2) และวางท้ายวลีเวลา ไม่วางหน้าจุดเวลาแบบนี้", "form"),
            ],
            hint=f"'{pt}' เป็น 'จุดเริ่มต้นของเวลา' หรือ 'จำนวนระยะเวลา'?",
            steps=[
                "ประโยคเป็น Present Perfect (has been)",
                f"'{pt}' เป็นจุดเริ่มต้นของเวลา จึงต้องใช้ 'since'",
            ],
        )
    if mode == "for":
        sp = pick(["forty-five minutes", "almost three hours", "several weeks", "a long time", "ten days"])
        return mcq(
            stem=f"The committee has discussed the new school rules ____ {sp}.",
            correct="for",
            wrongs=[
                W("since", f"'{sp}' เป็นจำนวนระยะเวลา ต้องใช้ for ไม่ใช่ since", "concept"),
                W("from", "from ต้องมีจุดเริ่มต้นหรือคู่กับ to ไม่ใช้บอกระยะเวลารวมกับ Present Perfect", "context"),
                W("in", "in ไม่ใช่บุพบทบอกระยะเวลาต่อเนื่องในประโยคบอกเล่า Present Perfect", "form"),
            ],
            hint=f"'{sp}' บอกความยาวนานของเวลา (ระยะเวลา)",
            steps=[
                f"'{sp}' เป็นช่วงระยะเวลา (duration) ไม่ใช่จุดเริ่มต้น",
                "จึงต้องใช้ 'for' คู่กับ Present Perfect",
            ],
        )
    task = pick(["packed the camping gear", "submitted the art assignment", "replied to the invitation", "cleaned the laboratory"])
    return mcq(
        stem=f"Have the students {task} ____? The bus leaves in ten minutes.",
        correct="yet",
        wrongs=[
            W("already", "ในประโยคคำถามทั่วไปที่ถามว่า 'หรือยัง' ตำแหน่งท้ายประโยคใช้ yet เป็นหลัก", "context"),
            W("since", "since ต้องตามด้วยจุดเริ่มต้นของเวลา ไม่วางเดี่ยว ๆ ท้ายคำถาม", "form"),
            W("ever", "ever วางหน้ากริยาช่อง 3 (Have they ever...) ไม่วางท้ายประโยค", "form"),
        ],
        hint="คำใดวางท้ายประโยคคำถามและปฏิเสธใน Present Perfect เพื่อแปลว่า 'หรือยัง'?",
        steps=[
            "ประโยคเป็นคำถาม Present Perfect (Have the students + V.3 ...?)",
            "คำที่วางท้ายประโยคคำถามเพื่อถามว่าทำเสร็จหรือยัง คือ 'yet'",
        ],
    )


# ---------------------------------------------------------------------------
# 4. Subject-Verb Agreement
# ---------------------------------------------------------------------------

skill(
    "e.gram.sva", "e.gram", "Subject-Verb Agreement",
    lesson={
        "concept": "กริยาต้องผันตาม 'ประธานหลัก' เสมอ ไม่ใช่คำนามที่อยู่ติดกริยา: ประธานที่มี with / as well as / along with ยึดตัวหน้า, Either...or / Neither...nor ยึดตัวหลังใกล้กริยา, Each / Every / Everyone / One of the + N.พหูพจน์ ใช้กริยาเอกพจน์",
        "steps": [
            "หาประธานหลักของประโยคให้เจอ (ตัดส่วนขยาย prepositional phrase เช่น of..., with... ออกก่อน)",
            "จำกฎพิเศษ: Everyone/Somebody/Each/One of... = เอกพจน์เสมอ",
            "จำคู่: A number of + N.พหูพจน์ = กริยาพหูพจน์ แต่ The number of + N.พหูพจน์ = กริยาเอกพจน์",
        ],
        "example": {
            "q": "One of my classmates ____ won the national spelling bee.",
            "steps": [
                "ประธานหลักคือคำว่า One (หนึ่งคน) ไม่ใช่ classmates",
                "ประธานเอกพจน์ ใช้กริยาเอกพจน์คือ has",
            ],
            "a": "has",
        },
        "mistakes": [
            "หลงดูคำนามพหูพจน์ที่อยู่หน้ากริยาในโครงสร้าง One of the + N.พหูพจน์ หรือ The box of + N.พหูพจน์",
            "คิดว่า Everyone / Everybody เป็นพหูพจน์เพราะแปลว่าทุกคน",
        ],
        "tips": ["ขีดฆ่าวลีที่ขึ้นต้นด้วย of / with / together with / as well as ออกในใจ จะเห็นประธานตัวจริงทันที"],
    },
    weight=1.5,
)


@template("e.gram.sva", "medium")
def _sva_indefinite_and_one_of():
    name, _ = name_en()
    pattern = pick(["one_of", "indef", "with_phrase"])
    if pattern == "one_of":
        group = pick([
            ("paintings in the gallery", "is", "are", "were", "being", "worth a lot of money"),
            ("students in our club", "speaks", "speak", "speaking", "are speaking", "three foreign languages"),
            ("books on the top shelf", "belongs", "belong", "belonging", "are belonging", f"to {name}"),
            ("players on the team", "has", "have", "having", "are having", "a gold medal"),
            ("rooms on the second floor", "needs", "need", "needing", "are needing", "new curtains"),
        ])
        noun_pl, sing_v, plur_v, w2, w3, tail = group
        lead = pick(["One of the", "Each of the", "Every one of the"])
        return mcq(
            stem=f"{lead} {noun_pl} ____ {tail}.",
            correct=sing_v,
            wrongs=[
                W(plur_v, f"ประธานแท้จริงคือ '{lead.split()[0]}' (เอกพจน์) ไม่ใช่คำนามพหูพจน์ข้างหลัง", "agreement"),
                W(w2, "ผิดทั้งพจน์ของประธานหรือผิดเวลาของประโยค", "agreement"),
                W(w3, "รูปกริยาไม่ถูกต้องตามโครงสร้างประโยค", "form"),
            ],
            hint=f"ในโครงสร้าง '{lead} + คำนามพหูพจน์' ประธานหลักคือคำหน้าสุดซึ่งเป็นเอกพจน์",
            steps=[
                f"ตัดส่วนขยาย 'of the {noun_pl}' ออก จะเห็นประธานหลักคือ '{lead.split()[0]}' (เอกพจน์)",
                f"ดังนั้นต้องใช้กริยาเอกพจน์คือ '{sing_v}'",
            ],
        )
    if pattern == "indef":
        pron = pick(["Everyone", "Everybody", "Someone", "Nobody", "Each student", "Every participant"])
        place = pick(["in the auditorium", "in our study group", "at the summer camp", "on the school bus", "in the science club"])
        verb_set = pick([
            ("has", "have", "are having", "having", "a name badge before entering"),
            ("knows", "know", "are knowing", "knowing", "the emergency exit route"),
            ("wants", "want", "are wanting", "wanting", "to win the quiz trophy"),
            ("needs", "need", "are needing", "needing", "to bring a water bottle"),
            ("enjoys", "enjoy", "are enjoying", "enjoying", "the outdoor workshop"),
        ])
        sing_v, plur_v, w2, w3, tail = verb_set
        return mcq(
            stem=f"{pron} {place} ____ {tail}.",
            correct=sing_v,
            wrongs=[
                W(plur_v, f"'{pron}' ถือเป็นประธานเอกพจน์เสมอในภาษาอังกฤษ ต้องใช้กริยาเอกพจน์", "agreement"),
                W(w2, f"'{pron}' เป็นเอกพจน์ใช้ are ไม่ได้ และกริยานี้ไม่นิยมใช้รูป -ing", "agreement"),
                W(w3, "V.ing อยู่เดี่ยว ๆ ทำหน้าที่เป็นกริยาแท้ของประโยคไม่ได้", "form"),
            ],
            hint=f"คำสรรพนาม '{pron}' นับเป็นเอกพจน์หรือพหูพจน์?",
            steps=[
                f"'{pron}' เป็นประธานเอกพจน์เสมอ (แม้ความหมายรวมหลายคน)",
                f"จึงต้องใช้กริยาเอกพจน์คือ '{sing_v}'",
            ],
        )
    # with / along with / as well as
    conn = pick(["together with", "along with", "as well as", "accompanied by"])
    acc = pick(["her two cousins", "several classmates", "the assistant coaches", "his younger brothers", "three club members"])
    act = pick([
        ("is preparing", "are preparing", "prepare", "have prepared", "for the charity concert"),
        ("has arrived", "have arrived", "arrive", "are arriving", "at the competition venue"),
        ("plans", "plan", "are planning", "planning", "to visit the museum this weekend"),
        ("checks", "check", "are checking", "checking", "the equipment every Friday"),
    ])
    sing_v, plur_v, w2, w3, tail = act
    return mcq(
        stem=f"{name}, {conn} {acc}, ____ {tail}.",
        correct=sing_v,
        wrongs=[
            W(plur_v, f"วลีที่คั่นด้วย '{conn} {acc}' เป็นเพียงส่วนขยาย กริยาต้องผันตามประธานตัวหน้าคือ {name} (เอกพจน์)", "trap"),
            W(w2, f"ประธานหลักคือ {name} (เอกพจน์) ใช้กริยาพหูพจน์ '{w2}' ไม่ได้", "agreement"),
            W(w3, "รูปกริยาไม่ถูกต้องกับประธานเอกพจน์", "form"),
        ],
        hint=f"เมื่อมี '{conn}' คั่นกลาง กริยาต้องผันตามประธานตัวหน้าสุด",
        steps=[
            f"วลี '{conn} {acc}' เป็นส่วนขยาย ไม่ทำให้ประธานกลายเป็นพหูพจน์",
            f"ประธานหลักคือ '{name}' (เอกพจน์) จึงตอบ '{sing_v}'",
        ],
    )


@template("e.gram.sva", "challenge")
def _sva_either_neither_and_number_of():
    name, _ = name_en()
    mode = pick(["neither_sing", "either_plur", "the_number", "a_number"])
    if mode in ("neither_sing", "either_plur"):
        if mode == "neither_sing":
            s1 = pick(["the players", "the students", "the dancers", "the committee members"])
            s2 = pick(["the coach", "the teacher", f"{name}", "the team captain"])
            conj1, conj2 = "Neither", "nor"
            correct, wrong_agr = "is", "are"
            tail = pick(["satisfied with the noisy rehearsal room", "aware of the schedule change", "ready for the sudden inspection", "in the meeting room right now"])
            explain = f"โครงสร้าง Neither...nor กริยาผันตามประธานตัวหลังที่อยู่ใกล้กริยา คือ '{s2}' (เอกพจน์)"
        else:
            s1 = pick(["the manager", "the class president", f"{name}", "the tour guide"])
            s2 = pick(["the assistants", "her classmates", "the volunteers", "his teammates"])
            conj1, conj2 = "Either", "or"
            correct, wrong_agr = "have", "has"
            tail = pick(["the keys to the storage cabinet", "the extra worksheets for today", "the contact list for the trip", "the tickets for the front row"])
            explain = f"โครงสร้าง Either...or กริยาผันตามประธานตัวใกล้กริยา คือ '{s2}' (พหูพจน์)"
        return mcq(
            stem=f"{conj1} {s1} {conj2} {s2} ____ {tail}.",
            correct=correct,
            wrongs=[
                W(wrong_agr, explain, "agreement"),
                W("having" if correct in ("has", "have") else "being", "V.ing อยู่เดี่ยว ๆ เป็นกริยาแท้ของประโยคไม่ได้", "form"),
                W("were" if correct == "is" else "was", "ไม่สอดคล้องกับพจน์ของประธานตัวใกล้กริยา", "agreement"),
            ],
            hint=f"โครงสร้าง {conj1}...{conj2} ให้ดูประธานตัวที่อยู่ใกล้ช่องว่างที่สุด",
            steps=[
                explain,
                f"ดังนั้นจึงต้องใช้กริยา '{correct}'",
            ],
        )
    noun = pick(["applicants for the scholarship", "books donated to the library", "students joining the coding club", "tourists visiting the island", "cyclists in the marathon"])
    if mode == "the_number":
        tail = pick(["increases every year", "is higher than last semester", "has risen sharply this month", "surprises the organizers"])
        wrong_pl = tail.replace("increases", "increase").replace("is ", "are ").replace("has ", "have ").replace("surprises", "surprise")
        correct_v = tail.split()[0]
        wrong_v = wrong_pl.split()[0]
        rest = " ".join(tail.split()[1:])
        return mcq(
            stem=f"The number of {noun} ____ {rest}.",
            correct=correct_v,
            wrongs=[
                W(wrong_v, "'The number of...' แปลว่า 'จำนวนของ...' ประธานคือคำว่า number (เอกพจน์) จึงต้องใช้กริยาเอกพจน์", "trap"),
                W("were" if correct_v == "is" else "are", "The number of ใช้กริยาเอกพจน์เสมอ ไม่ผันตามคำนามพหูพจน์หลัง of", "agreement"),
                W("being", "รูปกริยาไม่สมบูรณ์ ไม่สามารถเป็นกริยาแท้ของประโยคได้", "form"),
            ],
            hint="ระวังความต่างระหว่าง 'The number of' (จำนวนของ... = เอกพจน์) กับ 'A number of' (จำนวนมาก = พหูพจน์)",
            steps=[
                "'The number of + คำนามพหูพจน์' มีประธานหลักคือคำว่า The number (เอกพจน์)",
                f"จึงต้องใช้กริยาเอกพจน์คือ '{correct_v}'",
            ],
        )
    # a_number
    act = pick([
        ("are participating", "is participating", "participates", "has participated", "in the regional math olympiad"),
        ("have signed up", "has signed up", "signs up", "is signing up", "for the robotics workshop"),
        ("volunteer", "volunteers", "is volunteering", "has volunteered", "at the animal shelter every weekend"),
    ])
    plur_v, sing_v, w2, w3, rest = act
    return mcq(
        stem=f"A number of {noun} ____ {rest}.",
        correct=plur_v,
        wrongs=[
            W(sing_v, "'A number of...' แปลว่า 'จำนวนมาก (many)' ใช้คู่กับกริยาพหูพจน์เสมอ", "trap"),
            W(w2, "A number of + คำนามพหูพจน์ ต้องตามด้วยกริยาพหูพจน์ ไม่เติม -s", "agreement"),
            W(w3, "has เป็นกริยาเอกพจน์ ไม่ใช้กับ A number of", "agreement"),
        ],
        hint="'A number of' มีความหมายเหมือน 'Many' จึงถือเป็นพหูพจน์",
        steps=[
            "'A number of + คำนามพหูพจน์' แปลว่า มีจำนวนมาก จึงใช้กริยาพหูพจน์",
            f"คำตอบที่ถูกต้องคือ '{plur_v}'",
        ],
    )


# ---------------------------------------------------------------------------
# 5. Pronouns, Articles & Quantifiers
# ---------------------------------------------------------------------------

skill(
    "e.gram.pron_det", "e.gram", "Pronouns, Articles & Quantifiers",
    lesson={
        "concept": "แยกหน้าที่ของสรรพนาม (ประธาน / กรรม / แสดงความเป็นเจ้าของ my vs mine / สะท้อนตัวเอง -self) การใช้ a/an ตามเสียงขึ้นต้น (an hour, a university) และคำบอกปริมาณ: นับได้พหูพจน์ (many, few/a few) vs นับไม่ได้ (much, little/a little)",
        "steps": [
            "ถ้ามีคำนามตามหลังใช้ Possessive Adjective (my, her, their) ถ้าไม่มีคำนามตามหลังใช้ Possessive Pronoun (mine, hers, theirs)",
            "ดูเสียงพยัญชนะหรือเสียงสระตอนออกเสียงคำแรกหลัง a/an (เสียง อ- ใช้ an เช่น an honest boy, เสียง ย- ใช้ a เช่น a uniform)",
            "เช็กว่าคำนามนับได้หรือนับไม่ได้ และดูว่าประโยคสื่อความหมายเชิงบวก (a few / a little = พอมีอยู่บ้าง) หรือเชิงลบ (few / little = แทบไม่มี)",
        ],
        "example": {
            "q": "It takes about ____ hour to travel to the ____ university by train.",
            "steps": [
                "hour ออกเสียง 'อาว-เออะ' ขึ้นต้นด้วยเสียงสระ ใช้ an",
                "university ขึ้นต้นด้วยเสียง 'ยู' (พยัญชนะ y) หรือชี้เฉพาะเจาะจงตามบริบท",
            ],
            "a": "an",
        },
        "mistakes": [
            "ดูแค่ตัวอักษร u หรือ h โดยไม่ดูเสียงอ่านจริง (เช่นเผลอตอบ an university หรือ a hour)",
            "สับสนระหว่าง few/a few (นามนับได้) กับ little/a little (นามนับไม่ได้)",
        ],
        "tips": ["จำคู่เสียงหลอกข้อสอบ: a uniform, a university, a European, a one-way ticket | an hour, an honest man, an honor"],
    },
    weight=1.3,
)

_PRON_TABLE = [
    ("I", "me", "my", "mine", "myself"),
    ("she", "her", "her", "hers", "herself"),
    ("he", "him", "his", "his", "himself"),
    ("we", "us", "our", "ours", "ourselves"),
    ("they", "them", "their", "theirs", "themselves"),
    ("you", "you", "your", "yours", "yourself"),
]


@template("e.gram.pron_det", "easy")
def _pronouns_possessive_and_reflexive():
    name, _ = name_en()
    mode = pick(["poss_pron", "reflexive"])
    if mode == "poss_pron":
        item_noun = pick(["calculator", "water bottle", "umbrella", "sketchbook", "badminton racket", "dictionary", "jacket", "compass"])
        subj, obj, adj, poss_p, refl = pick([("I", "me", "my", "mine", "myself"), ("we", "us", "our", "ours", "ourselves"), ("they", "them", "their", "theirs", "themselves"), ("you", "you", "your", "yours", "yourself")])
        w_second = subj if obj == adj else obj
        return mcq(
            stem=f"This {item_noun} isn't {adj} {item_noun}; {name} borrowed it because ____ was left at home.",
            correct=poss_p,
            wrongs=[
                W(adj, f"หลังช่องว่างไม่มีคำนามตามหลัง ต้องใช้ Possessive Pronoun ('{poss_p}') ไม่ใช่ '{adj}'", "form"),
                W(w_second, f"'{w_second}' ไม่ใช่รูปแสดงความเป็นเจ้าของที่วางเดี่ยว ๆ เป็นประธานของ was ได้", "form"),
                W(refl, f"'{refl}' เป็นสรรพนามสะท้อนตัวเอง ไม่ได้แปลว่าสิ่งของของตน", "meaning"),
            ],
            hint="หลังช่องว่างเป็นกริยา 'was' ทันที ไม่มีคำนามตามหลัง ต้องใช้รูปที่แปลว่า 'ของ...' แบบไม่ต้องมีนามตาม",
            steps=[
                f"ช่องว่างหมายถึง '{adj} {item_noun}' แต่ละคำนามออกเพื่อไม่ให้ซ้ำ",
                f"เมื่อไม่มีคำนามตามหลัง จึงต้องใช้ Possessive Pronoun คือ '{poss_p}'",
            ],
        )
    subj, obj, adj, poss_p, refl = pick([
        ("I", "me", "my", "mine", "myself"),
        ("we", "us", "our", "ours", "ourselves"),
        ("they", "them", "their", "theirs", "themselves"),
        ("he", "him", "his", "his", "himself"),
    ])
    task = pick([
        "assembled the bookshelf",
        "baked the birthday cake",
        "repaired the broken bicycle",
        "designed the club logo",
        "translated the whole article",
        "painted the bedroom walls",
        "organized the charity booth",
        "programmed the mini robot",
    ])
    subj_cap = f"{name} and I" if subj == "we" else (name if subj == "he" else (f"{name} and her friends" if subj == "they" else "I"))
    return mcq(
        stem=f"{subj_cap} {task} all by ____ without any help from adults.",
        correct=refl,
        wrongs=[
            W(obj, "สำนวน 'by + reflexive pronoun' แปลว่าทำด้วยตัวเอง ต้องใช้รูปที่ลงท้ายด้วย -self/-selves", "form"),
            W(adj, f"'{adj}' ต้องมีคำนามตามหลัง วางหลัง by เดี่ยว ๆ ไม่ได้", "form"),
            W(subj, f"หลังบุพบท 'by' และเมื่อประธานทำเองใช้ '{refl}' ไม่ใช่รูปประธาน '{subj}'", "form"),
        ],
        hint="สำนวน 'by + ...self / ...selves' แปลว่า 'ด้วยตัวเองตามลำพัง'",
        steps=[
            f"ประธานคือ '{subj_cap}' และมีสำนวน 'all by ____' (ด้วยตัวเอง)",
            f"สรรพนามสะท้อนตัวเองที่ตรงกับประธานคือ '{refl}'",
        ],
    )


@template("e.gram.pron_det", "medium")
def _articles_and_quantifiers():
    name, _ = name_en()
    if random.random() < 0.5:
        pair = pick([
            ("uniform", "hour", "a", "an", "uniform ขึ้นต้นด้วยเสียงพยัญชนะ /j/ (ย) ใช้ a ส่วน hour ออกเสียงสระ (h ไม่ออกเสียง) ใช้ an"),
            ("university", "honest", "a", "an", "university ออกเสียง /j/ (ย) ใช้ a ส่วน honest ไม่ออกเสียงตัว h จึงขึ้นต้นด้วยเสียงสระ ใช้ an"),
            ("European", "umbrella", "a", "an", "European ออกเสียง /j/ (ย) ใช้ a ส่วน umbrella ออกเสียงสระอะ ใช้ an"),
            ("one-way", "island", "a", "an", "one-way ออกเสียง /w/ (ว) ใช้ a ส่วน island ออกเสียงสระไอ ใช้ an"),
        ])
        w1, w2, a1, a2, exp = pair
        sentences = {
            ("uniform", "hour"): f"{name} must wear ____ {w1} and arrive half ____ {w2} before the assembly.",
            ("university", "honest"): f"{name}'s brother studies at ____ {w1} and is known as ____ {w2} person.",
            ("European", "umbrella"): f"{name} met ____ {w1} tourist who lent us ____ {w2} during the storm.",
            ("one-way", "island"): f"{name} bought ____ {w1} ticket to visit ____ {w2} in the south.",
        }
        return mcq(
            stem=sentences[(w1, w2)],
            correct=f"{a1} / {a2}",
            wrongs=[
                W(f"{a2} / {a1}", f"สลับกันเพราะดูแต่รูปตัวอักษร: {exp}", "trap"),
                W("an / an", f"คำว่า '{w1}' ออกเสียงขึ้นต้นด้วยพยัญชนะ จึงต้องใช้ a ไม่ใช่ an", "trap"),
                W("a / a", f"คำว่า '{w2}' ออกเสียงขึ้นต้นด้วยเสียงสระ จึงต้องใช้ an ไม่ใช่ a", "concept"),
            ],
            hint="อย่าดูแค่รูปสระ a, e, i, o, u แต่ให้ฟัง 'เสียงแรก' ที่เปล่งออกมา",
            steps=[exp, f"จึงตอบ '{a1} / {a2}'"],
        )
    # Quantifiers: countable vs uncountable & positive vs negative
    q_item = pick([
        ("information", "much", "many", "a few", "several", "คำว่า information เป็นคำนามนับไม่ได้ในประโยคปฏิเสธ ใช้ much"),
        ("advice", "a little", "a few", "many", "several", "advice เป็นคำนามนับไม่ได้ ใช้ a little (พอมีคำแนะนำบ้าง) ไม่ใช้ a few/many"),
        ("furniture", "much", "many", "few", "a few", "furniture เป็นนามนับไม่ได้ ใช้ much ในประโยคปฏิเสธ"),
        ("chairs", "a few", "a little", "much", "an", "chairs เป็นคำนามนับได้พหูพจน์ ใช้ a few (มีเก้าอี้ว่างอยู่บ้าง)"),
        ("mistakes", "few", "little", "much", "a little", "mistakes เป็นคำนามนับได้พหูพจน์ ใช้ few ไม่ใช้ little/much"),
        ("patience", "little", "few", "many", "a few", "patience เป็นคำนามนับไม่ได้ ใช้ little"),
    ])
    noun, corr, w1, w2, w3, exp = q_item
    ctx_map = {
        "information": f"{name} didn't find ____ {noun} about the ancient temple on that website.",
        "advice": f"Could you give {name} ____ {noun} on how to prepare for the interview?",
        "furniture": f"There isn't ____ {noun} in {name}'s new apartment yet.",
        "chairs": f"There are still ____ empty {noun} near {name}, so we can sit together.",
        "mistakes": f"{name} checked the essay carefully, so there were very ____ {noun} on the page.",
        "patience": f"{name}'s little cousin had very ____ {noun} and started crying in the long queue.",
    }
    return mcq(
        stem=ctx_map[noun],
        correct=corr,
        wrongs=[
            W(w1, f"ใช้ผิดประเภทคำนาม: {exp}", "concept"),
            W(w2, f"'{noun}' ไม่สามารถใช้คู่กับ '{w2}' ได้ ({exp})", "agreement"),
            W(w3, f"'{w3}' ไม่สอดคล้องกับพจน์หรือการนับได้ของ '{noun}'", "form"),
        ],
        hint=f"เช็กก่อนว่า '{noun}' เป็นคำนามนับได้พหูพจน์ หรือคำนามนับไม่ได้",
        steps=[exp, f"คำตอบที่ถูกต้องคือ '{corr}'"],
    )


# ---------------------------------------------------------------------------
# 6. Prepositions & Conjunctions
# ---------------------------------------------------------------------------

skill(
    "e.gram.prep_conj", "e.gram", "Prepositions & Conjunctions",
    lesson={
        "concept": "บุพบทบอกเวลา: in + เดือน/ปี/ฤดู/ช่วงวัน, on + วัน/วันที่, at + เวลาจุดเป๊ะ ๆ ส่วนคำเชื่อมความขัดแย้ง: although / even though + ประโยค (S + V) แต่ despite / in spite of + คำนาม/V.ing และ because + ประโยค แต่ because of / due to + คำนาม",
        "steps": [
            "ถ้าเป็นเรื่องเวลา/สถานที่ ให้ดูหน่วยที่ตามหลัง (on Monday, on May 5th, at 7:30, in July)",
            "ถ้าเป็นคำเชื่อม ให้ดูสองอย่าง: (1) ความหมายของสองฝั่ง (คล้อยตาม/ขัดแย้ง/เหตุผล) และ (2) สิ่งที่ตามหลังช่องว่างว่าเป็น 'ประโยค (S+V)' หรือ 'วลีนาม (Noun phrase)'",
        ],
        "example": {
            "q": "____ the heavy traffic, Ploy arrived at the exam hall on time.",
            "steps": [
                "ใจความสองฝั่งขัดแย้งกัน (รถติดหนัก แต่มาทันเวลา)",
                "หลังช่องว่างเป็นวลีนาม 'the heavy traffic' (ไม่มีกริยาแท้) จึงใช้ Despite",
            ],
            "a": "Despite",
        },
        "mistakes": [
            "ใช้ in กับวันที่มีเดือนนำหน้า เช่น May 15th (ที่ถูกคือมีวันที่ต้องใช้ on เสมอ)",
            "ใส่ Although หน้าคำนาม หรือใส่ Despite หน้าประโยค S + V",
        ],
        "tips": ["จำคู่โครงสร้าง: Although + S + V = Despite + N. | Because + S + V = Because of + N."],
    },
    weight=1.3,
)


@template("e.gram.prep_conj", "easy")
def _prepositions_time_and_adj():
    name, _ = name_en()
    if random.random() < 0.5:
        date_str = pick(["Monday morning", "July 24th", "New Year's Eve", "Friday afternoon", "Children's Day", "October 12th"])
        clock_str = pick(["8:30 a.m.", "noon", "quarter past nine", "6:45 p.m.", "midnight"])
        event = pick(["the science camp starts", "our train departs", "the registration closes", "the final match begins", "the museum opens"])
        return mcq(
            stem=f"According to the notice, {event} ____ {clock_str} ____ {date_str}.",
            correct="at / on",
            wrongs=[
                W("on / in", f"เวลาจุดชัดเจน ({clock_str}) ใช้ at และวันหรือวันที่ ({date_str}) ใช้ on ไม่ใช่ in", "concept"),
                W("in / on", f"เวลาตามนาฬิกา ({clock_str}) ต้องใช้ at ไม่ใช่ in", "concept"),
                W("at / in", f"'{date_str}' ระบุวัน/วันที่ชัดเจน ต้องใช้ on ไม่ใช่ in (in ใช้กับเดือนหรือปีเดี่ยว ๆ)", "trap"),
            ],
            hint="จำหลัก: at + เวลาจุดตามนาฬิกา, on + วันหรือวันที่, in + เดือน/ปี",
            steps=[
                f"'{clock_str}' เป็นจุดเวลาที่แน่นอน จึงใช้ 'at'",
                f"'{date_str}' เป็นวันหรือวันที่ จึงใช้ 'on' → ตอบ 'at / on'",
            ],
        )
    adj_prep = pick([
        ("interested", "in", "on", "at", "about", "astronomy and space exploration"),
        ("good", "at", "in", "on", "with", "solving mental math problems"),
        ("afraid", "of", "from", "with", "at", "walking alone in the dark"),
        ("proud", "of", "for", "with", "in", "her younger brother's achievement"),
        ("famous", "for", "of", "in", "with", "its delicious mango sticky rice"),
        ("different", "from", "with", "to", "at", "the old version of the textbook"),
        ("fond", "of", "in", "at", "for", "classical music and painting"),
    ])
    adj, corr, w1, w2, w3, tail = adj_prep
    subj = "This town" if adj == "famous" else ("The new schedule" if adj == "different" else name)
    return mcq(
        stem=f"{subj} is very {adj} ____ {tail}.",
        correct=corr,
        wrongs=[
            W(w1, f"คำคุณศัพท์ '{adj}' ต้องใช้คู่กับบุพบท '{corr}' ({adj} {corr}) ไม่ใช่ '{w1}'", "form"),
            W(w2, f"ไม่ใช้ '{adj} {w2}' ในโครงสร้างนี้ ต้องจำคู่คำ {adj} {corr}", "form"),
            W(w3, f"บุพบทที่คู่กับ '{adj}' คือ '{corr}'", "form"),
        ],
        hint=f"คำคุณศัพท์ '{adj}' มักมาคู่กับบุพบทประจำตัวคำใด?",
        steps=[
            f"โครงสร้างคำคุณศัพท์คู่บุพบทคือ '{adj} {corr}'",
            f"จึงเติม '{corr}' ลงในช่องว่าง",
        ],
    )


@template("e.gram.prep_conj", "hard")
def _conjunctions_clause_vs_phrase():
    name, pron = name_en()
    mode = pick(["although_clause", "despite_np", "because_of_np", "unless_clause"])
    if mode == "although_clause":
        cl = pick([
            (f"{pron} had a slight fever", "finished the math competition"),
            ("the trail was steep and muddy", "reached the waterfall before noon"),
            (f"{pron} practiced for only two weeks", "played the flute confidently"),
            ("the instructions were complicated", "assembled the robot correctly"),
        ])
        sub_cl, main_vp = cl
        return mcq(
            stem=f"____ {sub_cl}, {name} {main_vp}.",
            correct="Although",
            wrongs=[
                W("Despite", f"หลังช่องว่างเป็นประโยคที่มีประธานและกริยา ('{sub_cl}') ใช้ Despite ไม่ได้ เพราะ Despite ต้องตามด้วยคำนาม/V.ing", "trap"),
                W("Because of", "ทั้งผิดความหมาย (ประโยคนี้ขัดแย้งกัน) และ Because of ต้องตามด้วยคำนาม", "meaning"),
                W("Because", "ใจความสองส่วนขัดแย้งกัน ไม่ใช่เหตุและผล จึงต้องใช้ Although", "context"),
            ],
            hint="เช็ก 2 ขั้น: (1) ใจความขัดแย้งหรือคล้อยตาม (2) หลังช่องว่างเป็น ประโยค (S+V) หรือ คำนาม",
            steps=[
                f"ใจความสองฝั่งขัดแย้งกัน และหลังช่องว่าง '{sub_cl}' เป็นประโยคเต็ม (S + V)",
                "จึงต้องใช้คำเชื่อม 'Although' (ใช้ Despite ไม่ได้เพราะ Despite ตามด้วยคำนาม)",
            ],
        )
    if mode == "despite_np":
        np_pair = pick([
            ("the heavy rain", "the football match continued as scheduled"),
            ("his injured ankle", f"{name} completed the 5-kilometer run"),
            ("the loud noise outside", "the students stayed focused on the test"),
            ("her busy schedule", f"{name} volunteers at the library every Saturday"),
        ])
        np_str, main_cl = np_pair
        return mcq(
            stem=f"____ {np_str}, {main_cl}.",
            correct="Despite",
            wrongs=[
                W("Although", f"หลังช่องว่าง '{np_str}' เป็นวลีนาม (ไม่มีกริยาแท้) จึงใช้ Although ไม่ได้", "trap"),
                W("Because of", "ใจความสองฝั่งขัดแย้งกัน ไม่ใช่เหตุผล จึงใช้ Because of ไม่ได้", "meaning"),
                W("However", "However ใช้เชื่อมประโยคเต็มแล้วตามด้วยเครื่องหมายจุลภาค ไม่วางหน้าวลีนามแบบนี้", "form"),
            ],
            hint=f"สังเกตว่า '{np_str}' เป็นเพียงวลีนาม (ไม่มีกริยาแท้) และใจความขัดแย้งกัน",
            steps=[
                f"ใจความขัดแย้งกัน และ '{np_str}' เป็นวลีนาม (Noun Phrase)",
                "จึงต้องใช้ 'Despite' (ถ้าใช้ Although ต้องตามด้วย Subject + Verb)",
            ],
        )
    if mode == "because_of_np":
        np_pair = pick([
            ("the thick fog", "several morning flights were delayed"),
            ("the road construction", "our school bus took a different route"),
            ("the sudden thunderstorm", "the outdoor concert was postponed"),
            (f"{name}'s clear explanation", "everyone understood the science experiment"),
        ])
        np_str, main_cl = np_pair
        return mcq(
            stem=f"____ {np_str}, {main_cl}.",
            correct="Because of",
            wrongs=[
                W("Because", f"หลังช่องว่าง '{np_str}' เป็นวลีนาม ไม่มีกริยาแท้ ต้องใช้ Because of ไม่ใช่ Because", "trap"),
                W("Although", "ใจความเป็นเหตุและผลกัน ไม่ใช่ความขัดแย้ง และหลังช่องว่างเป็นวลีนาม", "meaning"),
                W("Despite", "ใจความเป็นเหตุเป็นผลกัน ไม่ได้ขัดแย้งกัน", "meaning"),
            ],
            hint="ใจความเป็นเหตุและผลกัน และสิ่งที่ตามหลังช่องว่างเป็นวลีนาม (ไม่มีกริยา)",
            steps=[
                f"'{np_str}' เป็นสาเหตุที่ทำให้เกิด '{main_cl}' และเป็นวลีนาม",
                "จึงต้องใช้ 'Because of' + คำนาม",
            ],
        )
    # unless_clause
    cond = pick([
        ("you hurry up", "you will miss the school shuttle bus"),
        (f"{pron} wears a warm coat", f"{name} will catch a cold in the mountain breeze"),
        ("we reserve a table today", "there won't be any seats left on Friday"),
        ("you water these seedlings regularly", "they will wither in the hot sun"),
    ])
    c_cl, m_cl = cond
    return mcq(
        stem=f"____ {c_cl}, {m_cl}.",
        correct="Unless",
        wrongs=[
            W("If", f"ถ้าใส่ If ความหมายจะกลับด้าน ต้องใช้ Unless ซึ่งแปลว่า 'ถ้า...ไม่ (If...not)'", "meaning"),
            W("Because of", "หลังช่องว่างเป็นประโยคเต็ม (S + V) และเป็นเงื่อนไขอนาคต", "form"),
            W("Despite", "Despite ตามด้วยคำนาม ไม่ตามด้วยประโยค S + V", "form"),
        ],
        hint="คำเชื่อมใดมีความหมายเท่ากับ 'If ... not' (ถ้า...ไม่)?",
        steps=[
            f"ความหมายคือ 'ถ้าไม่ ({c_cl}) ก็จะเกิด ({m_cl})'",
            "คำเชื่อมที่แปลว่า 'ถ้า...ไม่' คือ 'Unless'",
        ],
    )


# ---------------------------------------------------------------------------
# 7. Comparatives & Superlatives
# ---------------------------------------------------------------------------

skill(
    "e.gram.compare", "e.gram", "Comparatives & Superlatives",
    lesson={
        "concept": "ขั้นปกติใช้ as + adj/adv + as, ขั้นกว่า (เปรียบเทียบ 2 สิ่ง) ใช้ adj-er / more + adj + than, ขั้นสูงสุด (3 สิ่งขึ้นไป หรือมี in/of the...) ใช้ the + adj-est / the most + adj และจำรูปพิเศษ: good → better → best, bad → worse → worst, far → farther/further → farthest/furthest",
        "steps": [
            "มองหาคำใบ้ในประโยค: as...as (ขั้นปกติ), than (ขั้นกว่า), the ... in/of (ขั้นสูงสุด)",
            "นับพยางค์ของคำคุณศัพท์: สั้น 1 พยางค์เติม -er/-est, ยาว 2–3 พยางค์ขึ้นไปใช้ more/most และห้ามใช้ซ้อนกัน เช่น more better",
            "โครงสร้างยิ่ง...ยิ่ง...: The + ขั้นกว่า ..., the + ขั้นกว่า ...",
        ],
        "example": {
            "q": "This math puzzle is ____ than the one we solved yesterday.",
            "steps": [
                "มีคำว่า than บอกการเปรียบเทียบขั้นกว่า",
                "difficult มี 3 พยางค์ ใช้ more difficult",
            ],
            "a": "more difficult",
        },
        "mistakes": [
            "ใส่ more ซ้อนกับ -er เช่น more faster หรือ more better",
            "ลืมใส่ the หน้าขั้นสูงสุด หรือใส่ขั้นกว่าเมื่อมี of all / in the class",
        ],
        "tips": ["เจอ than → ขั้นกว่า | เจอ of all / in the world / ever → the + ขั้นสูงสุด | เจอ as ... as → รูปปกติห้ามเติม -er"],
    },
    weight=1.3,
)

_ADJ_SETS = [
    ("heavy", "heavier", "the heaviest", "more heavy", "most heavy", "backpack"),
    ("expensive", "more expensive", "the most expensive", "expensiver", "most expensive", "watch"),
    ("good", "better", "the best", "more better", "gooder", "project"),
    ("bad", "worse", "the worst", "more worse", "badder", "traffic jam"),
    ("careful", "more careful", "the most careful", "carefuler", "most careful", "driver"),
    ("far", "farther", "the farthest", "more far", "farer", "village"),
    ("early", "earlier", "the earliest", "more early", "earliest", "train"),
    ("comfortable", "more comfortable", "the most comfortable", "comfortabler", "most comfortable", "armchair"),
]


@template("e.gram.compare", "easy")
def _compare_basic_than_and_superlative():
    name, _ = name_en()
    base, comp, sup, w_double, w_form, noun = pick(_ADJ_SETS)
    if random.random() < 0.5:
        other = pick(["the old one", "mine", f"{name}'s {noun}", "the one we saw yesterday"])
        return mcq(
            stem=f"This {noun} is much ____ than {other}.",
            correct=comp,
            wrongs=[
                W(w_double, f"รูปขั้นกว่าของ '{base}' คือ '{comp}' ห้ามใช้ more ซ้อนหรือเติมผิดรูปเป็น '{w_double}'", "form"),
                W(sup, "มีคำว่า 'than' เป็นการเปรียบเทียบ 2 สิ่ง ต้องใช้ขั้นกว่า ไม่ใช่ขั้นสูงสุด", "concept"),
                W(base, "เมื่อมีคำว่า 'than' ต้องเปลี่ยนคำคุณศัพท์เป็นรูปขั้นกว่า", "form"),
            ],
            hint="สังเกตคำว่า 'than' หลังช่องว่าง (และคำว่า much สามารถวางขยายหน้าขั้นกว่าได้)",
            steps=[
                "ในประโยคมีคำว่า 'than' จึงต้องใช้ Comparative Degree (ขั้นกว่า)",
                f"รูปขั้นกว่าที่ถูกต้องของ '{base}' คือ '{comp}'",
            ],
        )
    scope = pick(["in the whole school", "of all the entries", "in our neighborhood", "I have ever seen", "of the three options"])
    return mcq(
        stem=f"Everyone agrees that this is ____ {noun} {scope}.",
        correct=sup,
        wrongs=[
            W(comp, f"มีขอบเขตเปรียบเทียบทั้งหมด ('{scope}') ต้องใช้ขั้นสูงสุด (the + superlative) ไม่ใช่ขั้นกว่า", "concept"),
            W(w_form, f"ขาด 'the' นำหน้าขั้นสูงสุด หรือผันรูปคำคุณศัพท์ '{base}' ผิด", "form"),
            W(base, f"มี '{scope}' บอกความเป็นที่สุด ต้องใช้รูปขั้นสูงสุด '{sup}'", "concept"),
        ],
        hint=f"วลี '{scope}' บอกการเปรียบเทียบกับกลุ่มทั้งหมด (3 สิ่งขึ้นไป)",
        steps=[
            f"'{scope}' เป็นตัวบ่งชี้ขั้นสูงสุด (Superlative Degree)",
            f"รูปขั้นสูงสุดของ '{base}' คือ '{sup}'",
        ],
    )


@template("e.gram.compare", "hard")
def _compare_as_as_and_double_comparative():
    name, _ = name_en()
    if random.random() < 0.5:
        base, comp, sup, w_double, _, noun = pick(_ADJ_SETS)
        mult = pick(["not quite", "almost", "just", "nearly", "twice"])
        return mcq(
            stem=f"The second riddle was {mult} as ____ as the first one {name} solved.",
            correct=base,
            wrongs=[
                W(comp, "ในโครงสร้าง 'as ... as' ต้องใช้คำคุณศัพท์รูปปกติ (Positive Degree) ห้ามใช้รูปขั้นกว่า", "trap"),
                W(sup.replace("the ", ""), "หลัง 'as ... as' ต้องใช้รูปเดิม ไม่ใช้รูปขั้นสูงสุด", "form"),
                W(w_double, "รูปคำผิดไวยากรณ์ และใน 'as ... as' ต้องใช้รูปปกติเท่านั้น", "form"),
            ],
            hint="ระหว่าง 'as ____ as' คำคุณศัพท์ต้องอยู่ในรูปใดเสมอ แม้มี almost / twice นำหน้า?",
            steps=[
                "โครงสร้างการเปรียบเทียบขั้นเท่ากัน 'as + adj/adv + as' ต้องใช้คำคุณศัพท์รูปปกติ (ไม่ผัน)",
                f"จึงต้องตอบ '{base}'",
            ],
        )
    pair = pick([
        ("harder", "better", "hardest", "best", "more hard", "you practice the violin", "your performance will become"),
        ("higher", "colder", "highest", "coldest", "more high", "we climbed up the mountain", "the wind became"),
        ("earlier", "easier", "earliest", "easiest", "more early", "we leave home", "it is to find a parking spot"),
        ("more carefully", "fewer", "most carefully", "fewest", "carefuller", f"{name} checks the calculations", "mistakes she makes"),
        ("longer", "more impatient", "longest", "most impatient", "more long", "they waited in the queue", "the crowd grew"),
    ])
    c1, c2, s1, s2, w1, cl1, cl2 = pair
    return mcq(
        stem=f"The {c1} {cl1}, ____ {cl2}.",
        correct=f"the {c2}",
        wrongs=[
            W(f"the {s2}", "โครงสร้าง 'ยิ่ง...ยิ่ง...' ต้องใช้ The + ขั้นกว่า คู่กับ the + ขั้นกว่า ไม่ใช่ขั้นสูงสุด", "trap"),
            W(c2, "ขาดคำว่า 'the' นำหน้าขั้นกว่าในครึ่งหลังของโครงสร้าง The + comparative, the + comparative", "form"),
            W(f"more {c2}" if not c2.startswith("more") else c2.replace("more ", ""), "ผันรูปขั้นกว่าผิดหรือขาด the นำหน้า", "form"),
        ],
        hint="โครงสร้าง 'ยิ่ง...ก็ยิ่ง...' คือ The + ขั้นกว่า ..., the + ขั้นกว่า ...",
        steps=[
            f"ประโยคหน้าขึ้นต้นด้วย 'The {c1}...' (The + ขั้นกว่า)",
            f"ประโยคหลังจึงต้องคู่กันด้วย 'the + ขั้นกว่า' คือ 'the {c2}'",
        ],
    )


# ---------------------------------------------------------------------------
# 8. Modals, Conditionals, Passive Voice & Question Tags
# ---------------------------------------------------------------------------

skill(
    "e.gram.modal_cond_passive", "e.gram", "Modals, Conditionals, Passive & Question Tags",
    lesson={
        "concept": "รวมโครงสร้างออกสอบบ่อย: (1) If-clause Type 1: If + Present Simple, will + V.1 และ Type 2 (สมมติไม่จริงในปัจจุบัน): If + Past Simple (were/V.2), would + V.1 (2) Passive Voice: ประธานถูกกระทำใช้ be + V.3 (3) Question Tag: ประโยคบอกเล่า → tag ปฏิเสธ, ประโยคปฏิเสธ (รวม never/seldom/hardly) → tag บอกเล่า",
        "steps": [
            "ถ้าเป็น If-clause ให้ดูคู่กริยาอีกฝั่ง: เห็น will คู่กับ V.1/V.s | เห็น would + V.1 คู่กับ V.2 (ใช้ were กับทุกประธาน)",
            "ถ้าประธานเป็นสิ่งของที่ไม่สามารถทำกริยาเองได้ (เช่น สะพานถูกสร้าง จดหมายถูกส่ง) ให้ใช้ Passive Voice (be + V.3)",
            "ถ้าเป็น Question Tag ให้เช็กกริยาช่วยในประโยคหลัก และระวังคำที่มีความหมายเชิงลบ (never, rarely, hardly, seldom) ต้องใช้ tag บอกเล่า",
        ],
        "example": {
            "q": "The ancient temple ____ more than two hundred years ago.",
            "steps": [
                "ประธาน The ancient temple สร้างตัวเองไม่ได้ ต้องถูกสร้าง (Passive: be + V.3)",
                "มี two hundred years ago เป็นอดีตเอกพจน์ จึงใช้ was built",
            ],
            "a": "was built",
        },
        "mistakes": [
            "ใส่ will หรือ would ในฝั่ง If-clause",
            "ลืมว่าคำว่า never / seldom / hardly มีความหมายเป็นปฏิเสธอยู่แล้ว จึงเผลอใช้ tag ปฏิเสธซ้ำ",
        ],
        "tips": ["ท่องจำเร็ว: If + V.1 → will + V.1 | If + V.2 (were) → would + V.1 | ประธานถูกกระทำ → be + V.3"],
    },
    weight=1.6,
)


@template("e.gram.modal_cond_passive", "medium")
def _conditionals_and_modals():
    name, pron = name_en()
    mode = pick(["if_type1", "if_type2", "modal_rule"])
    if mode == "if_type1":
        sc = pick([
            ("rains", "will rain", "rained", "rain", "it", "this afternoon", f"{name}'s class will move the picnic indoors"),
            ("reviews", "will review", "reviewed", "review", name, "the notes tonight", f"{pron} will pass the quiz easily"),
            ("misses", "will miss", "missed", "miss", name, "the 7 o'clock bus", f"{pron} will be late for the first period"),
            ("finishes", "will finish", "finished", "finish", name, "the chores early", f"{pron} will watch the documentary tonight"),
        ])
        corr, w_will, w_past, w_agr, subj, tail, main_cl = sc
        return mcq(
            stem=f"If {subj} ____ {tail}, {main_cl}.",
            correct=corr,
            wrongs=[
                W(w_will, "ในส่วนของ If-clause (เงื่อนไข) ห้ามใช้ will ให้ใช้ Present Simple แทน", "trap"),
                W(w_past, "ประโยคหลักใช้ 'will + V.1' (If-clause Type 1) ส่วน If จึงต้องใช้ Present Simple ไม่ใช่ Past Simple", "form"),
                W(w_agr, f"ประธาน '{subj}' ไม่สอดคล้องกับรูปกริยา '{w_agr}' ใน Present Simple", "agreement"),
            ],
            hint="สังเกตประโยคหลักมี 'will + V.1' แสดงว่าเป็น If-clause Type 1",
            steps=[
                "โครงสร้าง If-clause Type 1 คือ If + Present Simple, Subject + will + V.1",
                f"ประธาน '{subj}' ในส่วน If จึงต้องใช้ '{corr}'",
            ],
        )
    if mode == "if_type2":
        sc = pick([
            ("had", "have", "will have", "would have", "a pair of wings", "fly across the ocean"),
            ("knew", "know", "will know", "would know", "the secret code", "open the treasure chest"),
            ("lived", "live", "will live", "would live", "near the beach", "go swimming every afternoon"),
            ("were", "am", "will be", "would be", "in your position", "apologize to the teacher immediately"),
        ])
        corr, w_pres, w_will, w_would, cond_tail, act_tail = sc
        subj = "I" if corr == "were" else name
        pron_m = "I" if corr == "were" else pron
        return mcq(
            stem=f"If {subj} ____ {cond_tail}, {pron_m} would {act_tail}.",
            correct=corr,
            wrongs=[
                W(w_pres, "ประโยคหลักใช้ 'would + V.1' เป็นเรื่องสมมติที่ไม่จริงในปัจจุบัน (Type 2) ส่วน If ต้องใช้ Past Simple", "form"),
                W(w_would, "ห้ามใส่ would ในฝั่ง If-clause", "trap"),
                W(w_will, "นี่คือประโยคสมมติ Type 2 (คู่กับ would) ไม่ใช้ will", "form"),
            ],
            hint="ประโยคหลักมี 'would + V.1' แสดงว่าเป็น If-clause Type 2 (สมมติในปัจจุบัน)",
            steps=[
                "โครงสร้าง If-clause Type 2 คือ If + Past Simple (V.2 / were), Subject + would + V.1",
                f"ดังนั้นในช่องว่างหลัง If จึงต้องใช้ '{corr}'",
            ],
        )
    # modal_rule: mustn't vs don't have to
    rule = pick([
        ("must not", "don't have to", "should", "may", f"touch the glass tubes in {name}'s lab group because they are extremely hot"),
        ("must not", "needn't", "can", "ought to", f"use a mobile phone inside {name}'s examination room; it is strictly forbidden"),
        ("don't have to", "must not", "cannot", "should not", f"bring your own paintbrushes because {name} will provide them for everyone"),
        ("doesn't have to", "must not", "cannot", "may not", "pay for the museum ticket because children under twelve can enter for free"),
    ])
    corr, w_opp, w2, w3, tail = rule
    subj = name if corr == "doesn't have to" else "Students"
    why_opp = "must not แปลว่า 'ห้ามทำเด็ดขาด' แต่ don't/doesn't have to แปลว่า 'ไม่จำเป็นต้องทำ' ต้องเลือกให้ตรงบริบท"
    return mcq(
        stem=f"{subj} ____ {tail}.",
        correct=corr,
        wrongs=[
            W(w_opp, why_opp, "meaning"),
            W(w2, "ความหมายขัดแย้งกับเหตุผลที่ให้ไว้ท้ายประโยค", "context"),
            W(w3, "ความหมายไม่ตรงกับกฎหรือเงื่อนไขในประโยค", "meaning"),
        ],
        hint="แยกความหมาย: 'ห้ามทำเด็ดขาด' (must not) กับ 'ไม่จำเป็นต้องทำ' (don't/doesn't have to)",
        steps=[
            f"อ่านบริบทท้ายประโยค: '{tail}'",
            f"ความหมายที่ตรงกับบริบทคือ '{corr}'",
        ],
    )


@template("e.gram.modal_cond_passive", "challenge")
def _passive_voice_and_question_tags():
    name, pron = name_en()
    if random.random() < 0.5:
        pv = pick([
            ("The city library", "was designed", "designed", "were designed", "has designed", f"by {name}'s uncle in 1998"),
            ("These wooden toys", "are made", "make", "is made", "were making", f"by craftsmen in {name}'s hometown every month"),
            ("The Science Fair winners", "were announced", "announced", "was announced", "have announcing", f"by Principal {name} yesterday"),
            ("This classic novel", "was translated", "translated", "were translated", "is translating", f"into Thai before {name} was born"),
            ("All classroom windows", "are cleaned", "clean", "is cleaned", "have cleaning", f"by {name}'s group every Friday"),
            ("The lost wallet", "was found", "found", "were found", "has finding", f"by {name} under the bench this morning"),
        ])
        subj, corr, w_active, w_agr, w_form, tail = pv
        return mcq(
            stem=f"{subj} ____ {tail}.",
            correct=corr,
            wrongs=[
                W(w_active, f"ประธาน '{subj}' ไม่ได้ทำกริยาเอง แต่เป็นฝ่ายถูกกระทำ (มี '{tail}') ต้องใช้ Passive Voice (be + V.3)", "concept"),
                W(w_agr, f"ประธาน '{subj}' ไม่สอดคล้องกับเอกพจน์/พหูพจน์ของ Verb to be", "agreement"),
                W(w_form, "โครงสร้าง Passive Voice ต้องเป็น Verb to be + V.3 ไม่ใช่ have/is + V.ing", "form"),
            ],
            hint=f"ดูว่าประธาน '{subj}' ทำเองหรือถูกกระทำ (สังเกตคำว่า by ... และคำบอกเวลา)",
            steps=[
                f"ประธาน '{subj}' เป็นผู้ถูกกระทำ (มี by ...) จึงต้องใช้โครงสร้าง Passive Voice: Verb to be + V.3",
                f"เมื่อผันตามเวลาและพจน์ของประธาน จึงได้คำตอบคือ '{corr}'",
            ],
        )
    # Question tags (including negative adverbs & Let's)
    tag_item = pick([
        (f"{name} rarely eats fast food at night", f"does {pron}", f"doesn't {pron}", f"is {pron}", f"did {pron}",
         "คำว่า 'rarely' (แทบจะไม่) มีความหมายเป็นปฏิเสธอยู่แล้ว ดังนั้น Question Tag ต้องเป็นบอกเล่า"),
        (f"{name} has never visited Chiang Rai before", f"has {pron}", f"hasn't {pron}", f"does {pron}", f"did {pron}",
         "ในประโยคมี 'never' ซึ่งมีความหมายเป็นปฏิเสธ และมีกริยาช่วย has ดังนั้น Tag ต้องเป็นบอกเล่าคือ 'has + ประธาน'"),
        ("Let's organize a book-swap corner for our class", "shall we", "will you", "don't we", "aren't we",
         "ประโยคชักชวนที่ขึ้นต้นด้วย Let's (Let us) ต้องใช้ Question Tag ว่า 'shall we' เสมอ"),
        (f"{name} and her brother can swim across the pool", "can't they", "can they", "don't they", "aren't they",
         "ประโยคหลักเป็นบอกเล่าที่มีกริยาช่วย can และประธานสองคนเป็นพหูพจน์ (they) จึงใช้ Tag ปฏิเสธ 'can't they'"),
        (f"Your parents bought this piano last year", "didn't they", "did they", "don't they", "weren't they",
         "ประโยคหลักใช้กริยาช่อง 2 (bought) เป็นบอกเล่าในอดีต ไม่มีกริยาช่วย จึงต้องใช้ did ในรูปปฏิเสธคือ 'didn't they'"),
    ])
    stmt, corr, w_trap, w2, w3, exp = tag_item
    return mcq(
        stem=f"{stmt}, ____?",
        correct=corr,
        wrongs=[
            W(w_trap, exp, "trap"),
            W(w2, "ใช้กริยาช่วยไม่ตรงกับกริยาหลักในประโยคหน้า", "form"),
            W(w3, "ใช้กริยาช่วยผิด Tense หรือผิดโครงสร้างของประโยคหน้า", "form"),
        ],
        hint="เช็กกริยาช่วยในประโยคหน้า และระวังคำที่มีความหมายเชิงลบ เช่น never / rarely / seldom หรือโครงสร้าง Let's",
        steps=[exp, f"ดังนั้น Question Tag ที่ถูกต้องคือ '{corr}'"],
    )
