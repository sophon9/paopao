"""English vocabulary question bank (topic ``e.vocab``) for M.1 entrance prep."""

import random

from backend.bank.core import W, mcq, name_en, pick, skill, template

# ---------------------------------------------------------------------------
# 1. Meaning in Context (e.vocab.context)
# ---------------------------------------------------------------------------

skill(
    "e.vocab.context", "e.vocab", "Vocabulary in Context (เดาคำศัพท์จากบริบท)",
    lesson={
        "concept": "การเลือกคำศัพท์เติมในช่องว่างต้องอาศัย 'ตัวใบ้ในบริบท (Context Clues)' เช่น เหตุและผล (because, so, therefore) การเปรียบเทียบหรือขัดแย้ง (although, but, however) หรือคำขยายที่อยู่ข้างเคียง",
        "steps": [
            "อ่านประโยคให้จบแล้วหาคำเชื่อมบอกทิศทางของความหมาย (เป็นบวกหรือลบ คล้อยตามหรือขัดแย้ง)",
            "ขีดเส้นใต้คำสำคัญที่เป็นเบาะแส เช่น อาการ สถานที่ หรือผลลัพธ์ที่ตามมา",
            "ตัดตัวเลือกที่มีความหมายตรงข้ามหรือผิดชนิดคำออกก่อน",
        ],
        "example": {
            "q": "The hikers were completely ____ after climbing the steep mountain trail for six hours.",
            "steps": [
                "เบาะแสคือ 'เดินขึ้นเขาชันนานถึง 6 ชั่วโมง'",
                "ผลลัพธ์จึงต้องเป็น 'เหนื่อยล้ามาก' คือ exhausted",
            ],
            "a": "exhausted",
        },
        "mistakes": [
            "แปลแค่คำหน้าช่องว่างโดยไม่อ่านส่วนขยายหลัง because / so / although",
            "เลือกคำที่มีรูปคล้ายกันแต่ความหมายคนละเรื่อง",
        ],
        "tips": ["หาคำใบ้หลัง because / so / after ให้เจอ คำตอบจะสอดคล้องกับเหตุการณ์นั้นเสมอ"],
    },
    weight=1.5,
)

# 16 rich adjective/verb context entries
_CTX_EASY = [
    ("exhausted", "เหน็ดเหนื่อยหมดแรง", "delighted", "ดีใจมาก", "curious", "อยากรู้อยากเห็น", "generous", "ใจกว้าง",
     "after practicing basketball for three hours in the hot sun"),
    ("generous", "ใจดีมีน้ำใจ", "selfish", "เห็นแก่ตัว", "nervous", "กังวลประหม่า", "careless", "สะเพร่า",
     "because {pron} always shares snacks and stationery with classmates"),
    ("nervous", "ตื่นเต้นกังวล", "confident", "มั่นใจ", "cheerful", "ร่าเริง", "sleepy", "ง่วงนอน",
     "before walking onto the stage to give {pos} first speech"),
    ("polite", "สุภาพเรียบร้อย", "rude", "หยาบคาย", "lazy", "ขี้เกียจ", "noisy", "เสียงดัง",
     "and always says 'thank you' and 'excuse me' to teachers and elders"),
    ("curious", "ช่างสงสัยอยากรู้", "bored", "เบื่อหน่าย", "afraid", "หวาดกลัว", "angry", "โกรธ",
     "about how rockets work and asked the scientist many questions"),
    ("patient", "อดทนใจเย็น", "impatient", "ใจร้อน", "cruel", "โหดร้าย", "weak", "อ่อนแอ",
     "when explaining difficult math steps to {pos} younger sister again and again"),
    ("grateful", "ซาบซึ้งขอบคุณ", "jealous", "อิจฉา", "lonely", "เหงา", "proud", "หยิ่ง/ภูมิใจ",
     "to the neighbor who helped repair {pos} broken bicycle in the rain"),
    ("punctual", "ตรงต่อเวลา", "late", "มาสาย", "absent", "ขาดเรียน", "forgetful", "ขี้ลืม",
     "and arrives at the school gate ten minutes early every single day"),
    ("brave", "กล้าหาญ", "timid", "ขี้ขลาด", "greedy", "โลภมาก", "clumsy", "ซุ่มซ่าม",
     "enough to rescue the little puppy from the deep ditch"),
    ("honest", "ซื่อสัตย์", "dishonest", "ไม่ซื่อสัตย์", "strict", "เข้มงวด", "shy", "ขี้อาย",
     "and immediately returned the lost wallet to the school office"),
]

_CTX_HARD = [
    ("postpone", "เลื่อนออกไปก่อน", "cancel", "ยกเลิกถาวร", "celebrate", "เฉลิมฉลอง", "expand", "ขยายขนาด",
     "the outdoor sports day until next Friday because of the heavy storm"),
    ("fragile", "เปราะบางแตกหักง่าย", "durable", "ทนทานแข็งแรง", "ancient", "โบราณ", "flexible", "ยืดหยุ่น",
     "so please wrap the glass ornaments carefully before putting them in the box"),
    ("essential", "จำเป็นอย่างยิ่ง", "optional", "เลือกทำหรือไม่ก็ได้", "harmful", "เป็นอันตราย", "temporary", "ชั่วคราว",
     "for all campers to bring a flashlight and a raincoat to the forest trip"),
    ("scarce", "ขาดแคลน/หายาก", "abundant", "อุดมสมบูรณ์", "delicious", "อร่อย", "artificial", "เทียม/สังเคราะห์",
     "during the long dry season, so villagers had to save every drop of water"),
    ("persuade", "โน้มน้าวชักจูง", "prevent", "ขัดขวาง/ป้องกัน", "complain", "บ่นต่อว่า", "ignore", "เพิกเฉย",
     "{pos} parents to let {obj} adopt the stray kitten by promising to feed it daily"),
    ("reluctant", "ลังเลไม่เต็มใจ", "eager", "กระตือรือร้น", "grateful", "รู้สึกขอบคุณ", "confident", "มั่นใจ",
     "to dive into the swimming pool because the water looked freezing cold"),
    ("investigate", "ตรวจสอบ/สืบสวน", "decorate", "ตกแต่ง", "abandon", "ละทิ้ง", "predict", "ทำนาย",
     "the cause of the strange noise coming from the school laboratory"),
    ("nutritious", "มีคุณค่าทางโภชนาการ", "poisonous", "มีพิษ", "tasteless", "จืดชืดไร้รสชาติ", "expensive", "ราคาแพง",
     "meals with fresh vegetables, fish, and brown rice for the young athletes"),
    ("visible", "มองเห็นได้", "invisible", "มองไม่เห็น", "silent", "เงียบสงบ", "distant", "ห่างไกล",
     "with the naked eye on a clear, cloudless night in winter"),
    ("apologize", "ขอโทษ", "congratulate", "แสดงความยินดี", "interrupt", "พูดแทรก", "forgive", "ให้อภัย",
     "sincerely to the librarian for returning the borrowed encyclopedia three days late"),
]


