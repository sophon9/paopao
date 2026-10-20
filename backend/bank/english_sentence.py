"""English sentence structure and error identification (e.write) for M.1 entrance."""

import random

from backend.bank.core import W, mcq, name_en, pick, skill, template

# ---------------------------------------------------------------------------
# 1. Error Identification (e.write.error)
# ---------------------------------------------------------------------------

skill(
    "e.write.error", "e.write", "การหาจุดผิดในประโยค (Error Identification)",
    lesson={
        "concept": "ข้อสอบ Error Identification ขีดเส้นใต้ 4 ส่วน (A), (B), (C), (D) เพื่อวัดความแม่นยำด้านไวยากรณ์ เช่น ความสอดคล้องของประธานกับกริยา (Subject-Verb Agreement), กาลเวลา (Tense), รูปกริยาหลัง Modal/Preposition และคำสรรพนาม",
        "steps": [
            "หาประธานหลักและกริยาแท้ของประโยค แล้วเช็คว่าพจน์ (เอกพจน์/พหูพจน์) และ Tense ตรงกับคำบอกเวลาหรือไม่",
            "ดูคำที่อยู่ข้างหน้าส่วนที่ขีดเส้นใต้ เช่น หลังบุพบท (in, on, of, without, before) ต้องตามด้วย V-ing หรือคำนาม",
            "เช็คคำคุณศัพท์/กริยาวิเศษณ์ และการใช้คำเชื่อม",
        ],
        "example": {
            "q": "Each of the ==(A) students== in our class ==(B) have== to ==(C) submit== the project ==(D) by Friday==.",
            "steps": [
                "ประธานหลักคือ Each (เอกพจน์เสมอ) ไม่ใช่ students",
                "กริยา (B) have จึงผิด ต้องแก้เป็น has",
            ],
            "a": "(B) have",
        },
        "mistakes": [
            "ดูแต่คำนามที่อยู่ติดกริยาโดยลืมดูประธานตัวจริงที่อยู่หน้า of / with / along with",
        ],
        "tips": [
            "จุดที่ออกสอบบ่อยที่สุด 3 อันดับแรก: 1) ประธานเอกพจน์-พหูพจน์ 2) Tense ขัดกับคำบอกเวลา 3) รูปกริยา to V1 / V-ing / V3",
        ],
    },
    weight=1.4,
)


@template("e.write.error", "medium")
def _error_id_sva_tense():
    name, pron = name_en()
    place = pick(["the science museum", "the national library", "the botanical garden", "the planetarium", "the art gallery"])
    years = random.randint(3, 9)
    hobby = pick(["collecting stamps", "playing chess", "baking pastries", "painting landscapes", "growing orchids"])
    subj = pick(["mathematics", "physics", "history", "geography", "literature"])
    cases = [
        (f"Neither {name} ==(A) nor== the other club members ==(B) is== available ==(C) to attend== the rehearsal ==(D) this evening==.",
         "(B) is",
         [W("(A) nor", "Neither ใช้คู่กับ nor ถูกต้องตามโครงสร้างแล้ว", "form"),
          W("(C) to attend", "available to + V1 ใช้บอกความพร้อมที่จะทำบางสิ่ง ถูกต้องแล้ว", "form"),
          W("(D) this evening", "เป็นคำบอกเวลาที่ถูกต้อง", "context")],
         "โครงสร้าง Neither A nor B กริยาต้องผันตามประธานตัวหลัง (B = the other club members ซึ่งเป็นพหูพจน์) จึงต้องแก้ is เป็น are"),
        (f"{name}, ==(A) together with== three classmates, ==(B) are planning== to visit ==(C) {place}== ==(D) next Saturday==.",
         "(B) are planning",
         [W("(A) together with", "เป็นวลีขยายประธานที่ใช้ได้ถูกต้อง", "form"),
          W(f"(C) {place}", "เป็นกรรมของกริยา visit ถูกต้องแล้ว", "form"),
          W("(D) next Saturday", "สอดคล้องกับการวางแผนไปในอนาคต", "context")],
         f"ประธานหลักคือ {name} (เอกพจน์) ส่วน together with three classmates เป็นเพียงส่วนขยาย กริยาจึงต้องแก้ are planning เป็น is planning"),
        (f"My uncle ==(A) has lived== in Chiang Mai ==(B) since== {years} years and ==(C) still enjoys== the cool weather ==(D) there==.",
         "(B) since",
         [W("(A) has lived", "ใช้ Present Perfect กับเหตุการณ์ที่ดำเนินต่อเนื่องมาจนถึงปัจจุบัน ถูกต้องแล้ว", "form"),
          W("(C) still enjoys", "ประธาน My uncle เป็นเอกพจน์ กริยาเติม -s ถูกต้องแล้ว", "agreement"),
          W("(D) there", "เป็นกริยาวิเศษณ์อ้างถึงเชียงใหม่ ถูกต้องแล้ว", "form")],
         f"{years} years เป็นระยะเวลา (period of time) ต้องใช้ for {years} years ไม่ใช่ since"),
        (f"One of the ==(A) most difficult== subjects ==(B) for many students== ==(C) are== ==(D) {subj}==.",
         "(C) are",
         [W("(A) most difficult", "ขั้นสูงสุด the most difficult ใช้ถูกต้องแล้ว", "form"),
          W("(B) for many students", "บุพบทวลีขยายความหมายได้ถูกต้อง", "form"),
          W(f"(D) {subj}", "ชื่อวิชาเป็นคำนามส่วนเติมเต็ม ถูกต้องแล้ว", "form")],
         "โครงสร้าง One of the + นามพหูพจน์ ประธานหลักคือคำว่า One (หนึ่งเดียว) กริยาจึงต้องเป็นเอกพจน์ แก้ are เป็น is"),
        (f"While {name} ==(A) was walking== home from school ==(B) yesterday==, it ==(C) begins== to rain ==(D) heavily==.",
         "(C) begins",
         [W("(A) was walking", "Past Continuous ใช้กับเหตุการณ์ที่กำลังดำเนินอยู่ในอดีต ถูกต้องแล้ว", "form"),
          W("(B) yesterday", "ระบุเวลาในอดีตชัดเจน", "context"),
          W("(D) heavily", "เป็น adverb ขยายกริยา rain ถูกต้องแล้ว", "form")],
         "เหตุการณ์เกิดขึ้นเมื่อวานนี้ (yesterday) กริยาที่เข้ามาแทรกต้องเป็น Past Simple แก้ begins เป็น began"),
        (f"==(A) {hobby.capitalize()}== ==(B) require== a lot of ==(C) patience== and careful ==(D) attention==.",
         "(B) require",
         [W(f"(A) {hobby.capitalize()}", "Gerund (V-ing) ทำหน้าที่เป็นประธานเอกพจน์ของประโยคได้ถูกต้อง", "form"),
          W("(C) patience", "เป็นคำนามนับไม่ได้ตามหลัง a lot of ถูกต้องแล้ว", "form"),
          W("(D) attention", "เป็นคำนามที่ถูกขยายด้วยคำคุณศัพท์ careful ถูกต้องแล้ว", "form")],
         f"ประธานคือการกระทำ ({hobby.capitalize()}) ซึ่งเป็น Gerund ถือเป็นเอกพจน์เสมอ กริยาจึงต้องเติม -s เป็น requires"),
    ]
    stem_sent, ans, wrongs, exp = pick(cases)
    return mcq(
        stem=f"Identify the underlined part that is grammatically INCORRECT.\n\n{stem_sent}",
        correct=ans,
        wrongs=wrongs,
        hint="ตรวจสอบประธานหลักของประโยค คำบอกเวลา และความสอดคล้องของพจน์",
        steps=[exp, f"ส่วนที่ผิดไวยากรณ์คือ \"{ans}\""],
    )


