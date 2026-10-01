# Phase 1 report: engine, shell and first validated score set

## What was built
- Data-driven score engine with a safe expression language, not-testable handling, conditional insights and share text.
- Native Android shell: private local origin, offline-only networking, share/copy, theme-aware system bars, system text scaling, content-override folder.
- Home (search, priority/pinned scores, score-group shortcuts, recent calculators, recent guides, saved guides), Calculate, Guide (15 standard sections, "Calculate this score →"), Settings (theme, high contrast, startup screen, priority score ordering, group ordering/visibility/Home shortcuts, clear/reset).
- Result-driven UI: 8 semantic states, each with colour, icon and label; sticky result bar on phones; two-pane calculator on tablets.
- Ten scores: GCS, GCS-P, FOUR, ICH Score, Hunt & Hess (1968 with modifier), WFNS (1988), m-WFNS (2015), Modified Fisher (2006), mRS, RASS.

## Verification and licensing notes
- GCS-P formula (GCS − PRS, range 1–15) and the WFNS/m-WFNS definitions were checked against published sources. The modified Fisher crude odds ratios are taken from Frontera 2006.
- Undefined combinations are surfaced, not guessed: WFNS GCS 15 with deficit, and modified Fisher IVH without SAH.
- FOUR: the official figure is © Mayo Foundation. Criteria are in original wording; confirm permission before commercial distribution.
- GCS: official teaching aids are not reproduced.

## Tests
- `tests/engine.test.js`: 69 checks, covering content validation, known values for every score, edge cases, and exhaustive input combinations (e.g. 420 for GCS-P, 625 for FOUR).
- `tests/ui.test.py`: 30 end-to-end checks on phone and tablet viewports covering search, calculation, NT handling, pinning, guide↔calculator round trip with preserved inputs, reset, back handling, invalid number input, dark mode, hidden groups, startup screen and high contrast, with zero JavaScript errors.

## Known issues
- Content has not yet had independent clinician review.
- Not yet tested on physical devices: hardware back, share sheet and system-bar colours were verified only by code review.
- The content-override folder exists, but no update mechanism populates it yet.
- Paediatric GCS is not implemented.

## Recommended Phase 2
Stroke and ICH expansion: NIHSS (public domain; full 15-item implementation with untestable-item rules), ASPECTS and pc-ASPECTS (region checklist input type), FUNC, Graeb and modified Graeb, original Fisher. This adds `checklist` and `multi-region` input types to the engine.
