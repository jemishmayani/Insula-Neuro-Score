"""Phase 6 — walk every implemented calculator and guide in the real UI; check under-review entries."""
import asyncio, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); SHOTS = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(SHOTS, exist_ok=True); PORT = 8769; U = f"http://localhost:{PORT}/index.html"; results = []
def check(n, c, info=""): results.append((n, bool(c))); print(("PASS " if c else "FAIL ") + n + (f"  [{info}]" if info and not c else ""))
CAT = json.load(open(os.path.join(ROOT, "content", "catalog.json")))
IMPL = [s for s in CAT["scores"] if s["status"] == "implemented"]; REVIEW = [s for s in CAT["scores"] if s["status"] == "review"]
SHOT_IDS = {"aspects", "abcd2", "ich", "marshall", "rts", "iss", "rtokuhashi", "gose"}

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
            check(f"catalogue: {len(IMPL)} implemented, {len(REVIEW)} under review, 0 placeholders", {s["id"] for s in IMPL} == {f[:-5] for f in os.listdir(os.path.join(ROOT, "content", "scores"))} and not [s for s in CAT["scores"] if s["status"] == "placeholder"])
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
            for s in REVIEW:
                await pg.goto(U + f"#/calculate/s/{s['id']}"); await pg.wait_for_selector(".detail-head")
                txt = await pg.locator("main").inner_text()
                check(f"{s['id']}: under review, reason shown ({s['reviewCategory']})", "Under review" in txt and s["reviewReason"][:40] in txt and await pg.locator(".field").count() == 0)
            await pg.goto(U + "#/calculate/c/spine"); await pg.wait_for_selector(".score-card")
            badges = await pg.locator(".score-card .status-badge").all_inner_texts()
            check("category list distinguishes Calculator / Under review badges", "Calculator" in badges and "Under review" in badges, str(badges))
            await pg.screenshot(path=f"{SHOTS}/p6_stroke_list.png")
            await pg.goto(U + "#/calculate/s/sofa"); await pg.wait_for_selector(".detail-head"); await pg.screenshot(path=f"{SHOTS}/p6_sofa_review.png")
            check("no JS errors across the library", not errs, errs[:3])
            await b.close()
    finally: srv.terminate()
    f = [n for n, ok in results if not ok]; print(f"\n{len(results) - len(f)} passed, {len(f)} failed" + (": " + "; ".join(f) if f else "")); sys.exit(1 if f else 0)
asyncio.run(main())