@template("e.vocab.context", "easy")
def _vocab_context_adj():
    name, pron = name_en()
    pos = "her" if pron == "she" else "his"
    corr, corr_th, w1, w1_th, w2, w2_th, w3, w3_th, clue_raw = pick(_CTX_EASY)
    clue = clue_raw.format(pron=pron, pos=pos)
    return mcq(
        stem=f"{name} was very ____ {clue}.",
        correct=corr,
        wrongs=[
            W(w1, f"'{w1}' แปลว่า {w1_th} ซึ่งขัดแย้งกับบริบทในประโยค", "context"),
            W(w2, f"'{w2}' แปลว่า {w2_th} ไม่สอดคล้องกับเหตุการณ์ที่บอกไว้", "meaning"),
            W(w3, f"'{w3}' แปลว่า {w3_th} ไม่ตรงกับเบาะแสในประโยค", "meaning"),
        ],
        hint="อ่านเหตุผลหรือการกระทำข้างหลังช่องว่าง เพื่อดูว่าตรงกับนิสัยหรือความรู้สึกแบบใด",
        steps=[
            f"เบาะแสในประโยคคือ '{clue}'",
            f"คำศัพท์ที่ตรงกับบริบทนี้คือ '{corr}' ({corr_th})",
        ],
    )


@template("e.vocab.context", "hard")
def _vocab_context_advanced():
    name, pron = name_en()
    pos = "her" if pron == "she" else "his"
    obj = "her" if pron == "she" else "him"
    corr, corr_th, w1, w1_th, w2, w2_th, w3, w3_th, clue_raw = pick(_CTX_HARD)
    clue = clue_raw.format(pron=pron, pos=pos, obj=obj)
    prompts = {
        "postpone": f"Principal {name} decided to ____ {clue}.",
        "fragile": f"The ceramic cups in {name}'s parcel are extremely ____, {clue}.",
        "essential": f"Coach {name} reminded us that it is ____ {clue}.",
        "scarce": f"In {name}'s village, fresh water became very ____ {clue}.",
        "persuade": f"{name} tried to ____ {clue}.",
        "reluctant": f"{name} was ____ {clue}.",
        "investigate": f"{name} and the science teacher went to ____ {clue}.",
        "nutritious": f"The chef at {name}'s school prepares ____ {clue}.",
        "visible": f"{name} read that the bright comet will be clearly ____ {clue}.",
        "apologize": f"{name} went to ____ {clue}.",
    }
    return mcq(
        stem=prompts[corr],
        correct=corr,
        wrongs=[
            W(w1, f"'{w1}' แปลว่า {w1_th} ซึ่งไม่ตรงกับเงื่อนไขในประโยค (คำที่ถูกคือ {corr} = {corr_th})", "context"),
            W(w2, f"'{w2}' แปลว่า {w2_th} ไม่เข้ากับบริบทของประโยคนี้", "meaning"),
            W(w3, f"'{w3}' แปลว่า {w3_th} ความหมายไม่สอดคล้องกับเนื้อความ", "meaning"),
        ],
        hint="พิจารณาเหตุและผลในประโยค แล้วเลือกคำที่มีความหมายสอดคล้องกับสถานการณ์มากที่สุด",
        steps=[
            f"วิเคราะห์บริบท: '{clue}'",
            f"คำที่เหมาะสมที่สุดคือ '{corr}' ซึ่งแปลว่า {corr_th}",
        ],
    )


# ---------------------------------------------------------------------------
# 2. Synonyms / Closest in Meaning (e.vocab.synonym)
# ---------------------------------------------------------------------------

skill(
    "e.vocab.synonym", "e.vocab", "Synonyms (คำที่มีความหมายเหมือนกัน/ใกล้เคียง)",
    lesson={
        "concept": "ข้อสอบ Synonym มักขีดเส้นใต้คำศัพท์ในประโยคแล้วถามหาคำที่มีความหมายใกล้เคียงที่สุด (closest in meaning) ถ้านึกคำแปลไม่ออก ให้ใช้บริบทของประโยคช่วยเดาทิศทางความหมายก่อน",
        "steps": [
            "ดูคำที่เน้น (**...**) ในประโยค แล้วอ่านบริบทรอบข้างเพื่อระบุความหมายและชนิดของคำ (Noun/Verb/Adj)",
            "ตัดตัวเลือกที่เป็นคำตรงข้าม (Antonym) ซึ่งข้อสอบชอบนำมาหลอกเป็นตัวเลือกแรก",
            "แทนค่าคำตอบลงในประโยคเดิมเพื่อตรวจว่าความหมายไม่เปลี่ยน",
        ],
        "example": {
            "q": "Which word is closest in meaning to the bold word?\nThe museum displays **ancient** coins from two thousand years ago.",
            "steps": [
                "ancient ขยายเหรียญจากเมื่อ 2,000 ปีก่อน แปลว่า เก่าแก่/โบราณ",
                "คำที่มีความหมายใกล้เคียงที่สุดคือ very old",
            ],
            "a": "very old",
        },
        "mistakes": [
            "สับสนระหว่างโจทย์ที่ถามหา closest in meaning (ความหมายเหมือน) กับ opposite in meaning (ความหมายตรงข้าม)",
        ],
        "tips": ["สังเกตคำโจทย์ให้ดีว่าถาม CLOSEST / SIMILAR (เหมือนกัน) หรือ OPPOSITE (ตรงข้าม)"],
    },
    weight=1.4,
)

