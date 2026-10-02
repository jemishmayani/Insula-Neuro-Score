/* =========================================================================
   Insula Neuro Score — Expression language
   Used by score data for scoring rules, interpretation rules and insights.
   Recursive-descent parser; no eval, no Function, no access to globals.

   Grammar: numbers, 'strings', true/false/null, identifiers (variables),
   + - * / %, < > <= >=, == !=, && || !, cond ? a : b, ( ), and the
   whitelisted functions below. Arithmetic with null yields null;
   comparisons with null yield false.
   ========================================================================= */
(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else { root.InsulaEngine = root.InsulaEngine || {}; root.InsulaEngine.expr = api; }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  var has = Object.prototype.hasOwnProperty;

  var FUNCS = {
    min: function () { var a = [].slice.call(arguments); return a.some(isNull) ? null : Math.min.apply(null, a); },
    max: function () { var a = [].slice.call(arguments); return a.some(isNull) ? null : Math.max.apply(null, a); },
    abs: function (x) { return isNull(x) ? null : Math.abs(x); },
    round: function (x, dp) { if (isNull(x)) return null; var f = Math.pow(10, dp || 0); return Math.round(x * f) / f; },
    floor: function (x) { return isNull(x) ? null : Math.floor(x); },
    ceil: function (x) { return isNull(x) ? null : Math.ceil(x); },
    clamp: function (x, a, b) { return isNull(x) ? null : Math.max(a, Math.min(b, x)); },
    between: function (x, a, b) { return !isNull(x) && x >= a && x <= b; },
    isnull: function (x) { return isNull(x); },
    /* largest(k, a, b, ...) → k-th largest value (1-based); null if any value is null. Used by ISS. */
    largest: function (k) { var a = [].slice.call(arguments, 1); if (a.some(isNull) || k < 1 || k > a.length) return null; return a.sort(function (x, y) { return y - x; })[k - 1]; },
    coalesce: function (x, d) { return isNull(x) ? d : x; },
    roman: function (n) { return ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"][n] || String(n); },
    signed: function (n) { return isNull(n) ? "" : (n > 0 ? "+" + n : String(n)); },
    fixed: function (x, dp) { return isNull(x) ? "" : Number(x).toFixed(dp || 0); }
  };
  function isNull(x) { return x === null || x === undefined || (typeof x === "number" && isNaN(x)); }

  var TOKEN = /\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(&&|\|\||==|!=|<=|>=|[-+*/%<>!?:(),])|'([^']*)')/y;

  function tokenize(src) {
    var out = [], i = 0, m;
    while (i < src.length) {
      TOKEN.lastIndex = i; m = TOKEN.exec(src);
      if (!m) { if (/^\s*$/.test(src.slice(i))) break; throw new SyntaxError("Unexpected character at " + i + " in: " + src); }
      if (m[1] != null) out.push({ k: "lit", v: parseFloat(m[1]) });
      else if (m[2] != null) out.push({ k: "id", v: m[2] });
      else if (m[3] != null) out.push({ k: "op", v: m[3] });
      else out.push({ k: "lit", v: m[4] });
      i = TOKEN.lastIndex;
    }
    return out;
  }

  function parse(src) {
    if (typeof src !== "string" || !src.trim()) throw new SyntaxError("Empty expression");
    var t = tokenize(src), p = 0;
    function is(v) { return t[p] && t[p].k === "op" && t[p].v === v; }
    function eat(v) { if (!is(v)) throw new SyntaxError("Expected '" + v + "' in: " + src); p++; }
    function binary(next, ops) {
      return function () {
        var l = next();
        while (t[p] && t[p].k === "op" && ops.indexOf(t[p].v) >= 0) { var o = t[p++].v; l = { k: "bin", o: o, l: l, r: next() }; }
        return l;
      };
    }
    function unary() {
      if (is("!")) { p++; return { k: "not", e: unary() }; }
      if (is("-")) { p++; return { k: "neg", e: unary() }; }
      return primary();
    }
    var mul = binary(unary, ["*", "/", "%"]), add = binary(mul, ["+", "-"]), cmp = binary(add, ["<", ">", "<=", ">="]),
        eq = binary(cmp, ["==", "!="]), and = binary(eq, ["&&"]), or = binary(and, ["||"]);
    function ternary() {
      var c = or();
      if (is("?")) { p++; var a = ternary(); eat(":"); return { k: "?", c: c, a: a, b: ternary() }; }
      return c;
    }
    function primary() {
      var tk = t[p++];
      if (!tk) throw new SyntaxError("Unexpected end of: " + src);
      if (tk.k === "lit") return { k: "lit", v: tk.v };
      if (tk.k === "id") {
        if (tk.v === "true") return { k: "lit", v: true };
        if (tk.v === "false") return { k: "lit", v: false };
        if (tk.v === "null") return { k: "lit", v: null };
        if (is("(")) {
          p++; var args = [];
          if (!is(")")) { args.push(ternary()); while (is(",")) { p++; args.push(ternary()); } }
          eat(")");
          if (!has.call(FUNCS, tk.v)) throw new SyntaxError("Unknown function '" + tk.v + "'");
          return { k: "call", f: tk.v, a: args };
        }
        return { k: "var", v: tk.v };
      }
      if (tk.k === "op" && tk.v === "(") { var e = ternary(); eat(")"); return e; }
      throw new SyntaxError("Unexpected '" + tk.v + "' in: " + src);
    }
    var ast = ternary();
    if (p !== t.length) throw new SyntaxError("Unexpected trailing input in: " + src);
    return ast;
  }

  function run(n, v) {
    switch (n.k) {
      case "lit": return n.v;
      case "var": return has.call(v, n.v) ? v[n.v] : null;
      case "not": return !run(n.e, v);
      case "neg": var x = run(n.e, v); return isNull(x) ? null : -x;
      case "?": return run(n.c, v) ? run(n.a, v) : run(n.b, v);
      case "call": return FUNCS[n.f].apply(null, n.a.map(function (a) { return run(a, v); }));
      case "bin":
        if (n.o === "&&") return run(n.l, v) && run(n.r, v);
        if (n.o === "||") return run(n.l, v) || run(n.r, v);
        var l = run(n.l, v), r = run(n.r, v);
        if (n.o === "==") return l === r;
        if (n.o === "!=") return l !== r;
        if (n.o === "+" && (typeof l === "string" || typeof r === "string")) return (isNull(l) ? "" : String(l)) + (isNull(r) ? "" : String(r));
        if (isNull(l) || isNull(r)) return /[<>]/.test(n.o) ? false : null;
        switch (n.o) {
          case "+": return l + r; case "-": return l - r; case "*": return l * r;
          case "/": return r === 0 ? null : l / r; case "%": return r === 0 ? null : l % r;
          case "<": return l < r; case ">": return l > r; case "<=": return l <= r; case ">=": return l >= r;
        }
    }
    throw new Error("Invalid expression node");
  }

  var cache = Object.create(null);
  function compile(src) { return cache[src] || (cache[src] = parse(src)); }
  function evaluate(src, vars) { return run(compile(src), vars || {}); }
  /** Fill "{expr}" placeholders in a template string. */
  function template(tpl, vars) {
    return String(tpl).replace(/\{([^{}]+)\}/g, function (_, e) { var r = evaluate(e, vars); return isNull(r) ? "–" : String(r); });
  }
  /** Identifiers referenced by an expression (used by the model validator). */
  function identifiers(src) {
    var out = [];
    (function walk(n) {
      if (!n) return;
      if (n.k === "var" && out.indexOf(n.v) < 0) out.push(n.v);
      ["e", "c", "a", "b", "l", "r"].forEach(function (k) { if (n[k] && typeof n[k] === "object" && !Array.isArray(n[k])) walk(n[k]); });
      if (n.k === "call") n.a.forEach(walk);
    })(compile(src));
    return out;
  }
  return { evaluate: evaluate, template: template, compile: compile, identifiers: identifiers, isNull: isNull, FUNCTIONS: Object.keys(FUNCS) };
});
