const test = require("node:test"), assert = require("node:assert/strict");
const { Inputs, demo } = require("./helpers");
const D = demo(), def = (id) => D.inputDefinitions.find((d) => d.id === id);
const N = (id, raw) => Inputs.normalize(def(id), raw);
test("single choice", () => {
  assert.equal(N("single", "b").points, 1);
  assert.equal(N("single", "zz").status, "invalid");
  assert.equal(N("single", "").status, "empty");
});
test("dropdown", () => { assert.equal(N("dropdown", "z").points, 2); assert.equal(N("dropdown", "q").status, "invalid"); });
test("yes/no accepts strings and booleans", () => {
  assert.equal(N("yes_no", "yes").points, 1); assert.equal(N("yes_no", false).points, 0); assert.equal(N("yes_no", "maybe").status, "invalid");
});
test("multiple choice: sum, cap, exclusive option", () => {
  assert.equal(N("multi", ["p", "q"]).points, 2);
  assert.equal(N("multi", ["p", "q", "r"]).points, 3);
  assert.equal(N("multi", ["none"]).points, 0);
  assert.equal(N("multi", ["none", "p"]).status, "invalid");
  assert.equal(N("multi", ["p", "p"]).points, 1, "duplicates ignored");
  assert.equal(N("multi", ["x"]).status, "invalid");
  assert.equal(N("multi", []).status, "empty");
});
test("integer rejects decimals and out-of-range; bands map to points", () => {
  assert.equal(N("integer", "3.5").status, "invalid");
  assert.equal(N("integer", 11).status, "invalid");
  assert.equal(N("integer", -1).status, "invalid");
  assert.equal(N("integer", "3").points, 0); assert.equal(N("integer", 4).points, 1); assert.equal(N("integer", 8).points, 2);
  assert.equal(N("integer", "abc").status, "invalid");
  assert.equal(N("integer", "1e3").status, "invalid", "no exponent notation");
});
test("decimal enforces precision and accepts comma", () => {
  assert.equal(N("decimal", "2.55").status, "invalid");
  assert.equal(N("decimal", "2,5").points, 1);
  assert.equal(N("decimal", "2.4").points, 0);
});
test("number: optional, unit label", () => { assert.equal(N("number", "").status, "empty"); assert.match(N("number", 60).label, /units/); });
test("measurement converts units to canonical", () => {
  const f = N("temperature", { value: "100.4", unit: "F" });
  assert.equal(f.status, "ok"); assert.equal(f.value, 38); assert.equal(f.points, 1);
  assert.equal(N("temperature", { value: 37, unit: "C" }).points, 0);
  assert.equal(N("temperature", { value: 120, unit: "F" }).status, "invalid");
  assert.equal(N("temperature", { value: 37, unit: "K" }).status, "invalid");
  assert.equal(N("temperature", { value: "", unit: "C" }).status, "empty");
});
test("not testable only where allowed", () => {
  assert.equal(N("single", { nt: true }).status, "nt");
  assert.equal(N("dropdown", { nt: true }).status, "invalid");
});
test("definition validation", () => {
  assert.deepEqual(Inputs.validateDefinition({ id: "ok", type: "integer", min: 0, max: 1 }), []);
  assert.ok(Inputs.validateDefinition({ id: "Bad", type: "single", options: [] }).length >= 2);
  assert.ok(Inputs.validateDefinition({ id: "x", type: "integer" }).length === 1);
  assert.ok(Inputs.validateDefinition({ id: "x", type: "wat" }).length === 1);
});
