"""English conversation and situational expressions (e.conv) for M.1 entrance."""

import random

from backend.bank.core import W, mcq, name_en, pick, skill, template

# ---------------------------------------------------------------------------
# 1. Polite expressions: requests, offers, apologies, thanks, permission
# ---------------------------------------------------------------------------

skill(
    "e.conv.polite", "e.conv", "สำนวนสุภาพ การขอร้อง ขออนุญาต และกล่าวขอบคุณ/ขอโทษ",
    lesson={
        "concept": "การพูดอย่างสุภาพในภาษาอังกฤษต้องเลือกสำนวนให้ตรงกับเจตนา เช่น ขอร้อง (Could you...), ขออนุญาต (Would you mind if I...), เสนอความช่วยเหลือ (Shall I...) และการตอบรับที่เหมาะสม",
        "steps": [
            "ดูสถานะและความสัมพันธ์ของผู้พูด (เพื่อน ครู พนักงาน หรือคนแปลกหน้า)",
            "สังเกตโครงสร้างสำคัญ เช่น Would you mind + V-ing / if I + V1 ตอบรับอนุญาตต้องใช้คำปฏิเสธ (No, not at all / Of course not)",
            "ตรวจสอบว่าการตอบรับสอดคล้องกับประโยคต่อมาหรือไม่",
        ],
        "example": {
            "q": "A: Would you mind opening the window?\nB: ____. It's quite stuffy in here too.",
            "steps": [
                "Would you mind...? แปลว่า 'คุณจะรังเกียจไหมถ้า...'",
                "ประโยคหลัง B บอกว่า 'ในนี้อึดอัดเหมือนกัน' แปลว่า B ยินดีเปิดให้ (ไม่รังเกียจ)",
                "ตอบว่าไม่รังเกียจ ต้องใช้ Not at all. หรือ Of course not.",
            ],
            "a": "Not at all",
        },
        "mistakes": [
            "ตอบ Yes, I do mind เมื่อตั้งใจจะอนุญาต (Yes แปลว่ารังเกียจ/ไม่อนุญาต)",
            "สับสนระหว่าง Never mind (ไม่เป็นไร ใช้ตอบคำขอโทษ) กับ You're welcome (ด้วยความยินดี ใช้ตอบคำขอบคุณ)",
        ],
        "tips": [
            "จำคู่สำนวน: Thank you → You're welcome / My pleasure | I'm sorry → Never mind / That's all right | Would you mind...? → Not at all (อนุญาต)",
        ],
    },
    weight=1.2,
)


@template("e.conv.polite", "easy")
def _polite_thanks_apology():
    n1, _ = name_en()
    n2, _ = name_en()
    while n2 == n1:
        n2, _ = name_en()
    scenarios = [
        (f"returning a borrowed {pick(['dictionary', 'calculator', 'umbrella', 'notebook', 'compass'])}",
         f"{n1}: Thanks a lot for lending me your {pick(['pen', 'book', 'ruler', 'jacket'])}. It really helped.\n{n2}: ____",
         "My pleasure. Anytime!",
         [W("Never mind.", "Never mind ใช้ตอบรับคำขอโทษ ไม่ใช่คำขอบคุณ", "context"),
          W("Yes, please.", "Yes, please ใช้ตอบรับข้อเสนอ ไม่ใช่คำขอบคุณ", "context"),
          W("Take it easy.", "Take it easy แปลว่า ใจเย็น ๆ ไม่เหมาะกับการตอบรับคำขอบคุณ", "meaning")],
         "ผู้พูดกล่าวขอบคุณ (Thanks a lot) ต้องตอบรับด้วยสำนวนที่แปลว่า 'ด้วยความยินดี'"),
        (f"accidentally bumping into someone at the {pick(['library', 'cafeteria', 'hallway', 'bookshop'])}",
         f"{n1}: Oh, I'm terribly sorry for stepping on your foot!\n{n2}: ____ I'm fine.",
         "That's all right.",
         [W("You're welcome.", "You're welcome ใช้ตอบรับคำขอบคุณ ไม่ใช่คำขอโทษ", "context"),
          W("My pleasure.", "My pleasure ใช้ตอบรับคำขอบคุณ", "context"),
          W("Same to you.", "Same to you ใช้ตอบคำอวยพร เช่น Have a nice day", "meaning")],
         "เมื่ออีกฝ่ายกล่าวขอโทษ (I'm terribly sorry) และเราไม่เป็นไร ควรตอบว่า 'ไม่เป็นไร'"),
        (f"helping carry heavy {pick(['boxes', 'books', 'project boards', 'sports bags'])}",
         f"{n1}: Your bag looks really heavy. Shall I carry it for you?\n{n2}: ____ That's very kind of you.",
         "Yes, please.",
         [W("No, thank you.", "ประโยคต่อมาชมว่าใจดีมาก แสดงว่าตอบรับความช่วยเหลือ ไม่ได้ปฏิเสธ", "context"),
          W("Never mind.", "Never mind ใช้ตอบคำขอโทษหรือบอกให้ช่างมัน", "meaning"),
          W("You're welcome.", "คนถูกเสนอช่วยต้องเป็นฝ่ายขอบคุณ ไม่ใช่พูด You're welcome", "trap")],
         "A เสนอความช่วยเหลือ (Shall I...?) และ B พูดต่อว่าใจดีมาก แปลว่า B ตอบรับ"),
        (f"wishing a friend good luck before a {pick(['math contest', 'piano recital', 'swimming race', 'science fair'])}",
         f"{n1}: I hope you have a great weekend with your family!\n{n2}: ____",
         "Thanks! Same to you.",
         [W("Don't mention it.", "Don't mention it ใช้ตอบรับเมื่อมีคนขอบคุณเรา", "context"),
          W("Never mind.", "Never mind แปลว่า ช่างมันเถอะ/ไม่เป็นไร", "meaning"),
          W("Excuse me.", "Excuse me ใช้ขอทางหรือเรียกความสนใจ", "context")],
         "เมื่อมีคนอวยพรให้มีวันหยุดที่ดี ควรกล่าวขอบคุณและอวยพรกลับ"),
        (f"spill water at the {pick(['canteen', 'art room', 'science lab', 'picnic table'])}",
         f"{n1}: I'm so sorry I spilled water on your worksheet.\n{n2}: ____ I have an extra copy in my folder.",
         "Never mind.",
         [W("With pleasure.", "With pleasure ใช้ตอบรับเมื่อเต็มใจทำสิ่งใดให้", "meaning"),
          W("Not at all.", "Not at all มักใช้ตอบรับคำขอบคุณ หรือตอบ Would you mind", "trap"),
          W("Bless you.", "Bless you ใช้พูดเมื่อมีคนจาม", "context")],
         "อีกฝ่ายมีชุดสำรองจึงไม่ถือโทษคำขอโทษ ใช้สำนวนที่แปลว่า 'ไม่เป็นไร'"),
    ]
    ctx, passage, ans, wrongs, exp = pick(scenarios)
    return mcq(
        stem=f"Choose the best response to complete the dialogue ({ctx}).",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ดูว่าประโยคแรกเป็นการขอบคุณ ขอโทษ เสนอความช่วยเหลือ หรืออวยพร",
        steps=[exp, f"คำตอบที่เหมาะสมที่สุดคือ \"{ans}\""],
    )