# 14 synonym sets with dynamic sentence frames
_SYN_BANK = [
    ("enormous", "huge", "tiny", "ordinary", "fragile", "ขนาดใหญ่มหึมา",
     "{name} saw an **enormous** whale skeleton in the main hall of the museum."),
    ("ancient", "very old", "modern", "expensive", "common", "เก่าแก่โบราณ",
     "{name} read an article about **ancient** temples built over a thousand years ago."),
    ("purchase", "buy", "sell", "borrow", "repair", "ซื้อ",
     "{name} went to **purchase** notebooks and pens at the school cooperative store."),
    ("assist", "help", "bother", "ignore", "follow", "ช่วยเหลือ",
     "{name} volunteered to **assist** the art teacher in setting up the exhibition."),
    ("rapidly", "quickly", "slowly", "quietly", "carelessly", "อย่างรวดเร็ว",
     "{name} noticed the dark storm clouds moving **rapidly** across the afternoon sky."),
    ("wealthy", "rich", "poor", "famous", "strict", "มั่งคั่งร่ำรวย",
     "A **wealthy** businessman donated fifty new computers to {name}'s school."),
    ("construct", "build", "destroy", "paint", "measure", "สร้าง/ก่อสร้าง",
     "Workers will **construct** a new pedestrian bridge in front of {name}'s school."),
    ("fortunate", "lucky", "unlucky", "careful", "exhausted", "โชคดี",
     "{name} was **fortunate** to catch the last bus before the heavy rain started."),
    ("vacant", "empty", "crowded", "locked", "clean", "ว่าง/ไม่มีคนอยู่",
     "There were only two **vacant** seats left in the cinema when {name} arrived."),
    ("brief", "short", "long", "boring", "difficult", "สั้นกระชับ",
     "{name} listened to a **brief** welcome speech before the concert began."),
    ("accomplish", "achieve", "fail", "postpone", "forget", "ทำสำเร็จลุล่วง",
     "Working together helped {name}'s team **accomplish** their science project on time."),
    ("intelligent", "clever", "foolish", "lazy", "polite", "ฉลาดหลักแหลม",
     "{name}'s dog is so **intelligent** that it can open the garden gate by itself."),
    ("prohibit", "forbid", "allow", "encourage", "suggest", "ห้ามปราม",
     "Park rules at {name}'s camp strictly **prohibit** visitors from feeding the wild monkeys."),
    ("exhausted", "very tired", "energetic", "delighted", "confused", "เหนื่อยล้าอย่างมาก",
     "After the two-hour badminton match, {name} felt completely **exhausted**."),
]


@template("e.vocab.synonym", "easy")
def _vocab_synonym_basic():
    name, _ = name_en()
    word, syn, ant, w2, w3, th_meaning, sent_tmpl = pick(_SYN_BANK[:8])
    sent = sent_tmpl.format(name=name)
    return mcq(
        stem=f"Choose the word that is **closest in meaning** to the highlighted word.\n{sent}",
        correct=syn,
        wrongs=[
            W(ant, f"'{ant}' เป็นคำตรงข้าม (Antonym) ของ '{word}' ไม่ใช่คำความหมายเหมือน", "trap"),
            W(w2, f"'{w2}' มีความหมายไม่ตรงกับ '{word}' ซึ่งแปลว่า {th_meaning}", "meaning"),
            W(w3, f"'{w3}' ไม่ใช่คำที่มีความหมายใกล้เคียงกับ '{word}' ({th_meaning})", "meaning"),
        ],
        hint=f"อ่านประโยคเพื่อเดาความหมายของ **{word}** แล้วเลือกคำที่แปลเหมือนกัน",
        steps=[
            f"ในบริบทนี้ '**{word}**' แปลว่า {th_meaning}",
            f"คำที่มีความหมายใกล้เคียงที่สุด (Synonym) คือ '{syn}'",
        ],
    )


@template("e.vocab.synonym", "medium")
def _vocab_synonym_intermediate():
    name, _ = name_en()
    word, syn, ant, w2, w3, th_meaning, sent_tmpl = pick(_SYN_BANK[5:])
    sent = sent_tmpl.format(name=name)
    return mcq(
        stem=f"Which word can best replace **{word}** without changing the meaning of the sentence?\n{sent}",
        correct=syn,
        wrongs=[
            W(ant, f"ระวัง! '{ant}' มีความหมายตรงกันข้ามกับ '{word}' ({th_meaning})", "trap"),
            W(w2, f"'{w2}' ไม่สามารถแทนที่ '{word}' ซึ่งแปลว่า {th_meaning} ได้", "meaning"),
            W(w3, f"'{w3}' มีความหมายคนละด้านกับ '{word}' ในบริบทนี้", "context"),
        ],
        hint=f"หาคำที่แทนที่ **{word}** ในประโยคได้โดยความหมายคงเดิม",
        steps=[
            f"คำว่า '**{word}**' ในประโยคนี้มีความหมายว่า {th_meaning}",
            f"จึงสามารถใช้ '{syn}' แทนได้โดยความหมายไม่เปลี่ยน",
        ],
    )


# ---------------------------------------------------------------------------
# 3. Antonyms / Opposite in Meaning (e.vocab.antonym)
# ---------------------------------------------------------------------------

skill(
    "e.vocab.antonym", "e.vocab", "Antonyms (คำที่มีความหมายตรงข้าม)",
    lesson={
        "concept": "Antonym คือคำที่มีความหมายตรงกันข้าม ข้อสอบอาจถามตรง ๆ ว่าคำใดมีค่าตรงข้าม (opposite in meaning) หรือให้เติมคำในประโยคที่มีคำเชื่อมขัดแย้ง เช่น while, whereas, but, unlike",
        "steps": [
            "เช็กโจทย์ให้ชัดว่าถามหา **OPPOSITE** (ตรงข้าม)",
            "ระวังตัวลวงที่เป็น Synonym (คำแปลเหมือนกัน) ซึ่งมักวางไว้หลอกคนที่อ่านโจทย์เร็วเกินไป",
            "สังเกตอุปสรรค (Prefix) บอกความหมายตรงข้าม เช่น un-, in-, im-, il-, ir-, dis-",
        ],
        "example": {
            "q": "Choose the word that is **opposite in meaning** to the bold word.\nThe river is very **shallow** near the bank.",
            "steps": [
                "shallow แปลว่า ตื้น",
                "คำตรงข้ามของตื้นคือ ลึก (deep)",
            ],
            "a": "deep",
        },
        "mistakes": [
            "เผลอเลือกคำที่มีความหมายเหมือนกัน (Synonym) เพราะลืมดูคำว่า OPPOSITE ในโจทย์",
        ],
        "tips": ["เจอคำว่า OPPOSITE ในโจทย์ ให้ตีกรอบไว้ทันที แล้วหาคู่ตรงข้าม เช่น generous ↔ stingy/selfish, permanent ↔ temporary"],
    },
    weight=1.3,
)

