/* =========================================================================
   Insula Neuro Score — Local persistence
   Single versioned record in localStorage. Never stores patient data.
   ========================================================================= */
(function (global) {
  "use strict";
  var KEY = "ins.store.v2", LEGACY_KEY = "ins.prefs", VERSION = 2, RECENT_MAX = 10;
  var HOME_SECTIONS = ["priorityScores", "priorityGroups", "favorites", "recentCalc", "recentGuide"];

  function defaults() {
    return {
      v: VERSION,
      theme: "system",              // system | light | dark
      highContrast: false,
      startup: "home",              // home | calculate | guide
      favorites: [],                // score ids
      priorityScores: ["gcs", "nihss", "ich", "wfns"],
      priorityGroups: ["stroke", "consciousness", "sah"],
      recentCalc: [],
      recentGuide: [],
      hiddenGroups: [],             // category ids hidden from Calculate/Guide lists
      groupOrder: [],               // category ids, full order
      homeSections: HOME_SECTIONS.map(function (id) { return { id: id, visible: true }; })
    };
  }

  function isStrArr(a) { return Array.isArray(a) && a.every(function (x) { return typeof x === "string"; }); }
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }); }

  /* Coerce any stored object into a valid current-version state. */
  function sanitize(raw) {
    var d = defaults(), s = Object.assign({}, d);
    if (!raw || typeof raw !== "object") return s;
    if (["system", "light", "dark"].indexOf(raw.theme) >= 0) s.theme = raw.theme;
    s.highContrast = raw.highContrast === true;
    if (["home", "calculate", "guide"].indexOf(raw.startup) >= 0) s.startup = raw.startup;
    ["favorites", "priorityScores", "priorityGroups", "recentCalc", "recentGuide", "hiddenGroups", "groupOrder"].forEach(function (k) {
      if (isStrArr(raw[k])) s[k] = uniq(raw[k]);
    });
    s.recentCalc = s.recentCalc.slice(0, RECENT_MAX); s.recentGuide = s.recentGuide.slice(0, RECENT_MAX);
    if (Array.isArray(raw.homeSections)) {
      var seen = {}, out = [];
      raw.homeSections.forEach(function (h) { if (h && HOME_SECTIONS.indexOf(h.id) >= 0 && !seen[h.id]) { seen[h.id] = 1; out.push({ id: h.id, visible: h.visible !== false }); } });
      HOME_SECTIONS.forEach(function (id) { if (!seen[id]) out.push({ id: id, visible: true }); });
      s.homeSections = out;
    }
    return s;
  }

  /* v0.1.0 stored {pinned, favGuides, recentCalc, recentGuide, groupOrder, hiddenGroups, homeGroups, theme, highContrast, startup}. */
  function migrateLegacy(old) {
    var s = defaults();
    if (["system", "light", "dark"].indexOf(old.theme) >= 0) s.theme = old.theme;
    s.highContrast = old.highContrast === true;
    if (old.startup === "calc") s.startup = "calculate"; else if (old.startup === "guide" || old.startup === "home") s.startup = old.startup;
    if (isStrArr(old.pinned) && old.pinned.length) s.priorityScores = old.pinned;
    if (isStrArr(old.favGuides)) s.favorites = old.favGuides;
    if (isStrArr(old.homeGroups) && old.homeGroups.length) s.priorityGroups = old.homeGroups;
    ["recentCalc", "recentGuide", "groupOrder", "hiddenGroups"].forEach(function (k) { if (isStrArr(old[k])) s[k] = old[k]; });
    return s;
  }

  var state, listeners = [], storageOk = true;
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw) return sanitize(JSON.parse(raw));
      var legacy = localStorage.getItem(LEGACY_KEY);
      if (legacy) { var m = sanitize(migrateLegacy(JSON.parse(legacy))); persist(m); localStorage.removeItem(LEGACY_KEY); return m; }
    } catch (e) { storageOk = false; }
    return defaults();
  }
  function persist(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); storageOk = true; } catch (e) { storageOk = false; }
  }
  state = load();

  var Store = {
    get: function () { return state; },
    /** update(fn) — fn receives a draft copy; result is sanitised, saved and broadcast. */
    update: function (fn) {
      var draft = JSON.parse(JSON.stringify(state));
      var r = fn(draft); state = sanitize(r || draft); persist(state);
      listeners.forEach(function (l) { l(state); });
      return state;
    },
    subscribe: function (fn) { listeners.push(fn); },
    reset: function () { state = defaults(); persist(state); listeners.forEach(function (l) { l(state); }); },
    storageAvailable: function () { return storageOk; },
    /** Remove ids that no longer exist in the catalogue (e.g. after a content update). */
    prune: function (scoreIds, groupIds) {
      var keepS = function (a) { return a.filter(function (x) { return scoreIds.indexOf(x) >= 0; }); };
      var keepG = function (a) { return a.filter(function (x) { return groupIds.indexOf(x) >= 0; }); };
      Store.update(function (d) {
        ["favorites", "priorityScores", "recentCalc", "recentGuide"].forEach(function (k) { d[k] = keepS(d[k]); });
        ["priorityGroups", "hiddenGroups", "groupOrder"].forEach(function (k) { d[k] = keepG(d[k]); });
        return d;
      });
    },
    /* helpers */
    toggleIn: function (key, id) { return Store.update(function (d) { var i = d[key].indexOf(id); if (i >= 0) d[key].splice(i, 1); else d[key].push(id); return d; }); },
    pushRecent: function (key, id) { return Store.update(function (d) { d[key] = [id].concat(d[key].filter(function (x) { return x !== id; })).slice(0, RECENT_MAX); return d; }); },
    move: function (key, index, delta) {
      return Store.update(function (d) {
        var a = d[key], j = index + delta; if (j < 0 || j >= a.length) return d;
        var t = a[index]; a[index] = a[j]; a[j] = t; return d;
      });
    },
    HOME_SECTIONS: HOME_SECTIONS, RECENT_MAX: RECENT_MAX, _sanitize: sanitize, _migrateLegacy: migrateLegacy
  };
  global.Store = Store;
})(window);
