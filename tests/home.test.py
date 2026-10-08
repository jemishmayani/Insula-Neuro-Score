"""Phase 5 — personalized Home: favorites, recents, priorities, startup, migration, performance."""
import asyncio, json, os, subprocess, sys, time, copy
from playwright.async_api import async_playwright

ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); SHOTS = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(SHOTS, exist_ok=True); PORT = 8768; U = f"http://localhost:{PORT}/index.html"; results = []
def check(n, c, info=""): results.append((n, bool(c))); print(("PASS " if c else "FAIL ") + n + (f"  [{info}]" if info and not c else ""))
KEY = "ins.store.v3"

async def store(pg): return await pg.evaluate(f"JSON.parse(localStorage.getItem('{KEY}') || 'null')")
async def home_ids(pg): return await pg.evaluate("[...document.querySelectorAll('#page-body > .section[id^=home-]')].map(e => e.id)")
async def titles(pg, sec): return [t.split("\n")[0].replace("Placeholder", "").strip() for t in await pg.locator(f"#home-{sec} .home-row .title").all_inner_texts()]
async def go(pg, h, sel=".bottomnav"): await pg.goto(U + h); await pg.wait_for_selector(sel)
async def pick(pg, inp, val): await pg.click(f'.field[data-field="{inp}"] input[value="{val}"] >> xpath=..')
async def complete(pg, sid):
    fills = {"gcs": [("e", "3"), ("v", "4"), ("m", "6")], "mrs": [("grade", "2")],
             "sins": [("location", "2"), ("pain", "1"), ("lesion", "1"), ("alignment", "0"), ("collapse", "0"), ("posterolateral", "0")]}
    await go(pg, f"#/calculate/s/{sid}", ".field")
    for i, v in fills[sid]: await pick(pg, i, v)

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            ctx = await b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=2)
            pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await go(pg, "#/home")

            # ---------- 1. order + empty states ----------
            check("Home order: Search, Priority groups (default quick groups), Favorite scores, Favorite guides, Recent calculators, Recent guides, Priority scores",
                  await pg.evaluate("document.querySelector('#page-body').previousElementSibling.previousElementSibling.classList.contains('searchbar')") and
                  await home_ids(pg) == ["home-priorityGroups", "home-favorites", "home-favoriteGuides", "home-recentCalc", "home-recentGuide", "home-priorityScores"])
            dchips = [c.split("\n")[0].strip() for c in await pg.locator("#home-priorityGroups .chip").all_inner_texts()]
            check("default priority groups on a fresh install: Quick Clinical Examination, Neurotrauma, Vascular", dchips == ["Quick Clinical Examination", "Neurotrauma", "Vascular"], str(dchips))
            empty = await pg.locator("#home-favorites .empty-state").inner_text()
            check("empty state copy: 'No favorite scores yet.' / 'Add a score to Favorites for one-tap access.'", "No favorite scores yet." in empty and "Add a score to Favorites for one-tap access." in empty)
            for sec in ["favoriteGuides", "recentCalc", "recentGuide", "priorityScores"]:
                check(f"empty state for {sec} has title + guidance", await pg.locator(f"#home-{sec} .empty-state h3").count() == 1 and await pg.locator(f"#home-{sec} .empty-state p").count() == 1)
            check("recent calculators empty state states inputs are never stored", "never your inputs" in await pg.locator("#home-recentCalc .empty-state").inner_text())
            await pg.click("#home-favorites .empty-state .btn"); await pg.wait_for_selector(".category-grid")
            check("empty-state action navigates (Browse calculators)", await pg.evaluate("location.hash") == "#/calculate")
            await pg.screenshot(path=f"{SHOTS}/p5_empty.png")

            # ---------- 2. favorites: separate for calculator and guide ----------
            await go(pg, "#/calculate/s/gcs", ".field")
            await pg.click(".appbar [data-act=toggle-favorite]")
            st = await store(pg)
            check("star on calculator → favorite scores only", st["favorites"] == ["gcs"] and st["favoriteGuides"] == [])
            await go(pg, "#/guide/s/nihss", "#g-sources")
            star = pg.locator(".appbar [data-act=toggle-favorite]")
            check("guide star is a separate favorite (unpressed)", await star.get_attribute("aria-pressed") == "false" and "favorite guides" in await star.get_attribute("aria-label"))
            await star.click(); st = await store(pg)
            check("star on guide → favorite guides only", st["favoriteGuides"] == ["nihss"] and st["favorites"] == ["gcs"])
            await go(pg, "#/guide/c/spine", ".score-card")
            await pg.click(".score-card:has-text('SINS') [data-act=toggle-favorite]")
            check("star in Guide list adds to favorite guides", (await store(pg))["favoriteGuides"] == ["nihss", "sins"])
            await go(pg, "#/home")
            check("Favorite scores section shows GCS", await titles(pg, "favorites") == ["GCS"])
            check("Favorite guides section shows NIHSS, SINS", await titles(pg, "favoriteGuides") == ["NIHSS", "SINS"])
            await pg.click("#home-favorites .home-row a.open"); await pg.wait_for_selector(".field")
            ok1 = await pg.evaluate("location.hash") == "#/calculate/s/gcs"
            await go(pg, "#/home"); await pg.click("#home-favorites .home-row a.alt-view"); await pg.wait_for_selector("#g-sources")
            check("favorite score: row opens calculator, second button opens guide (both one tap)", ok1 and await pg.evaluate("location.hash") == "#/guide/s/gcs")
            await go(pg, "#/home"); await pg.click("#home-favoriteGuides .home-row:has-text('NIHSS') a.open"); await pg.wait_for_selector("#g-sources")
            ok2 = await pg.evaluate("location.hash") == "#/guide/s/nihss"
            await go(pg, "#/home"); await pg.click("#home-favoriteGuides .home-row:has-text('NIHSS') a.alt-view"); await pg.wait_for_selector(".field")
            check("favorite guide: row opens guide, second button opens calculator", ok2 and await pg.evaluate("location.hash") == "#/calculate/s/nihss")

            # ---------- 3. recents ----------
            await pg.evaluate(f"(() => {{ const s = JSON.parse(localStorage.getItem('{KEY}')); s.recentCalc = []; s.recentGuide = []; localStorage.setItem('{KEY}', JSON.stringify(s)); }})()")
            await pg.reload(); await go(pg, "#/calculate/s/sins", ".field")
            await pick(pg, "location", "3")
            check("opening/partially filling a calculator does not record use", (await store(pg))["recentCalc"] == [])
            await complete(pg, "gcs")
            rc = (await store(pg))["recentCalc"]
            check("completed calculation recorded with timestamp", len(rc) == 1 and rc[0]["id"] == "gcs" and rc[0]["at"] > 0)
            await complete(pg, "sins"); await complete(pg, "mrs"); await complete(pg, "gcs")
            check("recent calculators newest first, no duplicates", [r["id"] for r in (await store(pg))["recentCalc"]] == ["gcs", "mrs", "sins"])
            await go(pg, "#/calculate/s/gcs", ".field"); await pick(pg, "v", "__nt")
            check("not-testable GCS still counts as a completed use", [r["id"] for r in (await store(pg))["recentCalc"]][0] == "gcs")
            for sid in ["gcs", "nihss", "mrs", "sins", "wfns", "mrc", "ich", "marshall", "rotterdam", "kps", "ecog", "hb"]:
                await go(pg, f"#/guide/s/{sid}", ".detail-head")
            rg = (await store(pg))["recentGuide"]
            check("recent guides capped at 10, newest first", len(rg) == 10 and rg[0]["id"] == "hb" and "gcs" not in [r["id"] for r in rg])
            raw = await pg.evaluate(f"localStorage.getItem('{KEY}')")
            check("history stores ids and times only (no inputs)", all(k not in raw for k in ['"e":', '"answers"', '"location":"', '"grade"']))
            await go(pg, "#/home")
            meta = await pg.locator("#home-recentCalc .home-row .row-meta").first.inner_text()
            check("recent row shows relative time ('Calculated just now')", meta == "Calculated just now", meta)
            check("recent rows offer both views", await pg.locator("#home-recentCalc .home-row a.alt-view").count() == 3)
            await pg.screenshot(path=f"{SHOTS}/p5_populated.png", full_page=True)
            await pg.click("#home-recentCalc [data-act=clear-recent]")
            check("clear recent calculators from Home → empty state", await pg.locator("#home-recentCalc .empty-state").count() == 1 and (await store(pg))["recentCalc"] == [])
            check("clear offers Undo", await pg.locator(".toast .toast-action").inner_text() == "Undo")
            await pg.click(".toast .toast-action")
            check("Undo restores recent calculators", [r["id"] for r in (await store(pg))["recentCalc"]] == ["gcs", "mrs", "sins"] and await pg.locator("#home-recentCalc .home-row").count() == 3)
            await go(pg, "#/settings", "#s-history")
            hist = await pg.locator("#s-history").inner_text()
            check("Settings History shows counts", "3 items" in hist and "10 items" in hist, hist[:120])
            await pg.click("#s-history button:has-text('Clear all history')")
            st = await store(pg)
            check("Clear all history (Settings)", st["recentCalc"] == [] and st["recentGuide"] == [])
            check("favorites untouched by clearing history", st["favorites"] == ["gcs"] and st["favoriteGuides"] == ["nihss", "sins"])

            # ---------- 4. priority scores: GCS, NIHSS, WFNS, SINS above everything ----------
            for sid in ["gcs", "nihss", "wfns", "sins"]:
                await go(pg, f"#/calculate/s/{sid}", "[data-act=toggle-priority]"); await pg.click("[data-act=toggle-priority]")
            check("promote score to Home from its screen", (await store(pg))["priorityScores"] == ["gcs", "nihss", "wfns", "sins"])
            await go(pg, "#/settings", "#s-home")
            for _ in range(5):
                idx = await pg.evaluate("[...document.querySelectorAll('#s-home .reorder-row .label')].map(e=>e.textContent).indexOf('Priority scores')")
                await pg.click(f"#s-home [data-act=move][data-index='{idx}'][data-delta='-1']")
            await go(pg, "#/home")
            ids = await home_ids(pg)
            check("Priority scores can be moved above everything else (first after Search)", ids[0] == "home-priorityScores", str(ids))
            check("priority shows GCS, NIHSS, WFNS, SINS in the user's order", await titles(pg, "priorityScores") == ["GCS", "NIHSS", "WFNS", "SINS"], str(await titles(pg, "priorityScores")))
            await pg.screenshot(path=f"{SHOTS}/p5_priority_top.png")
            await pg.click("#home-priorityScores [data-act=home-edit]")
            check("Edit mode shows reorder/remove controls", await pg.locator("#home-priorityScores .home-row.is-editing").count() == 4 and await pg.locator("#home-priorityScores [data-act=home-remove]").count() == 4)
            await pg.click("#home-priorityScores [data-act=home-move][data-index='3'][data-delta='-1']")
            check("reorder on Home (SINS up)", (await store(pg))["priorityScores"] == ["gcs", "nihss", "sins", "wfns"])
            foc = await pg.evaluate("document.activeElement && document.activeElement.getAttribute('aria-label')")
            check("focus follows the moved item", foc == "Move SINS up", str(foc))
            await pg.screenshot(path=f"{SHOTS}/p5_edit.png")
            await pg.click("#home-priorityScores [data-act=home-remove][data-id=nihss]")
            check("remove from priority area on Home", (await store(pg))["priorityScores"] == ["gcs", "sins", "wfns"])
            await pg.click(".toast .toast-action")
            check("Undo restores removed priority score in place", (await store(pg))["priorityScores"] == ["gcs", "nihss", "sins", "wfns"])
            await pg.click("#home-priorityScores [data-act=home-edit]")
            check("Done exits edit mode", await pg.locator("#home-priorityScores .home-row.is-editing").count() == 0)
            await go(pg, "#/settings", "#s-priority")
            await pg.click("#s-priority [data-act=remove][data-id=wfns]")
            check("remove from priority in Settings", (await store(pg))["priorityScores"] == ["gcs", "nihss", "sins"])

            # ---------- 5. priority groups: promote, reorder, hide ----------
            for cat in ["stroke", "spine", "sah"]:
                await go(pg, f"#/calculate/c/{cat}", "[data-act=promote-group]"); await pg.click("[data-act=promote-group]")
            check("promote category to Home", (await store(pg))["priorityGroups"] == ["quick-exam", "neurotrauma", "vascular", "stroke", "spine", "sah"])
            await go(pg, "#/home")
            chips = [c.split("\n")[0].strip() for c in await pg.locator("#home-priorityGroups .chip").all_inner_texts()]
            check("priority groups shown on Home in order", chips == ["Quick Clinical Examination", "Neurotrauma", "Vascular", "Stroke", "Spine and spinal cord", "Subarachnoid haemorrhage"], str(chips))
            await pg.click("#home-priorityGroups [data-act=home-edit]")
            await pg.click("#home-priorityGroups [data-act=home-move][data-index='5'][data-delta='-1']")
            check("reorder categories on Home", (await store(pg))["priorityGroups"] == ["quick-exam", "neurotrauma", "vascular", "stroke", "sah", "spine"])
            await pg.click("#home-priorityGroups [data-act=home-edit]")
            await go(pg, "#/calculate/c/spine", "[data-act=hide-group]"); await pg.click("[data-act=hide-group]")
            check("hide category → banner on its screen", await pg.locator("text=This group is hidden").count() == 1)
            await go(pg, "#/calculate", ".category-card")
            check("hidden category removed from Calculate list", "Spine and spinal cord" not in await pg.locator(".category-card .name").all_inner_texts())
            await go(pg, "#/home")
            check("hidden category left out of Home priority groups", await pg.locator("#home-priorityGroups .chip:has-text('Spine')").count() == 0 and await pg.locator("#home-priorityGroups .chip").count() == 5)
            await pg.fill("#search", "sins"); await pg.wait_for_timeout(50)
            check("hidden category's scores remain searchable", await pg.locator("#search-results .home-row:has-text('SINS')").count() == 1)
            await go(pg, "#/calculate/c/spine", "[data-act=hide-group]"); await pg.click("[data-act=hide-group]")
            check("show category again", "spine" not in (await store(pg))["hiddenGroups"])
            await go(pg, "#/settings", "#s-groups")
            await pg.click("#s-groups [data-act=move][data-key=groupOrder][data-index='4'][data-delta='-1']")   # Stroke above Consciousness
            await go(pg, "#/calculate", ".category-card")
            names = await pg.locator("#cats .category-card .name").all_inner_texts()
            check("reorder categories in Settings changes Calculate list", names[0] == "Stroke", str(names[:4]))

            # ---------- 6. startup screen remembered ----------
            for choice, h in [("calculate", "#/calculate"), ("guide", "#/guide"), ("home", "#/home")]:
                await go(pg, "#/settings", "#s-startup"); await pg.click(f"[data-act=set-pref][data-key=startup][data-value={choice}]")
                await pg.goto(U); await pg.reload(); await pg.wait_for_selector(".bottomnav"); await pg.wait_for_timeout(150)
                check(f"startup = {choice} remembered across restart", await pg.evaluate("location.hash") == h)

            # ---------- 7. everything persists across restart ----------
            before = await store(pg)
            await pg.reload(); await pg.wait_for_selector(".bottomnav")
            after = await store(pg)
            check("all personalization persists across restart", before == after and after["favorites"] == ["gcs"] and after["priorityScores"] == ["gcs", "nihss", "sins"])
            check("no JS errors during personalization", not errs, errs[:3])

            # ---------- 8. migration v2 → v3 ----------
            async def migrated(v2):
                c2 = await b.new_context(viewport={"width": 412, "height": 915}); m = await c2.new_page()
                await m.goto(U); await m.evaluate("v => { localStorage.clear(); localStorage.setItem('ins.store.v2', JSON.stringify(v)); }", v2)
                await m.reload(); await m.wait_for_selector(".bottomnav")
                s3, gone, ids = await store(m), await m.evaluate("localStorage.getItem('ins.store.v2')"), await home_ids(m)
                await c2.close(); return s3, gone, ids
            v2default = {"v": 2, "theme": "dark", "startup": "guide", "favorites": ["gcs"], "priorityScores": ["nihss"], "priorityGroups": ["stroke"],
                         "recentCalc": ["sins", "gcs"], "recentGuide": ["mrs"], "hiddenGroups": [], "groupOrder": [],
                         "homeSections": [{"id": i, "visible": True} for i in ["priorityScores", "priorityGroups", "favorites", "recentCalc", "recentGuide"]]}
            s3, gone, ids = await migrated(v2default)
            check("v2 → v3: data kept, recents gain timestamps, key replaced", s3["v"] == 3 and s3["favorites"] == ["gcs"] and s3["favoriteGuides"] == [] and
                  s3["recentCalc"] == [{"id": "sins", "at": 0}, {"id": "gcs", "at": 0}] and s3["theme"] == "dark" and gone is None, str(s3)[:200])
            check("v2 default layout → current default order", ids == ["home-priorityGroups", "home-favorites", "home-favoriteGuides", "home-recentCalc", "home-recentGuide", "home-priorityScores"], str(ids))
            v2custom = copy.deepcopy(v2default); v2custom["homeSections"] = [{"id": i, "visible": i != "recentGuide"} for i in ["favorites", "priorityScores", "recentCalc", "priorityGroups", "recentGuide"]]
            s3, gone, ids = await migrated(v2custom)
            check("v2 customised layout kept; favorite guides inserted after favorites", ids == ["home-favorites", "home-favoriteGuides", "home-priorityScores", "home-recentCalc", "home-priorityGroups"], str(ids))

            # ---------- 9. performance with a large library ----------
            real = json.load(open(os.path.join(ROOT, "content", "catalog.json")))
            big = copy.deepcopy(real); cats = [c["id"] for c in real["categories"]]
            for k in range(2000):
                big["scores"].append({"id": f"syn-{k}", "abbreviation": f"SYN{k}", "name": f"Synthetic score {k}", "category": cats[k % len(cats)], "summary": f"Synthetic test entry {k}",
                                      "status": "implemented" if k < 20 else "placeholder"})
            gcs = json.load(open(os.path.join(ROOT, "content", "scores", "gcs.json")))
            pc = await b.new_context(viewport={"width": 412, "height": 915}); pp = await pc.new_page(); reqs = []; perrs = []
            pp.on("request", lambda r: reqs.append(r.url)); pp.on("pageerror", lambda e: perrs.append(str(e)))
            async def cat_route(route): await route.fulfill(status=200, content_type="application/json", body=json.dumps(big))
            async def syn_route(route):
                sid = route.request.url.rsplit("/", 1)[1].replace(".json", ""); g = copy.deepcopy(gcs); g["id"] = sid
                await route.fulfill(status=200, content_type="application/json", body=json.dumps(g))
            await pp.route("**/content/catalog.json", cat_route); await pp.route("**/content/scores/syn-*.json", syn_route)
            await pp.goto(U); await pp.wait_for_selector(".bottomnav")   # let the first load finish its own store write before seeding
            await pp.evaluate(f"""localStorage.setItem('{KEY}', JSON.stringify({{v:3, favorites: Array.from({{length: 60}}, (_, i) => 'syn-' + i),
              favoriteGuides: Array.from({{length: 60}}, (_, i) => 'syn-' + (100 + i)), recentCalc: Array.from({{length: 10}}, (_, i) => ({{id: 'syn-' + (200 + i), at: Date.now() - i * 60000}})),
              priorityScores: ['gcs', 'nihss', 'syn-5'], priorityGroups: ['stroke', 'spine']}}))""")
            reqs.clear(); t0 = time.time(); await pp.reload(); await pp.wait_for_selector("#home-favorites .home-row"); load_ms = (time.time() - t0) * 1000
            check(f"large library ({len(big['scores'])} scores): Home ready in {load_ms:.0f} ms (< 1500)", load_ms < 1500)
            check("startup + Home load no score or guide documents", not any("/content/scores/" in u for u in reqs), [u for u in reqs if "/content/scores/" in u][:3])
            render_ms = await pp.evaluate("""() => new Promise(res => { location.hash = '#/calculate'; setTimeout(() => {
                const t0 = performance.now(); addEventListener('hashchange', () => res(performance.now() - t0), { once: true }); location.hash = '#/home'; }, 50); })""")
            check(f"Home re-render with 60+60 favorites, 10 recents: {render_ms:.1f} ms (< 150)", render_ms < 150)
            times = await pp.evaluate("""() => { const el = document.querySelector('#search'), out = [];
                for (const q of ['s', 'sy', 'syn1', 'synthetic score 19', 'gcs', 'zzz']) { const t0 = performance.now(); el.value = q; el.dispatchEvent(new Event('input', { bubbles: true })); out.push(performance.now() - t0); }
                return out; }""")
            check(f"search across {len(big['scores'])} scores per keystroke ≤ 50 ms (max {max(times):.1f} ms)", max(times) <= 50, str([round(t, 1) for t in times]))
            await pp.evaluate("document.querySelector('#search').value='synthetic'; document.querySelector('#search').dispatchEvent(new Event('input',{bubbles:true}))")
            check("broad search renders at most 50 rows", await pp.locator("#search-results .home-row").count() == 50)
            for k in range(20):
                await pp.goto(U + f"#/calculate/s/syn-{k}"); await pp.wait_for_selector(".field")
            cache = await pp.evaluate("window.__insDebug.cacheSize()")
            check(f"documents load on demand and the in-memory cache stays bounded ({cache} ≤ 12 after opening 20)", cache <= 12)
            check("no JS errors with large library", not perrs, perrs[:2])

            # ---------- 10. layouts ----------
            for name, vp in [("small", {"width": 320, "height": 640}), ("tablet", {"width": 1280, "height": 900})]:
                c3 = await b.new_context(viewport=vp, device_scale_factor=2 if name == "small" else 1, color_scheme="dark" if name == "tablet" else "light"); q = await c3.new_page()
                await q.goto(U); await q.evaluate(f"""localStorage.setItem('{KEY}', JSON.stringify({{v:3, favorites:['gcs','sins'], favoriteGuides:['nihss'],
                  recentCalc:[{{id:'gcs',at:Date.now()-120000}},{{id:'mrs',at:Date.now()-7200000}}], recentGuide:[{{id:'sins',at:Date.now()-90000000}}],
                  priorityScores:['gcs','nihss','wfns','sins'], priorityGroups:['stroke','spine'],
                  homeSections:[{{id:'priorityScores',visible:true}},{{id:'favorites',visible:true}},{{id:'favoriteGuides',visible:true}},{{id:'recentCalc',visible:true}},{{id:'recentGuide',visible:true}},{{id:'priorityGroups',visible:true}}]}}))""")
                await q.reload(); await q.wait_for_selector("#home-priorityScores .home-row")
                check(f"{name}: Home has no horizontal overflow", await q.evaluate("document.documentElement.scrollWidth <= innerWidth"))
                await q.click("#home-priorityScores [data-act=home-edit]")
                check(f"{name}: edit controls fit (no overflow)", await q.evaluate("document.documentElement.scrollWidth <= innerWidth"))
                await q.click("#home-priorityScores [data-act=home-edit]")
                await q.screenshot(path=f"{SHOTS}/p5_{name}.png", full_page=True); await c3.close()
            await b.close()
    finally:
        srv.terminate()
    f = [n for n, ok in results if not ok]; print(f"\n{len(results) - len(f)} passed, {len(f)} failed" + (": " + "; ".join(f) if f else "")); sys.exit(1 if f else 0)

asyncio.run(main())
