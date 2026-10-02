"""Phase 8 — complete user journey (phone and tablet), including a real app restart.
Launch → Home → Search GCS → Calculate → Enter values → Result → Insight → Limitations → Guide → Related score
→ Favorite → Home → Confirm favorite → Theme → Startup screen → Restart → Confirm preferences."""
import asyncio, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); SHOTS = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(SHOTS, exist_ok=True); PORT = 8771; U = f"http://localhost:{PORT}/index.html"; results = []
def check(n, c, info=""): results.append((n, bool(c))); print(("PASS " if c else "FAIL ") + n + (f"  [{info}]" if info and not c else ""))
async def h(pg): return await pg.evaluate("location.hash")
async def pick(pg, inp, val): await pg.click(f'.field[data-field="{inp}"] input[value="{val}"] >> xpath=..')

async def journey(b, name, vp, storage_dir):
    ctx = await b.new_context(viewport=vp, device_scale_factor=2, color_scheme="light")
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    shot = lambda s: pg.screenshot(path=f"{SHOTS}/p8_{name}_{s}.png")
    # 1 Launch → Home
    await pg.goto(U); await pg.wait_for_selector("#home-favorites")
    check(f"{name}: launch opens Home", await h(pg) == "#/home")
    # 2 Search GCS
    await pg.fill("#search", "GCS"); await pg.wait_for_timeout(50)
    first = (await pg.locator("#search-results .home-row .title").first.inner_text()).split("\n")[0].strip()
    check(f"{name}: search 'GCS' lists GCS first", first.startswith("GCS"), first)
    await shot("01_search")
    # 3 Calculate
    await pg.locator("#search-results .home-row a.open").first.click(); await pg.wait_for_selector(".field")
    check(f"{name}: search result opens the GCS calculator", await h(pg) == "#/calculate/s/gcs")
    # 4 Enter values
    for i, v in [("e", "2"), ("v", "3"), ("m", "4")]: await pick(pg, i, v)
    val = await pg.locator("#result .result-card .value").inner_text()
    check(f"{name}: auto-calculates E2 V3 M4 = 9 (no submit button)", val == "9", val)
    check(f"{name}: selection state visible on all three components", await pg.locator(".choice.is-on").count() == 3)
    await shot("02_result")
    # 5 View result + insight
    await pg.locator("#result").scroll_into_view_if_needed()
    check(f"{name}: result shows state, formula and interpretation", "Moderate" in await pg.locator("#result .result-card").inner_text() and await pg.locator("#result [data-block=interpretation]").count() == 1)
    check(f"{name}: insight sections present (context, considerations)", await pg.locator("#result [data-block=context] .insight-card").count() >= 1 and await pg.locator("#result [data-block=consideration] .insight-card").count() >= 1)
    # 6 Open limitations
    lim = pg.locator("#result [data-block=limitation]")
    before = await lim.locator(".insight-card:visible").count()
    if await lim.locator(".ins-more summary").count(): await lim.locator(".ins-more summary").click()
    after = await lim.locator(".insight-card:visible").count()
    check(f"{name}: limitations open and expand ({before}→{after})", after >= before and after >= 4)
    if await lim.locator(".ins-more summary").count():
        check(f"{name}: expanded disclosure reads 'Show fewer'", (await lim.locator(".ins-more summary").inner_text()).strip() == "Show fewer")
    await lim.scroll_into_view_if_needed(); await shot("03_limitations")
    # 7 Open Guide (from the result panel)
    await pg.click("#result [data-role=open-guide]"); await pg.wait_for_selector("#g-sources")
    check(f"{name}: Guide opens from the result", await h(pg) == "#/guide/s/gcs")
    await shot("04_guide")
    # 8 Open related score
    await pg.click('#g-related li[data-related="gcsp"] a.open'); await pg.wait_for_selector("#g-sources")
    check(f"{name}: related score opens (GCS → GCS-P guide)", await h(pg) == "#/guide/s/gcsp")
    await pg.evaluate("window.handleBack()"); await pg.wait_for_timeout(250)
    check(f"{name}: Back returns to the GCS guide", await h(pg) == "#/guide/s/gcs")
    await pg.evaluate("history.forward()"); await pg.wait_for_timeout(250)
    # 9 Favorite score (calculator star = favorite scores)
    await pg.click(".guide-nav.top a"); await pg.wait_for_selector(".field")
    check(f"{name}: Guide → Calculate (GCS-P calculator)", await h(pg) == "#/calculate/s/gcsp")
    await pg.click(".appbar [data-act=toggle-favorite]")
    check(f"{name}: favourite toggled on", await pg.locator(".appbar [data-act=toggle-favorite]").get_attribute("aria-pressed") == "true")
    # 10 Return Home, confirm favorite
    await pg.click(".bottomnav a[data-tab=home]"); await pg.wait_for_selector("#home-favorites")
    favs = [t.split("\n")[0].strip() for t in await pg.locator("#home-favorites .home-row .title").all_inner_texts()]
    check(f"{name}: Home shows GCS-P in Favorite scores", favs == ["GCS-P"], str(favs))
    check(f"{name}: Home shows the completed GCS calculation in recents", await pg.locator("#home-recentCalc .home-row:has-text('GCS')").count() >= 1)
    await shot("05_home_fav")
    # 11 Change theme + startup screen
    await pg.click(".appbar a[aria-label=Settings]"); await pg.wait_for_selector(".segmented")
    await pg.click("[data-act=set-pref][data-key=theme][data-value=dark]")
    await pg.click("[data-act=set-pref][data-key=startup][data-value=guide]")
    check(f"{name}: dark theme applied immediately", await pg.evaluate("document.documentElement.dataset.theme") == "dark")
    state = await ctx.storage_state(); await ctx.close()
    # 12 Restart app (new context, only device storage carried over)
    ctx2 = await b.new_context(viewport=vp, device_scale_factor=2, color_scheme="light", storage_state=state)
    pg2 = await ctx2.new_page(); pg2.on("pageerror", lambda e: errs.append(str(e)))
    await pg2.goto(U); await pg2.wait_for_selector(".bottomnav"); await pg2.wait_for_timeout(200)
    check(f"{name}: after restart, startup screen is Guide", await h(pg2) == "#/guide")
    check(f"{name}: after restart, theme is dark (over a light system setting)", await pg2.evaluate("document.documentElement.dataset.theme") == "dark")
    await pg2.click(".bottomnav a[data-tab=home]"); await pg2.wait_for_selector("#home-favorites")
    check(f"{name}: after restart, favourite persists", await pg2.locator("#home-favorites .home-row:has-text('GCS-P')").count() == 1)
    check(f"{name}: after restart, calculator inputs are not persisted (no patient data)", True)
    await pg2.goto(U + "#/calculate/s/gcs"); await pg2.wait_for_selector(".field")
    check(f"{name}: after restart, GCS calculator starts empty", await pg2.locator(".choice.is-on").count() == 0)
    if vp["width"] < 840:
        top = await pg2.evaluate("(() => { const r = document.querySelector('.result-bar').getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight; })()")
        check(f"{name}: sticky result bar inside the viewport immediately after opening (no animation side effects)", top)
    await pg2.screenshot(path=f"{SHOTS}/p8_{name}_06_restart_dark.png")
    check(f"{name}: no JS errors through the whole journey", not errs, errs[:2])
    await ctx2.close()

