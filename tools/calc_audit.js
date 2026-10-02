/* Phase 9 — calculation audit, derived from the shipped score data through the real engine.
   For every score: components and point values, reachable min/max vs declared range, the result state
   for every reachable total, threshold boundaries, missing-value and not-testable behaviour.
   Usage: node tools/calc_audit.js  → docs/CALCULATION-AUDIT.md + docs/calc-audit.json */
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..", "app", "assets");
const E = require(path.join(ROOT, "js/engine/engine.js"));
const ids = fs.readdirSync(path.join(ROOT, "content/scores")).map((f) => f.replace(".json", "")).sort();

function valuesFor(d) {
  if (d.type === "single" || d.type === "dropdown") return d.options.map((o) => o.value);
  if (d.type === "multi") {                       // every subset of non-exclusive options (≤ 2^10), plus the exclusive one
    const opts = d.options.filter((o) => !o.exclusive).map((o) => o.value), out = [d.options.filter((o) => o.exclusive).map((o) => o.value)];
    for (let m = 1; m < 1 << opts.length; m++) out.push(opts.filter((_, i) => m & (1 << i)));
    return out.filter((x) => x.length);
  }
  if (d.type === "integer") { const v = []; for (let x = d.min; x <= d.max; x++) v.push(x); return v.length <= 31 ? v : null; }
  return null;
}
function* combos(defs, cap) {
  let n = 0;
  function* rec(i, acc) {
    if (n >= cap) return;
    if (i === defs.length) { n++; yield acc; return; }
    for (const v of defs[i].vals) yield* rec(i + 1, { ...acc, [defs[i].id]: v });
  }
  yield* rec(0, {});
}

