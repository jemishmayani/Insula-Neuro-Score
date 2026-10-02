"""Phase 7 — Guide experience: structure, navigation, related-score links (all clicked), search, hierarchy."""
import asyncio, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); SHOTS = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(SHOTS, exist_ok=True); PORT = 8770; U = f"http://localhost:{PORT}/index.html"; results = []
def check(n, c, info=""): results.append((n, bool(c))); print(("PASS " if c else "FAIL ") + n + (f"  [{info}]" if info and not c else ""))
CAT = json.load(open(os.path.join(ROOT, "content", "catalog.json"))); BY = {s["id"]: s for s in CAT["scores"]}
IMPL = [s["id"] for s in CAT["scores"] if s["status"] == "implemented"]; REVIEW = [s["id"] for s in CAT["scores"] if s["status"] == "review"]
ORDER = ["Overview", "Purpose", "Intended population", "When to use", "Calculation", "Interpretation", "Clinical context", "Limitations", "Confounders",
         "Common mistakes", "What it does not tell you", "Related scores", "Version", "Sources"]

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await (await b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=2)).new_page()
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(U); await pg.wait_for_selector(".bottomnav")
            hashof = lambda: pg.evaluate("location.hash")
            async def open_guide(sid): await pg.goto(U + f"#/guide/s/{sid}"); await pg.wait_for_selector("#g-sources")

            # ---------- 1. structure, hierarchy, limitations prominence: every implemented guide ----------
            bad_order, bad_lims, long_paras, missing_parts = [], [], [], []
            for sid in IMPL:
                await open_guide(sid)
                titles = [t.split("\n")[-1].strip() for t in await pg.locator(".guide-body > .section-card > h3").all_inner_texts()]
                if titles != ORDER: bad_order.append(sid)
                kw = await pg.locator("#g-overview [data-block=key-warnings] .insight-card, #g-overview [data-block=key-warnings] .banner").count()
                if kw < 1: bad_lims.append(sid)
                longest = await pg.evaluate("Math.max(...[...document.querySelectorAll('.guide-body p')].map(p => p.textContent.length))")
                if longest > 420: long_paras.append(f"{sid}:{longest}")
                parts = await pg.evaluate("""({ facts: !!document.querySelector('#g-overview table.g-facts'), box: document.querySelectorAll('.guide-body .g-box').length,
                    tables: document.querySelectorAll('#g-calculation table.breakdown').length, steps: document.querySelectorAll('#g-calculation .g-steps li').length,
                    lim: document.querySelectorAll('#g-limitations .insight-card').length, conf: document.querySelectorAll('#g-confounders .insight-card').length,
                    states: document.querySelectorAll('#g-interpretation .state-card').length, warn: document.querySelectorAll('#g-mistakes .insight-card').length })""")
                if not (parts["facts"] and parts["box"] >= 2 and parts["tables"] >= 1 and parts["steps"] >= 1 and parts["lim"] >= 2 and parts["conf"] >= 1 and parts["states"] >= 1 and parts["warn"] >= 1):
                    missing_parts.append(f"{sid}:{parts}")
            check(f"all {len(IMPL)} guides: 14 sections in the Phase 7 order", not bad_order, str(bad_order))
            check("all guides: limitations surfaced in Overview (key warnings) and full section at position 8 of 14", not bad_lims and ORDER.index("Limitations") == 7, str(bad_lims))
            check("all guides: no paragraph over 420 characters", not long_paras, str(long_paras[:5]))
            check("all guides: fact table, highlight boxes, component tables, numbered steps, limitation/confounder/state/warning cards", not missing_parts, str(missing_parts[:2]))
            await open_guide("gcs")
            await pg.click("#g-overview [data-block=key-warnings] .g-jump"); await pg.wait_for_timeout(200)
            in_view = await pg.evaluate("(() => { const r = document.querySelector('#g-limitations').getBoundingClientRect(); return r.top >= 0 && r.top < innerHeight / 2; })()")
            check("'See all limitations' jumps to the Limitations section", in_view)
            await pg.screenshot(path=f"{SHOTS}/p7_gcs_limitations.png")

            # ---------- 2. top and bottom navigation on every guide ----------
            top_bad, bottom_bad = [], []
            for sid in IMPL + REVIEW:
                await open_guide(sid)
                await pg.click("[data-block=guide-nav-top] .btn-primary"); await pg.wait_for_timeout(60)
                if await hashof() != f"#/calculate/s/{sid}": top_bad.append(sid)
                await open_guide(sid)
                await pg.click("[data-block=guide-nav-bottom] .btn-primary"); await pg.wait_for_timeout(60)
                if await hashof() != f"#/calculate/s/{sid}": bottom_bad.append(sid)
            check(f"top 'Calculate' works on all {len(IMPL) + len(REVIEW)} guides", not top_bad, str(top_bad))
            check(f"bottom 'Calculate this score' works on all {len(IMPL) + len(REVIEW)} guides", not bottom_bad, str(bottom_bad))
            await open_guide("nihss"); await pg.click("[data-block=guide-nav-top] .g-jump"); await pg.wait_for_timeout(200)
            check("top 'Related scores →' jumps to Related", await pg.evaluate("document.querySelector('#g-related').getBoundingClientRect().top < innerHeight / 2"))

            # ---------- 3. spec examples ----------
            async def related_ids(sid):
                await open_guide(sid); return await pg.evaluate("[...new Set([...document.querySelectorAll('#g-related [data-related]')].map(e => e.dataset.related))]")
            r = await related_ids("gcs"); check("GCS → GCS-P, FOUR, GOSE", all(x in r for x in ["gcsp", "four", "gose"]), str(r))
            r = await related_ids("wfns"); check("SAH → Hunt & Hess, Modified Fisher, Fisher (from WFNS)", all(x in r for x in ["hunthess", "mfisher", "fisher"]), str(r))
            check("SAH cluster card present", await pg.locator("#g-related [data-cluster=sah]").count() == 1)
            r = await related_ids("sins"); check("Spinal metastases → Tokuhashi, Tomita, KPS (from SINS)", all(x in r for x in ["rtokuhashi", "tomita", "kps"]), str(r))
            r = await related_ids("nihss"); check("Stroke → ASPECTS, mRS (from NIHSS)", all(x in r for x in ["aspects", "mrs"]), str(r))
            await pg.screenshot(path=f"{SHOTS}/p7_nihss_related.png")

            # ---------- 4. click EVERY related link in EVERY guide, and back ----------
            clicked, failures, back_fail = 0, [], []
            for sid in IMPL + REVIEW:
                await open_guide(sid)
                targets = await pg.evaluate("""[...document.querySelectorAll('#g-related [data-related]')].flatMap(row => {
                    const id = row.dataset.related, out = [{ id, kind: 'guide', sel: '[data-related=\"' + id + '\"] a.open' }];
                    if (row.querySelector('a.alt-view')) out.push({ id, kind: 'calculate', sel: '[data-related=\"' + id + '\"] a.alt-view' });
                    return out; })""")
                seen = set()
                for t in targets:
                    key = (t["id"], t["kind"])
                    if key in seen: continue
                    seen.add(key)
                    await open_guide(sid)
                    await pg.locator("#g-related " + t["sel"]).first.click()
                    want = BY[t["id"]]["abbreviation"]
                    try: await pg.wait_for_function("w => { const a = document.querySelector('.detail-head .abbr'); return a && a.textContent.trim() === w; }", arg=want, timeout=3000)
                    except Exception: pass
                    h = await hashof(); head = await pg.locator(".detail-head .abbr").inner_text()
                    ok = h == f"#/{t['kind']}/s/{t['id']}" and head.strip() == BY[t["id"]]["abbreviation"] and await pg.locator(".error-state").count() == 0
                    if not ok: failures.append(f"{sid}→{t['id']}({t['kind']}) got {h} '{head}'")
                    clicked += 1
                    await pg.evaluate("window.handleBack()"); await pg.wait_for_timeout(80)
                    if await hashof() != f"#/guide/s/{sid}": back_fail.append(f"{sid}←{t['id']}")
            check(f"every related link opens the right score ({clicked} links clicked across {len(IMPL) + len(REVIEW)} guides)", not failures and clicked > 150, str(failures[:4]))
            check("Back from each related score returns to the originating guide", not back_fail, str(back_fail[:4]))
            un = BY["four"]; await open_guide("gcs"); await pg.locator('#g-related [data-related="four"] a.open').first.click(); await pg.wait_for_selector(".detail-head")
            check("related under-review score opens with its review reason", "Under review" in await pg.locator("main").inner_text())

            # ---------- 5. Guide search ----------
            async def gsearch(q):
                await pg.goto(U + "#/guide"); await pg.wait_for_selector("#search"); await pg.fill("#search", q); await pg.wait_for_timeout(60)
                return [t.split("\n")[0].replace("Calculator", "").replace("Under review", "").strip() for t in await pg.locator("#search-results .score-card .title").all_inner_texts()]
            r = await gsearch("SAH"); check("'SAH' surfaces Hunt & Hess, WFNS, Fisher, Modified Fisher first", sorted(r[:4]) == sorted(["Hunt & Hess", "WFNS", "Fisher", "mFisher"]), str(r))
            await pg.screenshot(path=f"{SHOTS}/p7_search_sah.png")
            check("search shows why a result matched", await pg.locator("#search-results .sub:has-text('matched')").count() >= 1)
            r = await gsearch("gcs"); check("abbreviation search (GCS first)", r[0] == "GCS", str(r))
            r = await gsearch("Rankin"); check("name search (Rankin → mRS)", r[:1] == ["mRS"], str(r))
            r = await gsearch("subarachnoid"); check("category search (subarachnoid)", set(["Hunt & Hess", "WFNS", "Fisher", "mFisher"]) <= set(r), str(r))
            r = await gsearch("radiation oncology"); check("specialty search (radiation oncology)", "SINS" in r and "KPS" in r, str(r))
            r = await gsearch("lvo"); check("keyword search (LVO → RACE, LAMS, FAST-ED)", {"RACE", "LAMS", "FAST-ED"} <= set(r), str(r))
            r = await gsearch("spinal metastasis"); check("keyword search (spinal metastasis → SINS, Tokuhashi, Tomita)", {"SINS", "Revised Tokuhashi", "Tomita"} <= set(r), str(r))
            r = await gsearch("hemorrhage"); r2 = await gsearch("haemorrhage"); check("spelling variants (hemorrhage / haemorrhage) both find ICH", "ICH Score" in r and "ICH Score" in r2)
            r = await gsearch("tia"); check("keyword search (TIA → ABCD²)", "ABCD²" in r, str(r))
            await pg.locator("#search-results .score-card a.open").first.click(); await pg.wait_for_selector("#g-sources")
            check("search result opens the guide", (await hashof()).startswith("#/guide/s/"))

            # ---------- 6. layouts ----------
            for name, vp, scheme in [("small", {"width": 320, "height": 640}, "light"), ("tablet", {"width": 1280, "height": 900}, "dark")]:
                c = await b.new_context(viewport=vp, device_scale_factor=2 if name == "small" else 1, color_scheme=scheme); q = await c.new_page()
                for sid in ["gcs", "iss", "sins"]:
                    await q.goto(U + f"#/guide/s/{sid}"); await q.wait_for_selector("#g-sources")
                    if not await q.evaluate("document.documentElement.scrollWidth <= innerWidth"): check(f"{name}: {sid} guide overflows", False)
                check(f"{name}: guides fit without horizontal scroll", True)
                await q.goto(U + "#/guide/s/sins"); await q.wait_for_selector("#g-sources"); await q.screenshot(path=f"{SHOTS}/p7_{name}_sins.png")
                await q.goto(U + "#/guide/s/iss"); await q.wait_for_selector("#g-sources"); await q.locator("#g-calculation").screenshot(path=f"{SHOTS}/p7_{name}_iss_calc.png")
                await c.close()
            check("no JS errors", not errs, errs[:3])
            await b.close()
    finally: srv.terminate()
    f = [n for n, ok in results if not ok]; print(f"\n{len(results) - len(f)} passed, {len(f)} failed" + (": " + "; ".join(f) if f else "")); sys.exit(1 if f else 0)
asyncio.run(main())
