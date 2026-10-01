global.window = global;
require("../app/assets/js/engine.js");
const E = window.ScoreEngine, fs = require("fs");
const S = id => JSON.parse(fs.readFileSync(`app/assets/content/scores/${id}.json`));
let pass = 0, fail = 0;
function eq(name, got, exp) { if (JSON.stringify(got) === JSON.stringify(exp)) pass++; else { fail++; console.log("FAIL", name, "got", got, "expected", exp); } }
function calc(id, a) { return E.calculate(S(id), a); }

// validation of all content
for (const f of fs.readdirSync("app/assets/content/scores")) { const errs = E.validate(JSON.parse(fs.readFileSync("app/assets/content/scores/" + f))); eq("validate " + f, errs, []); }

// GCS
let r = calc("gcs", { e: "4", v: "5", m: "6" }); eq("gcs 15", [r.display, r.state.state], ["15", "normal"]);
r = calc("gcs", { e: "3", v: "4", m: "6" }); eq("gcs 13", [r.display, r.state.state], ["13", "low"]);
r = calc("gcs", { e: "2", v: "3", m: "5" }); eq("gcs 10", [r.display, r.state.state, r.share], ["10", "moderate", "GCS 10 (E2 V3 M5) — Moderate impairment"]);
r = calc("gcs", { e: "2", v: "2", m: "4" }); eq("gcs 8", [r.display, r.state.state], ["8", "high"]);
r = calc("gcs", { e: "1", v: "1", m: "1" }); eq("gcs 3", [r.display, r.state.state], ["3", "high"]);
r = calc("gcs", { e: "2", v: "NT", m: "5" }); eq("gcs NT", [r.display, r.state.state, r.insights.length > 0], ["E2 VNT M5", "incomplete", true]);
r = calc("gcs", { e: "2", m: "5" }); eq("gcs missing", [r.state.state, r.missing.length], ["incomplete", 1]);
// GCS-P
r = calc("gcsp", { e: "1", v: "1", m: "1", prs: "2" }); eq("gcsp min", [r.display, r.state.state], ["1", "high"]);
r = calc("gcsp", { e: "4", v: "5", m: "6", prs: "1" }); eq("gcsp 14", [r.display, r.state.state, r.share], ["14", "info", "GCS-P 14 (GCS 15: E4 V5 M6; PRS 1) — Calculated"]);
r = calc("gcsp", { e: "3", v: "3", m: "4", prs: "1" }); eq("gcsp 9", r.display, "9");
r = calc("gcsp", { e: "2", v: "2", m: "4", prs: "0" }); eq("gcsp 8", r.state.state, "high");
// FOUR
r = calc("four", { e: "4", m: "4", b: "4", r: "4" }); eq("four 16", [r.display, r.state.state], ["16", "normal"]);
r = calc("four", { e: "0", m: "0", b: "0", r: "0" }); eq("four 0", [r.display, r.state.state], ["0", "critical"]);
r = calc("four", { e: "4", m: "0", b: "4", r: "4" }); eq("four locked-in insight", r.insights.some(i => /locked-in/.test(i.text)), true);
// ICH
const ichMort = ["0%", "13%", "26%", "72%", "97%", "100%"];
for (let t = 0; t <= 5; t++) {
  const a = { gcs: "0", vol: "0", ivh: "no", infra: "0", age: "0" }; const k = ["vol", "infra", "age", "gcs", "gcs"]; let n = 0;
  // build total t
  const combos = [{}, { vol: "1" }, { vol: "1", age: "1" }, { vol: "1", age: "1", infra: "1" }, { vol: "1", age: "1", infra: "1", ivh: "yes" }, { vol: "1", age: "1", infra: "1", ivh: "yes", gcs: "1" }];
  r = calc("ich", Object.assign(a, combos[t])); eq("ich " + t, [r.display, r.state.summary.includes(ichMort[t])], [String(t), true]);
}
r = calc("ich", { gcs: "2", vol: "1", ivh: "yes", infra: "1", age: "1" }); eq("ich 6", [r.display, r.state.state], ["6", "critical"]);
// Hunt & Hess
r = calc("hunthess", { grade: "3", mod: "no" }); eq("hh III", r.display, "Grade III");
r = calc("hunthess", { grade: "3", mod: "yes" }); eq("hh III+mod", [r.display, r.share.startsWith("Hunt & Hess Grade IV (clinical III + modifier)")], ["Grade IV", true]);
r = calc("hunthess", { grade: "5", mod: "yes" }); eq("hh cap", r.display, "Grade V");
// WFNS
const w = (g, d) => calc("wfns", { gcs: g, deficit: d });
eq("wfns 15-", w(15, "no").display, "Grade I"); eq("wfns 15+", [w(15, "yes").display, w(15, "yes").state.state], ["Undefined", "incomplete"]);
eq("wfns 14-", w(14, "no").display, "Grade II"); eq("wfns 13+", w(13, "yes").display, "Grade III");
eq("wfns 12", w(12, "no").display, "Grade IV"); eq("wfns 7+", w(7, "yes").display, "Grade IV");
eq("wfns 6", w(6, "no").display, "Grade V"); eq("wfns 3", w(3, "yes").display, "Grade V");
eq("wfns invalid 16", w(16, "no").state.state, "incomplete"); eq("wfns invalid 7.5", w(7.5, "no").state.state, "incomplete");
eq("wfns empty", w("", "no").state.state, "incomplete");
// m-WFNS
const mw = g => calc("mwfns", { gcs: g }).display;
eq("mwfns", [mw(15), mw(14), mw(13), mw(12), mw(7), mw(6), mw(3)], ["Grade I", "Grade II", "Grade III", "Grade IV", "Grade IV", "Grade V", "Grade V"]);
// mFisher
const mf = (s, i) => calc("mfisher", { sah: s, ivh: i });
eq("mf", [mf("0", "no").display, mf("1", "no").display, mf("1", "yes").display, mf("2", "no").display, mf("2", "yes").display], ["Grade 0", "Grade 1", "Grade 2", "Grade 3", "Grade 4"]);
eq("mf undefined", [mf("0", "yes").display, mf("0", "yes").state.state], ["Undefined", "incomplete"]);
// mRS
for (let g = 0; g <= 6; g++) eq("mrs " + g, calc("mrs", { grade: String(g) }).display, "mRS " + g);
// RASS
eq("rass +4", calc("rass", { level: "4" }).display, "RASS +4"); eq("rass 0", calc("rass", { level: "0" }).display, "RASS 0");
eq("rass -5", [calc("rass", { level: "-5" }).display, calc("rass", { level: "-5" }).state.state], ["RASS -5", "moderate"]);
eq("rass -3 state", calc("rass", { level: "-3" }).state.label, "Moderate sedation");

// Exhaustive: every combination of every choice-only score yields a state and a display without throwing
for (const id of ["gcs", "gcsp", "four", "ich", "hunthess", "mfisher", "mrs", "rass"]) {
  const s = S(id); let combos = [{}];
  for (const inp of s.inputs) { const nx = []; for (const c of combos) for (const o of inp.options) nx.push(Object.assign({}, c, { [inp.id]: o.value })); combos = nx; }
  let bad = 0; for (const c of combos) { try { const x = E.calculate(s, c); if (!x.state || !x.display) bad++; if (x.state.state !== "incomplete" && x.primaryValue == null) bad++; } catch (e) { bad++; console.log(id, e.message); } }
  eq("exhaustive " + id + " (" + combos.length + ")", bad, 0);
}
// Expression safety: no access to globals
let threw = false; try { E.evaluate("constructor", {}); } catch (e) { threw = true; } eq("no global access", E.evaluate("constructor", {}) === null || threw, true);
threw = false; try { E.evaluate("alert(1)", {}); } catch (e) { threw = true; } eq("no unknown funcs", threw, true);
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