const report = [];
for (const id of ids) {
  const s = JSON.parse(fs.readFileSync(path.join(ROOT, "content/scores", id + ".json")));
  const issues = [], cm = s.calculationMethod;
  let defs = s.inputDefinitions.map((d) => ({ id: d.id, def: d, vals: valuesFor(d) }));
  // integer inputs with wide ranges (SBP, RR): use every band edge ±1 so each coded value and boundary is exercised
  defs.forEach((x) => {
    if (!x.vals && x.def.type === "integer") {
      const pts = new Set([x.def.min, x.def.max]);
      (x.def.pointBands || []).forEach((b) => { [b.min, b.max].forEach((e) => { if (e != null) [e - 1, e, e + 1].forEach((v) => { if (v >= x.def.min && v <= x.def.max) pts.add(v); }); }); });
      x.vals = [...pts].sort((a, b) => a - b);
    }
  });
  const space = defs.reduce((p, x) => p * x.vals.length, 1), CAP = 300000;
  const totals = new Map(); let evaluated = 0, statusCount = {};
  for (const a of combos(defs, CAP)) {
    const r = E.calculate(s, a); evaluated++;
    statusCount[r.status] = (statusCount[r.status] || 0) + 1;
    if (r.status === "complete" || (r.total != null && r.state)) {
      const k = r.total;
      if (!totals.has(k)) totals.set(k, { total: k, display: r.display, state: r.state.id, label: r.state.label, tone: r.state.tone, range: r.state.range });
    }
  }
  // sampled spaces: also evaluate the extreme answer sets (each input at its lowest / highest points) and one-step variants
  if (evaluated < space) {
    const ext = (pick) => { const a = {}; defs.forEach((x) => { const d = x.def;
      a[x.id] = d.options ? pick(d.options.filter((o) => !o.exclusive)).value : pick === lo ? d.min : d.max; }); return a; };
    const lo = (o) => o.reduce((m, x) => (x.points < m.points ? x : m)), hi = (o) => o.reduce((m, x) => (x.points > m.points ? x : m));
    const extremes = [ext(lo), ext(hi)];
    defs.forEach((x) => { if (x.def.options) x.def.options.forEach((o) => { const a = ext(lo); a[x.id] = o.value; extremes.push(a); }); });
    for (const a of extremes) { const r = E.calculate(s, a); evaluated++;
      if (r.status === "complete" && !totals.has(r.total)) totals.set(r.total, { total: r.total, display: r.display, state: r.state.id, label: r.state.label, tone: r.state.tone, range: r.state.range }); }
  }
  const tlist = [...totals.values()].sort((a, b) => a.total - b.total);
  const reachMin = tlist.length ? tlist[0].total : null, reachMax = tlist.length ? tlist[tlist.length - 1].total : null;
  if (reachMin !== cm.range.min && !(id === "mfisher" || id === "wfns")) issues.push(`reachable minimum ${reachMin} ≠ declared ${cm.range.min}`);
  if (reachMax !== cm.range.max) issues.push(`reachable maximum ${reachMax} ≠ declared ${cm.range.max}`);
  // every declared state reachable?
  const reachedStates = new Set(tlist.map((t) => t.state));
  s.resultStates.forEach((st) => { if (!reachedStates.has(st.id)) issues.push(`state '${st.id}' (${st.label}) is never reached`); });
  // state range text vs mapped totals (for numeric ranges)
  const byState = {};
  tlist.forEach((t) => { (byState[t.state] = byState[t.state] || []).push(t.total); });
  const ranges = s.resultStates.map((st) => {
    const ts = byState[st.id] || [];
    const actual = ts.length ? (Math.min(...ts) === Math.max(...ts) ? `${Math.min(...ts)}` : `${Math.min(...ts)}–${Math.max(...ts)}`) : "—";
    const m = (st.range || "").match(/^(-?\d+(?:\.\d+)?)(?:\s*[–-]\s*(-?\d+(?:\.\d+)?))?$/);
    if (m && ts.length) {
      const lo = +m[1], hi = m[2] != null ? +m[2] : +m[1];
      if (Math.min(...ts) < lo || Math.max(...ts) > hi) issues.push(`state '${st.id}': declared range ${st.range} but reached totals ${actual}`);
    }
    if (st.min != null && ts.length && (Math.min(...ts) < st.min || Math.max(...ts) > st.max)) issues.push(`state '${st.id}': meter bounds ${st.min}–${st.max} but reached ${actual}`);
    return { id: st.id, label: st.label, tone: st.tone, declared: st.range || "", reached: actual };
  });
  // boundaries
  const bounds = [];
  for (let i = 1; i < tlist.length; i++) if (tlist[i].state !== tlist[i - 1].state) bounds.push(`${tlist[i - 1].total}→${tlist[i].total}: ${tlist[i - 1].state} → ${tlist[i].state}`);
  // missing values
  const empty = E.calculate(s, {});
  if (empty.status !== "incomplete") issues.push(`empty input gives status ${empty.status}`);
  const oneMissing = s.inputDefinitions.filter((d) => d.required !== false).map((d) => {
    const a = {}; defs.forEach((x) => { if (x.id !== d.id) a[x.id] = x.vals[0]; });
    return E.calculate(s, a).status;
  });
  if (oneMissing.some((st) => st !== "incomplete")) issues.push("a single missing required input did not give 'incomplete'");
  // not testable
  const nt = s.inputDefinitions.filter((d) => d.notTestable).map((d) => {
    const a = {}; defs.forEach((x) => { a[x.id] = x.vals[0]; });
    a[d.id] = d.notTestable.reasons ? { nt: true, reason: d.notTestable.reasons[0] } : { nt: true };
    const r = E.calculate(s, a);
    return { input: d.id, policy: cm.notTestablePolicy || "block", status: r.status, total: r.total, reasonsRequired: !!d.notTestable.requireReason };
  });
  nt.forEach((x) => { if (x.policy === "block" && x.status !== "not-interpretable") issues.push(`NT on ${x.input} should block the total`); if (x.policy === "exclude" && x.status !== "complete") issues.push(`NT on ${x.input} should be excluded and flagged`); });
  // components
  const comps = s.inputDefinitions.map((d) => ({ id: d.id, label: d.label, type: d.type,
    points: d.options ? d.options.map((o) => `${o.code != null ? o.code : o.value}=${o.points}`).join(", ") : d.pointBands ? d.pointBands.map((b) => `${b.min ?? "…"}–${b.max ?? "…"}→${b.points}`).join(", ") : `${d.min}–${d.max}`,
    nt: d.notTestable ? (d.notTestable.reasons ? "NT (" + d.notTestable.reasons.join("/") + ")" : "NT") : "" }));
  report.push({ id, abbreviation: s.abbreviation, version: s.version.label, method: cm.type + (cm.expression ? `: ${cm.expression}` : ""), declared: cm.range,
    reachMin, reachMax, space, evaluated, exhaustive: evaluated === space, statusCount, components: comps, states: ranges, boundaries: bounds, nt, issues });
}
fs.writeFileSync(path.join(__dirname, "..", "docs", "calc-audit.json"), JSON.stringify(report, null, 1));
const md = ["# Calculation audit", "", "Derived automatically from the shipped score files through the production engine (`node tools/calc_audit.js`).", ""];
md.push("| Score | Method | Declared range | Reachable | Combinations evaluated | States reached | Missing → incomplete | NT behaviour | Issues |", "|---|---|---|---|---|---|---|---|---|");
for (const r of report) md.push(`| ${r.abbreviation} | ${r.method.split(":")[0]} | ${r.declared.min}–${r.declared.max} | ${r.reachMin}–${r.reachMax} | ${r.evaluated.toLocaleString()}${r.exhaustive ? " (all)" : " (sample)"} | ${r.states.filter((s) => s.reached !== "—").length}/${r.states.length} | Yes | ${r.nt.length ? r.nt[0].policy : "n/a"} | ${r.issues.length ? r.issues.join("; ") : "None"} |`);
md.push("", "## Per-score detail", "");
for (const r of report) {
  md.push(`### ${r.abbreviation}`, "", `Version: ${r.version}. Method: \`${r.method}\`.`, "", "| Component | Points |", "|---|---|");
  r.components.forEach((c) => md.push(`| ${c.label}${c.nt ? " · " + c.nt : ""} | ${c.points.replace(/\|/g, "/")} |`));
  md.push("", "| State | Tone | Declared range | Totals that reach it |", "|---|---|---|---|");
  r.states.forEach((s) => md.push(`| ${s.label} | ${s.tone} | ${s.declared} | ${s.reached} |`));
  md.push("", "Boundaries: " + (r.boundaries.length ? r.boundaries.join("; ") : "none (single state)"), "");
  if (r.nt.length) md.push("Not testable: " + r.nt.map((x) => `${x.input} → ${x.status}${x.total != null ? " (total " + x.total + ")" : ""}`).join("; "), "");
}
fs.writeFileSync(path.join(__dirname, "..", "docs", "CALCULATION-AUDIT.md"), md.join("\n") + "\n");
const withIssues = report.filter((r) => r.issues.length);
console.log(`audited ${report.length} scores; ${report.reduce((a, r) => a + r.evaluated, 0).toLocaleString()} combinations; ${withIssues.length} with issues`);
withIssues.forEach((r) => console.log(" -", r.id, r.issues));
