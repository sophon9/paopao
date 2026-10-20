"""English reading comprehension (e.read) for M.1 entrance."""

import random

from backend.bank.core import W, mcq, name_en, num, pick, skill, template

# ---------------------------------------------------------------------------
# Skills registration (6 skills under e.read)
# ---------------------------------------------------------------------------

skill(
    "e.read.notice", "e.read", "การอ่านป้ายประกาศ ป้ายเตือน และตารางข้อมูล",
    lesson={
        "concept": "ป้ายประกาศ (Signs & Notices) และตารางเวลา (Timetables/Schedules) มุ่งสื่อสารข้อมูลสำคัญอย่างกระชับ เช่น สถานที่พบป้าย ข้อห้าม เงื่อนไขเวลา และกลุ่มเป้าหมาย",
        "steps": [
            "อ่านหัวข้อป้าย คำกริยาสำคัญ (เช่น Prohibited, Authorized, Admission, Fragile) และเงื่อนไขตัวเลข/เวลา",
            "ถ้าเป็นตาราง ให้ดูหัวตาราง (แถวและคอลัมน์) แล้วเทียบข้อมูลให้ตรงช่องที่โจทย์ถาม",
        ],
        "example": {
            "q": "Sign: 'SILENCE PLEASE — Exam in Progress'\nWhere would you most likely see this sign?",
            "steps": [
                "ป้ายขอความเงียบเพราะกำลังมีการสอบ (Exam in Progress)",
                "สถานที่ที่พบต้องเป็นหน้าห้องสอบหรืออาคารเรียน",
            ],
            "a": "Outside a school examination hall",
        },
        "mistakes": [
            "ไม่อ่านหมายเหตุดอกจัน (*) หรือเงื่อนไขยกเว้น เช่น Free for children under 10",
            "สับสนคำว่า prohibited / forbidden (ห้าม) กับ permitted / allowed (อนุญาต)",
        ],
        "tips": [
            "จำคำศัพท์ป้ายที่ออกสอบบ่อย: Fragile (แตกหักง่าย), Keep off (ห้ามเหยียบ/เข้าใกล้), Admission (ค่าเข้าชม), Complimentary (ฟรี/อภินันทนาการ)",
        ],
    },
    weight=1.1,
)

skill(
    "e.read.detail", "e.read", "การหาข้อมูลรายละเอียดจากบทอ่าน (Scanning for Details)",
    lesson={
        "concept": "คำถามรายละเอียดถามสิ่งที่ระบุไว้ในเรื่องโดยตรง (Who, What, Where, When, How many, Why) แต่อาจเปลี่ยนคำพ้องความหมาย (Paraphrase) ในตัวเลือก",
        "steps": [
            "ขีดเส้นใต้คำสำคัญ (Keywords) ในคำถาม เช่น ชื่อคน ตัวเลข วันเวลา หรือสถานที่",
            "กวาดสายตา (Scan) หาคำสำคัญนั้นในบทอ่าน แล้วอ่านประโยคเต็ม ๆ เพื่อเช็คว่าตรงกับตัวเลือกใด",
        ],
        "example": {
            "q": "Passage: 'The workshop starts at 9:30 a.m., Beat the queue by arriving 15 minutes earlier for registration.'\nWhat time should participants arrive to register?",
            "steps": [
                "เริ่ม 9:30 น. แต่ควรมาถึงก่อน 15 นาทีเพื่อลงทะเบียน",
                "9:30 น. ย้อนไป 15 นาที คือ 9:15 a.m.",
            ],
            "a": "At 9:15 a.m.",
        },
        "mistakes": [
            "เห็นตัวเลขในบทอ่านแล้วตอบทันทีโดยไม่ดูว่าต้องบวกหรือลบตามเงื่อนไขหรือไม่",
            "ระวังคำถาม NOT true หรือ EXCEPT ซึ่งต้องหาข้อที่ผิดจากเนื้อเรื่อง",
        ],
        "tips": [
            "สำหรับโจทย์ Which is NOT true? ให้เช็คตัวเลือกกับเนื้อเรื่องทีละข้อ ข้อที่ขัดกับเรื่องชัดเจนคือคำตอบ",
        ],
    },
    weight=1.4,
)

skill(
    "e.read.main", "e.read", "การจับใจความสำคัญและจุดประสงค์ของผู้เขียน (Main Idea & Purpose)",
    lesson={
        "concept": "ใจความสำคัญ (Main Idea / Best Title) คือประเด็นหลักที่ครอบคลุมทั้งย่อหน้าหรือทั้งเรื่อง ไม่แคบเกินไป (เป็นแค่รายละเอียดจุดเดียว) และไม่กว้างเกินกว่าที่บทอ่านกล่าวถึง",
        "steps": [
            "อ่านประโยคแรก (Topic Sentence) และประโยคสรุปของเรื่อง",
            "ถามตัวเองว่า 'เรื่องนี้พูดถึงใคร/อะไร และต้องการบอกอะไรเป็นหลัก'",
            "ตัดตัวเลือกที่เป็นเพียงตัวอย่างย่อย ๆ ในย่อหน้าออก",
        ],
        "example": {
            "q": "เรื่องเล่าถึงประโยชน์ของการนอนหลับต่อความจำ อารมณ์ และภูมิคุ้มกันของนักเรียน\nWhat is the best title for the passage?",
            "steps": [
                "ทุกย่อหน้าพูดถึงข้อดีของการนอนหลับให้เพียงพอ",
                "ชื่อเรื่องที่ดีต้องครอบคลุมประโยชน์ของการนอนหลับทั้งหมด",
            ],
            "a": "Why Getting Enough Sleep Matters for Students",
        },
        "mistakes": [
            "เลือกตัวเลือกที่มีคำศัพท์ตรงกับประโยคหนึ่งในเรื่อง แต่เป็นแค่รายละเอียดปลีกย่อย",
        ],
        "tips": [
            "ถ้าถาม Purpose (จุดประสงค์): to inform (ให้ข้อมูล), to persuade (โน้มน้าว), to warn (เตือน), to advertise (โฆษณา)",
        ],
    },
    weight=1.2,
)

