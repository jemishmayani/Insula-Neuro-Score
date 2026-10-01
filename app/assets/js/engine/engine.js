/* =========================================================================
   Insula Neuro Score — Score engine
   Score data (JSON) ──► engine ──► ResultModel ──► UI
   The engine has no DOM access and no score-specific code.

   Pipeline (calculate):
     1 validate inputs         5 determine result state
     2 component scores        6 interpretation
     3 total / result          7 contextual insights
     4 breakdown               8 limitations (static + contextual)
                               9 related scores
   ========================================================================= */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory(require("./expr.js"), require("./inputs.js"));
  else { root.InsulaEngine = root.InsulaEngine || {}; root.InsulaEngine.engine = factory(root.InsulaEngine.expr, root.InsulaEngine.inputs); }
})(typeof self !== "undefined" ? self : this, function (X, Inputs) {
  "use strict";

  var TONES = ["normal", "low", "mild", "moderate", "high", "critical", "informational", "incomplete", "not-interpretable"];
  var METHODS = ["sum", "expression", "select"];
  var NT_POLICIES = ["block", "exclude"];
  var REQUIRED = ["id", "name", "abbreviation", "category", "subcategory", "specialties", "version", "purpose", "intendedPopulation",
    "components", "inputDefinitions", "scoringRules", "calculationMethod", "interpretationRules", "resultStates", "clinicalInsights",
    "limitations", "confounders", "commonErrors", "whatItDoesNotTellYou", "relatedScores", "guideSections", "sources", "lastReviewed"];
  var RESERVED = ["total", "nt_count", "missing_count", "answered_count"];

  /* ---------------------------------------------------------------------
     Model validation — catches content mistakes before a score can load.
     --------------------------------------------------------------------- */
  function validateScore(s) {
    var e = [];
    if (!s || typeof s !== "object") return ["score is not an object"];
    REQUIRED.forEach(function (k) { if (s[k] == null) e.push("missing field: " + k); });
    if (e.length) return e;
    if (!/^[a-z][a-z0-9-]*$/.test(s.id)) e.push("id must be lower-case: " + s.id);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s.lastReviewed)) e.push("lastReviewed must be YYYY-MM-DD");
    if (!s.version.label) e.push("version.label is required");
    if (!Array.isArray(s.sources) || !s.sources.length) e.push("at least one source is required");

    var ids = {};
    s.inputDefinitions.forEach(function (d) {
      Inputs.validateDefinition(d).forEach(function (m) { e.push(m); });
      if (ids[d.id]) e.push("duplicate input id: " + d.id);
      if (RESERVED.indexOf(d.id) >= 0) e.push("input id is reserved: " + d.id);
      ids[d.id] = "input";
    });
    // components must partition the inputs
    var covered = {};
    s.components.forEach(function (c) {
      if (ids[c.id]) e.push("component id clashes with another id: " + c.id); else ids[c.id] = "component";
      (c.inputs || []).forEach(function (i) {
        if (ids[i] !== "input") e.push("component " + c.id + " references unknown input " + i);
        if (covered[i]) e.push("input " + i + " is in more than one component");
        covered[i] = 1;
      });
    });
    s.inputDefinitions.forEach(function (d) { if (!covered[d.id]) e.push("input " + d.id + " is not in any component"); });

    var known = {}; Object.keys(ids).forEach(function (k) { known[k] = 1; });
    s.inputDefinitions.forEach(function (d) { known[d.id + "_nt"] = 1; known[d.id + "_value"] = 1; known[d.id + "_code"] = 1; });
    RESERVED.forEach(function (k) { known[k] = 1; });
    function checkExpr(src, where) {
      try { X.identifiers(src).forEach(function (id) { if (!known[id]) e.push(where + ": unknown identifier '" + id + "'"); }); }
      catch (err) { e.push(where + ": " + err.message); }
    }
    s.scoringRules.forEach(function (r, i) {
      if (!r.id || !r.expr) { e.push("scoringRules[" + i + "] needs id and expr"); return; }
      if (known[r.id] && RESERVED.indexOf(r.id) < 0) e.push("scoring rule id clashes: " + r.id);
      checkExpr(r.expr, "scoringRules." + r.id); known[r.id] = 1;
    });
    var cm = s.calculationMethod;
    if (METHODS.indexOf(cm.type) < 0) e.push("calculationMethod.type must be one of " + METHODS.join(", "));
    if (cm.type === "expression") { if (!cm.expression) e.push("expression method needs calculationMethod.expression"); else checkExpr(cm.expression, "calculationMethod"); }
    if (cm.type === "select" && ids[cm.input] !== "input") e.push("select method needs a valid calculationMethod.input");
    if (NT_POLICIES.indexOf(cm.notTestablePolicy || "block") < 0) e.push("notTestablePolicy must be block or exclude");
    if (!cm.range || cm.range.min == null || cm.range.max == null) e.push("calculationMethod.range {min,max} is required");
    ["display", "share"].forEach(function (k) {
      if (cm[k]) (cm[k].match(/\{([^{}]+)\}/g) || []).forEach(function (m) { checkExpr(m.slice(1, -1), "calculationMethod." + k); });
    });
    var stateIds = {};
    s.resultStates.forEach(function (st) {
      if (!st.id) e.push("result state needs id");
      if (stateIds[st.id]) e.push("duplicate result state: " + st.id);
      stateIds[st.id] = 1;
      if (TONES.indexOf(st.tone) < 0) e.push("state " + st.id + ": tone must be one of " + TONES.join(", "));
      if (!st.label) e.push("state " + st.id + " needs a label");
    });
    s.interpretationRules.forEach(function (r, i) {
      if (!stateIds[r.state]) e.push("interpretationRules[" + i + "] references unknown state " + r.state);
      if (r.when) checkExpr(r.when, "interpretationRules[" + i + "]");
    });
    if (!s.interpretationRules.length) e.push("at least one interpretation rule is required");
    (s.consistencyRules || []).forEach(function (r, i) {
      checkExpr(r.when, "consistencyRules[" + i + "]");
      if (["warning", "error"].indexOf(r.severity) < 0) e.push("consistencyRules[" + i + "] severity must be warning or error");
    });
    s.clinicalInsights.forEach(function (r, i) { if (r.when) checkExpr(r.when, "clinicalInsights[" + i + "]"); if (!r.text) e.push("clinicalInsights[" + i + "] needs text"); });
    s.limitations.forEach(function (r, i) { if (typeof r === "object" && r.when) checkExpr(r.when, "limitations[" + i + "]"); });
    s.relatedScores.forEach(function (r) { if (!r.id) e.push("related score needs id"); });
    return e;
  }

  /* ---------------------------------------------------------------------
     Calculation
     --------------------------------------------------------------------- */
  function calculate(score, answers) {
    answers = answers || {};
    var cm = score.calculationMethod, policy = cm.notTestablePolicy || "block";
    var R = {
      scoreId: score.id, version: score.version.label, status: "complete",
      total: null, display: "–", range: cm.range, values: {},
      state: null, interpretation: null, breakdown: [],
      errors: [], warnings: [], missing: [], notTestable: [],
      insights: [], limitations: [], related: [], shareText: ""
    };

    /* 1. Validate inputs */
    var norm = {}, vars = {};
    score.inputDefinitions.forEach(function (d) {
      var n = Inputs.normalize(d, answers[d.id]); norm[d.id] = n;
      if (n.status === "invalid") R.errors.push({ inputId: d.id, message: n.error });
      else if (n.status === "empty" && d.required !== false) R.missing.push(d.id);
      else if (n.status === "nt") R.notTestable.push(d.id);
      vars[d.id] = n.status === "ok" ? n.points : null;
      vars[d.id + "_value"] = n.status === "ok" ? n.value : null;
      vars[d.id + "_code"] = n.status === "ok" || n.status === "nt" ? n.code : null;
      vars[d.id + "_nt"] = n.status === "nt";
    });
    vars.nt_count = R.notTestable.length; vars.missing_count = R.missing.length;
    vars.answered_count = score.inputDefinitions.length - R.missing.length;

    /* 2 + 4. Component scores and breakdown */
    var excludeNT = policy === "exclude";
    score.components.forEach(function (c) {
      var items = c.inputs.map(function (id) {
        var d = def(score, id), n = norm[id];
        return { inputId: id, label: d.label, short: d.short || d.label, status: n.status,
          display: n.status === "ok" || n.status === "nt" ? n.label : (n.status === "invalid" ? "Invalid" : "Not entered"),
          code: n.code || null, points: n.status === "ok" ? n.points : null, reason: n.reason || null, error: n.error || null };
      });
      var complete = items.every(function (it) { return it.status === "ok" || (it.status === "nt" && excludeNT) || (it.status === "empty" && def(score, it.inputId).required === false); });
      var subtotal = complete ? items.reduce(function (s, it) { return s + (typeof it.points === "number" ? it.points : 0); }, 0) : null;
      R.breakdown.push({ componentId: c.id, label: c.label, items: items, subtotal: c.showSubtotal === false ? null : subtotal });
      vars[c.id] = subtotal;
    });

    R.insights = pickInsights(score, vars, "always");
    R.related = score.relatedScores.slice();
    R.limitations = pickLimitations(score, vars, false);

    if (R.errors.length) { R.status = "invalid"; return finish(score, R, vars, stateOf("invalid", "Check entries", R.errors.length + " entr" + (R.errors.length === 1 ? "y needs" : "ies need") + " correcting.")); }
    if (R.missing.length) {
      R.status = "incomplete";
      return finish(score, R, vars, stateOf("incomplete", "Incomplete", "Complete " + R.missing.length + " more item" + (R.missing.length === 1 ? "" : "s") + ": " +
        R.missing.map(function (id) { var d = def(score, id); return d.short || d.label; }).join(", ") + "."));
    }
    if (R.notTestable.length && policy === "block") {
      var nt = score.notTestable || {};
      R.status = "not-interpretable";
      R.display = nt.display ? X.template(nt.display, vars) : "–";
      R.insights = R.insights.concat(pickInsights(score, vars, "notTestable"));
      R.limitations = pickLimitations(score, vars, true);
      R.shareText = nt.share ? X.template(nt.share, vars) : score.abbreviation + " not reported (item not testable)";
      return finish(score, R, vars, { id: "not-testable", tone: "not-interpretable", label: nt.label || "Not interpretable as a total",
        summary: nt.summary || "One or more items could not be tested, so a total is not reported.", detail: nt.detail || null });
    }

    /* 3. Total / result */
    if (excludeNT) score.inputDefinitions.forEach(function (d) { if (vars[d.id + "_nt"]) vars[d.id] = 0; });
    score.scoringRules.forEach(function (r) { vars[r.id] = X.evaluate(r.expr, vars); R.values[r.id] = vars[r.id]; });
    var total;
    if (cm.type === "sum") total = score.inputDefinitions.reduce(function (s, d) { return s + (typeof vars[d.id] === "number" ? vars[d.id] : 0); }, 0);
    else if (cm.type === "select") total = vars[cm.input];
    else total = X.evaluate(cm.expression, vars);
    if (typeof total === "number" && !isNaN(total)) total = Math.round(total * 1e6) / 1e6;
    vars.total = total; R.total = total; R.values.total = total;
    if (total == null || (typeof total === "number" && (total < cm.range.min || total > cm.range.max))) {
      R.status = "invalid"; R.errors.push({ inputId: null, message: "Result outside defined range" });
      return finish(score, R, vars, stateOf("invalid", "Calculation error", "The result is outside the score's defined range. Check the inputs and report this score for review."));
    }

    // consistency rules (e.g. instrument rules that tie items together)
    (score.consistencyRules || []).forEach(function (r) {
      if (X.evaluate(r.when, vars)) (r.severity === "error" ? R.errors : R.warnings).push({ message: r.message, inputs: r.inputs || [], inputId: (r.inputs || [])[0] || null });
    });
    if (R.errors.length) { R.status = "invalid"; return finish(score, R, vars, stateOf("invalid", "Check entries", R.errors[0].message)); }

    /* 5. Result state */
    var st = null;
    for (var i = 0; i < score.interpretationRules.length; i++) {
      var rule = score.interpretationRules[i];
      if (!rule.when || X.evaluate(rule.when, vars)) { st = stateById(score, rule.state); break; }
    }
    if (!st) st = { id: "calculated", tone: "informational", label: "Calculated", summary: "" };

    R.display = X.template(cm.display || "{total}", vars);
    if (R.notTestable.length && excludeNT) R.warnings.push({ message: R.notTestable.length + " item" + (R.notTestable.length === 1 ? " was" : "s were") + " untestable and contributed no points. The total may underestimate the deficit.", inputs: R.notTestable.slice() });

    /* 7–8. Contextual insight and limitations */
    R.insights = R.insights.concat(pickInsights(score, vars, "result"));
    R.limitations = pickLimitations(score, vars, true);
    R.shareText = X.template(cm.share || score.abbreviation + " {total}", vars) + (st.label ? " — " + st.label : "") +
      (R.notTestable.length ? " (untestable: " + R.notTestable.map(function (id) { return def(score, id).short || id; }).join(", ") + ")" : "");
    return finish(score, R, vars, st);
  }

  function finish(score, R, vars, st) {
    /* 6. Interpretation */
    var filled = { id: st.id, tone: st.tone, label: X.template(st.label, vars), range: st.range || null,
      summary: st.summary ? X.template(st.summary, vars) : "", detail: st.detail ? X.template(st.detail, vars) : null };
    R.state = filled;
    R.interpretation = { summary: filled.summary, detail: filled.detail };
    return R;
  }
  function stateOf(kind, label, summary) { return { id: kind, tone: "incomplete", label: label, summary: summary }; }
  function stateById(score, id) { for (var i = 0; i < score.resultStates.length; i++) if (score.resultStates[i].id === id) return score.resultStates[i]; return null; }
  function def(score, id) { for (var i = 0; i < score.inputDefinitions.length; i++) if (score.inputDefinitions[i].id === id) return score.inputDefinitions[i]; return null; }
  function pickInsights(score, vars, when) {
    return score.clinicalInsights.filter(function (r) {
      var on = r.on || (r.when ? "result" : "always");
      if (on !== when) return false;
      try { return !r.when || !!X.evaluate(r.when, vars); } catch (e) { return false; }
    }).map(function (r) { return X.template(r.text, vars); });
  }
  function pickLimitations(score, vars, evaluateConditional) {
    var ctx = [], stat = [];
    score.limitations.forEach(function (l) {
      if (typeof l === "string") stat.push({ text: l, contextual: false });
      else if (evaluateConditional && l.when) { try { if (X.evaluate(l.when, vars)) ctx.push({ text: X.template(l.text, vars), contextual: true }); } catch (e) {} }
      else if (!l.when) stat.push({ text: l.text, contextual: false });
    });
    return ctx.concat(stat);
  }

  /** Blank answer set; inputs with a `default` are pre-filled. */
  function initialAnswers(score) {
    var a = {}; score.inputDefinitions.forEach(function (d) { if (d.default !== undefined) a[d.id] = d.default; }); return a;
  }

  return { calculate: calculate, validateScore: validateScore, initialAnswers: initialAnswers, TONES: TONES, METHODS: METHODS, INPUT_TYPES: Inputs.TYPES };
});