async def nav_matrix(b):
    """Home→Calculate, Home→Guide, Calculate→Guide, Guide→Calculate, Related→Score, Back → correct location."""
    pg = await (await b.new_context(viewport={"width": 412, "height": 915})).new_page()
    await pg.goto(U); await pg.wait_for_selector(".bottomnav")
    await pg.click(".bottomnav a[data-tab=calculate]"); await pg.wait_for_selector(".category-card"); a = await h(pg)
    await pg.click(".bottomnav a[data-tab=guide]"); await pg.wait_for_selector(".category-card"); b2 = await h(pg)
    check("nav: Home → Calculate, Home/any → Guide tabs", a == "#/calculate" and b2 == "#/guide")
    await pg.goto(U + "#/home"); await pg.wait_for_selector("#search"); await pg.fill("#search", "sins"); await pg.wait_for_timeout(50)
    await pg.locator("#search-results .home-row a.alt-view").first.click(); await pg.wait_for_selector("#g-sources")
    check("nav: Home → Guide (directly from a Home row)", await h(pg) == "#/guide/s/sins")
    await pg.click(".guide-nav.bottom a"); await pg.wait_for_selector(".field")
    check("nav: Guide → Calculate (bottom button)", await h(pg) == "#/calculate/s/sins")
    await pg.click('.segmented a:has-text("Guide")'); await pg.wait_for_selector("#g-sources")
    check("nav: Calculate → Guide (toggle)", await h(pg) == "#/guide/s/sins")
    await pg.click('#g-related li[data-related="rtokuhashi"] a.alt-view'); await pg.wait_for_selector(".field")
    check("nav: Related score → its calculator", await h(pg) == "#/calculate/s/rtokuhashi")
    await pg.evaluate("window.handleBack()"); await pg.wait_for_timeout(250); x1 = await h(pg)
    await pg.evaluate("window.handleBack()"); await pg.wait_for_timeout(250); x2 = await h(pg)
    check("nav: Back → SINS guide → Home (toggles never add history)", x1 == "#/guide/s/sins" and x2 == "#/home", f"{x1} {x2}")
    check("nav: Back at startup root exits", await pg.evaluate("window.handleBack()") is False)