_ANT_BANK = [
    ("shallow", "deep", "narrow", "clear", "calm", "ตื้น", "ลึก",
     "The stream behind {name}'s house is very **shallow** in summer."),
    ("generous", "stingy", "kind", "wealthy", "polite", "ใจกว้าง/เอื้อเฟื้อ", "ขี้เหนียว/ตระหนี่",
     "Everyone admires {name}'s aunt because she is **generous** to charity."),
    ("artificial", "natural", "fake", "modern", "colorful", "เทียม/ทำขึ้น", "ตามธรรมชาติ",
     "{name} noticed that the café decorated its balcony with **artificial** flowers."),
    ("permanent", "temporary", "lasting", "serious", "regular", "ถาวร", "ชั่วคราว",
     "The road closure near {name}'s school is only a **permanent** arrangement—or so we thought."),
    ("expand", "shrink", "grow", "stretch", "combine", "ขยายตัว", "หดตัว",
     "{name} learned that most metals **expand** slightly when they are heated in the lab."),
    ("compulsory", "optional", "necessary", "strict", "difficult", "บังคับ", "เลือกได้ตามสมัครใจ",
     "Wearing a swimming cap is **compulsory** at {name}'s sports club."),
    ("ancient", "modern", "historic", "antique", "fragile", "โบราณ", "ทันสมัย/ยุคใหม่",
     "{name} loves comparing the **ancient** city wall with the surrounding buildings."),
    ("brave", "cowardly", "courageous", "strong", "honest", "กล้าหาญ", "ขี้ขลาด",
     "{name} read a story about a **brave** firefighter who rescued a family."),
    ("abundant", "scarce", "plentiful", "fresh", "expensive", "อุดมสมบูรณ์/มีมาก", "ขาดแคลน/หายาก",
     "Wild berries are **abundant** in {name}'s hometown during autumn."),
    ("polite", "rude", "courteous", "quiet", "gentle", "สุภาพ", "หยาบคาย",
     "{name} gave a **polite** reply to the customer's question."),
    ("accept", "refuse", "receive", "agree", "invite", "ยอมรับ", "ปฏิเสธ",
     "{name} was happy to **accept** the invitation to the science camp."),
    ("occupied", "vacant", "busy", "crowded", "locked", "มีคนใช้อยู่/ไม่ว่าง", "ว่าง",
     "All the study booths near {name} were **occupied** before the exam."),
]


@template("e.vocab.antonym", "easy")
def _vocab_antonym_direct():
    name, _ = name_en()
    word, ant, syn_trap, w2, w3, word_th, ant_th, sent_tmpl = pick(_ANT_BANK[:8])
    sent = sent_tmpl.format(name=name)
    return mcq(
        stem=f"Choose the word that is **opposite in meaning** to the highlighted word.\n{sent}",
        correct=ant,
        wrongs=[
            W(syn_trap, f"'{syn_trap}' เป็นคำที่มีความหมายใกล้เคียงกับ '{word}' ({word_th}) แต่โจทย์ถามหาคำตรงข้าม (opposite)", "trap"),
            W(w2, f"'{w2}' ไม่ใช่คำตรงข้ามของ '{word}' ({word_th} ↔ {ant_th})", "meaning"),
            W(w3, f"'{w3}' มีความหมายไม่ตรงข้ามกับ '{word}'", "meaning"),
        ],
        hint=f"ระวัง! โจทย์ถามหาคำที่มีความหมาย **ตรงกันข้าม (opposite)** กับ **{word}**",
        steps=[
            f"คำว่า '**{word}**' แปลว่า {word_th}",
            f"คำที่มีความหมายตรงข้ามคือ '{ant}' ซึ่งแปลว่า {ant_th}",
        ],
    )


@template("e.vocab.antonym", "hard")
def _vocab_antonym_contrast_sentence():
    name, _ = name_en()
    word, ant, syn_trap, w2, w3, word_th, ant_th, _ = pick(_ANT_BANK[3:])
    conn = pick(["Whereas", "While", "Unlike"])
    if conn == "Unlike":
        stem = f"Unlike the first task which was **{word}**, the second task was completely ____ for {name}'s team."
    else:
        stem = f"{conn} the old rules made the activity **{word}**, the new policy makes it ____ for {name}'s class."
    return mcq(
        stem=stem,
        correct=ant,
        wrongs=[
            W(syn_trap, f"มีคำเชื่อมเปรียบเทียบความต่าง '{conn}' ต้องใช้คำตรงข้ามของ '{word}' ({word_th}) ไม่ใช่คำความหมายคล้าย ('{syn_trap}')", "trap"),
            W(w2, f"'{w2}' ไม่ได้สื่อความหมายตรงข้ามกับ '{word}' ({word_th})", "context"),
            W(w3, f"'{w3}' ไม่สอดคล้องกับการเปรียบเทียบความตรงกันข้ามในประโยค", "meaning"),
        ],
        hint=f"คำขึ้นต้น '{conn}' บอกว่าครึ่งหลังของประโยคต้องมีความหมายตรงข้ามกับ **{word}**",
        steps=[
            f"'{conn}' แสดงความขัดแย้ง/ตรงกันข้ามกับคำว่า '**{word}**' ({word_th})",
            f"จึงต้องเติมคำตรงข้ามคือ '{ant}' ({ant_th})",
        ],
    )


# ---------------------------------------------------------------------------
# 4. Word Forms & Parts of Speech (e.vocab.wordform)
# ---------------------------------------------------------------------------

