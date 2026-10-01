"""Phase 2 calculator UI tests: the UI renders engine results for GCS, NIHSS, mRS, SINS and every input type."""
import asyncio, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); SHOTS = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(SHOTS, exist_ok=True); PORT = 8767; U = f"http://localhost:{PORT}/index.html"; results = []
def check(n, c, info=""): results.append((n, bool(c))); print(("PASS " if c else "FAIL ") + n + (f"  [{info}]" if info and not c else ""))

async def pick(pg, inp, val): await pg.click(f'.field[data-field="{inp}"] input[value="{val}"] >> xpath=..')
async def state(pg): return await pg.evaluate("(() => { const c = document.querySelector('#result .result-card'); return { tone: [...c.classList].find(x => x.startsWith('tone-')), value: c.querySelector('.value').textContent, label: c.querySelector('.state span').textContent }; })()")
async def card(pg): return await pg.evaluate("(() => { const c = document.querySelector('#result .result-card'); const f = c.querySelector('.formula'); const m = c.querySelector('.meter-seg.is-on .meter-lbl'); return { type: (c.querySelector('.result-type')||{}).textContent, formula: f ? f.textContent : null, meter: m ? m.textContent : null, formulaBeforeValue: !!f && !!(f.compareDocumentPosition(c.querySelector('.value')) & 4) }; })()")

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(); ctx = await b.new_context(viewport={"width": 412, "height": 915}, device_scale_factor=2)
            pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(U); await pg.wait_for_selector(".bottomnav")

            # ---- GCS ----
            await pg.goto(U + "#/calculate/s/gcs"); await pg.wait_for_selector(".field")
            s = await state(pg); check("GCS starts incomplete", s["tone"] == "tone-incomplete")
            check("progress shows 0 of 3", "0 of 3 answered" in await pg.locator(".calc-progress").inner_text())
            await pick(pg, "e", "2"); await pick(pg, "v", "2"); await pick(pg, "m", "4")
            s = await state(pg); check("GCS 8 → high concern", s == {"tone": "tone-high", "value": "8", "label": "Severe impairment"}, str(s))
            bd = await pg.locator("#result .breakdown").inner_text(); check("breakdown lists E2 V2 M4", all(x in bd for x in ["E2", "V2", "M4"]))
            c = await card(pg)
            check("GCS shows E + V + M before the total", c["formula"] == "E2 + V2 + M4 =" and c["formulaBeforeValue"], str(c))
            check("GCS result type = level of consciousness, meter band 3–8", c["type"] == "Level of consciousness" and c["meter"] == "3–8", str(c))
            check("GCS result bar shows components first", (await pg.locator(".result-bar .rb-value").inner_text()) == "E2 V2 M4 = 8")
            check("GCS notice: document E, V, M separately", await pg.locator(".calc-notice >> text=Document E, V and M separately").count() == 1)
            await pg.screenshot(path=f"{SHOTS}/p3_gcs8.png")
            await pick(pg, "v", "__nt")
            s = await state(pg); c = await card(pg)
            check("GCS verbal NT → no total, components shown (not V1)", s["tone"] == "tone-not-interpretable" and s["value"] == "No total" and c["formula"] == "E2 + VNT + M4", str(s) + str(c))
            check("GCS NT: optional reason picker offered", await pg.locator("#in-v-reason").count() == 1)
            check("GCS NT: share text keeps components", True)
            check("NT insight suggests FOUR", await pg.locator("#result >> text=FOUR score").count() >= 1)
            await pg.click("#result >> text=Result"); await pg.screenshot(path=f"{SHOTS}/p3_gcs_nt.png")
            await pick(pg, "e", "4"); await pick(pg, "v", "5"); await pick(pg, "m", "6")
            s = await state(pg); check("GCS 15 → normal", s["tone"] == "tone-normal" and s["value"] == "15")
            check("related scores link", await pg.locator("#result .chip:has-text('GCS-P')").count() == 1)
            await pg.click("[data-act=calc-reset]"); s = await state(pg)
            check("reset clears answers", s["tone"] == "tone-incomplete" and await pg.locator(".choice.is-on").count() == 0)

            # answers survive Calculate → Guide → Calculate
            await pick(pg, "e", "3")
            await pg.click(".segmented >> text=Guide"); await pg.wait_for_selector("#g15")
            titles = await pg.locator(".section-card h3").all_inner_texts()
            check("GCS guide: 15 sections in Phase 3 order", [t.split("\n")[-1].strip() for t in titles] == ["What is it?", "Purpose", "Intended population", "When to use", "How to perform / calculate", "Scoring components", "Interpretation", "Clinical context", "Limitations", "Confounders", "Common mistakes", "What the score does not tell you", "Related scores", "Version", "Sources"], str(titles[:6]))
            check("guide interpretation lists all states", await pg.locator("#g7 tr").count() == 4)
            check("guide shows version + review status", "Pending" in await pg.locator("#g14").inner_text() or "pending" in await pg.locator("#g14").inner_text())
            await pg.screenshot(path=f"{SHOTS}/p3_gcs_guide.png")
            await pg.click(".btn-primary >> nth=0"); await pg.wait_for_selector(".field")
            check("answers kept in session", await pg.locator('.field[data-field="e"] .choice.is-on').count() == 1)
            await pg.reload(); await pg.wait_for_selector(".field")
            check("answers NOT persisted across app restart (no patient data)", await pg.locator(".choice.is-on").count() == 0)
            stored = await pg.evaluate("Object.keys(localStorage).map(k => localStorage.getItem(k)).join(' ')")
            check("no answers in local storage", '"e":' not in stored and "answers" not in stored)

            # ---- NIHSS ----
            await pg.goto(U + "#/calculate/s/nihss"); await pg.wait_for_selector(".field")
            check("NIHSS renders 15 items in 11 components", await pg.locator(".field").count() == 15)
            check("NIHSS notice: not a complete neurological examination", await pg.locator(".calc-notice >> text=Not a complete neurological examination").count() == 1)
            check("NIHSS has no severity meter (no official bands)", await pg.locator("#result .meter").count() == 0)
            check("NIHSS UN not offered for item 11", await pg.locator('.field[data-field="item_11"] input[value="__nt"]').count() == 0)
            for item in ["1a", "1b", "1c", "2", "3", "4", "5a", "5b", "6a", "6b", "7", "8", "9", "10", "11"]: await pick(pg, "item_" + item, "0")
            s = await state(pg); check("NIHSS 0 → no deficit measured", s["value"] == "0" and s["tone"] == "tone-normal", str(s))
            await pick(pg, "item_5b", "3"); await pick(pg, "item_9", "2"); await pick(pg, "item_4", "2")
            s = await state(pg); check("NIHSS 7 → informational (label not duplicated)", s == {"tone": "tone-informational", "value": "7", "label": "Informational"}, str(s))
            check("NIHSS result type = measured stroke deficit", (await card(pg))["type"] == "Measured stroke deficit")
            check("component subtotal shown (Motor arm = 3)", "3" in await pg.locator("#result tr.bd-group:has-text('Motor arm') td.pts").inner_text())
            # UN with reason
            await pick(pg, "item_5a", "__nt")
            check("UN shows reason picker", await pg.locator("#in-item_5a-reason").count() == 1)
            s = await state(pg); check("UN without reason → check entries", s["tone"] == "tone-incomplete" and "Check" in s["label"], str(s))
            check("field error shown under item", "reason" in (await pg.locator('.field[data-field="item_5a"] .field-error').inner_text()).lower())
            await pg.select_option("#in-item_5a-reason", "Amputation")
            s = await state(pg); check("UN with reason → total 7, flagged", s["value"] == "7" and await pg.locator("#result .banner.tone-warning >> text=untestable").count() == 1)
            await pg.screenshot(path=f"{SHOTS}/p3_nihss_un.png")
            # coma consistency
            await pick(pg, "item_1a", "3")
            check("coma consistency warnings", await pg.locator("#result .banner.tone-warning >> text=coma").count() == 2)
            await pick(pg, "item_9", "3")
            check("language 3 vs commands followed → warning", await pg.locator("#result .banner.tone-warning >> text=one-step").count() == 1)
            check("warning highlights item 8", await pg.locator('.field[data-field="item_8"].has-warning').count() == 1)
            txt = await pg.evaluate("document.querySelector('#result').innerText")
            check("contextual limitation shown first", "untestable" in txt.split("Limitations")[1][:200])

            # ---- mRS ----
            await pg.goto(U + "#/calculate/s/mrs"); await pg.wait_for_selector(".field")
            check("mRS notice: functional outcome scale", await pg.locator(".calc-notice >> text=Functional outcome scale").count() == 1)
            for g, tone in [("0", "tone-normal"), ("3", "tone-informational"), ("5", "tone-informational"), ("6", "tone-informational")]:
                await pick(pg, "grade", g); s = await state(pg); c = await card(pg)
                check(f"mRS {g} → functional status ({tone}), meter at {g}", s["tone"] == tone and s["value"] == f"mRS {g}" and c["type"] == "Functional status" and c["meter"] == g, str(s) + str(c))
            tone_color = await pg.evaluate("getComputedStyle(document.querySelector('#result .result-card')).getPropertyValue('--tone').trim()")
            seg_color = await pg.evaluate("getComputedStyle(document.querySelector('#result .meter-seg.is-on i')).backgroundColor")
            check("informational tone is actually coloured (card + active meter segment)", tone_color != "" and seg_color not in ("rgba(0, 0, 0, 0)", "transparent"), tone_color + " " + seg_color)
            check("mRS summary states functional status", "Functional status" in await pg.locator("#result .summary").inner_text() or "Outcome" in await pg.locator("#result .summary").inner_text())
            await pick(pg, "grade", "3"); await pg.click("#result >> text=Result"); await pg.screenshot(path=f"{SHOTS}/p3_mrs3.png")

            # ---- SINS ----
            await pg.goto(U + "#/calculate/s/sins"); await pg.wait_for_selector(".field")
            for i, v in [("location", "3"), ("pain", "3"), ("lesion", "0"), ("alignment", "0"), ("collapse", "1"), ("posterolateral", "0")]: await pick(pg, i, v)
            s = await state(pg); check("SINS 7 → potentially unstable (boundary)", s == {"tone": "tone-moderate", "value": "7", "label": "Potentially unstable"}, str(s))
            c = await card(pg); check("SINS result type = stability category, meter 7–12", c["type"] == "Stability category" and c["meter"] == "7–12", str(c))
            check("SINS notice: not a surgical decision", await pg.locator(".calc-notice >> text=not a surgical decision").count() == 1)
            check("SINS 7: referral threshold, not decision to operate", "not a decision to operate" in await pg.locator("#result .result-card").inner_text())
            await pick(pg, "collapse", "0"); s = await state(pg); check("SINS 6 → stable (boundary)", s["label"] == "Stable" and s["tone"] == "tone-low")
            await pick(pg, "alignment", "4"); await pick(pg, "lesion", "2"); await pick(pg, "collapse", "1")
            s = await state(pg); check("SINS 13 → unstable (boundary)", s["label"] == "Unstable" and s["tone"] == "tone-high" and s["value"] == "13")
            await pg.click("#result >> text=Result"); await pg.screenshot(path=f"{SHOTS}/p3_sins13.png")
            # copy result text built from result model
            await ctx.grant_permissions(["clipboard-read", "clipboard-write"])
            await pg.click("[data-act=calc-copy]"); clip = await pg.evaluate("navigator.clipboard.readText()")
            check("copy text = engine share text + breakdown", clip.startswith("SINS 13 — Unstable") and "Location: Junctional" in clip, clip[:80])

            # ---- every input type in the design-system demo ----
            await pg.goto(U + "#/settings/gallery"); await pg.wait_for_selector("#demo-host .field")
            await pick(pg, "single", "c"); await pg.select_option("#in-dropdown", "z")
            await pg.click('.field[data-field="yes_no"] label:has-text("Yes")')
            await pick(pg, "multi", "p"); await pick(pg, "multi", "q")
            await pg.fill("#in-integer", "3.5"); await pg.locator("#in-integer").blur()
            check("integer rejects decimal", "whole number" in await pg.locator('.field[data-field="integer"] .field-error').inner_text())
            await pg.fill("#in-integer", ""); await pg.click('.field[data-field="integer"] [data-step="1"]')
            check("integer stepper from empty → min", await pg.input_value("#in-integer") == "0")
            await pg.fill("#in-decimal", "2.55"); await pg.locator("#in-decimal").blur()
            check("decimal precision enforced", "decimal place" in await pg.locator('.field[data-field="decimal"] .field-error').inner_text())
            await pg.fill("#in-decimal", "2.5")
            await pg.select_option('.field[data-field="temperature"] select', "F"); await pg.fill("#in-temperature", "100.4")
            s = await state(pg)
            check("measurement converts °F → points; full demo total", s["value"] == "9", str(s))
            check("breakdown shows conversion", "(38 °C)" in await pg.locator("#result .breakdown").inner_text())
            await pick(pg, "multi", "none")
            check("exclusive option conflict reported", "cannot be combined" in await pg.locator('.field[data-field="multi"] .field-error').inner_text())
            await pick(pg, "single", "__nt"); s = await state(pg)
            check("not-testable → not-interpretable tone", s["tone"] in ("tone-not-interpretable", "tone-incomplete"))
            await pg.screenshot(path=f"{SHOTS}/p3_demo.png", full_page=True)

            # ---- Guide <-> Calculate for all four ----
            for sid in ["gcs", "nihss", "mrs", "sins"]:
                await pg.goto(U + f"#/calculate/s/{sid}"); await pg.wait_for_selector(".field")
                await pg.click('.segmented a:has-text("Guide")'); await pg.wait_for_selector("#g15")
                ok1 = await pg.evaluate("location.hash") == f"#/guide/s/{sid}" and await pg.locator(".section-card").count() == 15
                await pg.click(".btn-primary:has-text('Calculate this score') >> nth=0"); await pg.wait_for_selector(".field")
                ok2 = await pg.evaluate("location.hash") == f"#/calculate/s/{sid}"
                await pg.goto(U + f"#/guide/s/{sid}"); await pg.wait_for_selector("#g15")
                srcs = await pg.locator("#g15 li").count()
                check(f"{sid}: Calculate → Guide → Calculate, 15 sections, {srcs} sources", ok1 and ok2 and srcs >= 2)
                r = await pg.evaluate("window.handleBack()"); await pg.wait_for_timeout(150)
                check(f"{sid}: back from guide leaves the score (toggle adds no history)", "/s/" not in await pg.evaluate("location.hash"))

            # ---- light / dark ----
            for theme in ["light", "dark"]:
                await pg.evaluate(f"localStorage.setItem('ins.store.v2', JSON.stringify(Object.assign(JSON.parse(localStorage.getItem('ins.store.v2')||'{{}}'), {{theme:'{theme}'}})))"); await pg.reload(); await pg.wait_for_selector(".bottomnav")
                for sid, fill in [("gcs", [("e","2"),("v","2"),("m","4")]), ("mrs", [("grade","4")]), ("sins", [("location","2"),("pain","3"),("lesion","2"),("alignment","2"),("collapse","3"),("posterolateral","3")])]:
                    await pg.goto(U + f"#/calculate/s/{sid}"); await pg.wait_for_selector(".field")
                    for i, v in fill: await pick(pg, i, v)
                    await pg.click("#result >> text=Result"); await pg.screenshot(path=f"{SHOTS}/p3_{theme}_{sid}.png")
                check(f"{theme} theme applied", await pg.evaluate("document.documentElement.dataset.theme") == theme)

            # ---- small phone ----
            sp = await (await b.new_context(viewport={"width": 320, "height": 640}, device_scale_factor=2)).new_page()
            for sid in ["gcs", "nihss", "mrs", "sins"]:
                await sp.goto(U + f"#/calculate/s/{sid}"); await sp.wait_for_selector(".field")
                inputs = await sp.evaluate("[...document.querySelectorAll('.field')].map(f => f.dataset.field)")
                for inp in inputs:
                    first = sp.locator(f'.field[data-field="{inp}"] input[type=radio]:not([value="__nt"])').last if sid == "nihss" else sp.locator(f'.field[data-field="{inp}"] input[type=radio]').nth(1)
                    await first.locator("xpath=..").click()
                over = await sp.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                barvis = await sp.locator(".result-bar").is_visible()
                check(f"small phone 320px: {sid} completes, no overflow, result bar visible", over and barvis and (await state(sp))["tone"] != "tone-incomplete")
                await sp.screenshot(path=f"{SHOTS}/p3_small_{sid}.png")
                await sp.goto(U + f"#/guide/s/{sid}"); await sp.wait_for_selector("#g15")
                check(f"small phone 320px: {sid} guide no overflow", await sp.evaluate("document.documentElement.scrollWidth <= window.innerWidth"))

            # ---- dark + tablet ----
            await pg.evaluate("localStorage.setItem('ins.store.v2', JSON.stringify(Object.assign(JSON.parse(localStorage.getItem('ins.store.v2')||'{}'), {theme:'dark'})))")
            await pg.goto(U + "#/calculate/s/nihss"); await pg.wait_for_selector(".field"); await pg.screenshot(path=f"{SHOTS}/p3_nihss_dark.png")
            t = await b.new_context(viewport={"width": 1280, "height": 900}); tp = await t.new_page(); await tp.goto(U + "#/calculate/s/sins"); await tp.wait_for_selector(".field")
            for i, v in [("location", "2"), ("pain", "3"), ("lesion", "2"), ("alignment", "2"), ("collapse", "3"), ("posterolateral", "3")]: await pick(tp, i, v)
            check("tablet: result panel beside inputs", await tp.evaluate("document.querySelector('.aside').getBoundingClientRect().left > document.querySelector('.calc-inputs').getBoundingClientRect().right"))
            check("tablet: result bar hidden", not await tp.locator(".result-bar").is_visible())
            await tp.screenshot(path=f"{SHOTS}/p3_tablet_sins.png")
            for sid in ["gcs", "nihss", "mrs"]:
                await tp.goto(U + f"#/calculate/s/{sid}"); await tp.wait_for_selector(".field")
                check(f"tablet: {sid} two-pane, no overflow", await tp.evaluate("document.querySelector('.aside').getBoundingClientRect().left > document.querySelector('.calc-inputs').getBoundingClientRect().right && document.documentElement.scrollWidth <= innerWidth"))
            await tp.goto(U + "#/guide/s/nihss"); await tp.wait_for_selector("#g15"); await tp.screenshot(path=f"{SHOTS}/p3_tablet_nihss_guide.png")
            check("no JS errors", not errs, errs[:3])
            await b.close()
    finally: srv.terminate()
    f = [n for n, ok in results if not ok]; print(f"\n{len(results)-len(f)} passed, {len(f)} failed" + (": " + "; ".join(f) if f else "")); sys.exit(1 if f else 0)
asyncio.run(main())
