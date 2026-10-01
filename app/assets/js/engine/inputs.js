/* =========================================================================
   Insula Neuro Score — Input types
   Each type turns a raw answer into a normalised value with points, a
   display label and a short code — or reports it as empty or invalid.

   Answer formats (what the UI stores in answers[inputId]):
     single / dropdown / yesno : option value string ("yes"/"no" for yesno)
     multi                     : array of option value strings
     number / integer / decimal: number or numeric string
     measurement               : { value: number|string, unit: unitId }
     any input with notTestable: { nt: true, reason?: string }
   ========================================================================= */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else { root.InsulaEngine = root.InsulaEngine || {}; root.InsulaEngine.inputs = api; }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  function isEmpty(raw) {
    return raw === undefined || raw === null || raw === "" || (Array.isArray(raw) && raw.length === 0) ||
      (typeof raw === "object" && !Array.isArray(raw) && !raw.nt && (raw.value === undefined || raw.value === null || raw.value === ""));
  }
  function empty() { return { status: "empty" }; }
  function invalid(msg) { return { status: "invalid", error: msg }; }
  function ok(o) { o.status = "ok"; return o; }

  function findOption(def, v) {
    for (var i = 0; i < def.options.length; i++) if (String(def.options[i].value) === String(v)) return def.options[i];
    return null;
  }
  function toNumber(raw) {
    if (typeof raw === "number") return raw;
    if (typeof raw !== "string") return NaN;
    var s = raw.trim().replace(",", ".");
    return /^[-+]?(\d+\.?\d*|\.\d+)$/.test(s) ? Number(s) : NaN;
  }
  function decimalsOf(n) { var s = String(n); var i = s.indexOf("."); return i < 0 ? 0 : s.length - i - 1; }
  function bandPoints(def, v) {
    if (!def.pointBands) return v;
    for (var i = 0; i < def.pointBands.length; i++) {
      var b = def.pointBands[i];
      if ((b.min == null || v >= b.min) && (b.max == null || v <= b.max)) return b.points;
    }
    return null;
  }
  function rangeMsg(def, unit) {
    return "Enter a value from " + def.min + " to " + def.max + (unit ? " " + unit : "") + ".";
  }

  /* ---------- choice types ---------- */
  function choice(def, raw) {
    var o = findOption(def, raw);
    if (!o) return invalid("Choose one of the listed options.");
    return ok({ value: o.value, points: o.points == null ? null : o.points, label: o.label, code: o.code != null ? String(o.code) : (o.points != null ? String(o.points) : o.label) });
  }
  function yesno(def, raw) {
    var v = raw === true ? "yes" : raw === false ? "no" : String(raw).toLowerCase();
    if (v !== "yes" && v !== "no") return invalid("Answer yes or no.");
    var pts = def.points || { yes: 1, no: 0 }, labels = def.labels || { yes: "Yes", no: "No" };
    return ok({ value: v, points: pts[v], label: labels[v], code: String(pts[v]) });
  }
  function multi(def, raw) {
    if (!Array.isArray(raw)) return invalid("Select one or more options.");
    var opts = [], seen = {};
    for (var i = 0; i < raw.length; i++) {
      var o = findOption(def, raw[i]);
      if (!o) return invalid("Unknown option selected.");
      if (!seen[o.value]) { seen[o.value] = 1; opts.push(o); }
    }
    var excl = opts.filter(function (o) { return o.exclusive; });
    if (excl.length && opts.length > 1) return invalid("'" + excl[0].label + "' cannot be combined with other options.");
    if (def.minSelected != null && opts.length < def.minSelected) return invalid("Select at least " + def.minSelected + ".");
    if (def.maxSelected != null && opts.length > def.maxSelected) return invalid("Select no more than " + def.maxSelected + ".");
    var pts = def.pointsMode === "count" ? opts.filter(function (o) { return !o.exclusive; }).length
      : opts.reduce(function (s, o) { return s + (o.points || 0); }, 0);
    if (def.maxPoints != null) pts = Math.min(pts, def.maxPoints);
    return ok({ value: opts.map(function (o) { return o.value; }), points: pts, label: opts.map(function (o) { return o.label; }).join(", "), code: String(pts), selected: opts.length });
  }

  /* ---------- numeric types ---------- */
  function numeric(kind) {
    return function (def, raw) {
      var n = toNumber(raw);
      if (isNaN(n)) return invalid("Enter a number.");
      if (kind === "integer" && n % 1 !== 0) return invalid("Enter a whole number.");
      if (kind === "decimal" && def.decimals != null && decimalsOf(n) > def.decimals) return invalid("Use at most " + def.decimals + " decimal place" + (def.decimals === 1 ? "" : "s") + ".");
      if ((def.min != null && n < def.min) || (def.max != null && n > def.max)) return invalid(rangeMsg(def, def.unit));
      var p = bandPoints(def, n);
      return ok({ value: n, points: p, label: n + (def.unit ? " " + def.unit : ""), code: String(p != null ? p : n) });
    };
  }
  function measurement(def, raw) {
    if (!raw || typeof raw !== "object") return invalid("Enter a value.");
    var unit = null;
    for (var i = 0; i < def.units.length; i++) if (def.units[i].id === (raw.unit || def.units[0].id)) unit = def.units[i];
    if (!unit) return invalid("Choose a unit.");
    var n = toNumber(raw.value);
    if (isNaN(n)) return invalid("Enter a number.");
    var canonical = n * (unit.factor == null ? 1 : unit.factor) + (unit.offset || 0);
    canonical = Math.round(canonical * 1e6) / 1e6;
    if ((def.min != null && canonical < def.min) || (def.max != null && canonical > def.max))
      return invalid(rangeMsg(def, def.units[0].label || def.units[0].id) + (unit !== def.units[0] ? " (" + n + " " + (unit.label || unit.id) + " = " + canonical + " " + (def.units[0].label || def.units[0].id) + ")" : ""));
    var p = bandPoints(def, canonical);
    return ok({ value: canonical, points: p, label: n + " " + (unit.label || unit.id) + (unit !== def.units[0] ? " (" + canonical + " " + (def.units[0].label || def.units[0].id) + ")" : ""), code: String(p != null ? p : canonical), unit: unit.id });
  }

  var TYPES = {
    single: choice, dropdown: choice, yesno: yesno, multi: multi,
    number: numeric("number"), integer: numeric("integer"), decimal: numeric("decimal"), measurement: measurement
  };

  /** normalize(def, raw) → {status: 'ok'|'empty'|'invalid'|'nt', value, points, label, code, error} */
  function normalize(def, raw) {
    if (raw && typeof raw === "object" && !Array.isArray(raw) && raw.nt) {
      if (!def.notTestable) return invalid("This item cannot be marked not testable.");
      if (def.notTestable.requireReason && !(raw.reason && String(raw.reason).trim())) return invalid("Give a reason why this item is not testable.");
      if (raw.reason && Array.isArray(def.notTestable.reasons) && def.notTestable.reasons.indexOf(raw.reason) < 0) return invalid("Not testable is allowed only for: " + def.notTestable.reasons.join(", ") + ".");
      return { status: "nt", value: null, points: null, label: def.notTestable.label || "Not testable", code: def.notTestable.code || "NT", reason: raw.reason || null };
    }
    if (isEmpty(raw)) return empty();
    var fn = TYPES[def.type];
    if (!fn) return invalid("Unsupported input type: " + def.type);
    return fn(def, raw);
  }

  /** Schema checks for a single input definition (used by the model validator). */
  function validateDefinition(def) {
    var e = [];
    if (!def.id || !/^[a-z][a-z0-9_]*$/.test(def.id)) e.push("input id must be lower_snake_case: " + def.id);
    if (!TYPES[def.type]) e.push(def.id + ": unknown type " + def.type);
    if (["single", "dropdown", "multi"].indexOf(def.type) >= 0) {
      if (!Array.isArray(def.options) || def.options.length < 2) e.push(def.id + ": needs at least 2 options");
      else {
        var vals = def.options.map(function (o) { return String(o.value); });
        if (vals.some(function (v, i) { return vals.indexOf(v) !== i; })) e.push(def.id + ": duplicate option values");
      }
    }
    if (["number", "integer", "decimal"].indexOf(def.type) >= 0 && (def.min == null || def.max == null)) e.push(def.id + ": numeric inputs need min and max");
    if (def.type === "measurement" && !(Array.isArray(def.units) && def.units.length)) e.push(def.id + ": measurement needs units");
    if (def.type === "measurement" && (def.min == null || def.max == null)) e.push(def.id + ": measurement needs min and max (canonical unit)");
    return e;
  }

  return { normalize: normalize, validateDefinition: validateDefinition, TYPES: Object.keys(TYPES), isEmpty: isEmpty };
});