skill(
    "e.vocab.wordform", "e.vocab", "Word Forms (รูปคำและหน้าที่ของคำ)",
    lesson={
        "concept": "คำศัพท์รากเดียวกันเปลี่ยน Suffix เพื่อเปลี่ยนหน้าที่: คำนาม (Noun: -tion, -ment, -ness, -ity) วางหลัง a/an/the/my, คำคุณศัพท์ (Adjective: -ful, -less, -ous, -ive, -able) ขยายคำนามหรือหลัง Verb to be, คำกริยาวิเศษณ์ (Adverb: -ly) ขยายกริยาแท้ และคุณศัพท์ -ed (คนรู้สึก) vs -ing (สิ่งของ/เรื่องราวน่า...)",
        "steps": [
            "ดูตำแหน่งของช่องว่างว่าทำหน้าที่ขยายอะไรในประโยค",
            "ถ้าอยู่หลัง a/an/the/his/great และหน้า of → เลือก Noun | ถ้าอยู่หน้า Noun → เลือก Adjective | ถ้าขยายกริยาอาการ → เลือก Adverb (-ly)",
            "ถ้าเป็นตระกูลรู้สึก (interested/interesting, excited/exciting) ดูว่าขยาย 'คนที่รู้สึก (-ed)' หรือ 'สิ่งที่น่า... (-ing)'",
        ],
        "example": {
            "q": "The audience clapped ____ at the end of the concert.",
            "steps": [
                "ช่องว่างทำหน้าที่ขยายกริยาแท้ clapped (ปรบมืออย่างไร)",
                "ต้องใช้ Adverb ที่ลงท้ายด้วย -ly คือ loudly / enthusiastically",
            ],
            "a": "enthusiastically",
        },
        "mistakes": [
            "ใช้ Adjective แทน Adverb เวลาขยายกริยาแท้ เช่นพูดว่า drive careful แทนที่จะเป็น drive carefully",
            "สลับ -ed กับ -ing เช่นบอกว่า The movie was boring vs I was bored",
        ],
        "tips": ["จำโครงสร้าง: the + Noun + of | be + Adj | V.แท้ + Adv (-ly) | คนรู้สึก = -ed, สิ่งนั้นน่า... = -ing"],
    },
    weight=1.4,
)

_WF_FAMILIES = [
    # (noun, verb, adj, adv, stem_type, sentence_template, explanation)
    ("success", "succeed", "successful", "successfully", "adv",
     "{name}'s team completed the robotics challenge ____ before the timer ran out.",
     "ขยายกริยาแท้ 'completed' (ทำสำเร็จอย่างไร) ต้องใช้ Adverb (-ly)"),
    ("carefulness", "care", "careful", "carefully", "adv",
     "{name} checked every calculation ____ to avoid making silly mistakes.",
     "ขยายกริยาแท้ 'checked' ต้องใช้ Adverb คือ carefully"),
    ("decision", "decide", "decisive", "decisively", "noun",
     "After a long discussion, {name} made an important ____ about the club budget.",
     "อยู่หลังคำคุณศัพท์ 'an important' ต้องเป็นคำนามเอกพจน์ (decision)"),
    ("invention", "invent", "inventive", "inventively", "noun",
     "{name} gave a presentation about a revolutionary ____ that changed global communication.",
     "อยู่หลัง 'a revolutionary' ต้องเป็นคำนาม (invention)"),
    ("danger", "endanger", "dangerous", "dangerously", "adj",
     "{name} knows that swimming in the river during a thunderstorm is extremely ____.",
     "อยู่หลัง Verb to be (is) และมี Adverb (extremely) ขยายข้างหน้า ต้องเป็นคำคุณศัพท์ (dangerous)"),
    ("beauty", "beautify", "beautiful", "beautifully", "adv",
     "{name} sang the traditional song ____ at the school talent show.",
     "ขยายกริยาแท้ 'sang' (ร้องเพลงอย่างไพเราะ) ต้องใช้ Adverb (beautifully)"),
    ("confidence", "confide", "confident", "confidently", "noun",
     "Speaking in front of the class every week helped {name} build great ____.",
     "เป็นกรรมตามหลังกริยา build และมีคำคุณศัพท์ great ขยายหน้า ต้องใช้คำนาม (confidence)"),
    ("creativity", "create", "creative", "creatively", "adj",
     "The judges praised {name} for coming up with such a ____ solution to the problem.",
     "วางหน้าคำนาม 'solution' เพื่อขยายนาม ต้องใช้คำคุณศัพท์ (creative)"),
    ("announcement", "announce", "announced", "announcing", "noun",
     "{name} listened quietly to the principal's ____ about the field trip.",
     "อยู่หลังคำแสดงความเป็นเจ้าของ (the principal's) ต้องตามด้วยคำนาม (announcement)"),
    ("patience", "patientness", "patient", "patiently", "adv",
     "{name} and the other passengers waited ____ in the hall while the train was delayed.",
     "ขยายกริยา 'waited' (รอคอยอย่างอดทน) ต้องใช้ Adverb (patiently)"),
]

_ED_ING_PAIRS = [
    ("interested", "interesting", "interest", "interestingly", "astronomy documentary", "in learning about black holes"),
    ("excited", "exciting", "excite", "excitedly", "championship match", "about the upcoming camping trip"),
    ("exhausted", "exhausting", "exhaust", "exhaustingly", "four-hour hike", "after carrying the heavy backpack"),
    ("amazed", "amazing", "amaze", "amazingly", "magic performance", "by the magician's final trick"),
    ("confused", "confusing", "confuse", "confusingly", "subway map", "by the complicated directions"),
    ("disappointed", "disappointing", "disappoint", "disappointingly", "rainy weather", "with the cancelled picnic"),
]


@template("e.vocab.wordform", "medium")
def _vocab_wordform_pos():
    name, _ = name_en()
    noun, verb, adj, adv, target_pos, sent_tmpl, exp = pick(_WF_FAMILIES)
    sent = sent_tmpl.format(name=name)
    pos_map = {"noun": noun, "verb": verb, "adj": adj, "adv": adv}
    correct = pos_map[target_pos]
    wrongs = []
    if target_pos != "adj":
        wrongs.append(W(adj, f"'{adj}' เป็นคำคุณศัพท์ (Adjective) แต่ตำแหน่งนี้{exp}", "form"))
    if target_pos != "adv":
        wrongs.append(W(adv, f"'{adv}' เป็นกริยาวิเศษณ์ (Adverb) แต่ตำแหน่งนี้{exp}", "form"))
    if target_pos != "noun":
        wrongs.append(W(noun, f"'{noun}' เป็นคำนาม (Noun) แต่ตำแหน่งนี้{exp}", "form"))
    if target_pos != "verb" and verb != noun and verb != adj:
        wrongs.append(W(verb, f"'{verb}' เป็นคำกริยา (Verb) ไม่ตรงกับหน้าที่ของคำในช่องว่าง", "form"))
    return mcq(
        stem=f"Choose the correct word form to complete the sentence:\n{sent}",
        correct=correct,
        wrongs=wrongs,
        hint="ดูคำข้างหน้าและข้างหลังช่องว่าง เพื่อระบุว่าต้องการ Noun, Verb, Adjective หรือ Adverb (-ly)",
        steps=[exp, f"ดังนั้นรูปคำที่ถูกต้องคือ '{correct}'"],
    )


