/* Insula Neuro Score — Score Engine
 * Scores are pure data (content/scores/*.json). This engine:
 *  1. resolves inputs (choice / number) into variables,
 *  2. evaluates derived values with a small, safe expression language (no eval),
 *  3. selects the first matching result state, conditional insights, and a share summary.
 */
(function (global) {
  "use strict";

  /* ---------- Safe expression language ----------
   * Numbers, identifiers, true/false/null, + - * / %, comparisons, == !=, && || !, ?:, ( ),
   * and whitelisted functions. Any null operand in arithmetic yields null.            */
  var FUNCS = {
    min: Math.min, max: Math.max, abs: Math.abs, round: Math.round, floor: Math.floor, ceil: Math.ceil,
    clamp: function (x, a, b) { return x == null ? null : Math.max(a, Math.min(b, x)); },
    between: function (x, a, b) { return x != null && x >= a && x <= b; },
    roman: function (n) { return ["0", "I", "II", "III", "IV", "V", "VI"][n] || String(n); },
    signed: function (n) { return n == null ? "" : (n > 0 ? "+" + n : String(n)); },
    isnull: function (x) { return x == null; }
  };

  function tokenize(src) {
    var t = [], i = 0, m;
    var re = /\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(&&|\|\||==|!=|<=|>=|[-+*/%<>!?:(),])|'([^']*)')/y;
    while (i < src.length) {
      re.lastIndex = i;
      m = re.exec(src);
      if (!m) { if (/^\s*$/.test(src.slice(i))) break; throw new Error("Bad token at " + i + " in: " + src); }
      if (m[1] != null) t.push({ k: "num", v: parseFloat(m[1]) });
      else if (m[2] != null) t.push({ k: "id", v: m[2] });
      else if (m[3] != null) t.push({ k: "op", v: m[3] });
      else if (m[4] != null) t.push({ k: "str", v: m[4] });
      i = re.lastIndex;
    }
    return t;
  }

  function parse(src) {
    var t = tokenize(src), p = 0;
    function peek(v) { return t[p] && t[p].k === "op" && t[p].v === v; }
    function eat(v) { if (!peek(v)) throw new Error("Expected " + v + " in: " + src); p++; }
    function ternary() {
      var c = or();
      if (peek("?")) { p++; var a = ternary(); eat(":"); var b = ternary(); return { k: "?", c: c, a: a, b: b }; }
      return c;
    }
    function bin(next, ops) {
      return function () {
        var l = next();
        while (t[p] && t[p].k === "op" && ops.indexOf(t[p].v) >= 0) { var o = t[p++].v; l = { k: "bin", o: o, l: l, r: next() }; }
        return l;
      };
    }
    function unary() {
      if (peek("!")) { p++; return { k: "not", e: unary() }; }
      if (peek("-")) { p++; return { k: "neg", e: unary() }; }
      return primary();
    }
    var mul = bin(unary, ["*", "/", "%"]), add = bin(mul, ["+", "-"]), cmp = bin(add, ["<", ">", "<=", ">="]),
        eq = bin(cmp, ["==", "!="]), and = bin(eq, ["&&"]), or = bin(and, ["||"]);
    function primary() {
      var tk = t[p++];
      if (!tk) throw new Error("Unexpected end in: " + src);
      if (tk.k === "num" || tk.k === "str") return { k: "num", v: tk.v };
      if (tk.k === "id") {
        if (tk.v === "true") return { k: "num", v: true };
        if (tk.v === "false") return { k: "num", v: false };
        if (tk.v === "null") return { k: "num", v: null };
        if (peek("(")) {
          p++; var args = [];
          if (!peek(")")) { args.push(ternary()); while (peek(",")) { p++; args.push(ternary()); } }
          eat(")");
          if (!Object.prototype.hasOwnProperty.call(FUNCS, tk.v)) throw new Error("Unknown function " + tk.v);
          return { k: "call", f: tk.v, a: args };
        }
        return { k: "var", v: tk.v };
      }
      if (tk.k === "op" && tk.v === "(") { var e = ternary(); eat(")"); return e; }
      throw new Error("Unexpected token in: " + src);
    }
    var ast = ternary();
    if (p !== t.length) throw new Error("Trailing tokens in: " + src);
    return ast;
  }

  var cache = Object.create(null);
  function evaluate(src, vars) {
    var ast = cache[src] || (cache[src] = parse(src));
    return run(ast, vars);
  }
  function run(n, v) {
    switch (n.k) {
      case "num": return n.v;
      case "var": return Object.prototype.hasOwnProperty.call(v, n.v) ? v[n.v] : null;
      case "not": return !run(n.e, v);
      case "neg": var x = run(n.e, v); return x == null ? null : -x;
      case "?": return run(n.c, v) ? run(n.a, v) : run(n.b, v);
      case "call": return FUNCS[n.f].apply(null, n.a.map(function (a) { return run(a, v); }));
      case "bin":
        if (n.o === "&&") return run(n.l, v) && run(n.r, v);
        if (n.o === "||") return run(n.l, v) || run(n.r, v);
        var l = run(n.l, v), r = run(n.r, v);
        if (n.o === "==") return l === r;
        if (n.o === "!=") return l !== r;
        if (l == null || r == null) return n.o.match(/[<>]/) ? false : null;
        switch (n.o) {
          case "+": return l + r; case "-": return l - r; case "*": return l * r;
          case "/": return r === 0 ? null : l / r; case "%": return l % r;
          case "<": return l < r; case ">": return l > r; case "<=": return l <= r; case ">=": return l >= r;
        }
    }
    throw new Error("Bad node");
  }

  function fill(tpl, vars) {
    return String(tpl).replace(/\{([^{}]+)\}/g, function (_, e) {
      var r = evaluate(e, vars);
      return r == null ? "–" : String(r);
    });
  }

  /* ---------- Score validation (catches content mistakes at load time) ---------- */
  var STATES = ["normal", "low", "mild", "moderate", "high", "critical", "info", "incomplete"];
  function validate(score) {
    var errs = [];
    ["id", "name", "abbreviation", "category", "version", "inputs", "values", "primary", "states", "sources", "lastReviewed"].forEach(function (k) {
      if (score[k] == null) errs.push("missing " + k);
    });
    (score.inputs || []).forEach(function (inp) {
      if (inp.type === "choice" && !(inp.options && inp.options.length)) errs.push(inp.id + ": no options");
      if (inp.type === "number" && (inp.min == null || inp.max == null)) errs.push(inp.id + ": number needs min/max");
    });
    var probe = {};
    (score.inputs || []).forEach(function (i) { probe[i.id] = 1; });
    try {
      (score.values || []).forEach(function (d) { parse(d.expr); probe[d.id] = 1; });
      (score.states || []).forEach(function (s) { if (s.when) parse(s.when); if (STATES.indexOf(s.state) < 0) errs.push("bad state " + s.state); });
      (score.insights || []).forEach(function (s) { if (s.when) parse(s.when); });
    } catch (e) { errs.push(e.message); }
    return errs;
  }

  /* ---------- Calculation ---------- */
  function calculate(score, answers) {
    var vars = {}, missing = [], nt = [], breakdown = [];
    score.inputs.forEach(function (inp) {
      var a = answers[inp.id], item = { id: inp.id, label: inp.label, short: inp.short || inp.label };
      if (inp.type === "choice") {
        var opt = null;
        for (var i = 0; i < inp.options.length; i++) if (String(inp.options[i].value) === String(a)) opt = inp.options[i];
        if (!opt) { missing.push(inp); vars[inp.id] = null; item.missing = true; }
        else {
          item.choice = opt.label; item.code = opt.code;
          if (opt.nt) { nt.push(inp); vars[inp.id] = null; item.nt = true; item.points = null; }
          else { vars[inp.id] = opt.points; item.points = opt.points; }
        }
      } else if (inp.type === "number") {
        var n = (a === "" || a == null) ? NaN : Number(a);
        if (isNaN(n) || n < inp.min || n > inp.max || (inp.integer && n % 1 !== 0)) { missing.push(inp); vars[inp.id] = null; item.missing = true; item.invalid = a != null && a !== ""; }
        else { vars[inp.id] = n; item.points = n; item.choice = n + (inp.unit ? " " + inp.unit : ""); }
      }
      breakdown.push(item);
    });

    var res = { breakdown: breakdown, missing: missing, nt: nt, vars: vars, insights: [] };

    if (missing.length) {
      res.state = { state: "incomplete", label: "Incomplete", summary: "Complete " + missing.map(function (m) { return m.short || m.label; }).join(", ") + " to see the result." };
      res.display = "–";
      return res;
    }
    if (nt.length) {
      var pol = score.notTestable || {};
      res.state = { state: "incomplete", label: pol.label || "Not interpretable as a total",
        summary: pol.summary || "One or more components could not be tested.", detail: pol.detail };
      res.display = pol.display ? fill(pol.display, codeVars(score, answers, vars)) : "–";
      res.share = pol.share ? fill(pol.share, codeVars(score, answers, vars)) : null;
      res.insights = pickInsights(score, vars, true);
      return res;
    }
    score.values.forEach(function (d) { vars[d.id] = evaluate(d.expr, vars); });
    var cv = codeVars(score, answers, vars);
    for (var s = 0; s < score.states.length; s++) {
      var st = score.states[s];
      if (!st.when || evaluate(st.when, vars)) { res.state = st; break; }
    }
    if (!res.state) res.state = { state: "info", label: "Calculated", summary: "" };
    res.display = fill(score.display || "{" + score.primary + "}", cv);
    res.share = fill(score.share || score.abbreviation + " {" + score.primary + "}", cv) + (res.state.label ? " — " + res.state.label : "");
    res.insights = pickInsights(score, vars, false);
    res.primaryValue = vars[score.primary];
    return res;
  }
  // Exposes option codes (e.g. "E2", "VNT") as variables named <inputId>_code for templates.
  function codeVars(score, answers, vars) {
    var cv = Object.assign({}, vars);
    score.inputs.forEach(function (inp) {
      if (inp.type !== "choice") return;
      inp.options.forEach(function (o) { if (String(o.value) === String(answers[inp.id])) cv[inp.id + "_code"] = o.code || o.points; });
    });
    return cv;
  }
  function pickInsights(score, vars, ntMode) {
    return (score.insights || []).filter(function (i) {
      if (ntMode && !i.whenNotTestable) return false;
      if (!ntMode && i.whenNotTestable) return false;
      if (!i.when) return true;
      try { return !!evaluate(i.when, vars); } catch (e) { return false; }
    });
  }

  global.ScoreEngine = { evaluate: evaluate, fill: fill, calculate: calculate, validate: validate, STATES: STATES };
})(window);
