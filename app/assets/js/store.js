/* =========================================================================
   Insula Neuro Score — Local persistence (schema v3)
   One versioned record in localStorage. Stores preferences, score ids and
   timestamps only — never calculator inputs or any patient data.
   ========================================================================= */
(function (global) {
  "use strict";
  var KEY = "ins.store.v3", V2_KEY = "ins.store.v2", LEGACY_KEY = "ins.prefs", VERSION = 3, RECENT_MAX = 10;
  /* Home order: search is fixed on top; these sections follow. v0.11: priority groups first, so the
     default quick groups (Quick Clinical Examination, Neurotrauma, Vascular) are the top level on Home. */
  var HOME_SECTIONS = ["priorityGroups", "favorites", "favoriteGuides", "recentCalc", "recentGuide", "priorityScores"];
  var V2_DEFAULT_ORDER = ["priorityScores", "priorityGroups", "favorites", "recentCalc", "recentGuide"];

  function defaults() {
    return {
      v: VERSION,
      theme: "system", highContrast: false, startup: "home",
      favorites: [],            // favourite scores (open calculator; guide also one tap away)
      favoriteGuides: [],       // favourite guides
      recentCalc: [],           // [{id, at}] completed calculations, newest first
      recentGuide: [],          // [{id, at}] opened guides, newest first
      priorityScores: [],       // user-selected scores promoted to Home
      priorityGroups: ["quick-exam", "neurotrauma", "vascular"],   // groups promoted to Home; defaults = catalog.defaultPriorityGroups
      hiddenGroups: [], groupOrder: [],
      homeSections: HOME_SECTIONS.map(function (id) { return { id: id, visible: true }; })
    };
  }

  function isStrArr(a) { return Array.isArray(a) && a.every(function (x) { return typeof x === "string"; }); }
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }); }
  function recents(a) {
    if (!Array.isArray(a)) return [];
    var seen = {}, out = [];
    a.forEach(function (r) {
      var e = typeof r === "string" ? { id: r, at: 0 } : r;
      if (e && typeof e.id === "string" && !seen[e.id]) { seen[e.id] = 1; out.push({ id: e.id, at: typeof e.at === "number" && isFinite(e.at) ? e.at : 0 }); }
    });
    return out.slice(0, RECENT_MAX);
  }

  /* Coerce any stored object into a valid v3 state. */
  function sanitize(raw) {
    var s = defaults();
    if (!raw || typeof raw !== "object") return s;
    if (["system", "light", "dark"].indexOf(raw.theme) >= 0) s.theme = raw.theme;
    s.highContrast = raw.highContrast === true;
    if (["home", "calculate", "guide"].indexOf(raw.startup) >= 0) s.startup = raw.startup;
    ["favorites", "favoriteGuides", "priorityScores", "priorityGroups", "hiddenGroups", "groupOrder"].forEach(function (k) { if (isStrArr(raw[k])) s[k] = uniq(raw[k]); });
    s.recentCalc = recents(raw.recentCalc); s.recentGuide = recents(raw.recentGuide);
    if (Array.isArray(raw.homeSections)) {
      var seen = {}, out = [];
      raw.homeSections.forEach(function (h) { if (h && HOME_SECTIONS.indexOf(h.id) >= 0 && !seen[h.id]) { seen[h.id] = 1; out.push({ id: h.id, visible: h.visible !== false }); } });
      HOME_SECTIONS.forEach(function (id) { if (!seen[id]) out.push({ id: id, visible: true }); });
      s.homeSections = out;
    }
    return s;
  }

  /* v2 → v3: favourites stay as favourite scores; recents gain timestamps (unknown = 0);
     Home order moves to the Phase 5 order unless the user had customised it. */
  function migrateV2(old) {
    var s = Object.assign({}, old);
    s.favoriteGuides = [];
    var order = Array.isArray(old.homeSections) ? old.homeSections.map(function (h) { return h.id; }) : null;
    var customised = order && JSON.stringify(order) !== JSON.stringify(V2_DEFAULT_ORDER);
    if (customised) {
      var hs = old.homeSections.slice(), i = order.indexOf("favorites");
      hs.splice(i < 0 ? hs.length : i + 1, 0, { id: "favoriteGuides", visible: true });
      s.homeSections = hs;
    } else {
      var vis = {}; (old.homeSections || []).forEach(function (h) { vis[h.id] = h.visible !== false; });
      s.homeSections = HOME_SECTIONS.map(function (id) { return { id: id, visible: vis[id] !== false }; });
    }
    return sanitize(s);
  }
  /* v0.1 (ins.prefs) → v3. */
  function migrateLegacy(old) {
    var s = {};
    if (["system", "light", "dark"].indexOf(old.theme) >= 0) s.theme = old.theme;
    s.highContrast = old.highContrast === true;
    s.startup = old.startup === "calc" ? "calculate" : old.startup;
    s.priorityScores = isStrArr(old.pinned) ? old.pinned : [];
    s.favoriteGuides = isStrArr(old.favGuides) ? old.favGuides : [];
    s.priorityGroups = isStrArr(old.homeGroups) ? old.homeGroups : [];
    ["recentCalc", "recentGuide", "groupOrder", "hiddenGroups"].forEach(function (k) { if (isStrArr(old[k])) s[k] = old[k]; });
    return sanitize(s);
  }

  var state, listeners = [], storageOk = true;
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw) return sanitize(JSON.parse(raw));
      var v2 = localStorage.getItem(V2_KEY);
      if (v2) { var m2 = migrateV2(JSON.parse(v2)); persist(m2); localStorage.removeItem(V2_KEY); return m2; }
      var legacy = localStorage.getItem(LEGACY_KEY);
      if (legacy) { var m1 = migrateLegacy(JSON.parse(legacy)); persist(m1); localStorage.removeItem(LEGACY_KEY); return m1; }
    } catch (e) { storageOk = false; }
    return defaults();
  }
  function persist(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); storageOk = true; } catch (e) { storageOk = false; } }
  state = load();

  var Store = {
    get: function () { return state; },
    update: function (fn) {
      var draft = JSON.parse(JSON.stringify(state));
      var r = fn(draft); state = sanitize(r || draft); persist(state);
      listeners.forEach(function (l) { l(state); });
      return state;
    },
    subscribe: function (fn) { listeners.push(fn); },
    reset: function () { state = defaults(); persist(state); listeners.forEach(function (l) { l(state); }); },
    storageAvailable: function () { return storageOk; },
    prune: function (scoreIds, groupIds) {
      var S = {}, G = {}; scoreIds.forEach(function (x) { S[x] = 1; }); groupIds.forEach(function (x) { G[x] = 1; });
      var okS = function (x) { return S[typeof x === "string" ? x : x.id] === 1; }, okG = function (x) { return G[x] === 1; };
      Store.update(function (d) {
        ["favorites", "favoriteGuides", "priorityScores", "recentCalc", "recentGuide"].forEach(function (k) { d[k] = d[k].filter(okS); });
        ["priorityGroups", "hiddenGroups", "groupOrder"].forEach(function (k) { d[k] = d[k].filter(okG); });
        return d;
      });
    },
    has: function (key, id) { return state[key].indexOf(id) >= 0; },
    toggleIn: function (key, id) { return Store.update(function (d) { var i = d[key].indexOf(id); if (i >= 0) d[key].splice(i, 1); else d[key].push(id); return d; }); },
    removeFrom: function (key, id) { return Store.update(function (d) { d[key] = d[key].filter(function (x) { return (typeof x === "string" ? x : x.id) !== id; }); return d; }); },
    pushRecent: function (key, id, now) {
      return Store.update(function (d) { d[key] = [{ id: id, at: now || Date.now() }].concat(d[key].filter(function (x) { return x.id !== id; })).slice(0, RECENT_MAX); return d; });
    },
    move: function (key, index, delta) {
      return Store.update(function (d) {
        var a = d[key], j = index + delta; if (j < 0 || j >= a.length) return d;
        var t = a[index]; a[index] = a[j]; a[j] = t; return d;
      });
    },
    snapshot: function (keys) { var o = {}; keys.forEach(function (k) { o[k] = JSON.parse(JSON.stringify(state[k])); }); return o; },
    restore: function (snap) { return Store.update(function (d) { Object.keys(snap).forEach(function (k) { d[k] = snap[k]; }); return d; }); },
    HOME_SECTIONS: HOME_SECTIONS, RECENT_MAX: RECENT_MAX, KEY: KEY, _sanitize: sanitize, _migrateV2: migrateV2, _migrateLegacy: migrateLegacy
  };
  global.Store = Store;
})(window);
