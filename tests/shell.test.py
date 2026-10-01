"""Insula Neuro Score — Phase 1 shell tests (Playwright, Chromium).
Run: python3 tests/shell.test.py   (serves app/assets on localhost)"""
import asyncio, os, re, subprocess, sys, time, glob, json
from playwright.async_api import async_playwright

ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets")
SHOTS = os.path.join(os.path.dirname(__file__), "shots"); os.makedirs(SHOTS, exist_ok=True)
PORT = 8766; U = f"http://localhost:{PORT}/index.html"
results = []
def check(name, cond, info=""):
    results.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info and not cond else ""))

# ---------- static checks ----------
def static_checks():
    hexre = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(")
    offenders = []
    for f in glob.glob(ROOT + "/js/*.js") + [ROOT + "/css/components.css", ROOT + "/index.html"]:
        for i, line in enumerate(open(f), 1):
            if hexre.search(line): offenders.append(f"{os.path.basename(f)}:{i}")
    check("no colour values outside tokens.css", not offenders, ", ".join(offenders))
    js = open(ROOT + "/js/app.js").read() + open(ROOT + "/js/ui.js").read()
    check("no network APIs besides local catalogue fetch", js.count("fetch(") == 1 and "XMLHttpRequest" not in js and "WebSocket" not in js)
    comps = ["AppBar","BottomNavigation","SearchBar","ScoreCard","CategoryCard","ResultCard","StatusBadge","SectionCard","PrimaryButton","SecondaryButton","Toggle","EmptyState","InfoBanner","WarningBanner","ErrorState","LoadingState"]
    ui = open(ROOT + "/js/ui.js").read()
    missing = [c for c in comps if ("function " + c + "(") not in ui]
    check("all 16 design-system components exist", not missing, ", ".join(missing))
    cat = json.load(open(ROOT + "/content/catalog.json"))
    check("catalogue is placeholder-only (no scoring rules)", all(s.get("status") == "placeholder" and "inputs" not in s for s in cat["scores"]))

async def no_overflow(pg):
    return await pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")

async def main():
    static_checks()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()

            async def newpage(w, h, scheme="light", storage=None):
                ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, color_scheme=scheme)
                pg = await ctx.new_page(); pg.errs = []; pg.reqs = []
                pg.on("pageerror", lambda e: pg.errs.append(str(e)))
                pg.on("console", lambda m: m.type == "error" and pg.errs.append(m.text))
                pg.on("request", lambda r: pg.reqs.append(r.url))
                if storage is not None:
                    await pg.goto(U); await pg.evaluate("s => { localStorage.clear(); for (const k in s) localStorage.setItem(k, s[k]); }", storage)
                await pg.goto(U); await pg.wait_for_selector(".bottomnav")
                return pg
            back = lambda pg: pg.evaluate("window.handleBack()")
            hashof = lambda pg: pg.evaluate("location.hash")

            # ============ Phone (large) ============
            pg = await newpage(412, 915, storage={})
            check("startup default = Home", await hashof(pg) == "#/home")
            await pg.screenshot(path=f"{SHOTS}/01_home_light.png")
            for sid in ["priorityScores", "priorityGroups", "favorites", "recentCalc", "recentGuide"]:
                check(f"home section present: {sid}", await pg.locator(f"#home-{sid}").count() == 1)
            check("home placeholders realistic (GCS, NIHSS in priority)", await pg.locator("#home-priorityScores >> text=NIHSS").count() == 1)
            check("empty favourites shows EmptyState", await pg.locator("#home-favorites .empty-state").count() == 1)
            check("settings in top-right app bar", await pg.locator(".appbar a[aria-label=Settings]").count() == 1)
            check("bottom nav has Home|Calculate|Guide", [t.strip() for t in await pg.locator(".bottomnav a").all_inner_texts()] == ["Home", "Calculate", "Guide"])

            # search
            await pg.fill("#search", "sedat"); await pg.wait_for_timeout(50)
            check("search by topic (sedation→RASS)", await pg.locator("#search-results >> text=RASS").count() >= 1)
            await pg.fill("#search", "wfns"); check("search exact abbreviation first", (await pg.locator("#search-results .score-card .title").first.inner_text()).startswith("WFNS"))
            await pg.fill("#search", "qqqq"); check("search no-results EmptyState", await pg.locator("#search-results .empty-state").count() == 1)
            await pg.click("[data-act=clear-search]"); check("clear search restores page", await pg.locator("#page-body").is_visible())

            # ---- navigation & back stack ----
            await pg.click(".bottomnav >> text=Calculate"); await pg.wait_for_selector(".category-grid")
            check("Calculate shows category cards", await pg.locator(".category-card").count() == 9)
            await pg.screenshot(path=f"{SHOTS}/02_calculate.png")
            await pg.click(".category-card:has-text('Subarachnoid')"); await pg.wait_for_selector(".score-card")
            check("category → score list", await hashof(pg) == "#/calculate/c/sah" and await pg.locator(".score-card").count() == 4)
            await pg.click(".score-card a:has-text('WFNS')"); await pg.wait_for_selector(".segmented")
            check("score detail (calculate tab)", await hashof(pg) == "#/calculate/s/wfns")
            check("detail shows placeholder ResultCard + WarningBanner", await pg.locator(".result-card.tone-incomplete").count() == 1 and await pg.locator(".banner.tone-warning").count() == 1)
            await pg.screenshot(path=f"{SHOTS}/03_detail_calc.png")
            await pg.click(".segmented >> text=Guide"); await pg.wait_for_selector(".section-card")
            check("Calculate→Guide toggle", await hashof(pg) == "#/guide/s/wfns" and await pg.locator(".section-card").count() == 15)
            check("guide has 'Calculate this score →'", await pg.locator("text=Calculate this score →").count() == 2)
            await pg.screenshot(path=f"{SHOTS}/04_detail_guide.png")
            await pg.click("a.btn-primary >> nth=0"); await pg.wait_for_selector(".result-card")
            check("Guide→Calculate navigation", await hashof(pg) == "#/calculate/s/wfns")
            r = await back(pg); await pg.wait_for_timeout(150)
            check("back from detail → category (toggle did not add history)", r is True and await hashof(pg) == "#/calculate/c/sah", await hashof(pg))
            r = await back(pg); await pg.wait_for_timeout(150)
            check("back → Calculate root", await hashof(pg) == "#/calculate")
            r = await back(pg); await pg.wait_for_timeout(150)
            check("back from tab root → startup tab (Home)", r is True and await hashof(pg) == "#/home")
            r = await back(pg)
            check("back at startup root exits app (returns false)", r is False)
            # deep link back: open detail directly, back goes to parent
            await pg.goto(U + "#/guide/s/gcs"); await pg.wait_for_selector(".section-card")
            await back(pg); await pg.wait_for_timeout(150)
            check("deep-linked detail back → its category", await hashof(pg) == "#/guide/c/consciousness")
            # app bar back button
            await pg.click(".appbar [data-act=back]"); await pg.wait_for_timeout(150)
            check("app bar back button", await hashof(pg) == "#/guide")
            # unknown route
            await pg.goto(U + "#/calculate/s/doesnotexist"); await pg.wait_for_selector(".error-state")
            check("unknown score → ErrorState", await pg.locator(".error-state").count() == 1)

            # ---- favourites ----
            await pg.goto(U + "#/calculate/c/stroke"); await pg.wait_for_selector(".score-card")
            star = pg.locator(".score-card:has-text('NIHSS') [data-act=toggle-favorite]")
            await star.click()
            check("favourite toggles aria-pressed", await star.get_attribute("aria-pressed") == "true")
            await pg.reload(); await pg.wait_for_selector(".score-card")
            check("favourite persists after reload", await pg.locator(".score-card:has-text('NIHSS') [data-act=toggle-favorite]").get_attribute("aria-pressed") == "true")
            await pg.goto(U + "#/calculate/s/nihss"); await pg.wait_for_selector(".appbar")
            check("detail star reflects favourite", await pg.locator(".appbar [data-act=toggle-favorite]").get_attribute("aria-pressed") == "true")
            await pg.click("[data-act=toggle-priority]")
            await pg.goto(U + "#/home"); await pg.wait_for_selector("#home-favorites")
            check("favourite shown on Home", await pg.locator("#home-favorites >> text=NIHSS").count() == 1)
            check("recent calculators recorded", await pg.locator("#home-recentCalc >> text=NIHSS").count() == 1)
            check("recent guides recorded", await pg.locator("#home-recentGuide >> text=GCS").count() == 1)
            check("toggle priority from detail removes NIHSS from priority", await pg.locator("#home-priorityScores >> text=NIHSS").count() == 0)

            # ---- settings: reordering ----
            await pg.goto(U + "#/settings"); await pg.wait_for_selector("#s-priority")
            await pg.screenshot(path=f"{SHOTS}/05_settings.png", full_page=True)
            before = await pg.evaluate("JSON.parse(localStorage.getItem('ins.store.v2')).priorityScores")
            await pg.click("#s-priority [data-act=move][data-index='0'][data-delta='1']")
            after = await pg.evaluate("JSON.parse(localStorage.getItem('ins.store.v2')).priorityScores")
            check("reorder priority scores", after == [before[1], before[0]] + before[2:], f"{before}→{after}")
            focused = await pg.evaluate("document.activeElement && document.activeElement.getAttribute('aria-label')")
            check("focus follows moved item", focused is not None and "Move" in focused, str(focused))
            await pg.reload(); await pg.wait_for_selector("#s-priority")
            check("reorder persists after reload", await pg.evaluate("JSON.parse(localStorage.getItem('ins.store.v2')).priorityScores") == after)
            await pg.goto(U + "#/home"); await pg.wait_for_selector("#home-priorityScores")
            firsts = await pg.locator("#home-priorityScores .score-card .title").all_inner_texts()
            check("Home reflects priority order", firsts[0].startswith(score_abbr := {"gcs":"GCS","ich":"ICH Score","wfns":"WFNS","nihss":"NIHSS"}[after[0]]), f"{firsts}")
            # home section reorder + visibility
            await pg.goto(U + "#/settings"); await pg.wait_for_selector("#s-home")
            await pg.click("#s-home [data-act=move][data-index='0'][data-delta='1']")
            await pg.click("#s-home input[data-id=recentGuide]")
            await pg.goto(U + "#/home"); await pg.wait_for_selector(".section")
            ids = await pg.evaluate("[...document.querySelectorAll('#page-body > .section[id^=home-]')].map(e=>e.id)")
            check("Home section order + visibility applied", ids[:2] == ["home-priorityGroups", "home-priorityScores"] and "home-recentGuide" not in ids, str(ids))
            # group order & hide
            await pg.goto(U + "#/settings"); await pg.wait_for_selector("#s-groups")
            await pg.click("#s-groups [data-act=move][data-index='1'][data-delta='-1']")
            await pg.click("#s-groups input[data-id=oncology]")
            await pg.goto(U + "#/calculate"); await pg.wait_for_selector(".category-card")
            names = await pg.locator(".category-card .name").all_inner_texts()
            check("group order applied", names[0] == "Stroke", str(names[:3]))
            check("hidden group removed from Calculate", "Neuro-oncology" not in names and await pg.locator("text=1 hidden group").count() == 1)
            await pg.goto(U + "#/guide"); await pg.wait_for_selector(".category-card")
            check("hidden group removed from Guide", "Neuro-oncology" not in await pg.locator(".category-card .name").all_inner_texts())
            # pickers
            await pg.goto(U + "#/settings/pick/priorityGroups"); await pg.wait_for_selector("input[data-act=pick]")
            await pg.click("#p-spine"); await pg.goto(U + "#/home"); await pg.wait_for_selector("#home-priorityGroups")
            check("priority group picker adds chip", await pg.locator("#home-priorityGroups >> text=Spine and spinal cord").count() == 1)
            await pg.goto(U + "#/settings"); await pg.wait_for_selector("#s-favorites")
            await pg.click("#s-favorites [data-act=remove]")
            check("remove favourite in Settings", await pg.evaluate("JSON.parse(localStorage.getItem('ins.store.v2')).favorites.length") == 0)

            # ---- themes ----
            bg = lambda: pg.evaluate("getComputedStyle(document.body).backgroundColor")
            light_bg = await bg()
            await pg.click("[data-act=set-pref][data-key=theme][data-value=dark]")
            check("dark mode applied", await pg.evaluate("document.documentElement.dataset.theme") == "dark" and await bg() != light_bg)
            await pg.reload(); await pg.wait_for_selector(".segmented")
            check("dark mode persists", await pg.evaluate("document.documentElement.dataset.theme") == "dark")
            await pg.screenshot(path=f"{SHOTS}/06_settings_dark.png")
            for path, name in [("#/home", "07_home_dark"), ("#/calculate/s/gcs", "08_detail_dark"), ("#/guide/s/gcs", "09_guide_dark")]:
                await pg.goto(U + path); await pg.wait_for_selector(".bottomnav"); await pg.screenshot(path=f"{SHOTS}/{name}.png")
            await pg.goto(U + "#/settings"); await pg.wait_for_selector(".segmented")
            await pg.click("[data-act=set-pref][data-key=theme][data-value=light]")
            check("light mode applied", await pg.evaluate("document.documentElement.dataset.theme") == "light" and await bg() == light_bg)
            await pg.click("#hc"); check("high contrast applied", await pg.evaluate("document.documentElement.dataset.contrast") == "high")
            await pg.click("#hc")
            # ---- startup preference ----
            await pg.click("[data-act=set-pref][data-key=startup][data-value=guide]")
            await pg.goto(U); await pg.wait_for_timeout(400)
            check("startup preference = Guide", await hashof(pg) == "#/guide")
            check("back from startup root exits", await back(pg) is False)
            await pg.click(".bottomnav >> text=Home"); await pg.wait_for_timeout(100)
            await back(pg); await pg.wait_for_timeout(150)
            check("back from Home → startup tab (Guide)", await hashof(pg) == "#/guide")
            check("no network beyond app files", all(u.startswith(f"http://localhost:{PORT}/") for u in pg.reqs), [u for u in pg.reqs if "localhost" not in u][:3])
            check("no JS errors (phone)", not pg.errs, pg.errs[:3])

            # ---- system theme ----
            dp = await newpage(412, 915, scheme="dark", storage={})
            check("System theme follows device dark mode", await dp.evaluate("document.documentElement.dataset.theme") == "dark")
            await dp.emulate_media(color_scheme="light"); await dp.wait_for_timeout(100)
            check("System theme reacts to device change", await dp.evaluate("document.documentElement.dataset.theme") == "light")

            # ---- migration from v0.1.0 ----
            legacy = json.dumps({"theme": "dark", "startup": "calc", "pinned": ["mrs", "rass"], "favGuides": ["four"], "homeGroups": ["sah"], "hiddenGroups": ["spine"]})
            mp = await newpage(412, 915, storage={"ins.prefs": legacy})
            st = await mp.evaluate("JSON.parse(localStorage.getItem('ins.store.v2'))")
            check("migrates v0.1.0 preferences", st["priorityScores"] == ["mrs", "rass"] and st["favorites"] == ["four"] and st["startup"] == "calculate" and st["theme"] == "dark" and st["hiddenGroups"] == ["spine"], str(st))
            check("legacy key removed after migration", await mp.evaluate("localStorage.getItem('ins.prefs')") is None)
            # corrupt storage resilience
            cp = await newpage(412, 915, storage={"ins.store.v2": "{not json"})
            check("corrupt storage falls back to defaults", await hashof(cp) == "#/home" and not cp.errs, cp.errs[:2])

            # ---- loading / error states ----
            ctx = await b.new_context(viewport={"width": 412, "height": 915}); ep = await ctx.new_page()
            await ep.route("**/content/catalog.json", lambda route: route.abort())
            await ep.goto(U); await ep.wait_for_selector(".error-state")
            check("catalogue failure → ErrorState with retry", await ep.locator("[data-act=retry]").count() == 1)
            await ep.screenshot(path=f"{SHOTS}/10_error.png")
            await ep.unroute("**/content/catalog.json"); await ep.click("[data-act=retry]"); await ep.wait_for_selector(".bottomnav")
            check("retry recovers", await ep.locator(".bottomnav").count() == 1)
            slow = await b.new_context(viewport={"width": 412, "height": 915}); sp = await slow.new_page()
            async def delay(route): await asyncio.sleep(1.2); await route.continue_()
            await sp.route("**/content/catalog.json", delay); await sp.goto(U); await sp.wait_for_timeout(300)
            check("LoadingState shown while loading", await sp.locator(".loading-state").count() == 1)
            await sp.screenshot(path=f"{SHOTS}/11_loading.png")

            # ---- responsive sweep ----
            screens = ["#/home", "#/calculate", "#/calculate/c/consciousness", "#/calculate/s/gcs", "#/guide/s/gcs", "#/settings", "#/settings/pick/favorites", "#/settings/gallery"]
            sizes = [("small phone 320x568", 320, 568), ("large phone 430x932", 430, 932), ("phone landscape 844x390", 844, 390),
                     ("tablet portrait 820x1180", 820, 1180), ("tablet landscape 1366x1024", 1366, 1024)]
            for label, w, h in sizes:
                rp = await newpage(w, h, storage={})
                over = []
                for sc in screens:
                    await rp.goto(U + sc); await rp.wait_for_selector(".bottomnav")
                    if not await no_overflow(rp): over.append(sc)
                check(f"{label}: no horizontal overflow", not over, ", ".join(over))
                rail = await rp.evaluate("getComputedStyle(document.querySelector('.bottomnav')).flexDirection") == "column"
                expect_rail = w >= 840 or (w > h and h <= 560 and w >= 560)
                check(f"{label}: {'navigation rail' if expect_rail else 'bottom navigation'}", rail == expect_rail)
                # touch targets on detail + settings
                small = []
                for sc in ["#/calculate/s/gcs", "#/settings"]:
                    await rp.goto(U + sc); await rp.wait_for_selector(".bottomnav")
                    small += await rp.evaluate("""[...document.querySelectorAll('button, a.btn, .icon-button, .bottomnav a, .segmented > *, .score-card a.open, .category-card, .chip')]
                      .filter(e => e.offsetParent).map(e => [e.getBoundingClientRect(), e]).filter(([r]) => r.height < 40 || r.width < 40).map(([r, e]) => (e.getAttribute('aria-label')||e.textContent.trim()).slice(0,30) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height))""")
                check(f"{label}: touch targets ≥ 40px", not small, "; ".join(small[:4]))
                unnamed = await rp.evaluate("""[...document.querySelectorAll('button, a, input')].filter(e => e.offsetParent || e.type==='checkbox')
                   .filter(e => !(e.getAttribute('aria-label') || e.textContent.trim() || (e.id && document.querySelector('label[for="'+e.id+'"]')))).length""")
                check(f"{label}: all controls have accessible names", unnamed == 0, str(unnamed))
                if label.startswith("small"):
                    await rp.goto(U + "#/home"); await rp.wait_for_selector(".bottomnav"); await rp.screenshot(path=f"{SHOTS}/12_small_home.png")
                    await rp.goto(U + "#/calculate/s/gcs"); await rp.wait_for_selector(".bottomnav"); await rp.screenshot(path=f"{SHOTS}/13_small_detail.png")
                if label.startswith("phone landscape"):
                    await rp.goto(U + "#/calculate"); await rp.wait_for_selector(".bottomnav"); await rp.screenshot(path=f"{SHOTS}/14_phone_landscape.png")
                if label.startswith("tablet landscape"):
                    await rp.goto(U + "#/calculate/s/gcs"); await rp.wait_for_selector(".bottomnav"); await rp.screenshot(path=f"{SHOTS}/15_tablet_detail.png")
                    await rp.goto(U + "#/calculate"); await rp.wait_for_selector(".bottomnav"); await rp.screenshot(path=f"{SHOTS}/16_tablet_calculate.png")
                    await rp.goto(U + "#/settings/gallery"); await rp.wait_for_selector(".bottomnav"); await rp.screenshot(path=f"{SHOTS}/17_gallery.png", full_page=True)
                check(f"{label}: no JS errors", not rp.errs, rp.errs[:2])

            # ---- rotation ----
            rot = await newpage(412, 915, storage={})
            await rot.goto(U + "#/calculate/c/stroke"); await rot.wait_for_selector(".score-card")
            await rot.click(".score-card:has-text('ASPECTS') [data-act=toggle-favorite] >> nth=0")
            await rot.set_viewport_size({"width": 915, "height": 412}); await rot.wait_for_timeout(200)
            check("rotation keeps route and state", await hashof(rot) == "#/calculate/c/stroke" and await rot.locator("[data-act=toggle-favorite][aria-pressed=true]").count() == 1)
            check("rotation switches to navigation rail", await rot.evaluate("getComputedStyle(document.querySelector('.bottomnav')).flexDirection") == "column")
            check("rotation: no overflow", await no_overflow(rot))
            await rot.set_viewport_size({"width": 412, "height": 915}); await rot.wait_for_timeout(200)
            check("rotate back restores bottom navigation", await rot.evaluate("getComputedStyle(document.querySelector('.bottomnav')).flexDirection") == "row")
            await b.close()
    finally:
        srv.terminate()
    failed = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed" + (": " + "; ".join(failed) if failed else ""))
    sys.exit(1 if failed else 0)

asyncio.run(main())
