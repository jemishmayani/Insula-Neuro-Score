"""Fail if the catalogue, shipped score JSON, related links, groups, fixtures, audit evidence and
app defaults disagree. Run after content_src/build_scores.py (CI runs it on every push).
States: implemented (catalog.scores, JSON shipped) | withheld (catalog.withheld, no JSON) | planned (catalog.planned, no JSON)."""
import json, os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), ".."); A = os.path.join(ROOT, "app", "assets", "content")
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(ROOT, "content_src"))
from evidence import EVIDENCE, WITHHELD as EV_WITHHELD
import withheld as withheld_src, itemtypes
cat = json.load(open(os.path.join(A, "catalog.json"))); rel = json.load(open(os.path.join(A, "related.json")))
problems = []
def need(cond, msg):
    if not cond: problems.append(msg)

shipped = {f[:-5] for f in os.listdir(os.path.join(A, "scores")) if f.endswith(".json")}
impl = {s["id"] for s in cat["scores"]}; wh = {w["id"] for w in cat["withheld"]}; pl = {p["id"] for p in cat.get("planned", [])}
need(impl == shipped, f"catalogue scores {sorted(impl - shipped)} have no JSON; JSON {sorted(shipped - impl)} not in catalogue")
need(all(s.get("status") == "implemented" for s in cat["scores"]), "catalog.scores must hold only implemented entries")
need(not (impl & wh) and not (impl & pl) and not (wh & pl), f"an id is in more than one state: {sorted((impl & wh) | (impl & pl) | (wh & pl))}")
need(all(w.get("withheldCategory") and w.get("withheldReason") for w in cat["withheld"]), "every withheld entry needs a category and reason")
for s in cat["scores"]:
    d = json.load(open(os.path.join(A, "scores", s["id"] + ".json")))
    need(d.get("itemType") in itemtypes.TYPE_LABEL and d.get("itemType") == s.get("itemType"), f"{s['id']}: itemType missing or differs between JSON and catalogue")
    bad = [r["id"] for r in d["relatedScores"] if r["id"] not in impl]
    need(not bad, f"{s['id']}: related links to scores not shown in the app: {bad}")
for c in rel["clusters"]:
    need(set(c["members"]) <= impl, f"cluster {c['id']} lists scores not shown: {sorted(set(c['members']) - impl)}")
for c in cat["categories"]:
    mem = c.get("include", []) + [m for g in c.get("groups", []) for m in g["members"]]
    need(set(mem) <= impl, f"group {c['id']} lists scores not shown: {sorted(set(mem) - impl)}")
coll = {c["id"] for c in cat["categories"] if c.get("collection")}
need(set(cat.get("defaultPriorityGroups", [])) <= coll, "defaultPriorityGroups must be collections")
store = open(os.path.join(ROOT, "app", "assets", "js", "store.js")).read()
m = re.search(r'priorityGroups: \[([^\]]*)\]', store)
need(m and [x.strip().strip('"') for x in m.group(1).split(",") if x.strip()] == cat.get("defaultPriorityGroups"), "store.js default priorityGroups differ from catalog.defaultPriorityGroups")
need(set(EVIDENCE) == impl, f"evidence ledger mismatch: missing {sorted(impl - set(EVIDENCE))}, extra {sorted(set(EVIDENCE) - impl)}")
need(set(EV_WITHHELD) <= wh, f"withheld evidence for ids not withheld: {sorted(set(EV_WITHHELD) - wh)}")
src_ids = {s["id"] for s in withheld_src.build()}
need(src_ids <= wh and src_ids == set(EV_WITHHELD), f"content_src/withheld.py ids {sorted(src_ids)} must be withheld and match the withheld evidence")
fx = {f.split(".")[0] for f in os.listdir(os.path.join(ROOT, "tests", "engine", "fixtures"))}
fxw = {f.split(".")[0] for f in os.listdir(os.path.join(ROOT, "tests", "engine", "fixtures-withheld"))}
need(fx == impl, f"fixtures mismatch: missing {sorted(impl - fx)}, extra {sorted(fx - impl)}")
need(fxw <= wh, f"withheld fixtures for ids not withheld: {sorted(fxw - wh)}")
related_src = open(os.path.join(ROOT, "content_src", "related.py")).read()
leaked = [w for w in wh if re.search(r'"%s"' % re.escape(w), related_src)]
need(not leaked, f"content_src/related.py still references withheld ids: {leaked}")
if problems:
    print("CONSISTENCY FAILED:"); [print(" -", p) for p in problems]; sys.exit(1)
print(f"consistent: {len(impl)} implemented (JSON, catalogue, evidence, fixtures agree), {len(wh)} withheld (no JSON; {len(src_ids)} with retained source), {len(pl)} planned")
