"""Phase 6 / v0.10 — walk every implemented calculator and guide in the real UI; check the active catalogue holds no under-review entries."""
import asyncio, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); SHOTS = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(SHOTS, exist_ok=True); PORT = 8769; U = f"http://localhost:{PORT}/index.html"; results = []
def check(n, c, info=""): results.append((n, bool(c))); print(("PASS " if c else "FAIL ") + n + (f"  [{info}]" if info and not c else ""))
CAT = json.load(open(os.path.join(ROOT, "content", "catalog.json")))
IMPL = [s for s in CAT["scores"] if s["status"] == "implemented"]; WITHHELD = CAT.get("withheld", []); EXAM = next(c for c in CAT["categories"] if c["id"] == "exam")
SHOT_IDS = {"aspects", "abcd2", "ich", "marshall", "rts", "iss", "rtokuhashi", "gose", "mrcss", "mts", "gr", "lawtonyoung"}

async def fill_all(pg, sid):
    score = json.load(open(os.path.join(ROOT, "content", "scores", sid + ".json")))
    for d in score["inputDefinitions"]:
        f = f'.field[data-field="{d["id"]}"]'
        if d["type"] in ("single", "yesno"):
            await pg.locator(f'{f} input[type=radio]:not([value="__nt"])').nth(min(1, len(d.get("options", [1, 1])) - 1)).locator("xpath=..").click()
        elif d["type"] == "multi":
            await pg.locator(f"{f} input[type=checkbox]").first.locator("xpath=..").click()
        elif d["type"] in ("integer", "number", "decimal"):
            await pg.fill(f"#in-{d['id']}", str(d["max"] if sid == "rts" else (d["min"] + d["max"]) // 2))
        elif d["type"] == "dropdown":
            await pg.select_option(f"#in-{d['id']}", index=1)
    return score

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await (await b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=2)).new_page()
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(U); await pg.wait_for_selector(".bottomnav")
            check(f"catalogue: {len(IMPL)} implemented, only implemented scores listed ({len(WITHHELD)} withheld, {len(CAT.get('planned', []))} planned kept out of the app)",
                  {s["id"] for s in IMPL} == {f[:-5] for f in os.listdir(os.path.join(ROOT, "content", "scores"))} and len(IMPL) == len(CAT["scores"]))
            for s in IMPL:
                sid = s["id"]
                await pg.goto(U + f"#/calculate/s/{sid}"); await pg.wait_for_selector(".field")
                score = await fill_all(pg, sid)
                await pg.wait_for_timeout(30)
                st = await pg.evaluate("(() => { const c = document.querySelector('#result .result-card'); return { tone: [...c.classList].find(x => x.startsWith('tone-')), value: c.querySelector('.value').textContent, type: (c.querySelector('.result-type')||{}).textContent }; })()")
                blocks = await pg.evaluate("[...document.querySelectorAll('#result [data-block]')].map(b => b.dataset.block)")
                ok_calc = st["tone"] != "tone-incomplete" or sid in ("wfns", "mfisher")
                check(f"{sid}: calculator completes ({st['value']}, {st['type']}), insight sections present", ok_calc and st["type"] and "breakdown" in blocks and "limitation" in blocks, str(st) + str(blocks))
                if sid in SHOT_IDS:
                    await pg.click("#result >> text=Breakdown"); await pg.screenshot(path=f"{SHOTS}/p6_{sid}.png")
                await pg.click('.segmented a:has-text("Guide")'); await pg.wait_for_selector("#g-sources")
                n = await pg.locator(".section-card").count(); srcs = await pg.locator("#g-sources li").count()
                ver = await pg.locator("#g-version").inner_text()
                check(f"{sid}: guide has 14 sections, version shown, {srcs} source(s)", n == 14 and srcs >= 1 and score["version"]["label"] in ver)
            # ---------- v0.10: no under-review cards anywhere; withheld scores unreachable ----------
            seen_review = []
            for c in CAT["categories"]:
                for tab in ("calculate", "guide"):
                    await pg.goto(U + f"#/{tab}/c/{c['id']}"); await pg.wait_for_selector(".score-card")
                    if "under review" in (await pg.locator("main").inner_text()).lower(): seen_review.append(f"{tab}/{c['id']}")
            check("no 'Under review' text in any Calculate or Guide group list", not seen_review, str(seen_review))
            for w in WITHHELD:
                await pg.goto(U + f"#/calculate/s/{w['id']}"); await pg.wait_for_selector("main")
                await pg.goto(U + "#/calculate"); await pg.wait_for_selector("#search"); await pg.fill("#search", w["abbreviation"]); await pg.wait_for_timeout(60)
                titles = [t.split("\n")[0].strip() for t in await pg.locator("#search-results .score-card .title").all_inner_texts()]
                check(f"withheld {w['abbreviation']}: not in search results", w["abbreviation"] not in [t.replace("Calculator", "").strip() for t in titles], str(titles))
            # ---------- v0.10: Neurosurgical Examination & Grades ----------
            await pg.goto(U + "#/home"); await pg.wait_for_selector("#search"); await pg.goto(U + "#/calculate"); await pg.wait_for_selector(".category-card")
            check("root list section is titled 'Scores & Grades'", "Scores & Grades" in await pg.locator("#cats").inner_text())
            check("'Neurosurgical Examination & Grades' group listed", await pg.locator('.category-card:has-text("Neurosurgical Examination & Grades")').count() == 1)
            await pg.goto(U + "#/calculate/c/exam"); await pg.wait_for_selector(".score-card")
            heads = [h.strip() for h in await pg.locator(".group-h").all_inner_texts()]
            check("exam group shows its sub-sections in order", heads == [g["title"] for g in EXAM["groups"]], str(heads))
            ids = await pg.evaluate("[...document.querySelectorAll('main .score-card a.open')].map(a => a.getAttribute('href').split('/').pop())")
            expect = [m for g in EXAM["groups"] for m in g["members"]]
            check(f"exam group lists all {len(expect)} entries (incl. cross-listed KPS, ECOG)", ids == expect, str(ids))
            await pg.screenshot(path=f"{SHOTS}/v10_exam_group.png", full_page=True)
            await pg.goto(U + "#/calculate/c/tbi"); await pg.wait_for_selector(".score-card")
            check("Markwalder also listed under Traumatic brain injury", await pg.locator('main .score-card a.open[href$="/markwalder"]').count() == 1)
            await pg.goto(U + "#/calculate"); await pg.fill("#search", "spasticity"); await pg.wait_for_timeout(60)
            r = [t.split("\n")[0].replace("Calculator", "").strip() for t in await pg.locator("#search-results .score-card .title").all_inner_texts()]
            check("search 'spasticity' finds MAS and MTS", "MAS" in r and "MTS" in r, str(r))
            await pg.fill("#search", "avm"); await pg.wait_for_timeout(60)
            r = [t.split("\n")[0].replace("Calculator", "").strip() for t in await pg.locator("#search-results .score-card .title").all_inner_texts()]
            check("search 'avm' finds Spetzler-Martin and Lawton-Young", "Spetzler-Martin" in r and "Lawton-Young" in r, str(r))
            # favourite + recent work for a new grade
            await pg.goto(U + "#/calculate/c/exam"); await pg.wait_for_selector(".score-card")
            await pg.locator('main .score-card:has(a.open[href$="/hb"]) [data-act="toggle-favorite"]').first.click()
            await pg.goto(U + "#/calculate/s/hb"); await pg.wait_for_selector(".field"); await fill_all(pg, "hb"); await pg.wait_for_timeout(1200)
            st = await pg.evaluate("JSON.parse(localStorage.getItem('ins.store.v3'))")
            check("favourite and recent calculator recorded for a new grade (House-Brackmann)", "hb" in st["favorites"] and any(r["id"] == "hb" for r in st["recentCalc"]), str({k: st[k] for k in ("favorites", "recentCalc")}))
            await pg.goto(U + "#/home"); await pg.wait_for_selector("#home-favorites")
            check("Home shows the new favourite", await pg.locator('#home-favorites a.open[href$="/hb"]').count() == 1)
            check("no JS errors across the library", not errs, errs[:3])
            await b.close()
    finally: srv.terminate()
    f = [n for n, ok in results if not ok]; print(f"\n{len(results) - len(f)} passed, {len(f)} failed" + (": " + "; ".join(f) if f else "")); sys.exit(1 if f else 0)
asyncio.run(main())
