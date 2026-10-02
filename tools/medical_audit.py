"""Phase 9 — build docs/MEDICAL-CONTENT-AUDIT.md from the evidence ledger, calculation audit, tests and catalogue.
Run after: node tools/calc_audit.js"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.dirname(__file__)); from evidence import EVIDENCE, HELD
A = os.path.join(ROOT, "app", "assets", "content"); FX = os.path.join(ROOT, "tests", "engine", "fixtures"); FXP = os.path.join(ROOT, "tests", "engine", "fixtures-pending")
cat = json.load(open(os.path.join(A, "catalog.json"))); calc = {r["id"]: r for r in json.load(open(os.path.join(ROOT, "docs", "calc-audit.json")))}
def fixtures(i):
    for d in (FX, FXP):
        p = os.path.join(d, i + ".fixture.json")
        if os.path.exists(p): return len(json.load(open(p))["cases"])
    return 0
mark = lambda v: "⚠ FLAG" if v == "FLAG" else v
rows, flags = [], []
order = [c["id"] for c in cat["categories"]]
impl = sorted([c for c in cat["scores"] if c["status"] == "implemented"], key=lambda c: (order.index(c["category"]), c["abbreviation"].lower()))
for c in impl:
    s = json.load(open(os.path.join(A, "scores", c["id"] + ".json"))); e = EVIDENCE[c["id"]]; ca = calc[c["id"]]
    calcv = "⚠ FLAG" if e["calc"] == "FLAG" else ("Verified" if not ca["issues"] else "⚠ FLAG") + ("" if e["calc"] == "Verified" else " (secondary)")
    rows.append([s["abbreviation"], s["version"]["label"], calcv, mark(e["interp"]), mark(e["pop"]), mark(e["lim"]), mark(e["src"]),
                 f"{fixtures(c['id'])} hand-calculated cases; {ca['evaluated']:,} combinations ({'all' if ca['exhaustive'] else 'sampled + extremes'}); fuzz",
                 "Scripted UI walkthrough (calculator + guide); human clinical testing pending", s["lastReviewed"]])
    for f in e.get("flags", []): flags.append((s["abbreviation"], f))
held_rows = []
for i, e in HELD.items():
    c = next(x for x in cat["scores"] if x["id"] == i)
    held_rows.append([c["abbreviation"], mark(e["calc"]), mark(e["src"]), f"{fixtures(i)} hand-calculated cases retained", c.get("reviewReason", "")])
    for f in e["flags"]: flags.append((c["abbreviation"] + " (held)", f))
calc_issues = sum(len(r["issues"]) for r in calc.values())
needs = [r[0] for r in rows if "FLAG" in " ".join(r[2:7])]
H = ["Score", "Version", "Calculation verified", "Interpretation verified", "Population verified", "Limitations verified", "Source verified", "Automated tests", "Manual tests", "Last reviewed"]
md = ["# Medical content audit (Phase 9)", "",
      "> **Not clinically ready.** Unresolved items below require review by a qualified clinician before any clinical use. Calculation engine and data are internally consistent; source fidelity is verified as described per score.", "",
      "Legend: **Verified** = matched a primary or authoritative source; **Verified (secondary)** = matched several independent secondary sources (primary full text not seen); **Editorial** = guidance text needing clinician review; **⚠ FLAG** = manual verification required.", "",
      "## 1. Content audit", "", "| " + " | ".join(H) + " |", "|" + "---|" * len(H)]
md += ["| " + " | ".join(str(x).replace("|", "/") for x in r) + " |" for r in rows]
md += ["", "### Verified but held back (licensing review)", "", "| Score | Calculation | Source | Tests | Reason |", "|---|---|---|---|---|"]
md += ["| " + " | ".join(r) + " |" for r in held_rows]
md += ["", "## 2. Calculation audit", "",
       f"All {len(calc)} implemented scores were evaluated through the production engine: **{sum(r['evaluated'] for r in calc.values()):,} input combinations** (exhaustive where the input space allows; otherwise a 300,000 sample plus every extreme and one-step variant).",
       "", "For every score the audit confirmed: every component's point values; reachable minimum and maximum equal the declared range; every result state is reached, and only within its stated range; every threshold boundary; missing input → incomplete; not-testable input → blocked or excluded-and-flagged as designed. "
       f"**Internal calculation issues found: {calc_issues}.** Full per-score tables (components, states, boundaries): [CALCULATION-AUDIT.md](CALCULATION-AUDIT.md).", "",
       "Internal consistency does not prove source fidelity: the source column above and the flags below cover that.", "",
       "## 3. Unresolved issues", ""]
md += [f"{k}. **{a}**: {f}" for k, (a, f) in enumerate(flags, 1)]
md += ["", "### Applies to all scores", "- **Limitations, confounders and clinical-context text** is editorial (source-supported, not scoring rules) and requires clinician review.",
       "- **Citations:** DOIs are shown only where confirmed during the project; other bibliographic details (volume, pages) need a reference check.",
       "- **Related-score links** (`content_src/related.py`) were reviewed for clinical logic; no illogical links were found, but they remain editorial.",
       "", "## 4. Scores requiring manual verification", "",
       "**Calculation-affecting (must be resolved before clinical use):**", "- **Revised Tokuhashi**: vertebral-body metastasis item conflict between published tables.", "",
       "**Interpretation or wording (review before release):**"]
md += [f"- **{n}**" for n in needs if n not in ("Revised Tokuhashi",)]
md += [f"- **{a}**" for a in sorted({a for a, _ in flags}) if a not in needs and "held" not in a and a != "Revised Tokuhashi"]
md += ["", "**Secondary-source verification only (confirm against primary full text):** " + ", ".join(r[0] for r in rows if "secondary" in " ".join(r[2:7])) + ".", "",
       "**Not implemented (under review):** " + "; ".join(f"{c['abbreviation']} ({c.get('reviewCategory','')})" for c in cat['scores'] if c['status'] == 'review') + ". Reasons: [CONTENT-AUDIT.md](CONTENT-AUDIT.md).", "",
       "## Corrections made during this audit", "- ICH Score: removed an unverified cohort size from the version text.", "- Hunt & Hess: Grade IV restored to the original wording ('…and vegetative disturbances').",
       "- GCS-P: the 1–8 band now states it is not defined in the original publication.", "- Revised Tokuhashi: calculator notice added about the conflicting item (scoring unchanged pending review).",
       "- ECOG: licensing status updated to public domain (ECOG-ACRIN).", "- RASS: held back pending licensing review (content and tests retained; reinstatement is a one-line change).",
       "- Audit tooling: the calculation audit now also evaluates extremes for sampled input spaces (initially missed NIHSS maximum in a sample)."]
open(os.path.join(ROOT, "docs", "MEDICAL-CONTENT-AUDIT.md"), "w").write("\n".join(md) + "\n")
print(f"{len(rows)} implemented, {len(held_rows)} held, {len(flags)} flags, {calc_issues} calc issues; needs manual: {needs}")
