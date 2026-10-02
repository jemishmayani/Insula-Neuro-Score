const test = require("node:test"), assert = require("node:assert/strict");
const { Engine, load, scoreIds } = require("./helpers");
/* Phase 8: the engine must never throw, whatever arrives as input. */
const GARBAGE = [undefined, null, "", " ", "abc", "1e9", "-1", "NaN", NaN, Infinity, -Infinity, 1e12, -5, 3.7, 0, true, false, [], ["x"], ["none", "none"], {}, { nt: true }, { nt: false },
  { nt: true, reason: 42 }, { value: "x", unit: "?" }, { value: 1 }, "__proto__", "constructor", "<script>", "\u0000"];
let seed = 99; const rnd = (n) => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed % n; };
test("engine never throws on malformed answers (every score × 1,500 fuzzed answer sets)", () => {
  let runs = 0;
  for (const id of scoreIds()) {
    const s = load(id);
    for (let k = 0; k < 1500; k++) {
      const a = {};
      for (const d of s.inputDefinitions) {
        const r = rnd(4);
        if (r === 0) continue;                                                // missing
        if (r === 1 && d.options) a[d.id] = d.options[rnd(d.options.length)].value; // valid
        else a[d.id] = GARBAGE[rnd(GARBAGE.length)];                          // garbage
      }
      if (rnd(10) === 0) a.unknown_input = "x";
      let r; assert.doesNotThrow(() => { r = Engine.calculate(s, a); }, id + " " + JSON.stringify(a));
      assert.ok(["complete", "incomplete", "invalid", "not-interpretable"].includes(r.status), id + " status");
      assert.ok(r.state && typeof r.state.label === "string" && typeof r.display === "string", id + " result shape");
      if (r.status === "complete") assert.ok(r.total >= s.calculationMethod.range.min && r.total <= s.calculationMethod.range.max, id + " range");
      runs++;
    }
  }
  assert.ok(runs > 40000, "runs " + runs);
});
test("engine handles missing or null answer objects", () => {
  for (const id of scoreIds()) for (const a of [undefined, null, {}]) assert.doesNotThrow(() => Engine.calculate(load(id), a), id);
});
test("unsupported calculations are reported, not crashed", () => {
  const s = JSON.parse(JSON.stringify(load("gcs")));
  s.inputDefinitions[0].type = "mystery";
  assert.ok(Engine.validateScore(s).some((e) => /unknown type/.test(e)));
  const r = Engine.calculate(s, { e: "4", v: "5", m: "6" });
  assert.equal(r.status, "invalid"); assert.ok(r.errors.some((e) => /Unsupported input type/.test(e.message)));
  const t = JSON.parse(JSON.stringify(load("gcs"))); t.calculationMethod = { ...t.calculationMethod, type: "expression", expression: "e / 0" };
  assert.equal(Engine.calculate(t, { e: "4", v: "5", m: "6" }).status, "invalid", "null total is a calculation error");
});