@template("e.vocab.wordform", "hard")
def _vocab_wordform_ed_vs_ing():
    name, _ = name_en()
    ed, ing, base_v, adv, thing_np, person_tail = pick(_ED_ING_PAIRS)
    if random.random() < 0.5:
        return mcq(
            stem=f"The {thing_np} was so ____ that {name} talked about it all evening.",
            correct=ing,
            wrongs=[
                W(ed, f"ประธานคือ '{thing_np}' (สิ่งของ/เหตุการณ์) ซึ่งเป็นตัวทำให้เกิดความรู้สึก ต้องใช้รูป -ing ('{ing}') ไม่ใช่ -ed", "trap"),
                W(base_v, f"หลัง 'was so' ต้องเป็นคำคุณศัพท์ ไม่ใช่กริยาช่อง 1 ('{base_v}')", "form"),
                W(adv, "หลัง Verb to be (was) ต้องใช้คำคุณศัพท์ขยายประธาน ไม่ใช้ Adverb (-ly)", "form"),
            ],
            hint=f"ช่องว่างขยาย '{thing_np}' (สิ่งของ/เหตุการณ์) ว่าเป็นสิ่งที่ 'น่า...' ใช้ -ed หรือ -ing?",
            steps=[
                f"ประธานที่ถูกขยายคือ 'The {thing_np}' ซึ่งเป็นสิ่งของ/เหตุการณ์ (น่า...)",
                f"จึงต้องใช้ Present Participle Adjective ที่ลงท้ายด้วย -ing คือ '{ing}'",
            ],
        )
    return mcq(
        stem=f"{name} felt very ____ {person_tail}.",
        correct=ed,
        wrongs=[
            W(ing, f"ประธานคือ '{name}' (บุคคลผู้รู้สึก) ต้องใช้คำคุณศัพท์ลงท้ายด้วย -ed ('{ed}') ไม่ใช่ -ing", "trap"),
            W(base_v, "หลังกริยาเชื่อม 'felt very' ต้องตามด้วยคำคุณศัพท์", "form"),
            W(adv, "หลัง linking verb 'felt' ต้องใช้ Adjective บอกความรู้สึก ไม่ใช่ Adverb (-ly)", "form"),
        ],
        hint=f"ประธานคือ '{name}' ซึ่งเป็นคนที่มีความรู้สึกนั้นเอง ใช้ -ed หรือ -ing?",
        steps=[
            f"ประธาน '{name}' เป็นบุคคลผู้ได้รับความรู้สึก (รู้สึก...)",
            f"จึงต้องใช้ Past Participle Adjective ที่ลงท้ายด้วย -ed คือ '{ed}'",
        ],
    )


# ---------------------------------------------------------------------------
# 5. Collocations & Verb Phrases (e.vocab.collocation)
# ---------------------------------------------------------------------------

skill(
    "e.vocab.collocation", "e.vocab", "Collocations (คำที่มักใช้คู่กัน: make/do/take/have)",
    lesson={
        "concept": "Collocation คือคำที่เจ้าของภาษาใช้คู่กันเสมอ แปลตรงตัวจากภาษาไทยไม่ได้ เช่น make a mistake / make a decision / make progress แต่ใช้ do homework / do a favor / do research และ take a break / take an exam / take medicine",
        "steps": [
            "ดูคำนามที่อยู่หลังช่องว่าง แล้วนึกคู่กริยาที่ติดกันเป็นสำนวน",
            "แยกกลุ่ม do (งาน/หน้าที่/กิจวัตร: do homework, do housework, do an experiment) ออกจาก make (การสร้าง/ตัดสินใจ/ผลลัพธ์: make a noise, make an effort, make a mistake)",
        ],
        "example": {
            "q": "Please don't ____ a loud noise while the baby is sleeping.",
            "steps": [
                "คำนามข้างหลังคือ a loud noise",
                "สำนวนส่งเสียงดังใช้ make a noise",
            ],
            "a": "make",
        },
        "mistakes": [
            "แปลตรงตัวจากภาษาไทยว่า 'ทำการบ้าน / ทำความผิดพลาด / ทำการตัดสินใจ' แล้วใช้ do กับทุกคำ",
        ],
        "tips": ["ท่องชุดออกสอบบ่อย: make a mistake / decision / effort / progress / noise | do homework / housework / a favor / research | take a photo / a break / medicine"],
    },
    weight=1.3,
)

_COLLOC_BANK = [
    ("make", "do", "take", "have", "a big mistake", "ทำผิดพลาด ใช้ make a mistake (ไม่ใช้ do)"),
    ("make", "do", "take", "get", "a final decision", "ตัดสินใจ ใช้ make a decision"),
    ("make", "do", "play", "keep", "great progress", "มีความก้าวหน้า ใช้ make progress"),
    ("make", "do", "take", "give", "an effort", "พยายาม ใช้ make an effort"),
    ("make", "do", "have", "take", "a loud noise", "ส่งเสียงดัง ใช้ make a noise"),
    ("do", "make", "take", "build", "the science experiment", "ทำการทดลอง ใช้ do an experiment"),
    ("do", "make", "give", "keep", "me a favor", "ช่วยเหลือฉันหน่อย ใช้ do (someone) a favor"),
    ("do", "make", "take", "play", "the household chores", "ทำงานบ้าน ใช้ do the chores / housework"),
    ("take", "make", "do", "eat", "this cough medicine", "กินยา ใช้สำนวน take medicine (ไม่ใช้ eat medicine)"),
    ("take", "make", "do", "work", "a short break", "พักเบรก ใช้ take a break"),
    ("take", "do", "make", "draw", "a group photo", "ถ่ายรูป ใช้ take a photo"),
    ("pay", "give", "make", "take", "close attention", "ตั้งใจฟัง/ใส่ใจ ใช้ pay attention (to)"),
    ("keep", "make", "do", "take", "a secret", "เก็บความลับ ใช้ keep a secret"),
    ("catch", "take", "make", "get", "a bad cold", "เป็นหวัด ใช้สำนวน catch a cold"),
]


