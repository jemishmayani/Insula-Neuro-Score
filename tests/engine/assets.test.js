const test = require("node:test"), assert = require("node:assert/strict");
const fs = require("fs"), path = require("path");
const { ROOT } = require("./helpers");
/* Phase 8: every shipped script must parse — a syntax error would stop the app from starting. */
test("all shipped JavaScript parses", () => {
  const files = ["js/store.js", "js/ui.js", "js/calculator.js", "js/app.js", "js/engine/expr.js", "js/engine/inputs.js", "js/engine/insights.js", "js/engine/engine.js"];
  for (const f of files) assert.doesNotThrow(() => new Function(fs.readFileSync(path.join(ROOT, f), "utf8")), f);
  const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
  for (const m of html.matchAll(/<script src="([^"]+)"/g)) assert.ok(fs.existsSync(path.join(ROOT, m[1])), "index.html references missing " + m[1]);
});
test("all shipped JSON parses", () => {
  const walk = (d) => fs.readdirSync(d).flatMap((f) => { const p = path.join(d, f); return fs.statSync(p).isDirectory() ? walk(p) : [p]; });
  for (const f of walk(path.join(ROOT, "content")).filter((f) => f.endsWith(".json"))) assert.doesNotThrow(() => JSON.parse(fs.readFileSync(f, "utf8")), f);
});
