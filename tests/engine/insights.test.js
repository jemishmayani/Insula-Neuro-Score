const test = require("node:test"), assert = require("node:assert/strict");
const fs = require("fs"), path = require("path");
const { Engine, load, scoreIds, ROOT } = require("./helpers");
const I = Engine.insights, clone = (o) => JSON.parse(JSON.stringify(o));
const IDS = ["gcs", "nihss", "mrs", "sins"];
const sec = (r, t) => r.insightSet.sections.find((s) => s.type === t);

/* ---------- structure ---------- */
test("insight set always has the five sections in fixed order", () => {
  for (const id of IDS) {
    const r = Engine.calculate(load(id), {});
    assert.deepEqual(r.insightSet.sections.map((s) => s.type), ["context", "consideration", "limitation", "confounder", "boundary"], id);
  }
});
test("every score has content in every insight type and at least one major limitation", () => {
  for (const id of IDS) {
    const s = load(id);
    for (const f of ["clinicalContext", "clinicalInsights", "limitations", "confounders", "whatItDoesNotTellYou", "commonErrors"]) assert.ok(s[f].length >= 1, id + " " + f);
    assert.ok(s.limitations.some((l) => l.importance === "major"), id + " has a major limitation");
    assert.ok(s.confounders.every((c) => typeof c === "string" || (c.factor && c.effect)), id + " confounders have factor + effect");
  }
});
test("ordering: contextual first, then major, then standard", () => {
  const r = Engine.calculate(load("gcs"), { e: "1", v: "1", m: "2" });
  const items = sec(r, "consideration").items;
  assert.ok(items[0].contextual && items[0].importance === "major", JSON.stringify(items[0]));
  const rank = (i) => (i.contextual ? 0 : 2) + (i.importance === "major" ? 0 : 1);
  for (const s of r.insightSet.sections) for (let k = 1; k < s.items.length; k++) assert.ok(rank(s.items[k - 1]) <= rank(s.items[k]), s.type);
});
test("not-testable-only insights appear only when a component is NT", () => {
  const s = load("gcs");
  const nt = Engine.calculate(s, { e: "3", v: { nt: true }, m: "6" }), ok = Engine.calculate(s, { e: "3", v: "4", m: "6" });
  assert.ok(sec(nt, "consideration").items.some((i) => /FOUR score/.test(i.text)));
  assert.ok(!sec(ok, "consideration").items.some((i) => /FOUR score/.test(i.text)));
  assert.ok(sec(nt, "limitation").items[0].text.startsWith("1 component(s) non-testable"), "contextual NT limitation first");
});
test("conditional insights are evaluated against the result", () => {
  const n = load("nihss"), z = {}; for (const d of n.inputDefinitions) z[d.id] = "0";
  assert.ok(sec(Engine.calculate(n, z), "consideration").items.some((i) => i.contextual && /score of 0/.test(i.text)));
  assert.ok(!sec(Engine.calculate(n, { ...z, item_4: "1" }), "consideration").items.some((i) => /score of 0/.test(i.text)));
  assert.ok(sec(Engine.calculate(n, { ...z, item_9: "2" }), "consideration").items.some((i) => /left-hemisphere/.test(i.text)));
});
test("incomplete results show only general (unconditional) insights", () => {
  for (const id of IDS) for (const s of Engine.calculate(load(id), {}).insightSet.sections) assert.ok(s.items.every((i) => !i.contextual), id + " " + s.type);
});
test("guide view: all items, templated ones only via guideText, majors first", () => {
  for (const id of IDS) {
    const g = I.forGuide(load(id));
    for (const s of g) {
      assert.ok(s.items.every((i) => !/\{/.test(i.text)), id + " " + s.type + " has unresolved template");
      const firstStd = s.items.findIndex((i) => i.importance !== "major");
      assert.ok(firstStd < 0 || s.items.slice(firstStd).every((i) => i.importance !== "major"), id + " " + s.type + " majors first");
    }
  }
  assert.ok(I.forGuide(load("gcs")).find((s) => s.type === "limitation").items.some((i) => i.conditional && /no total can be reported/.test(i.text)));
});

/* ---------- validator: insight content and semantic tone policy ---------- */
test("validator rejects malformed insight content", () => {
  const cases = [
    [(s) => s.limitations.push({ text: "" }), /needs text/],
    [(s) => s.limitations.push({ text: "x", importance: "huge" }), /importance/],
    [(s) => s.limitations.push({ text: "{nt_count} things" }), /templated text must be conditional/],
    [(s) => s.clinicalInsights.push({ when: "bogus > 1", text: "x" }), /unknown identifier 'bogus'/],
    [(s) => s.confounders.push({ factor: "Thing" }), /needs effect/],
    [(s) => delete s.clinicalContext, /clinicalContext/],
  ];
  for (const [mut, re] of cases) { const s = clone(load("gcs")); mut(s); const e = Engine.validateScore(s); assert.ok(e.some((m) => re.test(m)), re + " → " + JSON.stringify(e)); }
});
test("semantic tone policy: non-severity result types cannot borrow severity colours", () => {
  const m = clone(load("mrs")); m.resultStates[5].tone = "critical";
  assert.ok(Engine.validateScore(m).some((x) => /not used for functional-status/.test(x)));
  const n = clone(load("nihss")); n.resultStates[1].tone = "high";
  assert.ok(Engine.validateScore(n).some((x) => /not used for deficit/.test(x)));
  for (const t of Object.keys(I.PRESENTATIONS)) assert.ok(I.PRESENTATIONS[t].tones.length && I.PRESENTATIONS[t].describes, t);
  for (const t of ["severity", "classification", "functional-status", "disability", "stability", "imaging-classification", "prognostic-category"]) assert.ok(I.PRESENTATIONS[t], t + " supported");
});

/* ---------- safety: content never directs treatment or claims normality ---------- */
const DIRECTIVES = [/\bintubate\b/i, /\badminister\b(?! the (items|scale))/i, /\bprescribe\b/i, /\bgive (tpa|alteplase|tenecteplase|thrombolysis)\b/i, /\bshould be (intubated|treated|operated|ventilated)\b/i,
  /\b(indicates|indicated for|requires) (surgery|intubation|thrombolysis|thrombectomy|decompression)\b/i, /\brecommend(s|ed)? (surgery|intubation|thrombolysis|thrombectomy)\b/i,
  /\bstart (treatment|thrombolysis)\b/i, /\bpatient is normal\b/i, /\bis normal\b/i, /\bdiagnos(is|es|ed) of\b/i, /\bconfirms? (stroke|diagnosis)\b/i];
function allText(o, out = []) { if (typeof o === "string") out.push(o); else if (Array.isArray(o)) o.forEach((x) => allText(x, out)); else if (o && typeof o === "object") for (const k in o) if (k !== "sources" && k !== "licensing" && k !== "inputDefinitions") allText(o[k], out); return out; }
test("content lint: no autonomous diagnosis or treatment directives in any score", () => {
  for (const id of scoreIds()) for (const t of allText(load(id))) for (const re of DIRECTIVES) assert.ok(!re.test(t), `${id}: "${t}" matches ${re}`);
});
test("favourable states are positive but cautious (time-bound, not 'normal') — all scores", () => {
  for (const id of scoreIds()) for (const st of load(id).resultStates.filter((x) => x.tone === "favorable")) {
    assert.match(st.summary, /(at this assessment|at the time of assessment)/, id + " " + st.id);
    assert.ok(st.detail && st.detail.length > 20, id + " " + st.id + " has a cautionary detail");
  }
});
test("NIHSS 0 and severe GCS use the specified language", () => {
  const n = load("nihss"), z = {}; for (const d of n.inputDefinitions) z[d.id] = "0";
  assert.equal(Engine.calculate(n, z).state.summary, "No measurable deficit on the NIHSS at the time of assessment.");
  const g = Engine.calculate(load("gcs"), { e: "1", v: "2", m: "4" });
  assert.equal(g.state.tone, "high"); assert.match(g.state.detail, /^Correlate with airway, respiratory, neurological and systemic assessment/);
});
test("high and critical states explain themselves without directing treatment — all scores", () => {
  for (const id of scoreIds()) for (const st of load(id).resultStates.filter((x) => ["high", "critical"].includes(x.tone))) {
    assert.ok(st.detail, id + " " + st.id + " needs explanation");
    assert.match(st.detail, /(correlate|according to|depends on|integrate|management depends|assess)/i, id + " " + st.id);
  }
});

/* ---------- extensive: every combination yields a well-formed result + insight set ---------- */
function wellFormed(id, r) {
  assert.ok(r.state && r.state.label && r.state.summary, id + " state");
  assert.ok(Engine.TONES.includes(r.state.tone), id + " tone");
  assert.ok(r.presentation && r.presentation.typeLabel && r.presentation.describes, id + " presentation");
  assert.equal(r.insightSet.sections.length, 5);
  for (const s of r.insightSet.sections) for (const i of s.items) { assert.ok(i.text && !/[{}]/.test(i.text), id + " unresolved text: " + i.text); }
  for (const t of [r.state.summary, r.state.detail || "", r.display, r.shareText || ""]) assert.ok(!/[{}]/.test(t), id + " template left: " + t);
}
function* product(defs, withNT) {
  if (!defs.length) { yield {}; return; }
  const [d, ...rest] = defs, vals = d.options.map((o) => o.value);
  if (withNT && d.notTestable) vals.push(d.notTestable.reasons ? { nt: true, reason: d.notTestable.reasons[0] } : { nt: true });
  for (const v of vals) for (const r of product(rest, withNT)) yield { [d.id]: v, ...r };
}
test("GCS: all 210 combinations including NT give well-formed results", () => {
  const s = load("gcs"); let n = 0, nt = 0;
  for (const a of product(s.inputDefinitions, true)) { const r = Engine.calculate(s, a); wellFormed("gcs", r); n++; if (r.status === "not-interpretable") { nt++; assert.equal(r.total, null); assert.ok(/NT/.test(r.formula)); } }
  assert.equal(n, 210); assert.equal(nt, 90);
});
test("SINS: all 1,296 combinations give well-formed stability results", () => {
  const s = load("sins"); let n = 0;
  for (const a of product(s.inputDefinitions, false)) { const r = Engine.calculate(s, a); wellFormed("sins", r); assert.ok(["favorable", "moderate", "high"].includes(r.state.tone)); n++; }
  assert.equal(n, 1296);
});
test("mRS: all grades give functional-status results, never severity colours", () => {
  const s = load("mrs");
  for (let g = 0; g <= 6; g++) { const r = Engine.calculate(s, { grade: String(g) }); wellFormed("mrs", r); assert.ok(["favorable", "informational"].includes(r.state.tone)); assert.equal(r.presentation.type, "functional-status"); }
});
test("NIHSS: 3,000 random examinations including UN items give well-formed deficit results", () => {
  const s = load("nihss"); let seed = 7; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  let withUN = 0;
  for (let k = 0; k < 3000; k++) {
    const a = {};
    for (const d of s.inputDefinitions) a[d.id] = d.notTestable && rnd() < 0.08 ? { nt: true, reason: d.notTestable.reasons[0] } : d.options[Math.floor(rnd() * d.options.length)].value;
    const r = Engine.calculate(s, a); wellFormed("nihss", r); assert.equal(r.status, "complete");
    assert.ok(["favorable", "informational"].includes(r.state.tone));
    assert.ok(!/NIHSS \d+ — NIHSS/.test(r.shareText), "share text not duplicated: " + r.shareText);
    if (r.notTestable.length) { withUN++; assert.ok(sec(r, "limitation").items[0].contextual, "UN limitation first"); assert.ok(r.warnings.some((w) => /untestable/.test(w.message))); }
  }
  assert.ok(withUN > 300, "UN path exercised " + withUN);
});

/* ---------- Phase 6: every library score, every combination (or a deterministic sample) ---------- */
function* combos(defs) {
  if (!defs.length) { yield {}; return; }
  const [d, ...rest] = defs;
  let vals;
  if (d.type === "single" || d.type === "dropdown") vals = d.options.map((o) => o.value);
  else if (d.type === "multi") { const nonEx = d.options.filter((o) => !o.exclusive).map((o) => o.value); vals = [["none"], [nonEx[0]], nonEx.slice(0, 3), nonEx]; }
  else if (d.type === "integer") vals = [...new Set([d.min, Math.round((d.min + d.max) / 2), d.max, ...(d.pointBands || []).flatMap((b) => [b.min, b.max]).filter((x) => x != null)])];
  for (const v of vals) for (const r of combos(rest)) yield { [d.id]: v, ...r };
}
test("every implemented score: all (or banded) input combinations yield well-formed results", () => {
  let total = 0;
  for (const id of scoreIds()) {
    const s = load(id); let n = 0;
    for (const a of combos(s.inputDefinitions)) {
      if (n++ > 20000) break;
      const r = Engine.calculate(s, a); wellFormed(id, r); total++;
      assert.ok(["complete", "not-interpretable"].includes(r.status) || r.state.tone === "incomplete", id + " status " + r.status + " " + JSON.stringify(a));
      if (r.status === "complete") assert.ok(r.total >= s.calculationMethod.range.min && r.total <= s.calculationMethod.range.max, id + " in range");
      const allowed = Engine.insights.PRESENTATIONS[s.resultPresentation.type].tones.concat(["incomplete", "not-interpretable"]);
      assert.ok(allowed.includes(r.state.tone), id + " tone policy " + r.state.tone);
    }
  }
  assert.ok(total > 10000, "combinations evaluated: " + total);
});