@template("e.vocab.collocation", "easy")
def _vocab_collocation_make_do_take():
    name, pron = name_en()
    corr, w1, w2, w3, phrase, exp = pick(_COLLOC_BANK[:11])
    time_tail = pick(["this afternoon", "before dinner", "in the classroom", "during the workshop", "every evening"])
    return mcq(
        stem=f"{name} promised to ____ {phrase} {time_tail}.",
        correct=corr,
        wrongs=[
            W(w1, f"ไม่ใช้ '{w1} {phrase}': {exp}", "trap"),
            W(w2, f"คำกริยาที่เข้าคู่ (Collocation) กับ '{phrase}' คือ '{corr}' ไม่ใช่ '{w2}'", "context"),
            W(w3, f"'{w3}' ไม่ใช่คำที่ใช้คู่กับ '{phrase}' ตามหลักภาษาอังกฤษ", "meaning"),
        ],
        hint=f"คำนาม '{phrase}' ต้องใช้คู่กับกริยาใดตามธรรมชาติของภาษาอังกฤษ (Collocation)?",
        steps=[
            f"สังเกตวลีนาม '{phrase}' หลังช่องว่าง",
            f"{exp} จึงตอบ '{corr}'",
        ],
    )


@template("e.vocab.collocation", "medium")
def _vocab_collocation_phrases_in_context():
    name, pron = name_en()
    corr, w1, w2, w3, phrase, exp = pick(_COLLOC_BANK[4:])
    situations = {
        "a loud noise": f"The librarian asked {name}'s group not to ____ {phrase} in the reading room.",
        "the science experiment": f"{name} put on safety goggles before starting to ____ {phrase}.",
        "me a favor": f"Could you please ____ {phrase} and help {name} carry these books?",
        "the household chores": f"Every Saturday morning, {name} helps her parents ____ {phrase}.",
        "this cough medicine": f"The doctor told {name} to ____ {phrase} after meals twice a day.",
        "a short break": f"After studying for two hours, {name} decided to ____ {phrase} and stretch.",
        "a group photo": f"{name} asked a passerby to ____ {phrase} in front of the monument.",
        "close attention": f"Students should ____ {phrase} to the safety instructions in the lab.",
        "a secret": f"Can you ____ {phrase}? We are planning a surprise birthday party for {name}.",
        "a bad cold": f"Bring an umbrella with you, or you might ____ {phrase} in the rain.",
    }
    return mcq(
        stem=situations[phrase],
        correct=corr,
        wrongs=[
            W(w1, f"คนไทยมักแปลตรงตัวแล้วเผลอใช้ '{w1}' แต่ที่ถูกต้องคือ: {exp}", "trap"),
            W(w2, f"ไม่ใช้ '{w2}' คู่กับ '{phrase}' ({exp})", "context"),
            W(w3, f"'{w3}' ไม่ใช่ Collocation ของ '{phrase}'", "meaning"),
        ],
        hint=f"นึกถึงสำนวนกริยาที่ใช้คู่กับ '{phrase}' เสมอ",
        steps=[exp, f"คำกริยาที่ถูกต้องคือ '{corr}'"],
    )


# ---------------------------------------------------------------------------
# 6. Phrasal Verbs & Confusing Words (e.vocab.phrasal_confuse)
# ---------------------------------------------------------------------------

skill(
    "e.vocab.phrasal_confuse", "e.vocab", "Phrasal Verbs & Confusing Words (กริยาวลีและคำสับสน)",
    lesson={
        "concept": "Phrasal Verb คือกริยา + บุพบทที่เปลี่ยนความหมายไปจากเดิม เช่น look after (ดูแล), look for (มองหา), look up (ค้นคำศัพท์), look forward to (ตั้งตารอ), put off (เลื่อนออกไป), put out (ดับไฟ), give up (ยอมแพ้), run out of (หมด) รวมถึงคู่คำที่มักสับสน เช่น borrow/lend, bring/take, remind/remember",
        "steps": [
            "ดูบริบทของประโยคว่าต้องการกริยาวลีที่มีความหมายใด (เช่น ไฟไหม้ → ดับไฟ = put out, รถติด → เลื่อนงาน = put off)",
            "ถ้าเป็นคู่คำสับสน ให้เช็กทิศทางหรือโครงสร้าง เช่น borrow (ยืมจาก: borrow from) vs lend (ให้ยืมแก่: lend to)",
        ],
        "example": {
            "q": "The firefighters worked bravely to ____ the forest fire.",
            "steps": [
                "บริบทคือพนักงานดับเพลิงจัดการกับไฟป่า ต้องแปลว่า 'ดับไฟ'",
                "กริยาวลีที่แปลว่าดับไฟคือ put out",
            ],
            "a": "put out",
        },
        "mistakes": [
            "เดาความหมาย Phrasal Verb จากคำบุพบทตรงตัว เช่นคิดว่า put out แปลว่าวางข้างนอก หรือ give up แปลว่าให้ขึ้นไป",
            "สลับ borrow (ขอยืมของคนอื่นมา) กับ lend (ให้คนอื่นยืมของของเราไป)",
        ],
        "tips": ["จัดกลุ่มจำ: look after = ดูแล, look for = หา, look up = ค้นข้อมูล | put on = สวมใส่, put off = เลื่อน, put out = ดับไฟ | turn on/off = เปิด/ปิด, turn up/down = เพิ่ม/ลดเสียง"],
    },
    weight=1.5,
)

