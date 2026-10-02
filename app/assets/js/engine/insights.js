/* =========================================================================
   Insula Neuro Score — Clinical insight engine
   Turns a score's structured insight content into an ordered InsightSet.
   No free text is generated: every item comes from validated score data.

   Insight types (fixed order):
     interpretation · context · consideration · limitation · confounder · boundary
   Item shape (in score JSON):
     { id?, text, title?, importance?: "major"|"standard", when?: expr, on?: "always"|"result"|"notTestable",
       guideText?, factor?, effect? }   (confounders use factor + effect)
   ========================================================================= */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("./expr.js"));
  else { root.InsulaEngine = root.InsulaEngine || {}; root.InsulaEngine.insights = factory(root.InsulaEngine.expr); }
})(typeof self !== "undefined" ? self : this, function (X) {
  "use strict";

  /** Section definitions: score field → insight type, heading, question it answers. */
  var SECTIONS = [
    { type: "context", field: "clinicalContext", title: "Clinical context", question: "What does this score help describe?" },
    { type: "consideration", field: "clinicalInsights", title: "Important considerations", question: "What else should the clinician consider?" },
    { type: "limitation", field: "limitations", title: "Limitations", question: "What can make this score misleading?" },
    { type: "confounder", field: "confounders", title: "Confounders", question: "What factors interfere with calculation?" },
    { type: "boundary", field: "whatItDoesNotTellYou", title: "What it does not tell you", question: "Where does interpretation stop?" }
  ];
  var IMPORTANCE = ["major", "standard"];

  /** Result types and the tones each may use (no score is forced into a severity scale). */
  var PRESENTATIONS = {
    "severity":               { label: "Severity", tones: ["favorable", "low", "mild", "moderate", "high", "critical", "informational"],
                                describes: "Where this result sits on the score's own severity scale." },
    "deficit":                { label: "Measured deficit", tones: ["favorable", "informational"],
                                describes: "The amount of deficit measured on the score's items. It has no official severity categories." },
    "classification":         { label: "Classification", tones: ["favorable", "low", "mild", "moderate", "high", "informational"],
                                describes: "The category that the findings fall into." },
    "functional-status":      { label: "Functional status", tones: ["favorable", "informational"],
                                describes: "Level of function or dependence in daily life, not neurological severity." },
    "disability":             { label: "Disability", tones: ["favorable", "informational"],
                                describes: "Degree of disability; not a measure of the underlying condition's severity." },
    "stability":              { label: "Stability", tones: ["favorable", "low", "moderate", "high"],
                                describes: "Mechanical stability category; not a treatment decision." },
    "imaging-classification": { label: "Imaging classification", tones: ["favorable", "low", "mild", "moderate", "high", "informational"],
                                describes: "A category assigned from imaging findings." },
    "prognostic-category":    { label: "Prognostic category", tones: ["favorable", "low", "mild", "moderate", "high", "critical", "informational"],
                                describes: "A group-level association with outcome in the derivation data; not an individual prediction." },
    "informational":          { label: "Informational", tones: ["favorable", "informational"], describes: "Descriptive information." }
  };

  function normalize(item, type) {
    var o = typeof item === "string" ? { text: item } : Object.assign({}, item);
    o.type = type;
    o.importance = o.importance || "standard";
    if (type === "confounder" && !o.text && o.factor) o.text = o.factor + (o.effect ? ": " + o.effect : "");
    return o;
  }
  function ordered(items) {
    var rank = function (i) { return (i.contextual ? 0 : 2) + (i.importance === "major" ? 0 : 1); };
    return items.map(function (x, i) { return [x, i]; }).sort(function (a, b) { return rank(a[0]) - rank(b[0]) || a[1] - b[1]; }).map(function (p) { return p[0]; });
  }

  /** Validate insight content; returns error strings. `known` = identifiers the score defines. */
  function validate(score, checkExpr) {
    var e = [];
    SECTIONS.forEach(function (sec) {
      var list = score[sec.field];
      if (!Array.isArray(list)) { e.push(sec.field + " must be an array"); return; }
      list.forEach(function (raw, i) {
        var it = normalize(raw, sec.type), where = sec.field + "[" + i + "]";
        if (!it.text || !String(it.text).trim()) e.push(where + " needs text");
        if (IMPORTANCE.indexOf(it.importance) < 0) e.push(where + " importance must be major or standard");
        if (it.on && ["always", "result", "notTestable"].indexOf(it.on) < 0) e.push(where + " 'on' must be always, result or notTestable");
        if (it.when) checkExpr(it.when, where);
        (String(it.text).match(/\{([^{}]+)\}/g) || []).forEach(function (m) { checkExpr(m.slice(1, -1), where + " template"); });
        if (/\{/.test(it.text) && !it.when) e.push(where + ": templated text must be conditional (when)");
        if (sec.type === "confounder" && typeof raw === "object" && raw.factor && !raw.effect) e.push(where + " confounder needs effect");
      });
    });
    var pres = score.resultPresentation;
    if (pres && PRESENTATIONS[pres.type]) {
      var allowed = PRESENTATIONS[pres.type].tones;
      (score.resultStates || []).forEach(function (st) {
        if (allowed.indexOf(st.tone) < 0) e.push("state " + st.id + ": tone '" + st.tone + "' is not used for " + pres.type + " results (allowed: " + allowed.join(", ") + ")");
      });
    }
    return e;
  }

  /**
   * Build the InsightSet for a calculated result.
   * mode: "result" (complete), "notTestable", or "pending" (incomplete/invalid: general items only)
   */
  function build(score, vars, mode) {
    var sections = SECTIONS.map(function (sec) {
      var items = [];
      (score[sec.field] || []).forEach(function (raw) {
        var it = normalize(raw, sec.type), on = it.on || (it.when ? "result" : "always");
        if (on === "notTestable" && mode !== "notTestable") return;
        if (on === "result" && mode !== "result") return;
        if (it.when) {
          var hit = false; try { hit = !!X.evaluate(it.when, vars); } catch (err) { hit = false; }
          if (!hit) return;
          it.contextual = true;
        }
        it.text = X.template(it.text, vars);
        items.push(it);
      });
      return { type: sec.type, title: sec.title, question: sec.question, items: ordered(items) };
    });
    return { sections: sections };
  }

  /** Guide view: every item, conditional ones marked "applies when…" (guideText or untemplated text). */
  function forGuide(score) {
    return SECTIONS.map(function (sec) {
      var items = (score[sec.field] || []).map(function (raw) { return normalize(raw, sec.type); }).filter(function (it) { return it.guideText || !/\{/.test(it.text); })
        .map(function (it) { var o = Object.assign({}, it); if (it.guideText) o.text = it.guideText; o.conditional = !!it.when; return o; });
      items.sort(function (a, b) { return (a.importance === "major" ? 0 : 1) - (b.importance === "major" ? 0 : 1); });
      return { type: sec.type, title: sec.title, question: sec.question, items: items };
    });
  }

  function presentation(score) {
    var p = score.resultPresentation; if (!p) return null;
    var def = PRESENTATIONS[p.type] || {};
    return { type: p.type, typeLabel: p.typeLabel || def.label, meter: !!p.meter, describes: p.describes || def.describes };
  }

  return { SECTIONS: SECTIONS, PRESENTATIONS: PRESENTATIONS, IMPORTANCE: IMPORTANCE, build: build, forGuide: forGuide, validate: validate, presentation: presentation, normalize: normalize };
});
