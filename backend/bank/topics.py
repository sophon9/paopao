"""Topic list (display order) and the exam blueprints that use them.

Content modules register skills under these topic keys.
"""

from backend.bank.core import topic

# ---- Math -----------------------------------------------------------------
topic("m.num", "math", "จำนวนและตัวประกอบ", "🔢",
      "ค่าประจำหลัก ลำดับการคำนวณ จำนวนเฉพาะ ห.ร.ม. ค.ร.น. การหารลงตัว จำนวนเต็ม เลขยกกำลัง")
topic("m.frac", "math", "เศษส่วนและทศนิยม", "🍰",
      "เปรียบเทียบ บวก ลบ คูณ หาร เศษส่วน/ทศนิยม และโจทย์ปัญหาเศษส่วน")
topic("m.ratio", "math", "อัตราส่วนและร้อยละ", "⚖️",
      "อัตราส่วน สัดส่วน มาตราส่วน ร้อยละ ลดราคา กำไร-ขาดทุน ดอกเบี้ย")
topic("m.alg", "math", "แบบรูปและสมการ", "🧩",
      "แบบรูปของจำนวน/รูป สมการเชิงเส้น และการเขียนสมการจากโจทย์")
topic("m.geo", "math", "เรขาคณิต", "📐",
      "มุม เส้นขนาน รูปสามเหลี่ยม รูปหลายเหลี่ยม วงกลม สมบัติของรูป รูปเรขาคณิตสามมิติ")
topic("m.meas", "math", "การวัด พื้นที่ และปริมาตร", "📏",
      "ความยาวรอบรูป พื้นที่ พื้นที่แรเงา ปริมาตรและความจุ การแปลงหน่วย")
topic("m.data", "math", "สถิติ กราฟ และความน่าจะเป็น", "📊",
      "ค่าเฉลี่ย มัธยฐาน ฐานนิยม การอ่านแผนภูมิแท่ง/วงกลม/กราฟเส้น ความน่าจะเป็นเบื้องต้น")
topic("m.word", "math", "โจทย์ปัญหาและการคิดวิเคราะห์", "🧠",
      "ความเร็ว งาน อายุ เวลา-ปฏิทิน การนับ ตรรกะ และโจทย์หลายขั้นตอน")

# ---- English --------------------------------------------------------------
topic("e.gram", "english", "Grammar ไวยากรณ์", "✍️",
      "Tenses, subject-verb agreement, pronouns, articles, prepositions, comparison, modals, conjunctions")
topic("e.vocab", "english", "Vocabulary คำศัพท์", "📚",
      "Meaning in context, synonyms/antonyms, word forms, collocations, phrasal verbs")
topic("e.conv", "english", "Conversation บทสนทนา", "💬",
      "Situational responses and dialogue completion")
topic("e.read", "english", "Reading การอ่าน", "📖",
      "Details, main idea, inference, vocabulary in context, reference words, signs and notices")
topic("e.write", "english", "Sentence & Error โครงสร้างประโยค", "🔍",
      "Error identification, sentence order, combining sentences, question forms")


# ---------------------------------------------------------------------------
# Exam blueprints: (topic, count). Difficulty mix applies within each topic.
# Modelled on top-school M.1 entrance papers (Suankularb, Triam Noi/MWIT
# feeder programmes, Satit, Gifted): more multi-step and analysis items
# than school tests.
# ---------------------------------------------------------------------------

MOCK = {
    "math": {
        "label": "ข้อสอบจำลอง คณิตศาสตร์",
        "seconds": 60 * 60,
        "plan": [("m.num", 4), ("m.frac", 4), ("m.ratio", 4), ("m.alg", 4),
                 ("m.geo", 3), ("m.meas", 4), ("m.data", 3), ("m.word", 4)],
        "mix": {"easy": 0.15, "medium": 0.40, "hard": 0.33, "challenge": 0.12},
    },
    "english": {
        "label": "ข้อสอบจำลอง ภาษาอังกฤษ",
        "seconds": 50 * 60,
        "plan": [("e.gram", 12), ("e.vocab", 8), ("e.conv", 6), ("e.write", 5), ("e.read", 9)],
        "mix": {"easy": 0.15, "medium": 0.45, "hard": 0.30, "challenge": 0.10},
    },
}

DIAGNOSTIC = {
    "math": {"label": "วัดระดับ คณิตศาสตร์", "per_topic": 3, "seconds": None},
    "english": {"label": "วัดระดับ ภาษาอังกฤษ", "per_topic": 4, "seconds": None},
}

# Expected seconds per item by difficulty — used for pace analysis.
TARGET_SECONDS = {
    "math": {"easy": 50, "medium": 100, "hard": 150, "challenge": 210},
    "english": {"easy": 30, "medium": 50, "hard": 75, "challenge": 95},
}
