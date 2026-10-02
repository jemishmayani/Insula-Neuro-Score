"""Phase 8 audit: every key screen × device × theme × text size.
Checks overflow, clipped text, overlapping controls, touch targets, accessible names, WCAG contrast.
Usage: python3 tests/audit.py [--quick]   (prints a findings report; exit 1 if any finding)"""
import asyncio, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "assets"); PORT = 8770; U = f"http://localhost:{PORT}/index.html"
QUICK = "--quick" in sys.argv

DEVICES = [("small-android 360x640", 360, 640), ("large-android 412x915", 412, 915), ("tablet 800x1280", 800, 1280), ("tablet-landscape 1280x800", 1280, 800), ("phone-landscape 915x412", 915, 412)]
SCALES = [1.0, 1.3, 2.0]
THEMES = ["light", "dark", "dark-hc"]
SEED = {"v": 3, "favorites": ["gcs", "sins"], "favoriteGuides": ["nihss"], "recentCalc": [{"id": "gcs", "at": 1}], "recentGuide": [{"id": "sins", "at": 1}],
        "priorityScores": ["gcs", "nihss", "wfns", "sins"], "priorityGroups": ["stroke", "sah"]}
SCREENS = [("home", "#/home", None), ("calculate", "#/calculate", None), ("category", "#/calculate/c/sah", None),
           ("gcs-filled", "#/calculate/s/gcs", "gcs"), ("nihss", "#/calculate/s/nihss", None), ("iss", "#/calculate/s/iss", "iss"), ("rts", "#/calculate/s/rts", "rts"),
           ("aspects", "#/calculate/s/aspects", "aspects"), ("guide-gcs", "#/guide/s/gcs", None), ("guide-sins", "#/guide/s/sins", None),
           ("review-sofa", "#/guide/s/sofa", None), ("settings", "#/settings", None), ("search", "#/guide?search=sah", "search")]
if QUICK: DEVICES, SCALES, THEMES = DEVICES[:1] + DEVICES[3:4], [1.0, 2.0], ["light", "dark"]

PROBE = r"""
(() => {
  const out = { overflow: document.documentElement.scrollWidth > innerWidth + 1, clipped: [], overlaps: [], small: [], unnamed: [], contrast: [] };
  const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !e.closest('[hidden],details:not([open]) > :not(summary)'); };
  const isFixed = e => { for (let x = e; x; x = x.parentElement) { const p = getComputedStyle(x).position; if (p === 'fixed' || p === 'sticky') return x; } return null; };
  const label = e => (e.getAttribute('aria-label') || e.textContent || e.id || e.className || e.tagName).trim().replace(/\s+/g, ' ').slice(0, 40);
  // clipped text (overflow hidden without ellipsis)
  for (const e of document.querySelectorAll('main *, .appbar *, .result-bar *, .bottomnav *')) {
    if (!vis(e) || !e.childNodes.length || e.closest('.vh') || e.matches('input, select')) continue;   // visually-hidden labels are clipped by design; inputs scroll
    const s = getComputedStyle(e);
    if ((s.overflowX === 'hidden' || s.overflow === 'hidden') && s.textOverflow !== 'ellipsis' && e.scrollWidth > e.clientWidth + 2 && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()))
      out.clipped.push(label(e) + ' ' + e.scrollWidth + '>' + e.clientWidth);
  }
  // interactive elements
  const ctrls = [...document.querySelectorAll('button, a[href], input:not(.vh):not([type=radio]):not([type=checkbox]), select, label.choice, .segmented > *, summary')].filter(vis);
  for (const e of ctrls) {
    const r = e.getBoundingClientRect();
    const tiny = (r.height < 44 || r.width < 44) && !e.closest('.toc') && !e.matches('main p a, .sources a, .lede a, .badges a, .ins-body a');
    if (tiny) out.small.push(label(e) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
    const name = e.getAttribute('aria-label') || e.textContent.trim() || (e.id && document.querySelector('label[for="' + e.id + '"]')) || e.getAttribute('aria-labelledby');
    if (!name) out.unnamed.push(e.outerHTML.slice(0, 60));
  }
  const flow = ctrls.filter(e => !isFixed(e));
  for (let i = 0; i < flow.length; i++) for (let j = i + 1; j < flow.length; j++) {
    const a = flow[i], b = flow[j]; if (a.contains(b) || b.contains(a)) continue;
    if ([a, b].some(x => x.closest('.searchbar .clear'))) continue;   // clear button sits inside the search field by design
    const r = a.getBoundingClientRect(), q = b.getBoundingClientRect();
    const w = Math.min(r.right, q.right) - Math.max(r.left, q.left), h = Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top);
    if (w > 2 && h > 2) out.overlaps.push(label(a) + ' ⟷ ' + label(b));
  }
  // contrast (WCAG AA): text nodes vs effective background
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const blend = (top, bot) => ({ r: top.r * top.a + bot.r * (1 - top.a), g: top.g * top.a + bot.g * (1 - top.a), b: top.b * top.a + bot.b * (1 - top.a), a: 1 });
  const bgOf = e => { const stack = []; for (let x = e; x; x = x.parentElement) { const c = parse(getComputedStyle(x).backgroundColor); if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break; } }
                      let bg = parse(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255, a: 1 }; for (let i = stack.length - 1; i >= 0; i--) bg = blend(stack[i], bg); return bg; };
  const seen = new Set();
  for (const e of document.querySelectorAll('body *')) {
    if (!vis(e) || e.closest('svg') || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const s = getComputedStyle(e); let fg = parse(s.color); if (!fg) continue;
    const op = parseFloat(s.opacity) * (e.closest('[aria-disabled=true],[disabled]') ? 0 : 1); if (op === 0) continue;   // disabled controls exempt (WCAG 1.4.3)
    const bg = bgOf(e); fg = blend({ ...fg, a: fg.a * op }, bg);
    const L1 = lum(fg), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const size = parseFloat(s.fontSize), bold = parseInt(s.fontWeight) >= 700, large = size >= 24 || (bold && size >= 18.66);
    const need = large ? 3 : 4.5;
    if (ratio < need) { const k = label(e) + ' ' + ratio.toFixed(2); if (!seen.has(k)) { seen.add(k); out.contrast.push(k); } }
  }
  return out;
})()"""

