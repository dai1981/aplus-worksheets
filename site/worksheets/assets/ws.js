/*! Aplus worksheets  /worksheets/assets/ws.js
 *  One file = reactions + scores + 100-question quiz + top CTA.
 *  Ported from eigo-duke.com sansu-fx.js / sansu-progress.js / sansu-quiz.js.
 *  All words come from window.WS_T (set by PHP per language).
 *
 *  Page markup:
 *    <div class="sn-quiz" data-quiz="s1"></div>
 *    <script type="application/json" data-quiz-for="s1">
 *      {"title":"...","key":"us-math-grade-3-area-1","items":[{"q":"","c":["","","",""],"a":0,"e":""}]}
 *    </script>
 *    <span class="sp-bar" data-prog="us-math-grade-3-area" data-sets="5"></span>
 *    <p data-prog-total="us-math-grade-3"></p>  <button data-prog-clear="us-math-grade-3">
 *  Scores live in localStorage only:  wsq:<key>-<set> = {"o":best correct,"t":total}
 */
(function () {
  "use strict";

  var T = window.WS_T || {};
  var ST = "wsq:";
  function t(k, map) {
    var s = T[k] != null ? String(T[k]) : k;
    if (map) for (var m in map) s = s.split("{" + m + "}").join(map[m]);
    return s;
  }

  // ------------------------------------------------------------ settings
  var CONFIG = {
    on: true,
    flow: { autoNext: true, okMs: 650, expOnCorrect: false, keys: true },
    color: { ok: "#006633", okLight: "#7fd3a0", ng: "#c0392b",
             confetti: ["#006633", "#7fd3a0", "#f2c94c", "#eb5757", "#2f80ed", "#9b51e0"] },
    particles: 12, confetti: 70, goodLine: 80,
    streakAt: [3, 5, 10, 15, 20]
  };
  var reduced = false;
  try { reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function later(n, ms) { setTimeout(function () { if (n && n.parentNode) n.parentNode.removeChild(n); }, ms); }

  // ------------------------------------------------------------ effects
  function ringSvg(c) {
    return '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="17" fill="none" stroke="'
      + c + '" stroke-width="6" stroke-linecap="round"/></svg>';
  }
  function crossSvg(c) {
    return '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M13 13 L35 35 M35 13 L13 35" fill="none" stroke="'
      + c + '" stroke-width="6" stroke-linecap="round"/></svg>';
  }
  function svgMark(ok) { return ok ? ringSvg(CONFIG.color.ok) : crossSvg(CONFIG.color.ng); }

  var FX = {
    badge: function (target, ok) {
      var b = el("span", "fx-badge" + (reduced ? " fx-still" : ""), svgMark(ok));
      target.appendChild(b);
      later(b, 1400);
    },
    word: function (root, text, ok) {
      if (!text) return;
      var w = el("div", "fx-word " + (ok ? "ok" : "ng") + (reduced ? " fx-still" : ""), text);
      root.appendChild(w);
      later(w, 1300);
    },
    particles: function (target) {
      if (reduced || !CONFIG.particles) return;
      var r = target.getBoundingClientRect(), wrap = el("div", "fx-parts");
      wrap.style.left = (r.left + r.width / 2) + "px";
      wrap.style.top = (r.top + r.height / 2) + "px";
      for (var i = 0; i < CONFIG.particles; i++) {
        var p = el("i"), ang = (Math.PI * 2 / CONFIG.particles) * i, d = 40 + Math.random() * 40;
        p.style.background = i % 2 ? CONFIG.color.ok : CONFIG.color.okLight;
        p.style.setProperty("--dx", Math.cos(ang) * d + "px");
        p.style.setProperty("--dy", Math.sin(ang) * d + "px");
        wrap.appendChild(p);
      }
      document.body.appendChild(wrap);
      later(wrap, 900);
    },
    confetti: function (root) {
      if (reduced || !CONFIG.confetti) return;
      var wrap = el("div", "fx-confetti");
      for (var i = 0; i < CONFIG.confetti; i++) {
        var p = el("i");
        p.style.left = Math.random() * 100 + "%";
        p.style.background = pick(CONFIG.color.confetti);
        p.style.animationDelay = (Math.random() * 500) + "ms";
        p.style.animationDuration = (1400 + Math.random() * 900) + "ms";
        wrap.appendChild(p);
      }
      root.appendChild(wrap);
      later(wrap, 2800);
    },
    answer: function (btn, ok, root, streak, quiet) {
      if (!CONFIG.on) return;
      if (!reduced) btn.classList.add(ok ? "fx-pop" : "fx-shake");
      FX.badge(btn, ok);
      if (ok) FX.particles(btn);
      if (quiet) return;
      var words = ok ? (T.okWords || ["Correct!"]) : (T.ngWords || ["Almost!"]);
      var text = pick(words);
      if (ok && streak && CONFIG.streakAt.indexOf(streak) >= 0 && T.streak && T.streak[streak]) {
        text = T.streak[streak];
      }
      FX.word(root, text, ok);
    },
    clear: function (root) {
      Array.prototype.forEach.call(root.querySelectorAll(".fx-word"), function (w) {
        if (w.parentNode) w.parentNode.removeChild(w);
      });
    },
    finish: function (root, ok, total) {
      var rate = total ? ok / total * 100 : 0;
      if (rate >= 100) { FX.confetti(root); FX.word(root, t("perfect"), true); }
      else if (rate >= CONFIG.goodLine) FX.word(root, t("good"), true);
    }
  };

  // ------------------------------------------------------------ scores
  function get(k) {
    try {
      var d = JSON.parse(localStorage.getItem(ST + k));
      return (d && typeof d.o === "number") ? d : null;
    } catch (e) { return null; }
  }
  function put(k, ok, total) {
    try {
      var cur = get(k);
      if (!cur || ok > cur.o) localStorage.setItem(ST + k, JSON.stringify({ o: ok, t: total }));
    } catch (e) {}
  }
  function sum(prefix, sets) {
    var ok = 0, total = 0, done = 0, bars = [];
    for (var i = 1; i <= sets; i++) {
      var d = get(prefix + "-" + i);
      total += d ? d.t : 20;
      if (d) { ok += d.o; if (d.o === d.t) done++; bars.push(Math.round(d.o / d.t * 100)); }
      else bars.push(-1);
    }
    return { ok: ok, total: total, done: done, bars: bars };
  }
  function drawBar(e) {
    var n = parseInt(e.getAttribute("data-sets"), 10) || 5, s = sum(e.getAttribute("data-prog"), n);
    var h = '<span class="sp-segs">';
    for (var i = 0; i < s.bars.length; i++) {
      var v = s.bars[i];
      h += '<i class="' + (v < 0 ? "none" : v === 100 ? "full" : "part") + '"><b style="width:' + (v < 0 ? 0 : v) + '%"></b></i>';
    }
    e.innerHTML = h + '</span><span class="sp-num">' + (s.ok ? s.ok + " / " + s.total : t("notYet")) + "</span>";
    e.setAttribute("data-done", s.done === n ? "1" : "0");
  }
  function drawTotal(e) {
    var g = e.getAttribute("data-prog-total"), ok = 0, total = 0, units = 0, clear = 0;
    Array.prototype.forEach.call(document.querySelectorAll('.sp-bar[data-prog^="' + g + '-"]'), function (r) {
      var n = parseInt(r.getAttribute("data-sets"), 10) || 5, s = sum(r.getAttribute("data-prog"), n);
      ok += s.ok; total += s.total; units++;
      if (s.done === n) clear++;
    });
    e.innerHTML = t("total", { o: ok, t: total }) + (clear ? " " + t("mastered", { c: clear, u: units }) : "");
  }
  function drawHook(b) {
    var k = b.getAttribute("data-k"), n = parseInt(b.getAttribute("data-n"), 10) || 5, done = 0, tried = 0;
    for (var i = 1; i <= n; i++) { var d = get(k + "-" + i); if (d) { tried++; if (d.o === d.t) done++; } }
    var m = b.querySelector(".qz-hook-m");
    if (m) m.textContent = !tried ? t("hook0") : done === n ? t("hookAll") : t("hookSome", { d: done, n: n, r: n - done });
  }
  function redraw() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-prog]"), drawBar);
    Array.prototype.forEach.call(document.querySelectorAll("[data-prog-total]"), drawTotal);
    Array.prototype.forEach.call(document.querySelectorAll(".qz-hook[data-k]"), drawHook);
    Rank.refresh();
  }
  function bindClear() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-prog-clear]"), function (b) {
      b.addEventListener("click", function () {
        if (!window.confirm(t("confirm"))) return;
        var g = ST + b.getAttribute("data-prog-clear") + "-";
        try {
          var del = [];
          for (var i = 0; i < localStorage.length; i++) {
            var k = localStorage.key(i);
            if (k && k.indexOf(g) === 0) del.push(k);
          }
          del.forEach(function (k) { localStorage.removeItem(k); });
        } catch (e) {}
        Rank.clear(b.getAttribute("data-prog-clear"));
        redraw();
      });
    });
  }


  // ------------------------------------------------------------ records
  //  ws:sum  { unitKey: {x: correct answers in total, n: sets done} }
  //  ws:day  { "2026-11-01": { gradeKey: correct answers } }  (60 days)
  //  ws:lv   { gradeKey: {goal: tier index, got: tiers reached, seen: number shown last time} }
  function rd(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function wr(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function today() { var d = new Date(); return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

  function record(setKey, gradeKey, ok, total) {
    var u = String(setKey).replace(/-\d+$/, "");
    var sum = rd("ws:sum", {}), e = sum[u] || (sum[u] = { x: 0, n: 0 });
    e.x += ok; e.n += 1;
    wr("ws:sum", sum);
    if (gradeKey) {
      var day = rd("ws:day", {}), d = day[today()] || (day[today()] = {});
      d[gradeKey] = (d[gradeKey] || 0) + ok;
      var ks = Object.keys(day).sort();
      while (ks.length > 60) delete day[ks.shift()];
      wr("ws:day", day);
    }
  }

  // ------------------------------------------------------------ ranks
  //  1 lap = every question of the grade answered correctly once.
  //  Each skill counts only up to the lap you are on, so practicing every skill moves you up.
  var Rank = (function () {
    var TIERS = [
      { k: "above",  x: 0.5 },  { k: "sight", x: 0.75 }, { k: "class", x: 1 },
      { k: "grade",  x: 2 },    { k: "state", x: 3 },    { k: "nation", x: 4 }, { k: "world", x: 5 }
    ];
    var COLORS = ["#4f9a6a", "#1f7a4c", "#b4783f", "#8e9cab", "#d39b12", "#c0392b", "#2f6fc4"];
    var FIRST_GOAL = 2, PER_SET = 20, RED = "#d6453b";
    function name(i) { return i < 0 ? t("start") : (T.tier && T.tier[TIERS[i].k]) || TIERS[i].k; }
    function lapText(i) { var x = TIERS[i].x; return x >= 1 ? t(x === 1 ? "lap" : "laps", { n: x }) : ""; }

    function best(u) {
      var b = 0;
      for (var i = 1; i <= u.sets; i++) { var d = get(u.k + "-" + i); if (d) b += d.o; }
      return b;
    }
    function measure(units, goal) {
      var sum = rd("ws:sum", {}), N = 0, xs = [];
      units.forEach(function (u) {
        var q = u.sets * PER_SET, x = Math.max(sum[u.k] ? sum[u.k].x : 0, best(u));
        N += q; xs.push([x, q]);
      });
      function capped(L) { var c = 0; xs.forEach(function (a) { c += Math.min(a[0], L * a[1]); }); return c; }
      var T2 = TIERS.map(function (r) { return Math.round(r.x * N); }), got = 0;
      for (var i = 0; i < TIERS.length && i <= goal; i++) {
        if (N && capped(Math.max(1, Math.ceil(TIERS[i].x))) >= T2[i]) got = i + 1;
      }
      return { N: N, T: T2, got: got, total: capped(Math.max(1, Math.ceil(TIERS[goal].x))) };
    }
    function st(g) { var s = rd("ws:lv", {}); return s[g] || { goal: FIRST_GOAL, got: 0, seen: 0 }; }
    function save(g, v) { var s = rd("ws:lv", {}); s[g] = v; wr("ws:lv", s); }
    function todayOf(g) { var d = rd("ws:day", {})[today()]; return (d && d[g]) || 0; }

    function starPath(cx, cy, R1, r) {
      var p = "";
      for (var i = 0; i < 10; i++) {
        var a = (-90 + 36 * i) * Math.PI / 180, rr = i % 2 ? r : R1;
        p += (i ? "L" : "M") + (cx + rr * Math.cos(a)).toFixed(1) + " " + (cy + rr * Math.sin(a)).toFixed(1);
      }
      return p + "Z";
    }
    function medal(i, sz, dim) {
      var c = i < 0 || dim ? "#c9c2b6" : COLORS[i], inner;
      if (i === TIERS.length - 1) inner = '<circle cx="32" cy="41" r="10" fill="none" stroke="#fff" stroke-width="2.4"/><ellipse cx="32" cy="41" rx="4.2" ry="10" fill="none" stroke="#fff" stroke-width="2"/><path d="M22 41h20" stroke="#fff" stroke-width="2"/>';
      else if (i <= 0) inner = '<circle cx="32" cy="41" r="5" fill="#fff"/>';
      else inner = '<path d="' + starPath(32, 41, 10.5, 4.6) + '" fill="#fff"/>';
      return '<svg class="lv-medal" width="' + sz + '" height="' + sz + '" viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
        + '<path d="M17 2h12l7 21H24z" fill="' + c + '" opacity=".7"/><path d="M47 2H35l-7 21h12z" fill="' + c + '"/>'
        + '<circle cx="32" cy="41" r="20" fill="' + c + '"/><circle cx="32" cy="41" r="15.5" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.5"/>'
        + inner + "</svg>";
    }
    var CHECK = '<svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    // ---------- the big card (grade page)
    function cardHTML(ctx, m, s, from) {
      var goal = s.goal, top = m.T[goal], reached = m.total >= top, got = Math.max(m.got, s.got), tn = todayOf(ctx.g), h = "";
      h += '<div class="lv-head">' + medal(got - 1, 64) + '<div class="lv-hd"><p class="lv-sub">' + t("yourRank", { name: ctx.name })
        + '</p><p class="lv-title">' + name(got - 1) + '</p></div><p class="lv-cnt"><b class="lv-num">' + fmt(from) + "</b><span>"
        + t("correct") + "</span>" + (tn ? "<i>" + t("todayPlus", { n: fmt(tn) }) + "</i>" : "") + "</p></div>";
      var p0 = top ? Math.min(100, from / top * 100) : 0;
      h += '<div class="lv-track"><div class="lv-in"><div class="lv-bar"><i class="lv-fill" style="width:' + p0.toFixed(1) + '%"></i></div>'
        + '<span class="lv-pin" style="left:' + p0.toFixed(1) + '%"><b></b></span>';
      for (var i = goal === FIRST_GOAL ? 0 : FIRST_GOAL; i < goal; i++) {
        var at = m.T[i] / top * 100;
        h += '<span class="lv-mk' + (m.total >= m.T[i] ? " on" : "") + (i % 2 ? " lo" : "") + '" style="left:' + at.toFixed(1) + '%"><em></em><small>'
          + name(i) + '<span class="c"><br>' + fmt(m.T[i]) + "</span></small></span>";
      }
      h += '</div><span class="lv-flag' + (reached ? " got" : "") + '">' + medal(goal, 46) + "</span></div>";
      h += '<div class="lv-ends"><span>' + t("start") + '</span><span class="lv-goalname"><b>' + name(goal) + "</b><small>"
        + (lapText(goal) ? lapText(goal) + " · " : "") + fmt(top) + "</small></span></div>";
      if (!reached) h += '<p class="lv-rest">' + t("more", { n: fmt(top - m.total), t: name(goal) }) + "</p>";
      else if (goal + 1 < TIERS.length) h += '<button type="button" class="lv-up">' + t("reachedBtn") + "</button>";
      else h += '<p class="lv-rest"><b>' + t("allDone") + "</b></p>";
      return h + ladderHTML(ctx, m, got, goal);
    }

    // ---------- ranking ladder: top rank first, "You" row where you stand
    //  Ranks up to the current goal are shown. Above it, one locked row:
    //  far from the goal it only says more ranks follow; one rank before the goal it reveals the next rank's name,
    //  so a new target is waiting before the current one is reached.
    var LOCK = '<svg width="30" height="30" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><circle cx="32" cy="34" r="22" fill="#ece7df"/>'
      + '<rect x="21" y="31" width="22" height="16" rx="3" fill="#b3aa9e"/><path d="M25 31v-5a7 7 0 0 1 14 0v5" fill="none" stroke="#b3aa9e" stroke-width="4"/></svg>';
    function ladderHTML(ctx, m, got, goal) {
      var h = '<div class="lv-ladder"><p class="lv-lh">' + t("ranks") + "</p><ol>", you = false, nextShown = false;
      var top = Math.min(TIERS.length - 1, Math.max(FIRST_GOAL, got, goal || 0));
      if (top < TIERS.length - 1) {
        if (got >= top) h += '<li class="lock peek"><span class="md">' + LOCK + '</span><span class="n">' + name(top + 1)
          + "<small>" + t("unlocksAfter", { t: name(top) }) + '</small></span><span class="r">' + fmt(m.T[top + 1]) + '</span><span class="s"></span></li>';
        else h += '<li class="lock"><span class="md">' + LOCK + '</span><span class="n">' + t("moreAfter", { t: name(top) })
          + '</span><span class="r"></span><span class="s"></span></li>';
      }
      function youRow() {
        return '<li class="you"><span class="md"><span class="dot"></span></span><span class="n">' + t("you") + '</span><span class="r">'
          + fmt(m.total) + "</span><span class=\"s\"></span></li>";
      }
      for (var i = top; i >= 0; i--) {
        var done = i < got;
        if (done && !you) { h += youRow(); you = true; }
        var cls = done ? "done" : "", tag = "";
        if (done) tag = CHECK + '<span class="tx">' + t("reached") + "</span>";
        else if (i === got) { cls = "next"; tag = t("toGoShort", { n: fmt(Math.max(0, m.T[i] - m.total)) }); nextShown = true; }
        h += '<li class="' + cls + '"><span class="md">' + medal(i, 30, !done && i !== got) + '</span><span class="n">' + name(i)
          + (lapText(i) ? "<small>" + lapText(i) + "</small>" : "") + '</span><span class="r">' + fmt(m.T[i]) + '</span><span class="s">' + tag + "</span></li>";
      }
      if (!you) h += youRow();
      return h + '</ol><p class="lv-how">' + t("how", { name: ctx.name, n: fmt(m.N) }) + "</p></div>";
    }

    // ---------- small strip (skill page) and tiles (subject page)
    function miniHTML(ctx, m, s) {
      var got = Math.max(m.got, s.got), goal = s.goal, top = m.T[goal], p = top ? Math.min(100, m.total / top * 100) : 0;
      return medal(got - 1, 38) + '<span class="t"><small>' + t("rankOf", { name: ctx.name }) + "</small><b>" + name(got - 1) + "</b></span>"
        + '<span class="br"><i style="width:' + p.toFixed(1) + '%"></i></span><span class="c">'
        + (m.total >= top ? name(goal) + " " + CHECK : t("toGo", { n: fmt(top - m.total), t: name(goal) })) + "</span>";
    }
    function tileHTML(m, s) {
      var got = Math.max(m.got, s.got), top = m.T[s.goal], p = top ? Math.min(100, m.total / top * 100) : 0;
      if (!m.total) return '<span class="lv-t0">' + t("notStarted") + "</span>";
      return '<span class="lv-t">' + medal(got - 1, 20) + name(got - 1) + '</span><span class="lv-tb"><i style="width:' + p.toFixed(1) + '%"></i></span>';
    }

    // ---------- popups
    function confetti() {
      if (reduced) return "";
      var cols = ["#d6453b", "#d39b12", "#2f6fc4", "#1f8a5b", "#b4783f"], cf = "";
      for (var i = 0; i < 28; i++) cf += '<i style="left:' + (Math.random() * 100).toFixed(1) + "%;background:" + cols[i % 5] + ";animation-delay:" + (Math.random() * .6).toFixed(2) + 's"></i>';
      return '<div class="lv-cf">' + cf + "</div>";
    }
    function modal(html, buttons) {
      var el = document.createElement("div");
      el.className = "lv-pop"; el.setAttribute("role", "dialog"); el.setAttribute("aria-modal", "true");
      el.innerHTML = confetti() + '<div class="lv-pin2">' + html + '<p class="lv-btns"></p></div>';
      var row = el.querySelector(".lv-btns");
      function close() { if (el.parentNode) el.parentNode.removeChild(el); }
      buttons.forEach(function (b, i) {
        var bt = document.createElement("button");
        bt.type = "button"; bt.className = i ? "sub" : ""; bt.textContent = b.t;
        bt.onclick = function () { close(); if (b.f) b.f(); };
        row.appendChild(bt);
      });
      el.addEventListener("click", function (e) { if (e.target === el) close(); });
      document.body.appendChild(el);
      try { row.firstChild.focus(); } catch (e) {}
    }
    function popPass(i) {
      modal(medal(i, 96) + '<p class="lv-p1">' + t("levelUp") + '</p><p class="lv-p2">' + name(i) + '</p><p class="lv-p3">'
        + t("keepGoing", { t: name(i + 1) }) + "</p>", [{ t: t("yay") }]);
    }
    function popGoal(i, onYes) {
      var nx = i + 1 < TIERS.length ? '<p class="lv-ask">' + t("ask", { t: name(i + 1), l: lapText(i + 1) }) + "</p>" : "";
      modal(medal(i, 110) + '<p class="lv-p1">' + t("achieved") + '</p><p class="lv-p2">' + name(i) + "</p>" + nx,
        nx ? [{ t: t("goFor"), f: onYes }, { t: t("later") }] : [{ t: t("yay") }]);
    }

    // ---------- mount
    function ctxOf(el) {
      var units = [];
      try { units = JSON.parse(el.getAttribute("data-lv-units")) || []; } catch (e) {}
      return { el: el, g: el.getAttribute("data-lv"), name: el.getAttribute("data-lv-name") || "",
               mode: el.getAttribute("data-lv-mode") || "card",
               units: units.map(function (a) { return { k: a[0], sets: a[1] || 5 }; }) };
    }
    var popped = false;
    function draw(ctx) {
      var s = st(ctx.g), m = measure(ctx.units, s.goal);
      if (!m.N) return;
      if (ctx.mode === "tile") { ctx.el.innerHTML = tileHTML(m, s); return; }
      if (ctx.mode === "mini") ctx.el.innerHTML = miniHTML(ctx, m, s);
      if (ctx.mode === "card") {
        var sig = m.total + "|" + s.goal + "|" + todayOf(ctx.g);
        if (ctx.sig !== sig) {
          ctx.sig = sig;
          var from = Math.min(m.total, s.seen || 0);
          ctx.el.innerHTML = cardHTML(ctx, m, s, from);
          grow(ctx.el, from, m.total, m.T[s.goal]);
          var up = ctx.el.querySelector(".lv-up");
          if (up) up.onclick = function () { popGoal(s.goal, function () { next(ctx); }); };
        }
        s.seen = m.total;
      }
      // a new rank was reached: celebrate once (card or mini, not tiles)
      if (m.got > (s.got || 0)) {
        var i = m.got - 1, goal = s.goal;
        s.got = m.got;
        if (!popped) {
          popped = true;
          setTimeout(function () {
            popped = false;
            if (i === goal) popGoal(i, function () { next(ctx); }); else popPass(i);
          }, ctx.mode === "card" ? 1700 : 300);
        }
      }
      save(ctx.g, s);
    }
    function next(ctx) {
      var s = st(ctx.g);
      if (s.goal + 1 < TIERS.length) s.goal++;
      s.seen = 0;
      save(ctx.g, s);
      ctx.sig = "";
      draw(ctx);
    }
    function grow(root, from, to, top) {
      var fill = root.querySelector(".lv-fill"), pin = root.querySelector(".lv-pin"), tag = pin && pin.querySelector("b"),
          num = root.querySelector(".lv-num"), pct = (top ? Math.min(100, to / top * 100) : 0).toFixed(1) + "%";
      if (tag) tag.textContent = to > from ? "+" + fmt(to - from) : fmt(to);
      setTimeout(function () {
        if (fill) fill.style.width = pct;
        if (pin) pin.style.left = pct;
        if (tag) tag.className = "show";
        if (!num) return;
        if (reduced || to === from) { num.textContent = fmt(to); return; }
        var t0 = null;
        function step(ts) {
          if (!t0) t0 = ts;
          var k = Math.min(1, (ts - t0) / 1400), e = 1 - Math.pow(1 - k, 3);
          num.textContent = fmt(Math.round(from + (to - from) * e));
          if (k < 1) requestAnimationFrame(step);
          else { num.className = "lv-num pop"; if (tag) tag.textContent = fmt(to); }
        }
        requestAnimationFrame(step);
      }, 250);
    }

    var list = null;
    function refresh() {
      if (!list) list = Array.prototype.map.call(document.querySelectorAll("[data-lv]"), ctxOf);
      list.forEach(draw);
    }
    function clear(g) {
      var s = rd("ws:lv", {}); delete s[g]; wr("ws:lv", s);
      var sum = rd("ws:sum", {});
      Object.keys(sum).forEach(function (k) { if (k.indexOf(g + "-") === 0) delete sum[k]; });
      wr("ws:sum", sum);
      var day = rd("ws:day", {});
      Object.keys(day).forEach(function (d) { delete day[d][g]; });
      wr("ws:day", day);
      (list || []).forEach(function (c) { c.sig = ""; });
    }
    return { refresh: refresh, clear: clear };
  })();

  // ------------------------------------------------------------ quiz
  function cols(cs) {
    var mx = 0;
    for (var i = 0; i < cs.length; i++) {
      var s = String(cs[i]).replace(/<[^>]*>/g, "");
      if (s.length > mx) mx = s.length;
    }
    return mx <= 12 ? " sn-c2" : "";
  }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), x = a[i]; a[i] = a[j]; a[j] = x;
    }
    return a;
  }

  function Quiz(root, data) {
    var self = this;
    this.root = root;
    this.title = data.title || t("practice");
    this.key = data.key || location.pathname + root.getAttribute("data-quiz");
    this.grade = data.grade || "";
    this.all = data.items || [];
    this.minH = 0;
    this.timer = null;
    this.shell();
    this.begin(this.all);
    setTimeout(function () { self.lock(); }, 0);
    try { if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { self.lock(); }); } catch (e) {}
    window.addEventListener("load", function () { self.lock(); });
    var rt = null;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { self.lock(true); }, 200);
    });
  }

  Quiz.prototype.shell = function () {
    var self = this;
    this.root.innerHTML = '<div class="sn-quiz-h"><span class="t"></span><span class="n"></span></div>'
      + '<div class="sn-quiz-b"><div class="sn-bar"><i></i></div><div class="sn-stage">'
      + '<div class="sn-q"></div><div class="sn-choices"></div></div><div class="sn-fb" hidden></div></div>';
    this.root.querySelector(".sn-quiz-h .t").textContent = this.title;
    this.eN = this.root.querySelector(".sn-quiz-h .n");
    this.eBar = this.root.querySelector(".sn-bar i");
    this.eStage = this.root.querySelector(".sn-stage");
    this.eQ = this.root.querySelector(".sn-q");
    this.eC = this.root.querySelector(".sn-choices");
    this.eFb = this.root.querySelector(".sn-fb");
    this.eFb.addEventListener("click", function () { self.next(); });
    this.root.addEventListener("keydown", function (ev) {
      if (!CONFIG.flow.keys) return;
      if (ev.key === "Enter" || ev.key === " ") {
        if (!self.eFb.hidden) { ev.preventDefault(); self.next(); }
        return;
      }
      var k = "1234".indexOf(ev.key);
      if (k >= 0 && self.eFb.hidden) {
        var b = self.eC.children[k];
        if (b && !b.disabled) { ev.preventDefault(); b.click(); }
      }
    });
  };

  // measure every question once so the card height never jumps
  Quiz.prototype.lock = function (reset) {
    if (!this.all.length) return;
    var w = this.root.offsetWidth;
    if (!w) return;
    if (reset) { this.minH = 0; this.eStage.style.minHeight = ""; }
    if (this.lockedW === w && this.minH && !reset) return;
    this.lockedW = w;
    var probe = document.createElement("div");
    probe.className = "sn-quiz";
    probe.style.cssText = "position:absolute;left:-99999px;top:0;visibility:hidden;pointer-events:none;box-sizing:border-box;width:" + w + "px;";
    document.body.appendChild(probe);
    var max = 0;
    for (var i = 0; i < this.all.length; i++) {
      var it = this.all[i], html = "";
      for (var k = 0; k < it.c.length; k++) html += '<button type="button">' + it.c[k] + "</button>";
      probe.innerHTML = '<div class="sn-quiz-b"><div class="sn-bar"><i></i></div><div class="sn-stage"><div class="sn-q">'
        + it.q + '</div><div class="sn-choices' + cols(it.c) + '">' + html + "</div></div></div>";
      max = Math.max(max, probe.querySelector(".sn-stage").offsetHeight);
      probe.innerHTML = '<div class="sn-quiz-b"><div class="sn-fb ng" style="position:static"><div class="sn-fb-in"><div class="sn-fb-body">'
        + '<div class="sn-fb-mk">' + svgMark(false) + '</div><p class="sn-fb-t">' + t("ng") + '</p><p class="sn-fb-a">'
        + t("ans") + " <b>" + it.c[it.a] + "</b></p>" + (it.e ? '<div class="sn-exp">' + it.e + "</div>" : "")
        + '</div><button type="button" class="sn-next">' + t("next") + "</button></div></div></div>";
      max = Math.max(max, probe.querySelector(".sn-fb").offsetHeight);
    }
    probe.parentNode.removeChild(probe);
    max = Math.max(max, this.eStage.scrollHeight);
    if (max > this.minH) { this.minH = max; this.eStage.style.minHeight = max + "px"; }
  };

  Quiz.prototype.begin = function (items) {
    this.items = items.slice();
    this.i = 0; this.ok = 0; this.streak = 0; this.miss = []; this.ended = false;
    this.draw();
  };

  Quiz.prototype.draw = function () {
    if (this.i >= this.items.length) return this.done();
    var self = this, it = this.items[this.i], n = this.items.length;
    clearTimeout(this.timer);
    FX.clear(this.root);
    this.eFb.hidden = true;
    this.eFb.className = "sn-fb";
    this.eFb.innerHTML = "";
    this.eN.textContent = (this.i + 1) + " / " + n;
    this.eBar.style.width = (this.i / n * 100) + "%";
    this.eQ.innerHTML = it.q;
    this.eC.className = "sn-choices" + cols(it.c);
    this.eC.innerHTML = "";
    var opts = it.c.map(function (s, k) { return { t: s, ok: k === it.a }; });
    // choices that are picture labels (A-D, Net 1, Mix B) stay in order so they match the picture
    var labels = it.c.every(function (s) { return /^\s*(?:[A-H]|[A-Za-z]+ [A-H1-9])\s*$/.test(String(s).replace(/<[^>]+>/g, "")); });
    this.opts = labels ? opts.sort(function (x, y) {
      var a = String(x.t).replace(/<[^>]+>/g, "").trim(), b = String(y.t).replace(/<[^>]+>/g, "").trim();
      return a.localeCompare(b, "en", { numeric: true });
    }) : shuffle(opts);
    this.opts.forEach(function (o) {
      var b = document.createElement("button");
      b.type = "button";
      b.innerHTML = o.t;
      b.addEventListener("click", function () { self.hit(o.ok, b); });
      self.eC.appendChild(b);
    });
    var h = this.eStage.scrollHeight;
    if (h > this.minH) { this.minH = h; this.eStage.style.minHeight = h + "px"; }
  };

  Quiz.prototype.hit = function (right, clicked) {
    var self = this, it = this.items[this.i], F = CONFIG.flow;
    var btns = this.eC.querySelectorAll("button");
    Array.prototype.forEach.call(btns, function (b, k) {
      b.disabled = true;
      if (self.opts[k].ok) b.classList.add("ok");
    });
    if (right) { this.ok++; this.streak++; }
    else { clicked.classList.add("ng"); this.streak = 0; this.miss.push(it); }
    FX.answer(clicked, right, this.root, this.streak, !right || F.expOnCorrect || !F.autoNext);
    if (!right) {
      Array.prototype.forEach.call(btns, function (b, k) { if (self.opts[k].ok) FX.badge(b, true); });
    }
    if (right && F.autoNext && !F.expOnCorrect) {
      this.timer = setTimeout(function () { self.next(); }, F.okMs);
      return;
    }
    this.show(right, it);
  };

  Quiz.prototype.show = function (right, it) {
    var self = this, last = this.i + 1 >= this.items.length, ans = "";
    if (!right) for (var k = 0; k < this.opts.length; k++) if (this.opts[k].ok) { ans = this.opts[k].t; break; }
    this.eFb.className = "sn-fb " + (right ? "ok" : "ng");
    this.eFb.innerHTML = '<div class="sn-fb-in"><div class="sn-fb-body"><div class="sn-fb-mk">' + svgMark(right) + "</div>"
      + '<p class="sn-fb-t">' + t(right ? "ok" : "ng") + "</p>"
      + (ans ? '<p class="sn-fb-a">' + t("ans") + " <b>" + ans + "</b></p>" : "")
      + (it.e ? '<div class="sn-exp">' + it.e + "</div>" : "")
      + '</div><button type="button" class="sn-next">' + t(last ? "result" : "next") + "</button></div>";
    this.eFb.hidden = false;
    var nx = this.eFb.querySelector(".sn-next");
    nx.addEventListener("click", function (ev) { ev.stopPropagation(); self.next(); });
    try { nx.focus({ preventScroll: true }); } catch (e) { nx.focus(); }
    if (right && CONFIG.flow.autoNext) this.timer = setTimeout(function () { self.next(); }, CONFIG.flow.okMs + 900);
  };

  Quiz.prototype.next = function () {
    clearTimeout(this.timer);
    if (this.ended) return;
    this.i++;
    this.draw();
  };

  Quiz.prototype.done = function () {
    var self = this, n = this.items.length, rate = n ? Math.round(this.ok / n * 100) : 0, prev = get(this.key);
    this.ended = true;
    clearTimeout(this.timer);
    if (n === this.all.length) put(this.key, this.ok, n);   // retrying only the misses is not recorded
    record(this.key, this.grade, this.ok, n);                // every correct answer counts toward the rank
    this.eN.textContent = t("done");
    this.eBar.style.width = "100%";
    this.eFb.hidden = true;
    this.eFb.innerHTML = "";
    this.eStage.innerHTML = '<div class="sn-result"><p class="sn-score">' + t("score", { o: this.ok, n: n }) + "</p>"
      + (prev ? '<p class="sn-best">' + t("best", { o: prev.o, t: prev.t }) + "</p>" : "")
      + '<p class="sn-msg">' + t(rate === 100 ? "m100" : rate >= 80 ? "m80" : "mlow") + "</p>"
      + (this.miss.length ? '<button type="button" class="sn-again" data-m="1">' + t("redoMiss", { n: this.miss.length }) + "</button>" : "")
      + '<button type="button" class="sn-again" data-m="0">' + t("redoAll") + "</button></div>";
    FX.finish(this.root, this.ok, n);
    redraw();
    Array.prototype.forEach.call(this.eStage.querySelectorAll(".sn-again"), function (btn) {
      btn.addEventListener("click", function () {
        self.eStage.innerHTML = '<div class="sn-q"></div><div class="sn-choices"></div>';
        self.eQ = self.eStage.querySelector(".sn-q");
        self.eC = self.eStage.querySelector(".sn-choices");
        if (self.minH) self.eStage.style.minHeight = self.minH + "px";
        self.begin(btn.getAttribute("data-m") === "1" ? self.miss : self.all);
      });
    });
  };

  // ------------------------------------------------------------ boot
  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll(".sn-quiz[data-quiz]"), function (root) {
      var src = document.querySelector('script[data-quiz-for="' + root.getAttribute("data-quiz") + '"]');
      if (!src) return;
      var data;
      try { data = JSON.parse(src.textContent); }
      catch (e) { root.innerHTML = '<div class="sn-quiz-b">' + t("loadErr") + "</div>"; return; }
      if (data.items && data.items.length) new Quiz(root, data);
    });
    bindClear();
    redraw();
  }
  window.WS = { config: CONFIG, redraw: redraw, get: get, put: put, rank: Rank };
  window.addEventListener("pageshow", function (e) { if (e.persisted) redraw(); });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
