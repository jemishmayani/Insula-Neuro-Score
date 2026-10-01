const test = require("node:test"), assert = require("node:assert/strict");
const { Engine, demo, load } = require("./helpers");
const clone = (o) => JSON.parse(JSON.stringify(o));
const DEMO_FULL = { single: "c", dropdown: "z", yes_no: "yes", multi: ["p", "q", "r"], integer: 9, decimal: 3, number: 70, temperature: { value: 39, unit: "C" } };

test("result model has all pipeline outputs", () => {
  const r = Engine.calculate(demo(), DEMO_FULL);
  for (const k of ["scoreId", "status", "total", "display", "state", "interpretation", "breakdown", "errors", "warnings", "missing", "notTestable", "insights", "limitations", "related", "shareText"]) assert.ok(k in r, k);
  assert.equal(r.status, "complete"); assert.equal(r.total, 13); assert.equal(r.state.tone, "informational");
  assert.equal(r.breakdown.length, 2); assert.equal(r.breakdown[0].subtotal, 8); assert.equal(r.breakdown[1].subtotal, 5);
});
test("all input types flow through to a total", () => {
  const r = Engine.calculate(demo(), { single: "a", dropdown: "x", yes_no: "no", multi: ["none"], integer: 0, decimal: 0, temperature: { value: 97, unit: "F" } });
  assert.equal(r.status, "complete"); assert.equal(r.total, 0, "optional number may be blank"); assert.equal(r.state.tone, "normal");
});
test("every result state tone reachable in demo", () => {
  const tones = new Set();
  for (let t = 0; t <= 11; t++) {
    const s = clone(demo()); s.calculationMethod = { ...s.calculationMethod, type: "expression", expression: String(t) };
    tones.add(Engine.calculate(s, DEMO_FULL).state.tone);
  }
  tones.add(Engine.calculate(demo(), { ...DEMO_FULL, single: { nt: true } }).state.tone);
  tones.add(Engine.calculate(demo(), {}).state.tone);
  assert.deepEqual([...tones].sort(), Engine.TONES.slice().sort());
});
test("invalid input takes precedence and is reported per input", () => {
  const r = Engine.calculate(demo(), { ...DEMO_FULL, integer: 2.5, decimal: 9 });
  assert.equal(r.status, "invalid"); assert.equal(r.total, null);
  assert.deepEqual(r.errors.map((e) => e.inputId).sort(), ["decimal", "integer"]);
});
test("missing inputs list labels; optional inputs not required", () => {
  const a = { ...DEMO_FULL }; delete a.integer; delete a.number;
  const r = Engine.calculate(demo(), a);
  assert.equal(r.status, "incomplete"); assert.deepEqual(r.missing, ["integer"]); assert.match(r.state.summary, /Integer/);
});
test("block policy: not-testable → not-interpretable, no total", () => {
  const r = Engine.calculate(demo(), { ...DEMO_FULL, single: { nt: true } });
  assert.equal(r.status, "not-interpretable"); assert.equal(r.total, null); assert.equal(r.breakdown[0].subtotal, null);
});
test("exclude policy: not-testable scored 0, flagged, contextual limitation first", () => {
  const s = clone(demo()); s.calculationMethod.notTestablePolicy = "exclude";
  s.limitations.push({ when: "nt_count > 0", text: "{nt_count} untestable" });
  const r = Engine.calculate(s, { ...DEMO_FULL, single: { nt: true } });
  assert.equal(r.status, "complete"); assert.equal(r.total, 11); assert.equal(r.warnings.length, 1);
  assert.deepEqual(r.limitations[0], { text: "1 untestable", contextual: true });
});
test("result outside declared range is a calculation error, not a result", () => {
  const s = clone(demo()); s.calculationMethod.type = "expression"; s.calculationMethod.expression = "total_not_defined_yet + 99";
  s.scoringRules = [{ id: "total_not_defined_yet", expr: "1" }];
  const r = Engine.calculate(s, DEMO_FULL);
  assert.equal(r.status, "invalid"); assert.equal(r.state.label, "Calculation error");
});
test("scoring rules feed expression method", () => {
  const s = clone(demo()); s.scoringRules = [{ id: "choice_part", expr: "single + dropdown" }];
  s.calculationMethod = { ...s.calculationMethod, type: "expression", expression: "choice_part * 2" };
  const r = Engine.calculate(s, DEMO_FULL); assert.equal(r.total, 8); assert.equal(r.values.choice_part, 4);
});
test("related scores and insights are returned", () => {
  const r = Engine.calculate(load("gcs"), { e: "1", v: "1", m: "2" });
  assert.ok(r.related.some((x) => x.id === "four"));
  assert.ok(r.insights.some((t) => /motor score/.test(t)));
});
test("validator rejects malformed models with specific messages", () => {
  const good = load("sins"); assert.deepEqual(Engine.validateScore(good), []);
  const cases = [
    [(s) => delete s.sources, /missing field: sources/],
    [(s) => (s.interpretationRules[0].when = "totl > 3"), /unknown identifier 'totl'/],
    [(s) => (s.interpretationRules[0].state = "nope"), /unknown state nope/],
    [(s) => (s.resultStates[0].tone = "red"), /tone must be one of/],
    [(s) => s.components[0].inputs.pop(), /not in any component/],
    [(s) => s.inputDefinitions.push({ ...s.inputDefinitions[0] }), /duplicate input id/],
    [(s) => (s.calculationMethod.type = "magic"), /calculationMethod.type/],
    [(s) => (s.calculationMethod.display = "{bogus}"), /unknown identifier 'bogus'/],
    [(s) => (s.clinicalInsights[1].when = "total >"), /Unexpected end/],
    [(s) => (s.lastReviewed = "2026"), /lastReviewed/],
    [(s) => (s.inputDefinitions[0].id = "total"), /reserved/],
  ];
  for (const [mut, re] of cases) { const s = clone(good); mut(s); const e = Engine.validateScore(s); assert.ok(e.some((m) => re.test(m)), re + " → " + JSON.stringify(e)); }
});
test("engine is deterministic and does not mutate inputs", () => {
  const s = load("nihss"), a = { item_1a: "1" }, sCopy = JSON.stringify(s), aCopy = JSON.stringify(a);
  Engine.calculate(s, a); Engine.calculate(s, a);
  assert.equal(JSON.stringify(s), sCopy); assert.equal(JSON.stringify(a), aCopy);
});
