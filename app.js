/* Suankularb M.1 Practice App */
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
  const LETTERS_TH = ["ก", "ข", "ค", "ง"];
  const LETTERS_EN = ["A", "B", "C", "D"];
  const DIFF_TH = { easy: "ง่าย", medium: "ปานกลาง", hard: "ยาก" };

  /** @type {{mode:string, questions:any[], answers:(number|null)[], index:number, remaining:number|null, totalSeconds:number|null, allowPause:boolean, paused:boolean, timerId:number|null, startedAt:number, practiceSubject?:string, practiceTopic?:string}} */
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

  function pickQuestions(pool, n) {
    if (pool.length <= n) return shuffle(pool);
    return shuffle(pool).slice(0, n);
  }

  function buildExamSet(mode) {
    const math = window.MATH_QUESTIONS || [];
    const eng = window.ENGLISH_QUESTIONS || [];
    if (mode === "math") return pickQuestions(math, 30);
    if (mode === "english") return pickQuestions(eng, 30);
    // combined: 30 math then 30 english (sectioned)
    return pickQuestions(math, 30).concat(pickQuestions(eng, 30));
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
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function saveHistory(entry) {
    const list = loadHistory();
    list.unshift(entry);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(list.slice(0, 10)));
  }

  function renderHistory() {
    const list = loadHistory();
    const ul = $("#history-list");
    const empty = $("#history-empty");
    if (!list.length) {
      ul.classList.add("hidden");
      empty.classList.remove("hidden");
      return;
    }
    empty.classList.add("hidden");
    ul.classList.remove("hidden");
    ul.innerHTML = list
      .map((h) => {
        const d = new Date(h.at);
        const dateStr = d.toLocaleString("th-TH", {
          dateStyle: "medium",
          timeStyle: "short",
        });
        return `<li>
          <span><strong>${escapeHtml(h.label)}</strong><br/><span style="color:var(--muted);font-size:0.85rem">${escapeHtml(dateStr)}</span></span>
          <span class="score">${h.percent}% · ${h.correct}/${h.total}</span>
        </li>`;
      })
      .join("");
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
    const questions = shuffle(pool);
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
    // leave unanswered, move next
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

    saveHistory({
      at: Date.now(),
      label: state.label + (auto ? " (หมดเวลา)" : ""),
      mode: state.mode,
      percent,
      correct,
      total,
      usedSec,
    });

    $("#result-title").textContent = auto ? "หมดเวลา — สรุปคะแนน" : "สรุปคะแนน";
    $("#result-percent").textContent = percent + "%";
    $("#result-summary").textContent =
      "ได้ " + correct + " จาก " + total + " ข้อ · " + state.label;
    $("#stat-correct").textContent = String(correct);
    $("#stat-wrong").textContent = String(wrong);
    $("#stat-blank").textContent = String(blank);
    $("#stat-time").textContent = formatTime(usedSec);

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
          <div class="status">ข้อ ${i + 1} · ${status}</div>
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
          renderTopicChips();
          return;
        }
        startExamMode(mode);
      });
    });

    $$("#subject-chips .chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        practiceSubject = btn.getAttribute("data-subject");
        $$("#subject-chips .chip").forEach((c) =>
          c.classList.toggle("active", c === btn)
        );
        renderTopicChips();
      });
    });

    $("#btn-start-practice").addEventListener("click", startPractice);
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
        startPractice();
      } else {
        startExamMode(m);
      }
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
