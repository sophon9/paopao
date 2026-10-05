/* Suankularb M.1 Practice App
   Each paper is a new random set: questions are drawn across topics,
   order is shuffled, and choices are reshuffled so students analyze
   instead of memorizing a letter. History keeps topic results so the
   home screen can show what to practice next.
*/
(function () {
  "use strict";

  const MATH_TOPICS = [
    "จำนวนและการดำเนินการ",
    "ทศนิยมเศษส่วน",
    "อัตราส่วนร้อยละ",
    "สมการ",
    "เรขาคณิตพื้นที่ปริมาตร",
    "สถิติโจทย์ปัญหา",
  ];

  const ENG_TOPICS = [
    "Grammar/Tenses",
    "Vocabulary",
    "Conversation",
    "Reading",
  ];

  const MODE_CONFIG = {
    math: { label: "คณิตศาสตร์", count: 30, seconds: 40 * 60, subjects: ["math"] },
    english: { label: "ภาษาอังกฤษ", count: 30, seconds: 35 * 60, subjects: ["english"] },
    combined: { label: "สอบรวม", count: 60, seconds: 75 * 60, subjects: ["math", "english"] },
  };

  const HISTORY_KEY = "sk_m1_history_v1";
  const SEEN_KEY = "sk_m1_seen_v1";
  const HISTORY_LIMIT = 30;
  /* Remember about one paper's worth so the next set prefers unseen items. */
  const SEEN_CAP = 24;
  const LETTERS_TH = ["ก", "ข", "ค", "ง"];
  const LETTERS_EN = ["A", "B", "C", "D"];
  const DIFF_TH = { easy: "ง่าย", medium: "ปานกลาง", hard: "ยาก" };

  /** @type {{mode:string, label:string, questions:any[], answers:(number|null)[], index:number, remaining:number|null, totalSeconds:number|null, allowPause:boolean, paused:boolean, timerId:number|null, startedAt:number, practiceSubject?:string, practiceTopic?:string}|null} */
  let state = null;

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  /* Move the correct choice to a new slot without changing the question text. */
  function presentQuestion(q) {
    const order = shuffle(q.choices.map((_, i) => i));
    return {
      id: q.id,
      subject: q.subject,
      topic: q.topic,
      difficulty: q.difficulty,
      stem: q.stem,
      passage: q.passage,
      choices: order.map((i) => q.choices[i]),
      answerIndex: order.indexOf(q.answerIndex),
      explanation: q.explanation,
    };
  }

  function loadSeen(subject) {
    try {
      const raw = JSON.parse(localStorage.getItem(SEEN_KEY) || "{}");
      const list = raw && Array.isArray(raw[subject]) ? raw[subject] : [];
      return list.filter((id) => typeof id === "string");
    } catch {
      return [];
    }
  }

  function rememberSeen(questions) {
    let raw = {};
    try {
      raw = JSON.parse(localStorage.getItem(SEEN_KEY) || "{}") || {};
    } catch {
      raw = {};
    }
    ["math", "english"].forEach((subject) => {
      const ids = questions.filter((q) => q.subject === subject).map((q) => q.id);
      if (!ids.length) return;
      const idSet = new Set(ids);
      const prev = (Array.isArray(raw[subject]) ? raw[subject] : []).filter((id) => !idSet.has(id));
      raw[subject] = prev.concat(ids).slice(-SEEN_CAP);
    });
    localStorage.setItem(SEEN_KEY, JSON.stringify(raw));
  }

  function groupByTopic(pool) {
    const map = new Map();
    pool.forEach((q) => {
      if (!map.has(q.topic)) map.set(q.topic, []);
      map.get(q.topic).push(q);
    });
    return Array.from(map.values());
  }

  /* Spread a paper across topics the way a real exam does, then fill leftovers. */
  function allocateCounts(groups, n) {
    const total = groups.reduce((sum, g) => sum + g.length, 0);
    if (total <= n) return groups.map((g) => g.length);
    const raw = groups.map((g) => (g.length / total) * n);
    const counts = raw.map((x, i) => Math.min(groups[i].length, Math.floor(x)));
    let left = n - counts.reduce((sum, c) => sum + c, 0);
    const order = raw
      .map((x, i) => ({ i, frac: x - Math.floor(x) }))
      .sort((a, b) => b.frac - a.frac);
    let guard = 0;
    while (left > 0 && guard < groups.length * 4) {
      guard += 1;
      let placed = false;
      for (const slot of order) {
        if (left <= 0) break;
        if (counts[slot.i] < groups[slot.i].length) {
          counts[slot.i] += 1;
          left -= 1;
          placed = true;
        }
      }
      if (!placed) break;
    }
    return counts;
  }

  function takePreferFresh(pool, n, seenSet) {
    const fresh = shuffle(pool.filter((q) => !seenSet.has(q.id)));
    const stale = shuffle(pool.filter((q) => seenSet.has(q.id)));
    return fresh.concat(stale).slice(0, Math.min(n, pool.length));
  }

  function buildSubjectPaper(pool, n) {
    if (!pool.length) return [];
    const subject = pool[0].subject;
    const seenSet = new Set(loadSeen(subject));
    const groups = groupByTopic(pool);
    const counts = allocateCounts(groups, n);
    const picked = [];
    groups.forEach((group, i) => {
      takePreferFresh(group, counts[i], seenSet).forEach((q) => picked.push(q));
    });
    return shuffle(picked).map(presentQuestion);
  }

  function buildExamSet(mode) {
    const math = window.MATH_QUESTIONS || [];
    const eng = window.ENGLISH_QUESTIONS || [];
    if (mode === "math") return buildSubjectPaper(math, MODE_CONFIG.math.count);
    if (mode === "english") return buildSubjectPaper(eng, MODE_CONFIG.english.count);
    /* Combined keeps two sections, like the real sitting, but each section is a new paper. */
    return buildSubjectPaper(math, MODE_CONFIG.math.count).concat(
      buildSubjectPaper(eng, MODE_CONFIG.english.count)
    );
  }

  function formatTime(sec) {
    if (sec == null || sec < 0) sec = 0;
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return m + ":" + String(s).padStart(2, "0");
  }

  function showScreen(id) {
    ["screen-home", "screen-exam", "screen-results"].forEach((sid) => {
      const el = document.getElementById(sid);
      if (el) el.classList.toggle("hidden", sid !== id);
    });
  }

  function loadHistory() {
    try {
      const raw = localStorage.getItem(HISTORY_KEY);
      const list = raw ? JSON.parse(raw) : [];
      return Array.isArray(list) ? list : [];
    } catch {
      return [];
    }
  }

  function saveHistory(entry) {
    const list = loadHistory();
    list.unshift(entry);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(list.slice(0, HISTORY_LIMIT)));
  }

  function topicRows(questions, answers) {
    const map = new Map();
    questions.forEach((q, i) => {
      const key = q.subject + "\0" + q.topic;
      if (!map.has(key)) {
        map.set(key, {
          subject: q.subject,
          topic: q.topic,
          correct: 0,
          wrong: 0,
          blank: 0,
          total: 0,
        });
      }
      const row = map.get(key);
      row.total += 1;
      if (answers[i] == null) row.blank += 1;
      else if (answers[i] === q.answerIndex) row.correct += 1;
      else row.wrong += 1;
    });
    return Array.from(map.values());
  }

  function percentOf(row) {
    return row.total ? Math.round((row.correct / row.total) * 100) : 0;
  }

  function aggregateTopics(list) {
    const map = new Map();
    list.forEach((entry) => {
      (entry.topics || []).forEach((t) => {
        const key = t.subject + "\0" + t.topic;
        if (!map.has(key)) {
          map.set(key, { subject: t.subject, topic: t.topic, correct: 0, total: 0 });
        }
        const row = map.get(key);
        row.correct += Number(t.correct) || 0;
        row.total += Number(t.total) || 0;
      });
    });
    return Array.from(map.values())
      .filter((t) => t.total > 0)
      .map((t) => ({ ...t, percent: percentOf(t) }))
      .sort((a, b) => a.percent - b.percent || b.total - a.total);
  }

  function weakestTopics(rows, limit) {
    return rows
      .slice()
      .sort((a, b) => percentOf(a) - percentOf(b) || b.total - a.total)
      .slice(0, limit);
  }

  function subjectPrefix(subject) {
    return subject === "english" ? "อังกฤษ" : "คณิต";
  }

  function renderTopicBars(el, rows) {
    if (!el) return;
    const ordered = rows.slice().sort((a, b) => percentOf(a) - percentOf(b) || b.total - a.total);
    el.innerHTML = ordered
      .map((t) => {
        const pct = percentOf(t);
        const level = pct < 50 ? "low" : pct < 75 ? "mid" : "high";
        const name = subjectPrefix(t.subject) + " · " + t.topic;
        return `<div class="topic-bar-row">
          <span class="topic-name">${escapeHtml(name)}</span>
          <span class="bar-track" aria-hidden="true"><span class="bar-fill ${level}" style="width:${pct}%"></span></span>
          <span class="topic-pct">${pct}% <span class="topic-frac">${t.correct}/${t.total}</span></span>
        </div>`;
      })
      .join("");
  }

  function trendText(list) {
    if (list.length < 2) {
      return "ชุดแรกเสร็จแล้ว ทำชุดถัดไปได้เลย — ข้อและตัวเลือกจะถูกสุ่มใหม่ เพื่อดูว่าวิเคราะห์ได้ดีขึ้นไหม";
    }
    const latest = list[0];
    const prevSame = list.slice(1).find((h) => h.mode === latest.mode);
    const prev = prevSame || list[1];
    const delta = latest.percent - prev.percent;
    const which = prevSame ? "ครั้งก่อนในโหมดเดียวกัน" : "ชุดก่อนหน้า";
    if (delta > 0) return "คะแนนล่าสุดสูงกว่า" + which + " " + delta + " จุด — กำลังพัฒนา";
    if (delta < 0) {
      return "คะแนนล่าสุดต่ำกว่า" + which + " " + Math.abs(delta) + " จุด — กลับไปฝึกหัวข้อด้านล่างก่อนสอบชุดใหม่";
    }
    return "คะแนนล่าสุดเท่ากับ" + which + " — ลองชุดสุ่มชุดใหม่เพื่อยืนยันว่าคิดได้จริง ไม่ใช่จำข้อ";
  }

  function renderHistory() {
    const list = loadHistory();
    const ul = $("#history-list");
    const empty = $("#history-empty");
    if (!list.length) {
      ul.classList.add("hidden");
      empty.classList.remove("hidden");
      ul.innerHTML = "";
    } else {
      empty.classList.add("hidden");
      ul.classList.remove("hidden");
      ul.innerHTML = list
        .map((h, index) => {
          const d = new Date(h.at);
          const dateStr = d.toLocaleString("th-TH", {
            dateStyle: "medium",
            timeStyle: "short",
          });
          const prevSame = list.slice(index + 1).find((item) => item.mode === h.mode);
          let deltaHtml = "";
          if (prevSame && typeof h.percent === "number" && typeof prevSame.percent === "number") {
            const delta = h.percent - prevSame.percent;
            if (delta > 0) deltaHtml = `<span class="delta up">+${delta}</span>`;
            else if (delta < 0) deltaHtml = `<span class="delta down">${delta}</span>`;
            else deltaHtml = `<span class="delta flat">เท่าเดิม</span>`;
          }
          const weak = weakestTopics(h.topics || [], 2).filter((t) => percentOf(t) < 80);
          const weakHtml = weak.length
            ? `<span class="weak-inline">ควรทบทวน: ${escapeHtml(weak.map((t) => t.topic).join(", "))}</span>`
            : "";
          return `<li>
            <span>
              <strong>${escapeHtml(h.label)}</strong>
              <span class="when">${escapeHtml(dateStr)}</span>
              ${weakHtml}
            </span>
            <span class="score">${h.percent}% · ${h.correct}/${h.total} ${deltaHtml}</span>
          </li>`;
        })
        .join("");
    }
    renderInsights(list);
  }

  function renderInsights(list) {
    const empty = $("#insight-empty");
    const body = $("#insight-body");
    if (!list.length) {
      empty.classList.remove("hidden");
      body.classList.add("hidden");
      return;
    }
    empty.classList.add("hidden");
    body.classList.remove("hidden");
    const avg = Math.round(list.reduce((sum, h) => sum + (Number(h.percent) || 0), 0) / list.length);
    $("#insight-summary").textContent = "ทำไปแล้ว " + list.length + " ชุด · คะแนนเฉลี่ย " + avg + "%";
    $("#insight-trend").textContent = trendText(list);

    const topics = aggregateTopics(list);
    const weakBox = $("#weak-list");
    const drill = $("#btn-practice-weak");
    if (!topics.length) {
      weakBox.innerHTML = `<p class="history-empty">ชุดที่บันทึกไว้ก่อนหน้านี้ยังไม่มีคะแนนรายหัวข้อ ทำอีกหนึ่งชุดแล้วจะเห็นว่าควรฝึกบทไหน</p>`;
      drill.classList.add("hidden");
      return;
    }
    renderTopicBars(weakBox, topics.slice(0, 4));
    const worst = topics[0];
    drill.classList.remove("hidden");
    drill.textContent = "ฝึกหัวข้อที่ควรพัฒนา: " + worst.topic;
    drill.dataset.subject = worst.subject;
    drill.dataset.topic = worst.topic;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* ---------- Practice panel ---------- */
  let practiceSubject = "math";
  let practiceTopic = MATH_TOPICS[0];

  function syncSubjectChips() {
    $$("#subject-chips .chip").forEach((c) => {
      c.classList.toggle("active", c.getAttribute("data-subject") === practiceSubject);
    });
  }

  function renderTopicChips() {
    const topics = practiceSubject === "math" ? MATH_TOPICS : ENG_TOPICS;
    if (!topics.includes(practiceTopic)) practiceTopic = topics[0];
    const box = $("#topic-chips");
    box.innerHTML = topics
      .map(
        (t) =>
          `<button type="button" class="chip${t === practiceTopic ? " active" : ""}" data-topic="${escapeHtml(t)}">${escapeHtml(t)}</button>`
      )
      .join("");
    box.querySelectorAll(".chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        practiceTopic = btn.getAttribute("data-topic");
        renderTopicChips();
      });
    });
  }

  function startPractice() {
    const pool =
      practiceSubject === "math"
        ? (window.MATH_QUESTIONS || []).filter((q) => q.topic === practiceTopic)
        : (window.ENGLISH_QUESTIONS || []).filter((q) => q.topic === practiceTopic);
    if (!pool.length) {
      alert("ยังไม่มีข้อในหัวข้อนี้");
      return;
    }
    const questions = shuffle(pool).map(presentQuestion);
    const useTimer = $("#practice-timer-on").checked;
    const seconds = useTimer ? Math.max(60, Math.round(questions.length * 72)) : null;
    beginSession({
      mode: "practice",
      label: "ฝึก: " + practiceTopic,
      questions,
      seconds,
      allowPause: true,
      practiceSubject,
      practiceTopic,
    });
  }

  function startTopicDrill(subject, topic) {
    practiceSubject = subject === "english" ? "english" : "math";
    practiceTopic = topic;
    syncSubjectChips();
    renderTopicChips();
    const panel = $("#practice-panel");
    if (panel) panel.classList.remove("hidden");
    startPractice();
  }

  /* ---------- Session ---------- */
  function beginSession({ mode, label, questions, seconds, allowPause, practiceSubject: ps, practiceTopic: pt }) {
    clearTimer();
    state = {
      mode,
      label: label || (MODE_CONFIG[mode] && MODE_CONFIG[mode].label) || mode,
      questions,
      answers: questions.map(() => null),
      index: 0,
      remaining: seconds,
      totalSeconds: seconds,
      allowPause: !!allowPause,
      paused: false,
      timerId: null,
      startedAt: Date.now(),
      practiceSubject: ps,
      practiceTopic: pt,
    };
    showScreen("screen-exam");
    $("#btn-pause").classList.toggle("hidden", !allowPause || seconds == null);
    $("#exam-timer").classList.toggle("hidden", seconds == null);
    if (seconds == null) {
      $("#exam-timer").textContent = "—";
    } else {
      updateTimerDisplay();
      startTimer();
    }
    renderExam();
  }

  function startExamMode(mode) {
    const cfg = MODE_CONFIG[mode];
    const questions = buildExamSet(mode);
    beginSession({
      mode,
      label: cfg.label,
      questions,
      seconds: cfg.seconds,
      allowPause: false,
    });
  }

  function clearTimer() {
    if (state && state.timerId) {
      clearInterval(state.timerId);
      state.timerId = null;
    }
  }

  function startTimer() {
    clearTimer();
    state.timerId = setInterval(() => {
      if (!state || state.paused) return;
      state.remaining -= 1;
      updateTimerDisplay();
      if (state.remaining <= 0) {
        clearTimer();
        finishExam(true);
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const el = $("#exam-timer");
    if (!state || state.remaining == null) return;
    el.textContent = formatTime(state.remaining);
    el.classList.remove("warn", "danger");
    if (state.remaining <= 60) el.classList.add("danger");
    else if (state.remaining <= 300) el.classList.add("warn");
  }

  function currentSubjectLabel() {
    const q = state.questions[state.index];
    if (state.mode === "combined") {
      return q.subject === "math" ? "สอบรวม · คณิตศาสตร์" : "สอบรวม · ภาษาอังกฤษ";
    }
    if (state.mode === "practice") return "ฝึก · " + q.topic;
    return state.label;
  }

  function lettersFor(q) {
    return q.subject === "english" ? LETTERS_EN : LETTERS_TH;
  }

  function renderExam() {
    if (!state) return;
    const q = state.questions[state.index];
    const n = state.questions.length;
    $("#exam-subject").textContent = currentSubjectLabel();
    $("#exam-progress").textContent = "ข้อ " + (state.index + 1) + " / " + n;
    $("#q-topic").textContent = q.topic;
    const diffEl = $("#q-diff");
    diffEl.textContent = DIFF_TH[q.difficulty] || q.difficulty;
    diffEl.className = "tag diff-" + (q.difficulty || "medium");

    const passage = $("#q-passage");
    if (q.passage) {
      passage.textContent = q.passage;
      passage.classList.remove("hidden");
    } else {
      passage.classList.add("hidden");
      passage.textContent = "";
    }

    $("#q-stem").textContent = q.stem;

    const letters = lettersFor(q);
    const selected = state.answers[state.index];
    const box = $("#q-choices");
    box.innerHTML = q.choices
      .map((c, i) => {
        const sel = selected === i ? " selected" : "";
        return `<button type="button" class="choice${sel}" role="option" aria-selected="${selected === i}" data-index="${i}">
          <span class="letter">${letters[i]}</span>
          <span class="text">${escapeHtml(c)}</span>
        </button>`;
      })
      .join("");

    box.querySelectorAll(".choice").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.getAttribute("data-index"));
        state.answers[state.index] = i;
        renderExam();
      });
    });

    $("#btn-prev").disabled = state.index === 0;
    $("#btn-next").textContent = state.index === n - 1 ? "ส่งคำตอบ" : "ถัดไป →";

    renderGrid();
  }

  function renderGrid() {
    const grid = $("#q-grid");
    grid.innerHTML = state.questions
      .map((_, i) => {
        const classes = [
          "q-dot",
          state.answers[i] != null ? "answered" : "",
          i === state.index ? "current" : "",
        ]
          .filter(Boolean)
          .join(" ");
        return `<button type="button" class="${classes}" data-i="${i}" aria-label="ไปข้อ ${i + 1}">${i + 1}</button>`;
      })
      .join("");
    grid.querySelectorAll(".q-dot").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.index = Number(btn.getAttribute("data-i"));
        renderExam();
      });
    });
  }

  function goNext() {
    if (state.index >= state.questions.length - 1) {
      askSubmit();
      return;
    }
    state.index += 1;
    renderExam();
  }

  function goPrev() {
    if (state.index <= 0) return;
    state.index -= 1;
    renderExam();
  }

  function skip() {
    if (state.index < state.questions.length - 1) {
      state.index += 1;
      renderExam();
    }
  }

  function askSubmit() {
    const blank = state.answers.filter((a) => a == null).length;
    $("#modal-title").textContent = "ยืนยันส่งคำตอบ?";
    $("#modal-body").textContent =
      blank > 0
        ? "ยังมี " + blank + " ข้อที่ยังไม่ได้ตอบ คุณต้องการส่งเลยหรือไม่"
        : "ตอบครบทุกข้อแล้ว ต้องการส่งคำตอบหรือไม่";
    $("#modal").classList.remove("hidden");
    $("#modal-confirm").onclick = () => {
      $("#modal").classList.add("hidden");
      finishExam(false);
    };
  }

  function improveSentence(rows) {
    const weak = weakestTopics(rows, 3).filter((t) => percentOf(t) < 80);
    if (!weak.length) {
      return "ชุดนี้วิเคราะห์ได้ดีทุกหัวข้อ ลองสุ่มชุดใหม่เพื่อยืนยันว่าทำข้อที่ไม่เคยเจอได้เหมือนกัน";
    }
    return "ควรกลับไปฝึกคิดหัวข้อ: " + weak.map((t) => t.topic).join(", ");
  }

  function finishExam(auto) {
    clearTimer();
    if (state) state.paused = false;
    $("#pause-overlay").classList.add("hidden");
    $("#modal").classList.add("hidden");

    const qs = state.questions;
    const ans = state.answers;
    let correct = 0;
    let wrong = 0;
    let blank = 0;
    qs.forEach((q, i) => {
      if (ans[i] == null) blank += 1;
      else if (ans[i] === q.answerIndex) correct += 1;
      else wrong += 1;
    });
    const total = qs.length;
    const percent = total ? Math.round((correct / total) * 100) : 0;
    let usedSec = 0;
    if (state.totalSeconds != null && state.remaining != null) {
      usedSec = Math.max(0, state.totalSeconds - Math.max(0, state.remaining));
    } else {
      usedSec = Math.round((Date.now() - state.startedAt) / 1000);
    }

    const topics = topicRows(qs, ans);
    rememberSeen(qs);
    saveHistory({
      at: Date.now(),
      label: state.label + (auto ? " (หมดเวลา)" : ""),
      mode: state.mode,
      percent,
      correct,
      wrong,
      blank,
      total,
      usedSec,
      topics: topics.map((t) => ({
        subject: t.subject,
        topic: t.topic,
        correct: t.correct,
        wrong: t.wrong,
        blank: t.blank,
        total: t.total,
      })),
    });

    $("#result-title").textContent = auto ? "หมดเวลา — สรุปคะแนน" : "สรุปคะแนน";
    $("#result-percent").textContent = percent + "%";
    $("#result-summary").textContent =
      "ได้ " + correct + " จาก " + total + " ข้อ · " + state.label;
    $("#stat-correct").textContent = String(correct);
    $("#stat-wrong").textContent = String(wrong);
    $("#stat-blank").textContent = String(blank);
    $("#stat-time").textContent = formatTime(usedSec);

    renderTopicBars($("#topic-bars"), topics);
    $("#improve-note").textContent = improveSentence(topics);
    const worst = weakestTopics(topics, 1)[0];
    const drill = $("#btn-drill");
    if (worst && percentOf(worst) < 80) {
      drill.classList.remove("hidden");
      drill.textContent = "ฝึกหัวข้อที่ควรพัฒนา: " + worst.topic;
      drill.dataset.subject = worst.subject;
      drill.dataset.topic = worst.topic;
    } else {
      drill.classList.add("hidden");
    }

    const review = $("#review-list");
    review.innerHTML = qs
      .map((q, i) => {
        const a = ans[i];
        let klass = "blank";
        let status = "ไม่ตอบ";
        if (a != null && a === q.answerIndex) {
          klass = "ok";
          status = "ถูก";
        } else if (a != null) {
          klass = "bad";
          status = "ผิด";
        }
        const letters = lettersFor(q);
        const your =
          a == null ? "—" : letters[a] + ". " + escapeHtml(q.choices[a]);
        const right =
          letters[q.answerIndex] + ". " + escapeHtml(q.choices[q.answerIndex]);
        const passageHtml = q.passage
          ? `<div class="passage" style="margin-bottom:8px">${escapeHtml(q.passage)}</div>`
          : "";
        return `<article class="review-item ${klass}">
          <div class="status">ข้อ ${i + 1} · ${status} · ${escapeHtml(q.topic)}</div>
          ${passageHtml}
          <div class="q-stem">${escapeHtml(q.stem)}</div>
          <div>คำตอบของคุณ: <strong>${your}</strong></div>
          <div>เฉลย: <strong>${right}</strong></div>
          <div class="explain">${escapeHtml(q.explanation || "")}</div>
        </article>`;
      })
      .join("");

    showScreen("screen-results");
    renderHistory();
  }

  function quitExam() {
    $("#modal-title").textContent = "ออกจากการสอบ?";
    $("#modal-body").textContent = "ความคืบหน้าครั้งนี้จะไม่ถูกบันทึกเป็นคะแนน";
    $("#modal").classList.remove("hidden");
    $("#modal-confirm").onclick = () => {
      $("#modal").classList.add("hidden");
      clearTimer();
      state = null;
      showScreen("screen-home");
      renderHistory();
    };
  }

  /* ---------- Keyboard ---------- */
  function onKey(e) {
    if (!state) return;
    if ($("#modal") && !$("#modal").classList.contains("hidden")) return;
    if ($("#pause-overlay") && !$("#pause-overlay").classList.contains("hidden")) return;
    if (document.getElementById("screen-exam").classList.contains("hidden")) return;

    if (e.key === "ArrowRight") {
      e.preventDefault();
      goNext();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      goPrev();
    } else if (["1", "2", "3", "4"].includes(e.key)) {
      e.preventDefault();
      const i = Number(e.key) - 1;
      const q = state.questions[state.index];
      if (i >= q.choices.length) return;
      state.answers[state.index] = i;
      renderExam();
    }
  }

  /* ---------- Wire up ---------- */
  function init() {
    $$(".mode-card[data-mode]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.getAttribute("data-mode");
        if (mode === "practice") {
          $("#practice-panel").classList.toggle("hidden");
          syncSubjectChips();
          renderTopicChips();
          return;
        }
        startExamMode(mode);
      });
    });

    $$("#subject-chips .chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        practiceSubject = btn.getAttribute("data-subject");
        syncSubjectChips();
        renderTopicChips();
      });
    });

    $("#btn-start-practice").addEventListener("click", startPractice);
    $("#btn-practice-weak").addEventListener("click", () => {
      const btn = $("#btn-practice-weak");
      if (!btn.dataset.topic) return;
      startTopicDrill(btn.dataset.subject, btn.dataset.topic);
    });
    $("#btn-prev").addEventListener("click", goPrev);
    $("#btn-next").addEventListener("click", goNext);
    $("#btn-skip").addEventListener("click", skip);
    $("#btn-submit").addEventListener("click", askSubmit);
    $("#btn-quit-exam").addEventListener("click", quitExam);
    $("#modal-cancel").addEventListener("click", () => {
      $("#modal").classList.add("hidden");
    });
    $("#btn-home").addEventListener("click", () => {
      state = null;
      showScreen("screen-home");
      renderHistory();
    });
    $("#btn-retry").addEventListener("click", () => {
      if (!state) {
        showScreen("screen-home");
        return;
      }
      const m = state.mode;
      if (m === "practice") {
        practiceSubject = state.practiceSubject || "math";
        practiceTopic = state.practiceTopic || MATH_TOPICS[0];
        syncSubjectChips();
        renderTopicChips();
        startPractice();
      } else {
        startExamMode(m);
      }
    });
    $("#btn-drill").addEventListener("click", () => {
      const btn = $("#btn-drill");
      if (!btn.dataset.topic) return;
      startTopicDrill(btn.dataset.subject, btn.dataset.topic);
    });

    $("#btn-pause").addEventListener("click", () => {
      if (!state || !state.allowPause) return;
      state.paused = true;
      $("#pause-overlay").classList.remove("hidden");
    });
    $("#btn-resume").addEventListener("click", () => {
      if (!state) return;
      state.paused = false;
      $("#pause-overlay").classList.add("hidden");
    });

    document.addEventListener("keydown", onKey);
    renderTopicChips();
    renderHistory();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
