# Insula Neuro Score — Calculator & Guide

Offline-first clinical calculation and reference app for Neurology, Neurosurgery, Neurocritical Care, Stroke and Spine clinicians. Part of the Insula Neurosciences product family.

> Not a diagnostic or treatment tool. The app calculates validated scores, explains them, and shows their limitations.

## Status: Phase 8 complete, final UX and performance (v0.9.0)

**29 scores implemented**, each verified against cited sources; **12 under review**, with the reason recorded (licensing, version or verification). See [docs/CONTENT-AUDIT.md](docs/CONTENT-AUDIT.md). Each was verified against its authoritative source. Results and guides are built by the structured clinical insight engine. Final UX and performance: [docs/PHASE-8.md](docs/PHASE-8.md). Guide experience: [docs/PHASE-7.md](docs/PHASE-7.md). Library expansion: [docs/PHASE-6.md](docs/PHASE-6.md). Personalized Home: [docs/PHASE-5.md](docs/PHASE-5.md). See [docs/PHASE-4.md](docs/PHASE-4.md), [docs/PHASE-3.md](docs/PHASE-3.md) and [docs/SCORE-MODEL.md](docs/SCORE-MODEL.md).

## Repository layout

```
app/
  AndroidManifest.xml
  src/com/insula/neuroscore/MainActivity.java  native shell (local origin, offline-only, theme-aware system bars)
  res/                                         launcher + adaptive icons
  assets/
    index.html
    css/tokens.css        design tokens: the ONLY place colour values live (light, dark, high contrast)
    css/components.css    component and layout styles (tokens only)
    js/ui.js              design-system components
    js/store.js           versioned local persistence (+ migration from v0.1.0)
    js/engine/            score engine (expr.js, inputs.js, insights.js, engine.js); pure, also runs in Node
    js/calculator.js      renders inputs from definitions and the engine's result model
    js/app.js             router and screens
    content/scores/       implemented scores (generated from content_src/)
    content/dev/          non-clinical input-types demo
    content/catalog.json  placeholder catalogue (categories + score names; no criteria)
  build.sh                Gradle-free APK build
tests/engine/             engine unit tests + per-score fixtures (node --test)
tests/calculator.test.py  calculator UI tests (Playwright)
tests/home.test.py        personalization + performance tests (Playwright)
tests/shell.test.py       shell regression tests (Playwright)
content_src/              score content source (library.py, related.py clusters)
brand/                    app icon sources (SVG). Current logo: Insula_Neuro_Score_Full_Better.svg
docs/                     architecture and phase reports
```

## Build and test

```bash
# Ubuntu 24.04
apt-get install android-sdk-platform-23 aapt apksigner zipalign dalvik-exchange openjdk-21-jdk-headless
pip install playwright && playwright install chromium

python3 content_src/build_scores.py      # score JSON from source
node --test tests/engine/*.test.js      # engine unit + fixture tests
python3 tests/calculator.test.py        # calculator UI tests
python3 tests/shell.test.py             # shell regression
python3 tests/home.test.py              # personalization + performance
python3 tests/library.test.py           # every calculator and guide in the UI
python3 tests/guide.test.py             # guide structure, navigation, all related links, search
python3 tests/journey.test.py           # full user journey (phone + tablet), errors, reduced motion
python3 tests/perf.test.py              # performance under 4x CPU throttle
python3 tests/audit.py                  # 585-render responsiveness/accessibility/contrast audit
python3 tools/content_audit.py          # regenerate docs/CONTENT-AUDIT.md
cd app && KEYSTORE=/path/to/release.keystore KS_PASS=... ./build.sh
```

Without `KEYSTORE`, `build.sh` generates `keystore/local.keystore`. **Never commit keystores.** Updates must be signed with the same key.

Minimum Android 7.0 (API 24), target API 34.
