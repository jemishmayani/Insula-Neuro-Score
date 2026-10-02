/* =========================================================================
   Insula Neuro Score — App shell (Phase 1)
   Screens: Home · Calculate · Guide · Score detail (Calculate/Guide) · Settings
   No calculator logic, no network, no patient data.
   ========================================================================= */
(function () {
  "use strict";
  var UI = window.UI, Store = window.Store, esc = UI.esc;
  var Android = window.Android || null;
  var root = document.getElementById("app"), live = document.getElementById("live");
  var CATALOG = null, SCORE_CACHE = {}, SESSION_ANSWERS = {};   // answers live only in memory (no patient data persisted)
  function loadJSON(path) {
    return fetch(path, { cache: "no-store" }).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
  }
  var SCORE_CACHE_MAX = 12, SCORE_CACHE_ORDER = [];
  function cacheScore(id, sc) {
    SCORE_CACHE[id] = sc; SCORE_CACHE_ORDER = [id].concat(SCORE_CACHE_ORDER.filter(function (x) { return x !== id; }));
    while (SCORE_CACHE_ORDER.length > SCORE_CACHE_MAX) delete SCORE_CACHE[SCORE_CACHE_ORDER.pop()];
  }
  window.__insDebug = { cacheSize: function () { return Object.keys(SCORE_CACHE).length; } };
  function loadScore(id) {
    if (SCORE_CACHE[id]) { cacheScore(id, SCORE_CACHE[id]); return Promise.resolve(SCORE_CACHE[id]); }
    return loadJSON("content/scores/" + encodeURIComponent(id) + ".json").then(function (sc) {
      var errs = window.InsulaEngine.engine.validateScore(sc);
      if (errs.length) throw new Error("Score content failed validation: " + errs.slice(0, 3).join("; "));
      cacheScore(id, sc); return sc;
    });
  }
  function scoreLinks(tabDefault) {
    return function (id, tab) {
      var s = score(id); if (!s) return null;
      return { href: "#/" + (tab || tabDefault) + "/s/" + id, label: s.abbreviation };
    };
  }
  var TABS = [
    { id: "home", label: "Home", icon: "home", href: "#/home" },
    { id: "calculate", label: "Calculate", icon: "calculate", href: "#/calculate" },
    { id: "guide", label: "Guide", icon: "guide", href: "#/guide" }
  ];
  var GUIDE_SECTIONS = ["What is this score?", "Purpose", "Intended population", "When it is useful", "Components", "How to calculate",
    "Interpretation", "Clinical context", "Important limitations", "Confounders / factors affecting scoring", "Common calculation mistakes",
    "What the score does NOT tell you", "Related scores", "Version / classification information", "Evidence / sources"];
  var HOME_SECTION_META = {
    favorites: { title: "Favorite scores", kind: "score", emptyTitle: "No favorite scores yet.", empty: "Add a score to Favorites for one-tap access.", icon: "star",
                 action: { label: "Browse calculators", href: "#/calculate", icon: "calculate" }, editable: true, picker: "favorites" },
    favoriteGuides: { title: "Favorite guides", kind: "guide", emptyTitle: "No favorite guides yet.", empty: "Save a guide to Favorites to reopen it in one tap.", icon: "guide",
                 action: { label: "Browse guides", href: "#/guide", icon: "guide" }, editable: true, picker: "favoriteGuides" },
    recentCalc: { title: "Recently used calculators", kind: "score", emptyTitle: "No recent calculations.", empty: "Scores you calculate appear here. Only the score and time are kept on this device, never your inputs.", icon: "clock", recent: true },
    recentGuide: { title: "Recently viewed guides", kind: "guide", emptyTitle: "No recently viewed guides.", empty: "Guides you open appear here.", icon: "clock", recent: true },
    priorityScores: { title: "Priority scores", kind: "score", emptyTitle: "No priority scores yet.", empty: "Promote the scores you use most so they appear on Home in your order.", icon: "pin",
                 action: { label: "Choose priority scores", href: "#/settings/pick/priorityScores", icon: "plus" }, editable: true, picker: "priorityScores" },
    priorityGroups: { title: "Priority groups", kind: "group", emptyTitle: "No priority groups yet.", empty: "Promote score groups to Home for quick access.", icon: "pin",
                 action: { label: "Choose priority groups", href: "#/settings/pick/priorityGroups", icon: "plus" }, editable: true, picker: "priorityGroups" }
  };
  var homeEdit = {};   // section id → edit mode on/off (session only)

  /* ---------------- catalogue helpers ---------------- */
  var IDX = null;   // built once per catalogue load; Home and search never touch score documents
  function buildIndex(cat) {
    var byId = {}, catById = {}, byCat = {}, search = [];
    cat.categories.forEach(function (c) { catById[c.id] = c; byCat[c.id] = []; });
    cat.scores.forEach(function (s) {
      byId[s.id] = s; (byCat[s.category] = byCat[s.category] || []).push(s);
      search.push({ s: s, a: s.abbreviation.toLowerCase(), n: s.name.toLowerCase(), m: (s.summary || "").toLowerCase(), al: (s.aliases || []).join(" ").toLowerCase(),
                    c: ((catById[s.category] || {}).name || "").toLowerCase() });
    });
    return { byId: byId, catById: catById, byCat: byCat, search: search };
  }
  function score(id) { return IDX.byId[id] || null; }
  function category(id) { return IDX.catById[id] || null; }
  function orderedCategories(includeHidden) {
    var st = Store.get(), order = st.groupOrder.slice();
    CATALOG.categories.forEach(function (c) { if (order.indexOf(c.id) < 0) order.push(c.id); });
    return order.map(category).filter(Boolean).filter(function (c) { return includeHidden || st.hiddenGroups.indexOf(c.id) < 0; });
  }
  function scoresIn(catId) { return IDX.byCat[catId] || []; }
  function search(q, limit) {
    q = q.trim().toLowerCase(); if (!q) return [];
    var hidden = {}; Store.get().hiddenGroups.forEach(function (h) { hidden[h] = 1; });
    var out = [];
    for (var i = 0; i < IDX.search.length; i++) {
      var e = IDX.search[i], r = 99;
      if (e.a === q) r = 0; else if (e.a.indexOf(q) === 0) r = 1; else if (e.n.indexOf(q) === 0) r = 2;
      else if (e.a.indexOf(q) >= 0 || e.n.indexOf(q) >= 0) r = 3; else if (e.al.indexOf(q) >= 0) r = 4; else if (e.m.indexOf(q) >= 0) r = 5; else if (e.c.indexOf(q) >= 0) r = 6;
      if (r < 99) out.push({ s: e.s, r: r + (hidden[e.s.category] ? 10 : 0) });
    }
    out.sort(function (x, y) { return x.r - y.r || (x.s.abbreviation < y.s.abbreviation ? -1 : 1); });
    return out.slice(0, limit || 50).map(function (x) { return x.s; });
  }
  function relTime(at) {
    if (!at) return "";
    var d = (Date.now() - at) / 1000;
    if (d < 60) return "just now"; if (d < 3600) return Math.floor(d / 60) + " min ago"; if (d < 86400) return Math.floor(d / 3600) + " h ago";
    if (d < 172800) return "yesterday"; return new Date(at).toLocaleDateString(undefined, { day: "numeric", month: "short" });
  }
  var placeholderBadge = function () { return UI.StatusBadge({ tone: "neutral", label: "Placeholder", icon: false }); };
  function badgeFor(s) { return s.status === "implemented" ? UI.StatusBadge({ tone: "primary", label: "Calculator", icon: false }) : placeholderBadge(); }
  function sub(s) { return s.name === s.abbreviation ? s.summary : s.name; }

  /* ---------------- theme ---------------- */
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  function applyTheme() {
    var st = Store.get(), dark = st.theme === "dark" || (st.theme === "system" && !!(mq && mq.matches));
    var el = document.documentElement;
    el.setAttribute("data-theme", dark ? "dark" : "light");
    if (st.highContrast) el.setAttribute("data-contrast", "high"); else el.removeAttribute("data-contrast");
    try { if (Android && Android.setSystemBars) Android.setSystemBars(dark); } catch (e) {}
  }
  if (mq) { var onMq = function () { if (Store.get().theme === "system") applyTheme(); }; if (mq.addEventListener) mq.addEventListener("change", onMq); else if (mq.addListener) mq.addListener(onMq); }

  /* ---------------- router & back stack ---------------- */
  var depth = 0, scrollMemory = {}, goingBack = false, goingBackY = 0, route = {};
  function parse() {
    var h = (location.hash || "").replace(/^#\/?/, "");
    var p = h.split("/").filter(Boolean);
    return { tab: p[0] || "", kind: p[1] || null, id: p[2] ? decodeURIComponent(p[2]) : null, hash: "#/" + h };
  }
  function startHash() { return "#/" + Store.get().startup; }
  function navigate(hash) { if (hash === location.hash) return; scrollMemory[location.hash] = window.scrollY; depth++; location.hash = hash; }
  function replaceTo(hash) { scrollMemory[location.hash] = window.scrollY; location.replace(hash); }
  function parentOf(r) {
    if (r.tab === "calculate" || r.tab === "guide") {
      if (r.kind === "s") { var s = score(r.id); return "#/" + r.tab + (s ? "/c/" + s.category : ""); }
      if (r.kind === "c") return "#/" + r.tab;
    }
    if (r.tab === "settings" && r.kind) return "#/settings";
    var top = r.tab === "settings" ? null : "#/" + r.tab;
    if (r.tab === "settings" || top !== startHash()) return startHash();
    return null;
  }
  /** Called by the native back button. Returns true if handled in-app (false = let Android close). */
  window.handleBack = function () {
    if (depth > 0) { depth--; goingBack = true; history.back(); return true; }
    var p = parentOf(route); if (p) { goingBack = true; replaceTo(p); return true; }
    return false;
  };
  function hasInAppBack(r) { return depth > 0 || (!!r.kind) || r.tab === "settings"; }

  window.addEventListener("hashchange", render);

  /* ---------------- frame ---------------- */
  function frame(o) {
    var actions = (o.actions || []).concat(o.noSettings ? [] : [UI.IconButton({ icon: "settings", label: "Settings", href: "#/settings" })]);
    return UI.AppBar({ title: o.title, back: o.back, brand: o.brand, actions: actions }) +
      '<main id="main" class="content' + (o.wide ? " wide" : "") + '" tabindex="-1">' + o.body + "</main>" +
      UI.BottomNavigation({ active: o.tab, items: TABS });
  }
  function paint(html, opts) {
    var prevFocusAct = null;
    root.innerHTML = '<div class="shell">' + html + "</div>";
    document.title = (opts && opts.title ? opts.title + " · " : "") + "Insula Neuro Score";
    document.body.classList.remove("has-result-bar");
    var y = goingBack && scrollMemory[location.hash] != null ? scrollMemory[location.hash] : 0;
    goingBackY = goingBack ? y : 0;
    window.scrollTo(0, y);
    if (!goingBack && opts && opts.focusMain !== false) { var m = document.getElementById("main"); if (m) m.focus({ preventScroll: true }); }
    goingBack = false;
    return prevFocusAct;
  }
  function toast(msg, action) {
    document.querySelectorAll(".toast").forEach(function (t) { t.remove(); });
    var t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status");
    var span = document.createElement("span"); span.textContent = msg; t.appendChild(span);
    if (action) {
      var b = document.createElement("button"); b.type = "button"; b.className = "toast-action"; b.textContent = action.label;
      b.addEventListener("click", function () { t.remove(); action.run(); }); t.appendChild(b);
    }
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, action ? 6000 : 2200);
  }
  function announce(msg) { live.textContent = ""; setTimeout(function () { live.textContent = msg; }, 30); }

  function render() {
    document.querySelectorAll(".toast").forEach(function (t) { t.remove(); });
    route = parse();
    if (!CATALOG) return;
    var r = route;
    if (!r.tab) { location.replace(startHash()); return; }
    if (r.tab === "home" && !r.kind) return homeScreen();
    if ((r.tab === "calculate" || r.tab === "guide") && !r.kind) return rootListScreen(r.tab);
    if ((r.tab === "calculate" || r.tab === "guide") && r.kind === "c") return categoryScreen(r.tab, r.id);
    if ((r.tab === "calculate" || r.tab === "guide") && r.kind === "s") return detailScreen(r.tab, r.id);
    if (r.tab === "settings" && !r.kind) return settingsScreen();
    if (r.tab === "settings" && r.kind === "pick") return pickerScreen(r.id);
    if (r.tab === "settings" && r.kind === "gallery") return galleryScreen();
    notFound("This page does not exist.");
  }
  function notFound(msg) {
    paint(frame({ title: "Not found", tab: route.tab, back: true,
      body: UI.ErrorState({ title: "Page not found", message: msg, action: UI.PrimaryButton({ label: "Go to Home", href: "#/home", icon: "home" }) }) }));
  }

  /* ---------------- shared pieces ---------------- */
  function favKey(tab) { return tab === "guide" ? "favoriteGuides" : "favorites"; }
  function scoreCard(s, tab, opts) {
    opts = opts || {};
    var st = Store.get(), key = favKey(tab);
    return UI.ScoreCard({ score: s, href: "#/" + tab + "/s/" + s.id, sub: opts.withCategory ? sub(s) + " · " + category(s.category).name : sub(s),
      badge: badgeFor(s), favorite: opts.noStar ? null : st[key].indexOf(s.id) >= 0, favKey: key });
  }
  /** Home row: primary tap opens one view; a second button opens the other, so both are one tap away. */
  function homeRow(s, kind, o) {
    o = o || {};
    var primaryTab = kind === "guide" ? "guide" : "calculate", altTab = primaryTab === "guide" ? "calculate" : "guide";
    var meta = o.time ? '<span class="row-meta">' + esc(o.time) + "</span>" : "";
    var main = '<a class="open" href="#/' + primaryTab + "/s/" + s.id + '" data-nav><span class="row-icon" aria-hidden="true">' + UI.icon(primaryTab === "guide" ? "guide" : "calculate") + '</span><span class="text"><span class="title">' + esc(s.abbreviation) +
      (s.status !== "implemented" ? " " + placeholderBadge() : "") + '</span><span class="sub">' + esc(sub(s)) + "</span>" + meta + "</span></a>";
    var tail;
    if (o.edit) {
      tail = UI.IconButton({ icon: "up", label: "Move " + s.abbreviation + " up", act: "home-move", disabled: o.index === 0, data: { key: o.key, index: o.index, delta: -1 } }) +
        UI.IconButton({ icon: "down", label: "Move " + s.abbreviation + " down", act: "home-move", disabled: o.index === o.count - 1, data: { key: o.key, index: o.index, delta: 1 } }) +
        UI.IconButton({ icon: "close", label: "Remove " + s.abbreviation + " from " + o.sectionTitle, act: "home-remove", data: { key: o.key, id: s.id } });
    } else {
      tail = '<a class="alt-view" href="#/' + altTab + "/s/" + s.id + '" data-nav aria-label="Open ' + esc(s.abbreviation) + (altTab === "guide" ? " guide" : " calculator") + '">' + UI.icon(altTab === "guide" ? "guide" : "calculate") +
        '<span aria-hidden="true">' + (altTab === "guide" ? "Guide" : "Calculate") + "</span></a>";
    }
    return '<li class="score-card home-row' + (o.edit ? " is-editing" : "") + '" data-id="' + esc(s.id) + '">' + main + tail + "</li>";
  }
  function searchBlock(id, placeholder) {
    return UI.SearchBar({ id: id, placeholder: placeholder, label: placeholder }) + '<div id="search-results" aria-live="polite"></div>';
  }
  function renderSearch(q) {
    var res = document.getElementById("search-results"), body = document.getElementById("page-body"), clear = document.querySelector(".searchbar .clear");
    if (clear) clear.hidden = !q;
    if (!res) return;
    if (!q.trim()) { res.innerHTML = ""; if (body) body.hidden = false; return; }
    var tab = route.tab === "guide" ? "guide" : "calculate", hits = search(q);
    if (body) body.hidden = true;
    var rows = route.tab === "home" ? hits.map(function (s) { return homeRow(s, "score"); }) : hits.map(function (s) { return scoreCard(s, tab, { withCategory: true }); });
    res.innerHTML = UI.Section({ id: "results", title: hits.length + " result" + (hits.length === 1 ? "" : "s"),
      body: hits.length ? UI.CardList(rows, "Search results")
        : UI.EmptyState({ icon: "search", title: "No matching scores", message: "Try an abbreviation such as GCS or WFNS, or a topic such as sedation or spine." }) });
    announce(hits.length + " results");
  }

  /* ---------------- HOME ---------------- */
  /* Order: Search, then the user's section order (default: favorite scores, favorite guides,
     recent calculators, recent guides, priority scores, priority groups). Uses the catalogue only. */
  function homeScreen() {
    var st = Store.get(), sections = st.homeSections.filter(function (h) { return h.visible; });
    var body = searchBlock("search", "Search scores and guides") + '<div id="page-body">' +
      sections.map(function (h) { return homeSection(h.id, st); }).join("") +
      (sections.length ? "" : UI.EmptyState({ title: "All Home sections are hidden", message: "Choose which sections to show in Settings.", action: UI.SecondaryButton({ label: "Customise Home", href: "#/settings", icon: "settings" }) })) +
      '<div class="section home-foot"><a class="section-action" href="#/settings" data-nav>' + UI.icon("settings") + " Customise Home</a></div></div>";
    paint(frame({ title: "Insula Neuro Score", brand: true, tab: "home", body: body }), { title: "Home" });
  }
  function homeSection(id, st) {
    var meta = HOME_SECTION_META[id], editing = !!homeEdit[id], body, action = "";
    var empty = function () {
      return UI.EmptyState({ compact: true, icon: meta.icon, title: meta.emptyTitle, message: meta.empty,
        action: meta.action ? UI.SecondaryButton({ label: meta.action.label, href: meta.action.href, icon: meta.action.icon }) : "" });
    };
    if (id === "priorityGroups") {
      var hidden = st.hiddenGroups;
      var groups = st.priorityGroups.map(category).filter(function (c) { return c && hidden.indexOf(c.id) < 0; });
      if (!groups.length) body = empty();
      else if (editing) body = '<ul class="card-list">' + groups.map(function (c, i) {
          return '<li class="score-card home-row is-editing"><span class="open"><span class="row-icon" aria-hidden="true">' + UI.icon(c.glyph) + '</span><span class="text"><span class="title">' + esc(c.name) + '</span><span class="sub">' + scoresIn(c.id).length + " scores</span></span></span>" +
            UI.IconButton({ icon: "up", label: "Move " + c.name + " up", act: "home-move", disabled: i === 0, data: { key: "priorityGroups", index: st.priorityGroups.indexOf(c.id), delta: -1, to: groups[i - 1] ? st.priorityGroups.indexOf(groups[i - 1].id) : "" } }) +
            UI.IconButton({ icon: "down", label: "Move " + c.name + " down", act: "home-move", disabled: i === groups.length - 1, data: { key: "priorityGroups", index: st.priorityGroups.indexOf(c.id), delta: 1, to: groups[i + 1] ? st.priorityGroups.indexOf(groups[i + 1].id) : "" } }) +
            UI.IconButton({ icon: "close", label: "Remove " + c.name + " from priority groups", act: "home-remove", data: { key: "priorityGroups", id: c.id } }) + "</li>"; }).join("") + "</ul>";
      else body = '<div class="chip-row">' + groups.map(function (c) {
          return '<a class="chip" href="#/calculate/c/' + c.id + '" data-nav>' + UI.icon(c.glyph) + esc(c.name) + ' <span class="n">' + scoresIn(c.id).length + "</span></a>"; }).join("") + "</div>";
      if (groups.length) action = editBtn(id, editing);
    } else {
      var entries = meta.recent ? st[id].filter(function (r) { return score(r.id); }) : st[id].filter(function (x) { return score(x); }).map(function (x) { return { id: x }; });
      if (!entries.length) body = empty();
      else body = UI.CardList(entries.map(function (e, i) {
          var verb = id === "recentCalc" ? "Calculated " : "Opened ";
          return homeRow(score(e.id), meta.kind, { edit: editing && meta.editable, key: id, index: st[id].map(function (x) { return typeof x === "string" ? x : x.id; }).indexOf(e.id), count: entries.length,
            sectionTitle: meta.title.toLowerCase(), time: meta.recent && e.at ? verb + relTime(e.at) : "" });
        }), meta.title);
      if (entries.length) action = meta.recent ? '<button class="section-action" type="button" data-act="clear-recent" data-key="' + id + '">Clear</button>' : editBtn(id, editing);
    }
    return UI.Section({ id: "home-" + id, title: meta.title, action: action, body: body });
  }
  function editBtn(id, editing) {
    return '<button class="section-action" type="button" data-act="home-edit" data-key="' + id + '" aria-pressed="' + editing + '">' + (editing ? "Done" : "Edit") + "</button>";
  }

  /* ---------------- CALCULATE / GUIDE lists ---------------- */
  function rootListScreen(tab) {
    var cats = orderedCategories(false), hiddenN = Store.get().hiddenGroups.length;
    var body = searchBlock("search", tab === "calculate" ? "Search calculators" : "Search guides") + '<div id="page-body">' +
      UI.Section({ id: "cats", title: "Categories", body: cats.length ? '<div class="category-grid">' + cats.map(function (c) {
        return UI.CategoryCard({ category: c, href: "#/" + tab + "/c/" + c.id, count: scoresIn(c.id).length }); }).join("") + "</div>"
        : UI.EmptyState({ title: "All groups are hidden", message: "Show groups again in Settings.", action: UI.SecondaryButton({ label: "Manage groups", href: "#/settings", icon: "settings" }) }) }) +
      (hiddenN ? '<p class="lede" style="margin-top:var(--space-4)">' + hiddenN + " hidden group" + (hiddenN > 1 ? "s" : "") + '. <a href="#/settings" data-nav>Manage groups</a></p>' : "") + "</div>";
    paint(frame({ title: tab === "calculate" ? "Calculate" : "Guide", tab: tab, body: body, wide: true }), { title: tab === "calculate" ? "Calculate" : "Guide" });
  }
  function categoryScreen(tab, catId) {
    var c = category(catId);
    if (!c) return notFound("This score group does not exist.");
    var list = scoresIn(c.id), st = Store.get(), onHome = st.priorityGroups.indexOf(c.id) >= 0, isHidden = st.hiddenGroups.indexOf(c.id) >= 0;
    var controls = '<div class="btn-row" style="margin-bottom:var(--space-2)">' +
      UI.SecondaryButton({ label: onHome ? "On Home (priority)" : "Add group to Home", icon: "pin", act: "promote-group", data: { id: c.id } }) +
      UI.SecondaryButton({ label: isHidden ? "Show group in lists" : "Hide group from lists", icon: isHidden ? "eye" : "close", act: "hide-group", data: { id: c.id } }) + "</div>" +
      (isHidden ? UI.InfoBanner({ title: "This group is hidden", message: "It does not appear in the Calculate and Guide lists or on Home. Its scores remain searchable." }) : "");
    var body = '<p class="lede">' + esc(c.description) + "</p>" + controls + UI.Section({ id: "scores", title: list.length + " score" + (list.length === 1 ? "" : "s"),
      body: list.length ? UI.CardList(list.map(function (s) { return scoreCard(s, tab); }), c.name) : UI.EmptyState({ title: "No scores in this group yet" }) });
    paint(frame({ title: c.name, tab: tab, back: true, body: body }), { title: c.name });
  }

  /* ---------------- SCORE DETAIL (shared shell, Calculate | Guide) ---------------- */
  function detailScreen(tab, id) {
    var s = score(id);
    if (!s) return notFound("This score is not in the catalogue.");
    if (tab === "guide") Store.pushRecent("recentGuide", id);   // calculators are recorded when a result is completed
    var fk = favKey(tab);
    var st = Store.get(), fav = st[fk].indexOf(id) >= 0, prio = st.priorityScores.indexOf(id) >= 0, c = category(s.category);
    var implemented = s.status === "implemented";
    var badge = implemented ? UI.StatusBadge({ tone: "warning", label: "Pending clinical review", icon: false }) : placeholderBadge();
    var head = '<div class="detail-head"><p class="abbr">' + esc(s.abbreviation) + '</p><p class="name">' + esc(s.name) + '</p><div class="badges">' + badge +
      '<a href="#/' + tab + "/c/" + c.id + '" data-nav>' + esc(c.name) + "</a>" + '<span id="version-label"></span></div></div>';
    var toggle = '<nav class="segmented" aria-label="Score view" style="margin-top:var(--space-4)">' +
      '<a href="#/calculate/s/' + id + '" data-replace' + (tab === "calculate" ? ' aria-current="page"' : "") + ">" + UI.icon("calculate") + "Calculate</a>" +
      '<a href="#/guide/s/' + id + '" data-replace' + (tab === "guide" ? ' aria-current="page"' : "") + ">" + UI.icon("guide") + "Guide</a></nav>";
    var prioBtn = UI.SecondaryButton({ label: prio ? "On Home (priority)" : "Add to Home priority", icon: "pin", act: "toggle-priority", data: { id: id } });
    var inner = implemented ? '<div id="score-host">' + UI.LoadingState({ message: "Loading " + s.abbreviation + "…", rows: 3 }) + "</div>" : (tab === "calculate" ? calcShell(s) : guideShell(s));
    var body = head + toggle + inner + '<div class="section btn-row">' + prioBtn + "</div>";
    var favNoun = tab === "guide" ? "favorite guides" : "favorite scores";
    var favBtn = UI.IconButton({ icon: "star", label: (fav ? "Remove from " : "Add to ") + favNoun, act: "toggle-favorite", pressed: fav, data: { id: id, key: fk } });
    paint(frame({ title: s.abbreviation, tab: tab, back: true, body: body, actions: [favBtn], wide: tab === "calculate" }), { title: s.abbreviation + (tab === "guide" ? " guide" : "") });
    if (!implemented) return;
    var routeAtLoad = location.hash, restoreY = goingBackY;
    loadScore(id).then(function (sc) {
      if (location.hash !== routeAtLoad) return;
      var host = document.getElementById("score-host"); if (!host) return;
      document.getElementById("version-label").textContent = sc.version.label;
      if (tab === "calculate") {
        var answers = SESSION_ANSWERS[id] || (SESSION_ANSWERS[id] = window.InsulaEngine.engine.initialAnswers(sc));
        var recorded = false;
        window.Calculator.mount(host, sc, answers, { links: scoreLinks("calculate"), toast: toast, onResult: function (r) {
          // Record use only for a completed calculation (score id + time only; inputs are never stored).
          if ((r.status === "complete" || r.status === "not-interpretable") && !recorded) { recorded = true; Store.pushRecent("recentCalc", id); }
          if (r.status === "incomplete") recorded = false;
        } });
        document.body.classList.add("has-result-bar");
      } else {
        host.innerHTML = window.Calculator.guideHTML(sc, scoreLinks("guide"), "#/calculate/s/" + id);
      }
      if (restoreY) window.scrollTo(0, restoreY);
    }).catch(function (e) {
      var host = document.getElementById("score-host");
      if (host) host.innerHTML = UI.ErrorState({ title: s.abbreviation + " could not be loaded", message: e.message, action: UI.SecondaryButton({ label: "Back to " + c.name, href: "#/" + tab + "/c/" + c.id, icon: "back" }) });
    });
  }
  function calcShell(s) {
    var rows = ""; for (var i = 1; i <= 3; i++) rows += '<div class="row"><span class="dot" aria-hidden="true"></span>Component ' + i + " (pending verification)</div>";
    return '<div class="section">' + UI.WarningBanner({ title: "Calculator not available yet", message: "This is a placeholder in the app shell. Scoring criteria are added only after the published version, sources and licensing are verified." }) + "</div>" +
      '<div class="detail-grid two"><div>' + UI.Section({ id: "inputs", title: "Inputs", body: '<div class="input-shell" aria-label="Input placeholders">' + rows + "</div>" }) + "</div>" +
      '<div class="aside">' + UI.Section({ id: "result", title: "Result", body: UI.ResultCard({ tone: "incomplete", label: "Not available", value: "–", meta: s.abbreviation + " · placeholder", summary: "No calculation in this build." }) +
        '<div class="btn-row" style="margin-top:var(--space-3)">' + UI.SecondaryButton({ label: "Reset", icon: "reset", disabled: true }) +
        UI.SecondaryButton({ label: "Open guide", icon: "guide", href: "#/guide/s/" + s.id, replace: true }) + "</div>" }) + "</div></div>";
  }
  function guideShell(s) {
    var toc = '<nav class="toc" aria-label="Guide sections">' + GUIDE_SECTIONS.map(function (t, i) { return '<a href="#" data-jump="g' + (i + 1) + '">' + (i + 1) + ". " + esc(t.split(" / ")[0]) + "</a>"; }).join("") + "</nav>";
    var cards = GUIDE_SECTIONS.map(function (t, i) {
      return UI.SectionCard({ id: "g" + (i + 1), number: i + 1, title: t, body: '<p class="lede" style="margin:0">Content pending verification.</p><div class="placeholder-lines" aria-hidden="true"><i></i><i></i><i></i></div>' });
    }).join("");
    return '<div class="section">' + UI.PrimaryButton({ label: "Calculate this score →", icon: "calculate", href: "#/calculate/s/" + s.id, replace: true, block: true }) + "</div>" +
      '<div class="section">' + UI.InfoBanner({ title: "Guide content pending", message: "Every guide follows the same 15-section structure shown below." }) + "</div>" +
      UI.Section({ id: "contents", title: "Contents", body: toc }) + '<div class="section">' + cards + "</div>" +
      '<div class="section">' + UI.PrimaryButton({ label: "Calculate this score →", icon: "calculate", href: "#/calculate/s/" + s.id, replace: true, block: true }) + "</div>";
  }

  /* ---------------- SETTINGS ---------------- */
  function reorderRow(o) {
    var b = '<div class="reorder-row' + (o.hidden ? " is-hidden" : "") + (o.moved ? " is-moved" : "") + '"><span class="text"><span class="label">' + esc(o.label) + "</span>" + (o.desc ? '<span class="desc">' + esc(o.desc) + "</span>" : "") + "</span>" +
      UI.IconButton({ icon: "up", label: "Move " + o.label + " up", act: "move", disabled: o.index === 0, data: { key: o.key, index: o.index, delta: -1 } }) +
      UI.IconButton({ icon: "down", label: "Move " + o.label + " down", act: "move", disabled: o.index === o.count - 1, data: { key: o.key, index: o.index, delta: 1 } });
    if (o.remove) b += UI.IconButton({ icon: "close", label: "Remove " + o.label, act: "remove", data: { key: o.key, id: o.id } });
    if (o.visibility != null) b += '<span class="toggle"><input type="checkbox" role="switch" aria-label="Show ' + esc(o.label) + '" data-act="' + o.visibilityAct + '" data-id="' + esc(o.id) + '"' + (o.visibility ? " checked" : "") + '><span class="track"></span></span>';
    return "<li>" + b + "</div></li>";
  }
  var lastMoved = null;
  function managedList(key, items, labelOf, descOf, addLabel, emptyMsg) {
    var list = items.length ? '<ul class="settings-list">' + items.map(function (x, i) {
      return reorderRow({ key: key, id: x.id, index: i, count: items.length, label: labelOf(x), desc: descOf(x), remove: true, moved: lastMoved && lastMoved.key === key && lastMoved.index === i });
    }).join("") + "</ul>" : UI.EmptyState({ compact: true, icon: "inbox", title: "None selected", message: emptyMsg });
    return list + '<div style="margin-top:var(--space-3)">' + UI.SecondaryButton({ label: addLabel, icon: "plus", href: "#/settings/pick/" + key, block: true }) + "</div>";
  }
  function settingsScreen() {
    var st = Store.get();
    var appearance = UI.Segmented({ label: "Appearance", act: "set-pref", key: "theme", value: st.theme, options: [{ value: "system", label: "System" }, { value: "light", label: "Light" }, { value: "dark", label: "Dark" }] }) +
      '<ul class="settings-list" style="margin-top:var(--space-3)"><li>' + UI.Toggle({ id: "hc", label: "High contrast", description: "Stronger borders and text", checked: st.highContrast, act: "toggle-contrast" }) + "</li></ul>" +
      '<p class="lede" style="margin-top:var(--space-2)">Text size follows your device font size setting.</p>';
    var startup = UI.Segmented({ label: "Startup screen", act: "set-pref", key: "startup", value: st.startup, options: [{ value: "home", label: "Home" }, { value: "calculate", label: "Calculate" }, { value: "guide", label: "Guide" }] });
    var homeLayout = '<ul class="settings-list">' + st.homeSections.map(function (h, i) {
      return reorderRow({ key: "homeSections", id: h.id, index: i, count: st.homeSections.length, label: HOME_SECTION_META[h.id].title, hidden: !h.visible,
        visibility: h.visible, visibilityAct: "toggle-section", moved: lastMoved && lastMoved.key === "homeSections" && lastMoved.index === i });
    }).join("") + "</ul>";
    var sc = function (x) { return x.abbreviation; }, sd = function (x) { return sub(x); };
    var favs = managedList("favorites", st.favorites.map(score).filter(Boolean), sc, sd, "Add favorite scores", "No favorite scores yet. Add a score to Favorites for one-tap access.");
    var favGuides = managedList("favoriteGuides", st.favoriteGuides.map(score).filter(Boolean), sc, sd, "Add favorite guides", "No favorite guides yet. Save a guide to Favorites to reopen it in one tap.");
    var prio = managedList("priorityScores", st.priorityScores.map(score).filter(Boolean), sc, sd, "Choose priority scores", "Priority scores appear first on Home.");
    var groups = managedList("priorityGroups", st.priorityGroups.map(category).filter(Boolean), function (c) { return c.name; }, function (c) { return scoresIn(c.id).length + " scores"; }, "Choose priority groups", "Priority groups appear as shortcuts on Home.");
    var allCats = orderedCategories(true);
    var groupVis = '<ul class="settings-list">' + allCats.map(function (c, i) {
      return reorderRow({ key: "groupOrder", id: c.id, index: i, count: allCats.length, label: c.name, desc: scoresIn(c.id).length + " scores", hidden: st.hiddenGroups.indexOf(c.id) >= 0,
        visibility: st.hiddenGroups.indexOf(c.id) < 0, visibilityAct: "toggle-group-visible", moved: lastMoved && lastMoved.key === "groupOrder" && lastMoved.index === i });
    }).join("") + "</ul>";
    lastMoved = null;
    var body =
      UI.Section({ id: "s-appearance", title: "Appearance", body: appearance }) +
      UI.Section({ id: "s-startup", title: "Startup screen", body: startup }) +
      UI.Section({ id: "s-home", title: "Home layout", body: '<p class="lede">Order and show or hide the sections on Home.</p>' + homeLayout }) +
      UI.Section({ id: "s-favorites", title: "Favorite scores", body: favs }) +
      UI.Section({ id: "s-favguides", title: "Favorite guides", body: favGuides }) +
      UI.Section({ id: "s-priority", title: "Priority scores", body: prio }) +
      UI.Section({ id: "s-pgroups", title: "Priority groups", body: groups }) +
      UI.Section({ id: "s-groups", title: "Score groups in Calculate and Guide", body: '<p class="lede">Order the groups and choose which are visible. Hidden groups are also left out of Home.</p>' + groupVis }) +
      UI.Section({ id: "s-history", title: "History", body: '<p class="lede">Kept only on this device: the score and the time. Calculator inputs are never stored.</p>' +
        '<ul class="settings-list">' +
        '<li class="reorder-row"><span class="text"><span class="label">Recently used calculators</span><span class="desc">' + st.recentCalc.length + " item" + (st.recentCalc.length === 1 ? "" : "s") + "</span></span>" +
          UI.SecondaryButton({ label: "Clear", act: "clear-recent", data: { key: "recentCalc" }, disabled: !st.recentCalc.length }) + "</li>" +
        '<li class="reorder-row"><span class="text"><span class="label">Recently viewed guides</span><span class="desc">' + st.recentGuide.length + " item" + (st.recentGuide.length === 1 ? "" : "s") + "</span></span>" +
          UI.SecondaryButton({ label: "Clear", act: "clear-recent", data: { key: "recentGuide" }, disabled: !st.recentGuide.length }) + "</li></ul>" +
        '<div style="margin-top:var(--space-3)">' + UI.SecondaryButton({ label: "Clear all history", icon: "clock", act: "clear-recent", data: { key: "all" }, block: true, disabled: !st.recentCalc.length && !st.recentGuide.length }) + "</div>" }) +
      UI.Section({ id: "s-data", title: "Data on this device", body: '<div class="btn-row">' +
        UI.SecondaryButton({ label: "Reset all settings", icon: "reset", act: "reset-all" }) + "</div>" +
        (Store.storageAvailable() ? "" : '<div style="margin-top:var(--space-3)">' + UI.WarningBanner({ title: "Settings cannot be saved", message: "Device storage is unavailable. Changes will last only until the app closes." }) + "</div>") }) +
      UI.Section({ id: "s-about", title: "About", body: '<div class="about"><p><b>Insula Neuro Score</b> · Insula Neurosciences<br>Version 0.6.0 (Phase 5: personalized Home)</p>' +
        '<p class="lede">A clinical calculation tool and reference guide. It does not diagnose and does not make treatment decisions. Works fully offline; preferences are stored only on this device. No patient data is collected or stored.</p>' +
        UI.SecondaryButton({ label: "Design system", icon: "eye", href: "#/settings/gallery", block: true }) + "</div>" });
    paint(frame({ title: "Settings", tab: "", back: true, noSettings: true, body: body }), { title: "Settings", focusMain: false });
  }
  function pickerScreen(key) {
    var st = Store.get(), titles = { favorites: "Favorite scores", favoriteGuides: "Favorite guides", priorityScores: "Priority scores", priorityGroups: "Priority groups" };
    if (!titles[key]) return notFound("Unknown list.");
    var body;
    if (key === "priorityGroups") {
      body = '<ul class="settings-list">' + orderedCategories(true).map(function (c) {
        return "<li>" + UI.Toggle({ id: "p-" + c.id, label: c.name, description: scoresIn(c.id).length + " scores", checked: st.priorityGroups.indexOf(c.id) >= 0, act: "pick", data: { key: key, id: c.id } }) + "</li>"; }).join("") + "</ul>";
    } else {
      body = orderedCategories(true).map(function (c) {
        return UI.Section({ id: "pk-" + c.id, title: c.name, body: '<ul class="settings-list">' + scoresIn(c.id).map(function (s) {
          return "<li>" + UI.Toggle({ id: "p-" + s.id, label: s.abbreviation, description: sub(s), checked: st[key].indexOf(s.id) >= 0, act: "pick", data: { key: key, id: s.id } }) + "</li>"; }).join("") + "</ul>" });
      }).join("");
    }
    paint(frame({ title: titles[key], tab: "", back: true, noSettings: true, body: '<p class="lede">Selected items appear on Home. Reorder them in Settings.</p>' + body }), { title: titles[key], focusMain: false });
  }
  function galleryScreen() {
    var tones = ["normal", "low", "mild", "moderate", "high", "critical", "info", "incomplete"];
    var g = function (t, h) { return '<div class="gallery-item"><h3>' + esc(t) + "</h3>" + h + "</div>"; };
    var demo = CATALOG.scores[0];
    var body = '<p class="lede">Every screen is built from these components. Colours come only from semantic tokens.</p>' +
      g("Semantic colours", '<div class="gallery-swatches">' + ["success", "warning", "concern", "error", "info", "neutral", "primary"].map(function (t) {
        return '<div class="swatch tone-' + t + '"><i></i><span>' + esc(t === "concern" ? "high concern" : t) + "</span></div>"; }).join("") + "</div>") +
      g("StatusBadge", '<div class="chip-row">' + tones.map(function (t) { return UI.StatusBadge({ tone: t }); }).join("") + "</div>") +
      g("ResultCard", '<div class="detail-grid">' + [["normal", "15", "No impairment measured"], ["moderate", "10", "Moderate range"], ["high", "7", "High concern example"], ["critical", "3", "Very high concern example"], ["info", "Grade II", "Classification result"], ["incomplete", "–", "Complete all inputs"]].map(function (x) {
        return UI.ResultCard({ tone: x[0], value: x[1], meta: "Example only", summary: x[2] }); }).join("") + "</div>") +
      g("SearchBar", UI.SearchBar({ id: "demo-search", placeholder: "Search scores" })) +
      g("ScoreCard", UI.CardList([UI.ScoreCard({ score: demo, href: "#/settings/gallery", badge: placeholderBadge(), favorite: true }), UI.ScoreCard({ score: CATALOG.scores[5], href: "#/settings/gallery", badge: placeholderBadge(), favorite: false })])) +
      g("CategoryCard", '<div class="category-grid">' + CATALOG.categories.slice(0, 2).map(function (c) { return UI.CategoryCard({ category: c, href: "#/settings/gallery", count: scoresIn(c.id).length }); }).join("") + "</div>") +
      g("SectionCard", UI.SectionCard({ number: 1, title: "What is this score?", body: "<p>Section content.</p>" })) +
      g("Buttons", '<div class="btn-row">' + UI.PrimaryButton({ label: "Primary action", icon: "calculate" }) + UI.SecondaryButton({ label: "Secondary action", icon: "guide" }) + UI.SecondaryButton({ label: "Disabled", disabled: true }) + "</div>") +
      g("Toggle and segmented control", '<ul class="settings-list"><li>' + UI.Toggle({ id: "demo-t", label: "Toggle", description: "Switch with label", checked: true }) + "</li></ul><div style=\"margin-top:var(--space-3)\">" + UI.Segmented({ label: "Demo", act: "noop", value: "a", options: [{ value: "a", label: "Option A" }, { value: "b", label: "Option B" }] }) + "</div>") +
      g("InfoBanner", UI.InfoBanner({ title: "Information", message: "Neutral contextual information." })) +
      g("WarningBanner", UI.WarningBanner({ title: "Warning", message: "Something needs attention before relying on this." })) +
      g("EmptyState", UI.EmptyState({ title: "Nothing here yet", message: "Explains what to do next.", action: UI.SecondaryButton({ label: "Take action", icon: "plus" }) })) +
      g("ErrorState", UI.ErrorState({ title: "Something went wrong", message: "Explains what happened and how to fix it.", action: UI.PrimaryButton({ label: "Try again", icon: "reset" }) })) +
      g("LoadingState", UI.LoadingState({ message: "Loading scores…", rows: 2 })) +
      g("Input controls (live engine, non-clinical demo)", UI.InfoBanner({ title: "Not a clinical score", message: "Exercises single choice, dropdown, yes/no, multiple choice, integer, decimal, number, clinical measurement and not-testable inputs." }) + '<div id="demo-host" style="margin-top:var(--space-3)"></div>');
    paint(frame({ title: "Design system", tab: "", back: true, noSettings: true, body: body, wide: true }), { title: "Design system", focusMain: false });
    loadJSON("content/dev/demo-inputs.json").then(function (sc) {
      var host = document.getElementById("demo-host"); if (!host) return;
      window.Calculator.mount(host, sc, SESSION_ANSWERS.__demo || (SESSION_ANSWERS.__demo = {}), { links: function () { return null; }, toast: toast }); document.body.classList.add("has-result-bar");
    });
  }

  /* ---------------- events ---------------- */
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a");
    if (a && a.hasAttribute("data-jump")) {
      ev.preventDefault(); var t = document.getElementById(a.getAttribute("data-jump"));
      if (t) { t.scrollIntoView({ block: "start" }); var h = t.querySelector("h3"); h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
      return;
    }
    if (a && a.hasAttribute("data-replace")) { ev.preventDefault(); replaceTo(a.getAttribute("href")); return; }
    if (a && a.hasAttribute("data-nav")) {
      ev.preventDefault();
      var href = a.getAttribute("href");
      if (a.hasAttribute("data-tab")) { depth = 0; if (href !== location.hash) replaceTo(href); else window.scrollTo(0, 0); return; }
      navigate(href); return;
    }
    var b = ev.target.closest("button[data-act]"); if (!b || b.disabled) return;
    var act = b.getAttribute("data-act"), d = b.dataset;
    switch (act) {
      case "back": if (!window.handleBack()) replaceTo(startHash()); break;
      case "clear-search": var inp = document.getElementById(d.for); inp.value = ""; renderSearch(""); inp.focus(); break;
      case "toggle-favorite": {
        var key = d.key || "favorites", on = Store.get()[key].indexOf(d.id) < 0, noun = key === "favoriteGuides" ? "favorite guides" : "favorite scores";
        Store.toggleIn(key, d.id);
        document.querySelectorAll('[data-act="toggle-favorite"][data-id="' + d.id + '"][data-key="' + key + '"]').forEach(function (el) {
          var sc = score(d.id); el.setAttribute("aria-pressed", String(on));
          el.setAttribute("aria-label", (on ? "Remove " : "Add ") + (el.closest(".appbar") ? "" : sc.abbreviation + " ") + (on ? "from " : "to ") + noun);
        });
        toast(on ? "Added to " + noun : "Removed from " + noun); break;
      }
      case "toggle-priority": {
        var on2 = Store.get().priorityScores.indexOf(d.id) < 0; Store.toggleIn("priorityScores", d.id);
        b.querySelector("span").textContent = on2 ? "On Home (priority)" : "Add to Home priority";
        toast(on2 ? "Added to Home priority" : "Removed from Home priority"); break;
      }
      case "set-pref": Store.update(function (s) { s[d.key] = d.value; return s; }); applyTheme(); refocusAfterRender(function () { settingsScreen(); }, '[data-act="set-pref"][data-key="' + d.key + '"][data-value="' + d.value + '"]'); announce("Saved"); break;
      case "move": {
        var key = d.key, i = Number(d.index), delta = Number(d.delta), sel;
        if (key === "groupOrder") Store.update(function (s) { var order = orderedCategories(true).map(function (c) { return c.id; }); var j = i + delta; var t = order[i]; order[i] = order[j]; order[j] = t; s.groupOrder = order; return s; });
        else Store.move(key, i, delta);
        lastMoved = { key: key, index: i + delta };
        sel = '[data-act="move"][data-key="' + key + '"][data-index="' + (i + delta) + '"][data-delta="' + delta + '"]';
        refocusAfterRender(settingsScreen, sel, '[data-act="move"][data-key="' + key + '"][data-index="' + (i + delta) + '"][data-delta="' + (-delta) + '"]');
        announce("Moved to position " + (i + delta + 1)); break;
      }
      case "remove": Store.removeFrom(d.key, d.id); refocusAfterRender(settingsScreen, "#s-" + ({ favorites: "favorites", favoriteGuides: "favguides", priorityScores: "priority" }[d.key] || "pgroups") + "-h"); toast("Removed"); break;
      case "clear-recent": {
        var keys = d.key === "all" ? ["recentCalc", "recentGuide"] : [d.key], snap = Store.snapshot(keys);
        Store.update(function (x) { keys.forEach(function (k) { x[k] = []; }); return x; });
        var redraw = function () { if (route.tab === "home") homeScreen(); else if (route.tab === "settings" && !route.kind) refocusAfterRender(settingsScreen, "#s-history-h"); };
        redraw();
        toast(d.key === "all" ? "History cleared" : d.key === "recentCalc" ? "Recent calculators cleared" : "Recent guides cleared", { label: "Undo", run: function () { Store.restore(snap); redraw(); announce("History restored"); } });
        break;
      }
      case "home-edit": homeEdit[d.key] = !homeEdit[d.key]; refocusAfterRender(homeScreen, '[data-act="home-edit"][data-key="' + d.key + '"]'); announce(homeEdit[d.key] ? "Editing " + HOME_SECTION_META[d.key].title : "Done"); break;
      case "home-move": {
        var i0 = Number(d.index), j0 = d.to !== undefined && d.to !== "" ? Number(d.to) : i0 + Number(d.delta);
        Store.update(function (x) { var arr = x[d.key]; if (j0 < 0 || j0 >= arr.length) return x; var t = arr[i0]; arr[i0] = arr[j0]; arr[j0] = t; return x; });
        var movedId = Store.get()[d.key][j0]; movedId = typeof movedId === "string" ? movedId : movedId && movedId.id;
        refocusAfterRender(homeScreen, '[data-act="home-move"][data-key="' + d.key + '"][data-index="' + j0 + '"][data-delta="' + d.delta + '"]', '[data-act="home-move"][data-key="' + d.key + '"][data-index="' + j0 + '"]');
        announce("Moved to position " + (j0 + 1)); break;
      }
      case "home-remove": {
        var snap2 = Store.snapshot([d.key]), label = d.key === "priorityGroups" ? category(d.id).name : score(d.id).abbreviation;
        Store.removeFrom(d.key, d.id);
        if (!Store.get()[d.key].length) homeEdit[d.key] = false;
        refocusAfterRender(homeScreen, "#home-" + d.key + "-h");
        toast(label + " removed", { label: "Undo", run: function () { Store.restore(snap2); homeScreen(); } }); break;
      }
      case "promote-group": {
        var onG = Store.get().priorityGroups.indexOf(d.id) < 0; Store.toggleIn("priorityGroups", d.id);
        b.querySelector("span").textContent = onG ? "On Home (priority)" : "Add group to Home";
        toast(onG ? category(d.id).name + " added to Home" : category(d.id).name + " removed from Home"); break;
      }
      case "hide-group": {
        var hiding = Store.get().hiddenGroups.indexOf(d.id) < 0, cname = category(d.id).name;
        Store.toggleIn("hiddenGroups", d.id); categoryScreen(route.tab, d.id);
        toast(hiding ? cname + " hidden from lists" : cname + " shown in lists", hiding ? { label: "Undo", run: function () { Store.toggleIn("hiddenGroups", d.id); categoryScreen(route.tab, d.id); } } : null); break;
      }
      case "reset-all":
        if (window.confirm("Reset appearance, startup screen, favourites, priority items, groups and Home layout to defaults?")) { Store.reset(); applyTheme(); settingsScreen(); toast("Settings reset"); }
        break;
    }
  });
  function refocusAfterRender(fn, selector, fallback) {
    var y = window.scrollY; fn(); window.scrollTo(0, y);
    var el = document.querySelector(selector); if (!el || el.disabled) el = fallback ? document.querySelector(fallback) : null;
    if (el) { if (el.tagName === "H2") el.setAttribute("tabindex", "-1"); el.focus({ preventScroll: true }); }
  }
  document.addEventListener("change", function (ev) {
    var t = ev.target, act = t.getAttribute("data-act"); if (!act) return;
    if (act === "toggle-contrast") { Store.update(function (s) { s.highContrast = t.checked; return s; }); applyTheme(); }
    else if (act === "toggle-section") { Store.update(function (s) { s.homeSections.forEach(function (h) { if (h.id === t.dataset.id) h.visible = t.checked; }); return s; }); t.closest(".reorder-row").classList.toggle("is-hidden", !t.checked); }
    else if (act === "toggle-group-visible") { Store.update(function (s) { var id = t.dataset.id; s.hiddenGroups = s.hiddenGroups.filter(function (x) { return x !== id; }); if (!t.checked) s.hiddenGroups.push(id); return s; }); t.closest(".reorder-row").classList.toggle("is-hidden", !t.checked); }
    else if (act === "pick") { Store.toggleIn(t.dataset.key, t.dataset.id); }
    announce("Saved");
  });
  document.addEventListener("input", function (ev) { if (ev.target.id === "search") renderSearch(ev.target.value); });
  window.addEventListener("ins-config", function () { /* system font scale or orientation changed natively; layout is fluid */ });

  /* ---------------- boot ---------------- */
  applyTheme();
  root.innerHTML = '<div class="shell">' + UI.AppBar({ title: "Insula Neuro Score", brand: true }) + '<main class="content">' + UI.LoadingState({ message: "Loading scores…", rows: 4 }) + "</main></div>";
  function boot() {
    loadJSON("content/catalog.json")
      .then(function (c) {
        if (!c || !Array.isArray(c.scores) || !Array.isArray(c.categories)) throw new Error("Catalogue format is invalid");
        CATALOG = c; IDX = buildIndex(c);
        Store.prune(c.scores.map(function (s) { return s.id; }), c.categories.map(function (x) { return x.id; }));
        if (!location.hash || location.hash === "#" || location.hash === "#/") location.replace(startHash());
        render();
      })
      .catch(function (e) {
        root.innerHTML = '<div class="shell">' + UI.AppBar({ title: "Insula Neuro Score", brand: true }) + '<main class="content">' +
          UI.ErrorState({ title: "Scores could not be loaded", message: "The bundled score catalogue could not be read (" + e.message + "). Reinstalling the app usually fixes this.", action: UI.PrimaryButton({ label: "Try again", icon: "reset", act: "retry" }) }) + "</main></div>";
      });
  }
  document.addEventListener("click", function (ev) { var b = ev.target.closest('[data-act="retry"]'); if (b) { root.innerHTML = '<div class="shell"><main class="content">' + UI.LoadingState({ message: "Loading scores…" }) + "</main></div>"; boot(); } });
  boot();
})();
