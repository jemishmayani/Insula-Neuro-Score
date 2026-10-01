/* Insula Neuro Score — application shell
 * Screens: Home, Calculate (list + calculator), Guide (list + guide), Settings.
 * All content comes from content/manifest.json and content/scores/<id>.json.        */
(function () {
  "use strict";
  var E = window.ScoreEngine;
  var A = window.Android || null;
  var $main = document.getElementById("main"), $bar = document.getElementById("appbar"),
      $tabs = document.getElementById("tabbar"), $live = document.getElementById("live");

  /* ---------------- icons ---------------- */
  function svg(p, extra) { return '<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"' + (extra || "") + '>' + p + '</svg>'; }
  var I = {
    home: svg('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
    calc: svg('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8"/><path d="M8 12h2M14 12h2M8 16h2M14 16h2"/>'),
    guide: svg('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/><path d="M9 7h6M9 11h6"/>'),
    gear: svg('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>'),
    search: svg('<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>'),
    star: svg('<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>'),
    chev: svg('<path d="M9 6l6 6-6 6"/>', ' class="i chev"'),
    back: svg('<path d="M15 6l-6 6 6 6"/>'),
    copy: svg('<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h8"/>'),
    share: svg('<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/>'),
    reset: svg('<path d="M4 12a8 8 0 1 0 2.3-5.7"/><path d="M4 4v4h4"/>'),
    up: svg('<path d="M6 15l6-6 6 6"/>'), down: svg('<path d="M6 9l6 6 6-6"/>'), x: svg('<path d="M6 6l12 12M18 6L6 18"/>'),
    flag: svg('<path d="M5 21V4h11l-1.5 4L16 12H5"/>')
  };
  var SI = { /* state icons: distinct shapes, never colour alone */
    normal: svg('<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.8"/>'),
    low: svg('<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.8"/>'),
    mild: svg('<circle cx="12" cy="12" r="9"/><path d="M8 12h8"/>'),
    moderate: svg('<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5"/><path d="M12 17.3v.2"/>'),
    high: svg('<path d="M8.2 2.8h7.6l5.4 5.4v7.6l-5.4 5.4H8.2l-5.4-5.4V8.2z"/><path d="M12 7.5v6"/><path d="M12 16.5v.2"/>'),
    critical: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M8.2 2.8h7.6l5.4 5.4v7.6l-5.4 5.4H8.2l-5.4-5.4V8.2z" fill="currentColor"/><path d="M12 7.5v6M12 16.5v.2" stroke="var(--surface)" stroke-width="2.4" stroke-linecap="round"/></svg>',
    info: svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v6"/><path d="M12 7.6v.2"/>'),
    incomplete: svg('<circle cx="12" cy="12" r="9" stroke-dasharray="3 3"/><path d="M8.5 12h.1M12 12h.1M15.5 12h.1"/>')
  };
  var STATE_NAME = { normal: "Normal / low concern", low: "Low concern", mild: "Mild", moderate: "Moderate", high: "High concern", critical: "Very high concern", info: "Informational", incomplete: "Incomplete" };

  /* ---------------- utils ---------------- */
  function esc(s) { return s == null ? "" : String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function toast(msg) {
    var t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); t.textContent = msg;
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 2200);
  }
  function uniqPush(arr, id, max) { arr = arr.filter(function (x) { return x !== id; }); arr.unshift(id); return arr.slice(0, max || 8); }

  /* ---------------- preferences ---------------- */
  var DEFAULTS = { theme: "system", highContrast: false, startup: "home", pinned: [], favGuides: [], recentCalc: [], recentGuide: [],
                   groupOrder: [], hiddenGroups: [], homeGroups: ["consciousness", "sah"] };
  var COMMON = ["gcs", "ich", "wfns", "mfisher", "mrs"];
  var P = (function () { try { return Object.assign({}, DEFAULTS, JSON.parse(localStorage.getItem("ins.prefs") || "{}")); } catch (e) { return Object.assign({}, DEFAULTS); } })();
  function save() { try { localStorage.setItem("ins.prefs", JSON.stringify(P)); } catch (e) {} }

  var mq = window.matchMedia ? matchMedia("(prefers-color-scheme: dark)") : null;
  function applyTheme() {
    var dark = P.theme === "dark" || (P.theme === "system" && mq && mq.matches);
    document.documentElement.setAttribute("data-theme", dark ? "dark" : "light");
    if (P.highContrast) document.documentElement.setAttribute("data-contrast", "high"); else document.documentElement.removeAttribute("data-contrast");
    try { if (A) A.setSystemBars(dark); } catch (e) {}
  }
  if (mq && mq.addEventListener) mq.addEventListener("change", function () { if (P.theme === "system") applyTheme(); });

  /* ---------------- content ---------------- */
  var M = null, cache = {}, answers = {};
  function loadManifest() { return fetch("content/manifest.json").then(function (r) { return r.json(); }).then(function (m) { M = m; return m; }); }
  function loadScore(id) {
    if (cache[id]) return Promise.resolve(cache[id]);
    return fetch("content/scores/" + encodeURIComponent(id) + ".json").then(function (r) { if (!r.ok) throw new Error("Score not found"); return r.json(); })
      .then(function (s) { var errs = E.validate(s); if (errs.length) throw new Error("Content error in " + id + ": " + errs.join("; ")); cache[id] = s; return s; });
  }
  function entry(id) { return M.scores.filter(function (s) { return s.id === id; })[0]; }
  function cats() {
    var order = P.groupOrder.slice();
    M.categories.forEach(function (c) { if (order.indexOf(c.id) < 0) order.push(c.id); });
    return order.map(function (id) { return M.categories.filter(function (c) { return c.id === id; })[0]; }).filter(Boolean)
      .map(function (c) { return Object.assign({}, c, { scores: M.scores.filter(function (s) { return s.category === c.id; }) }); });
  }
  function catName(id) { var c = M.categories.filter(function (c) { return c.id === id; })[0]; return c ? c.name : id; }
  function search(q) {
    q = q.trim().toLowerCase(); if (!q) return [];
    return M.scores.map(function (s) {
      var hay = [s.abbreviation, s.name].concat(s.aliases).map(function (x) { return x.toLowerCase(); }), rank = 9;
      hay.forEach(function (h, i) { if (h === q) rank = Math.min(rank, 0); else if (h.indexOf(q) === 0) rank = Math.min(rank, i < 2 ? 1 : 2); else if (h.indexOf(q) >= 0) rank = Math.min(rank, 3); });
      if (rank === 9 && catName(s.category).toLowerCase().indexOf(q) >= 0) rank = 4;
      return { s: s, rank: rank };
    }).filter(function (x) { return x.rank < 9; }).sort(function (a, b) { return a.rank - b.rank; }).map(function (x) { return x.s; });
  }

  /* ---------------- shell ---------------- */
  var navDepth = 0, route = {}, ignoreNextHash = false;
  function go(hash) { navDepth++; location.hash = hash; }
  window.addEventListener("hashchange", function () { render(); });
  window.handleBack = function () {
    if (navDepth > 0) { navDepth--; history.back(); return true; }
    var start = "#/" + (P.startup === "home" ? "home" : P.startup);
    if (location.hash !== start && route.section !== P.startup) { location.replace(start); return true; }
    return false;
  };

  function tabs(active) {
    var t = [["home", "Home", I.home], ["calc", "Calculate", I.calc], ["guide", "Guide", I.guide]];
    $tabs.innerHTML = t.map(function (x) {
      return '<a href="#/' + x[0] + '" data-nav ' + (active === x[0] ? 'aria-current="page"' : "") + '><span class="pill">' + x[2] + '</span>' + x[1] + '</a>';
    }).join("");
  }
  function appbar(title, opts) {
    opts = opts || {};
    var left = opts.back ? '<button class="iconbtn" data-act="back" aria-label="Back">' + I.back + '</button>' : "";
    var brand = opts.brand ? '<span class="brand"><img class="brand-mark" src="img/mark.png" alt="">' : "";
    $bar.style.paddingLeft = opts.back ? ".25rem" : "1rem";
    $bar.innerHTML = left + '<h1>' + brand + esc(title) + (opts.brand ? "</span>" : "") + '</h1>' +
      (opts.settings !== false ? '<a class="iconbtn" href="#/settings" data-nav aria-label="Settings">' + I.gear + '</a>' : "");
  }

  function parseHash() {
    var h = location.hash.replace(/^#\/?/, ""), q = {}, path = h, i = h.indexOf("?");
    if (i >= 0) { path = h.slice(0, i); h.slice(i + 1).split("&").forEach(function (kv) { var p = kv.split("="); q[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ""); }); }
    var parts = path.split("/").filter(Boolean);
    return { section: parts[0] || "", id: parts[1] || null, q: q };
  }

  function render() {
    route = parseHash();
    document.querySelectorAll(".toast").forEach(function (t) { t.remove(); });
    document.body.classList.remove("has-bar");
    var sb = document.querySelector(".sticky-result"); if (sb) sb.remove();
    var s = route.section;
    if (!s) { location.replace("#/" + (P.startup || "home")); return; }
    if (s === "home") return homeView();
    if (s === "calc" && route.id) return scoreView("calc", route.id);
    if (s === "guide" && route.id) return scoreView("guide", route.id);
    if (s === "calc" || s === "guide") return listView(s);
    if (s === "settings") return settingsView();
    location.replace("#/home");
  }
  function show(html) { $main.innerHTML = html; window.scrollTo(0, 0); }

  /* ---------------- rows ---------------- */
  function scoreRow(s, mode, opts) {
    opts = opts || {};
    var href = "#/" + (mode === "guide" ? "guide" : "calc") + "/" + s.id;
    var star = opts.star ? '<button class="iconbtn star" data-act="pin" data-id="' + s.id + '" aria-pressed="' + (P.pinned.indexOf(s.id) >= 0) + '" aria-label="' + (P.pinned.indexOf(s.id) >= 0 ? "Remove " + esc(s.abbreviation) + " from Home" : "Pin " + esc(s.abbreviation) + " to Home") + '">' + I.star + '</button>' : "";
    var both = opts.both ? '<span class="mini-links"><a href="#/calc/' + s.id + '" data-nav>Calculate</a><a href="#/guide/' + s.id + '" data-nav>Guide</a></span>' : "";
    var main = '<span class="row-main"><span class="row-title">' + esc(s.abbreviation) + (opts.kind ? '<span class="row-kind">' + opts.kind + '</span>' : "") + '</span><span class="row-sub">' + esc(s.name === s.abbreviation ? catName(s.category) : s.name) + (opts.cat && s.name !== s.abbreviation ? " · " + esc(catName(s.category)) : "") + '</span></span>';
    if (opts.both) return '<li class="row">' + main + both + '</li>';
    return '<li class="row"><a class="go" href="' + href + '" data-nav>' + main + I.chev + '</a>' + star + '</li>';
  }
  function list(items) { return items.length ? '<ul class="list">' + items.join("") + '</ul>' : ""; }

  /* ---------------- HOME ---------------- */
  function homeView() {
    tabs("home"); appbar("Insula Neuro Score", { brand: true });
    var q = route.q.q || "";
    var html = '<div class="narrow"><div class="search" role="search">' + I.search +
      '<label class="vh" for="q">Search scores</label><input id="q" type="search" placeholder="Search scores, e.g. GCS, Fisher, sedation" autocomplete="off" value="' + esc(q) + '"></div>' +
      '<div id="results"></div><div id="homebody">' + homeBody() + '</div></div>';
    show(html);
    if (q) runSearch(q);
  }
  function homeBody() {
    var h = "";
    var pinned = P.pinned.map(entry).filter(Boolean);
    h += '<div class="sec-row"><h2 class="sec">' + (pinned.length ? "Priority scores" : "Common scores") + '</h2>' + (pinned.length ? '<a href="#/settings" data-nav>Reorder</a>' : "") + '</div>';
    if (!pinned.length) h += '<p class="hint">Pin scores with the star to keep them here, in your own order.</p>';
    h += list((pinned.length ? pinned : COMMON.map(entry).filter(Boolean)).map(function (s) { return scoreRow(s, "calc", { both: true }); }));

    var groups = cats().filter(function (c) { return P.homeGroups.indexOf(c.id) >= 0 && P.hiddenGroups.indexOf(c.id) < 0 && c.scores.length; });
    if (groups.length) {
      h += '<h2 class="sec">Score groups</h2><div class="chips">' + groups.map(function (c) {
        return '<a class="chip" href="#/calc?group=' + c.id + '" data-nav>' + esc(c.name) + ' <span class="n">' + c.scores.length + '</span></a>'; }).join("") + '</div>';
    }
    var rc = P.recentCalc.map(entry).filter(Boolean).slice(0, 5);
    if (rc.length) h += '<h2 class="sec">Recent calculators</h2>' + list(rc.map(function (s) { return scoreRow(s, "calc"); }));
    var rg = P.recentGuide.map(entry).filter(Boolean).slice(0, 5);
    if (rg.length) h += '<h2 class="sec">Recently viewed guides</h2>' + list(rg.map(function (s) { return scoreRow(s, "guide"); }));
    var fg = P.favGuides.map(entry).filter(Boolean);
    if (fg.length) h += '<h2 class="sec">Saved guides</h2>' + list(fg.map(function (s) { return scoreRow(s, "guide"); }));
    h += '<p class="disclaim">A clinical calculation and reference tool. It does not diagnose or recommend treatment. Interpret every result in clinical context and according to local protocol.</p>';
    return h;
  }
  function runSearch(q) {
    var r = document.getElementById("results"), body = document.getElementById("homebody") || document.getElementById("listbody");
    if (!r) return;
    if (!q.trim()) { r.innerHTML = ""; if (body) body.hidden = false; return; }
    var hits = search(q);
    if (body) body.hidden = true;
    r.innerHTML = '<h2 class="sec">' + hits.length + ' result' + (hits.length === 1 ? "" : "s") + '</h2>' +
      (hits.length ? list(hits.map(function (s) { return scoreRow(s, route.section === "guide" ? "guide" : "calc", { both: route.section === "home", cat: true }); }))
                   : '<p class="empty">No score matches “' + esc(q) + '”. Try an abbreviation (GCS, WFNS) or a topic (sedation, vasospasm).</p>');
    $live.textContent = hits.length + " results";
  }

  /* ---------------- LISTS (Calculate / Guide) ---------------- */
  function listView(mode) {
    tabs(mode); appbar(mode === "calc" ? "Calculate" : "Guide");
    var only = route.q.group;
    var groups = cats().filter(function (c) { return c.scores.length && (only ? c.id === only : P.hiddenGroups.indexOf(c.id) < 0); });
    var h = '<div class="narrow"><div class="search" role="search">' + I.search + '<label class="vh" for="q">Search scores</label><input id="q" type="search" placeholder="Search ' + (mode === "calc" ? "calculators" : "guides") + '" autocomplete="off"></div><div id="results"></div><div id="listbody">';
    if (only) h += '<p class="hint" style="margin-top:1rem">Showing one group. <a href="#/' + mode + '" data-nav>Show all groups</a></p>';
    groups.forEach(function (c) { h += '<h2 class="sec">' + esc(c.name) + '</h2>' + list(c.scores.map(function (s) { return scoreRow(s, mode, { star: mode === "calc" }); })); });
    var hiddenN = P.hiddenGroups.filter(function (id) { return cats().some(function (c) { return c.id === id && c.scores.length; }); }).length;
    if (!only && hiddenN) h += '<p class="hint" style="margin-top:1rem">' + hiddenN + ' hidden group' + (hiddenN > 1 ? "s" : "") + '. <a href="#/settings" data-nav>Manage groups</a></p>';
    var planned = cats().filter(function (c) { return !c.scores.length; }).map(function (c) { return c.name; });
    if (!only && planned.length) h += '<p class="disclaim">Scores for ' + esc(planned.join(", ")) + ' are being verified for later releases. Scores are added only after their criteria, version and licensing are confirmed.</p>';
    show(h + '</div></div>');
  }

  /* ---------------- SCORE (Calculator / Guide) ---------------- */
  function scoreView(mode, id) {
    tabs(mode);
    var e = M && entry(id);
    appbar(e ? e.abbreviation : "", { back: true });
    $main.innerHTML = "";
    loadScore(id).then(function (s) {
      if (route.id !== id || route.section !== mode) return;
      if (mode === "calc") { P.recentCalc = uniqPush(P.recentCalc, id); save(); calcView(s); }
      else { P.recentGuide = uniqPush(P.recentGuide, id); save(); guideView(s); }
    }).catch(function (err) {
      show('<div class="errorbox" role="alert"><b>This score could not be loaded.</b><p>' + esc(err.message) + '</p></div>');
    });
  }
  function head(s) {
    return '<div class="score-head"><p class="abbr">' + esc(s.abbreviation) + '</p><p class="full">' + esc(s.name) + '</p>' +
      '<div class="meta"><span class="badge">' + esc(s.version.label) + '</span><span>' + esc(catName(s.category)) + '</span><span>Range ' + esc(s.range || "") + '</span></div></div>';
  }

  /* ----- calculator ----- */
  function calcView(s) {
    var a = answers[s.id] || (answers[s.id] = {});
    var pinned = P.pinned.indexOf(s.id) >= 0;
    var h = '<div class="calc-grid"><div class="inputs-col">' + head(s) +
      '<div class="actions">' +
        '<a class="btn" href="#/guide/' + s.id + '" data-nav>' + I.guide + 'Open guide</a>' +
        '<button class="btn star" data-act="pin" data-id="' + s.id + '" aria-pressed="' + pinned + '">' + I.star + '<span>' + (pinned ? "Pinned" : "Pin to Home") + '</span></button>' +
        '<button class="btn" data-act="reset">' + I.reset + 'Reset</button></div>' +
      '<p class="hint" style="margin-top:.75rem">' + esc(s.purpose) + '</p>' +
      '<form id="calcform" onsubmit="return false">' + s.inputs.map(function (inp) { return inputHTML(inp, a[inp.id]); }).join("") + '</form></div>' +
      '<div class="result-col"><section class="result" id="result" aria-labelledby="result-h"><h2 class="vh" id="result-h">Result</h2><div id="resultbody"></div></section></div></div>';
    show(h);
    var bar = document.createElement("button");
    bar.className = "sticky-result"; bar.setAttribute("data-act", "toresult"); bar.setAttribute("aria-label", "Jump to full result");
    document.body.appendChild(bar); document.body.classList.add("has-bar");
    updateResult(s);
  }
  function inputHTML(inp, val) {
    var help = inp.help ? '<p class="f-help">' + esc(inp.help) + '</p>' : "";
    if (inp.type === "choice") {
      return '<fieldset><legend>' + esc(inp.label) + '</legend>' + help + '<div class="opts" role="radiogroup">' +
        inp.options.map(function (o, i) {
          var checked = val != null && String(val) === String(o.value);
          var tag = o.nt ? "NT" : (o.code != null ? o.code : o.points);
          return '<label class="opt' + (checked ? " checked" : "") + (o.nt ? " is-nt" : "") + '"><input type="radio" name="' + esc(inp.id) + '" value="' + esc(o.value) + '"' + (checked ? " checked" : "") + '><span class="radio"></span>' +
            '<span class="opt-body"><span class="opt-label">' + esc(o.label) + '</span>' + (o.detail ? '<br><span class="opt-detail">' + esc(o.detail) + '</span>' : "") + '</span>' +
            '<span class="opt-pts" aria-label="' + (o.nt ? "not testable" : "scores " + esc(tag)) + '">' + esc(tag) + '</span></label>';
        }).join("") + '</div></fieldset>';
    }
    if (inp.type === "number") {
      return '<fieldset><legend><label for="n-' + esc(inp.id) + '">' + esc(inp.label) + '</label></legend>' + help +
        '<div class="num"><button type="button" data-act="step" data-id="' + esc(inp.id) + '" data-d="-1" aria-label="Decrease ' + esc(inp.short || inp.label) + '">−</button>' +
        '<input id="n-' + esc(inp.id) + '" name="' + esc(inp.id) + '" type="number" inputmode="numeric" min="' + inp.min + '" max="' + inp.max + '" step="1" value="' + (val == null ? "" : esc(val)) + '" aria-describedby="r-' + esc(inp.id) + '">' +
        '<button type="button" data-act="step" data-id="' + esc(inp.id) + '" data-d="1" aria-label="Increase ' + esc(inp.short || inp.label) + '">+</button>' +
        '<span class="range" id="r-' + esc(inp.id) + '">' + inp.min + '–' + inp.max + (inp.unit ? " " + esc(inp.unit) : "") + '</span></div>' +
        '<p class="f-error" id="e-' + esc(inp.id) + '" role="alert"></p>' +
        (inp.link ? '<a class="f-link" href="#/calc/' + esc(inp.link) + '" data-nav>Calculate ' + esc(entry(inp.link) ? entry(inp.link).abbreviation : inp.link) + ' first</a>' : "") + '</fieldset>';
    }
    return "";
  }
  var lastResult = null;
  function updateResult(s) {
    var a = answers[s.id] || {};
    var r = E.calculate(s, a); lastResult = { s: s, r: r };
    var st = r.state.state;
    var isText = /[A-Za-z]/.test(r.display) && r.display.length > 6;
    var h = '<div class="state st-' + st + '"><div class="state-top">' + SI[st] + '<span>' + esc(STATE_NAME[st]) + '</span></div>' +
      '<div class="state-value' + (isText ? " small" : "") + '">' + esc(r.display) + '</div>' +
      '<div class="state-range">' + esc(s.abbreviation) + (s.range ? ", range " + esc(s.range) : "") + '</div>' +
      (showLabel(r) ? '<p class="state-label">' + esc(r.state.label) + '</p>' : "") +
      '<p class="state-summary">' + esc(r.state.summary || "") + '</p>' +
      (r.state.detail ? '<p class="state-detail">' + esc(r.state.detail) + '</p>' : "") + '</div>';

    // breakdown
    h += '<div class="rblock"><h3>Components</h3><table class="bd"><tbody>' + r.breakdown.map(function (b) {
      return '<tr><th scope="row">' + esc(b.short) + '</th>' + (b.missing ? '<td class="miss">Not entered</td><td class="p">–</td>' :
        '<td>' + esc(b.choice) + '</td><td class="p">' + esc(b.nt ? "NT" : (b.code != null ? b.code : b.points)) + '</td>') + '</tr>';
    }).join("") + '<tr class="tot"><th scope="row">Result</th><td>' + esc(r.state.label || "") + '</td><td class="p">' + esc(r.display) + '</td></tr></tbody></table></div>';

    if (r.insights.length) h += '<div class="rblock"><h3>Clinical insight</h3><ul class="notes">' + r.insights.map(function (i) { return '<li>' + esc(i.text) + '</li>'; }).join("") + '</ul></div>';
    if (st !== "incomplete" || r.nt.length) h += '<div class="rblock"><h3>Key limitations</h3><ul class="notes warn">' + s.limitations.slice(0, 3).map(function (l) { return '<li>' + esc(l) + '</li>'; }).join("") + '</ul></div>';
    var canShare = st !== "incomplete" || r.share;
    h += '<div class="actions"><button class="btn" data-act="copy"' + (canShare ? "" : " disabled") + '>' + I.copy + 'Copy result</button><button class="btn" data-act="share"' + (canShare ? "" : " disabled") + '>' + I.share + 'Share</button></div>' +
      '<a class="btn block" href="#/guide/' + s.id + '" data-nav>' + I.guide + 'Open guide: interpretation, limitations, sources</a>' +
      '<p class="disclaim">' + esc(s.version.label) + ' · content ' + esc(s.contentVersion) + '. Supports, and does not replace, clinical judgement.</p>';
    document.getElementById("resultbody").innerHTML = h;

    var bar = document.querySelector(".sticky-result");
    if (bar) {
      bar.className = "sticky-result st-" + st;
      bar.innerHTML = SI[st] + '<span class="sv">' + esc(r.display) + '</span><span class="sl">' + esc(st === "incomplete" ? (r.missing.length ? r.missing.length + " to complete" : r.state.label) : (String(r.display).indexOf(r.state.label) >= 0 || String(r.state.label).indexOf(r.display) >= 0 ? STATE_NAME[st] : r.state.label)) + '</span>' + I.down;
    }
    $live.textContent = st === "incomplete" ? "" : s.abbreviation + " " + r.display + ", " + (r.state.label || "");
  }
  function showLabel(r) {
    var l = (r.state.label || "").toLowerCase(), d = String(r.display).toLowerCase(), sm = (r.state.summary || "").toLowerCase();
    if (!l || l === "incomplete" || l === "calculated") return false;
    if (d.indexOf(l) >= 0 || l.indexOf(d) >= 0) return false;
    return sm.split(" ")[0] !== l.split(" ")[0];
  }
  function shareText() {
    if (!lastResult) return "";
    var s = lastResult.s, r = lastResult.r;
    var line = r.share || (s.abbreviation + " " + r.display);
    var comps = r.breakdown.filter(function (b) { return !b.missing; }).map(function (b) { return b.short + ": " + b.choice + " (" + (b.nt ? "NT" : (b.code != null ? b.code : b.points)) + ")"; }).join("; ");
    return line + "\n" + comps + "\n" + s.version.label + ". Calculated with Insula Neuro Score; interpret in clinical context.";
  }

  /* ----- guide ----- */
  function guideView(s) {
    var g = s.guide || {}, saved = P.favGuides.indexOf(s.id) >= 0;
    var secs = [
      ["what", "What is this score?", '<p>' + esc(g.what) + '</p>'],
      ["purpose", "Purpose", '<p>' + esc(s.purpose) + '</p>'],
      ["population", "Intended population", '<p>' + esc(s.intendedPopulation) + '</p>'],
      ["when", "When it is useful", '<p>' + esc(g.whenUseful) + '</p>'],
      ["components", "Components", s.inputs.map(function (inp) {
        var body = inp.type === "choice" ? '<table class="bd"><tbody>' + inp.options.map(function (o) {
          return '<tr><td>' + esc(o.label) + (o.detail ? '<br><span class="opt-detail">' + esc(o.detail) + '</span>' : "") + '</td><td class="p">' + esc(o.nt ? "NT" : (o.code != null ? o.code : o.points)) + '</td></tr>'; }).join("") + '</tbody></table>'
          : '<p>Whole number from ' + inp.min + ' to ' + inp.max + (inp.unit ? " " + esc(inp.unit) : "") + '.</p>';
        return '<div class="comp"><h4>' + esc(inp.label) + '</h4>' + (inp.help ? '<p class="f-help">' + esc(inp.help) + '</p>' : "") + body + '</div>';
      }).join("")],
      ["how", "How to calculate", '<p>' + esc(g.howToCalculate) + '</p>'],
      ["interp", "Interpretation", '<table class="bd"><tbody>' + s.states.map(function (st) {
        return '<tr class="st-' + st.state + '"><th scope="row" style="color:var(--sc)">' + SI[st.state] + ' ' + esc(st.range || "") + '</th><td><b>' + esc(st.label) + '.</b> ' + esc(st.summary) + '</td></tr>'; }).join("") + '</tbody></table>'
        + (s.notTestable ? '<p class="hint" style="margin-top:.5rem"><b>' + esc(s.notTestable.label) + ':</b> ' + esc(s.notTestable.summary) + '</p>' : "")],
      ["context", "Clinical context", '<p>' + esc(g.clinicalContext) + '</p>' + (s.insights.length ? '<ul class="notes">' + s.insights.map(function (i) { return '<li>' + esc(i.text) + '</li>'; }).join("") + '</ul>' : "")],
      ["limits", "Important limitations", bullets(s.limitations)],
      ["confounders", "Confounders and factors affecting scoring", bullets(s.confounders)],
      ["errors", "Common calculation mistakes", bullets(s.commonErrors)],
      ["not", "What the score does not tell you", bullets(s.doesNotTellYou)],
      ["related", "Related scores", '<div class="related">' + s.related.map(function (rid) { var e = entry(rid); return e ? '<a class="chip" href="#/guide/' + rid + '" data-nav>' + esc(e.abbreviation) + '</a>' : ""; }).join("") + '</div>'],
      ["version", "Version and classification", '<dl class="vinfo"><dt>Version</dt><dd>' + esc(s.version.label) + '</dd><dt>Details</dt><dd>' + esc(s.version.detail) + '</dd>' +
        '<dt>Content</dt><dd>v' + esc(s.contentVersion) + '</dd><dt>Last reviewed</dt><dd>' + esc(s.lastReviewed) + '</dd><dt>Review status</dt><dd>' + esc(s.reviewStatus) + '</dd>' +
        '<dt>Licensing</dt><dd>' + esc(s.licensing.status) + '. ' + esc(s.licensing.note) + '</dd></dl>'],
      ["sources", "Evidence and sources", '<ol class="src">' + s.sources.map(function (src) {
        var link = src.doi ? "https://doi.org/" + src.doi : src.url;
        return '<li>' + esc(src.citation) + (link ? ' <a href="' + esc(link) + '" data-ext>' + esc(src.doi ? "doi:" + src.doi : "Website") + '</a>' : "") + '</li>'; }).join("") + '</ol>']
    ];
    var h = '<div class="narrow">' + head(s) +
      '<div class="guide-cta"><a class="btn primary block" href="#/calc/' + s.id + '" data-nav>' + I.calc + 'Calculate this score →</a></div>' +
      '<div class="actions" style="margin-top:.5rem"><button class="btn star" data-act="saveguide" data-id="' + s.id + '" aria-pressed="' + saved + '">' + I.star + '<span>' + (saved ? "Saved to Home" : "Save guide") + '</span></button></div>' +
      '<p class="review-flag">' + I.flag + '<span>' + esc(s.reviewStatus) + '</span></p>' +
      '<nav class="toc" aria-label="Guide sections">' + secs.map(function (x) { return '<a href="#" data-jump="g-' + x[0] + '">' + esc(x[1].replace(" and factors affecting scoring", "").replace("What the score does not tell you", "Does not tell you")) + '</a>'; }).join("") + '</nav>' +
      secs.map(function (x) { return '<section class="gsec" id="g-' + x[0] + '"><h3>' + esc(x[1]) + '</h3>' + x[2] + '</section>'; }).join("") +
      '<div class="guide-cta" style="margin-top:2rem"><a class="btn primary block" href="#/calc/' + s.id + '" data-nav>' + I.calc + 'Calculate this score →</a></div></div>';
    show(h);
  }
  function bullets(arr) { return arr && arr.length ? '<ul class="notes warn">' + arr.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join("") + '</ul>' : '<p class="hint">None listed.</p>'; }

  /* ---------------- SETTINGS ---------------- */
  function settingsView() {
    tabs(""); appbar("Settings", { back: true, settings: false });
    var seg = function (key, opts) { return '<div class="seg" role="group">' + opts.map(function (o) { return '<button data-act="pref" data-k="' + key + '" data-v="' + o[0] + '" aria-pressed="' + (P[key] === o[0]) + '">' + o[1] + '</button>'; }).join("") + '</div>'; };
    var pinned = P.pinned.map(entry).filter(Boolean);
    var groups = cats().filter(function (c) { return c.scores.length; });
    var h = '<div class="narrow">' +
      '<h2 class="sec">Appearance</h2>' + seg("theme", [["system", "System"], ["light", "Light"], ["dark", "Dark"]]) +
      '<ul class="list" style="margin-top:.75rem"><li class="set-row"><span class="row-main"><span class="row-title">High contrast</span><span class="row-sub">Stronger borders and text</span></span>' +
      '<label class="switch"><input type="checkbox" data-act="contrast" aria-label="High contrast"' + (P.highContrast ? " checked" : "") + '><span></span></label></li></ul>' +
      '<p class="hint">Text size follows your device font size setting.</p>' +
      '<h2 class="sec">Startup screen</h2>' + seg("startup", [["home", "Home"], ["calc", "Calculate"], ["guide", "Guide"]]) +
      '<h2 class="sec">Priority scores on Home</h2>' +
      (pinned.length ? '<ul class="list">' + pinned.map(function (s, i) {
        return '<li class="set-row"><span class="row-main"><span class="row-title">' + esc(s.abbreviation) + '</span><span class="row-sub">' + esc(s.name) + '</span></span>' +
          '<span class="reorder"><button data-act="mv" data-list="pinned" data-i="' + i + '" data-d="-1" aria-label="Move ' + esc(s.abbreviation) + ' up"' + (i === 0 ? " disabled" : "") + '>' + I.up + '</button>' +
          '<button data-act="mv" data-list="pinned" data-i="' + i + '" data-d="1" aria-label="Move ' + esc(s.abbreviation) + ' down"' + (i === pinned.length - 1 ? " disabled" : "") + '>' + I.down + '</button>' +
          '<button data-act="pin" data-id="' + s.id + '" aria-label="Remove ' + esc(s.abbreviation) + ' from Home">' + I.x + '</button></span></li>'; }).join("") + '</ul>'
        : '<p class="empty">No pinned scores yet. Use the star on any calculator to pin it.</p>') +
      '<h2 class="sec">Score groups</h2><p class="hint">Order applies to the Calculate and Guide lists. “On Home” shows the group as a shortcut; “Hidden” removes it from the lists.</p>' +
      '<ul class="list">' + groups.map(function (c, i) {
        return '<li><div class="set-row"><span class="row-main"><span class="row-title">' + esc(c.name) + '</span><span class="row-sub">' + c.scores.length + ' score' + (c.scores.length > 1 ? "s" : "") + '</span></span>' +
          '<span class="reorder"><button data-act="mvg" data-id="' + c.id + '" data-d="-1" aria-label="Move ' + esc(c.name) + ' up"' + (i === 0 ? " disabled" : "") + '>' + I.up + '</button>' +
          '<button data-act="mvg" data-id="' + c.id + '" data-d="1" aria-label="Move ' + esc(c.name) + ' down"' + (i === groups.length - 1 ? " disabled" : "") + '>' + I.down + '</button></span></div>' +
          '<div class="grp-toggles"><label><input type="checkbox" data-act="ghome" data-id="' + c.id + '"' + (P.homeGroups.indexOf(c.id) >= 0 ? " checked" : "") + '> On Home</label>' +
          '<label><input type="checkbox" data-act="ghide" data-id="' + c.id + '"' + (P.hiddenGroups.indexOf(c.id) >= 0 ? " checked" : "") + '> Hidden</label></div></li>'; }).join("") + '</ul>' +
      '<h2 class="sec">Data</h2><button class="btn block" data-act="clearrecent">Clear recent items</button>' +
      '<div style="height:.5rem"></div><button class="btn block" data-act="resetprefs">Reset all preferences</button>' +
      '<h2 class="sec">About</h2><p>Insula Neuro Score · Insula Neurosciences<br>App 0.1.0 (Phase 1) · Content v' + esc(M.contentVersion) + ' · ' + M.scores.length + ' scores</p>' +
      '<p class="hint">A clinical calculation tool and reference guide. It does not diagnose, and it does not make treatment decisions. Scores are implemented from their published sources in original wording; official worksheets are not reproduced. Content is pending independent clinician review.</p>' +
      '<p class="hint">All calculations, search, guides and settings work offline. Preferences are stored only on this device.</p></div>';
    show(h);
  }
  function moveIn(arr, i, d) { var j = i + d; if (j < 0 || j >= arr.length) return arr; var c = arr.slice(); var t = c[i]; c[i] = c[j]; c[j] = t; return c; }

  /* ---------------- events ---------------- */
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a");
    if (a && a.hasAttribute("data-ext")) { ev.preventDefault(); try { if (A) A.openUrl(a.href); else window.open(a.href, "_blank"); } catch (e) {} return; }
    if (a && a.hasAttribute("data-jump")) { ev.preventDefault(); var t = document.getElementById(a.getAttribute("data-jump")); if (t) { t.scrollIntoView(); t.querySelector("h3").setAttribute("tabindex", "-1"); t.querySelector("h3").focus({ preventScroll: true }); } return; }
    if (a && a.hasAttribute("data-nav")) { ev.preventDefault(); var href = a.getAttribute("href"); if (href !== location.hash) go(href); return; }
    var b = ev.target.closest("[data-act]"); if (!b || b.tagName === "INPUT") return;
    var act = b.getAttribute("data-act"), id = b.getAttribute("data-id");
    if (act === "back") { if (!window.handleBack()) location.hash = "#/home"; return; }
    if (act === "pin") {
      var on = P.pinned.indexOf(id) >= 0;
      P.pinned = on ? P.pinned.filter(function (x) { return x !== id; }) : P.pinned.concat([id]); save();
      toast(on ? "Removed from Home" : "Pinned to Home");
      if (route.section === "settings") return settingsView();
      document.querySelectorAll('[data-act="pin"][data-id="' + id + '"]').forEach(function (el) {
        el.setAttribute("aria-pressed", String(!on));
        var sp = el.querySelector("span"); if (sp) sp.textContent = !on ? "Pinned" : "Pin to Home";
      });
      return;
    }
    if (act === "saveguide") {
      var on2 = P.favGuides.indexOf(id) >= 0;
      P.favGuides = on2 ? P.favGuides.filter(function (x) { return x !== id; }) : P.favGuides.concat([id]); save();
      b.setAttribute("aria-pressed", String(!on2)); b.querySelector("span").textContent = on2 ? "Save guide" : "Saved to Home";
      toast(on2 ? "Guide removed from Home" : "Guide saved to Home"); return;
    }
    if (act === "reset" && lastResult) {
      answers[lastResult.s.id] = {}; calcView(lastResult.s); toast("Inputs cleared"); return;
    }
    if (act === "step" && lastResult) {
      var s = lastResult.s, inp = s.inputs.filter(function (x) { return x.id === id; })[0], el = document.getElementById("n-" + id);
      var cur = el.value === "" ? (b.getAttribute("data-d") === "1" ? inp.min - 1 : inp.max + 1) : Number(el.value);
      var nv = Math.max(inp.min, Math.min(inp.max, Math.round(cur) + Number(b.getAttribute("data-d"))));
      el.value = nv; answers[s.id][id] = String(nv); document.getElementById("e-" + id).textContent = ""; updateResult(s); return;
    }
    if (act === "toresult") { var r = document.getElementById("result"); if (r) r.scrollIntoView(); return; }
    if (act === "copy") { var txt = shareText(); try { if (A) A.copy(txt); else navigator.clipboard.writeText(txt); toast("Result copied"); } catch (e) { toast("Copy failed"); } return; }
    if (act === "share") { var tx = shareText(); try { if (A) A.share(tx); else if (navigator.share) navigator.share({ text: tx }); else { navigator.clipboard.writeText(tx); toast("Result copied"); } } catch (e) {} return; }
    if (act === "pref") { P[b.getAttribute("data-k")] = b.getAttribute("data-v"); save(); applyTheme(); settingsView(); return; }
    if (act === "mv") { var k = b.getAttribute("data-list"); P[k] = moveIn(P[k], Number(b.getAttribute("data-i")), Number(b.getAttribute("data-d"))); save(); settingsView(); focusAfter(b); return; }
    if (act === "mvg") {
      var order = cats().map(function (c) { return c.id; }), i = order.indexOf(id), d = Number(b.getAttribute("data-d"));
      var withScores = cats().filter(function (c) { return c.scores.length; }).map(function (c) { return c.id; });
      var j = withScores.indexOf(id) + d; if (j < 0 || j >= withScores.length) return;
      var target = withScores[j], ti = order.indexOf(target); order[i] = target; order[ti] = id;
      P.groupOrder = order; save(); settingsView(); focusAfter(b); return;
    }
    if (act === "clearrecent") { P.recentCalc = []; P.recentGuide = []; save(); toast("Recent items cleared"); return; }
    if (act === "resetprefs") { if (confirm("Reset theme, startup screen, pinned scores, saved guides and group settings?")) { P = Object.assign({}, DEFAULTS); save(); applyTheme(); settingsView(); toast("Preferences reset"); } return; }
  });
  function focusAfter(btn) {
    var sel = '[data-act="' + btn.getAttribute("data-act") + '"][data-d="' + btn.getAttribute("data-d") + '"]' + (btn.getAttribute("data-id") ? '[data-id="' + btn.getAttribute("data-id") + '"]' : "");
    var el = document.querySelector(sel); if (el && !el.disabled) el.focus();
  }
  document.addEventListener("change", function (ev) {
    var t = ev.target;
    if (t.type === "radio" && lastResult && route.section === "calc") {
      answers[lastResult.s.id][t.name] = t.value;
      t.closest(".opts").querySelectorAll(".opt").forEach(function (o) { o.classList.toggle("checked", o.querySelector("input").checked); });
      updateResult(lastResult.s); return;
    }
    if (t.getAttribute("data-act") === "contrast") { P.highContrast = t.checked; save(); applyTheme(); return; }
    if (t.getAttribute("data-act") === "ghome") { var id = t.getAttribute("data-id"); P.homeGroups = t.checked ? P.homeGroups.concat([id]) : P.homeGroups.filter(function (x) { return x !== id; }); save(); return; }
    if (t.getAttribute("data-act") === "ghide") { var id2 = t.getAttribute("data-id"); P.hiddenGroups = t.checked ? P.hiddenGroups.concat([id2]) : P.hiddenGroups.filter(function (x) { return x !== id2; }); save(); return; }
  });
  document.addEventListener("input", function (ev) {
    var t = ev.target;
    if (t.id === "q") { runSearch(t.value); return; }
    if (t.type === "number" && lastResult && route.section === "calc") {
      var s = lastResult.s, inp = s.inputs.filter(function (x) { return x.id === t.name; })[0];
      answers[s.id][t.name] = t.value;
      var v = t.value === "" ? null : Number(t.value), err = document.getElementById("e-" + t.name);
      err.textContent = v == null ? "" : (isNaN(v) || v % 1 !== 0 || v < inp.min || v > inp.max) ? "Enter a whole number from " + inp.min + " to " + inp.max + "." : "";
      updateResult(s);
    }
  });

  /* ---------------- boot ---------------- */
  applyTheme();
  loadManifest().then(function () {
    if (!location.hash || location.hash === "#" || location.hash === "#/") location.replace("#/" + (P.startup || "home"));
    render();
  }).catch(function (e) {
    $main.innerHTML = '<div class="errorbox" role="alert"><b>Content could not be loaded.</b><p>' + esc(e.message) + '</p></div>';
  });
})();