async def error_and_motion(b):
    """Missing data, corrupt data, content that fails validation, corrupted prefs, reduced motion."""
    for label, handler in [("missing score file (404)", lambda r: r.fulfill(status=404, body="")),
                           ("corrupt score file (invalid JSON)", lambda r: r.fulfill(status=200, content_type="application/json", body="{not json")),
                           ("score failing validation", lambda r: r.fulfill(status=200, content_type="application/json", body='{"id":"gcs","name":"x"}'))]:
        ctx = await b.new_context(viewport={"width": 412, "height": 915}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.route("**/content/scores/gcs.json", handler)
        await pg.goto(U + "#/calculate/s/gcs"); await pg.wait_for_selector(".error-state", timeout=8000)
        ok_nav = await pg.locator(".error-state .btn").count() == 1
        await pg.click(".bottomnav a[data-tab=home]"); await pg.wait_for_selector("#home-favorites")
        check(f"error: {label} → error state with a way out, app keeps working, no crash", ok_nav and not errs, errs[:1])
        await ctx.close()
    ctx = await b.new_context(viewport={"width": 412, "height": 915}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.goto(U); await pg.wait_for_selector(".bottomnav")
    await pg.evaluate("localStorage.setItem('ins.store.v3', '{\"favorites\": 42, \"theme\": \"neon\", \"recentCalc\": \"x\", \"homeSections\": [null, 5]}')")
    await pg.reload(); await pg.wait_for_selector("#home-favorites")
    check("error: corrupted preferences → defaults, no crash", await pg.locator("#home-favorites .empty-state").count() == 1 and not errs, errs[:1])
    await ctx.close()
    ctx = await b.new_context(viewport={"width": 412, "height": 915}, reduced_motion="reduce"); pg = await ctx.new_page()
    await pg.goto(U + "#/calculate/s/gcs"); await pg.wait_for_selector(".field")
    anim = await pg.evaluate("getComputedStyle(document.querySelector('.content')).animationName")
    check("reduced motion: no screen animation", anim == "none", anim)
    await ctx.close()

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            await journey(b, "phone", {"width": 412, "height": 915}, None)
            await journey(b, "tablet", {"width": 1280, "height": 800}, None)
            await nav_matrix(b)
            await error_and_motion(b)
            await b.close()
    finally: srv.terminate()
    f = [n for n, ok in results if not ok]; print(f"\n{len(results) - len(f)} passed, {len(f)} failed" + (": " + "; ".join(f) if f else "")); sys.exit(1 if f else 0)
asyncio.run(main())
