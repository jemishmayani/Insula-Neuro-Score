"""Phase 8 — performance under 4× CPU throttling (approximates a mid-range Android phone).
Measures cold startup, navigation, search, calculation, Guide opening (first / repeat) and Home rendering."""
import asyncio, json, os, statistics, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); PORT = 8772; U = f"http://localhost:{PORT}/index.html"; results = []; table = []
def check(n, c, info=""): results.append((n, bool(c))); print(("PASS " if c else "FAIL ") + n + (f"  [{info}]" if info and not c else ""))
BUDGET = {"cold start (Home ready)": 2500, "tab navigation": 200, "search keystroke": 60, "calculation update": 50,
          "Guide open (first)": 900, "Guide open (repeat)": 350, "Home render": 200}

TO = """async ([hash, sel]) => { const t0 = performance.now(); location.hash = hash;
  await new Promise(r => { const ch = () => document.querySelector(sel) ? r() : requestAnimationFrame(ch); ch(); }); return performance.now() - t0; }"""

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(); m = {k: [] for k in BUDGET}
            for run in range(3):
                ctx = await b.new_context(viewport={"width": 412, "height": 915}); pg = await ctx.new_page()
                cdp = await ctx.new_cdp_session(pg); await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
                await pg.goto(U); await pg.wait_for_selector("#home-favorites")
                m["cold start (Home ready)"].append(await pg.evaluate("performance.now()"))
                m["tab navigation"].append(await pg.evaluate(TO, ["#/calculate", ".category-card"]))
                m["Home render"].append(await pg.evaluate(TO, ["#/home", "#home-favorites"]))
                m["search keystroke"].append(max(await pg.evaluate("""() => { const el = document.querySelector('#search'), out = [];
                    for (const q of ['g', 'gc', 'gcs', 'sah', 'spinal met', 'hemorrhage']) { const t0 = performance.now(); el.value = q; el.dispatchEvent(new Event('input', { bubbles: true })); out.push(performance.now() - t0); }
                    return out; }""")))
                m["Guide open (first)"].append(await pg.evaluate(TO, ["#/guide/s/nihss", "#g-sources"]))
                await pg.evaluate(TO, ["#/home", "#home-favorites"])
                m["Guide open (repeat)"].append(await pg.evaluate(TO, ["#/guide/s/nihss", "#g-sources"]))
                await pg.evaluate(TO, ["#/calculate/s/nihss", ".field"])
                m["calculation update"].append(max(await pg.evaluate("""() => { const out = [];
                    for (const f of [...document.querySelectorAll('.field[data-field^=item_]')].slice(0, 8)) {
                      const inp = f.querySelector('input[type=radio]:not([value=__nt])'); const t0 = performance.now(); inp.click(); out.push(performance.now() - t0); }
                    return out; }""")))
                await ctx.close()
            for k, v in m.items():
                med = statistics.median(v); table.append((k, med, max(v), BUDGET[k]))
                check(f"{k}: median {med:.0f} ms, worst {max(v):.0f} ms (budget {BUDGET[k]} ms, 4× CPU throttle)", max(v) <= BUDGET[k])
            await b.close()
    finally: srv.terminate()
    with open(os.path.join(os.path.dirname(__file__), "..", "docs", "PERFORMANCE.md"), "w") as f:
        f.write("# Performance (4× CPU throttling, 412×915, 3 runs)\n\n| Measure | Median | Worst | Budget |\n|---|---|---|---|\n")
        for k, med, mx, bud in table: f.write(f"| {k} | {med:.0f} ms | {mx:.0f} ms | {bud} ms |\n")
    fl = [n for n, ok in results if not ok]; print(f"\n{len(results) - len(fl)} passed, {len(fl)} failed"); sys.exit(1 if fl else 0)
asyncio.run(main())
