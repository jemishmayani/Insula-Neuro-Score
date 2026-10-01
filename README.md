# Insula Neuro Score — Calculator & Guide

Offline-first clinical calculation and reference app for Neurology, Neurosurgery, Neurocritical Care, Stroke and Spine clinicians. Part of the Insula Neurosciences product family.

> Not a diagnostic or treatment tool. The app calculates validated scores, explains them, and shows their limitations.

## Status: Phase 1, app shell (v0.2.0)

The shell, design system, navigation, theming, responsive layout and local persistence are complete. **All scores are placeholders**; there is no calculator logic in this build.

A score engine and ten verified scores were prototyped earlier. They are preserved on the `engine-preview` branch for a later phase.

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
    js/app.js             router and screens
    content/catalog.json  placeholder catalogue (categories + score names; no criteria)
  build.sh                Gradle-free APK build
tests/shell.test.py       end-to-end shell tests (Playwright)
brand/                    app icon sources (SVG)
docs/                     architecture and phase reports
```

## Build and test

```bash
# Ubuntu 24.04
apt-get install android-sdk-platform-23 aapt apksigner zipalign dalvik-exchange openjdk-21-jdk-headless
pip install playwright && playwright install chromium

python3 tests/shell.test.py
cd app && KEYSTORE=/path/to/release.keystore KS_PASS=... ./build.sh
```

Without `KEYSTORE`, `build.sh` generates `keystore/local.keystore`. **Never commit keystores.** Updates must be signed with the same key.

Minimum Android 7.0 (API 24), target API 34.
