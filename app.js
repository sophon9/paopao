/* M.1 Entrance Personal Tutor & Exam Analytics Frontend */
(function () {
  "use strict";

  const LETTERS_TH = ["ก", "ข", "ค", "ง"];
  const LETTERS_EN = ["A", "B", "C", "D"];
  const DIFF_TH = {
    easy: "ง่าย",
    medium: "ปานกลาง",
    hard: "ยาก",
    challenge: "ท้าทาย",
  };
  const STATUS_TH = {
    mastered: "★ แม่นยำแล้ว",
    practicing: "● กำลังฝึกให้คล่อง",
    learning: "◐ กำลังปูพื้นฐาน",
    rusty: "↻ ควรทบทวนกันลืม",
    unseen: "○ ยังไม่เคยฝึก",
  };

  let dashboard = null;
  let state = null;
  let loading = false;

  // Practice builder state
  let practiceSubject = "math";
  let practiceTopicKey = "m.num";
  let practiceSkillKey = ""; // "" means whole topic
  let practiceDiff = "";
  let practiceCount = 8;

  // Tabs & filters
  let activeTab = "overview";
  let currSubjFilter = "all";
  let notebookSubjFilter = "";
  let reviewFilter = "all";
  let lastResult = null;
  let viewingHistory = false;
  let currentLessonSkill = null;

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  function escapeHtml(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /**
   * Render rich markup:
   *   [[2 3/4]] -> mixed number with stacked fraction
   *   [[3/4]]   -> stacked fraction
   *   **bold**  -> <strong>
   *   ==text==  -> <span class="u-highlight">
   *   ____      -> <span class="ans-blank">
   */
  function renderMarkup(raw) {
    if (raw == null) return "";
    let t = escapeHtml(raw);
    t = t.replace(
      /\[\[(\d+)\s+(\d+)\/(\d+)\]\]/g,
      '<span class="mixed">$1<span class="frac"><span>$2</span><span>$3</span></span></span>'
    );
    t = t.replace(
      /\[\[([^\]/]+)\/([^\]]+)\]\]/g,
      '<span class="frac"><span>$1</span><span>$2</span></span>'
    );
    t = t.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    t = t.replace(/==(.+?)==/g, '<span class="u-highlight">$1</span>');
    t = t.replace(/_{3,}/g, '<span class="ans-blank">&nbsp;</span>');
    return t.replace(/\n/g, "<br/>");
  }

  function renderTableHtml(table) {
    if (!table || !Array.isArray(table.rows)) return "";
    const cap = table.caption ? `<caption>${renderMarkup(table.caption)}</caption>` : "";
    const head =
      Array.isArray(table.head) && table.head.length
        ? `<thead><tr>${table.head.map((h) => `<th>${renderMarkup(String(h))}</th>`).join("")}</tr></thead>`
        : "";
    const rows = table.rows
      .map((r) => `<tr>${r.map((c) => `<td>${renderMarkup(String(c))}</td>`).join("")}</tr>`)
      .join("");
    return `<table class="q-table">${cap}${head}<tbody>${rows}</tbody></table>`;
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
    const s = Math.round(sec % 60);
    return m + ":" + String(s).padStart(2, "0");
  }

  function showScreen(id) {
    ["screen-home", "screen-exam", "screen-results"].forEach((sid) => {
      const el = document.getElementById(sid);
      if (el) el.classList.toggle("hidden", sid !== id);
    });
  }

  function switchTab(tabName) {
    activeTab = tabName;
    $$(".main-tab").forEach((btn) => {
      const isAct = btn.getAttribute("data-tab") === tabName;
      btn.classList.toggle("active", isAct);
      btn.setAttribute("aria-selected", String(isAct));
    });
    ["overview", "curriculum", "analytics", "history"].forEach((t) => {
      const pane = document.getElementById("tab-" + t);
      if (pane) pane.classList.toggle("hidden", t !== tabName);
    });
    if (tabName === "analytics") {
      loadMistakeNotebook();
    }
  }

  function showBusy(text) {
    $("#busy-text").textContent = text || "กำลังสร้างชุดข้อสอบใหม่";
    $("#busy").classList.remove("hidden");
  }

  function hideBusy() {
    $("#busy").classList.add("hidden");
  }

  // ==================== DASHBOARD & ANALYTICS RENDERING ====================

  function renderReadiness(data) {
    const r = data.readiness || { overall: 0, math: {}, english: {}, benchmarks: [] };
    const overall = r.overall || 0;
    $("#readiness-overall").textContent = overall + "%";
    const circumference = 2 * Math.PI * 56; // ~351.86
    const filled = Math.round((overall / 100) * circumference);
    const ring = $("#overall-ring");
    if (ring) ring.setAttribute("stroke-dasharray", `${filled} ${Math.round(circumference)}`);

    let verdict = "เริ่มต้นวัดระดับหรือฝึกทีละทักษะ เพื่อให้ระบบประเมินความพร้อมเข้าโรงเรียนชั้นนำ";
    if (overall >= 85) {
      verdict = "ยอดเยี่ยม! ความแม่นยำถึงเกณฑ์ลุ้นห้องเรียนพิเศษ Gifted / EP และโรงเรียนแข่งขันสูง";
    } else if (overall >= 75) {
      verdict = "อยู่ในโซนลุ้นสอบติด สวนกุหลาบ · สาธิต · เตรียมฯ น้อย เก็บจุดอ่อนอีกนิดจะมั่นใจมาก!";
    } else if (overall >= 60) {
      verdict = "พื้นฐานดีแล้ว ฝึกเพิ่มในหัวข้อที่ยังต่ำกว่า 75% และเพิ่มโจทย์ระดับยาก-ท้าทาย";
    } else if (overall > 0) {
      verdict = "กำลังสะสมความแม่นยำ แนะนำเรียนสรุปหลักคิดและฝึกในโหมดติวเตอร์ทีละทักษะ";
    }
    $("#readiness-verdict").textContent = verdict;

    const benchEl = $("#benchmarks-list");
    if (benchEl) {
      benchEl.innerHTML = (r.benchmarks || [])
        .map((b) => {
          const diff = overall - b.target;
          const stClass = diff >= 0 ? "pass" : diff >= -12 ? "near" : "gap";
          const stText =
            diff >= 0
              ? `✔ ถึงเกณฑ์ (${b.target}%)`
              : `เป้าหมาย ${b.target}% (อีก ${Math.abs(diff)}%)`;
          const pct = Math.min(100, Math.round((overall / b.target) * 100));
          return `<div class="bench-row">
            <span class="bench-name">${escapeHtml(b.name)}</span>
            <span class="bench-status ${stClass}">${stText}</span>
            <div class="bench-track"><div class="bench-fill" style="width:${pct}%"></div></div>
          </div>`;
        })
        .join("");
    }

    const m = r.math || { readiness: 0, coverage: 0, accuracy: 0 };
    const e = r.english || { readiness: 0, coverage: 0, accuracy: 0 };
    $("#math-readiness").textContent = (m.readiness || 0) + "%";
    $("#math-cov-text").textContent = `ครอบคลุม ${m.coverage || 0}% · แม่นยำ ${m.accuracy || 0}%`;
    $("#math-bar").style.width = (m.readiness || 0) + "%";

    $("#eng-readiness").textContent = (e.readiness || 0) + "%";
    $("#eng-cov-text").textContent = `ครอบคลุม ${e.coverage || 0}% · แม่นยำ ${e.accuracy || 0}%`;
    $("#eng-bar").style.width = (e.readiness || 0) + "%";

    const st = data.streak || { days: 0, todayTotal: 0, dailyGoal: 15, activity14d: [] };
    $("#streak-days").textContent = String(st.days || 0);
    $("#today-done").textContent = String(st.todayTotal || 0);
    $("#today-goal").textContent = String(st.dailyGoal || 15);

    const actEl = $("#activity-14d");
    if (actEl && Array.isArray(st.activity14d)) {
      const maxDay = Math.max(10, ...st.activity14d.map((d) => d.total));
      actEl.innerHTML = st.activity14d
        .map((d) => {
          const h = d.total ? Math.max(6, Math.round((d.total / maxDay) * 26)) : 4;
          return `<span class="act-bar${d.total ? " active" : ""}" style="height:${h}px" title="${d.date}: ทำ ${d.total} ข้อ (ถูก ${d.correct})"></span>`;
        })
        .join("");
    }
  }

  function renderStudyPlan(plan) {
    const grid = $("#study-plan-grid");
    if (!grid) return;
    grid.innerHTML = (plan || [])
      .map((item, idx) => {
        const lessonBtn = item.skill
          ? `<button type="button" class="btn btn-xs btn-outline plan-lesson-btn" data-skill="${escapeHtml(item.skill)}">📖 บทเรียน</button>`
          : "";
        return `<article class="plan-card ${escapeHtml(item.kind || "")}">
          <div>
            <span class="plan-badge">${escapeHtml(item.badge || "แนะนำ")}</span>
            <h4>${escapeHtml(item.title)}</h4>
            <p>${escapeHtml(item.reason)}</p>
          </div>
          <div class="plan-actions">
            <button type="button" class="btn btn-xs btn-primary plan-go-btn" data-idx="${idx}">${escapeHtml(item.cta || "เริ่มฝึก")}</button>
            ${lessonBtn}
          </div>
        </article>`;
      })
      .join("");

    grid.querySelectorAll(".plan-go-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const item = plan[Number(btn.getAttribute("data-idx"))];
        if (!item || !item.action) return;
        startCustomSession(item.action);
      });
    });

    grid.querySelectorAll(".plan-lesson-btn").forEach((btn) => {
      btn.addEventListener("click", () => openLessonModal(btn.getAttribute("data-skill")));
    });
  }

  function renderTopicBars(el, rows) {
    if (!el) return;
    el.innerHTML = (rows || [])
      .map((t) => {
        const pct = Math.max(0, Math.min(100, Number(t.percent ?? t.mastery) || 0));
        const name = t.topic || t.name;
        const rightText =
          t.total != null
            ? `${t.correct}/${t.total} · ${pct}%`
            : `ความแม่น ${pct}%`;
        return `<div class="topic-bar">
          <span class="name">${escapeHtml(t.icon ? t.icon + " " + name : name)}</span>
          <span class="score">${rightText}</span>
          <div class="track"><div class="fill" style="width:${pct}%"></div></div>
        </div>`;
      })
      .join("");
  }

  function renderInsights(data) {
    const topics = data.topics || [];
    const practiced = topics.filter((t) => t.attempts > 0);
    const empty = $("#insight-empty");
    const body = $("#insight-body");
    const note = $("#bank-note");
    if (note && data.bankStats) {
      note.textContent =
        `คลังความรู้ ${data.bankStats.topicsCount} บท · ${data.bankStats.skillsCount} ทักษะย่อย · ` +
        `แม่แบบโจทย์ ${data.bankStats.templatesCount} รูปแบบ · สร้างข้อสอบไม่ซ้ำไปแล้ว ${data.bankStats.questionsGenerated} ข้อ`;
    }
    if (!practiced.length) {
      empty.classList.remove("hidden");
      body.classList.add("hidden");
      return;
    }
    empty.classList.add("hidden");
    body.classList.remove("hidden");

    const sorted = [...practiced].sort((a, b) => a.mastery - b.mastery);
    const worst = sorted[0];
    const below = sorted.filter((t) => t.mastery < 80);
    $("#insight-summary").textContent = below.length
      ? "บทเรียนที่ควรเสริมความแม่นยำให้ถึง 80% เพื่อความพร้อมระดับโรงเรียนชั้นนำ:"
      : "ทุกบทที่ฝึกมามีความแม่นยำดีเยี่ยม! ลองฝึกทักษะที่ยังไม่เคยทำหรือจำลองสนามสอบจริง";

    renderTopicBars(
      $("#weak-list"),
      sorted.slice(0, 6).map((t) => ({
        icon: t.icon,
        topic: t.name,
        correct: t.correct,
        total: t.attempts,
        percent: t.mastery,
      }))
    );

    const btn = $("#btn-practice-weak");
    if (worst) {
      btn.classList.remove("hidden");
      btn.textContent = `🎯 ฝึกซ่อมบทที่อ่อนที่สุด: ${worst.name}`;
      btn.dataset.subject = worst.subject;
      btn.dataset.topic = worst.key;
    }
  }

  function renderCurriculum(topics) {
    const box = $("#curriculum-topics");
    if (!box) return;
    const filtered = (topics || []).filter((t) =>
      currSubjFilter === "all" ? true : t.subject === currSubjFilter
    );

    box.innerHTML = filtered
      .map((t) => {
        const skillsHtml = (t.skills || [])
          .map((s) => {
            const st = s.status || "unseen";
            const stLabel = STATUS_TH[st] || st;
            const metaText =
              s.attempts > 0
                ? `ความแม่น ${s.mastery}% · ถูก ${s.correct}/${s.attempts} ข้อ`
                : "ยังไม่เคยฝึก — เริ่มจากอ่านบทเรียนได้เลย";
            return `<div class="skill-card">
              <div>
                <div class="skill-card-top">
                  <span class="skill-name">${escapeHtml(s.name)}</span>
                  <span class="status-pill ${st}">${stLabel}</span>
                </div>
                <div class="skill-meta">${metaText}</div>
              </div>
              <div class="skill-actions">
                <button type="button" class="btn btn-xs btn-outline btn-skill-lesson" data-skill="${escapeHtml(s.key)}">📖 บทเรียน</button>
                <button type="button" class="btn btn-xs btn-primary btn-skill-drill" data-skill="${escapeHtml(s.key)}" data-subject="${escapeHtml(s.subject)}">🧑‍🏫 ฝึกทักษะนี้</button>
              </div>
            </div>`;
          })
          .join("");

        return `<article class="curr-topic-card">
          <div class="curr-topic-head">
            <div class="curr-topic-title">
              <div class="curr-topic-icon">${escapeHtml(t.icon || "📘")}</div>
              <div>
                <h4>${escapeHtml(t.name)} <small style="color:var(--muted);font-weight:500">(${t.skillsMastered}/${t.skillsTotal} ทักษะแม่นยำ)</small></h4>
                <p class="curr-topic-blurb">${escapeHtml(t.blurb || "")}</p>
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
              <span style="font-weight:800;color:var(--pink-dark)">ความพร้อมบทนี้ ${t.mastery}%</span>
              <button type="button" class="btn btn-xs btn-ghost btn-topic-drill" data-topic="${escapeHtml(t.key)}" data-subject="${escapeHtml(t.subject)}">ฝึกทั้งบท</button>
            </div>
          </div>
          <div class="curr-skills-grid">${skillsHtml}</div>
        </article>`;
      })
      .join("");

    box.querySelectorAll(".btn-skill-lesson").forEach((btn) => {
      btn.addEventListener("click", () => openLessonModal(btn.getAttribute("data-skill")));
    });
    box.querySelectorAll(".btn-skill-drill").forEach((btn) => {
      btn.addEventListener("click", () => {
        startCustomSession({
          mode: "skill",
          subject: btn.getAttribute("data-subject"),
          focus: btn.getAttribute("data-skill"),
          tutor: true,
          count: 8,
        });
      });
    });
    box.querySelectorAll(".btn-topic-drill").forEach((btn) => {
      btn.addEventListener("click", () => {
        startCustomSession({
          mode: "skill",
          subject: btn.getAttribute("data-subject"),
          focus: btn.getAttribute("data-topic"),
          tutor: true,
          count: 8,
        });
      });
    });
  }

  function buildRadarSvg(title, topicList, color) {
    const n = topicList.length;
    if (n < 3) return "";
    const size = 240;
    const cx = size / 2;
    const cy = size / 2 + 4;
    const rMax = 76;
    const parts = [];

    // Concentric polygons (25%, 50%, 75%, 100%)
    [0.25, 0.5, 0.75, 1].forEach((lvl) => {
      const pts = topicList
        .map((_, i) => {
          const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
          return `${(cx + rMax * lvl * Math.cos(a)).toFixed(1)},${(cy + rMax * lvl * Math.sin(a)).toFixed(1)}`;
        })
        .join(" ");
      parts.push(`<polygon points="${pts}" fill="none" stroke="#E8DFE4" stroke-width="1"/>`);
    });

    // Axes & labels
    topicList.forEach((t, i) => {
      const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
      const x = cx + rMax * Math.cos(a);
      const y = cy + rMax * Math.sin(a);
      parts.push(`<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="#E8DFE4" stroke-width="1"/>`);
      const lx = cx + (rMax + 22) * Math.cos(a);
      const ly = cy + (rMax + 18) * Math.sin(a);
      const shortName = t.name.split(" ")[0].slice(0, 12);
      parts.push(
        `<text x="${lx.toFixed(1)}" y="${(ly + 4).toFixed(1)}" font-size="10" text-anchor="middle" fill="#463E4A" font-weight="600">${escapeHtml(shortName)}</text>`
      );
    });

    // Data polygon
    const dataPts = topicList
      .map((t, i) => {
        const val = Math.max(8, t.mastery || 0) / 100;
        const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
        return `${(cx + rMax * val * Math.cos(a)).toFixed(1)},${(cy + rMax * val * Math.sin(a)).toFixed(1)}`;
      })
      .join(" ");
    parts.push(
      `<polygon points="${dataPts}" fill="${color}" fill-opacity="0.22" stroke="${color}" stroke-width="2.5"/>`
    );

    return `<div class="radar-box">
      <h4>${escapeHtml(title)}</h4>
      <svg viewBox="0 0 ${size} ${size}" width="${size}" height="${size}" class="fig">${parts.join("")}</svg>
    </div>`;
  }

  function renderAnalyticsTab(data) {
    const topics = data.topics || [];
    const mathTopics = topics.filter((t) => t.subject === "math");
    const engTopics = topics.filter((t) => t.subject === "english");
    const radarBox = $("#radar-charts");
    if (radarBox) {
      radarBox.innerHTML =
        buildRadarSvg("🔢 เรดาร์คณิตศาสตร์ (8 บท)", mathTopics, "#E91E8C") +
        buildRadarSvg("🇬🇧 เรดาร์ภาษาอังกฤษ (5 บท)", engTopics, "#2563EB");
    }

    const patBox = $("#mistake-patterns-box");
    const pats = data.mistakePatterns || [];
    if (patBox) {
      if (!pats.length) {
        patBox.innerHTML = `<p class="history-empty">ยังไม่มีข้อมูลตัวลวงที่ผิดซ้ำ — เมื่อฝึกโจทย์ชุดใหม่ ระบบจะแยกประเภทความผิดพลาดให้โดยอัตโนมัติ</p>`;
      } else {
        patBox.innerHTML = pats
          .map(
            (p) => `<div class="mistake-pat-item">
            <div class="mistake-pat-head">
              <span>⚠️ ${escapeHtml(p.label)}</span>
              <span style="color:var(--bad)">${p.count} ครั้ง (${p.percent}%)</span>
            </div>
            <div class="progress-track" style="margin-bottom:4px"><div class="progress-fill math" style="width:${p.percent}%"></div></div>
            <p class="mistake-pat-advice">💡 <strong>วิธีแก้:</strong> ${escapeHtml(p.advice)}</p>
          </div>`
          )
          .join("");
      }
    }
  }

  async function loadMistakeNotebook() {
    const box = $("#notebook-list");
    if (!box) return;
    try {
      const q = notebookSubjFilter ? `?subject=${encodeURIComponent(notebookSubjFilter)}` : "";
      const res = await api("/api/mistakes" + q);
      const items = res.items || [];
      if (!items.length) {
        box.innerHTML = `<p class="history-empty">ไม่มีรายการข้อที่ผิดในหมวดนี้ ยอดเยี่ยมมาก!</p>`;
        return;
      }
      box.innerHTML = items
        .map((qItem) => {
          const letters = qItem.subject === "english" ? LETTERS_EN : LETTERS_TH;
          const your =
            qItem.chosen == null
              ? "— (ไม่ได้ตอบ)"
              : `${letters[qItem.chosen]}. ${ renderMarkup(qItem.choices[qItem.chosen]) }`;
          const right = `${letters[qItem.answerIndex]}. ${renderMarkup(qItem.choices[qItem.answerIndex])}`;
          const whyHtml = qItem.chosenWhy
            ? `<div class="tf-why-wrong"><strong>ทำไมตัวเลือกนี้ถึงผิด (${escapeHtml(qItem.mistakeLabel)}):</strong> ${renderMarkup(qItem.chosenWhy)}</div>`
            : "";
          const stepsHtml = (qItem.steps || []).map((s) => `<li>${renderMarkup(s)}</li>`).join("");
          const lessonBtn = qItem.hasLesson
            ? `<button type="button" class="btn btn-xs btn-outline nb-lesson-btn" data-skill="${escapeHtml(qItem.skill)}">📖 บทเรียน: ${escapeHtml(qItem.skillName)}</button>`
            : "";
          const drillBtn = qItem.hasLesson
            ? `<button type="button" class="btn btn-xs btn-primary nb-drill-btn" data-skill="${escapeHtml(qItem.skill)}" data-subject="${escapeHtml(qItem.subject)}">🎯 ฝึกซ่อมเรื่องนี้</button>`
            : "";

          return `<article class="review-item bad">
            <div class="status">
              <span>${escapeHtml(qItem.topicName)} · ${escapeHtml(qItem.skillName)}</span>
              <span class="tag">${escapeHtml(qItem.mistakeLabel)}</span>
            </div>
            ${qItem.passage ? `<div class="passage">${renderMarkup(qItem.passage)}</div>` : ""}
            ${qItem.figure ? `<div class="q-figure">${qItem.figure}</div>` : ""}
            ${qItem.table ? `<div class="q-table-wrap">${renderTableHtml(qItem.table)}</div>` : ""}
            <div class="q-stem">${renderMarkup(qItem.stem)}</div>
            <div>คำตอบที่เคยเลือก: <strong class="bad-text">${your}</strong></div>
            <div>เฉลยที่ถูกต้อง: <strong class="ok-text">${right}</strong></div>
            <div class="explain" style="margin-top:10px">
              ${whyHtml}
              <strong>🪜 วิธีคิดทีละขั้น:</strong>
              <ol class="tf-steps">${stepsHtml}</ol>
              <div class="nav-row" style="margin-top:8px">${lessonBtn}${drillBtn}</div>
            </div>
          </article>`;
        })
        .join("");

      box.querySelectorAll(".nb-lesson-btn").forEach((b) => {
        b.addEventListener("click", () => openLessonModal(b.getAttribute("data-skill")));
      });
      box.querySelectorAll(".nb-drill-btn").forEach((b) => {
        b.addEventListener("click", () => {
          startCustomSession({
            mode: "skill",
            subject: b.getAttribute("data-subject"),
            focus: b.getAttribute("data-skill"),
            tutor: true,
            count: 8,
          });
        });
      });
    } catch (err) {
      box.innerHTML = `<p class="history-empty">${escapeHtml(err.message)}</p>`;
    }
  }

  function renderTrendChart(history) {
    const wrap = $("#history-trend-chart");
    if (!wrap) return;
    if (!history || history.length < 2) {
      wrap.innerHTML = `<p class="history-empty">ทำข้อสอบอย่างน้อย 2 ชุดเพื่อดูกราฟแนวโน้มคะแนน</p>`;
      return;
    }
    const ptsList = [...history].slice(0, 20).reverse();
    const w = 680;
    const h = 160;
    const padL = 36;
    const padR = 16;
    const padT = 16;
    const padB = 26;
    const pw = w - padL - padR;
    const ph = h - padT - padB;
    const coords = ptsList.map((item, i) => {
      const x = padL + (pw * i) / (ptsList.length - 1);
      const y = padT + ph - (ph * (item.percent || 0)) / 100;
      return [x, y, item];
    });
    const poly = coords.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" ");
    const dots = coords
      .map(
        ([x, y, item]) =>
          `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="#E91E8C"><title>${escapeHtml(item.label)}: ${item.percent}%</title></circle>`
      )
      .join("");
    wrap.innerHTML = `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}" class="fig">
      <line x1="${padL}" y1="${padT + ph * 0.2}" x2="${w - padR}" y2="${padT + ph * 0.2}" stroke="#E7F8ED" stroke-width="2"/>
      <text x="${padL - 6}" y="${padT + ph * 0.2 + 4}" font-size="10" text-anchor="end" fill="#15803D">80%</text>
      <line x1="${padL}" y1="${padT + ph * 0.5}" x2="${w - padR}" y2="${padT + ph * 0.5}" stroke="#E8DFE4" stroke-width="1"/>
      <text x="${padL - 6}" y="${padT + ph * 0.5 + 4}" font-size="10" text-anchor="end" fill="#766B7A">50%</text>
      <polyline points="${poly}" fill="none" stroke="#E91E8C" stroke-width="2.5"/>
      ${dots}
    </svg>`;
  }

  function renderHistory(list) {
    const ul = $("#history-list");
    const empty = $("#history-empty");
    const hint = $("#history-hint");
    renderTrendChart(list);
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
            <span><strong>${escapeHtml(h.label)}</strong><br/><span class="history-meta">${escapeHtml(dateStr)} · ผิด ${wrong} · ไม่ตอบ ${blank} · เวลา ${formatTime(h.usedSec)}</span></span>
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
    showBusy("กำลังเปิดประวัติและบทวิเคราะห์");
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

  // ==================== PRACTICE BUILDER CHIPS ====================

  function syncBuilderChips() {
    if (!dashboard || !dashboard.topics) return;
    $$("#subject-chips .chip").forEach((c) => {
      c.classList.toggle("active", c.getAttribute("data-subject") === practiceSubject);
    });

    const subjTopics = dashboard.topics.filter((t) => t.subject === practiceSubject);
    if (!subjTopics.some((t) => t.key === practiceTopicKey) && subjTopics.length) {
      practiceTopicKey = subjTopics[0].key;
      practiceSkillKey = "";
    }

    const topicBox = $("#topic-chips");
    if (topicBox) {
      topicBox.innerHTML = subjTopics
        .map(
          (t) =>
            `<button type="button" class="chip${t.key === practiceTopicKey ? " active" : ""}" data-topic="${escapeHtml(t.key)}">${escapeHtml(t.icon + " " + t.name)} (${t.mastery}%)</button>`
        )
        .join("");
      topicBox.querySelectorAll(".chip").forEach((btn) => {
        btn.addEventListener("click", () => {
          practiceTopicKey = btn.getAttribute("data-topic");
          practiceSkillKey = "";
          syncBuilderChips();
        });
      });
    }

    const currentTopic = subjTopics.find((t) => t.key === practiceTopicKey);
    const skills = currentTopic ? currentTopic.skills || [] : [];
    const skillBox = $("#skill-chips");
    if (skillBox) {
      skillBox.innerHTML =
        `<button type="button" class="chip${practiceSkillKey === "" ? " active" : ""}" data-skill="">✨ รวมทุกทักษะในบทนี้</button>` +
        skills
          .map(
            (s) =>
              `<button type="button" class="chip${s.key === practiceSkillKey ? " active" : ""}" data-skill="${escapeHtml(s.key)}">${escapeHtml(s.name)} (${s.mastery}%)</button>`
          )
          .join("");
      skillBox.querySelectorAll(".chip").forEach((btn) => {
        btn.addEventListener("click", () => {
          practiceSkillKey = btn.getAttribute("data-skill") || "";
          syncBuilderChips();
        });
      });
    }

    const lessonBtn = $("#btn-open-selected-lesson");
    if (lessonBtn) {
      lessonBtn.classList.toggle("hidden", !practiceSkillKey);
    }
  }

  async function refreshHome() {
    try {
      const data = await api("/api/home");
      dashboard = data;
      renderReadiness(data);
      renderStudyPlan(data.studyPlan || []);
      renderInsights(data);
      renderCurriculum(data.topics || []);
      renderAnalyticsTab(data);
      renderHistory(data.history || []);
      syncBuilderChips();

      if (data.bankStats) {
        $("#tab-skills-count").textContent = String(data.bankStats.skillsCount || 0);
      }
      $("#tab-mistakes-count").textContent = String(data.mistakeCount || 0);
      $("#tab-history-count").textContent = String((data.history || []).length);
    } catch (err) {
      $("#bank-note").textContent = "ยังติดต่อเซิร์ฟเวอร์ไม่ได้ — เปิดแอปผ่าน python3 backend/server.py";
      console.error(err);
    }
  }

  // ==================== INTERACTIVE LESSON MODAL ====================

  async function openLessonModal(skillKey) {
    if (!skillKey) return;
    currentLessonSkill = skillKey;
    showBusy("กำลังเปิดบทเรียนและสร้างโจทย์ตัวอย่าง");
    try {
      const data = await api("/api/lessons/" + encodeURIComponent(skillKey));
      hideBusy();
      renderLessonModal(data);
      $("#lesson-modal").classList.remove("hidden");
    } catch (err) {
      hideBusy();
      alert(err.message);
    }
  }

  function renderLessonModal(data) {
    $("#lesson-topic-badge").textContent = `${data.topicName} · บทเรียนและเทคนิค`;
    $("#lesson-title").textContent = data.name;
    const l = data.lesson || {};
    const stepsHtml = (l.steps || []).map((s) => `<li>${renderMarkup(s)}</li>`).join("");
    const mistakesHtml = (l.mistakes || []).map((m) => `<li>${renderMarkup(m)}</li>`).join("");
    const tipsHtml = (l.tips || []).map((t) => `<li>${renderMarkup(t)}</li>`).join("");

    const ex = l.example || {};
    const exSteps = (ex.steps || []).map((s) => `<li>${renderMarkup(s)}</li>`).join("");

    const samplesHtml = (data.samples || [])
      .map(
        (smp, i) => `<div class="lesson-example-box">
        <div style="font-weight:700;color:var(--pink-dark);margin-bottom:4px">🎲 โจทย์ตัวอย่างสร้างสด ข้อที่ ${i + 1} (${DIFF_TH[smp.difficulty] || smp.difficulty})</div>
        ${smp.passage ? `<div class="passage">${renderMarkup(smp.passage)}</div>` : ""}
        ${smp.figure ? `<div class="q-figure">${smp.figure}</div>` : ""}
        ${smp.table ? `<div class="q-table-wrap">${renderTableHtml(smp.table)}</div>` : ""}
        <div style="font-weight:700;margin-bottom:6px">${renderMarkup(smp.stem)}</div>
        <ol style="margin:4px 0 6px;padding-left:20px">${(smp.steps || []).map((st) => `<li>${renderMarkup(st)}</li>`).join("")}</ol>
        <div class="ok-text" style="font-weight:800">✔ คำตอบ: ${renderMarkup(smp.answer)}</div>
      </div>`
      )
      .join("");

    $("#lesson-body").innerHTML = `
      <div class="lesson-sec concept-sec">
        <h4>💡 หลักคิดสำคัญ (Core Concept)</h4>
        <div>${renderMarkup(l.concept || "")}</div>
      </div>
      <div class="lesson-sec">
        <h4>🪜 ขั้นตอนการทำโจทย์</h4>
        <ol>${stepsHtml}</ol>
      </div>
      <div class="lesson-sec">
        <h4>✏️ ตัวอย่างต้นแบบ &amp; โจทย์สาธิต</h4>
        <div class="lesson-example-box">
          <div style="font-weight:700;margin-bottom:4px">${renderMarkup(ex.q || "")}</div>
          <ol style="margin:4px 0 6px;padding-left:20px">${exSteps}</ol>
          <div class="ok-text" style="font-weight:800">✔ คำตอบ: ${renderMarkup(ex.a || "")}</div>
        </div>
        ${samplesHtml}
      </div>
      <div class="lesson-sec">
        <h4>⚠️ กับดักและข้อผิดพลาดที่ต้องระวัง</h4>
        <ul>${mistakesHtml}</ul>
      </div>
      <div class="lesson-sec">
        <h4>⚡ เทคนิคทำข้อสอบให้ไว</h4>
        <ul>${tipsHtml}</ul>
      </div>
    `;

    $("#btn-lesson-start-drill").onclick = () => {
      $("#lesson-modal").classList.add("hidden");
      startCustomSession({
        mode: "skill",
        subject: data.subject,
        focus: data.key,
        tutor: true,
        count: 8,
      });
    };
  }

  // ==================== SESSION CREATION & EXAM ENGINE ====================

  async function startCustomSession(opts) {
    if (loading) return;
    loading = true;
    showBusy("กำลังสร้างชุดฝึกและคัดโจทย์ที่เหมาะกับคุณ");
    try {
      const paper = await api("/api/papers", {
        method: "POST",
        body: JSON.stringify(opts),
      });
      beginSession(paper, { allowPause: opts.mode !== "mock" });
    } catch (err) {
      alert(err.message);
    } finally {
      loading = false;
      hideBusy();
    }
  }

  async function startExamMode(mode) {
    await startCustomSession({ mode: mode, tutor: false, timer: true });
  }

  async function startPractice() {
    const useTimer = $("#practice-timer-on").checked;
    const useTutor = $("#practice-tutor-on").checked;
    const focus = practiceSkillKey || practiceTopicKey;
    await startCustomSession({
      mode: "skill",
      subject: practiceSubject,
      focus: focus,
      tutor: useTutor,
      timer: useTimer,
      count: practiceCount,
      difficulty: practiceDiff || null,
    });
  }

  function beginSession(paper, extra) {
    clearTimer();
    const seconds = paper.seconds == null ? null : paper.seconds;
    const n = paper.questions.length;
    state = {
      paperId: paper.paperId,
      mode: paper.mode,
      subject: paper.subject,
      focus: paper.focus,
      tutor: !!paper.tutor,
      label: paper.label,
      questions: paper.questions,
      answers: paper.questions.map(() => null),
      checked: paper.questions.map(() => null), // stores instant-check result per item
      hints: paper.questions.map(() => null),
      flags: paper.questions.map(() => false),
      timesMs: paper.questions.map(() => 0),
      questionEnteredAt: Date.now(),
      index: 0,
      remaining: seconds,
      totalSeconds: seconds,
      allowPause: !!(extra && extra.allowPause) || !!paper.tutor,
      paused: false,
      submitting: false,
      timerId: null,
      startedAt: Date.now(),
    };
    showScreen("screen-exam");
    $("#exam-mode-badge").textContent = state.tutor ? "🧑‍🏫 โหมดติวเตอร์" : "⏱️ โหมดสอบ";
    $("#btn-pause").classList.toggle("hidden", !state.allowPause || seconds == null);
    $("#exam-timer").classList.toggle("hidden", seconds == null);
    if (seconds == null) {
      $("#exam-timer").textContent = "—";
    } else {
      updateTimerDisplay();
      startTimer();
    }
    renderExam();
    window.scrollTo(0, 0);
  }

  function recordCurrentQuestionTime() {
    if (!state) return;
    const now = Date.now();
    const elapsed = Math.max(0, now - (state.questionEnteredAt || now));
    state.timesMs[state.index] = (state.timesMs[state.index] || 0) + elapsed;
    state.questionEnteredAt = now;
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

  function lettersFor(q) {
    return q.subject === "english" ? LETTERS_EN : LETTERS_TH;
  }

  function renderExam() {
    if (!state) return;
    const idx = state.index;
    const q = state.questions[idx];
    const n = state.questions.length;

    $("#exam-subject").textContent = state.label;
    $("#exam-progress").textContent = `ข้อ ${idx + 1} / ${n}`;
    $("#q-topic").textContent = q.topicName || q.topic;
    $("#q-skill").textContent = q.skillName || q.skill || "";
    $("#q-skill").classList.toggle("hidden", !q.skillName);

    const diffEl = $("#q-diff");
    diffEl.textContent = DIFF_TH[q.difficulty] || q.difficulty;
    diffEl.className = "tag diff-" + (q.difficulty || "medium");

    $("#btn-flag").classList.toggle("active", !!state.flags[idx]);
    $("#btn-flag").textContent = state.flags[idx] ? "🚩 ติดธงแล้ว" : "🚩 ติดธง";

    // Hint box
    const hintBox = $("#q-hint-box");
    const hData = state.hints[idx];
    if (hData) {
      hintBox.innerHTML =
        `<strong>💡 คำใบ้ช่วยคิด:</strong> ${renderMarkup(hData.hint)}` +
        (hData.concept ? `<div style="margin-top:4px;font-size:0.85rem">📌 <strong>หลักคิด:</strong> ${renderMarkup(hData.concept)}</div>` : "");
      hintBox.classList.remove("hidden");
    } else {
      hintBox.classList.add("hidden");
      hintBox.innerHTML = "";
    }

    // Passage
    const passage = $("#q-passage");
    if (q.passage) {
      passage.innerHTML = renderMarkup(q.passage);
      passage.classList.remove("hidden");
    } else {
      passage.classList.add("hidden");
      passage.innerHTML = "";
    }

    // SVG Figure
    const figEl = $("#q-figure");
    if (q.figure) {
      figEl.innerHTML = q.figure;
      figEl.classList.remove("hidden");
    } else {
      figEl.classList.add("hidden");
      figEl.innerHTML = "";
    }

    // Table
    const tblEl = $("#q-table");
    if (q.table) {
      tblEl.innerHTML = renderTableHtml(q.table);
      tblEl.classList.remove("hidden");
    } else {
      tblEl.classList.add("hidden");
      tblEl.innerHTML = "";
    }

    // Stem
    $("#q-stem").innerHTML = renderMarkup(q.stem);

    // Choices
    const letters = lettersFor(q);
    const selected = state.answers[idx];
    const checkRes = state.checked[idx];
    const box = $("#q-choices");
    box.innerHTML = q.choices
      .map((c, i) => {
        const classes = ["choice"];
        if (selected === i) classes.push("selected");
        if (checkRes) {
          if (i === checkRes.answerIndex) classes.push("correct-choice");
          else if (selected === i && !checkRes.correct) classes.push("wrong-choice");
        }
        return `<button type="button" class="${classes.join(" ")}" role="option" aria-selected="${selected === i}" data-index="${i}">
          <span class="letter">${letters[i] || ""}</span>
          <span class="text">${renderMarkup(c)}</span>
        </button>`;
      })
      .join("");

    box.querySelectorAll(".choice").forEach((btn) => {
      btn.addEventListener("click", () => {
        const cIdx = Number(btn.getAttribute("data-index"));
        state.answers[idx] = cIdx;
        if (state.tutor) {
          checkCurrentAnswer(cIdx);
        } else {
          renderExam();
        }
      });
    });

    renderTutorFeedback(checkRes);

    // Show manual "ตรวจคำตอบข้อนี้" button if not in tutor mode or if not yet checked
    const checkBtn = $("#btn-check-now");
    if (checkBtn) {
      checkBtn.classList.toggle("hidden", state.mode === "mock" || !!checkRes || selected == null);
    }

    $("#btn-prev").disabled = idx === 0;
    $("#btn-next").textContent = idx === n - 1 ? "ส่งคำตอบ" : "ถัดไป →";
    renderGrid();
  }

  function renderTutorFeedback(checkRes) {
    const fb = $("#tutor-feedback");
    if (!checkRes) {
      fb.classList.add("hidden");
      fb.innerHTML = "";
      return;
    }
    fb.classList.remove("hidden");
    fb.className = "tutor-feedback " + (checkRes.correct ? "ok" : "bad");

    const q = state.questions[state.index];
    const letters = lettersFor(q);
    const rightText = `${letters[checkRes.answerIndex]}. ${renderMarkup(q.choices[checkRes.answerIndex])}`;
    const title = checkRes.correct
      ? "🎉 ถูกต้อง! วิธีคิดแม่นยำมาก"
      : `❌ ยังไม่ถูก — คำตอบที่ถูกคือ ${rightText}`;

    const whyWrongHtml =
      !checkRes.correct && checkRes.chosenWhy
        ? `<div class="tf-why-wrong"><strong>🔍 จุดที่พลาด (${escapeHtml(checkRes.mistakeLabel || "กับดัก")}):</strong> ${renderMarkup(checkRes.chosenWhy)}</div>`
        : "";

    const stepsHtml = (checkRes.steps || []).map((s) => `<li>${renderMarkup(s)}</li>`).join("");

    fb.innerHTML = `
      <div class="tf-header">
        <span>${title}</span>
        ${checkRes.mistakeLabel ? `<span class="tag">${escapeHtml(checkRes.mistakeLabel)}</span>` : ""}
      </div>
      ${whyWrongHtml}
      <div><strong>🪜 เฉลยวิธีคิดทีละขั้น:</strong></div>
      <ol class="tf-steps">${stepsHtml}</ol>
      <div class="tf-actions">
        <button type="button" class="btn btn-xs btn-primary" id="btn-try-similar">➕ ลองทำโจทย์คล้ายกันอีกข้อ</button>
        <button type="button" class="btn btn-xs btn-outline" id="btn-tf-open-lesson">📖 เปิดบทเรียนเรื่อง ${escapeHtml(checkRes.skillName || "")}</button>
      </div>
    `;

    const simBtn = $("#btn-try-similar");
    if (simBtn) {
      simBtn.onclick = () => generateSimilarQuestion();
    }
    const lesBtn = $("#btn-tf-open-lesson");
    if (lesBtn) {
      lesBtn.onclick = () => openLessonModal(checkRes.skill);
    }
  }

  async function requestHint() {
    if (!state) return;
    const idx = state.index;
    if (state.hints[idx]) return;
    try {
      const h = await api(`/api/papers/${state.paperId}/hint`, {
        method: "POST",
        body: JSON.stringify({ position: idx }),
      });
      state.hints[idx] = h;
      renderExam();
    } catch (err) {
      alert(err.message);
    }
  }

  async function checkCurrentAnswer(chosenIdx) {
    if (!state) return;
    const idx = state.index;
    recordCurrentQuestionTime();
    try {
      const res = await api(`/api/papers/${state.paperId}/check`, {
        method: "POST",
        body: JSON.stringify({
          position: idx,
          chosen: chosenIdx,
          timeMs: state.timesMs[idx],
          flagged: state.flags[idx],
        }),
      });
      state.checked[idx] = res;
      renderExam();
    } catch (err) {
      console.error(err);
      renderExam();
    }
  }

  async function generateSimilarQuestion() {
    if (!state || loading) return;
    loading = true;
    showBusy("กำลังสร้างโจทย์คู่แฝดในทักษะเดียวกัน");
    try {
      const newQ = await api(`/api/papers/${state.paperId}/similar`, {
        method: "POST",
        body: JSON.stringify({ position: state.index }),
      });
      state.questions.push(newQ);
      state.answers.push(null);
      state.checked.push(null);
      state.hints.push(null);
      state.flags.push(false);
      state.timesMs.push(0);
      recordCurrentQuestionTime();
      state.index = state.questions.length - 1;
      renderExam();
    } catch (err) {
      alert(err.message);
    } finally {
      loading = false;
      hideBusy();
    }
  }

  function renderGrid() {
    const grid = $("#q-grid");
    grid.innerHTML = state.questions
      .map((_, i) => {
        const chk = state.checked[i];
        const classes = [
          "q-dot",
          state.answers[i] != null ? "answered" : "",
          chk ? (chk.correct ? "checked-ok" : "checked-bad") : "",
          state.flags[i] ? "flagged" : "",
          i === state.index ? "current" : "",
        ]
          .filter(Boolean)
          .join(" ");
        return `<button type="button" class="${classes}" data-i="${i}" aria-label="ไปข้อ ${i + 1}">${i + 1}</button>`;
      })
      .join("");
    grid.querySelectorAll(".q-dot").forEach((btn) => {
      btn.addEventListener("click", () => {
        recordCurrentQuestionTime();
        state.index = Number(btn.getAttribute("data-i"));
        renderExam();
      });
    });
  }

  function goNext() {
    if (!state) return;
    recordCurrentQuestionTime();
    if (state.index >= state.questions.length - 1) {
      askSubmit();
      return;
    }
    state.index += 1;
    renderExam();
  }

  function goPrev() {
    if (!state || state.index <= 0) return;
    recordCurrentQuestionTime();
    state.index -= 1;
    renderExam();
  }

  function skip() {
    if (!state) return;
    recordCurrentQuestionTime();
    if (state.index < state.questions.length - 1) {
      state.index += 1;
      renderExam();
    }
  }

  function askSubmit() {
    const blank = state.answers.filter((a) => a == null).length;
    const flagged = state.flags.filter(Boolean).length;
    $("#modal-title").textContent = "ยืนยันส่งกระดาษคำตอบ?";
    let msg =
      blank > 0
        ? `ยังมี ${blank} ข้อที่ยังไม่ได้ตอบ`
        : "ตอบครบทุกข้อแล้ว";
    if (flagged > 0) {
      msg += ` และมีข้อที่ติดธงไว้ ${flagged} ข้อ`;
    }
    $("#modal-body").textContent = msg + " ต้องการส่งคำตอบเลยหรือไม่?";
    $("#modal").classList.remove("hidden");
    $("#modal-confirm").onclick = () => {
      $("#modal").classList.add("hidden");
      finishExam(false);
    };
  }

  async function finishExam(auto) {
    if (!state || state.submitting) return;
    recordCurrentQuestionTime();
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

    showBusy("กำลังตรวจคำตอบและวิเคราะห์จุดอ่อน");
    let result;
    try {
      result = await api(`/api/papers/${state.paperId}/submit`, {
        method: "POST",
        body: JSON.stringify({
          answers: state.answers,
          usedSec: usedSec,
          auto: !!auto,
          timesMs: state.timesMs,
          flags: state.flags,
        }),
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

  // ==================== RESULTS & REVIEW RENDERING ====================

  function renderResult(result, options) {
    const fromHistory = !!(options && options.fromHistory);
    const auto = !!(options && options.auto);
    lastResult = result;

    $("#result-title").textContent = fromHistory
      ? "ประวัติคะแนนและบทวิเคราะห์"
      : auto
        ? "หมดเวลา — สรุปคะแนนและบทวิเคราะห์"
        : "สรุปคะแนนและบทวิเคราะห์";
    $("#result-percent").textContent = result.percent + "%";
    $("#result-summary").textContent = `ได้ ${result.correct} จาก ${result.total} ข้อ · ${result.label}`;
    $("#stat-correct").textContent = String(result.correct);
    $("#stat-wrong").textContent = String(result.wrong);
    $("#stat-blank").textContent = String(result.blank);
    $("#stat-time").textContent = formatTime(result.usedSec);

    renderTopicBars($("#topic-bars"), result.topics || []);
    $("#improve-note").textContent = result.improve || "";

    // Session mistake tags summary
    const mBox = $("#result-mistakes-summary");
    if (mBox) {
      const sm = result.sessionMistakes || [];
      mBox.innerHTML = sm.length
        ? sm.map((m) => `<span class="tag diff-hard">⚠️ ${escapeHtml(m.label)}: ${m.count} ข้อ</span>`).join("")
        : `<span class="tag diff-easy">✨ ไม่พบจุดผิดซ้ำในชุดนี้</span>`;
    }

    // Per-skill breakdown with direct Lesson & Drill buttons
    const sList = $("#result-skills-list");
    if (sList) {
      sList.innerHTML = (result.skills || [])
        .map((s) => {
          const lessonBtn = s.hasLesson
            ? `<button type="button" class="btn btn-xs btn-outline res-lesson-btn" data-skill="${escapeHtml(s.key)}">📖 เรียน</button>`
            : "";
          const drillBtn = s.hasLesson
            ? `<button type="button" class="btn btn-xs btn-primary res-drill-btn" data-skill="${escapeHtml(s.key)}" data-subject="${escapeHtml(s.subject)}">🎯 ฝึกซ่อม</button>`
            : "";
          return `<div class="res-skill-row">
            <div>
              <strong>${escapeHtml(s.name)}</strong>
              <span style="color:var(--muted);font-size:0.8rem"> · ${s.correct}/${s.total} (${s.percent}%)</span>
            </div>
            <div style="display:flex;gap:6px">${lessonBtn}${drillBtn}</div>
          </div>`;
        })
        .join("");
      sList.querySelectorAll(".res-lesson-btn").forEach((b) => {
        b.addEventListener("click", () => openLessonModal(b.getAttribute("data-skill")));
      });
      sList.querySelectorAll(".res-drill-btn").forEach((b) => {
        b.addEventListener("click", () => {
          startCustomSession({
            mode: "skill",
            subject: b.getAttribute("data-subject"),
            focus: b.getAttribute("data-skill"),
            tutor: true,
            count: 8,
          });
        });
      });
    }

    const worstSkill = (result.skills || []).find((s) => s.percent < 80 && s.hasLesson);
    const worstTopic = (result.topics || []).find((t) => t.percent < 80);
    const drill = $("#btn-drill");
    if (worstSkill) {
      drill.classList.remove("hidden");
      drill.textContent = `🎯 ฝึกซ่อมทักษะ: ${worstSkill.name}`;
      drill.dataset.subject = worstSkill.subject;
      drill.dataset.focus = worstSkill.key;
    } else if (worstTopic) {
      drill.classList.remove("hidden");
      drill.textContent = `🎯 ฝึกหัวข้อที่ควรพัฒนา: ${worstTopic.topic}`;
      drill.dataset.subject = worstTopic.subject;
      drill.dataset.focus = worstTopic.key || worstTopic.topic;
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
      .filter(({ q }) => {
        if (reviewFilter === "bad") return q.status !== "ok";
        if (reviewFilter === "flagged") return !!q.flagged;
        return true;
      });

    if (!items.length) {
      review.innerHTML = "";
      empty.classList.remove("hidden");
      return;
    }
    empty.classList.add("hidden");
    review.innerHTML = items
      .map(({ q, i }) => {
        const letters = lettersFor(q);
        const status = q.status === "ok" ? "✔ ตอบถูก" : q.status === "bad" ? "✘ ตอบผิด" : "— ไม่ได้ตอบ";
        const klass = q.status === "ok" ? "ok" : q.status === "bad" ? "bad" : "blank";
        const your =
          q.chosen == null ? "—" : `${letters[q.chosen]}. ${renderMarkup(q.choices[q.chosen])}`;
        const right = `${letters[q.answerIndex]}. ${renderMarkup(q.choices[q.answerIndex])}`;

        const passageHtml = q.passage ? `<div class="passage">${renderMarkup(q.passage)}</div>` : "";
        const figHtml = q.figure ? `<div class="q-figure">${q.figure}</div>` : "";
        const tblHtml = q.table ? `<div class="q-table-wrap">${renderTableHtml(q.table)}</div>` : "";

        const whyChosenHtml =
          q.status === "bad" && q.chosenWhy
            ? `<div class="tf-why-wrong"><strong>🔍 ทำไมตัวเลือกที่เลือกถึงผิด (${escapeHtml(q.mistakeLabel || "จุดหลอก")}):</strong> ${renderMarkup(q.chosenWhy)}</div>`
            : "";

        const stepsList = Array.isArray(q.steps) && q.steps.length
          ? `<ol class="tf-steps">${q.steps.map((s) => `<li>${renderMarkup(s)}</li>`).join("")}</ol>`
          : `<div>${renderMarkup(q.explanation || "")}</div>`;

        const lessonBtn = q.hasLesson
          ? `<button type="button" class="btn btn-xs btn-outline rev-lesson-btn" data-skill="${escapeHtml(q.skill)}">📖 ดูบทเรียน: ${escapeHtml(q.skillName)}</button>`
          : "";
        const drillBtn = q.hasLesson
          ? `<button type="button" class="btn btn-xs btn-primary rev-drill-btn" data-skill="${escapeHtml(q.skill)}" data-subject="${escapeHtml(q.subject)}">🎯 ฝึกซ่อมทักษะนี้</button>`
          : "";

        const timeTag = q.timeMs ? ` · ⏱️ ${Math.round(q.timeMs / 1000)} วินาที` : "";

        return `<article class="review-item ${klass}">
          <div class="status">
            <span>ข้อ ${i + 1} · ${status} · ${escapeHtml(q.topic)} (${escapeHtml(q.skillName || "")})${timeTag}</span>
            <span class="tag diff-${escapeHtml(q.difficulty || "medium")}">${escapeHtml(DIFF_TH[q.difficulty] || q.difficulty)}</span>
          </div>
          ${passageHtml}
          ${figHtml}
          ${tblHtml}
          <div class="q-stem">${renderMarkup(q.stem)}</div>
          <div>คำตอบของคุณ: <strong>${your}</strong></div>
          <div>เฉลยที่ถูกต้อง: <strong class="ok-text">${right}</strong></div>
          <div class="${q.status === "ok" ? "explain" : "mistake"}">
            ${whyChosenHtml}
            <strong>🪜 วิธีคิดทีละขั้น:</strong>
            ${stepsList}
            <div class="nav-row" style="margin-top:8px">${lessonBtn}${drillBtn}</div>
          </div>
        </article>`;
      })
      .join("");

    review.querySelectorAll(".rev-lesson-btn").forEach((b) => {
      b.addEventListener("click", () => openLessonModal(b.getAttribute("data-skill")));
    });
    review.querySelectorAll(".rev-drill-btn").forEach((b) => {
      b.addEventListener("click", () => {
        startCustomSession({
          mode: "skill",
          subject: b.getAttribute("data-subject"),
          focus: b.getAttribute("data-skill"),
          tutor: true,
          count: 8,
        });
      });
    });
  }

  // ==================== SCRATCHPAD CANVAS ====================

  function initScratchpad() {
    const canvas = $("#scratch-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let drawing = false;
    let penColor = "#1C1720";

    const colors = {
      ink: "#1C1720",
      pink: "#E91E8C",
      blue: "#2563EB",
    };

    $$(".scratch-tools .chip[data-pen]").forEach((btn) => {
      btn.addEventListener("click", () => {
        $$(".scratch-tools .chip[data-pen]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        penColor = colors[btn.getAttribute("data-pen")] || "#1C1720";
      });
    });

    function pos(e) {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return [(clientX - rect.left) * scaleX, (clientY - rect.top) * scaleY];
    }

    function start(e) {
      drawing = true;
      const [x, y] = pos(e);
      ctx.beginPath();
      ctx.moveTo(x, y);
      e.preventDefault();
    }

    function move(e) {
      if (!drawing) return;
      const [x, y] = pos(e);
      ctx.lineTo(x, y);
      ctx.strokeStyle = penColor;
      ctx.lineWidth = 2.4;
      ctx.lineCap = "round";
      ctx.stroke();
      e.preventDefault();
    }

    function stop() {
      drawing = false;
    }

    canvas.addEventListener("mousedown", start);
    canvas.addEventListener("mousemove", move);
    window.addEventListener("mouseup", stop);
    canvas.addEventListener("touchstart", start, { passive: false });
    canvas.addEventListener("touchmove", move, { passive: false });
    window.addEventListener("touchend", stop);

    $("#btn-scratch-clear").addEventListener("click", () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      $("#scratch-notes").value = "";
    });
  }

  function quitExam() {
    $("#modal-title").textContent = "ออกจากการฝึก/สอบ?";
    $("#modal-body").textContent = "ต้องการกลับหน้าหลักโดยไม่ส่งกระดาษคำตอบชุดนี้ใช่หรือไม่";
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
    if (["TEXTAREA", "INPUT"].includes(document.activeElement?.tagName)) return;
    if ($("#modal") && !$("#modal").classList.contains("hidden")) return;
    if ($("#lesson-modal") && !$("#lesson-modal").classList.contains("hidden")) return;
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
      if (state.tutor) {
        checkCurrentAnswer(i);
      } else {
        renderExam();
      }
    } else if (e.key === "h" || e.key === "H") {
      e.preventDefault();
      requestHint();
    } else if (e.key === "f" || e.key === "F") {
      e.preventDefault();
      state.flags[state.index] = !state.flags[state.index];
      renderExam();
    }
  }

  // ==================== INITIALIZATION ====================

  function init() {
    // Primary Tabs
    $$(".main-tab").forEach((btn) => {
      btn.addEventListener("click", () => switchTab(btn.getAttribute("data-tab")));
    });

    $("#btn-goto-curriculum").addEventListener("click", () => switchTab("curriculum"));

    // Quick action buttons on the Readiness Subject cards
    $$("[data-quick]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const q = btn.getAttribute("data-quick");
        if (q === "adaptive-math") startCustomSession({ mode: "adaptive", subject: "math", tutor: true, count: 10 });
        else if (q === "adaptive-eng") startCustomSession({ mode: "adaptive", subject: "english", tutor: true, count: 10 });
        else if (q === "diag-math") startCustomSession({ mode: "diagnostic", subject: "math", tutor: false });
        else if (q === "diag-eng") startCustomSession({ mode: "diagnostic", subject: "english", tutor: false });
        else if (q === "mock-math") startExamMode("math");
        else if (q === "mock-eng") startExamMode("english");
      });
    });

    // Mode Cards
    $$(".mode-card[data-mode]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const mode = btn.getAttribute("data-mode");
        if (mode === "practice") {
          const panel = $("#practice-panel");
          panel.classList.toggle("hidden");
          syncBuilderChips();
          if (!panel.classList.contains("hidden")) {
            panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
          }
          return;
        }
        startExamMode(mode);
      });
    });

    // Practice Builder controls
    $$("#subject-chips .chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        practiceSubject = btn.getAttribute("data-subject");
        practiceSkillKey = "";
        syncBuilderChips();
      });
    });

    $$("#diff-chips .chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        practiceDiff = btn.getAttribute("data-diff") || "";
        $$("#diff-chips .chip").forEach((b) => b.classList.toggle("active", b === btn));
      });
    });

    $$("#count-chips .chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        practiceCount = Number(btn.getAttribute("data-count")) || 8;
        $$("#count-chips .chip").forEach((b) => b.classList.toggle("active", b === btn));
      });
    });

    $("#btn-start-practice").addEventListener("click", startPractice);
    $("#btn-open-selected-lesson").addEventListener("click", () => {
      if (practiceSkillKey) openLessonModal(practiceSkillKey);
    });

    // Curriculum subject filter
    $$("#curr-subj-filter .chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        currSubjFilter = btn.getAttribute("data-curr-subj") || "all";
        $$("#curr-subj-filter .chip").forEach((b) => b.classList.toggle("active", b === btn));
        if (dashboard) renderCurriculum(dashboard.topics || []);
      });
    });

    // Notebook filter & review drill
    $$("#notebook-filter .chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        notebookSubjFilter = btn.getAttribute("data-nb-subj") || "";
        $$("#notebook-filter .chip").forEach((b) => b.classList.toggle("active", b === btn));
        loadMistakeNotebook();
      });
    });

    $("#btn-drill-mistakes").addEventListener("click", () => {
      startCustomSession({ mode: "review", subject: notebookSubjFilter || null, tutor: true, count: 8 });
    });

    $("#btn-review-mistakes-quick").addEventListener("click", () => {
      startCustomSession({ mode: "review", tutor: true, count: 8 });
    });

    $("#btn-practice-weak").addEventListener("click", () => {
      const btn = $("#btn-practice-weak");
      if (!btn.dataset.topic) return;
      startCustomSession({
        mode: "skill",
        subject: btn.dataset.subject,
        focus: btn.dataset.topic,
        tutor: true,
        count: 8,
      });
    });

    // Exam screen tools
    $("#btn-hint").addEventListener("click", requestHint);
    $("#btn-lesson-inline").addEventListener("click", () => {
      if (!state) return;
      const q = state.questions[state.index];
      if (q && q.skill) openLessonModal(q.skill);
    });
    $("#btn-flag").addEventListener("click", () => {
      if (!state) return;
      state.flags[state.index] = !state.flags[state.index];
      renderExam();
    });
    $("#btn-check-now").addEventListener("click", () => {
      if (!state) return;
      const sel = state.answers[state.index];
      if (sel != null) checkCurrentAnswer(sel);
    });
    $("#btn-toggle-scratch").addEventListener("click", () => {
      const sp = $("#scratchpad-panel");
      sp.classList.toggle("hidden");
      if (!sp.classList.contains("hidden")) {
        sp.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });

    $("#btn-prev").addEventListener("click", goPrev);
    $("#btn-next").addEventListener("click", goNext);
    $("#btn-skip").addEventListener("click", skip);
    $("#btn-submit").addEventListener("click", askSubmit);
    $("#btn-quit-exam").addEventListener("click", quitExam);

    $("#modal-cancel").addEventListener("click", () => {
      $("#modal").classList.add("hidden");
    });

    // Lesson modal controls
    $("#btn-close-lesson").addEventListener("click", () => {
      $("#lesson-modal").classList.add("hidden");
    });
    $("#btn-lesson-more-sample").addEventListener("click", () => {
      if (currentLessonSkill) openLessonModal(currentLessonSkill);
    });

    // Results screen buttons
    $("#btn-home").addEventListener("click", () => {
      state = null;
      viewingHistory = false;
      showScreen("screen-home");
      refreshHome();
    });

    $$("#review-filter .chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        reviewFilter = chip.getAttribute("data-filter") || "all";
        $$("#review-filter .chip").forEach((el) => el.classList.toggle("active", el === chip));
        renderReview();
      });
    });

    $("#btn-retry").addEventListener("click", () => {
      if (!state) {
        showScreen("screen-home");
        return;
      }
      startCustomSession({
        mode: state.mode,
        subject: state.subject,
        focus: state.focus,
        tutor: state.tutor,
        timer: state.totalSeconds != null,
      });
    });

    $("#btn-drill").addEventListener("click", () => {
      const btn = $("#btn-drill");
      if (!btn.dataset.focus) return;
      startCustomSession({
        mode: "skill",
        subject: btn.dataset.subject,
        focus: btn.dataset.focus,
        tutor: true,
        count: 8,
      });
    });

    $("#btn-pause").addEventListener("click", () => {
      if (!state || !state.allowPause) return;
      recordCurrentQuestionTime();
      state.paused = true;
      $("#pause-overlay").classList.remove("hidden");
    });
    $("#btn-resume").addEventListener("click", () => {
      if (!state) return;
      state.paused = false;
      state.questionEnteredAt = Date.now();
      $("#pause-overlay").classList.add("hidden");
    });

    document.addEventListener("keydown", onKey);
    initScratchpad();
    refreshHome();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