@template("e.write.error", "challenge")
def _error_id_verbals_modifiers():
    name, pron = name_en()
    inst = pick(["the violin", "the piano", "the acoustic guitar", "the flute"])
    city = pick(["Kyoto", "London", "Melbourne", "Zurich", "Vancouver"])
    book = pick(["detective novel", "science magazine", "history book", "biography"])
    cases = [
        (f"{name} is looking forward to ==(A) travel== to ==(B) {city}== with ==(C) family== during the ==(D) upcoming== holidays.",
         "(A) travel",
         [W(f"(B) {city}", "ชื่อเมืองตามหลังบุพบท to ถูกต้องแล้ว", "form"),
          W("(C) family", "ตามหลังบุพบท with ถูกต้องแล้ว", "form"),
          W("(D) upcoming", "คำคุณศัพท์ขยายคำนาม holidays ถูกต้องแล้ว", "form")],
         "สำนวน look forward to มีคำว่า to เป็นบุพบท (preposition) จึงต้องตามด้วย V-ing แก้ travel เป็น travelling/traveling"),
        (f"The {book} ==(A) was== ==(B) so== interesting that {name} could hardly ==(C) put down it== before ==(D) midnight==.",
         "(C) put down it",
         [W("(A) was", "ประธานเอกพจน์ใช้กริยา was ถูกต้องแล้ว", "agreement"),
          W("(B) so", "โครงสร้าง so + adj + that ใช้ถูกต้องแล้ว", "form"),
          W("(D) midnight", "before midnight ใช้บอกเวลาได้ถูกต้อง", "form")],
         "Phrasal verb ที่แยกได้ (put down) เมื่อกรรมเป็นคำสรรพนาม (it) ต้องวางไว้ตรงกลางเท่านั้น แก้เป็น put it down"),
        (f"==(A) Despite== the heavy traffic, {name} managed ==(B) arriving== at the examination hall ==(C) ten minutes== ==(D) early==.",
         "(B) arriving",
         [W("(A) Despite", "Despite + คำนาม/วลี (the heavy traffic) ถูกต้องแล้ว", "form"),
          W("(C) ten minutes", "ขยายคำว่า early เพื่อบอกเวลาที่เร็วกว่ากำหนด ถูกต้องแล้ว", "form"),
          W("(D) early", "เป็นกริยาวิเศษณ์ขยายการมาถึง ถูกต้องแล้ว", "form")],
         "คำกริยา manage ต้องตามด้วย to + V1 เสมอ (managed to arrive) ไม่ใช่ V-ing"),
        (f"The teacher made the students ==(A) to check== their ==(B) answers== ==(C) carefully== before ==(D) handing== in the test.",
         "(A) to check",
         [W("(B) answers", "คำนามพหูพจน์หลัง their ถูกต้องแล้ว", "form"),
          W("(C) carefully", "adverb ขยายกริยา check ถูกต้องแล้ว", "form"),
          W("(D) handing", "หลังบุพบท before ตามด้วย V-ing ถูกต้องแล้ว", "form")],
         "โครงสร้าง Causative verb: make + someone + V1 (ไม่ใช้ to) จึงต้องแก้ to check เป็น check"),
        (f"{name} has been practising ==(A) {inst}== ==(B) extreme== hard in order to ==(C) win== the youth competition ==(D) next month==.",
         "(B) extreme",
         [W(f"(A) {inst}", "เครื่องดนตรีตามหลัง practise ใช้ the นำหน้าถูกต้องแล้ว", "form"),
          W("(C) win", "หลัง in order to ต้องตามด้วย V1 ถูกต้องแล้ว", "form"),
          W("(D) next month", "บอกเวลาของการแข่งขันที่จะมาถึง ถูกต้องแล้ว", "context")],
         "คำที่ขยายกริยาวิเศษณ์ hard ต้องเป็นกริยาวิเศษณ์ (Adverb) จึงต้องแก้ extreme เป็น extremely"),
    ]
    stem_sent, ans, wrongs, exp = pick(cases)
    return mcq(
        stem=f"Identify the underlined part that is grammatically INCORRECT.\n\n{stem_sent}",
        correct=ans,
        wrongs=wrongs,
        hint="สังเกตโครงสร้างเฉพาะ เช่น look forward to + V-ing, make + O + V1, manage + to V1 และการวางกรรมของ Phrasal Verb",
        steps=[exp, f"ส่วนที่ผิดไวยากรณ์คือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 2. Word & Sentence Order (e.write.order)
# ---------------------------------------------------------------------------

skill(
    "e.write.order", "e.write", "การเรียงลำดับคำและประโยค (Word & Sentence Order)",
    lesson={
        "concept": "การเรียงคำในประโยคภาษาอังกฤษต้องยึดโครงสร้าง S + V + O/Complement รวมถึงลำดับคำคุณศัพท์ (OSASCOMP) และตำแหน่งของ Adverb of Frequency (หน้ากริยาแท้ หลัง V. to be)",
        "steps": [
            "หาประธาน (Subject) และกริยา (Verb) ของประโยคให้พบก่อน",
            "ถ้ามีคำคุณศัพท์หลายตัว ให้เรียงตามลำดับ: Opinion → Size → Age → Shape → Colour → Origin → Material → Purpose + Noun",
            "ถ้าเป็นการเรียงประโยคเป็นย่อหน้า ให้หาประโยคเปิดเรื่อง (Topic Sentence) และดูคำเชื่อมลำดับ (First, Then, Finally) หรือคำสรรพนามที่อ้างถึงประโยคก่อนหน้า",
        ],
        "example": {
            "q": "Rearrange: bought / a / wooden / round / small / table / she",
            "steps": [
                "ประธาน + กริยา = She bought",
                "เรียงคุณศัพท์ขยาย table: Size (small) → Shape (round) → Material (wooden)",
            ],
            "a": "She bought a small round wooden table.",
        },
        "mistakes": [
            "วางวัสดุ (wooden, leather, silk) ไว้หน้าขนาดหรือสี",
            "วาง Adverb of Frequency (always, seldom, never) ไว้หน้ากริยาช่วยหรือหลังกริยาแท้",
        ],
        "tips": [
            "คำนามหลักอยู่ท้ายสุดของกลุ่มคำนามเสมอ และวัสดุ (Material) จะอยู่ชิดคำนามหลักมากที่สุด",
        ],
    },
    weight=1.1,
)


@template("e.write.order", "easy")
def _order_adjectives_and_adverbs():
    name, pron = name_en()
    size = pick(["small", "large", "tiny"])
    age = pick(["old", "ancient", "modern", "new"])
    color = pick(["brown", "black", "white", "red", "blue"])
    origin = pick(["Japanese", "Italian", "Thai", "French", "Swiss"])
    mat_noun = pick([("wooden", "box"), ("leather", "bag"), ("ceramic", "vase"), ("silk", "scarf"), ("metal", "clock")])
    mat, noun = mat_noun
    mode = random.randint(1, 2)
    if mode == 1:
        ans = f"a {size} {age} {origin} {mat} {noun}"
        wrongs = [
            W(f"a {mat} {size} {age} {origin} {noun}", "วางวัสดุ (Material) ไว้หน้าสุด ซึ่งต้องอยู่ชิดคำนามหลัก", "form"),
            W(f"an {origin} {mat} {size} {age} {noun}", "สลับลำดับโดยนำสัญชาติและวัสดุมาไว้หน้าขนาดและอายุ", "form"),
            W(f"a {size} {mat} {origin} {age} {noun}", "ต้องเรียง Size → Age → Origin → Material", "form"),
        ]
        stem = f"Choose the phrase with the correct order of adjectives to complete the sentence:\n\"{name} found ____ in the attic.\""
        exp = f"ลำดับคำคุณศัพท์คือ Size ({size}) → Age ({age}) → Origin ({origin}) → Material ({mat}) + Noun ({noun})"
    else:
        adv = pick(["always", "usually", "seldom", "rarely", "often"])
        place = pick(["to the library", "to the sports club", "to the music room", "to the park"])
        day = pick(["on Saturdays", "after school", "on weekends", "in the afternoon"])
        ans = f"{name} {adv} walks {place} {day}."
        wrongs = [
            W(f"{name} walks {adv} {place} {day}.", f"ต้องวาง Adverb of Frequency ({adv}) ไว้หน้ากริยาแท้ walks", "form"),
            W(f"{name} {adv} {place} walks {day}.", "วางสถานที่คั่นระหว่าง Adverb of Frequency กับกริยาแท้ไม่ได้", "form"),
            W(f"{day.capitalize()} {name} walks {place} {adv}.", f"ไม่วาง {adv} ไว้ท้ายสุดของประโยคในโครงสร้างปกติ", "form"),
        ]
        stem = "Which sentence has the correct word order?"
        exp = f"Adverb of frequency ({adv}) ต้องวางไว้หน้ากริยาแท้ (walks) และตามด้วยสถานที่ + เวลา"
    return mcq(
        stem=stem,
        correct=ans,
        wrongs=wrongs,
        hint="จำลำดับคุณศัพท์ (Size → Age → Origin → Material + Noun) และตำแหน่ง Adverb of Frequency (หน้ากริยาแท้)",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.write.order", "hard")
def _order_paragraph_sentences():
    name, pron = name_en()
    dessert = pick(["sponge cake", "blueberry tart", "chocolate pie", "banana bread"])
    person = pick(["Mother's", "Father's", "Grandma's", "Sister's"])
    paragraphs = [
        (f"(1) Finally, {pron} decorated the top with fresh fruit and served it to the family.\n"
         f"(2) {name} decided to bake a homemade {dessert} for {person} birthday.\n"
         f"(3) Then, {pron} poured the batter into a tin and baked it for thirty minutes.\n"
         f"(4) First, {pron} mixed flour, sugar, butter, and eggs in a large bowl.",
         "(2) - (4) - (3) - (1)",
         [W("(4) - (2) - (3) - (1)", "ต้องขึ้นต้นด้วยประโยค (2) เพื่อแนะนำชื่อคนและหัวข้อก่อนใช้สรรพนามในข้อ (4)", "context"),
          W("(2) - (3) - (4) - (1)", "ต้องผสมแป้ง (First) ในข้อ (4) ก่อนเทใส่พิมพ์อบ (Then) ในข้อ (3)", "context"),
          W("(1) - (2) - (4) - (3)", "ข้อ (1) มีคำว่า Finally ต้องอยู่ท้ายสุด", "context")],
         f"เริ่มด้วย (2) แนะนำว่า {name} จะทำขนม → (4) First ผสมส่วนผสม → (3) Then เทใส่พิมพ์อบ → (1) Finally ตกแต่งและเสิร์ฟ"),
        (f"(1) However, when {pron} reached the {pick(['bus stop', 'train station', 'school gate'])}, {pron} realised the wallet was still on the desk.\n"
         f"(2) {name} woke up late this morning and had to get dressed in a hurry.\n"
         f"(3) As a result, {pron} had to run all the way back home to fetch it.\n"
         f"(4) Without eating breakfast, {pron} grabbed the schoolbag and rushed out of the house.",
         "(2) - (4) - (1) - (3)",
         [W("(2) - (1) - (4) - (3)", "ต้องวิ่งออกจากบ้านในข้อ (4) ก่อนไปถึงป้ายรถเมล์ในข้อ (1)", "context"),
          W("(4) - (2) - (1) - (3)", "ประโยคแรกต้องระบุชื่อประธานในข้อ (2) ก่อนใช้สรรพนามในข้อ (4)", "context"),
          W("(2) - (4) - (3) - (1)", "ต้องรู้ตัวว่าลืมกระเป๋าสตางค์ในข้อ (1) ก่อนจึงต้องวิ่งกลับมาเอาในข้อ (3)", "context")],
         f"เริ่มด้วย (2) {name} ตื่นสาย → (4) รีบคว้ากระเป๋าวิ่งออกจากบ้าน → (1) ถึงที่หมายแล้วพบว่าลืมกระเป๋าสตางค์ → (3) จึงต้องวิ่งกลับไปเอา"),
        (f"(1) Inside the protective case, the caterpillar slowly transforms into a pupa.\n"
         f"(2) The life cycle of a {pick(['monarch butterfly', 'swallowtail butterfly', 'painted lady butterfly', 'silk moth'])} begins when a female lays tiny eggs on a {pick(['mulberry', 'milkweed', 'citrus', 'green'])} leaf.\n"
         f"(3) After about {random.randint(2, 4)} weeks, a winged adult emerges and unfolds its wings.\n"
         f"(4) When the egg hatches, a hungry caterpillar comes out and munches on leaves.",
         "(2) - (4) - (1) - (3)",
         [W("(2) - (1) - (4) - (3)", "ไข่ต้องฟักออกมาเป็นหนอนในข้อ (4) ก่อนที่หนอนจะเข้าดักแด้ในข้อ (1)", "context"),
          W("(4) - (2) - (1) - (3)", "ต้องเริ่มจากประโยคเปิดเรื่อง (2) ที่บอกจุดเริ่มต้นด้วยการวางไข่", "context"),
          W("(2) - (4) - (3) - (1)", "ต้องเปลี่ยนเป็นดักแด้ในข้อ (1) ก่อนกลายเป็นตัวเต็มวัยในข้อ (3)", "context")],
         "เรียงตามวงจรชีวิตผีเสื้อ: (2) วางไข่บนใบไม้ → (4) ฟักเป็นตัวหนอนกินใบไม้ → (1) เข้าดักแด้ → (3) ออกมาเป็นผีเสื้อ"),
    ]
    passage, ans, wrongs, exp = pick(paragraphs)
    return mcq(
        stem="Rearrange the following sentences to form a logical paragraph.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="หาประโยคแรกที่แนะนำหัวข้อหรือชื่อตัวละคร (ยังไม่ใช้สรรพนามโดด ๆ) แล้วไล่ตามลำดับคำเชื่อม",
        steps=[exp, f"ลำดับที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 3. Combining Sentences (e.write.combine)
# ---------------------------------------------------------------------------

skill(
    "e.write.combine", "e.write", "การรวมประโยคด้วยคำเชื่อมและอนุประโยค (Sentence Combining)",
    lesson={
        "concept": "การรวมประโยคสองประโยคเข้าด้วยกันต้องเลือกคำเชื่อมที่ตรงกับความสัมพันธ์ของเนื้อความ (เหตุ-ผล, ขัดแย้ง, เงื่อนไข, ขยายคำนามด้วย Relative Clause หรือโครงสร้าง too...to / enough to / so...that)",
        "steps": [
            "วิเคราะห์ความสัมพันธ์ของ 2 ประโยค เช่น เหตุผล (because/so), ขัดแย้ง (although/despite), หรือผลลัพธ์ (so...that / too...to)",
            "เช็คโครงสร้างไวยากรณ์หลังคำเชื่อม เช่น although + S + V แต่ despite/in spite of + N/V-ing",
        ],
        "example": {
            "q": "Combine: The box is very heavy. The little boy cannot lift it.",
            "steps": [
                "กล่องหนักเกินไปจนเด็กชายยกไม่ไหว",
                "ใช้โครงสร้าง too + adj + (for someone) + to V1 (ต้องตัด it ท้ายประโยคออกเพราะอ้างถึงประธานแล้ว)",
            ],
            "a": "The box is too heavy for the little boy to lift.",
        },
        "mistakes": [
            "ใช้ Although คู่กับ but ในประโยคเดียวกัน (เช่น Although it rained, but we went out — ผิด)",
            "ลืมตัดคำสรรพนามซ้ำท้ายประโยคเมื่อใช้ too...to หรือ Relative Clause",
        ],
        "tips": [
            "จำคู่โครงสร้าง: so + adj + that + S + V | such + (a/an) + adj + N + that + S + V | too + adj + to + V1",
        ],
    },
    weight=1.2,
)


@template("e.write.combine", "medium")
def _combine_conjunctions_relatives():
    name, pron = name_en()
    obj = pick(["laptop", "camera", "bicycle", "watch", "guitar"])
    adj_pair = pick([
        ("very expensive", f"{name} couldn't afford to buy it", "expensive", "buy"),
        ("very complicated", f"{name} couldn't solve it alone", "complicated", "solve alone"),
        ("very hot", f"{name} couldn't drink it right away", "hot", "drink right away"),
    ])
    mode = random.randint(1, 3)
    if mode == 1:
        p1, p2, adj, verb_phr = adj_pair
        passage = f"1) The item was {p1}.\n2) {p2}."
        ans = f"The item was too {adj} for {name} to {verb_phr}."
        wrongs = [
            W(f"The item was so {adj} for {name} to {verb_phr}.", "โครงสร้าง too...to ต้องใช้ too ไม่ใช่ so (ถ้าใช้ so ต้องตามด้วย that + S + V)", "form"),
            W(f"The item was too {adj} that {p2}.", "คำว่า too ไม่ใช้คู่กับ that + ประโยค (ต้องเป็น so + adj + that)", "form"),
            W(f"The item was {adj} enough for {name} to {verb_phr}.", f"enough to แปลว่า พอที่จะทำได้ ซึ่งความหมายตรงข้ามกับโจทย์ที่บอกว่าทำไม่ได้", "meaning"),
        ]
        exp = f"การรวมประโยคที่บอกว่า 'มากเกินไปจนทำไม่ได้' ใช้โครงสร้าง too + adj + for someone + to V1 (และตัด it ท้ายประโยคออก)"
    elif mode == 2:
        place = pick(["Chiang Mai", "Phuket", "Krabi", "Nan"])
        passage = f"1) It rained heavily all afternoon.\n2) {name} and friends still enjoyed their trip to {place}."
        ans = f"Although it rained heavily all afternoon, {name} and friends still enjoyed their trip to {place}."
        wrongs = [
            W(f"Although it rained heavily all afternoon, but {name} and friends still enjoyed their trip to {place}.", "ห้ามใช้ Although คู่กับ but ในประโยคเดียวกัน", "form"),
            W(f"Despite it rained heavily all afternoon, {name} and friends still enjoyed their trip to {place}.", "หลัง Despite ต้องตามด้วยคำนามหรือ V-ing ไม่ตามด้วยประโยค S + V โดยตรง", "form"),
            W(f"Because it rained heavily all afternoon, {name} and friends still enjoyed their trip to {place}.", "ความหมายของสองประโยคขัดแย้งกัน ไม่ใช่เหตุและผล", "meaning"),
        ]
        exp = "สองประโยคมีความหมายขัดแย้งกัน และตามด้วยประโยค (it rained...) จึงใช้ Although โดยไม่มี but ซ้ำ"
    else:
        uncle = pick(["Uncle Somchai", "Aunt Malee", "Mr. Parker", "Dr. Wilson"])
        passage = f"1) The {obj} belongs to {uncle}.\n2) {name} borrowed it for the weekend competition."
        ans = f"The {obj} which {name} borrowed for the weekend competition belongs to {uncle}."
        wrongs = [
            W(f"The {obj} who {name} borrowed for the weekend competition belongs to {uncle}.", f"{obj} เป็นสิ่งของ ต้องใช้ which หรือ that ไม่ใช้ who", "form"),
            W(f"The {obj} which {name} borrowed it for the weekend competition belongs to {uncle}.", "เมื่อใช้ which แทนกรรมแล้ว ต้องตัดคำว่า it ที่ซ้ำออก", "trap"),
            W(f"The {obj} whose {name} borrowed for the weekend competition belongs to {uncle}.", "whose ใช้บอกความเป็นเจ้าของ ไม่ใช่กรรมของกริยา borrowed", "form"),
        ]
        exp = f"ขยายคำนามสิ่งของ ({obj}) ด้วย Relative pronoun 'which' และต้องตัดสรรพนาม 'it' ที่ซ้ำออก"
    return mcq(
        stem="Choose the best way to combine the two sentences without changing their meaning.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="เช็คทั้งความหมายและโครงสร้างไวยากรณ์ (ระวังการใช้ Although...but หรือการลืมตัด it ซ้ำ)",
        steps=[exp, f"ประโยคที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.write.combine", "hard")
def _combine_correlative_participle():
    name1, _ = name_en()
    name2, _ = name_en()
    while name2 == name1:
        name2, _ = name_en()
    lang1, lang2 = pick([("English", "French"), ("Japanese", "Mandarin"), ("German", "Spanish")])
    cases = [
        (f"1) {name1} does not eat spicy food.\n2) {name2} does not eat spicy food either.",
         f"Neither {name1} nor {name2} eats spicy food.",
         [W(f"Neither {name1} nor {name2} don't eat spicy food.", "คำว่า Neither มีความหมายเป็นปฏิเสธอยู่แล้ว ห้ามใส่ don't ซ้ำ (Double Negative)", "trap"),
          W(f"Either {name1} or {name2} eats spicy food.", "Either...or แปลว่า คนใดคนหนึ่ง แต่โจทย์บอกว่าไม่กินทั้งสองคน", "meaning"),
          W(f"Both {name1} and {name2} eats spicy food.", "Both...and แปลว่ากินทั้งคู่ (ตรงข้ามกับโจทย์) และกริยาหลัง Both ต้องไม่เติม -s", "meaning")],
         f"เมื่อทั้งสองคนไม่ทำทั้งคู่ ใช้ Neither A nor B และกริยาผันตามประธานตัวหลัง ({name2} เป็นเอกพจน์ → eats) โดยไม่ใส่ not ซ้ำ"),
        (f"1) {name1} speaks fluent {lang1}.\n2) {name1} also speaks fluent {lang2}.",
         f"{name1} speaks not only fluent {lang1} but also fluent {lang2}.",
         [W(f"{name1} speaks neither {lang1} nor {lang2} fluently.", "neither...nor แปลว่าไม่พูดทั้งสองภาษา ขัดกับโจทย์", "meaning"),
          W(f"{name1} speaks not only fluent {lang1} and also fluent {lang2}.", "โครงสร้างคู่คือ not only ... but also ... (ไม่ใช่ and also)", "form"),
          W(f"{name1} speaks either fluent {lang1} nor fluent {lang2}.", "จับคู่คำเชื่อมผิด (either ต้องคู่กับ or)", "form")],
         "การรวมประโยคที่ทำได้ทั้งสองอย่างใช้โครงสร้างคู่ขนาน not only ... but also ..."),
        (f"1) {name1} finished all the science homework.\n2) After that, {name1} went out to play badminton.",
         f"Having finished all the science homework, {name1} went out to play badminton.",
         [W(f"Having been finished by the homework, {name1} went out to play badminton.", f"{name1} เป็นผู้ทำการบ้านเสร็จเอง (Active) ไม่ใช่ถูกการบ้านทำ", "form"),
          W(f"Before finishing all the science homework, {name1} went out to play badminton.", "โจทย์บอกว่าทำเสร็จก่อนแล้วจึงออกไปเล่น ไม่ใช่ไปเล่นก่อนทำเสร็จ", "meaning"),
          W(f"Finished all the science homework, badminton was played by {name1}.", "เกิด Dangling participle เพราะประธานของประโยคหลักกลายเป็น badminton", "form")],
         f"เหตุการณ์ที่ทำเสร็จสมบูรณ์ก่อนอีกเหตุการณ์หนึ่ง ใช้ Perfect Participle: Having + V3 (Having finished...) โดยมีประธาน {name1} เป็นผู้กระทำ"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the sentence that best combines the given pair of sentences.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="ดูโครงสร้างคำเชื่อมคู่ (Neither...nor, not only...but also) หรือการลดรูป Participle",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 4. Question Forms, Tag Questions & Indirect Questions (e.write.question)
# ---------------------------------------------------------------------------

skill(
    "e.write.question", "e.write", "การสร้างประโยคคำถาม Question Tags และ Indirect Questions",
    lesson={
        "concept": "ประโยคคำถามมี 3 รูปแบบสำคัญที่ออกสอบบ่อย: 1) Wh-questions (Wh + กริยาช่วย + S + V) 2) Question Tags (หน้าบอกเล่า-หลังปฏิเสธ, หน้าปฏิเสธ-หลังบอกเล่า) 3) Indirect Questions (เรียงแบบประโยคบอกเล่า Wh + S + V)",
        "steps": [
            "สำหรับ Question Tag: ดูกริยาของประโยคหน้า และระวังคำที่มีความหมายเชิงลบ เช่น seldom, rarely, hardly, never, little, few ซึ่งต้องใช้ Tag เป็นบอกเล่า",
            "สำหรับ Indirect Question (หลัง Could you tell me / Do you know): ห้ามสลับกริยาช่วยมาไว้หน้าประธาน และตัด do/does/did ออก",
        ],
        "example": {
            "q": "Could you tell me where ____?",
            "steps": [
                "เป็น Indirect Question ที่ขึ้นต้นด้วย Could you tell me where...",
                "ส่วนหลัง where ต้องเรียงแบบประโยคบอกเล่า (S + V) คือ the post office is",
            ],
            "a": "the post office is",
        },
        "mistakes": [
            "เลือก where is the post office หลัง Could you tell me (ผิดเพราะสลับกริยามาหน้าประธานซ้ำซ้อน)",
            "ลืมว่า Let's... ใช้ Tag ว่า shall we? และคำสั่ง (Imperative) ใช้ will you?",
        ],
        "tips": [
            "จำพิเศษ Question Tags: I am → aren't I? | Let's → shall we? | Everyone/Someone → ...they? | hardly/seldom/never → Tag บอกเล่า",
        ],
    },
    weight=1.3,
)


@template("e.write.question", "easy")
def _question_tags():
    name, pron = name_en()
    place = pick(["the museum", "the swimming pool", "the concert", "the book fair", "the dentist's"])
    cases = [
        (f"{name} seldom eats fast food for dinner, ____?",
         f"does {pron}",
         [W(f"doesn't {pron}", "คำว่า seldom มีความหมายเป็นปฏิเสธ (แทบจะไม่) อยู่แล้ว ดังนั้น Tag จึงต้องเป็นบอกเล่า", "trap"),
          W(f"is {pron}", "กริยาหลักคือ eats (Present Simple) ต้องใช้กริยาช่วย does ไม่ใช่ is", "form"),
          W(f"did {pron}", "eats เป็น Present Simple ไม่ใช่อดีต", "form")],
         f"ประโยคหน้ามีคำว่า seldom (แทบจะไม่ = ปฏิเสธ) และกริยา eats เป็น Present Simple ดังนั้น Tag ต้องเป็นบอกเล่าคือ does {pron}?"),
        (f"Let's review the vocabulary list before the bell rings, ____?",
         "shall we",
         [W("don't we", "ประโยคชักชวนที่ขึ้นต้นด้วย Let's (Let us) ต้องใช้ Question Tag ว่า shall we เสมอ", "form"),
          W("will you", "will you ใช้กับประโยคคำสั่งหรือขอร้องทั่วไป ไม่ใช่ Let's", "trap"),
          W("aren't we", "ไม่ใช้ aren't we คู่กับ Let's", "form")],
         "ประโยคที่ขึ้นต้นด้วย Let's ... ต้องใช้ Question Tag ว่า shall we? เสมอ"),
        (f"{name} and {pick(['Leo', 'Maya', 'Ben'])} have already visited {place}, ____?",
         "haven't they",
         [W("don't they", "ประโยคหน้าใช้ Present Perfect (have visited) ดังนั้นกริยาช่วยใน Tag ต้องใช้ have → haven't they", "form"),
          W("have they", "ประโยคหน้าเป็นบอกเล่า ดังนั้น Tag ต้องเป็นรูปปฏิเสธ", "sign"),
          W("didn't they", "กริยาช่วยในประโยคคือ have ไม่ใช่ Past Simple", "form")],
         "ประธาน 2 คนแทนด้วย they และกริยาคือ have visited (บอกเล่า) จึงใช้ Tag ว่า haven't they?"),
        (f"Everyone in the auditorium enjoyed the magic show, ____?",
         "didn't they",
         [W("didn't he", "คำสรรพนามที่ใช้แทน Everyone / Everybody ใน Question Tag คือ they", "trap"),
          W("don't they", "กริยา enjoyed เป็นช่องที่ 2 (Past Simple) ต้องใช้ didn't", "form"),
          W("did they", "ประโยคหน้าเป็นบอกเล่า Tag ต้องเป็นปฏิเสธ", "sign")],
         "ประธาน Everyone แทนใน Tag ด้วย they และกริยา enjoyed เป็นอดีตบอกเล่า จึงใช้ didn't they?"),
        (f"I'm in the same project group as {name}, ____?",
         "aren't I",
         [W("amn't I", "ในภาษาอังกฤษมาตรฐานไม่มีรูปย่อ amn't I ต้องใช้ aren't I", "trap"),
          W("am I", "ประโยคหน้าเป็นบอกเล่า Tag ต้องเป็นปฏิเสธ", "sign"),
          W("don't I", "ประโยคหน้าใช้ V. to be (am) จึงไม่ใช้ don't", "form")],
         "Question Tag ของบอกเล่า 'I am...' คือ 'aren't I?' เสมอ"),
    ]
    stem_sent, ans, wrongs, exp = pick(cases)
    return mcq(
        stem=f"Choose the correct question tag to complete the sentence:\n\n\"{stem_sent}\"",
        correct=ans,
        wrongs=wrongs,
        hint="เช็คว่าประโยคหน้าเป็นบอกเล่าหรือปฏิเสธ (ระวังคำว่า seldom/hardly) และดูชนิดของกริยา",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.write.question", "hard")
def _question_indirect():
    name, pron = name_en()
    opener = pick(["Could you tell me", "Do you happen to know", "Can you explain", "I wonder"])
    q_mark = "?" if not opener.startswith("I wonder") else "."
    dest = pick(["the science laboratory", "the central station", "the principal's office", "the nearest pharmacy"])
    cases = [
        (f"{opener} where ____",
         f"{dest} is{q_mark}",
         [W(f"is {dest}{q_mark}", "ใน Indirect Question ห้ามวางกริยา is ไว้หน้าประธาน", "trap"),
          W(f"does {dest} be{q_mark}", "ไม่ใช้กริยาช่วย does กับ Verb to be", "form"),
          W(f"{dest} are{q_mark}", f"{dest} เป็นเอกพจน์ ต้องใช้กริยา is", "agreement")],
         "หลังคำถามนำ (Indirect Question) ต้องเรียงคำแบบประโยคบอกเล่า: where + ประธาน + กริยา"),
        (f"{opener} what time ____",
         f"the library closes on Fridays{q_mark}",
         [W(f"does the library close on Fridays{q_mark}", "ห้ามใส่กริยาช่วย does ใน Indirect Question ต้องตัด does ออกแล้วเติม -s ที่กริยาแท้", "trap"),
          W(f"the library close on Fridays{q_mark}", "ประธาน the library เป็นเอกพจน์ กริยาต้องเติม -s เป็น closes", "agreement"),
          W(f"closes the library on Fridays{q_mark}", "เรียงกริยาไว้หน้าประธานซึ่งผิดโครงสร้าง Indirect Question", "form")],
         "เมื่อเปลี่ยนเป็น Indirect Question ต้องตัด does ออก และผันกริยา closes ตามประธานเอกพจน์ the library"),
        (f"{opener} why ____",
         f"{name} was absent yesterday{q_mark}",
         [W(f"was {name} absent yesterday{q_mark}", f"ต้องเรียงประธาน {name} ไว้หน้ากริยา was", "trap"),
          W(f"did {name} absent yesterday{q_mark}", "absent เป็นคำคุณศัพท์ ต้องใช้กับ Verb to be (was absent) ไม่ใช้ did", "form"),
          W(f"{name} is absent yesterday{q_mark}", "มีคำบอกเวลา yesterday จึงต้องใช้รูปอดีต was", "form")],
         f"เรียงแบบบอกเล่าหลัง why คือ ประธาน ({name}) + กริยาอดีต (was) + absent yesterday"),
        (f"{opener} how much ____",
         f"this dictionary costs{q_mark}",
         [W(f"does this dictionary cost{q_mark}", "เป็น Indirect Question จึงต้องตัด does ออกแล้วเปลี่ยนกริยาเป็น costs", "trap"),
          W(f"this dictionary cost{q_mark}", "this dictionary เป็นเอกพจน์ ใน Present Simple ต้องเติม -s ที่ costs", "agreement"),
          W(f"is this dictionary cost{q_mark}", "cost เป็นกริยาแท้อยู่แล้ว ไม่ใช้คู่กับ is", "form")],
         "หลัง how much ใน Indirect Question ต้องเรียงแบบประโยคบอกเล่า: this dictionary (ประธานเอกพจน์) + costs"),
    ]
    stem_prefix, ans, wrongs, exp = pick(cases)
    return mcq(
        stem=f"Choose the grammatically correct completion:\n\n\"{stem_prefix}\"",
        correct=ans,
        wrongs=wrongs,
        hint="หลัง Could you tell me / Do you know / I wonder + Wh-word ต้องเรียงเป็น ประธาน + กริยา เสมอ",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 5. Choosing the Grammatically Correct Sentence (e.write.correct_sent)
# ---------------------------------------------------------------------------

skill(
    "e.write.correct_sent", "e.write", "การเลือกประโยคที่ถูกต้องตามหลักไวยากรณ์",
    lesson={
        "concept": "โจทย์ให้ประโยค 4 ข้อแล้วถามว่าข้อใดถูกไวยากรณ์ (Which sentence is grammatically correct?) มักทดสอบคำนามนับไม่ได้ (information, furniture, advice, equipment), การเปรียบเทียบ, การใช้ number of / amount of และ Conditional Sentences",
        "steps": [
            "อ่านตัวเลือกทั้ง 4 ข้อและมองหาคำสำคัญที่มักเป็นจุดหลอก เช่น informations, furnitures, advices (คำเหล่านี้ห้ามเติม -s เด็ดขาด)",
            "ตรวจสอบการใช้ The number of (+ นามพหูพจน์ + กริยาเอกพจน์) เทียบกับ A number of (+ นามพหูพจน์ + กริยาพหูพจน์)",
        ],
        "example": {
            "q": "Which sentence is grammatically correct?",
            "steps": [
                "advice, information, luggage, furniture เป็นคำนามนับไม่ได้ ห้ามเติม -s และไม่ใช้ a/an นำหน้าโดยตรง",
                "หากต้องการนับจำนวนต้องใช้ a piece of advice",
            ],
            "a": "My teacher gave me some useful advice before the exam.",
        },
        "mistakes": [
            "คิดว่า advice, equipment, furniture, information, homework เติม -s ได้",
            "สับสนระหว่าง The number of (แปลว่าจำนวนของ... ใช้กริยาเอกพจน์) กับ A number of (แปลว่ามี...จำนวนมาก ใช้กริยาพหูพจน์)",
        ],
        "tips": [
            "ท่องคำนามนับไม่ได้ยอดฮิต: advice, information, furniture, equipment, luggage, baggage, homework, news, traffic, progress",
        ],
    },
    weight=1.2,
)


@template("e.write.correct_sent", "medium")
def _correct_sentence_nouns_quantifiers():
    name, pron = name_en()
    uncountable = pick(["advice", "information", "furniture", "equipment", "luggage"])
    adj = pick(["useful", "important", "new", "modern", "essential"])
    group = random.randint(1, 3)
    if group == 1:
        ans = f"{name} found some {adj} {uncountable} on the website."
        wrongs = [
            W(f"{name} found many {adj} {uncountable}s on the website.", f"{uncountable} เป็นคำนามนับไม่ได้ ห้ามเติม -s และไม่ใช้กับ many", "form"),
            W(f"{name} found an {adj} {uncountable} on the website.", f"{uncountable} เป็นคำนามนับไม่ได้ ห้ามใช้ a/an นำหน้าโดยตรง (ต้องใช้ a piece of)", "form"),
            W(f"Those {uncountable} on the website are very {adj}.", f"{uncountable} เป็นคำนามนับไม่ได้ จึงใช้กับ Those และกริยาพหูพจน์ are ไม่ได้", "agreement"),
        ]
        exp = f"คำว่า '{uncountable}' เป็นคำนามนับไม่ได้ (Uncountable Noun) ห้ามเติม -s ห้ามใช้ a/an หรือ many/those แต่ใช้กับ some ได้"
    elif group == 2:
        noun_pl = pick(["applicants", "students", "volunteers", "participants", "members"])
        ans = f"The number of {noun_pl} in the club is increasing every year."
        wrongs = [
            W(f"The number of {noun_pl} in the club are increasing every year.", "The number of (จำนวนของ...) มีประธานหลักคือ The number จึงต้องใช้กริยาเอกพจน์ is", "agreement"),
            W(f"A number of {noun_pl} in the club is increasing every year.", "A number of แปลว่า มีจำนวนมาก (คล้าย many) ต้องใช้กริยาพหูพจน์ are", "agreement"),
            W(f"The amount of {noun_pl} in the club are increasing every year.", f"amount of ใช้กับคำนามนับไม่ได้ ไม่ใช้กับ {noun_pl}", "form"),
        ]
        exp = f"โครงสร้าง 'The number of + นามพหูพจน์' แปลว่า จำนวนของ... ถือเป็นเอกพจน์ ต้องใช้คู่กับกริยาเอกพจน์ (is)"
    else:
        place = pick(["in the library", "in the classroom", "in the auditorium", "at the station"])
        ans = f"There was hardly any noise {place} this morning."
        wrongs = [
            W(f"There were many noises {place} this morning.", "noise ในความหมายว่าเสียงรบกวนทั่วไปเป็นคำนามนับไม่ได้ ใช้กับ much/little ไม่ใช่ many", "form"),
            W(f"There was not no noise {place} this morning.", "ใช้ปฏิเสธซ้อน (not + no) ซึ่งผิดหลักไวยากรณ์มาตรฐาน", "form"),
            W(f"There were a few noise {place} this morning.", "a few ใช้กับคำนามพหูพจน์นับได้เท่านั้น ไม่ใช้กับ noise", "form"),
        ]
        exp = "noise เป็นคำนามนับไม่ได้ จึงใช้กับกริยาเอกพจน์ (There was) และใช้ hardly any ได้ถูกต้อง"
    return mcq(
        stem="Which of the following sentences is grammatically CORRECT?",
        correct=ans,
        wrongs=wrongs,
        hint="ระวังคำนามนับไม่ได้ (advice, information, furniture, equipment, noise) และโครงสร้าง The number of vs A number of",
        steps=[exp, f"ประโยคที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.write.correct_sent", "challenge")
def _correct_sentence_advanced():
    name, pron = name_en()
    subj = pick(["the piano", "chess", "badminton", "classical guitar", "table tennis"])
    bus = pick(["the school bus", "the morning train", "the first ferry", "the coach"])
    vehicle = pick(["a bicycle", "a scooter", "a skateboard", "a mountain bike"])
    cases = [
        (f"If {name} had woken up earlier, {pron} would not have missed {bus}.",
         [W(f"If {name} would have woken up earlier, {pron} did not miss {bus}.", "ใน If-clause ห้ามใช้ would have + V3 ต้องใช้ Past Perfect (had + V3)", "form"),
          W(f"If {name} woke up earlier, {pron} would not have missed {bus}.", "ประโยคเงื่อนไขตรงข้ามความจริงในอดีต (Type 3) ส่วน If-clause ต้องใช้ had woken up", "form"),
          W(f"If {name} had woken up earlier, {pron} will not miss {bus}.", "Main clause ของ Conditional Type 3 ต้องใช้ would have + V3 ไม่ใช่ will", "form")],
         "ประโยคเงื่อนไขแบบที่ 3 (ตรงข้ามกับความจริงในอดีต) มีโครงสร้าง: If + S + had + V3, S + would have + V3"),
        (f"The harder {name} practises {subj}, the more confident {pron} becomes.",
         [W(f"The more hard {name} practises {subj}, the confident {pron} becomes.", "ขั้นกว่าของ hard คือ harder และส่วนหลังต้องมี more หน้า confident", "form"),
          W(f"Harder {name} practises {subj}, more confident {pron} becomes.", "โครงสร้างยิ่ง...ก็ยิ่ง... ต้องมี The นำหน้าขั้นกว่าทั้งสองส่วน (The + comparative..., the + comparative...)", "form"),
          W(f"The hardest {name} practises {subj}, the most confident {pron} becomes.", "โครงสร้างนี้ต้องใช้ขั้นกว่า (Comparative) ไม่ใช่ขั้นสุด (Superlative)", "form")],
         "โครงสร้างเปรียบเทียบ 'ยิ่ง...ก็ยิ่ง...' ต้องใช้ The + ขั้นกว่า ..., the + ขั้นกว่า ... (The harder..., the more confident...)"),
        (f"It is essential that {name} wear a helmet when riding {vehicle} to school.",
         [W(f"It is essential that {name} wears a helmet when ride {vehicle} to school.", "หลัง when หากลดรูปต้องเป็น when riding (ไม่ใช่ when ride)", "form"),
          W(f"It is essential for {name} to wearing a helmet when riding {vehicle}.", "หลัง to ต้องเป็น V1 (to wear) ไม่ใช่ to wearing", "form"),
          W(f"{name} must to wear a helmet when riding {vehicle} to school.", "หลัง modal verb 'must' ห้ามมี to", "form")],
         "หลังโครงสร้าง It is essential that + S + V(infinitive without to) จึงใช้ wear และหลัง when ลดรูปเป็น when riding ได้ถูกต้อง"),
    ]
    ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Which of the following sentences is grammatically CORRECT?",
        correct=ans,
        wrongs=wrongs,
        hint="ตรวจสอบโครงสร้าง If-clause Type 3 (If + had V3, would have V3) หรือโครงสร้าง The + ขั้นกว่า, the + ขั้นกว่า",
        steps=[exp, f"ประโยคที่ถูกต้องคือ \"{ans}\""],
    )


# ---------------------------------------------------------------------------
# 6. Cloze Structure & Parallelism (e.write.cloze_struct)
# ---------------------------------------------------------------------------

skill(
    "e.write.cloze_struct", "e.write", "การเติมโครงสร้างประโยคและความคู่ขนาน (Parallel Structure)",
    lesson={
        "concept": "โครงสร้างคู่ขนาน (Parallelism) กำหนดว่าคำหรือวลีที่เชื่อมด้วย and, but, or, as well as, rather than ต้องมีรูปไวยากรณ์เหมือนกัน (เช่น V-ing คู่กับ V-ing, to V1 คู่กับ to V1, คำนามคู่กับคำนาม)",
        "steps": [
            "มองหาคำเชื่อมและรายการข้างหน้าช่องว่าง เช่น A, B, and ____",
            "ดูว่า A และ B อยู่ในรูปใด (เช่น V-ing, to V1, Adjective, หรือ Noun) แล้วเลือกตัวเลือกที่มีรูปเดียวกัน",
        ],
        "example": {
            "q": "During the camp, students learned how to pitch a tent, cook over a fire, and ____.",
            "steps": [
                "รายการข้างหน้าหลัง how to คือ pitch (V1), cook (V1)",
                "หลัง and จึงต้องเป็น V1 เช่นกัน คือ read a compass",
            ],
            "a": "read a compass",
        },
        "mistakes": [
            "เลือกรูป V-ing ทั้งที่คำข้างหน้าอยู่ในรูป V1 หรือ to + V1",
        ],
        "tips": [
            "ขีดเส้นใต้คำที่อยู่หน้าคำเชื่อม and / or แล้วจับคู่รูปคำให้หน้าตาเหมือนกันเป๊ะ!",
        ],
    },
    weight=1.1,
)


@template("e.write.cloze_struct", "easy")
def _cloze_parallel_structure():
    name, pron = name_en()
    inst = pick(["the ukulele", "the violin", "the keyboard", "the drums"])
    nurse = pick(["school nurse", "family doctor", "PE teacher", "coach"])
    topic_ex = pick(["science exhibition", "robotics workshop", "history documentary", "astronomy camp"])
    cases = [
        (f"In {name}'s free time, {pron} enjoys sketching cartoons, playing {inst}, and ____.",
         "baking chocolate brownies",
         [W("to bake chocolate brownies", "คำข้างหน้าหลัง enjoys คือ sketching (V-ing) และ playing (V-ing) จึงต้องใช้ V-ing ให้คู่ขนานกัน", "form"),
          W("baked chocolate brownies", "เป็นกริยาช่อง 2 ไม่คู่ขนานกับ sketching และ playing", "form"),
          W("bakes chocolate brownies", "เป็นกริยาเติม -s ไม่คู่ขนานกับรูป Gerund (V-ing)", "form")],
         "โครงสร้าง Parallelism หลัง enjoys: sketching (V-ing), playing (V-ing), and baking (V-ing)"),
        (f"To stay healthy, the {nurse} advised {name} to eat nutritious food, get enough sleep, and ____ regularly.",
         "exercise",
         [W("exercising", "คำข้างหน้าหลัง advised ... to คือ eat (V1) และ get (V1) จึงต้องใช้ V1 (exercise)", "form"),
          W("exercised", "ไม่อยู่ในรูป V1 เหมือน eat และ get", "form"),
          W("to exercising", "หลัง to ในที่นี้ละไว้และตามด้วย V1 ไม่ใช่ to V-ing", "form")],
         "รายการคำแนะนำหลัง advised ... to คือ (to) eat, (to) get, and (to) exercise ซึ่งต้องใช้รูป V1 เหมือนกันทั้งหมด"),
        (f"The new {topic_ex} is educational, interactive, and ____ for {name}'s class.",
         "inspiring",
         [W("inspiration", "inspiration เป็นคำนาม แต่ educational และ interactive เป็นคำคุณศัพท์ (Adjective)", "form"),
          W("inspire", "inspire เป็นคำกริยา ไม่คู่ขนานกับคำคุณศัพท์ข้างหน้า", "form"),
          W("inspiredly", "เป็นกริยาวิเศษณ์ แต่หลัง Verb to be (is) ในรายการนี้ต้องเป็นคำคุณศัพท์", "form")],
         "คำที่เชื่อมด้วย and หลัง is คือ educational (Adj.), interactive (Adj.), และต้องตามด้วย Adjective คือ inspiring"),
        (f"{name} would rather read a mystery novel at home than ____ in a crowded shopping mall.",
         "walk around",
         [W("walking around", "โครงสร้าง would rather + V1 ... than + V1 ต้องใช้รูปกริยาไม่ผัน (V1) ทั้งสองฝั่ง", "trap"),
          W("to walk around", "หลัง than ในโครงสร้าง would rather ... than ต้องตามด้วย V1 โดยไม่มี to", "form"),
          W("walked around", "ไม่ใช้รูปอดีตหลัง would rather ... than ในปัจจุบัน", "form")],
         "โครงสร้างคู่ขนาน would rather + V1 ... than + V1 ดังนั้นเมื่อข้างหน้าเป็น read หลัง than จึงต้องเป็น walk around"),
    ]
    stem_sent, ans, wrongs, exp = pick(cases)
    return mcq(
        stem=f"Choose the best word or phrase to maintain parallel structure:\n\n\"{stem_sent}\"",
        correct=ans,
        wrongs=wrongs,
        hint="ดูคำที่อยู่ในรายการเดียวกันข้างหน้า and / than แล้วเลือกรูปคำที่เหมือนกัน (Parallel Structure)",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )


@template("e.write.cloze_struct", "medium")
def _cloze_paragraph_completion():
    name, pron = name_en()
    city = pick(["Ayutthaya", "Sukhothai", "Chiang Mai", "Kanchanaburi", "Lopburi"])
    centuries = random.choice(["three", "four", "five", "six"])
    cases = [
        (f"Last Saturday, {name}'s class went on an educational trip to {city}. "
         f"__(1)__ arriving at the historical park, the students listened carefully to the local guide, "
         f"__(2)__ explained how the ancient temples were built {centuries} centuries ago.",
         "(1) Upon / (2) who",
         [W("(1) While / (2) which", "the local guide เป็นบุคคล ต้องใช้ Relative pronoun 'who' ไม่ใช่ 'which'", "form"),
          W("(1) Because / (2) whom", "หลัง because ต้องตามด้วยประโยค S + V และช่องที่ 2 ทำหน้าที่เป็นประธานของกริยา explained จึงต้องใช้ who", "form"),
          W("(1) Despite / (2) whose", "เนื้อความไม่ได้ขัดแย้งกัน และ explained เป็นกริยา ไม่ใช่คำนามตามหลัง whose", "meaning")],
         "ช่อง (1) Upon + V-ing แปลว่า ทันทีที่มาถึง ช่อง (2) ขยายบุคคล (the local guide) และทำหน้าที่เป็นประธานของกริยา explained จึงใช้ who"),
        (f"In {name}'s community, plastic waste takes hundreds of years to decompose in landfills. "
         f"__(1)__, bringing a reusable cloth bag to the {pick(['supermarket', 'fresh market', 'grocery store', 'bookshop'])} is a simple habit "
         f"__(2)__ can significantly reduce the number of plastic bags thrown away each week.",
         "(1) Therefore / (2) that",
         [W("(1) However / (2) who", "ประโยคที่สองเป็นผลสรุปไม่ใช่ความขัดแย้ง และ a simple habit เป็นสิ่งของ/แนวคิด ใช้ who ไม่ได้", "form"),
          W("(1) Although / (2) where", "Although ต้องเชื่อมอนุประโยคเข้ากับประโยคหลัก ไม่วางหน้าเครื่องหมายจุลภาคเดี่ยว ๆ แบบ Adverb", "form"),
          W("(1) Moreover / (2) whom", "whom ใช้กับบุคคลที่เป็นกรรม ไม่ใช้ขยายคำว่า a simple habit", "form")],
         "ช่อง (1) เชื่อมเหตุและผลด้วย Therefore (ดังนั้น) ช่อง (2) ใช้ Relative pronoun 'that' ขยายคำนาม a simple habit"),
        (f"In {name}'s history project about {city}, {pron} learned that before the printing press, every book __(1)__ by hand, "
         f"which made books extremely rare. As a result, only a small number of wealthy scholars "
         f"__(2)__ afford to own a personal library.",
         "(1) had to be copied / (2) could",
         [W("(1) had copied / (2) can", "หนังสือ (every book) ต้องเป็นฝ่ายถูกคัดลอก (Passive Voice: be + V3) และเป็นเหตุการณ์ในอดีต (could)", "form"),
          W("(1) is copied / (2) will", "เรื่องราวเกิดขึ้นก่อนการประดิษฐ์แท่นพิมพ์ในอดีต ต้องใช้ Past Tense", "form"),
          W("(1) was copying / (2) must", "หนังสือคัดลอกตัวเองไม่ได้ ต้องใช้ Passive Voice", "form")],
         "ช่อง (1) หนังสือเป็นฝ่ายถูกคัดลอกด้วยมือในอดีต (Passive: had to be copied) ช่อง (2) บอกความสามารถในอดีตจึงใช้ could"),
    ]
    passage, ans, wrongs, exp = pick(cases)
    return mcq(
        stem="Choose the best pair of words/phrases to complete the passage.",
        passage=passage,
        correct=ans,
        wrongs=wrongs,
        hint="พิจารณาทั้งคำเชื่อมความหมาย รูปประโยค Active/Passive และคำสรรพนามเชื่อมประโยค (Relative Pronoun)",
        steps=[exp, f"คำตอบที่ถูกต้องคือ \"{ans}\""],
    )
