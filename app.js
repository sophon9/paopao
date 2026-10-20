/* Suankularb M.1 practice.
   Papers come from the local backend. Each question is stored once and
   is never placed on another paper. */
(function () {
  "use strict";

  const LETTERS_TH = ["ก", "ข", "ค", "ง"];
  const LETTERS_EN = ["A", "B", "C", "D"];
  const DIFF_TH = { easy: "ง่าย", medium: "ปานกลาง", hard: "ยาก" };

  let topics = {
    math: [
      "จำนวนและการดำเนินการ",
      "ทศนิยมเศษส่วน",
      "อัตราส่วนร้อยละ",
      "สมการ",
      "เรขาคณิตพื้นที่ปริมาตร",
      "สถิติโจทย์ปัญหา",
    ],
    english: ["Grammar/Tenses", "Vocabulary", "Conversation", "Reading"],
  };

  /** @type {object|null} */
  let state = null;
  let loading = false;
  let practiceSubject = "math";
  let practiceTopic = topics.math[0];
  let lastResult = null;
  let reviewFilter = "all";
  let viewingHistory = false;

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  async function api(url, options) {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || "เชื่อมต่อเซิร์ฟเวอร์ไม่ได้");
    }
    return data;
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

  function showBusy(text) {
    $("#busy-text").textContent = text || "กำลังสร้างชุดข้อสอบใหม่";
    $("#busy").classList.remove("hidden");
  }

  function hideBusy() {
    $("#busy").classList.add("hidden");
  }

  function renderTopicBars(el, rows) {
    if (!el) return;
    el.innerHTML = (rows || [])
      .map((t) => {
        const pct = Math.max(0, Math.min(100, Number(t.percent) || 0));
        return `<div class="topic-bar">
          <span class="name">${escapeHtml(t.topic)}</span>
          <span class="score">${t.correct}/${t.total} · ${pct}%</span>
          <div class="track"><div class="fill" style="width:${pct}%"></div></div>
        </div>`;
      })
      .join("");
  }

  function renderHistory(list) {
    const ul = $("#history-list");
    const empty = $("#history-empty");
    const hint = $("#history-hint");
    if (!list.length) {
      ul.classList.add("hidden");
      empty.classList.remove("hidden");
      if (hint) hint.classList.add("hidden");
      return;
    }
    empty.classList.add("hidden");
    if (hint) hint.classList.remove("hidden");
    ul.classList.remove("hidden");
    ul.innerHTML = list
      .map((h) => {
        const dateStr = new Date(h.at).toLocaleString("th-TH", {
          dateStyle: "medium",
          timeStyle: "short",
        });
        const wrong = Number(h.wrong) || 0;
        const blank = Number(h.blank) || 0;
        return `<li>
          <button type="button" class="history-open" data-paper-id="${h.paperId}">
            <span><strong>${escapeHtml(h.label)}</strong><br/><span class="history-meta">${escapeHtml(dateStr)} · ผิด ${wrong} · ไม่ตอบ ${blank}</span></span>
            <span class="score">${h.percent}% · ${h.correct}/${h.total}</span>
          </button>
        </li>`;
      })
      .join("");
    ul.querySelectorAll(".history-open").forEach((btn) => {
      btn.addEventListener("click", () => openHistory(btn.getAttribute("data-paper-id")));
    });
  }

  async function openHistory(paperId) {
    if (!paperId || loading) return;
    loading = true;
    showBusy("กำลังเปิดประวัติ");
    try {
      const result = await api("/api/papers/" + paperId);
      viewingHistory = true;
      reviewFilter = "all";
      renderResult(result, { fromHistory: true });
    } catch (err) {
      alert(err.message);
    } finally {
      loading = false;
      hideBusy();
    }
  }

  function renderInsights(data) {
    const weak = (data.weak || []).filter((t) => t.total > 0);
    const empty = $("#insight-empty");
    const body = $("#insight-body");
    const note = $("#bank-note");
    if (note) {
      if (data.questionsUsed) {
        note.textContent =
          "เก็บข้อสอบไว้แล้ว " +
          data.questionsUsed +
          " ข้อ จาก " +
          data.papers +
          " ชุด · ข้อเหล่านี้จะไม่ถูกนำมาใช้อีก";
      } else {
        note.textContent = "แต่ละชุดถูกสร้างใหม่และเก็บลงฐานข้อมูล ข้อที่เคยออกจะไม่ถูกนำมาใช้อีก";
      }
    }
    if (!weak.length) {
      empty.classList.remove("hidden");
      body.classList.add("hidden");
      return;
    }
    empty.classList.add("hidden");
    body.classList.remove("hidden");
    const worst = weak[0];
    const below = weak.filter((t) => t.percent < 80).slice(0, 3);
    $("#insight-summary").textContent = below.length
      ? "หัวข้อที่ยังต่ำกว่า 80% และควรฝึกก่อนสอบจริง"
      : "ทุกหัวข้อที่ทำมาอยู่ที่ 80% ขึ้นไป ทำชุดใหม่เพื่อยืนยันกับโจทย์คนละข้อ";
    renderTopicBars($("#weak-list"), (below.length ? below : weak.slice(0, 4)));
    const btn = $("#btn-practice-weak");
    btn.classList.remove("hidden");
    btn.textContent = "ฝึกหัวข้อที่อ่อนที่สุด: " + worst.topic;
    btn.dataset.subject = worst.subject;
    btn.dataset.topic = worst.topic;
  }

  async function refreshHome() {
    try {
      const data = await api("/api/home");
      if (data.topics) topics = data.topics;
      if (!topics[practiceSubject].includes(practiceTopic)) {
        practiceTopic = topics[practiceSubject][0];
      }
      renderHistory(data.history || []);
      renderInsights(data);
      renderTopicChips();
    } catch (err) {
      $("#bank-note").textContent = "ยังติดต่อเซิร์ฟเวอร์ไม่ได้ — เปิดแอปผ่านเซิร์ฟเวอร์ฝึกสอบ";
      console.error(err);
    }
  }

  function syncSubjectChips() {
    $$("#subject-chips .chip").forEach((c) => {
      c.classList.toggle("active", c.getAttribute("data-subject") === practiceSubject);
    });
  }

  function renderTopicChips() {
    const list = topics[practiceSubject] || [];
    if (!list.includes(practiceTopic)) practiceTopic = list[0];
    const box = $("#topic-chips");
    box.innerHTML = list
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

  function beginSession(paper, extra) {
    clearTimer();
    const seconds = paper.seconds == null ? null : paper.seconds;
    state = {
      paperId: paper.paperId,
      mode: paper.mode,
      label: paper.label,
      questions: paper.questions,
      answers: paper.questions.map(() => null),
      index: 0,
      remaining: seconds,
      totalSeconds: seconds,
      allowPause: !!(extra && extra.allowPause),
      paused: false,
      submitting: false,
      timerId: null,
      startedAt: Date.now(),
      practiceSubject: paper.subject || (extra && extra.practiceSubject),
      practiceTopic: paper.topic || (extra && extra.practiceTopic),
    };
    showScreen("screen-exam");
    $("#btn-pause").classList.toggle("hidden", !state.allowPause || seconds == null);
    $("#exam-timer").classList.toggle("hidden", seconds == null);
    if (seconds == null) {
      $("#exam-timer").textContent = "—";
    } else {
      updateTimerDisplay();
      startTimer();
    }
    renderExam();
  }

  async function startExamMode(mode) {
    if (loading) return;
    loading = true;
    showBusy("กำลังสร้างชุดข้อสอบใหม่");
    try {
      const paper = await api("/api/papers", {
        method: "POST",
        body: JSON.stringify({ mode: mode }),
      });
      beginSession(paper, { allowPause: false });
    } catch (err) {
      alert(err.message);
    } finally {
      loading = false;
      hideBusy();
    }
  }

  async function startPractice() {
    if (loading) return;
    loading = true;
    showBusy("กำลังสร้างข้อฝึกของบทนี้");
    try {
      const useTimer = $("#practice-timer-on").checked;
      const paper = await api("/api/papers", {
        method: "POST",
        body: JSON.stringify({
          mode: "practice",
          subject: practiceSubject,
          topic: practiceTopic,
          timer: useTimer,
        }),
      });
      beginSession(paper, {
        allowPause: true,
        practiceSubject: practiceSubject,
        practiceTopic: practiceTopic,
      });
    } catch (err) {
      alert(err.message);
    } finally {
      loading = false;
      hideBusy();
    }
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

  function clearTimer() {
    if (state && state.timerId) {
      clearInterval(state.timerId);
      state.timerId = null;
    }
  }

  function startTimer() {
    clearTimer();
    state.timerId = setInterval(() => {
      if (!state || state.paused || state.submitting) return;
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
          <span class="letter">${letters[i] || ""}</span>
          <span class="text">${escapeHtml(c)}</span>
        </button>`;
      })
      .join("");
    box.querySelectorAll(".choice").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.answers[state.index] = Number(btn.getAttribute("data-index"));
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
        const classes = ["q-dot", state.answers[i] != null ? "answered" : "", i === state.index ? "current" : ""]
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
    if (!state) return;
    if (state.index >= state.questions.length - 1) {
      askSubmit();
      return;
    }
    state.index += 1;
    renderExam();
  }

  function goPrev() {
    if (!state || state.index <= 0) return;
    state.index -= 1;
    renderExam();
  }

  function skip() {
    if (!state) return;
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

  async function finishExam(auto) {
    if (!state || state.submitting) return;
    state.submitting = true;
    clearTimer();
    state.paused = false;
    $("#pause-overlay").classList.add("hidden");
    $("#modal").classList.add("hidden");

    let usedSec = 0;
    if (state.totalSeconds != null && state.remaining != null) {
      usedSec = Math.max(0, state.totalSeconds - Math.max(0, state.remaining));
    } else {
      usedSec = Math.round((Date.now() - state.startedAt) / 1000);
    }

    showBusy("กำลังตรวจคำตอบ");
    let result;
    try {
      result = await api("/api/papers/" + state.paperId + "/submit", {
        method: "POST",
        body: JSON.stringify({ answers: state.answers, usedSec: usedSec, auto: !!auto }),
      });
    } catch (err) {
      state.submitting = false;
      hideBusy();
      alert(err.message);
      if (state.totalSeconds != null) startTimer();
      return;
    }
    hideBusy();
    viewingHistory = false;
    reviewFilter = "all";
    renderResult(result, { fromHistory: false, auto: auto });
    refreshHome();
  }

  function renderResult(result, options) {
    const fromHistory = !!(options && options.fromHistory);
    const auto = !!(options && options.auto);
    lastResult = result;
    if (!fromHistory && state) {
      state.mode = result.mode;
      state.label = result.label;
      state.practiceSubject = result.practiceSubject;
      state.practiceTopic = result.practiceTopic;
    }

    $("#result-title").textContent = fromHistory
      ? "ประวัติคะแนน"
      : auto
        ? "หมดเวลา — สรุปคะแนน"
        : "สรุปคะแนน";
    $("#result-percent").textContent = result.percent + "%";
    $("#result-summary").textContent =
      "ได้ " + result.correct + " จาก " + result.total + " ข้อ · " + result.label;
    $("#stat-correct").textContent = String(result.correct);
    $("#stat-wrong").textContent = String(result.wrong);
    $("#stat-blank").textContent = String(result.blank);
    $("#stat-time").textContent = formatTime(result.usedSec);

    renderTopicBars($("#topic-bars"), result.topics || []);
    $("#improve-note").textContent = result.improve || "";
    const worst = (result.topics || []).filter((t) => t.percent < 80)[0];
    const drill = $("#btn-drill");
    if (worst) {
      drill.classList.remove("hidden");
      drill.textContent = "ฝึกหัวข้อที่ควรพัฒนา: " + worst.topic;
      drill.dataset.subject = worst.subject;
      drill.dataset.topic = worst.topic;
    } else {
      drill.classList.add("hidden");
    }
    $("#btn-retry").classList.toggle("hidden", fromHistory);
    $$("#review-filter .chip").forEach((chip) => {
      chip.classList.toggle("active", chip.getAttribute("data-filter") === reviewFilter);
    });
    renderReview();
    showScreen("screen-results");
    window.scrollTo(0, 0);
  }

  function renderReview() {
    const result = lastResult;
    const review = $("#review-list");
    const empty = $("#review-empty");
    if (!result) {
      review.innerHTML = "";
      return;
    }
    const items = result.questions
      .map((q, i) => ({ q, i }))
      .filter(({ q }) => (reviewFilter === "bad" ? q.status !== "ok" : true));
    if (!items.length) {
      review.innerHTML = "";
      empty.classList.remove("hidden");
      return;
    }
    empty.classList.add("hidden");
    review.innerHTML = items
      .map(({ q, i }) => {
        const letters = lettersFor(q);
        const status = q.status === "ok" ? "ถูก" : q.status === "bad" ? "ผิด" : "ไม่ตอบ";
        const klass = q.status === "ok" ? "ok" : q.status === "bad" ? "bad" : "blank";
        const your =
          q.chosen == null ? "—" : letters[q.chosen] + ". " + escapeHtml(q.choices[q.chosen]);
        const right = letters[q.answerIndex] + ". " + escapeHtml(q.choices[q.answerIndex]);
        const passageHtml = q.passage
          ? `<div class="passage" style="margin-bottom:8px">${escapeHtml(q.passage)}</div>`
          : "";
        const explain =
          q.status === "ok"
            ? `<div class="explain">${escapeHtml(q.explanation || "")}</div>`
            : `<div class="mistake"><strong>คำอธิบายข้อที่ผิด</strong>\n${escapeHtml(q.mistakeExplanation || q.explanation || "")}</div>`;
        return `<article class="review-item ${klass}">
          <div class="status">ข้อ ${i + 1} · ${status} · ${escapeHtml(q.topic)}</div>
          ${passageHtml}
          <div class="q-stem">${escapeHtml(q.stem)}</div>
          <div>คำตอบของคุณ: <strong>${your}</strong></div>
          <div>เฉลย: <strong>${right}</strong></div>
          ${explain}
        </article>`;
      })
      .join("");
  }

  function quitExam() {
    $("#modal-title").textContent = "ออกจากการสอบ?";
    $("#modal-body").textContent = "ข้อในชุดนี้ถูกเก็บแล้ว จะไม่ถูกนำมาใช้อีก และครั้งนี้จะไม่บันทึกคะแนน";
    $("#modal").classList.remove("hidden");
    $("#modal-confirm").onclick = () => {
      $("#modal").classList.add("hidden");
      clearTimer();
      state = null;
      showScreen("screen-home");
      refreshHome();
    };
  }

  function onKey(e) {
    if (!state || state.submitting) return;
    if ($("#modal") && !$("#modal").classList.contains("hidden")) return;
    if ($("#pause-overlay") && !$("#pause-overlay").classList.contains("hidden")) return;
    if ($("#busy") && !$("#busy").classList.contains("hidden")) return;
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
      viewingHistory = false;
      showScreen("screen-home");
      refreshHome();
    });
    $$("#review-filter .chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        reviewFilter = chip.getAttribute("data-filter") || "all";
        $$("#review-filter .chip").forEach((el) => {
          el.classList.toggle("active", el === chip);
        });
        renderReview();
      });
    });
    $("#btn-retry").addEventListener("click", () => {
      if (!state) {
        showScreen("screen-home");
        return;
      }
      const mode = state.mode;
      if (mode === "practice") {
        practiceSubject = state.practiceSubject || "math";
        practiceTopic = state.practiceTopic || topics.math[0];
        syncSubjectChips();
        renderTopicChips();
        startPractice();
      } else {
        startExamMode(mode);
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
    refreshHome();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