skill(
    "e.read.infer", "e.read", "การอนุมานและตีความจากบริบท (Inference & Conclusion)",
    lesson={
        "concept": "การอนุมาน (Inference) คือการสรุปจากหลักฐานที่มีในบทอ่าน แม้ผู้เขียนไม่ได้บอกตรง ๆ แต่สามารถใช้เหตุผลเชื่อมโยงจากข้อมูลในเรื่องได้อย่างมีหลักฐาน",
        "steps": [
            "ดูว่าคำถามถามถึงใครหรือเรื่องอะไร แล้วกลับไปอ่านประโยคที่เกี่ยวข้องในบทอ่าน",
            "สรุปผลตามตรรกะจากข้อมูลที่มี ห้ามคิดต่อเติมเกินกว่าหลักฐานในเรื่อง",
        ],
        "example": {
            "q": "Passage: 'Liam put on his heavy wool coat, grabbed his gloves, and stepped out into the biting wind.'\nWhat can be inferred from the sentence?",
            "steps": [
                "สวมเสื้อโค้ทขนสัตว์หนา หยิบถุงมือ และลมหนาวจัด",
                "อนุมานได้ว่าอากาศข้างนอกหนาวมาก (อาจเป็นฤดูหนาว)",
            ],
            "a": "The weather outside is freezing cold.",
        },
        "mistakes": [
            "เลือกข้อที่เดาเกินจริงโดยไม่มีหลักฐานในบทอ่านรองรับ",
        ],
        "tips": [
            "คำถามมักมีคำว่า infer, imply, suggest, conclude, most likely — คำตอบที่ถูกต้องมีประโยคในเรื่องเป็นหลักฐานยืนยันเสมอ",
        ],
    },
    weight=1.3,
)

skill(
    "e.read.vocab", "e.read", "การเดาความหมายคำศัพท์จากบริบท (Vocabulary in Context)",
    lesson={
        "concept": "เมื่อเจอคำศัพท์ที่ไม่คุ้นเคยในบทอ่าน เราสามารถเดาความหมายได้จากบริบทรอบข้าง (Context Clues) เช่น คำอธิบายขยายความ ตัวอย่าง คำเชื่อมบอกความขัดแย้ง หรือผลลัพธ์ที่ตามมา",
        "steps": [
            "อ่านประโยคที่มีคำศัพท์นั้น และประโยคก่อนหน้า/ถัดไป",
            "สังเกตว่าคำนั้นมีความหมายเชิงบวก (+) หรือเชิงลบ (−) และเป็นคำชนิดใด (นาม กริยา คุณศัพท์)",
            "ลองแทนค่าตัวเลือกลงในประโยคแล้วดูว่าความหมายสมเหตุสมผลที่สุดหรือไม่",
        ],
        "example": {
            "q": "'The hikers were **exhausted** after climbing the steep mountain for six hours without a break.'\nThe word 'exhausted' is closest in meaning to ____.",
            "steps": [
                "ปีนเขาสูงชันติดต่อกัน 6 ชั่วโมงโดยไม่พัก ต้องรู้สึกเหนื่อยล้ามาก",
                "exhausted จึงตรงกับ extremely tired",
            ],
            "a": "extremely tired",
        },
        "mistakes": [
            "เลือกคำศัพท์ที่คุ้นตาแต่เมื่อแทนค่าในประโยคแล้วความหมายขัดกับบริบท",
        ],
        "tips": [
            "ดูตัวชี้แนะ: or / that is (บอกความหมายเหมือน), but / however / although (บอกความหมายตรงข้าม), because / so (บอกเหตุผล)",
        ],
    },
    weight=1.2,
)

skill(
    "e.read.ref", "e.read", "การหาคำที่คำสรรพนามอ้างอิงถึง (Reference Words)",
    lesson={
        "concept": "คำสรรพนามและคำชี้เฉพาะ เช่น it, they, them, their, this, that, one, ones, which ใช้แทนคำนามที่กล่าวถึงข้างหน้าเพื่อไม่ให้เขียนซ้ำ",
        "steps": [
            "ดูว่าคำสรรพนามที่ถามเป็นเอกพจน์ (it, this, that) หรือพหูพจน์ (they, them, their, ones)",
            "ย้อนกลับไปอ่านประโยคหน้าหรือส่วนต้นของประโยคเดียวกันเพื่อหาคำนามที่มีพจน์และความหมายสอดคล้องกัน",
            "ลองนำคำนามนั้นไปแทนที่คำสรรพนาม แล้วอ่านดูว่าใจความถูกต้องหรือไม่",
        ],
        "example": {
            "q": "'Bees collect nectar from flowers and turn **it** into honey.'\nWhat does the word 'it' refer to?",
            "steps": [
                "it เป็นสรรพนามเอกพจน์ (นับไม่ได้) สิ่งที่ผึ้งเปลี่ยนให้เป็นน้ำผึ้งคือ nectar (น้ำหวาน)",
                "flowers เป็นพหูพจน์ (ใช้ them) ดังนั้น it จึงแทน nectar",
            ],
            "a": "nectar",
        },
        "mistakes": [
            "เลือกคำนามที่อยู่ติดกับสรรพนามมากที่สุดโดยไม่ได้เช็คเอกพจน์/พหูพจน์ หรือไม่ได้เช็คความหมาย",
        ],
        "tips": [
            "เช็คพจน์ก่อนเสมอ: it/its แทนคำนามเอกพจน์หรือคำนามนับไม่ได้ | they/them/their แทนคำนามพหูพจน์",
        ],
    },
    weight=1.0,
)


# ---------------------------------------------------------------------------
# Single-item templates (notices, tables, short texts)
# ---------------------------------------------------------------------------