@template("e.conv.polite", "medium")
def _polite_would_you_mind():
    n1, _ = name_en()
    n2, _ = name_en()
    item = pick(["air conditioner", "electric fan", "overhead light", "projector", "radio"])
    place = pick(["classroom", "study room", "music room", "school bus", "waiting room"])
    cases = [
        (f"{n1}: Would you mind turning down the {item} a bit?\n{n2}: ____ I was just thinking it's too loud.",
         "Not at all.",
         [W("Yes, I would.", "Yes แปลว่ารังเกียจ/ไม่ทำให้ ซึ่งขัดกับประโยคหลังที่เห็นด้วยว่าดังเกินไป", "trap"),
          W("Yes, please.", "Would you mind ไม่ตอบด้วย Yes, please เพราะแปลว่ารังเกียจไหม", "concept"),
          W("Never mind.", "Never mind แปลว่าช่างเถอะ ไม่ใช้ตอบรับคำขอร้อง", "meaning")],
         "ประโยคหลังเห็นด้วยว่าเสียงดัง แปลว่ายินดีทำให้ (ไม่รังเกียจ = Not at all)"),
        (f"{n1}: Do you mind if I sit next to you in the {place}?\n{n2}: ____ Nobody is using this seat.",
         "Of course not. Go ahead.",
         [W("Yes, I do.", "Yes, I do แปลว่า ฉันรังเกียจ/ห้ามนั่ง ซึ่งขัดกับที่บอกว่าไม่มีคนนั่ง", "trap"),
          W("Yes, certainly.", "การใช้ Yes กับ Do you mind มีความหมายว่า 'รังเกียจ' จึงผิดหลักไวยากรณ์", "concept"),
          W("You're welcome.", "ยังไม่ทันได้ขอบคุณ จึงไม่ใช้ You're welcome", "context")],
         "ที่นั่งว่างอยู่ แสดงว่าอนุญาตให้นั่งได้ ตอบ Do you mind ต้องใช้รูปปฏิเสธ เช่น Of course not"),
        (f"{n1}: Would you mind lending me your {pick(['highlighter', 'stapler', 'dictionary', 'eraser'])} for a minute?\n{n2}: ____ I'm using it right now to finish my report.",
         "I'm sorry, I'm afraid I can't.",
         [W("Not at all. Here you are.", "ประโยคหลังบอกว่ากำลังใช้อยู่ จึงให้ยืมทันทีไม่ได้", "context"),
          W("No, go ahead.", "No, go ahead แปลว่าเชิญเอาไปเลย ขัดกับที่บอกว่ากำลังใช้อยู่", "context"),
          W("My pleasure.", "My pleasure แปลว่าด้วยความยินดี แต่บริบทคือปฏิเสธอย่างสุภาพ", "meaning")],
         "ประโยคหลังบอกว่ากำลังใช้งานอยู่ จึงต้องปฏิเสธอย่างสุภาพด้วย I'm sorry..."),
        (f"{n1}: Could you possibly hold the door for me? My hands are full.\n{n2}: ____ Come right in.",
         "Certainly!",
         [W("No, I couldn't.", "ประโยคหลังบอกให้เดินเข้ามาได้เลย แสดงว่าช่วยเปิดประตูให้", "context"),
          W("I'd rather not.", "I'd rather not เป็นการปฏิเสธ ขัดกับประโยคถัดไป", "meaning"),
          W("Mind your step.", "ไม่ตรงกับการตอบรับคำขอร้อง Could you...?", "context")],
         "Could you possibly...? แปลว่าช่วย...ได้ไหม เมื่อเต็มใจช่วยจึงตอบรับด้วย Certainly!"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the most polite and appropriate response.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ระวังโครงสร้าง Would/Do you mind...? ถ้าอนุญาตต้องตอบเชิงปฏิเสธว่า 'ไม่รังเกียจ'",
        steps=[exp, f"ดังนั้นคำตอบคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 2. Daily life: shopping, restaurant, clinic, travel, weather
# ---------------------------------------------------------------------------

skill(
    "e.conv.daily", "e.conv", "บทสนทนาในชีวิตประจำวัน (ร้านค้า ร้านอาหาร โรงพยาบาล)",
    lesson={
        "concept": "สถานการณ์ในชีวิตประจำวันมีสำนวนเฉพาะ เช่น พนักงานขายถามไซส์/วิธีชำระเงิน พนักงานเสิร์ฟรับออเดอร์ หรือแพทย์ถามอาการเจ็บป่วย",
        "steps": [
            "ระบุสถานที่และบทบาทของคู่สนทนา (เช่น Waiter–Customer, Doctor–Patient, Shopkeeper–Buyer)",
            "ดูคำตอบหรือคำถามข้างเคียงเพื่อหาคำถาม/คำตอบที่เข้าคู่กัน",
        ],
        "example": {
            "q": "Waiter: Are you ready to order?\nCustomer: ____",
            "steps": [
                "บริบทคือร้านอาหาร พนักงานถามว่าพร้อมสั่งอาหารหรือยัง",
                "ลูกค้าควรสั่งอาหาร เช่น I'd like grilled salmon, please. หรือขอเวลาเพิ่ม",
            ],
            "a": "Yes, I'll have the chicken soup, please.",
        },
        "mistakes": [
            "สับสนระหว่าง What does he look like? (ถามรูปร่างหน้าตา) กับ How is he feeling? (ถามอาการ)",
            "ใช้ How much กับคำนามพหูพจน์เมื่อถามจำนวนชิ้น หรือสับสนการถามราคา",
        ],
        "tips": [
            "สังเกตคำสำคัญ: receipt/fitting room = ร้านเสื้อผ้า, bill/menu = ร้านอาหาร, prescription/symptom = คลินิก",
        ],
    },
    weight=1.2,
)


@template("e.conv.daily", "easy")
def _daily_shop_food():
    n1, _ = name_en()
    garment = pick(["sweater", "jacket", "pair of sneakers", "school uniform shirt", "raincoat"])
    dish = pick(["spaghetti carbonara", "grilled fish", "fried rice with shrimp", "mushroom soup", "roast chicken"])
    cases = [
        (f"Shop assistant: Good afternoon. May I help you?\n{n1}: Yes, please. I'm looking for a {garment}. ____\nShop assistant: Sure! The fitting room is right over there.",
         "Can I try this one on?",
         [W("How much does it cost?", "พนักงานตอบเรื่องห้องลองชุด (fitting room) ไม่ได้บอกราคา", "context"),
          W("Do you accept credit cards?", "คำตอบของพนักงานพูดถึงห้องลองชุด ไม่ใช่การจ่ายเงิน", "context"),
          W("Can I have a refund?", "การขอคืนเงินไม่สอดคล้องกับการชี้ไปที่ห้องลองชุด", "meaning")],
         "พนักงานชี้ไปที่ห้องลองเสื้อ (fitting room) แสดงว่าลูกค้าขออนุญาตลองสวม (try on)"),
        (f"Waiter: Good evening. ____\n{n1}: Yes, I'd like a bowl of {dish} and a glass of lemon tea, please.",
         "May I take your order?",
         [W("Could I have the bill, please?", "นี่เป็นประโยคของลูกค้าที่ขอเช็คบิล ไม่ใช่พนักงานถาม", "trap"),
          W("How would you like to pay?", "ลูกค้าตอบเป็นรายการอาหาร ไม่ใช่วิธีชำระเงิน", "context"),
          W("Did you enjoy your meal?", "ลูกค้าเพิ่งจะสั่งอาหาร ยังไม่ได้รับประทานเสร็จ", "context")],
         "ลูกค้าตอบเป็นชื่ออาหารที่ต้องการสั่ง พนักงานจึงต้องถามเพื่อรับรายการอาหาร"),
        (f"Doctor: Hello, {n1}. ____\n{n1}: I've had a sore throat and a high fever since yesterday evening.",
         "What seems to be the trouble?",
         [W("What do you do for a living?", "ถามอาชีพ ไม่ได้ถามอาการป่วย", "meaning"),
          W("How long will you stay here?", "ไม่สอดคล้องกับการบอกอาการเจ็บคอและมีไข้", "context"),
          W("Where is the nearest pharmacy?", "หมอไม่ถามคนไข้ว่างานร้านขายยาอยู่ที่ไหน", "context")],
         "คนไข้เล่าอาการป่วย (เจ็บคอและมีไข้) แพทย์จึงต้องถามอาการด้วย What seems to be the trouble?"),
        (f"Cashier: That will be 450 baht in total. ____\n{n1}: By QR code scan, please.",
         "How would you like to pay?",
         [W("Would you like a plastic bag?", "ลูกค้าตอบเรื่องสแกนจ่ายเงิน ไม่ใช่เรื่องถุง", "context"),
          W("Do you have a member card?", "ต้องตอบ Yes/No ไม่ใช่ตอบว่าสแกน QR code", "context"),
          W("How many do you want?", "ถามจำนวนชิ้น แต่ลูกค้าตอบวิธีชำระเงิน", "meaning")],
         "ลูกค้าตอบวิธีการชำระเงิน (By QR code scan) แคชเชียร์จึงต้องถามว่าต้องการจ่ายเงินอย่างไร"),
        (f"{n1}: Excuse me, this {dish} is cold. ____\nWaiter: I'm terribly sorry. I'll heat it up for you right away.",
         "Could you warm it up for me, please?",
         [W("Can I have the menu, please?", "อาหารมาเสิร์ฟแล้วและพนักงานบอกว่าจะนำไปอุ่นให้", "context"),
          W("Keep the change, please.", "Keep the change แปลว่าไม่ต้องทอนเงิน ไม่เกี่ยวกับอาหารเย็นชืด", "meaning"),
          W("How would you like your steak?", "นี่เป็นคำถามของพนักงานเรื่องระดับความสุก", "trap")],
         "อาหารเย็นชืดและพนักงานรับปากว่าจะนำไปอุ่นให้ (heat it up) ลูกค้าจึงขอให้อุ่นอาหาร"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best expression to complete the conversation.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="อ่านประโยคถัดไปเพื่อดูว่าคู่สนทนาตอบเรื่องอะไร (ห้องลองชุด รายการอาหาร อาการป่วย หรือการจ่ายเงิน)",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.conv.daily", "hard")
def _daily_complex_service():
    n1, _ = name_en()
    place = pick(["Chiang Mai", "Phuket", "Khon Kaen", "Hua Hin", "Ayutthaya"])
    item = pick(["watch", "headphones", "blender", "desk lamp", "keyboard"])
    cases = [
        (f"Clerk: Welcome to City Bookshop. How can I help you?\n{n1}: I bought this {item} here yesterday, but it doesn't work properly. ____\nClerk: Certainly, if you have the receipt with you.",
         "Could I exchange it for a new one?",
         [W("May I try it on in the fitting room?", f"{item} ไม่ใช่เสื้อผ้าที่นำไปลองในห้องลองชุด และซื้อไปแล้วเมื่อวาน", "context"),
          W("How long does the warranty last?", "คำถาม How long ต้องตอบเป็นระยะเวลา ไม่ใช่ตอบ Certainly", "form"),
          W("Where did you buy it?", "ลูกค้าเป็นคนซื้อเอง จึงไม่ถามพนักงานว่าซื้อที่ไหน", "misread")],
         "สินค้าที่ซื้อไปเสียและพนักงานบอกได้ถ้ามีใบเสร็จ จึงเป็นการขอเปลี่ยนสินค้า (exchange)"),
        (f"Ticket officer: Good morning. Where are you travelling to?\n{n1}: One ticket to {place}, please.\nTicket officer: ____\n{n1}: Round-trip, please. I'm coming back this Sunday.",
         "Single or return?",
         [W("Window or aisle seat?", "ลูกค้าตอบว่าไป-กลับ (Round-trip) ไม่ได้เลือกที่นั่งริมหน้าต่างหรือทางเดิน", "context"),
          W("What time does the train leave?", "ผู้ขายตั๋วไม่ถามเวลารถออกกับผู้โดยสาร และคำตอบคือไป-กลับ", "context"),
          W("How many bags are you checking in?", "คำตอบไม่ใช่จำนวนกระเป๋า", "meaning")],
         "ลูกค้าตอบว่า Round-trip (ตั๋วไป-กลับ) พนักงานจึงถามว่าต้องการตั๋วเที่ยวเดียวหรือไป-กลับ (Single or return?)"),
        (f"Receptionist: Dental Clinic, good morning. How may I help you?\n{n1}: Hello. ____ with Dr. Somchai for this Saturday?\nReceptionist: Let me check his schedule. Is 10 a.m. convenient for you?",
         "I'd like to make an appointment",
         [W("I'd like to cancel my flight", "ที่นี่คือคลินิกทันตกรรม ไม่ใช่สายการบิน", "context"),
          W("Could you give me a prescription", "การขอใบสั่งยาไม่ใช้โครงสร้างคู่กับพนักงานต้อนรับเพื่อเช็คตารางนัด", "meaning"),
          W("Would you mind checking me out", "Check out ใช้กับโรงแรม ไม่ใช่การนัดหมอฟัน", "meaning")],
         "พนักงานเช็คตารางเวลาของคุณหมอในวันเสาร์ แสดงว่าผู้โทรต้องการนัดหมาย (make an appointment)"),
        (f"Customer: Excuse me, do you have these running shoes in a larger size? These are a bit tight.\nSalesperson: ____ Let me check the stockroom for you.",
         "I'll see if we have size 40 in stock.",
         [W("They fit you like a glove.", "Fit like a glove แปลว่าพอดีเป๊ะ ขัดกับที่ลูกค้าบอกว่าคับไป", "meaning"),
          W("We only accept cash today.", "ไม่เกี่ยวกับเรื่องไซส์รองเท้าที่ลูกค้าถาม", "context"),
          W("You look great in that colour.", "ลูกค้าบ่นว่าคับและขอไซส์ใหญ่ขึ้น ไม่ได้ถามเรื่องสี", "context")],
         "ลูกค้าขอไซส์ใหญ่ขึ้นและพนักงานบอกจะไปเช็คห้องเก็บของ จึงต้องตอบว่าจะดูให้ว่ามีไซส์ในสต็อกไหม"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best expression to complete the dialogue.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="จับคำสำคัญของคำตอบถัดไป เช่น receipt, Round-trip, schedule, stockroom",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 3. School & Classroom life
# ---------------------------------------------------------------------------

skill(
    "e.conv.school", "e.conv", "บทสนทนาในโรงเรียนและห้องเรียน",
    lesson={
        "concept": "บทสนทนาในโรงเรียนเกี่ยวข้องกับการเรียน การบ้าน การทำงานกลุ่ม กฎระเบียบของห้องเรียน และการถามความหมายหรือการสะกดคำ",
        "steps": [
            "ดูว่าเป็นการคุยระหว่างครูกับนักเรียน หรือระหว่างเพื่อนนักเรียนด้วยกัน",
            "สังเกตคำถามเฉพาะในห้องเรียน เช่น How do you spell...? / What does ... mean? / When is the report due?",
        ],
        "example": {
            "q": "Student: Excuse me, Ms. Clara. ____\nTeacher: It's due next Monday.",
            "steps": [
                "ครูตอบว่า It's due next Monday (กำหนดส่งวันจันทร์หน้า)",
                "นักเรียนจึงต้องถามกำหนดส่งงาน",
            ],
            "a": "When do we have to hand in the science project?",
        },
        "mistakes": [
            "สับสนสำนวน hand in (ส่งงาน) กับ hand out (แจกเอกสาร)",
            "ใช้คำพูดไม่สุภาพเมื่อพูดกับครูผู้สอน",
        ],
        "tips": [
            "คำศัพท์ในห้องเรียนที่ออกบ่อย: hand in / turn in (ส่งงาน), due date (กำหนดส่ง), absent (ขาดเรียน), look up (ค้นคำศัพท์)",
        ],
    },
    weight=1.1,
)


@template("e.conv.school", "easy")
def _school_classroom_basics():
    n1, _ = name_en()
    subj = pick(["science", "history", "English", "geography", "mathematics"])
    word = pick(["environment", "magnificent", "photosynthesis", "temperature", "archipelago"])
    cases = [
        (f"{n1}: Excuse me, Mr. Wilson. ____\nTeacher: Sure. It means 'very large or impressive'.",
         f"What does '{word}' mean?",
         [W(f"How do you pronounce '{word}'?", "ครูตอบเป็นความหมาย (It means...) ไม่ได้สอนออกเสียง", "context"),
          W(f"Can you spell '{word}' for me?", "ครูไม่ได้สะกดตัวอักษรทีละตัว", "context"),
          W("Which page are we on?", "ครูอธิบายความหมายของคำศัพท์ ไม่ได้บอกเลขหน้า", "meaning")],
         "ครูตอบด้วย It means... (มันแปลว่า...) นักเรียนจึงต้องถามความหมายของคำศัพท์"),
        (f"Teacher: Please pass these worksheets to the back, {n1}.\n{n1}: ____ Oh, there seems to be one copy missing.",
         "Here you go, everyone.",
         [W("I forgot to do my homework.", "ครูให้ช่วยแจกใบงาน ไม่ได้ทวงการบ้าน", "context"),
          W("May I go to the restroom?", "ไม่สอดคล้องกับการรับใบงานมาแจกแล้วนับขาดไป 1 แผ่น", "context"),
          W("Congratulations on your score!", "บริบทคือการแจกใบงานในห้องเรียน", "meaning")],
         f"ครูให้ {n1} แจกใบงานไปด้านหลัง แล้วพบว่าขาดไป 1 แผ่น จึงเป็นคำพูดขณะส่งใบงานให้เพื่อน"),
        (f"{n1}: Why weren't you in {subj} class yesterday?\nFriend: ____ I had to see the dentist.",
         "I was absent because I had a bad toothache.",
         [W("I got full marks on the quiz.", "เพื่อนถามว่าทำไมเมื่อวานไม่มาเรียน ไม่ได้ถามคะแนนสอบ", "misread"),
          W("The class was really exciting.", "คนตอบไม่ได้เข้าเรียนเมื่อวาน کیونکہไปหาหมอฟัน", "context"),
          W("I've already handed it in.", "คำถามถามสาเหตุที่ขาดเรียน (Why weren't you...)", "context")],
         "เพื่อนถามสาเหตุที่ไม่มาเรียนเมื่อวาน และประโยคท้ายบอกว่าต้องไปหาหมอฟัน"),
        (f"Student: I'm sorry I'm late, Mrs. Davis. The traffic was terrible.\nTeacher: ____ Please take your seat quietly; we've just started.",
         "That's okay this time.",
         [W("You're welcome.", "นักเรียนกล่าวขอโทษที่มาสาย ไม่ได้กล่าวขอบคุณ", "context"),
          W("Keep up the good work!", "มาสายไม่ใช่เรื่องที่ควรชมเชยว่าทำดีมาก", "meaning"),
          W("See you tomorrow.", "เพิ่งเริ่มคาบเรียนและครูบอกให้นั่งลง", "context")],
         "นักเรียนขอโทษที่มาสายและครูบอกให้นั่งลงเงียบ ๆ แสดงว่าครูให้อภัยในครั้งนี้"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best expression to complete the classroom dialogue.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ดูความเชื่อมโยงระหว่างคำถามของนักเรียนกับคำตอบของครูหรือเพื่อน",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.conv.school", "medium")
def _school_projects_deadlines():
    n1, _ = name_en()
    n2, _ = name_en()
    while n2 == n1:
        n2, _ = name_en()
    subj = pick(["biology", "social studies", "literature", "art", "physics"])
    day = pick(["Wednesday", "Thursday", "Friday", "next Monday"])
    cases = [
        (f"{n1}: Have you finished the {subj} report yet?\n{n2}: Not yet. ____\n{n1}: No, the teacher extended it to {day}.",
         "Isn't it due tomorrow?",
         [W("When did you hand it in?", f"{n1} ตอบว่าNo และบอกว่าครูเลื่อนกำหนดส่งเป็น {day} จึงต้องเป็นคำถามเช็คกำหนดส่ง", "context"),
          W("Who is in your project group?", "คำตอบพูดถึงวันกำหนดส่ง ไม่ใช่รายชื่อสมาชิกกลุ่ม", "meaning"),
          W("How many pages did you write?", "คำตอบขึ้นต้นด้วย No และบอกวันส่งงาน", "form")],
         f"{n1} ตอบว่า 'ไม่นะ ครูขยายเวลาไปเป็น {day}' แสดงว่า {n2} เข้าใจว่าต้องส่งพรุ่งนี้"),
        (f"{n1}: The math exam is coming up next week. I still don't understand fractions.\n{n2}: ____ We can review the exercises together at the library after school.",
         "Don't worry. I can help you go over them.",
         [W("You should give up now.", "การบอกให้ยอมแพ้ไม่สอดคล้องกับการชวนไปติวด้วยกันที่ห้องสมุด", "context"),
          W("I have no idea where the library is.", "ตัวเองเป็นคนชวนไปห้องสมุดหลังเลิกเรียน", "context"),
          W("Good luck with your music lesson.", "กำลังคุยเรื่องสอบคณิตศาสตร์ ไม่ใช่เรียนดนตรี", "meaning")],
         f"{n2} ชวนไปทบทวนแบบฝึกหัดด้วยกันหลังเลิกเรียน จึงต้องพูดให้กำลังใจและเสนอช่วยติว"),
        (f"{n1}: Excuse me, is anyone sitting here?\n{n2}: ____ My friend went to get a tray of food and will be right back.",
         "Sorry, this seat is taken.",
         [W("No, please help yourself.", "ถ้าตอบว่าไม่มีคนนั่ง จะขัดกับประโยคหลังที่บอกว่าเพื่อนไปเอาถาดอาหารเดี๋ยวกลับมา", "trap"),
          W("Not at all, go ahead.", "เก้าอี้มีเพื่อนจองไว้แล้ว จึงอนุญาตให้นั่งไม่ได้", "context"),
          W("Yes, I'm leaving now.", "บอกว่าเพื่อนกำลังจะกลับมา ไม่ใช่กำลังจะลุกไป", "meaning")],
         "ประโยคหลังบอกว่าเพื่อนไปเอาอาหารและกำลังจะกลับมา แสดงว่าที่นั่งนี้มีคนนั่งแล้ว (is taken)"),
        (f"{n1}: How did you do on the {subj} quiz this morning?\n{n2}: ____ I studied the wrong chapter last night!",
         "I didn't do very well.",
         [W("It was a piece of cake!", "A piece of cake แปลว่าง่ายมาก ขัดกับที่บ่นว่าอ่านผิดบท", "meaning"),
          W("I couldn't agree more.", "ใช้แสดงความเห็นด้วย ไม่ใช่ตอบผลสอบของตัวเอง", "context"),
          W("I passed with flying colours!", "Pass with flying colours แปลว่าสอบผ่านได้คะแนนดีเยี่ยม ขัดกับที่อ่านผิดบท", "meaning")],
         "ประโยคหลังบอกว่าเมื่อคืนอ่านหนังสือผิดบท แสดงว่าทำข้อสอบได้ไม่ดี"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best expression to complete the school conversation.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="อ่านประโยคหลังช่องว่างให้ดี เพราะเป็นเหตุผลหรือผลลัพธ์ของประโยคในช่องว่าง",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 4. Opinions, suggestions, agreement, invitations
# ---------------------------------------------------------------------------

skill(
    "e.conv.opinion", "e.conv", "การแสดงความคิดเห็น การชักชวน และการเห็นด้วย/ไม่เห็นด้วย",
    lesson={
        "concept": "การเสนอแนะใช้ Why don't we... / How about + V-ing / Let's + V1 ส่วนการแสดงความเห็นด้วยอย่างยิ่งใช้ I couldn't agree more หรือ You can say that again",
        "steps": [
            "ดูว่าผู้พูดกำลังขอความเห็น (What do you think of...?) หรือชักชวน (Why don't we...?)",
            "ระวังสำนวนที่มีรูปปฏิเสธแต่แปลว่าเห็นด้วยอย่างยิ่ง เช่น I couldn't agree more",
        ],
        "example": {
            "q": "A: The new science museum is really fascinating.\nB: ____. I spent four hours there yesterday!",
            "steps": [
                "B บอกว่าใช้เวลาอยู่ที่นั่นถึง 4 ชั่วโมง แสดงว่าชอบมากและเห็นด้วยกับ A",
                "เลือกสำนวนที่แปลว่า 'เห็นด้วยอย่างยิ่ง'",
            ],
            "a": "I couldn't agree more",
        },
        "mistakes": [
            "แปล I couldn't agree more ว่า 'ไม่เห็นด้วย' ทั้งที่จริงแปลว่า 'เห็นด้วยที่สุด (ไม่สามารถเห็นด้วยไปมากกว่านี้ได้อีกแล้ว)'",
            "ตอบรับคำชวนแต่ประโยคถัดมากลับบอกเหตุผลที่ไปไม่ได้ (หรือในทางกลับกัน)",
        ],
        "tips": [
            "I couldn't agree more = I totally agree (เห็นด้วยอย่างยิ่ง) | I'm afraid I have to take a rain check = ขอเลื่อนไปโอกาสหน้า",
        ],
    },
    weight=1.2,
)


@template("e.conv.opinion", "medium")
def _opinion_invitations_suggestions():
    n1, _ = name_en()
    n2, _ = name_en()
    while n2 == n1:
        n2, _ = name_en()
    act = pick(["play badminton", "visit the book fair", "watch the new animated movie", "ride bicycles in the park", "bake chocolate cookies"])
    excuse = pick(["help my mum clean the house", "visit my grandparents", "prepare for my piano lesson", "finish my science model", "babysit my little brother"])
    cases = [
        (f"{n1}: Are you free this Saturday afternoon? Why don't we {act}?\n{n2}: ____ I have to {excuse}.",
         "I'd love to, but I can't.",
         [W("That sounds like a great plan! Let's go.", f"ประโยคหลังติดธุระต้อง {excuse} จึงตอบตกลงไปไม่ได้", "context"),
          W("Count me in!", "Count me in แปลว่า ขอร่วมด้วยคน ซึ่งขัดกับเหตุผลที่ติดธุระ", "meaning"),
          W("Yes, I'm completely free.", "ขัดแย้งกับประโยคหลังที่บอกว่าต้องไปทำธุระอื่น", "context")],
         f"ประโยคหลังบอกเหตุผลที่ไปไม่ได้ (I have to {excuse}) จึงต้องปฏิเสธคำชวนอย่างสุภาพ"),
        (f"{n1}: It's scorching hot today! ____\n{n2}: Good idea! Strawberry is my favourite flavour.",
         "How about getting some ice cream?",
         [W("Why don't we go jogging in the sun?", "ประโยคตอบพูดถึงรสสตรอว์เบอร์รี จึงต้องชวนกินไอศกรีม ไม่ใช่ไปวิ่ง", "context"),
          W("Shall we turn on the heater?", "อากาศร้อนจัด (scorching hot) ไม่ควรเปิดฮีตเตอร์", "meaning"),
          W("Do you like hot coffee?", "รสสตรอว์เบอร์รีไม่เข้ากับกาแฟร้อนในวันที่อากาศร้อนจัด", "context")],
         "B เห็นด้วยและบอกว่าชอบรสสตรอว์เบอร์รีมากที่สุด A จึงต้องชวนไปกินไอศกรีม"),
        (f"{n1}: What do you think of our new English club project?\n{n2}: ____ It helps us practise speaking in real situations.",
         "I think it's really useful.",
         [W("It's a total waste of time.", "ประโยคหลังชมว่าช่วยฝึกพูดในสถานการณ์จริง จึงต้องเป็นความเห็นเชิงบวก", "context"),
          W("I have no idea what it is.", "สามารถอธิบายประโยชน์ได้ชัดเจน แสดงว่ารู้จักโปรเจกต์นี้ดี", "context"),
          W("Yes, I do.", "คำถามขึ้นต้นด้วย What do you think... ไม่ตอบด้วย Yes/No", "form")],
         "ประโยคหลังอธิบายข้อดีของโปรเจกต์ จึงต้องแสดงความคิดเห็นในเชิงบวก"),
        (f"{n1}: What shall we buy for {pick(['Mintra', 'Pakin', 'Kwan', 'Tonkla'])}'s birthday?\n{n2}: ____ She loves painting and sketching.",
         "What about a set of watercolour paints?",
         [W("Let's buy her a pair of football boots.", "ประโยคหลังบอกว่าเธอชอบวาดภาพและระบายสี", "context"),
          W("When is her birthday party?", "ไม่ได้ตอบข้อเสนอแนะเรื่องของขวัญ และประโยคหลังพูดถึงการวาดภาพ", "context"),
          W("Happy birthday to her!", "เพื่อนถามว่าจะซื้ออะไรให้ดี ไม่ได้ให้กล่าวอวยพรตอนนี้", "meaning")],
         "ประโยคหลังให้เหตุผลว่าเธอชอบวาดภาพและระบายสี จึงควรเสนอซื้อชุดสีน้ำ"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best expression to complete the dialogue.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ดูว่าประโยคถัดไปเป็นการตอบรับ ปฏิเสธเพราะติดธุระ หรือบอกเหตุผลสนับสนุนข้อเสนอ",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.conv.opinion", "challenge")
def _opinion_idiomatic_agreement():
    n1, _ = name_en()
    n2, _ = name_en()
    while n2 == n1:
        n2, _ = name_en()
    topic_str = pick([
        ("The documentary about deep-sea creatures was truly eye-opening.", "The photography was breathtaking too."),
        ("Cutting down on single-use plastic is essential for our planet.", "Everyone should bring their own cloth bag."),
        ("Practising past exam papers is the best way to improve our speed.", "It really helps us spot common traps."),
        ("Public libraries are wonderful places for students during the holidays.", "They're quiet, cool, and full of great books."),
    ])
    s1, s2 = topic_str
    mode = random.randint(1, 3)
    if mode == 1:
        passage = f"{n1}: {s1}\n{n2}: ____ {s2}"
        ans = pick(["I couldn't agree more.", "You can say that again!", "That's exactly how I feel."])
        wrongs = [
            W("I beg to differ.", "I beg to differ แปลว่า ฉันขอเห็นต่าง ซึ่งขัดกับประโยคหลังที่พูดสนับสนุน", "meaning"),
            W("That's out of the question.", "Out of the question แปลว่า เป็นไปไม่ได้เลย/ไม่อนุญาต", "meaning"),
            W("Don't count on it.", "Don't count on it แปลว่า อย่าไปหวังพึ่งเรื่องนั้นเลย", "meaning"),
        ]
        exp = "ประโยคหลังของ B พูดเสริมในทิศทางเดียวกัน แสดงว่าเห็นด้วยอย่างยิ่ง (I couldn't agree more / You can say that again)"
    elif mode == 2:
        act = pick(["going bowling this evening", "joining the board-game session today", "watching the basketball final after school", "trying that new ramen shop tonight"])
        passage = f"{n1}: Do you fancy {act}?\n{n2}: I'm swamped with homework tonight, so ____. Maybe this weekend?"
        ans = "I'll have to take a rain check"
        wrongs = [
            W("I'm all ears", "I'm all ears แปลว่า ฉันพร้อมตั้งใจฟังแล้ว ไม่เกี่ยวกับการขอเลื่อนนัด", "meaning"),
            W("it's a piece of cake", "A piece of cake แปลว่า เรื่องกล้วย ๆ ไม่เข้ากับบริบทที่การบ้านท่วมหัว", "meaning"),
            W("you can count me in", "Count me in แปลว่า ขอไปด้วยคน แต่ B ติดการบ้านและขอเลื่อนเป็นสุดสัปดาห์", "trap"),
        ]
        exp = "สำนวน take a rain check หมายถึง ขอติดไว้ก่อนแล้วค่อยไปโอกาสหน้า (สังเกตจาก Maybe this weekend?)"
    else:
        passage = f"{n1}: Do you think the school should cancel all sports classes to give us more test prep time?\n{n2}: ____ Exercise actually helps our brains stay sharp and reduces stress."
        ans = "I'm afraid I don't see it that way."
        wrongs = [
            W("I couldn't agree more.", "ประโยคหลังแย้งว่าการออกกำลังกายช่วยให้สมองปลอดโปร่ง จึงไม่เห็นด้วยกับการยกเลิกวิชาพละ", "trap"),
            W("You took the words right out of my mouth.", "แปลว่า พูดตรงใจฉันเป๊ะ (เห็นด้วย) ซึ่งขัดกับเหตุผลประโยคหลัง", "meaning"),
            W("By all means.", "By all means แปลว่า ได้เลยอย่างแน่นอน", "meaning"),
        ]
        exp = "ประโยคหลังให้เหตุผลคัดค้าน (บอกว่าการออกกำลังกายมีประโยชน์ต่อสมอง) จึงต้องใช้สำนวนไม่เห็นด้วยอย่างสุภาพ"
    return mcq(
        stem="Choose the most idiomatic and appropriate expression to complete the conversation.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="สังเกตสำนวนภาษาอังกฤษ: I couldn't agree more (เห็นด้วยที่สุด), take a rain check (ขอเลื่อนนัด), I don't see it that way (ไม่เห็นด้วย)",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 5. Phone calls & Asking/Giving directions
# ---------------------------------------------------------------------------

skill(
    "e.conv.phone_direction", "e.conv", "การคุยโทรศัพท์และการถาม-บอกทาง",
    lesson={
        "concept": "การโทรศัพท์ใช้ This is... (แนะนำตัว), May I speak to...?, Hold on (ถือสายรอ), Leave a message (ฝากข้อความ) ส่วนการถามทางใช้ How can I get to...? / How far is it?",
        "steps": [
            "ในการคุยโทรศัพท์ ภาษาอังกฤษใช้ This is [ชื่อ] speaking และ Who's calling, please?",
            "ในการถามทาง ให้ดูคำตอบว่าเป็นทิศทาง (Go straight, turn left) หรือระยะเวลา/ระยะทาง (Ten minutes' walk)",
        ],
        "example": {
            "q": "Caller: Hello, may I speak to Mr. Parker, please?\nReceptionist: ____ He's in a meeting right now.",
            "steps": [
                "พนักงานบอกว่าเขากำลังประชุมอยู่ แสดงว่าพูดสายไม่ได้ในตอนนี้",
                "ต้องบอกให้ฝากข้อความไว้ หรือบอกว่าไม่อยู่รับสาย",
            ],
            "a": "I'm sorry, he's not available at the moment. Would you like to leave a message?",
        },
        "mistakes": [
            "ใช้ I am [ชื่อ] แทน This is [ชื่อ] เวลาแนะนำตัวทางโทรศัพท์ที่เป็นทางการ",
            "สับสนระหว่าง take a message (รับฝากข้อความ—ฝ่ายคนรับสายพูด) กับ leave a message (ฝากข้อความไว้—ฝ่ายคนโทรพูด)",
        ],
        "tips": [
            "คนโทร = leave a message | คนรับสาย = take a message | Hold on / Hang on = ถือสายรอสักครู่",
        ],
    },
    weight=1.1,
)


@template("e.conv.phone_direction", "medium")
def _phone_conversations():
    n1, _ = name_en()
    n2, p2 = name_en()
    while n2 == n1:
        n2, p2 = name_en()
    place = pick(["the shower", "the garden", "a staff meeting", "the kitchen", "the library"])
    cases = [
        (f"{n1}: Hello, may I speak to {n2}, please?\nParent: I'm sorry, {p2}'s in {place} right now. ____\n{n1}: Yes, please tell {n2} to call me back at 5 p.m.",
         "Can I take a message?",
         [W("Would you like to take a message?", "ผู้รับสายต้องเป็นฝ่ายรับฝากข้อความ (Can I take a message? หรือ Would you like to leave a message?)", "trap"),
          W("Who are you?", "ไม่สุภาพในการรับโทรศัพท์ ควรใช้ Who's calling, please?", "form"),
          W("Please hang up now.", "ผู้โทรตอบรับว่าขอฝากข้อความไว้ ไม่ได้ถูกสั่งให้วางสาย", "context")],
         "ผู้รับสายถามผู้โทรว่าต้องการฝากข้อความไหม ใช้ Can I take a message? (หรือ Would you like to leave a message?)"),
        (f"Receptionist: Sunrise Learning Centre. How may I direct your call?\n{n1}: Hello, could you put me through to Ms. Adams, please?\nReceptionist: ____ I'll connect you now.",
         "Hold the line, please.",
         [W("You have the wrong number.", "ประโยคหลังบอกว่าจะโอนสายให้เดี๋ยวนี้ (connect you now) จึงไม่ใช่โทรผิดเบอร์", "context"),
          W("The line is busy.", "ถ้าสายไม่ว่างจะโอนสายให้ทันทีไม่ได้", "context"),
          W("She has already left for the day.", "ขัดแย้งกับประโยคหลังที่กำลังโอนสายให้", "context")],
         "พนักงานกำลังจะโอนสายให้ (connect you now) จึงขอให้ถือสายรอสักครู่ (Hold the line, please)"),
        (f"{n1}: Hello, is that the City Sports Club?\nSpeaker: ____ This is a private residence.\n{n1}: Oh, I'm sorry to have bothered you.",
         "I'm afraid you have the wrong number.",
         [W("Speaking. How can I help you?", "ประโยคหลังบอกว่าเป็นบ้านพักส่วนตัว ไม่ใช่สโมสรกีฬา", "context"),
          W("Please hold on a moment.", "โทรผิดเบอร์จึงไม่ต้องถือสายรอ", "context"),
          W("May I ask who is calling?", "ผู้รับปฏิเสธว่าไม่ใช่สโมสรกีฬาและผู้โทรกล่าวขอโทษที่รบกวน", "context")],
         "ผู้รับบอกว่าที่นี่เป็นบ้านส่วนตัวและผู้โทรขอโทษ แสดงว่าโทรผิดหมายเลข (wrong number)"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best expression to complete the telephone conversation.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ทบทวนสำนวนโทรศัพท์: take a message (รับข้อความ), hold the line (ถือสายรอ), wrong number (โทรผิดเบอร์)",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.conv.phone_direction", "hard")
def _asking_directions():
    n1, _ = name_en()
    dest = pick(["Central Post Office", "National Science Museum", "Botanical Garden", "City Public Library", "Main Train Station"])
    landmark = pick(["traffic lights", "pedestrian bridge", "city bank", "roundabout", "clock tower"])
    mins = random.randint(5, 15)
    cases = [
        (f"{n1}: Excuse me, ____\nPasser-by: Go straight along this street for two blocks and turn left at the {landmark}. It's on your right.",
         f"could you tell me how to get to the {dest}?",
         [W(f"how far is the {dest} from here?", "คำตอบบอกเส้นทางละเอียด (ตรงไป เลี้ยวซ้าย) ไม่ได้บอกระยะทาง", "context"),
          W(f"what time does the {dest} open?", "คำตอบเป็นการบอกทาง ไม่ใช่เวลาเปิดทำการ", "context"),
          W(f"have you ever been to the {dest}?", "เป็น Yes/No question ไม่ตรงกับคำตอบที่อธิบายเส้นทาง", "form")],
         "ผู้ตอบอธิบายเส้นทางเดินไปอย่างละเอียด คำถามจึงต้องเป็นการถามทาง (how to get to...)"),
        (f"{n1}: Excuse me, is the {dest} within walking distance?\nPasser-by: Yes, it's quite close. ____\n{n1}: Great, I'll walk there then. Thank you!",
         f"It takes only about {mins} minutes on foot.",
         [W("You should definitely take a taxi.", "ขัดกับที่บอกว่าใกล้มาก (quite close) และผู้ถามตัดสินใจเดินไป", "context"),
          W("I'm a stranger here myself.", "ถ้าเป็นคนแปลกหน้าในพื้นที่นี้จะตอบไม่ได้ว่าอยู่ใกล้แค่ไหน", "context"),
          W("It's twenty kilometres away.", "20 กิโลเมตรไกลเกินกว่าจะบอกว่าใกล้และเดินไปได้ง่าย", "meaning")],
         f"ผู้ตอบบอกว่าอยู่ใกล้มากและ {n1} ตอบว่าจะเดินไป จึงเป็นการบอกเวลาเดินเท้าประมาณ {mins} นาที"),
        (f"Tourist: Excuse me, do you know where the nearest underground station is?\n{n1}: ____ I just moved to this neighbourhood yesterday.\nTourist: That's okay. I'll ask someone else.",
         "I'm sorry, I'm not familiar with this area.",
         [W("Go straight and take the second turning on the right.", "ประโยคหลังบอกว่าเพิ่งย้ายมาเมื่อวานและนักท่องเที่ยวบอกว่าจะไปถามคนอื่นแทน", "context"),
          W("You can't miss it!", "You can't miss it ใช้เมื่อบอกทางแล้วหาเจอง่ายมาก แต่ในที่นี้ผู้พูดไม่รู้ทาง", "meaning"),
          W("Follow me, I'm going there too.", "ขัดแย้งกับที่นักท่องเที่ยวบอกว่าจะไปถามคนอื่น", "context")],
         "ผู้พูดเพิ่งย้ายมาเมื่อวานและนักท่องเที่ยวจะไปถามคนอื่น แสดงว่าผู้พูดไม่คุ้นเคยกับย่านนี้"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best expression to complete the dialogue about directions.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="สังเกตความสัมพันธ์ระหว่างคำถามและคำตอบเรื่องเส้นทาง ระยะเวลาเดิน หรือการไม่รู้ทาง",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 6. Multi-turn & two-blank situational dialogues
# ---------------------------------------------------------------------------

skill(
    "e.conv.dialogue", "e.conv", "การเติมบทสนทนาต่อเนื่องหลายประโยค",
    lesson={
        "concept": "ข้อสอบเข้า ม.1 มักให้บทสนทนายาว 3–5 บรรทัด หรือเว้นว่าง 2 จุด ต้องอ่านทั้งบทสนทนาเพื่อจับอารมณ์ น้ำเสียง และความต่อเนื่องของเนื้อเรื่อง",
        "steps": [
            "อ่านบทสนทนาตั้งแต่ต้นจนจบก่อนดูตัวเลือก เพื่อเข้าใจสถานการณ์รวม",
            "ดูคำสรรพนาม คำเชื่อม และประโยคก่อน-หลังช่องว่างทุกจุด",
            "ตัดตัวเลือกที่ขัดแย้งกับบริบทแม้เพียงจุดเดียวออกทันที",
        ],
        "example": {
            "q": "A: You look pale. Are you okay?\nB: ____. I skipped breakfast this morning.\nA: Here, have this granola bar.",
            "steps": [
                "A ทักว่าหน้าซีด และ B บอกว่าไม่ได้กินมื้อเช้ามา",
                "ช่องว่างต้องบอกอาการที่เกิดจากการไม่ได้กินข้าว เช่น เวียนหัวหรือหิว",
            ],
            "a": "I feel a bit dizzy",
        },
        "mistakes": [
            "อ่านเฉพาะบรรทัดที่มีช่องว่างโดยไม่อ่านประโยคถัดไป ทำให้เลือกคำตอบที่ขัดกับตอนจบของบทสนทนา",
        ],
        "tips": [
            "ถ้ามี 2 ช่องว่าง ให้เช็คช่องว่างที่ชัดเจนที่สุดก่อน จะช่วยตัดตัวเลือกได้ถึง 2–3 ข้อทันที",
        ],
    },
    weight=1.3,
)


@template("e.conv.dialogue", "hard")
def _dialogue_multi_turn():
    n1, _ = name_en()
    n2, _ = name_en()
    while n2 == n1:
        n2, _ = name_en()
    lost_item = pick(["wallet", "student ID card", "scientific calculator", "locker key", "bus pass"])
    spot = pick(["gymnasium", "science lab", "art studio", "bicycle shed", "computer room"])
    cases = [
        (f"{n1}: You look worried, {n2}. What's the matter?\n"
         f"{n2}: I can't find my {lost_item} anywhere!\n"
         f"{n1}: Calm down. ____\n"
         f"{n2}: Let me think... I definitely had it when we were in the {spot}.\n"
         f"{n1}: Let's go back there and check right now.",
         "Where did you last use it?",
         [W("Why did you buy a new one?", f"{n2} กำลังนึกย้อนว่าใช้ครั้งสุดท้ายที่ {spot} ไม่ได้ซื้อใหม่", "context"),
          W("Whose calculator is this?", f"คำตอบของ {n2} คือการนึกถึงสถานที่ที่อยู่ก่อนหน้านี้", "context"),
          W("How much money was inside?", f"คำตอบของ {n2} ระบุสถานที่ ({spot}) ไม่ใช่จำนวนเงิน", "meaning")],
         f"{n2} ตอบโดยนึกย้อนถึงสถานที่ ({spot}) ดังนั้น {n1} จึงต้องถามว่าเห็นหรือใช้ครั้งสุดท้ายที่ไหน"),
        (f"{n1}: Guess what! My short story won first prize in the regional writing contest!\n"
         f"{n2}: ____ I knew all your hard work would pay off.\n"
         f"{n1}: Thanks! Ms. Carter helped me edit the final draft too.\n"
         f"{n2}: We should celebrate after school today!",
         "Congratulations! That's fantastic news!",
         [W("Better luck next time!", "ใช้ปลอบใจเมื่อแพ้หรือสอบตก แต่เพื่อนชนะรางวัลที่ 1", "meaning"),
          W("What a pity!", "What a pity แปลว่า น่าเสียดายจัง ใช้กับข่าวร้าย", "meaning"),
          W("I'm sorry to hear that.", "ใช้แสดงความเสียใจกับข่าวร้าย ไม่ใช่การชนะรางวัล", "context")],
         f"{n1} บอกข่าวดีว่าชนะรางวัลที่ 1 {n2} จึงต้องกล่าวแสดงความยินดี (Congratulations!)"),
        (f"{n1}: Look at those dark clouds gathering over the field.\n"
         f"{n2}: Oh no, ____ and I forgot to bring my umbrella.\n"
         f"{n1}: Don't worry. Mine is big enough for both of us.\n"
         f"{n2}: Thanks, {n1}! You're a lifesaver.",
         "it looks like it's going to pour",
         [W("the weather is clearing up nicely", "ขัดกับเมฆดำมืดและความกังวลที่ลืมเอาร่มมา", "context"),
          W("it's a lovely sunny afternoon", "เมฆดำครึ้มและต้องใช้ร่มด้วยกัน จึงไม่ใช่วันแดดจ้า", "meaning"),
          W("I love playing in the snow", "บริบทพูดถึงเมฆฝนและร่ม", "context")],
         "เห็นเมฆดำและกังวลเรื่องลืมร่ม แสดงว่าฝนกำลังจะตกหนัก (going to pour)"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Read the dialogue carefully and choose the best expression for the blank.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ดูทั้งประโยคก่อนหน้าและประโยคถัดไปเพื่อให้บทสนทนาไหลลื่นสมเหตุสมผล",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.conv.dialogue", "challenge")
def _dialogue_two_blanks():
    n1, _ = name_en()
    n2, _ = name_en()
    while n2 == n1:
        n2, _ = name_en()
    club = pick(["Robotics Club", "Debate Society", "School Orchestra", "Astronomy Club", "Young Reporters Club"])
    day = pick(["Tuesdays", "Wednesdays", "Thursdays"])
    cases = [
        (f"{n1}: Are you planning to join the {club} this semester?\n"
         f"{n2}: __(1)__ I'm really interested in it, but I'm not sure when they meet.\n"
         f"{n1}: They practise on {day} after school. __(2)__\n"
         f"{n2}: Yes, let's go sign up at the noticeboard together!",
         "(1) I'm thinking about it. / (2) Why don't we join together?",
         [W("(1) No way! / (2) You shouldn't go there.", "ประโยคต่อมาบอกว่าสนใจมาก และตอนจบชวนกันไปสมัคร", "context"),
          W("(1) I've already quit. / (2) When does it start?", "ขัดกับเนื้อเรื่องที่กำลังตัดสินใจจะสมัครชมรม", "context"),
          W("(1) I'm thinking about it. / (2) It's already full.", "ถ้าชมรมเต็มแล้ว ตอนจบจะชวนกันไปลงชื่อสมัครไม่ได้", "trap")],
         "ช่อง (1) กำลังคิดอยู่เพราะสนใจแต่ยังไม่รู้เวลา ช่อง (2) ชวนไปสมัครด้วยกันซึ่งสอดคล้องกับ Yes, let's go sign up"),
        (f"{n1}: Excuse me, is this the queue for the planetarium show?\n"
         f"{n2}: __(1)__ This line is for the 3D Dinosaur Exhibition.\n"
         f"{n1}: Oh, I see. Do you happen to know where the planetarium entrance is?\n"
         f"{n2}: __(2)__ Just follow the blue signs past the gift shop.",
         "(1) No, I'm afraid not. / (2) It's on the second floor.",
         [W("(1) Yes, it is. / (2) I have no idea.", "ประโยคต่อมาบอกว่าแถวนี้คือแถวนิทรรศการไดโนเสาร์ และตอนท้ายบอกทางได้ละเอียด", "context"),
          W("(1) No, I'm afraid not. / (2) Sorry, I'm new here too.", "ช่อง (2) บอกทางได้ชัดเจน (เดินตามป้ายสีฟ้าผ่านร้านขายของที่ระลึก) จึงไม่ใช่คนไม่รู้ทาง", "trap"),
          W("(1) Certainly! / (2) You can't go there.", "ขัดกับบริบททั้งสองช่อง", "meaning")],
         "ช่อง (1) ปฏิเสธเพราะแถวนี้เป็นของนิทรรศการไดโนเสาร์ ช่อง (2) บอกตำแหน่งทางเข้าซึ่งสอดคล้องกับการอธิบายทางต่อท้าย"),
        (f"{n1}: You look exhausted, {n2}. Did you stay up late last night?\n"
         f"{n2}: __(1)__ I was revising for today's history test until midnight.\n"
         f"{n1}: Wait—isn't the history test scheduled for next week?\n"
         f"{n2}: __(2)__ I must have misread the timetable on the board!",
         "(1) Yes, I barely slept. / (2) Are you serious?",
         [W("(1) No, I went to bed early. / (2) I knew that already.", "ขัดกับที่อ่านหนังสือถึงเที่ยงคืนและเข้าใจตารางสอบผิด", "context"),
          W("(1) Yes, I barely slept. / (2) Never mind, thank you.", "เมื่อรู้ว่าจำวันสอบผิด ต้องแสดงความตกใจ (Are you serious?) ไม่ใช่ขอบคุณ", "trap"),
          W("(1) Not at all. / (2) You're welcome.", "ไม่เข้ากับบริบทการอดนอนและจำวันสอบผิด", "meaning")],
         "ช่อง (1) ยอมรับว่าแทบไม่ได้นอนเพราะอ่านหนังสือถึงเที่ยงคืน ช่อง (2) ตกใจเมื่อเพื่อนทักว่าสอบสัปดาห์หน้า"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best pair of expressions to fill in blanks (1) and (2).",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ตรวจสอบให้ทั้งช่อง (1) และช่อง (2) สอดคล้องกับประโยคข้างเคียงทั้งสองจุด",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )
