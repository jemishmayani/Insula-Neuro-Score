# Insula Neuro Score — Calculator & Guide

Offline-first clinical calculation and reference app for Neurology, Neurosurgery, Neurocritical Care, Stroke and Spine clinicians. Part of the Insula Neurosciences product family.

> **Not a diagnostic or treatment tool.** The app calculates validated scores, explains them, and shows their limitations. It never turns a threshold into a treatment instruction.

## Status: Phase 1 (v0.1.0)

| Area | Status |
|---|---|
| Score engine (data-driven, no `eval`) | Done |
| Home · Calculate · Guide · Settings | Done |
| Personalisation (pinned scores, saved guides, recents, group order/visibility, startup screen, theme, high contrast) | Done |
| Scores | GCS, GCS-P, FOUR, ICH Score, Hunt & Hess, WFNS (1988), m-WFNS (2015), Modified Fisher, mRS, RASS |

All score content is **pending independent clinician review** before clinical release (shown in-app on every guide).

## Repository layout

```
app/
  AndroidManifest.xml
  src/com/insula/neuroscore/MainActivity.java   native shell (local origin, share/copy, system bars)
  res/                                          launcher + adaptive icons
  assets/
    index.html, css/app.css, js/app.js          UI
    js/engine.js                                score engine
    content/manifest.json                       categories + score index
    content/scores/<id>.json                    one file per score (generated)
  build.sh                                      Gradle-free APK build
content_src/scores.py                           score content source → JSON
tests/engine.test.js                            engine + scoring tests (node)
tests/ui.test.py                                end-to-end UI tests (Playwright)
brand/                                          app icon sources (SVG)
docs/                                           architecture, schema, phase reports
```

## Build

Requirements (Ubuntu 24.04): `apt-get install android-sdk-platform-23 aapt apksigner zipalign dalvik-exchange openjdk-21-jdk-headless`

```bash
python3 content_src/scores.py      # regenerate content JSON
node tests/engine.test.js          # scoring tests
python3 tests/ui.test.py           # UI tests (needs: pip install playwright && playwright install chromium)
cd app && KEYSTORE=/path/to/release.keystore KS_PASS=... ./build.sh
```

Without `KEYSTORE`, `build.sh` creates `keystore/local.keystore`. **Never commit keystores.** Every update must be signed with the same key, so keep the release keystore backed up privately.

Minimum Android 7.0 (API 24), target API 34.

## Adding or updating a score

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). In short: add a dict to `content_src/scores.py` (or a JSON file directly), run the generator and tests. No UI code changes are needed. Every score must have verified criteria, a named version, sources, limitations and licensing status before it is added.