_PHRASAL_BANK = [
    ("look after", "ดูแล", "look for", "มองหา", "look up", "ค้นหาคำศัพท์", "look out", "ระวัง",
     "{name} promised to ____ her neighbor's cat while they were away on holiday."),
    ("look up", "ค้นหาข้อมูล/คำศัพท์", "look after", "ดูแล", "look into", "สืบสวน", "look down", "มองลง/ดูถูก",
     "When {name} doesn't know a word, she will ____ it ____ in the dictionary."),
    ("look forward to", "ตั้งตารอคอย", "look up to", "เคารพชื่นชม", "look out for", "ระแวดระวัง", "look back on", "ย้อนนึกถึง",
     "{name} and her classmates really ____ visiting the science museum next Friday."),
    ("put out", "ดับไฟ", "put off", "เลื่อนออกไป", "put on", "สวมใส่", "put away", "เก็บเข้าที่",
     "{name}'s scout group poured buckets of water to ____ the campfire before going to sleep."),
    ("put off", "เลื่อนเวลาออกไป", "put out", "ดับไฟ", "put on", "สวมใส่", "put up", "ติดป้าย/สร้าง",
     "Because of the heavy rainstorm, Coach {name} had to ____ the football match until next week."),
    ("give up", "ยอมแพ้/เลิกทำ", "give in", "ยอมจำนน", "give out", "แจกจ่าย", "give back", "คืนให้",
     "Even though the math puzzle was very hard, {name} refused to ____ and finally solved it."),
    ("run out of", "หมดเกลี้ยง", "run into", "บังเอิญเจอ", "run after", "วิ่งไล่ตาม", "run away", "วิ่งหนี",
     "{name} needs to stop at the grocery store because her family has ____ milk and eggs."),
    ("turn down", "ลดเสียงลง / ปฏิเสธ", "turn up", "เพิ่มเสียง / มาถึง", "turn on", "เปิดเครื่อง", "turn into", "กลายเป็น",
     "Could you please ____ the volume of the television? {name} is studying for tomorrow's exam."),
    ("take off", "ถอดออก / เครื่องบินขึ้น", "take after", "หน้าตาหรือนิสัยเหมือน", "take over", "รับช่วงต่อ", "take up", "เริ่มงานอดิเรกใหม่",
     "Please ____ your muddy shoes before stepping onto the clean carpet in {name}'s room."),
    ("call off", "ยกเลิก", "call on", "แวะเยี่ยม/เรียกถาม", "call up", "โทรศัพท์หา", "call for", "เรียกร้อง",
     "Principal {name} decided to ____ the outdoor parade due to the severe flood warning."),
]

_CONFUSE_BANK = [
    ("borrow", "lend", "rent", "hire",
     "May I ____ your ruler for a moment? {name} left hers in the locker.",
     "ประธาน 'I' เป็นผู้ขอยืมของมาจากผู้ฟัง ต้องใช้ borrow (ส่วน lend แปลว่าให้ยืม)"),
    ("lend", "borrow", "spend", "owe",
     "Could you ____ {name} your umbrella? It is raining heavily outside.",
     "โครงสร้าง 'lend + คน + สิ่งของ' แปลว่าให้ยืม (ส่วน borrow คือขอยืม)"),
    ("remind", "remember", "memorize", "recall",
     "Please ____ {name} to bring the permission slip tomorrow morning.",
     "'remind + บุคคล + to V.1' แปลว่า เตือนความจำคนอื่น (ส่วน remember คือจำได้ด้วยตัวเอง)"),
    ("remember", "remind", "warn", "notice",
     "Did {name} ____ to lock the laboratory door before leaving?",
     "'remember + to V.1' แปลว่า จำได้ที่จะทำด้วยตัวเอง (ไม่มีกรรมเป็นคนตามหลังเหมือน remind)"),
    ("win", "beat", "earn", "gain",
     "{name}'s school team practiced hard and managed to ____ the championship trophy.",
     "ใช้ win คู่กับรางวัล/การแข่งขัน/ถ้วยรางวัล (ส่วน beat ใช้คู่กับคู่ต่อสู้ เช่น beat the other team)"),
    ("beat", "win", "score", "lose",
     "In the final match, {name} managed to ____ the defending champion in straight sets.",
     "ข้างหลังคือคู่แข่ง (the defending champion) ต้องใช้ beat (เอาชนะคู่ต่อสู้) ไม่ใช้ win"),
]


@template("e.vocab.phrasal_confuse", "hard")
def _vocab_phrasal_verbs():
    name, _ = name_en()
    corr, corr_th, w1, w1_th, w2, w2_th, w3, w3_th, sent_tmpl = pick(_PHRASAL_BANK)
    if "____ it ____" in sent_tmpl:
        sent = sent_tmpl.replace("____ it ____", "____ the word").format(name=name)
    else:
        sent = sent_tmpl.format(name=name)
    return mcq(
        stem=f"Choose the best phrasal verb to complete the sentence:\n{sent}",
        correct=corr,
        wrongs=[
            W(w1, f"'{w1}' แปลว่า {w1_th} แต่บริบทนี้ต้องการความหมายว่า '{corr_th}' ({corr})", "trap"),
            W(w2, f"'{w2}' แปลว่า {w2_th} ไม่ตรงกับสถานการณ์ในประโยค", "meaning"),
            W(w3, f"'{w3}' แปลว่า {w3_th} ไม่เข้ากับบริบทของประโยคนี้", "context"),
        ],
        hint="ดูบริบทของประโยคว่าต้องการกริยาวลีที่แปลว่าอะไร อย่าแปลแยกคำตรงตัว",
        steps=[
            f"จากบริบทของประโยค ต้องการกริยาวลีที่แปลว่า '{corr_th}'",
            f"กริยาวลีที่ถูกต้องคือ '{corr}'",
        ],
    )


@template("e.vocab.phrasal_confuse", "challenge")
def _vocab_confusing_pairs():
    name, _ = name_en()
    corr, w_trap, w2, w3, sent_tmpl, exp = pick(_CONFUSE_BANK)
    sent = sent_tmpl.format(name=name)
    return mcq(
        stem=f"Choose the most appropriate word to complete the sentence:\n{sent}",
        correct=corr,
        wrongs=[
            W(w_trap, f"สับสนคู่คำ: {exp}", "trap"),
            W(w2, f"'{w2}' มีความหมายและโครงสร้างไม่ตรงกับบริบทนี้ ({exp})", "meaning"),
            W(w3, f"'{w3}' ไม่สามารถใช้ในความหมายนี้ได้", "context"),
        ],
        hint="สังเกตทิศทางของการกระทำและโครงสร้างคำที่ตามหลังช่องว่าง (เช่น มีกรรมเป็นคนหรือสิ่งของ)",
        steps=[exp, f"ดังนั้นคำตอบที่ถูกต้องคือ '{corr}'"],
    )