@template("e.read.notice", "easy")
def _notice_signs():
    n = random.randint(8, 12)
    disc = random.choice([15, 20, 25, 30, 50])
    place = pick(["City Botanical Garden", "National Science Centre", "Aquarium World", "History Museum", "Safari Park"])
    signs = [
        (f"NOTICE — {place.upper()}\nAdmission: Adults 120 Baht / Students 60 Baht\n*Free entry for children under {n} years old and seniors over 60.*",
         "According to the notice, who can enter the place without paying?",
         f"A {n - 2}-year-old child visiting with parents",
         [W(f"A {n + 3}-year-old secondary school student", f"นักเรียนอายุ {n + 3} ปี เกินเกณฑ์ต่ำกว่า {n} ปี ต้องจ่ายค่าบัตรนักเรียน 60 บาท", "detail"),
          W("All visitors on weekends", "ป้ายไม่ได้ระบุว่าเข้าฟรีทุกคนในวันหยุดสุดสัปดาห์", "misread"),
          W("Adults who bring a student ID card", "ผู้ใหญ่ต้องจ่าย 120 บาท", "detail")],
         f"ป้ายระบุว่า Free entry for children under {n} years old ดังนั้นเด็กอายุ {n - 2} ปีจึงเข้าชมฟรี"),
        (f"CAUTION: WET FLOOR\nCleaning in progress near Gate {random.randint(2, 9)}.\nPlease use the side corridor to avoid slipping.",
         "What does this sign advise people to do?",
         "Walk through another passage and be careful not to slip",
         [W("Help the staff mop the hallway", "ป้ายเตือนระวังพื้นลื่น ไม่ได้ขอให้ช่วยถูพื้น", "meaning"),
          W("Run quickly across the wet area", "การวิ่งบนพื้นเปียกจะทำให้ลื่นล้มได้ง่าย", "context"),
          W("Wait until the building closes at night", "ป้ายแนะนำให้ใช้ทางเดินด้านข้าง (side corridor) แทน", "detail")],
         "ป้ายเตือนพื้นเปียก (Wet Floor) และแนะนำให้ใช้ทางเดินด้านข้างเพื่อป้องกันการลื่นล้ม"),
        (f"SCHOOL LIBRARY NOTICE\nAll borrowed books must be returned by Friday, {random.randint(10, 28)} March.\nA fine of {random.randint(5, 15)} baht per day will be charged for overdue items.",
         "What will happen if a student returns a book late?",
         "The student will have to pay money for each late day.",
         [W("The student will receive a free bookmark.", "คืนหนังสือช้า (overdue) จะต้องเสียค่าปรับ (fine) ไม่ใช่ได้ของแถม", "meaning"),
          W("The library will be closed on Friday.", "วันศุกร์เป็นวันกำหนดส่งคืนหนังสือ ไม่ใช่วันปิดห้องสมุด", "misread"),
          W("The student can keep the book forever.", "ป้ายระบุว่าต้องนำมาคืนภายในกำหนด", "detail")],
         "คำว่า overdue แปลว่าเกินกำหนด และ fine แปลว่าค่าปรับ ดังนั้นคืนช้าต้องเสียค่าปรับรายวัน"),
        (f"FLASH SALE AT GREEN BOOKSHOP!\nBuy 2 English storybooks and get {disc}% off the second book!\n(Valid only this Saturday and Sunday)",
         "Which statement is TRUE according to the advertisement?",
         "Customers get a discount on the second storybook only on the weekend.",
         [W(f"Every single book in the shop is {disc}% off all week.", "ส่วนลดใช้ได้เฉพาะเล่มที่ 2 และเฉพาะวันเสาร์-อาทิตย์เท่านั้น", "detail"),
          W("You must buy at least four books to get a discount.", "เงื่อนไขคือซื้อ 2 เล่ม (Buy 2)", "detail"),
          W("The promotion is available only on weekdays.", "ป้ายระบุว่า Valid only this Saturday and Sunday (สุดสัปดาห์)", "misread")],
         f"โปรโมชันซื้อ 2 เล่ม ลดราคาเล่มที่สอง {disc}% เฉพาะวันเสาร์และอาทิตย์เท่านั้น"),
    ]
    passage, stem, ans, wrongs, exp = pick(signs)
    return mcq(
        stem=stem,
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="อ่านรายละเอียดและเงื่อนไขในป้ายประกาศให้ครบทุกบรรทัด",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.read.notice", "medium")
def _notice_timetable():
    student, pron = name_en()
    clubs = pick([
        ("Robotics", "Monday", "15:30 - 17:00", "Room 302", "200 Baht"),
        ("Cooking", "Tuesday", "15:30 - 16:45", "Home Econ Lab", "350 Baht"),
        ("Badminton", "Wednesday", "16:00 - 17:30", "Sports Hall", "Free"),
        ("Drama", "Thursday", "15:30 - 17:00", "Auditorium", "150 Baht"),
        ("Astronomy", "Friday", "16:30 - 18:00", "Roof Deck", "100 Baht"),
    ], 4)
    table = {
        "caption": "After-School Club Schedule (Semester 1)",
        "head": ["Club Name", "Day", "Time", "Venue", "Material Fee"],
        "rows": [list(c) for c in clubs],
    }
    mode = random.randint(1, 3)
    c0, c1, c2, c3 = clubs
    if mode == 1:
        stem = f"According to the schedule, where and on what day does the {c1[0]} Club meet?"
        ans = f"In the {c1[3]} on {c1[1]}s"
        wrongs = [
            W(f"In the {c0[3]} on {c0[1]}s", f"นั่นเป็นสถานที่และวันของชมรม {c0[0]}", "detail"),
            W(f"In the {c2[3]} on {c1[1]}s", f"ดูช่อง Venue ผิดแถว ชมรม {c1[0]} เรียนที่ {c1[3]}", "misread"),
            W(f"In the {c1[3]} on {c3[1]}s", f"ดูวันผิดแถว ชมรม {c1[0]} เรียนวัน {c1[1]}", "misread"),
        ]
        exp = f"ดูแถวของชมรม {c1[0]} จะพบว่าเรียนวัน {c1[1]} ที่ {c1[3]}"
    elif mode == 2:
        target = c0
        stem = f"{student} wants to join the {target[0]} Club. How much is the material fee and when does it meet?"
        ans = f"{target[4]}, on {target[1]}s at {target[2]}"
        wrongs = [
            W(f"{c1[4]}, on {c1[1]}s at {c1[2]}", f"เป็นค่าธรรมเนียมและเวลาของชมรม {c1[0]}", "detail"),
            W(f"{target[4]}, on {c2[1]}s at {c2[2]}", f"ค่าธรรมเนียมถูก แต่วันและเวลาเป็นของชมรม {c2[0]}", "misread"),
            W(f"{c3[4]}, on {target[1]}s at {c3[2]}", f"ค่าธรรมเนียมและเวลาเป็นของชมรม {c3[0]}", "misread"),
        ]
        exp = f"ดูแถว {target[0]} Club: ค่าวัสดุ {target[4]} วัน {target[1]} เวลา {target[2]}"
    else:
        target = c2
        stem = f"Which statement is TRUE according to the club schedule?"
        ans = f"The {target[0]} Club meets on {target[1]} in the {target[3]}."
        wrongs = [
            W(f"The {c0[0]} Club meets on {c1[1]}.", f"ชมรม {c0[0]} พบกันวัน {c0[1]} ไม่ใช่ {c1[1]}", "detail"),
            W(f"The {c3[0]} Club is held in the {c0[3]}.", f"ชมรม {c3[0]} จัดที่ {c3[3]}", "detail"),
            W("All clubs start at the exact same time every day.", "เวลาเริ่มของแต่ละชมรมในตารางไม่เท่ากันทั้งหมด", "misread"),
        ]
        exp = f"ตรวจสอบตารางแถว {target[0]} Club: วัน {target[1]} สถานที่ {target[3]} ซึ่งตรงกับตัวเลือกที่ถูก"
    return mcq(
        stem=stem,
        table=table,
        correct=ans,
        wrongs=wrongs,
        hint="เทียบแถว (ชื่อชมรม) กับคอลัมน์ (วัน เวลา สถานที่ ค่าธรรมเนียม) ในตารางให้ตรงกัน",
        steps=[exp, f"คำตอบคือ \"{ans}\""],
    )


@template("e.read.detail", "easy")
def _detail_short_email():
    sender, s_pron = name_en()
    receiver, _ = name_en()
    while receiver == sender:
        receiver, _ = name_en()
    place = pick(["National Planetarium", "Green Valley Farm", "City Art Gallery", "Marine Science Centre"])
    time_meet = pick(["8:15 a.m.", "8:30 a.m.", "8:45 a.m."])
    bring = pick(["a notebook and a reusable water bottle", "a sketchpad and coloured pencils", "a cap and sunscreen lotion", "a packed lunch and a raincoat"])
    cost = random.choice([80, 100, 120, 150])
    passage = (
        f"To: {receiver}\nFrom: {sender}\nSubject: Saturday Field Trip\n\n"
        f"Hi {receiver},\n"
        f"Just a quick reminder about our class trip to the {place} this Saturday. "
        f"The school van will leave promptly at 9:00 a.m., so Mr. Harris asked everyone to gather at the front gate by {time_meet}. "
        f"Don't forget to bring {bring}. Also, the entrance ticket costs {cost} baht, but the school is paying half of it for us!\n"
        f"See you on Saturday,\n{sender}"
    )
    q_type = random.randint(1, 3)
    if q_type == 1:
        stem = f"How much does {receiver} actually have to pay for the entrance ticket?"
        ans = f"{cost // 2} baht"
        wrongs = [
            W(f"{cost} baht", f"{cost} บาทเป็นราคาเต็ม แต่โรงเรียนออกให้ครึ่งหนึ่ง (paying half)", "trap"),
            W(f"{cost * 2} baht", "นำราคาบัตรไปคูณสอง ซึ่งผิดจากที่โรงเรียนช่วยจ่ายครึ่งหนึ่ง", "calc"),
            W("Nothing at all", "โรงเรียนจ่ายให้ครึ่งเดียว (half) ไม่ใช่จ่ายให้ทั้งหมด", "misread"),
        ]
        exp = f"บัตรราคาเต็ม {cost} บาท แต่โรงเรียนช่วยจ่ายครึ่งหนึ่ง นักเรียนจึงจ่ายเอง {cost} ÷ 2 = {cost // 2} บาท"
    elif q_type == 2:
        stem = "What time must the students arrive at the school front gate?"
        ans = f"By {time_meet}"
        wrongs = [
            W("At 9:00 a.m.", "9:00 a.m. คือเวลารถตู้ล้อหมุนออกเดินทาง แต่ครูให้นัดเจอที่หน้าประตูก่อนหน้านั้น", "trap"),
            W("At 9:30 a.m.", "มาถึงหลังเวลารถออกจะตกรถ", "detail"),
            W("In the afternoon", "เป็นทริปช่วงเช้า (a.m.)", "misread"),
        ]
        exp = f"อีเมลระบุว่าครูขอให้ทุกคนมารวมตัวที่หน้าประตูโรงเรียนภายในเวลา {time_meet}"
    else:
        stem = f"What does {sender} remind {receiver} to bring on the trip?"
        ans = bring.capitalize()
        wrongs = [
            W("A camera and a pair of binoculars", "ไม่ได้ระบุไว้ในอีเมล", "detail"),
            W("A sleeping bag and a flashlight", "เป็นทริปไปเช้าเย็นกลับ ไม่ได้ให้นำถุงนอนไป", "detail"),
            W("A heavy winter coat and boots", "ไม่ได้กล่าวถึงในอีเมล", "detail"),
        ]
        exp = f"ในอีเมลมีประโยค 'Don't forget to bring {bring}.'"
    return mcq(
        stem=stem,
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="อ่านอีเมลอย่างละเอียด โดยเฉพาะตัวเลขเวลาและเงื่อนไขค่าตั๋ว",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.read.main", "medium")
def _main_idea_paragraph():
    city = pick(["Singapore", "Bangkok", "Tokyo", "Seoul", "Sydney"])
    crop = pick(["apples, almonds, and berries", "melons, cherries, and pumpkins", "pears, peaches, and tomatoes"])
    uni = pick(["Oxford", "Cambridge", "Waterloo", "Melbourne", "Toronto"])
    topics = [
        (f"Honeybees are much more than just makers of sweet honey. As they fly from blossom to blossom gathering nectar, they transfer pollen between plants. In fact, nearly one-third of the crops humans eat—including {crop}—depend on pollination by bees. Without these tiny insects, supermarket shelves would lose many colourful fruits and vegetables.",
         "The vital role of honeybees in pollinating food crops",
         [W("How to collect sweet honey from beehives safely", "บทอ่านไม่ได้สอนวิธีเก็บน้ำผึ้ง แต่เน้นเรื่องการผสมเกสรพืชอาหาร", "detail"),
          W(f"Why {crop.split(',')[0]} are more nutritious than other fruits", "ชื่อผลไม้เป็นเพียงตัวอย่างพืชที่พึ่งพาผึ้งในการผสมเกสร", "trap"),
          W("The life cycle of a queen bee inside the hive", "บทอ่านไม่ได้กล่าวถึงนางพญาผึ้งเลย", "misread")],
         "บทอ่านเน้นว่าผึ้งไม่ได้แค่ทำน้ำผึ้งแต่ช่วยผสมเกสรให้พืชอาหารของมนุษย์ถึง 1 ใน 3"),
        (f"Many students think reading aloud is only for young children, but psychologists at {uni} have found that it actually boosts memory for learners of all ages. When you read a word out loud, you both see it and hear yourself say it. This dual action creates a stronger pathway in the brain than reading silently.",
         "How reading aloud helps strengthen memory",
         [W("Why silent reading is better for older students", "บทอ่านบอกว่าการอ่านออกเสียงช่วยให้จำได้ดีกว่าอ่านในใจสำหรับทุกวัย", "misread"),
          W("The history of children's picture books", "ไม่ได้พูดถึงประวัติศาสตร์หนังสือภาพเด็ก", "detail"),
          W("How to speak louder in a noisy classroom", "ไม่ได้สอนการตะโกนในห้องเรียนที่เสียงดัง", "meaning")],
         "ใจความสำคัญคือการอ่านออกเสียงช่วยกระตุ้นทั้งการมองเห็นและการได้ยิน ทำให้สมองจดจำได้ดีกว่า"),
        (f"Vertical gardens—walls covered with living plants—are becoming popular in crowded cities like {city}. Because they grow upwards instead of spreading across the ground, they take up almost no street space. At the same time, the leaves absorb heat, filter dust from the air, and make grey concrete buildings look lively.",
         "The benefits of vertical gardens in busy cities",
         [W(f"The most expensive buildings in {city}", f"{city} เป็นเพียงตัวอย่างเมืองที่นิยมจัดสวนแนวตั้ง", "trap"),
          W("Why concrete is the best material for modern houses", "บทอ่านพูดถึงการใช้ต้นไม้ช่วยลดความร้อนของตึกคอนกรีต", "misread"),
          W("How to grow vegetables on a large country farm", "สวนแนวตั้งใช้ในเมืองที่พื้นที่จำกัด ไม่ใช่ฟาร์มชนบทขนาดใหญ่", "detail")],
         "ย่อหน้านี้กล่าวถึงสวนแนวตั้งในเมืองใหญ่ว่าช่วยประหยัดพื้นที่ ลดความร้อน กรองฝุ่น และเพิ่มความสวยงาม"),
        (f"Before paper money was invented, people around the world used surprising objects as currency. Over {random.randint(2, 4)} thousand years ago, cowrie shells were traded for goods. The Aztecs valued cocoa beans so highly that they used them as coins, while Roman soldiers were sometimes paid in salt—which is where the English word 'salary' comes from.",
         "Unusual items used as money in the past",
         [W("How to make delicious chocolate from Aztec cocoa beans", "เมล็ดโกโก้เป็นเพียงหนึ่งตัวอย่างของสิ่งที่ใช้แทนเงินในอดีต", "trap"),
          W("The daily training routine of ancient Roman soldiers", "ทหารโรมันถูกกล่าวถึงเฉพาะเรื่องการรับค่าจ้างเป็นเกลือ", "detail"),
          W("Why modern paper money is easy to carry", "เนื้อเรื่องเน้นสิ่งที่ใช้แทนเงินในสมัยโบราณก่อนมีธนบัตร", "misread")],
         "ประโยคแรก (Topic Sentence) และตัวอย่างทั้งเปลือกหอย เมล็ดโกโก้ และเกลือ ล้วนพูดถึงสิ่งของที่ใช้เป็นเงินตราในอดีต"),
    ]
    passage, ans, wrongs, exp = pick(topics)
    variant = pick(["What is the main idea of this paragraph?", "Which is the best title for the passage?", "What is the passage mainly about?"])
    return mcq(
        stem=variant,
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ดูประโยคแรกของย่อหน้า แล้วหาตัวเลือกที่ครอบคลุมเนื้อหาทั้งหมด ไม่ใช่แค่ตัวอย่างเดียว",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.read.vocab", "medium")
def _vocab_in_context_single():
    name, pron = name_en()
    hrs = random.randint(3, 6)
    items = [
        (f"After hiking through the desert sun for {hrs} hours, {name}'s water bottle was completely empty, and {pron} felt **parched**.",
         "parched", "extremely thirsty",
         [W("completely full", "กระติกน้ำหมดเกลี้ยงหลังเดินตากแดดในทะเลทราย จึงไม่สามารถอิ่มน้ำได้", "context"),
          W("deeply bored", "บริบทพูดถึงแดดทะเลทรายและน้ำหมดขวด จึงเกี่ยวกับความกระหายน้ำ", "meaning"),
          W("very wealthy", "wealthy แปลว่าร่ำรวย ไม่เกี่ยวกับการเดินป่ากลางแดด", "meaning")],
         f"เดินตากแดดในทะเลทราย {hrs} ชั่วโมงและน้ำหมดขวด คำว่า parched จึงหมายถึง กระหายน้ำอย่างมาก (extremely thirsty)"),
        (f"The ancient {pick(['porcelain vase', 'glass bowl', 'crystal teapot', 'clay statue'])} in the museum is extremely **fragile**; even a slight bump could shatter it into a hundred pieces.",
         "fragile", "easily broken",
         [W("heavy and solid", "ประโยคหลังบอกว่าแค่ชนเบา ๆ ก็แตกเป็นเสี่ยง ๆ จึงไม่ใช่ของแข็งแรงทนทาน", "context"),
          W("brand new", "เป็นของโบราณ (ancient) จึงไม่ใช่ของใหม่เอี่ยม", "misread"),
          W("cheaply made", "บริบทเน้นว่าแตกหักง่าย ไม่ได้พูดถึงราคา", "meaning")],
         "ประโยคหลังขยายความว่า 'แค่ชนเบา ๆ ก็แตกเป็นร้อยชิ้น' ดังนั้น fragile จึงแปลว่า แตกหักง่าย (easily broken)"),
        (f"Although {name} and {pick(['Leo', 'Maya', 'Toby', 'Zoe'])} are twins who look identical, their personalities are **distinct**—one is quiet and shy, while the other loves performing on stage.",
         "distinct", "clearly different",
         [W("almost the same", "มีคำเชื่อม Although (แม้ว่าหน้าตาเหมือนกัน) และยกตัวอย่างนิสัยที่ตรงข้ามกัน", "trap"),
          W("hard to notice", "นิสัยของทั้งสองคนแตกต่างกันอย่างชัดเจน", "meaning"),
          W("unfriendly", "ไม่ได้แปลว่าไม่เป็นมิตร แต่แปลว่าแตกต่างกัน", "meaning")],
         "สังเกตคำเชื่อม Although และตัวอย่างที่คนหนึ่งขี้อายแต่อีกคนชอบแสดงออก ดังนั้น distinct จึงแปลว่า แตกต่างกันอย่างชัดเจน"),
        (f"Heavy rain near {pick(['Chiang Rai', 'Nan', 'Mae Hong Son', 'Tak'])} caused a landslide that **obstructed** the mountain road, so drivers had to turn back and take another route.",
         "obstructed", "blocked",
         [W("repaired", "ถ้าซ่อมถนนเสร็จแล้ว คนขับคงไม่ต้องเลี้ยวกลับไปใช้เส้นทางอื่น", "context"),
          W("widened", "ดินถล่มทำให้คนขับต้องย้อนกลับ แปลว่าถนนถูกกีดขวาง ไม่ใช่ขยายกว้างขึ้น", "meaning"),
          W("decorated", "ดินถล่มจากพายุฝนไม่ได้ตกแต่งถนน", "meaning")],
         "ดินถล่มทำให้คนขับรถต้องย้อนกลับไปใช้ทางอื่น แสดงว่าถนนถูกปิดกั้นหรือกีดขวาง (blocked)"),
        (f"At first, {name} was **reluctant** to jump into the swimming pool because the water looked icy cold.",
         "reluctant", "unwilling and hesitant",
         [W("eager and excited", "เพราะน้ำดูเย็นจัดเหมือนน้ำแข็ง จึงเกิดความลังเลไม่อยากกระโดดลงไป", "trap"),
          W("proud", "ความภูมิใจไม่เกี่ยวกับการที่น้ำในสระเย็นจัด", "meaning"),
          W("careless", "บริบทบอกเหตุผลว่าน้ำเย็นจัดจึงลังเล", "meaning")],
         "เพราะน้ำดูเย็นจัดเหมือนน้ำแข็ง จึงรู้สึกไม่เต็มใจหรือลังเลที่จะกระโดดลงสระ (unwilling and hesitant)"),
    ]
    passage, word, ans, wrongs, exp = pick(items)
    return mcq(
        stem=f"In the sentence, the word **{word}** is closest in meaning to ____.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="อ่านคำใบ้ในประโยค เช่น คำเชื่อมความขัดแย้ง (Although) หรือเหตุและผล (because, so)",
        steps=[exp, f"ดังนั้น '{word}' จึงมีความหมายตรงกับ \"{ans}\""],
    )


@template("e.read.ref", "easy")
def _ref_pronoun_single():
    name, _ = name_en()
    n_trees = random.choice([150, 200, 250, 300])
    items = [
        (f"When {name} bought new leather shoes last week, **they** pinched at the toes, so {name} took them back to the shop.",
         "they", "new leather shoes",
         [W("the toes", "สิ่งที่ซื้อมาเมื่อสัปดาห์ก่อนและบีบรัดนิ้วเท้าคือรองเท้าหนังคู่ใหม่", "trap"),
          W("the shop", "shop เป็นเอกพจน์ แทนด้วย they ไม่ได้", "form"),
          W(name, f"{name} เป็นคนเดียว ใช้ he/she ไม่ใช่ they", "form")],
         "they เป็นพหูพจน์ แทนสิ่งที่บีบรัดนิ้วเท้าเมื่อซื้อมา คือ new leather shoes"),
        (f"Sea otters in {pick(['Alaska', 'the North Pacific', 'cold coastal waters'])} have thick fur that traps air bubbles, and **this** keeps their bodies warm in freezing ocean water.",
         "this", "having thick fur that traps air bubbles",
         [W("freezing ocean water", "น้ำทะเลที่เย็นจัดไม่ได้ช่วยให้ร่างกายอบอุ่น", "context"),
          W("sea otters", "sea otters เป็นพหูพจน์ แต่ this เป็นเอกพจน์ที่อ้างถึงกระบวนการข้างหน้า", "form"),
          W("other marine animals", "ไม่ได้กล่าวถึงในประโยค", "misread")],
         "this อ้างถึงข้อความข้างหน้าที่ว่า ขนหนาช่วยกักเก็บฟองอากาศไว้ ซึ่งช่วยให้ร่างกายอบอุ่น"),
        (f"The city council planted {n_trees} oak trees along the river because **their** deep roots help prevent soil erosion.",
         "their", "the oak trees'",
         [W("the city council's", "สภาเมืองไม่มีรากลึก (deep roots) ต้นโอ๊กต่างหากที่มีราก", "meaning"),
          W("the river's", "river เป็นเอกพจน์ และแม่น้ำไม่มีราก", "form"),
          W("the soil's", "soil เป็นนามนับไม่ได้ และสิ่งที่มีรากคือต้นไม้", "form")],
         f"คำนามพหูพจน์ที่มี deep roots (รากลึก) ช่วยยึดดินคือ {n_trees} oak trees"),
        (f"{name} tried the strawberry cupcakes and the lemon tarts, but {name} preferred the **ones** topped with fresh berries.",
         "ones", "cupcakes / pastries",
         [W("fresh berries", "ones แทนขนมที่ราดหน้าด้วยเบอร์รี ไม่ได้แทนตัวเบอร์รีซ้ำ", "trap"),
          W(name, "ones ใช้แทนคำนามพหูพจน์ที่กล่าวไปแล้ว คือขนมเค้ก/ทาร์ต", "form"),
          W("the bakery", "bakery เป็นเอกพจน์และไม่ได้อยู่ในประโยค", "form")],
         "ones เป็นสรรพนามพหูพจน์ใช้แทนคำนามพหูพจน์ที่กล่าวถึงข้างหน้า (cupcakes/tarts) เพื่อไม่ต้องเขียนซ้ำ"),
    ]
    passage, word, ans, wrongs, exp = pick(items)
    return mcq(
        stem=f"What does the word **{word}** in bold refer to?",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="เช็คพจน์ (เอกพจน์/พหูพจน์) และดูว่าสิ่งใดทำกริยาหรือมีลักษณะตามที่ประโยคระบุ",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.read.infer", "challenge")
def _infer_critical_reading():
    name, pron = name_en()
    baker = pick(["Mr. Sakda", "Mrs. Malee", "Uncle Sompong", "Mr. Chuchat"])
    inst = pick(["violin", "cello", "flute", "clarinet"])
    temp_c = random.choice([60, 65, 70])
    cases = [
        (f"Every evening at 6:00 p.m., {baker} closes the bakery door, puts the unsold loaves and pastries into clean paper bags, and hands them to street sweepers and night-shift guards walking past the shop. Only after the last bag is gone does {baker} count the day's earnings.",
         f"What can we infer about {baker}'s character?",
         "generous and caring towards workers in the community",
         [W("careless about cleanliness and food safety", "ใส่ถุงกระดาษสะอาด (clean paper bags) แสดงว่าใส่ใจความสะอาด", "inference"),
          W("dishonest and sells stale bread during the day", "แจกขนมที่ขายไม่หมดตอนปิดร้านให้ฟรี ไม่ได้นำของเก่ามาหลอกขาย", "misread"),
          W("greedy and charges guards extra after 6:00 p.m.", "คำว่า hands them to... และนับรายได้หลังจากแจกหมด แปลว่าให้โดยไม่คิดเงิน", "detail")],
         "จากการที่นำขนมที่เหลือใส่ถุงสะอาดแจกคนกวาดถนนและยามกะดึกทุกเย็นก่อนนับเงิน อนุมานได้ว่าเป็นคนใจกว้างและมีน้ำใจ"),
        (f"When {name} stepped onto the stage with the {inst}, {pron} gripped it so tightly that {pron}r knuckles turned white. However, as soon as the pianist played the opening chord, {name} took a slow breath, and a clear, steady melody filled the hall.",
         f"How did {name}'s feelings change in the passage?",
         "From nervous at the beginning to calm and focused once the music started",
         [W("From confident and proud to deeply disappointed", "ตอนท้ายบรรเลงเพลงได้อย่างไพเราะมั่นคง (clear, steady melody) ไม่ได้ผิดหวัง", "context"),
          W("From angry at the pianist to bored with the audience", "การกำแน่นจนข้อนิ้วขาวคืออาการตื่นเต้นประหม่า ไม่ใช่โกรธนักเปียโน", "inference"),
          W("From sleepy and tired to frightened by the loud noise", "ไม่มีหลักฐานว่าง่วงนอนหรือตกใจเสียงดัง", "inference")],
         "ตอนแรกกำแน่นจนข้อนิ้วขาวแสดงว่าตื่นเต้นประหม่า แต่พอเริ่มเล่นก็หายใจช้า ๆ และเล่นได้นิ่งและไพเราะ แสดงว่าสงบและมีสมาธิขึ้น"),
        (f"Although the new 'Eco-Bottle' is advertised as 100% biodegradable, a footnote on the label states that it breaks down only inside industrial composting tanks heated to {temp_c}°C—facilities that fewer than five percent of towns currently have.",
         "What is the author implying about the 'Eco-Bottle'?",
         "In most towns, the bottle will not actually break down as easily as buyers might think.",
         [W("The bottle will melt immediately if you pour warm water into it.", f"ต้องอยู่ในถังหมักอุตสาหกรรมความร้อน {temp_c}°C จึงจะย่อยสลาย ไม่ใช่ละลายทันทีเมื่อใส่น้ำอุ่น", "misread"),
          W("Every town already has the machines needed to recycle the bottle.", "บทอ่านระบุว่ามีเมืองไม่ถึง 5% เท่านั้นที่มีโรงงานแบบนั้น", "detail"),
          W("The company refuses to sell the bottle in big cities.", "ไม่ได้พูดถึงการห้ามขายในเมืองใหญ่", "inference")],
         "แม้โฆษณาว่าย่อยสลายได้ 100% แต่ต้องใช้โรงงานเฉพาะที่มีอยู่ไม่ถึง 5% ของเมืองทั้งหมด จึงตีความได้ว่าในเมืองส่วนใหญ่ขวดนี้จะไม่ได้ย่อยสลายได้เองตามธรรมชาติอย่างที่คนซื้อเข้าใจ"),
    ]
    passage, stem, ans, wrongs, exp = pick(cases)
    return mcq(
        stem=stem,
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="อาศัยหลักฐานจากรายละเอียดในบทอ่านเพื่อสรุปสิ่งที่ผู้เขียนบอกเป็นนัย",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# Group reading templates (multi-question passages)
# ---------------------------------------------------------------------------

@template("e.read.detail", "medium", group=True)
def _group_community_project():
    leader, l_pron = name_en()
    town = pick(["Greenwood", "Maplewood", "Riverside", "Brookfield", "Sunvale"])
    place = pick(["old canal bank", "abandoned railway lot", "empty corner behind the library", "unused school courtyard"])
    trees = random.randint(25, 60)
    volunteers = random.randint(30, 80)
    hours = random.randint(3, 5)
    sponsor = pick(["Sunrise Bakery", "Town Hardware Store", "Fresh Mart Supermarket", "Green Leaf Nursery"])
    passage = (
        f"Last month, a twelve-year-old student named {leader} noticed that the {place} in {town} was covered with plastic litter and tall weeds. "
        f"Instead of waiting for the town council, {leader} designed posters inviting neighbours to join a weekend clean-up. "
        f"To {leader}'s surprise, {volunteers} residents showed up on Saturday morning with gloves and rakes. "
        f"Working together for {hours} hours, **they** cleared ten bags of rubbish and planted {trees} young fruit trees donated by {sponsor}. "
        f"Today, the area has become a shady mini-park where children read and elderly neighbours **stroll** in the evening."
    )
    q1 = mcq(
        skill="e.read.main",
        difficulty="medium",
        passage=passage,
        stem="What is the passage mainly about?",
        correct=f"How a student's initiative turned a neglected spot in {town} into a community park",
        wrongs=[
            W(f"Why {sponsor} is the most popular shop in {town}", f"{sponsor} เป็นเพียงผู้บริจาคต้นไม้ ไม่ใช่ประเด็นหลักของเรื่อง", "trap"),
            W("How the town council fined people for littering in the canal", "ในเรื่องระบุว่าไม่ได้รอเทศบาล แต่คนในชุมชนช่วยกันทำเอง", "misread"),
            W("Different species of fruit trees that grow well in winter", "ต้นไม้ผลเป็นเพียงส่วนหนึ่งของกิจกรรมปลูกต้นไม้", "detail"),
        ],
        hint="ดูภาพรวมตั้งแต่ปัญหาเริ่มต้น การลงมือทำ ไปจนถึงผลลัพธ์สุดท้ายของพื้นที่นั้น",
        steps=[
            f"เรื่องเล่าตั้งแต่ {leader} เห็นพื้นที่รกร้าง จึงชวนคนในชุมชนมาทำความสะอาดและปลูกต้นไม้จนกลายเป็นสวนเล็ก ๆ",
            "ดังนั้นใจความสำคัญคือการริเริ่มของนักเรียนที่เปลี่ยนพื้นที่รกร้างให้เป็นสวนของชุมชน",
        ],
    )
    q2 = mcq(
        skill="e.read.detail",
        difficulty="medium",
        passage=passage,
        stem="According to the passage, how did the volunteers get the young fruit trees?",
        correct=f"They were given for free by {sponsor}.",
        wrongs=[
            W(f"{leader} bought them using pocket money.", f"เนื้อเรื่องบอกว่า donated (บริจาค) โดย {sponsor}", "detail"),
            W("The town council planted them the previous year.", "เทศบาลไม่ได้เป็นคนปลูก", "misread"),
            W(f"Each of the {volunteers} residents brought one tree from home.", "ชาวบ้านนำถุงมือและคราดมา ส่วนต้นไม้ได้รับบริจาค", "detail"),
        ],
        hint="หาคำว่า fruit trees ในบทอ่านแล้วดูคำว่า donated by...",
        steps=[
            f"บทอ่านระบุว่า 'planted {trees} young fruit trees donated by {sponsor}'",
            f"donated แปลว่า บริจาค (ให้ฟรี) ดังนั้นจึงได้รับมาจาก {sponsor}",
        ],
    )
    q3 = mcq(
        skill="e.read.ref",
        difficulty="medium",
        passage=passage,
        stem="In sentence 4, what does the word **they** in bold refer to?",
        correct=f"The {volunteers} residents who came to help",
        wrongs=[
            W("Gloves and rakes", "ถุงมือและคราดไม่สามารถเก็บขยะและปลูกต้นไม้เองได้", "meaning"),
            W("Plastic litter and tall weeds", "ขยะและวัชพืชไม่ใช่ผู้ที่ทำงานร่วมกัน", "meaning"),
            W("The town council members", "สมาชิกสภาเมืองไม่ได้มาในวันนั้น", "detail"),
        ],
        hint="ย้อนไปดูประโยคก่อนหน้าว่าใครเป็นคนมาปรากฏตัวในเช้าวันเสาร์",
        steps=[
            f"ประโยคก่อนหน้าพูดถึง '{volunteers} residents showed up on Saturday morning'",
            f"ดังนั้น they ที่ช่วยกันทำงาน {hours} ชั่วโมง จึงหมายถึงชาวบ้าน {volunteers} คนที่มาช่วยกัน",
        ],
    )
    q4 = mcq(
        skill="e.read.vocab",
        difficulty="medium",
        passage=passage,
        stem="The word **stroll** in the last sentence is closest in meaning to ____.",
        correct="walk in a slow, relaxed way",
        wrongs=[
            W("run at top speed", "ผู้สูงอายุ (elderly neighbours) มาพักผ่อนในสวนยามเย็น จึงเป็นการเดินเล่นช้า ๆ ไม่ใช่วิ่งสุดฝีเท้า", "context"),
            W("argue loudly", "สวนร่มรื่นที่เด็กอ่านหนังสือและผู้สูงอายุมาพักผ่อน ไม่ใช่การทะเลาะกัน", "meaning"),
            W("work hurriedly", "เป็นการพักผ่อนตอนเย็นหลังสวนเสร็จแล้ว", "context"),
        ],
        hint="ผู้สูงอายุในสวนร่มรื่นตอนเย็นควรทำกริยาอย่างไร",
        steps=[
            "บริบทคือสวนร่มรื่นที่เด็กมาอ่านหนังสือและผู้สูงอายุมาพักผ่อนในตอนเย็น",
            "คำว่า stroll จึงแปลว่า เดินเล่นอย่างผ่อนคลาย (walk in a slow, relaxed way)",
        ],
    )
    return [q1, q2, q3, q4]


@template("e.read.infer", "hard", group=True)
def _group_science_discovery():
    scientist = pick(["Dr. Elena Vance", "Dr. Kenji Sato", "Dr. Arisa Rattana", "Dr. Marcus Cole"])
    island = pick(["Coral Bay", "Mist Island", "Emerald Reef", "Silver Atoll"])
    creature = pick(["bioluminescent jellyfish", "deep-reef octopus", "glass-winged beetle", "lantern squid"])
    depth = random.randint(120, 350)
    temp = random.randint(4, 9)
    samples = random.randint(12, 28)
    passage = (
        f"During a three-week expedition near {island}, marine biologist {scientist} studied a rare species of {creature} "
        f"living {depth} metres below the surface, where sunlight never reaches and the water stays at {temp}°C. "
        f"Unlike shallow-water animals that use bright colours to hide among corals, **these creatures** produce brief flashes of blue light from their skin. "
        f"After observing {samples} individuals with an underwater camera, {scientist} discovered that the flashes are not used to attract prey, as earlier textbooks claimed. "
        f"Instead, when a predator approaches, the {creature} releases a glowing cloud to **baffle** the attacker while it jets backward into the darkness."
    )
    q1 = mcq(
        skill="e.read.detail",
        difficulty="hard",
        passage=passage,
        stem=f"Which of the following is NOT true according to {scientist}'s study?",
        correct=f"The {creature} uses its blue flashes mainly to lure food closer.",
        wrongs=[
            W(f"The habitat {depth} metres down receives no natural sunlight.", "ระบุไว้ตรง ๆ ว่า where sunlight never reaches", "detail"),
            W(f"{scientist} used an underwater camera to observe {samples} of the animals.", f"ระบุไว้ในเรื่องว่าสังเกต {samples} ตัวด้วยกล้องใต้น้ำ", "detail"),
            W(f"The water temperature in their habitat is around {temp}°C.", f"ระบุไว้ในเรื่องว่าน้ำมีอุณหภูมิ {temp}°C", "detail"),
        ],
        hint="ระวังโจทย์ถามข้อที่ NOT true! ดูประโยคที่พูดถึง earlier textbooks claimed",
        steps=[
            "บทอ่านระบุว่า 'the flashes are not used to attract prey, as earlier textbooks claimed'",
            "ดังนั้นข้อที่บอกว่าใช้แสงสีฟ้าเพื่อล่อเหยื่อ (lure food) จึงไม่เป็นความจริงตามการค้นพบใหม่",
        ],
    )
    q2 = mcq(
        skill="e.read.infer",
        difficulty="hard",
        passage=passage,
        stem="What can be inferred from the passage?",
        correct=f"Previous scientific books contained inaccurate information about why the {creature} glows.",
        wrongs=[
            W(f"The {creature} can easily survive in warm, shallow swimming pools.", f"มันอาศัยในน้ำลึก {depth} เมตรที่อุณหภูมิ {temp}°C ไม่ใช่สระน้ำตื้นอุ่น", "inference"),
            W(f"{scientist} captured all {samples} animals and brought them to a city zoo.", "นักวิทยาศาสตร์เพียงใช้กล้องใต้น้ำสังเกตการณ์ (observing with an underwater camera)", "misread"),
            W("Predators in the deep ocean are completely blind to blue light.", "ถ้าผู้ล่ามองไม่เห็นแสงสีฟ้าเลย การปล่อยแสงเพื่อหลอกล่อผู้ล่าคงไม่ได้ผล", "inference"),
        ],
        hint="เปรียบเทียบสิ่งที่ตำราเรียนเก่าเขียนไว้ (earlier textbooks claimed) กับสิ่งที่นักวิจัยค้นพบจริง",
        steps=[
            "ตำราเก่าอ้างว่าแสงใช้ล่อเหยื่อ แต่งานวิจัยใหม่ด้วยการสังเกตจริงพบว่าใช้ป้องกันตัวจากผู้ล่า",
            "จึงอนุมานได้ว่าข้อมูลในตำราเรียนก่อนหน้านี้ยังไม่ถูกต้อง",
        ],
    )
    q3 = mcq(
        skill="e.read.vocab",
        difficulty="hard",
        passage=passage,
        stem="The word **baffle** in the last sentence is closest in meaning to ____.",
        correct="confuse",
        wrongs=[
            W("welcome", "คงไม่ต้อนรับผู้ล่า (predator) ที่กำลังเข้ามาโจมตี", "context"),
            W("feed", "เป็นการปล่อยกลุ่มแสงเพื่อหนีเอาตัวรอด ไม่ใช่ให้อาหารผู้ล่า", "meaning"),
            W("strengthen", "ไม่ต้องการทำให้ผู้ล่าแข็งแกร่งขึ้น", "meaning"),
        ],
        hint="สัตว์ปล่อยกลุ่มแสงสว่างออกมาในขณะที่ตัวเองถอยหนีเข้าความมืด เพื่อทำอะไรกับผู้ล่า",
        steps=[
            "เมื่อผู้ล่าเข้ามาใกล้ มันปล่อยกลุ่มแสงเรืองรองเพื่อทำให้ผู้ล่าสับสนมึนงง (baffle = confuse) แล้วพุ่งตัวหนีไปในความมืด",
            "ดังนั้น baffle จึงมีควาหมายตรงกับ confuse",
        ],
    )
    q4 = mcq(
        skill="e.read.ref",
        difficulty="hard",
        passage=passage,
        stem="What does the phrase **these creatures** in sentence 2 refer to?",
        correct=f"The rare {creature} living {depth} metres below the surface",
        wrongs=[
            W("Shallow-water animals living among corals", "ประโยคขึ้นต้นว่า Unlike shallow-water animals... (ต่างจากสัตว์น้ำตื้น) ดังนั้น these creatures จึงหมายถึงสัตว์น้ำลึกที่กล่าวถึงในประโยคแรก", "trap"),
            W("Marine biologists on the expedition", "นักชีววิทยาทางทะเลไม่สามารถปล่อยแสงสีฟ้าออกจากผิวหนังได้", "meaning"),
            W("Colorful corals near the island", "ปะการังไม่ใช่สัตว์ที่ปล่อยแสงและพุ่งตัวหนีในเรื่องนี้", "detail"),
        ],
        hint="ดูโครงสร้าง Unlike X, these creatures... คำว่า these creatures ต้องไม่ใช่ X แต่เป็นสัตว์ในประโยคแรก",
        steps=[
            f"ประโยคที่ 2 เปรียบเทียบว่า 'ต่างจากสัตว์น้ำตื้น... สัตว์เหล่านี้ (these creatures) ผลิตแสงสีฟ้าจากผิวหนัง'",
            f"ดังนั้น these creatures จึงหมายถึง {creature} ที่กล่าวถึงในประโยคแรก",
        ],
    )
    return [q1, q2, q3, q4]
