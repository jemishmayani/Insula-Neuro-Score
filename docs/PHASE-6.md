# Phase 6 report: score library expansion (v0.7.0)

**29 scores implemented, 12 under review, 0 unverified.** Full table: [CONTENT-AUDIT.md](CONTENT-AUDIT.md), generated from shipped data by `tools/content_audit.py`.

## Verification log (this phase)
| Scores | Verified against |
|---|---|
| ASPECTS, pc-ASPECTS | Region definitions and weights from multiple independent descriptions of Barber 2000 and Puetz 2008 (Radiopaedia, trial protocol, patent text) |
| ABCD² | Johnston 2007 Lancet abstract (PubMed): points, risk groups and 2-day risks |
| RACE | Pérez de la Ossa 2014, via official EMS cards citing the authors (items, 0–9, aphasia/agnosia rule, ≥5 sensitivity) |
| LAMS | AHA material and Nazliel 2008 title (items 0–5, ≥4 association) |
| FUNC | Rost 2008 (PMC table and original paper excerpt): components 0–11; outcome statements from the paper |
| Fisher, Modified Fisher | Fisher 1980 grade definitions (non-monotonic); Frontera 2006 (verified in Phase 1) |
| Marshall, Rotterdam | Category definitions (Radiopaedia, published tables); Rotterdam items, +1 and 6-month mortality (Maas 2005) |
| RTS, ISS | Champion 1989 coding and weights; Baker 1974 sum of squares and the AIS 6 = 75 rule (trial protocols, LITFL, MDM) |
| Frankel, Nurick | Grade definitions (Frankel 1969; Nurick 1972, Brain) |
| Revised Tokuhashi, Tomita | Parameter tables reproduced from Tokuhashi 2005 and Tomita 2001 (WJO review, PMC) |
| KPS, ECOG | Structure and sources (Karnofsky 1949; Oken 1982) |
| GOS, GOSE | Category definitions; GOSE interview © 1998 (not reproduced) |
| GCS-P, ICH, Hunt & Hess, WFNS, RASS | Verified in Phase 1 and re-used |

## Not implemented (under review): reason shown in the app and in the audit
- **Licensing:**
  - FOUR (Mayo figure).
  - ISNCSCI/AIS (ASIA/ISCoS terms and revisions).
  - mJOA: permission statements in reproductions, and descriptor wording that differs between sources.
  - ODI: copyrighted questionnaire.
- **Version:**
  - TRISS: several coefficient sets.
  - JOA: several versions.
  - SOFA: SOFA-2 was published in JAMA 2025.
  - GPA: disease-specific versions that are updated frequently.
  - Tokuhashi 1990: superseded by the revised version.
- **Verification:**
  - FAST-ED: published tools define the denial/neglect item differently.
  - Graeb and modified Graeb: definitions not yet verified against the primary source.

## Process per implemented score
Verified → structured data (`content_src/library.py`) → manually verified fixtures (`tests/engine/fixtures/<id>.fixture.json`, with the hand calculation recorded) → all-combination engine sweep → safety lint → Guide (15 sections generated from data) → UI walkthrough (`tests/library.test.py`).

## Engine and UI changes (minimal)
- **Engine:**
  - `largest(k, …)` added to the expression language (needed by ISS).
  - `formulaEquals` added for formula lines that are context rather than an equation (RTS).
  - The incomplete and not-interpretable tones are always allowed, since they are status markers.
- **UI:**
  - An "Under review" badge, and the review reason on the detail and guide screens.
  - The result bar compacts only code-style formulas (e.g. E3 V4 M5).
- **No architectural changes.**

## Tests: all passing
- Engine: **221**, including 160 manually verified fixture cases across 29 scores, and the all-combination sweep (more than 10,000 evaluations) with tone-policy and range checks.
- Library UI walkthrough: **73**.
- Calculator UI: **109**.
- Shell: **99**.
- Home: **69**.

## Integrity fix during this phase
I removed **29 DOIs that I had written from memory and could not confirm in this session**: 23 in the new library and 6 in the Phase 3 scores. The citations (authors, title, journal, year) remain. Only DOIs seen in search results are kept. All bibliographic details are flagged for checking during clinical review.

## Known limitations
- All content is pending independent clinician review. Citation details, including volume, pages and the remaining DOIs, need a reference check.
- KPS and ECOG wording follows the standard published definitions, but this session did not see the full text of the original 1949 and 1982 sources.
- GOSE records categories only. Reliable assignment needs the official structured interview, which is not included.
- Tested in a browser at device sizes, not on a physical device.
