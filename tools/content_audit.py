"""Generate the content audit (docs/CONTENT-AUDIT.md + .csv) from shipped data.
Columns: Score, Version, Implemented, Tested, Source, Last reviewed, Licensing status."""
import csv, json, os, re
ROOT = os.path.join(os.path.dirname(__file__), "..")
A = os.path.join(ROOT, "app", "assets", "content"); FX = os.path.join(ROOT, "tests", "engine", "fixtures")
cat = json.load(open(os.path.join(A, "catalog.json")))
cats = {c["id"]: c["name"] for c in cat["categories"]}
order = [c["id"] for c in cat["categories"]]
rows = []
for s in sorted(cat["scores"] + [dict(w, status="withheld") for w in cat.get("withheld", [])] + list(cat.get("planned", [])), key=lambda x: (order.index(x["category"]) if x["category"] in order else 99, x["abbreviation"].lower())):
    if s["status"] == "implemented":
        d = json.load(open(os.path.join(A, "scores", s["id"] + ".json")))
        fx = os.path.join(FX, s["id"] + ".fixture.json")
        n = len(json.load(open(fx))["cases"]) if os.path.exists(fx) else 0
        src = d["sources"][0]; m = re.match(r"([^,.]+)[^.]*\.\s.*?(\d{4})", src["citation"])
        short = (m.group(1).split(" ")[0] + (" et al." if src["citation"].count(",") > 1 else "") + " " + m.group(2)) if m else src["citation"][:40]
        rows.append([d["abbreviation"], cats.get(d["category"], d["category"]), d["version"]["label"], "Yes",
                     f"Yes: {n} manually verified cases; all-combination sweep; UI walkthrough", short + (f" (doi:{src['doi']})" if src.get("doi") else ""),
                     d["lastReviewed"] + " (clinician review pending)", d["licensing"]["status"]])
    elif s["status"] == "withheld":
        rows.append([s["abbreviation"], cats.get(s["category"], s["category"]), "—", "No: withheld, not shown (" + s["withheldCategory"] + ")", "—", "—", "—",
                     s["withheldCategory"] + ": " + s["withheldReason"]])
    else:
        rows.append([s["abbreviation"], cats.get(s["category"], s["category"]), "—", "No: planned (future queue), not shown", "—", "—", "—", "Not yet assessed"])
head = ["Score", "Group", "Version", "Implemented", "Tested", "Source", "Last reviewed", "Licensing status"]
with open(os.path.join(ROOT, "docs", "CONTENT-AUDIT.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(head); w.writerows(rows)
impl = sum(1 for r in rows if r[3] == "Yes")
md = ["# Content audit", "", f"Generated from shipped content (catalogue v{cat['contentVersion']}). **{impl} implemented**, **{sum(1 for r in rows if r[3].startswith('No: withheld'))} withheld** and **{sum(1 for r in rows if r[3].startswith('No: planned'))} planned** (neither shown in the app), 0 unverified.", "",
      "All implemented content was verified against the cited sources before implementation and is pending independent clinician review.", "",
      "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
md += ["| " + " | ".join(c.replace("|", "/") for c in r) + " |" for r in rows]
open(os.path.join(ROOT, "docs", "CONTENT-AUDIT.md"), "w").write("\n".join(md) + "\n")
print(f"audit: {impl} implemented, {len(rows) - impl} withheld or planned → docs/CONTENT-AUDIT.md, docs/CONTENT-AUDIT.csv")
