const test = require("node:test"), assert = require("node:assert/strict");
const fs = require("fs"), path = require("path");
const { Engine, load, scoreIds, ROOT } = require("./helpers");
const FIX = path.join(__dirname, "fixtures");

test("every fixture case is a documented manual verification", () => {
  for (const f of fs.readdirSync(FIX)) for (const c of JSON.parse(fs.readFileSync(path.join(FIX, f))).cases)
    assert.ok(c.verification && c.verification.method === "manual" && c.verification.calculation, f + ": " + c.name);
});
test("every implemented score validates and has a fixture file", () => {
  for (const id of scoreIds()) {
    assert.deepEqual(Engine.validateScore(load(id)), [], id);
    assert.ok(fs.existsSync(path.join(FIX, id + ".fixture.json")), "fixture missing for " + id);
  }
  const cat = JSON.parse(fs.readFileSync(path.join(ROOT, "content/catalog.json")));
  const impl = cat.scores.filter((s) => s.status === "implemented").map((s) => s.id).sort();
  assert.deepEqual(impl, scoreIds().sort(), "catalogue status matches content files");
});

for (const file of fs.readdirSync(FIX)) {
  const fx = JSON.parse(fs.readFileSync(path.join(FIX, file))), score = load(fx.scoreId);
  for (const c of fx.cases) {
    const v = c.verification ? ` [${c.verification.calculation}]` : "";
    test(`${fx.scoreId}: ${c.name}${v}`, () => {
      const r = Engine.calculate(score, c.answers), e = c.expect;
      if ("status" in e) assert.equal(r.status, e.status);
      if ("total" in e) assert.equal(r.total, e.total);
      if ("display" in e) assert.equal(r.display, e.display);
      if ("state" in e) assert.equal(r.state.id, e.state);
      if ("tone" in e) assert.equal(r.state.tone, e.tone);
      if ("label" in e) assert.equal(r.state.label, e.label);
      for (const k of ["errors", "warnings", "missing", "notTestable"]) if (k in e) assert.equal(r[k].length, e[k], k + ": " + JSON.stringify(r[k]));
      if (e.shareText) assert.equal(r.shareText, e.shareText);
      if (e.formula) assert.equal(r.formula, e.formula);
      if (e.insightsContains) assert.ok(r.insights.some((t) => t.includes(e.insightsContains)), JSON.stringify(r.insights));
      if (e.warningContains) assert.ok(r.warnings.some((w) => w.message.includes(e.warningContains)));
      if (e.limitationsContains) assert.ok(r.limitations.some((l) => l.contextual && l.text.includes(e.limitationsContains)));
    });
  }
}

/* Exhaustive / property checks */
function* product(defs) {
  if (!defs.length) { yield {}; return; }
  const [d, ...rest] = defs;
  for (const o of d.options) for (const r of product(rest)) yield { [d.id]: o.value, ...r };
}
test("GCS: all 120 complete combinations sum correctly and map to the right band", () => {
  const s = load("gcs"); let n = 0;
  for (const a of product(s.inputDefinitions)) {
    const r = Engine.calculate(s, a), t = +a.e + +a.v + +a.m; n++;
    assert.equal(r.total, t);
    assert.equal(r.state.id, t === 15 ? "none" : t >= 13 ? "mild" : t >= 9 ? "moderate" : "severe");
    assert.equal(r.formula, `E${a.e} + V${a.v} + M${a.m}`);
  }
  assert.equal(n, 120);
});
test("SINS: all 1,296 combinations sum correctly and map to the right category", () => {
  const s = load("sins"); let n = 0;
  for (const a of product(s.inputDefinitions)) {
    const r = Engine.calculate(s, a), t = Object.values(a).reduce((x, v) => x + +v, 0); n++;
    assert.equal(r.total, t); assert.equal(r.state.id, t <= 6 ? "stable" : t <= 12 ? "potential" : "unstable");
  }
  assert.equal(n, 1296);
});
test("NIHSS: 5,000 random complete examinations stay within 0–42 and equal the item sum", () => {
  const s = load("nihss"); let seed = 42; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  for (let i = 0; i < 5000; i++) {
    const a = {}; let t = 0;
    for (const d of s.inputDefinitions) { const o = d.options[Math.floor(rnd() * d.options.length)]; a[d.id] = o.value; t += o.points; }
    const r = Engine.calculate(s, a);
    assert.equal(r.total, t); assert.ok(r.total >= 0 && r.total <= 42); assert.equal(r.status, "complete");
  }
});
test("NIHSS: item maxima sum to 42 and minima to 0", () => {
  const s = load("nihss");
  assert.equal(s.inputDefinitions.reduce((x, d) => x + Math.max(...d.options.map((o) => o.points)), 0), 42);
  assert.equal(s.inputDefinitions.length, 15);
});
test("SINS: component maxima sum to 18", () => {
  assert.equal(load("sins").inputDefinitions.reduce((x, d) => x + Math.max(...d.options.map((o) => o.points)), 0), 18);
});
