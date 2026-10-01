import asyncio, subprocess, sys, time
from playwright.async_api import async_playwright
srv = subprocess.Popen([sys.executable,"-m","http.server","8765","-d","app/assets"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
U="http://localhost:8765/index.html"
fails=[]
def check(name,cond):
    print(("PASS " if cond else "FAIL ")+name); 
    if not cond: fails.append(name)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(viewport={"width":390,"height":844},device_scale_factor=2)
        pg=await ctx.new_page(); errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m: m.type=="error" and errs.append(m.text))
        await pg.goto(U); await pg.wait_for_selector(".list")
        await pg.screenshot(path="tests/shots/01_home.png")
        check("home shows common scores", await pg.locator("text=Common scores").count()==1)
        # search
        await pg.fill("#q","vasospasm"); await pg.wait_for_timeout(100)
        check("search finds mFisher", await pg.locator("#results >> text=mFisher").count()>=1)
        await pg.fill("#q","sedation"); await pg.wait_for_timeout(100)
        check("search alias RASS", await pg.locator("#results >> text=RASS").count()>=1)
        await pg.fill("#q","zzz"); check("search empty msg", await pg.locator(".empty").count()==1)
        await pg.fill("#q","")
        # calculate list
        await pg.click(".tabbar >> text=Calculate"); await pg.wait_for_selector("text=Subarachnoid haemorrhage")
        await pg.screenshot(path="tests/shots/02_calc_list.png",full_page=True)
        # GCS calculator
        await pg.click("a.go:has-text('Glasgow Coma Scale')"); await pg.wait_for_selector("#calcform")
        check("incomplete initially", await pg.locator(".state.st-incomplete").count()==1)
        await pg.screenshot(path="tests/shots/03_gcs_empty.png")
        await pg.click("input[name=e][value='2'] >> xpath=..")
        await pg.click("input[name=v][value='2'] >> xpath=..")
        await pg.click("input[name=m][value='4'] >> xpath=..")
        check("GCS 8 high", await pg.locator(".state.st-high .state-value").inner_text()=="8")
        check("sticky bar shows 8", "8" in await pg.locator(".sticky-result").inner_text())
        await pg.screenshot(path="tests/shots/04_gcs_8.png")
        await pg.click(".sticky-result"); await pg.wait_for_timeout(200)
        await pg.screenshot(path="tests/shots/05_gcs_result.png")
        await pg.click("input[name=v][value='NT'] >> xpath=..")
        check("NT -> no total", (await pg.locator(".state-value").inner_text())=="E2 VNT M4")
        await pg.click("input[name=e][value='4'] >> xpath=.."); await pg.click("input[name=v][value='5'] >> xpath=.."); await pg.click("input[name=m][value='6'] >> xpath=..")
        check("GCS 15 normal", await pg.locator(".state.st-normal").count()==1)
        # pin
        await pg.click(".actions button.star"); check("pinned label", "Pinned" in await pg.locator(".actions button.star").inner_text())
        # open guide and back to calc keeps answers
        await pg.click("a.btn:has-text('Open guide')"); await pg.wait_for_selector("#g-sources")
        check("guide 15 sections", await pg.locator(".gsec").count()==15)
        await pg.screenshot(path="tests/shots/06_guide.png")
        await pg.screenshot(path="tests/shots/06b_guide_full.png",full_page=True)
        await pg.click(".guide-cta >> nth=0"); await pg.wait_for_selector("#calcform")
        check("answers persist across guide", await pg.locator(".state.st-normal").count()==1)
        await pg.click("button[data-act=reset]"); check("reset clears", await pg.locator(".state.st-incomplete").count()==1)
        # back navigation
        r=await pg.evaluate("window.handleBack()"); await pg.wait_for_timeout(200)
        check("back handled in app", r is True)
        # WFNS number input
        await pg.goto(U+"#/calc/wfns"); await pg.wait_for_selector("#calcform")
        await pg.fill("#n-gcs","15"); await pg.click("input[name=deficit][value=yes] >> xpath=..")
        check("WFNS undefined state", "Not defined" in await pg.locator(".state").inner_text())
        await pg.fill("#n-gcs","20"); check("WFNS invalid error", "whole number" in await pg.locator("#e-gcs").inner_text())
        await pg.fill("#n-gcs",""); await pg.click("button[data-act=step][data-d='1']")
        check("stepper from empty goes to min", await pg.input_value("#n-gcs")=="3")
        check("WFNS grade V", "Grade V" in await pg.locator(".state-value").inner_text())
        await pg.screenshot(path="tests/shots/07_wfns.png")
        # ICH
        await pg.goto(U+"#/calc/ich"); await pg.wait_for_selector("#calcform")
        for n,v in [("gcs","1"),("vol","1"),("ivh","yes"),("infra","0"),("age","0")]: await pg.click(f"input[name={n}][value='{v}'] >> xpath=..")
        check("ICH 3 -> 72%", "72%" in await pg.locator(".state-summary").inner_text())
        await pg.screenshot(path="tests/shots/08_ich.png")
        # RASS
        await pg.goto(U+"#/calc/rass"); await pg.wait_for_selector("#calcform")
        await pg.click("input[name=level][value='-4'] >> xpath=..")
        check("RASS -4 display", (await pg.locator(".state-value").inner_text())=="RASS -4")
        # home after pin
        await pg.goto(U+"#/home"); await pg.wait_for_selector(".list")
        check("priority scores shows GCS", await pg.locator("text=Priority scores").count()==1)
        check("recent calculators", await pg.locator("text=Recent calculators").count()==1)
        await pg.screenshot(path="tests/shots/09_home_personal.png",full_page=True)
        # settings: dark + startup + group hide
        await pg.goto(U+"#/settings"); await pg.wait_for_selector(".seg")
        await pg.click("button[data-k=theme][data-v=dark]")
        check("dark theme applied", await pg.evaluate("document.documentElement.dataset.theme")=="dark")
        await pg.click("input[data-act=ghide][data-id=sah]")
        await pg.screenshot(path="tests/shots/10_settings_dark.png",full_page=True)
        await pg.goto(U+"#/calc"); await pg.wait_for_selector(".list")
        check("hidden group removed", await pg.locator("h2:has-text('Subarachnoid')").count()==0)
        await pg.screenshot(path="tests/shots/11_calc_dark.png")
        await pg.goto(U+"#/calc/gcs"); await pg.wait_for_selector("#calcform")
        await pg.click("input[name=e][value='1'] >> xpath=.."); await pg.click("input[name=v][value='1'] >> xpath=.."); await pg.click("input[name=m][value='1'] >> xpath=..")
        await pg.click(".sticky-result"); await pg.wait_for_timeout(200)
        await pg.screenshot(path="tests/shots/12_gcs_dark.png")
        # startup preference
        await pg.goto(U+"#/settings"); await pg.click("button[data-k=startup][data-v=calc]")
        await pg.goto(U); await pg.wait_for_timeout(500)
        check("startup screen = calc", (await pg.evaluate("location.hash"))=="#/calc")
        # high contrast
        await pg.goto(U+"#/settings"); await pg.wait_for_selector(".switch input")
        await pg.click(".switch input"); check("high contrast", await pg.evaluate("document.documentElement.dataset.contrast")=="high")
        check("no JS errors (phone)", not errs); print(errs)
        # tablet
        t=await b.new_context(viewport={"width":1280,"height":800}); tp=await t.new_page(); terrs=[]
        tp.on("pageerror",lambda e:terrs.append(str(e)))
        await tp.goto(U+"#/calc/four"); await tp.wait_for_selector("#calcform")
        for n,v in [("e","4"),("m","0"),("b","4"),("r","4")]: await tp.click(f"input[name={n}][value='{v}'] >> xpath=..")
        check("tablet: locked-in insight", await tp.locator("text=locked-in").count()>=1)
        check("tablet: sticky bar hidden", not await tp.locator(".sticky-result").is_visible())
        await tp.screenshot(path="tests/shots/13_tablet_four.png")
        check("no JS errors (tablet)", not terrs)
        await b.close()
import os; os.makedirs("tests/shots",exist_ok=True)
try: asyncio.run(main())
finally: srv.terminate()
print(f"\n{'ALL PASSED' if not fails else str(len(fails))+' FAILED: '+', '.join(fails)}"); sys.exit(1 if fails else 0)