async def prep(pg, screen, extra):
    if extra == "gcs":
        for i, v in [("e", "2"), ("v", "3"), ("m", "5")]: await pg.click(f'.field[data-field="{i}"] input[value="{v}"] >> xpath=..')
    elif extra == "iss":
        for i, v in [("head", 3), ("chest", 4), ("abdomen", 5)]: await pg.fill(f"#in-{i}", str(v))
    elif extra == "rts":
        for i, v in [("gcs", 8), ("sbp", 70), ("rr", 32)]: await pg.fill(f"#in-{i}", str(v))
    elif extra == "aspects":
        await pg.click('.field[data-field="regions"] input[value="i"] >> xpath=..')
    elif extra == "search":
        await pg.fill("#search", "sah"); await pg.wait_for_timeout(50)

async def run():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    findings = {}; errs = []
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            for dname, w, h in DEVICES:
                for theme in THEMES:
                    for scale in SCALES:
                        ctx = await b.new_context(viewport={"width": w, "height": h}); pg = await ctx.new_page()
                        pg.on("pageerror", lambda e: errs.append(str(e)))
                        st = dict(SEED, theme="dark" if theme.startswith("dark") else "light", highContrast=theme.endswith("hc"))
                        await pg.goto(U); await pg.evaluate("s => localStorage.setItem('ins.store.v3', JSON.stringify(s))", st)
                        if scale != 1.0: await pg.add_init_script(f"document.addEventListener('DOMContentLoaded', () => document.documentElement.style.fontSize = '{16 * scale}px')")
                        await pg.reload(); await pg.wait_for_selector(".bottomnav")
                        for sname, h_, extra in SCREENS:
                            target = h_.split("?")[0]
                            await pg.goto(U + target); await pg.wait_for_selector(".bottomnav"); await pg.wait_for_timeout(120)
                            try: await prep(pg, sname, extra)
                            except Exception as e: findings.setdefault(f"{sname}: prep failed", set()).add(f"{dname}/{theme}/{scale}: {str(e)[:80]}"); continue
                            r = await pg.evaluate(PROBE)
                            key = f"{dname} · {theme} · {int(scale*100)}%"
                            if r["overflow"]: findings.setdefault(f"{sname}: horizontal overflow", set()).add(key)
                            for kind in ["clipped", "overlaps", "small", "unnamed", "contrast"]:
                                for item in r[kind]: findings.setdefault(f"{sname}: {kind}: {item}", set()).add(key)
                        await ctx.close()
            await b.close()
    finally: srv.terminate()
    for k in sorted(findings): print(f"- {k}\n    ({len(findings[k])}×) e.g. {sorted(findings[k])[0]}")
    print(f"\n{len(findings)} distinct findings; JS errors: {len(set(errs))} {list(set(errs))[:2]}")
    return 1 if findings or errs else 0

sys.exit(asyncio.run(run()))
