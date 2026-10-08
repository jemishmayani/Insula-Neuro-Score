# Insula Neuro Score — Calculator & Guide

Offline-first clinical calculation and reference app for Neurology, Neurosurgery, Neurocritical Care, Stroke and Spine clinicians. Part of the Insula Neurosciences product family.

> Not a diagnostic or treatment tool. The app calculates validated scores, explains them, and shows their limitations.

## Status: v0.11.0. **Not clinically ready**

50 scores and grades are implemented. Each was checked against its cited sources before implementation and is pending independent clinician review. Unresolved issues are listed in the [medical content audit](docs/MEDICAL-CONTENT-AUDIT.md).

- **What changed:** [CHANGELOG.md](CHANGELOG.md)
- **Latest release notes:** [docs/releases/v0.11.0.md](docs/releases/v0.11.0.md)
- **Download:** the APK is attached to each GitHub release. v0.11.0 installs over v0.10.0; uninstall versions before 0.10.0 first (new signing key from 0.10.0).

## Scores & Grades

Every item has a type: **Score** (points or a model give a total), **Grade** (one ordinal level, e.g. MRC 0–5, House-Brackmann), **Classification** (a category, e.g. Fisher, Cognard, Engel) or **Measurement** (e.g. Modified Tardieu angles). Grades and classifications are findings or categories, not prognostic scores.

**Quick groups** (on Home by default): **Quick Clinical Examination** (GCS, MRC power, House-Brackmann, reflex grade, Modified Ashworth) · **Neurotrauma** (GCS, GCS-P, Marshall, Rotterdam, ISS) · **Vascular** (Hunt & Hess, WFNS, Modified Fisher, Spetzler-Martin, Borden, Cognard).


| Group | Implemented |
|---|---|
| Consciousness | GCS, GCS-P, GOS, GOSE |
| Stroke | NIHSS, ASPECTS, pc-ASPECTS, ABCD², RACE, LAMS, FAST-ED |
| Intracerebral haemorrhage | ICH Score, FUNC, Graeb |
| Subarachnoid haemorrhage | Hunt & Hess, WFNS, Fisher, Modified Fisher |
| Traumatic brain injury | Marshall, Rotterdam, RTS, ISS, TRISS, Markwalder |
| Spine and spinal cord | Frankel, SINS, Nurick, mJOA |
| Neuro-oncology | KPS, ECOG, Tomita, Revised Tokuhashi, GPA |
| Functional and disability | mRS |
| Neurocritical care | SOFA (original) |
| **Neurosurgical Examination & Grades** | **Motor:** MRC power, MRC sum score · **Reflexes:** reflex grade (NINDS), clonus, plantar response · **Tone:** Modified Ashworth, Modified Tardieu · **Facial nerve:** House-Brackmann · **Hearing/CPA:** Gardner-Robertson · **Vascular:** Spetzler-Martin, Lawton-Young, Borden, Cognard · **Neurotrauma:** Markwalder · **Functional/neuro-oncology:** KPS, ECOG · **Epilepsy surgery:** Engel, ILAE outcome |

Only implemented scores appear in the app.

**Withheld** (recorded in `catalog.json` with the reason; no JSON ships, no links, not shown. RASS's verified content is kept only in `content_src/withheld.py`, which is never built): FOUR, RASS, ODI and ASIA/AIS (licensing); JOA and DS-GPA (version); Modified Graeb, Tokuhashi (1990) and SOFA-2 (verification); Sunnybrook (verification and licensing).

**Planned** (IDs reserved, not implemented): Helsinki CT, Stockholm CT, IMPACT, CRASH, SCIM III, WISCI II, RPA, Evans Index, FOHR.

## Principles

- Calculates, explains and shows limitations. It never turns a threshold into a treatment instruction.
- Never invents criteria or combines versions. Uncertain items are flagged or withheld.
- Fully offline. Inputs are never stored; only score IDs and times are kept for recent items.

## Documentation

[Architecture](docs/ARCHITECTURE.md) · [Score model](docs/SCORE-MODEL.md) · [Content audit](docs/CONTENT-AUDIT.md) · [Calculation audit](docs/CALCULATION-AUDIT.md) · [Medical content audit](docs/MEDICAL-CONTENT-AUDIT.md) · [Performance](docs/PERFORMANCE.md) · v0.10 notes: [docs/V0.10.md](docs/V0.10.md) · Phase reports: [1](docs/PHASE-1.md) [2](docs/PHASE-2.md) [3](docs/PHASE-3.md) [4](docs/PHASE-4.md) [5](docs/PHASE-5.md) [6](docs/PHASE-6.md) [7](docs/PHASE-7.md) [8](docs/PHASE-8.md)

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
    content/catalog.json  catalogue: implemented scores (shown), withheld and planned entries (not shown), group sub-sections
  build.sh                Gradle-free APK build
tests/engine/             engine unit tests + per-score fixtures (node --test)
tests/calculator.test.py  calculator UI tests (Playwright)
tests/home.test.py        personalization + performance tests (Playwright)
tests/shell.test.py       shell regression tests (Playwright)
content_src/              score content source (library.py, library2.py, library3.py; itemtypes.py types + quick groups; related.py; withheld.py never built)
tools/                    calculation, content and medical audits; evidence ledger
brand/                    app icon sources (SVG). Current logo: Insula_Neuro_Score_Full_Better.svg
docs/                     architecture and phase reports
```

## Build and test

```bash
# Ubuntu 24.04
apt-get install android-sdk-platform-23 aapt apksigner zipalign dalvik-exchange openjdk-21-jdk-headless
pip install playwright && playwright install chromium

python3 content_src/build_scores.py      # score JSON from source
python3 tools/consistency_check.py       # catalogue, JSON, links, fixtures and audit evidence agree
node --test tests/engine/*.test.js      # engine unit + fixture tests
python3 tests/calculator.test.py        # calculator UI tests
python3 tests/shell.test.py             # shell regression
python3 tests/home.test.py              # personalization + performance
python3 tests/library.test.py           # every calculator and guide in the UI
python3 tests/guide.test.py             # guide structure, navigation, all related links, search
python3 tests/journey.test.py           # full user journey (phone + tablet), errors, reduced motion
python3 tests/perf.test.py              # performance under 4x CPU throttle
python3 tests/audit.py                  # 585-render responsiveness/accessibility/contrast audit
node tools/calc_audit.js                # calculation audit (all combinations)
python3 tools/medical_audit.py          # regenerate docs/MEDICAL-CONTENT-AUDIT.md
python3 tools/content_audit.py          # regenerate docs/CONTENT-AUDIT.md
cd app && KEYSTORE=/path/to/release.keystore KS_PASS=... ./build.sh
```

### Releasing

`.github/workflows/release.yml` builds, tests, signs and publishes the APK as a GitHub release. To release:

1. Bump `versionCode` and `versionName` in `app/AndroidManifest.xml`.
2. Add `docs/releases/vX.Y.Z.md` and a CHANGELOG entry.
3. Push to `main`.

When no release exists yet for that version, the workflow creates the tag and the release with the APK attached. Pushes that don't change the version are skipped. Pushing a `v*` tag, or Actions → release → Run workflow, also works. Signing uses three repository secrets: `ANDROID_KEYSTORE_B64` (base64 of the keystore), `ANDROID_KS_PASS` and `ANDROID_KEY_ALIAS`.

Without `KEYSTORE`, `build.sh` generates `keystore/local.keystore`. **Never commit keystores.** Updates must be signed with the same key.

Minimum Android 7.0 (API 24), target API 34.
