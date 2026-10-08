# Changelog

All notable changes to Insula Neuro Score. Versions follow the Android `versionName`.
The app is **not clinically ready** in any version listed here; see [docs/MEDICAL-CONTENT-AUDIT.md](docs/MEDICAL-CONTENT-AUDIT.md).

## [Unreleased]
### Added
- Release workflow: pushing a `v*` tag builds, tests, signs and publishes the APK to GitHub Releases.

## [0.10.0] - 2026-10-08
Neurosurgical Examination & Grades. Under-review scores removed from the app.

### Added
- **Neurosurgical Examination & Grades** group, split into sub-sections, with 16 newly implemented items (each with Calculator, Guide, sources, limitations, common errors and hand-checked tests):
  - Motor: MRC muscle power (0–5), MRC sum score (0–60, with the <48 ICU-acquired weakness threshold)
  - Reflexes: deep tendon reflex grade (NINDS Myotatic Reflex Scale, 0–4+), clonus (absent / unsustained / sustained), plantar response
  - Tone and spasticity: Modified Ashworth Scale, Modified Tardieu Scale (X, R1, R2, R2−R1)
  - Facial nerve: House-Brackmann I–VI
  - Hearing and CPA: Gardner-Robertson I–V
  - Vascular neurosurgery: Spetzler-Martin, Lawton-Young supplementary grade (with combined Supp-SM), Borden, Cognard
  - Neurotrauma: Markwalder chronic SDH grade (also listed under Traumatic brain injury)
  - Functional and neuro-oncology: KPS and ECOG (existing scores, cross-listed, unchanged)
  - Epilepsy surgery: Engel, ILAE outcome (with class 1a)
- New result type **Examination grade**: describes a bedside finding, not a prognosis.
- Category groups can have sub-sections and can list scores from other groups. Search, favourites and recent items work for every listed score.
- Future queue with catalogue IDs reserved (not shown in the app): Helsinki CT, Stockholm CT, IMPACT, CRASH, SCIM III, WISCI II, RPA, Evans Index, FOHR.
- `CHANGELOG.md` and release notes in `docs/releases/`.

### Changed
- The Calculate and Guide lists are headed **Scores & Grades**.
- The catalogue lists implemented scores only. Scores that are not implemented are kept in `catalog.json → withheld` with the reason, and are not shown.
- Gardner-Robertson reports both classes when the pure-tone average and speech discrimination fall in different classes, because published rules conflict.

### Removed (from the app)
- Under-review cards, badges and banners.
- FOUR, Modified Graeb, ASIA/AIS (ISNCSCI), ODI, Tokuhashi (1990), RASS, JOA, SOFA-2 and DS-GPA. Reasons are kept in the catalogue and audit.
- Related-score links to those scores, and stale "(under review)" labels.

### Not implemented
- Sunnybrook Facial Grading System: item points not confirmed from a primary source, the stated range does not match its weights, and licensing is unclear.

### Fixed
- The formula line no longer shows "=" when the result is not a sum (Modified Tardieu, TRISS).
- The calculation audit now tests optional inputs left blank and states that share a total.

### Notes
- This APK is signed with a new key. Uninstall earlier versions before installing.
- Tests: engine 328/328 (72 new hand-calculated cases); calculation audit 50 scores, about 1.04 million combinations, 0 issues; all UI suites pass.

## [0.9.2] - 2026-10-02
### Added
- TRISS (1995 MTOS coefficients), original SOFA (Sepsis-3 table), Graeb (1982), FAST-ED, mJOA (Benzel 1991), original GPA (Sperduto 2008).
- CI workflow: rebuild content, engine tests and calculation audit on every push.
### Fixed
- Score detail badge bug.
### Notes
- Revised Tokuhashi: conflicting reproductions of the vertebral-body item are flagged in the calculator. Scoring unchanged pending review.
- Audit evidence (2026-10-08): textbook corroboration recorded for Graeb, mJOA bands and SOFA.

## [0.9.1] - 2026-10-02
### Added
- Medical content audit: per-score evidence ledger, calculation audit across all input combinations, and a list of issues needing clinician review. Status set to **not clinically ready**.
### Changed
- RASS held back pending licensing review. GCS-P severe band labelled as not defined in the original publication.

## [0.9.0] - 2026-10-02
### Added
- Final UX and performance: responsive layouts (phone, tablet, landscape), 200% text, high-contrast tokens, larger touch targets, result bar, undoable reset.
- Accessibility audit (585 renders), performance tests under 4× CPU throttle, full user-journey tests.

## [0.8.0] - 2026-10-02
### Added
- Guide experience: 14 standard sections per score, related-score clusters, Guide ↔ Calculate navigation, guide search.

## [0.7.0] - 2026-10-02
### Added
- Library expansion to 29 implemented scores, each verified against cited sources; content audit generated from shipped data.

## [0.6.0] - 2026-10-02
### Added
- Personalized Home: favourite scores and guides, recent items, priority scores and groups, reorderable and hideable sections.

## [0.5.0] - 2026-10-02
### Added
- Clinical insight engine: result → interpretation → context → considerations → limitations → confounders, with tone policies per result type.

## [0.4.0] - 2026-10-01
### Added
- Fully implemented GCS, NIHSS, mRS and SINS. New logo.

## [0.3.0] - 2026-10-01
### Added
- Data-driven score engine (safe expression language, input types, not-testable handling, result model).

## [0.2.0] - 2026-10-01
### Added
- App shell and design system: Home, Calculate, Guide, Settings; themes; offline-first WebView shell; Gradle-free APK build.
