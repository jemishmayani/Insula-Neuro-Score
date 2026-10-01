/* =========================================================================
   Insula Neuro Score — UI component library
   Every screen is composed from these functions. Components never contain
   colour values; tone is expressed through semantic classes (tone-*).
   ========================================================================= */
(function (global) {
  "use strict";

  function esc(s) {
    return s == null ? "" : String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function attrs(o) {
    if (!o) return "";
    return Object.keys(o).filter(function (k) { return o[k] != null && o[k] !== false; })
      .map(function (k) { return o[k] === true ? " " + k : " " + k + '="' + esc(o[k]) + '"'; }).join("");
  }

  /* ---------------- Icons ---------------- */
  function svg(paths, cls) {
    return '<svg class="icon' + (cls ? " " + cls : "") + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + paths + "</svg>";
  }
  var P = {
    home: '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    calculate: '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
    guide: '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M9 7h6M9 11h6"/>',
    settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-2.8 1.2V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-2.9-1.2l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0-1.2-2.9H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.2-2.9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 2.9-1.2V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 2.9 1.2l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0 1.2 2.9H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    star: '<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>',
    pin: '<path d="M9 4h6l-1 6 4 3v2H6v-2l4-3z"/><path d="M12 15v6"/>',
    chevron: '<path d="M9 6l6 6-6 6"/>',
    back: '<path d="M15 6l-6 6 6 6"/>',
    close: '<path d="M6 6l12 12M18 6L6 18"/>',
    up: '<path d="M6 15l6-6 6 6"/>',
    down: '<path d="M6 9l6 6 6-6"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.6v.2"/>',
    warning: '<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5M12 17.3v.2"/>',
    error: '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>',
    inbox: '<path d="M3 13l3-8h12l3 8v6H3z"/><path d="M3 13h5l1 2h6l1-2h5"/>',
    reset: '<path d="M4 12a8 8 0 1 0 2.3-5.7"/><path d="M4 4v4h4"/>',
    /* category glyphs */
    consciousness: '<circle cx="12" cy="12" r="3"/><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/>',
    stroke: '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    ich: '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    sah: '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M9 14h6"/>',
    tbi: '<path d="M12 3a8 8 0 0 0-8 8v3l-1 3h3v3h5l1-2"/><path d="M14 9l-2 3h3l-2 3"/>',
    spine: '<rect x="9" y="2" width="6" height="4" rx="1"/><rect x="9" y="8" width="6" height="4" rx="1"/><rect x="9" y="14" width="6" height="4" rx="1"/><path d="M12 18v4"/>',
    oncology: '<circle cx="12" cy="12" r="4"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M5 19l3-3M16 8l3-3"/>',
    functional: '<circle cx="12" cy="5" r="2"/><path d="M12 7v6l-3 8M12 13l3 8M7 10h10"/>',
    icu: '<path d="M3 12h4l2-5 4 10 2-5h6"/>'
  };
  var STATE_ICON = {
    normal: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.8"/>',
    success: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.8"/>',
    low: '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.7 2.7L16 9.8"/>',
    mild: '<circle cx="12" cy="12" r="9"/><path d="M8 12h8"/>',
    warning: P.warning,
    moderate: P.warning,
    high: '<path d="M8.2 2.8h7.6l5.4 5.4v7.6l-5.4 5.4H8.2l-5.4-5.4V8.2z"/><path d="M12 7.5v6M12 16.5v.2"/>',
    concern: '<path d="M8.2 2.8h7.6l5.4 5.4v7.6l-5.4 5.4H8.2l-5.4-5.4V8.2z"/><path d="M12 7.5v6M12 16.5v.2"/>',
    critical: '<path d="M8.2 2.8h7.6l5.4 5.4v7.6l-5.4 5.4H8.2l-5.4-5.4V8.2z" fill="currentColor"/><path d="M12 7.5v6M12 16.5v.2" stroke="var(--color-surface)" stroke-width="2.4"/>',
    error: P.error,
    info: P.info,
    incomplete: '<circle cx="12" cy="12" r="9" stroke-dasharray="3 3"/><path d="M8.5 12h.1M12 12h.1M15.5 12h.1"/>',
    neutral: '<circle cx="12" cy="12" r="9" stroke-dasharray="3 3"/>',
    primary: P.info
  };
  function icon(name, cls) { return svg(P[name] || STATE_ICON[name] || P.info, cls); }
  function stateIcon(tone) { return svg(STATE_ICON[tone] || STATE_ICON.info); }

  var TONE_LABEL = { normal: "Normal / low concern", low: "Low concern", mild: "Mild", moderate: "Moderate", high: "High concern",
    critical: "Very high concern", info: "Informational", incomplete: "Incomplete", success: "Success", warning: "Warning",
    concern: "High concern", error: "Error", neutral: "Neutral", primary: "Primary" };

  /* ---------------- Components ---------------- */

  /** AppBar({title, back, brand, actions: [html]}) */
  function AppBar(o) {
    return '<header class="appbar' + (o.back ? " has-back" : "") + '">' +
      (o.back ? IconButton({ icon: "back", label: "Back", act: "back" }) : "") +
      '<h1 class="appbar-title">' + (o.brand ? '<img class="appbar-mark" src="img/mark.png" alt="">' : "") + "<span>" + esc(o.title) + "</span></h1>" +
      (o.actions || []).join("") + "</header>";
  }

  /** IconButton({icon, label, act, href, pressed, data}) — 48dp target, always labelled */
  function IconButton(o) {
    var a = { "class": "icon-button", "aria-label": o.label, "data-act": o.act, "aria-pressed": o.pressed == null ? null : String(!!o.pressed), disabled: o.disabled };
    if (o.data) Object.keys(o.data).forEach(function (k) { a["data-" + k] = o.data[k]; });
    if (o.href) { a.href = o.href; a["data-nav"] = true; delete a.disabled; return "<a" + attrs(a) + ">" + icon(o.icon) + "</a>"; }
    a.type = "button";
    return "<button" + attrs(a) + ">" + icon(o.icon) + "</button>";
  }

  /** BottomNavigation({active, items:[{id,label,icon,href}]}) — rail on wide/landscape via CSS */
  function BottomNavigation(o) {
    return '<nav class="bottomnav" aria-label="Main">' + o.items.map(function (it) {
      return '<a href="' + esc(it.href) + '" data-nav data-tab="' + esc(it.id) + '"' + (o.active === it.id ? ' aria-current="page"' : "") + '>' +
        '<span class="indicator">' + icon(it.icon) + "</span>" + esc(it.label) + "</a>";
    }).join("") + "</nav>";
  }

  /** SearchBar({id, placeholder, value, label}) */
  function SearchBar(o) {
    return '<div class="searchbar" role="search">' + icon("search", "search-icon") +
      '<label class="vh" for="' + esc(o.id) + '">' + esc(o.label || "Search") + "</label>" +
      '<input id="' + esc(o.id) + '" type="search" enterkeyhint="search" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="' + esc(o.placeholder) + '" value="' + esc(o.value || "") + '">' +
      '<span class="clear"' + (o.value ? "" : " hidden") + ">" + IconButton({ icon: "close", label: "Clear search", act: "clear-search", data: { for: o.id } }) + "</span></div>";
  }

  /** StatusBadge({tone, label, icon}) — icon + text, never colour alone */
  function StatusBadge(o) {
    return '<span class="status-badge tone-' + esc(o.tone) + '">' + (o.icon === false ? "" : stateIcon(o.tone)) + esc(o.label || TONE_LABEL[o.tone]) + "</span>";
  }

  /** ScoreCard({score, href, sub, badge, favorite, trailing}) — list row (render inside CardList) */
  function ScoreCard(o) {
    var s = o.score;
    var fav = o.favorite == null ? "" : IconButton({ icon: "star", label: (o.favorite ? "Remove " : "Add ") + s.abbreviation + (o.favorite ? " from favourites" : " to favourites"), act: "toggle-favorite", pressed: o.favorite, data: { id: s.id } });
    return '<li class="score-card"><a class="open" href="' + esc(o.href) + '" data-nav><span class="text"><span class="title">' + esc(s.abbreviation) +
      (o.badge ? " " + o.badge : "") + '</span><span class="sub">' + esc(o.sub != null ? o.sub : s.name) + "</span></span>" + icon("chevron", "chev") + "</a>" + fav + (o.trailing || "") + "</li>";
  }
  function CardList(items, label) { return '<ul class="card-list"' + (label ? ' aria-label="' + esc(label) + '"' : "") + ">" + items.join("") + "</ul>"; }

  /** CategoryCard({category, href, count}) */
  function CategoryCard(o) {
    var c = o.category;
    return '<a class="category-card" href="' + esc(o.href) + '" data-nav><span class="glyph">' + icon(c.glyph) + '</span><span class="text"><span class="name">' + esc(c.name) +
      '</span><span class="count">' + o.count + " score" + (o.count === 1 ? "" : "s") + (c.description ? " · " + esc(c.description) : "") + "</span></span>" + icon("chevron", "chev") + "</a>";
  }

  /** ResultCard({tone, value, meta, summary, detail, label}) */
  function ResultCard(o) {
    var isText = /[A-Za-z]/.test(String(o.value)) && String(o.value).length > 5;
    return '<section class="result-card tone-' + esc(o.tone) + '" aria-live="polite" aria-label="Result"><div class="state">' + stateIcon(o.tone) + "<span>" + esc(o.label || TONE_LABEL[o.tone]) + "</span></div>" +
      '<div class="value' + (isText ? " text" : "") + '">' + esc(o.value) + "</div>" + (o.meta ? '<div class="meta">' + esc(o.meta) + "</div>" : "") +
      (o.summary ? '<p class="summary">' + esc(o.summary) + "</p>" : "") + (o.detail ? '<p class="detail">' + esc(o.detail) + "</p>" : "") + "</section>";
  }

  /** SectionCard({id, number, title, body(html)}) */
  function SectionCard(o) {
    return '<section class="section-card"' + (o.id ? ' id="' + esc(o.id) + '"' : "") + "><h3>" + (o.number != null ? '<span class="num">' + o.number + "</span>" : "") + esc(o.title) + "</h3>" + (o.body || "") + "</section>";
  }

  /** PrimaryButton / SecondaryButton({label, icon, href, act, block, disabled, data}) */
  function Button(kind, o) {
    var a = { "class": "btn btn-" + kind + (o.block ? " btn-block" : ""), "data-act": o.act };
    if (o.data) Object.keys(o.data).forEach(function (k) { a["data-" + k] = o.data[k]; });
    var inner = (o.icon ? icon(o.icon) : "") + "<span>" + esc(o.label) + "</span>";
    if (o.href) { a.href = o.href; a["data-nav"] = !o.replace; a["data-replace"] = o.replace; if (o.disabled) a["aria-disabled"] = "true"; return "<a" + attrs(a) + ">" + inner + "</a>"; }
    a.type = "button"; a.disabled = o.disabled;
    return "<button" + attrs(a) + ">" + inner + "</button>";
  }
  function PrimaryButton(o) { return Button("primary", o); }
  function SecondaryButton(o) { return Button("secondary", o); }

  /** Toggle({id, label, description, checked, act, data}) — switch with full-row label */
  function Toggle(o) {
    var a = { type: "checkbox", id: o.id, role: "switch", "data-act": o.act, checked: !!o.checked, "aria-describedby": o.description ? o.id + "-d" : null };
    if (o.data) Object.keys(o.data).forEach(function (k) { a["data-" + k] = o.data[k]; });
    return '<div class="toggle-row"><label class="text" for="' + esc(o.id) + '"><span class="label">' + esc(o.label) + "</span>" +
      (o.description ? '<span class="desc" id="' + esc(o.id) + '-d">' + esc(o.description) + "</span>" : "") + "</label>" +
      '<span class="toggle"><input' + attrs(a) + '><span class="track"></span></span></div>';
  }

  /** Segmented({label, options:[{value,label,icon}], value, act, key}) */
  function Segmented(o) {
    return '<div class="segmented" role="group" aria-label="' + esc(o.label) + '">' + o.options.map(function (op) {
      return '<button type="button" data-act="' + esc(o.act) + '" data-key="' + esc(o.key || "") + '" data-value="' + esc(op.value) + '" aria-pressed="' + (o.value === op.value) + '">' + (op.icon ? icon(op.icon) : "") + esc(op.label) + "</button>";
    }).join("") + "</div>";
  }

  /** EmptyState({icon, title, message, action(html), compact}) */
  function EmptyState(o) {
    return '<div class="empty-state' + (o.compact ? " compact" : "") + '"><span class="glyph">' + icon(o.icon || "inbox") + "</span><div>" +
      "<h3>" + esc(o.title) + "</h3>" + (o.message ? "<p>" + esc(o.message) + "</p>" : "") + (o.action || "") + "</div></div>";
  }

  /** InfoBanner / WarningBanner({title, message}) */
  function Banner(tone, iconName, o) {
    return '<div class="banner tone-' + tone + '" role="' + (tone === "warning" ? "note" : "note") + '">' + icon(iconName) + '<div class="text">' +
      (o.title ? "<b>" + esc(o.title) + "</b>" : "") + esc(o.message || "") + "</div></div>";
  }
  function InfoBanner(o) { return Banner("info", "info", o); }
  function WarningBanner(o) { return Banner("warning", "warning", o); }

  /** ErrorState({title, message, action(html)}) */
  function ErrorState(o) {
    return '<div class="error-state" role="alert"><span class="glyph">' + icon("error") + "</span><h3>" + esc(o.title) + "</h3>" +
      (o.message ? "<p>" + esc(o.message) + "</p>" : "") + (o.action || "") + "</div>";
  }

  /** LoadingState({message, rows}) */
  function LoadingState(o) {
    o = o || {};
    var rows = ""; for (var i = 0; i < (o.rows || 0); i++) rows += "<i></i>";
    return '<div class="loading-state" role="status" aria-live="polite"><div class="spinner" aria-hidden="true"></div>' + esc(o.message || "Loading…") +
      (rows ? '<div class="skeleton" aria-hidden="true">' + rows + "</div>" : "") + "</div>";
  }

  /** Section({title, action(html), body(html), id}) — titled page section */
  function Section(o) {
    return '<section class="section"' + (o.id ? ' id="' + esc(o.id) + '"' : "") + ' aria-labelledby="' + esc(o.id || o.title) + '-h"><div class="section-head"><h2 class="section-title" id="' + esc(o.id || o.title) + '-h">' + esc(o.title) + "</h2>" + (o.action || "") + "</div>" + o.body + "</section>";
  }

  global.UI = { esc: esc, icon: icon, stateIcon: stateIcon, TONE_LABEL: TONE_LABEL,
    AppBar: AppBar, IconButton: IconButton, BottomNavigation: BottomNavigation, SearchBar: SearchBar, StatusBadge: StatusBadge,
    ScoreCard: ScoreCard, CardList: CardList, CategoryCard: CategoryCard, ResultCard: ResultCard, SectionCard: SectionCard,
    PrimaryButton: PrimaryButton, SecondaryButton: SecondaryButton, Toggle: Toggle, Segmented: Segmented,
    EmptyState: EmptyState, InfoBanner: InfoBanner, WarningBanner: WarningBanner, ErrorState: ErrorState, LoadingState: LoadingState, Section: Section };
})(window);
