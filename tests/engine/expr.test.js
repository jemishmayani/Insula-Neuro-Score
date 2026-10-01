const test = require("node:test"), assert = require("node:assert/strict");
const { X } = require("./helpers");
test("arithmetic and precedence", () => {
  assert.equal(X.evaluate("1 + 2 * 3", {}), 7);
  assert.equal(X.evaluate("(1 + 2) * 3", {}), 9);
  assert.equal(X.evaluate("10 - 4 - 3", {}), 3);
  assert.equal(X.evaluate("-a + 5", { a: 2 }), 3);
});
test("comparison, logic, ternary", () => {
  assert.equal(X.evaluate("a >= 7 && a <= 12", { a: 7 }), true);
  assert.equal(X.evaluate("a == 15 ? 'x' : a >= 13 ? 'y' : 'z'", { a: 13 }), "y");
  assert.equal(X.evaluate("!(a > 1) || b", { a: 2, b: false }), false);
});
test("null semantics: arithmetic → null, comparison → false", () => {
  assert.equal(X.evaluate("a + 1", { a: null }), null);
  assert.equal(X.evaluate("a > 1", {}), false);
  assert.equal(X.evaluate("isnull(a)", {}), true);
  assert.equal(X.evaluate("coalesce(a, 4)", {}), 4);
  assert.equal(X.evaluate("1 / 0", {}), null);
});
test("strings and template", () => {
  assert.equal(X.evaluate("'Grade ' + roman(3)", {}), "Grade III");
  assert.equal(X.template("GCS {total} ({e_code})", { total: 9, e_code: "E2" }), "GCS 9 (E2)");
  assert.equal(X.template("{missing}", {}), "–");
  assert.equal(X.evaluate("signed(-2) + signed(3)", {}), "-2+3");
});
test("safety: no globals, prototype or unknown functions", () => {
  assert.equal(X.evaluate("constructor", {}), null);
  assert.equal(X.evaluate("__proto__", {}), null);
  assert.equal(X.evaluate("toString", { a: 1 }), null);
  assert.throws(() => X.evaluate("alert(1)", {}), /Unknown function/);
  assert.throws(() => X.evaluate("a; b", {}), SyntaxError);
  assert.throws(() => X.evaluate("1 +", {}), SyntaxError);
  assert.throws(() => X.evaluate("", {}), SyntaxError);
  assert.throws(() => X.evaluate("a[0]", {}), SyntaxError);
});
test("identifiers() lists referenced variables", () => {
  assert.deepEqual(X.identifiers("a + max(b, c) > 3 ? d : 'x'").sort(), ["a", "b", "c", "d"]);
});
