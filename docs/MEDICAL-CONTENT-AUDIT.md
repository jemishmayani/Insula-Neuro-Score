# Medical content audit (Phase 9)

> **Not clinically ready.** Unresolved items below require review by a qualified clinician before any clinical use. Calculation engine and data are internally consistent; source fidelity is verified as described per score.

Legend: **Verified** = matched a primary or authoritative source; **Verified (secondary)** = matched several independent secondary sources (primary full text not seen); **Editorial** = guidance text needing clinician review; **⚠ FLAG** = manual verification required.

## 1. Content audit

| Score | Version | Calculation verified | Interpretation verified | Population verified | Limitations verified | Source verified | Automated tests | Manual tests | Last reviewed |
|---|---|---|---|---|---|---|---|---|---|
| GCS | Adult GCS, Glasgow structured approach | Verified | Verified | Verified | Editorial | Verified | 14 hand-calculated cases; 120 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-01 |
| GCS-P | GCS-P (Brennan, Murray & Teasdale 2018) | Verified | ⚠ FLAG | Verified | Editorial | Verified | 7 hand-calculated cases; 360 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| GOS | GOS, five categories (Jennett & Bond 1975) | Verified | Verified | Verified | Editorial | Verified | 4 hand-calculated cases; 5 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| GOSE | GOSE, eight categories (Wilson et al. 1998) | Verified | Verified | Verified | Editorial | Verified | 4 hand-calculated cases; 8 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| ABCD² | ABCD² (Johnston et al. 2007) | Verified | Verified | Verified | Editorial | Verified | 6 hand-calculated cases; 72 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| ASPECTS | ASPECTS (Barber et al. 2000), non-contrast CT | Verified (secondary) | Verified | Verified | Editorial | Verified (secondary) | 5 hand-calculated cases; 1,024 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| FAST-ED | FAST-ED (Lima et al. 2016) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 162 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-03 |
| LAMS | LAMS (Llanes et al. 2004) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 18 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| NIHSS | NINDS NIH Stroke Scale (2024 update), 15 items | Verified | Verified | Verified | Editorial | Verified | 15 hand-calculated cases; 300,059 combinations (sampled + extremes); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-01 |
| pc-ASPECTS | pc-ASPECTS (Puetz et al. 2008) | Verified (secondary) | Verified | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 256 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| RACE | RACE (Pérez de la Ossa et al. 2014) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 162 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| FUNC | FUNC (Rost et al. 2008) | Verified | Verified | Verified | Editorial | Verified | 4 hand-calculated cases; 108 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| Graeb | Original Graeb score (Graeb et al. 1982) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 225 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-03 |
| ICH Score | ICH Score (Hemphill et al. 2001) | Verified | Verified | Verified | Editorial | Verified | 4 hand-calculated cases; 48 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| Fisher | Original Fisher scale (1980) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 4 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| Hunt & Hess | Hunt & Hess 1968 (original, with modifier) | Verified | Verified | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 10 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| mFisher | Modified Fisher (Frontera et al. 2006) | Verified | Verified | Verified | Editorial | Verified | 4 hand-calculated cases; 6 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| WFNS | Original WFNS (1988) | Verified | Verified | Verified | Editorial | Verified | 6 hand-calculated cases; 26 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| ISS | ISS (Baker et al. 1974) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 8 hand-calculated cases; 117,649 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| Marshall | Marshall CT classification (1991) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 7 hand-calculated cases; 32 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| Rotterdam | Rotterdam CT score (Maas et al. 2005) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 24 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| RTS | RTS (Champion et al. 1989), weighted | Verified | Verified (secondary) | Verified | Editorial | Verified | 7 hand-calculated cases; 3,328 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| TRISS | TRISS with 1995 MTOS coefficients (Champion et al.) | Verified (secondary) | Verified | Verified | Editorial | Verified (secondary) | 6 hand-calculated cases; 300,007 combinations (sampled + extremes); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-03 |
| Frankel | Frankel grade (Frankel et al. 1969) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 5 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| mJOA | mJOA, clinician-rated (Benzel et al. 1991), 0–18 | Verified | Verified | Verified | Editorial | Verified (secondary) | 8 hand-calculated cases; 768 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-03 |
| Nurick | Nurick grade (1972) | Verified (secondary) | Verified (secondary) | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 6 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| SINS | SOSG SINS (Fisher et al. 2010) | Verified | Verified | Verified | Editorial | Verified | 12 hand-calculated cases; 1,296 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-01 |
| ECOG | ECOG Performance Status (Oken et al. 1982) | Verified | Verified | Verified | Editorial | Verified | 3 hand-calculated cases; 6 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| GPA | Original GPA (Sperduto et al. 2008, RTOG database) | Verified | Verified | Verified | Editorial | Verified | 7 hand-calculated cases; 54 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-03 |
| KPS | Karnofsky Performance Status (Karnofsky 1949) | Verified | Verified | Verified | Editorial | Verified (secondary) | 6 hand-calculated cases; 11 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| Revised Tokuhashi | Revised Tokuhashi (Tokuhashi et al. 2005) | ⚠ FLAG | Verified | Verified | Editorial | Verified (secondary) | 5 hand-calculated cases; 1,458 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| Tomita | Tomita score (Tomita et al. 2001) | Verified | Verified | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 18 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-02 |
| mRS | Modified Rankin Scale 0–6 (van Swieten et al. 1988) | Verified | Verified | Verified | Editorial | Verified | 9 hand-calculated cases; 7 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-01 |
| SOFA | Original SOFA (Vincent et al. 1996), as tabulated in Sepsis-3 (Singer et al. 2016) | Verified | Verified | Verified | Editorial | Verified | 5 hand-calculated cases; 15,625 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-03 |
| Borden | Borden classification (Borden, Wu & Shucart 1995), types I–III with subtypes a/b | Verified | Verified | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 9 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Clonus | Descriptive examination record: absent, unsustained or sustained | Verified | Editorial | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 135 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Cognard | Cognard revised classification (Cognard et al. 1995): I, IIa, IIb, IIa+b, III, IV, V | Verified | Verified | Verified | Editorial | Verified (secondary) | 5 hand-calculated cases; 7 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Engel | Engel classification (Engel et al. 1993), classes I–IV with subclasses | Verified | Verified | Verified | Editorial | Verified (secondary) | 5 hand-calculated cases; 39 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Gardner-Robertson | Gardner-Robertson modified hearing classification (1988) | Verified | Verified | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 25 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| House-Brackmann | House-Brackmann grading system, grades I–VI (House & Brackmann 1985) | Verified | Verified | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 18 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| ILAE outcome | ILAE outcome classification (Wieser et al. 2001), classes 1–6 with 1a | Verified | Verified | Verified | Editorial | Verified | 5 hand-calculated cases; 54 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Lawton-Young | Lawton-Young supplementary grading scale (Lawton et al. 2010) | Verified | Verified (secondary) | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 72 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Markwalder | Markwalder grading scale (1981), grades 0–4 | Verified | Verified | Verified | Editorial | Verified (secondary) | 3 hand-calculated cases; 5 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| MAS | Modified Ashworth Scale (Bohannon & Smith 1987) | Verified | Verified | Verified | Editorial | Verified (secondary) | 6 hand-calculated cases; 126 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| MRC power | Medical Research Council scale, grades 0–5 | Verified | Verified | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 18 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| MRC-SS | MRC sum score, 12 muscle groups (Kleyweg et al. 1991) | Verified | Verified | Verified | Editorial | Verified (secondary) | 6 hand-calculated cases; 300,074 combinations (sampled + extremes); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| MTS | Modified Tardieu Scale (Boyd & Graham 1999) | Verified | Verified (secondary) | Verified | Editorial | Verified (secondary) | 6 hand-calculated cases; 576 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Plantar | Descriptive examination record: flexor, extensor, equivocal or no response | Verified | Verified | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 12 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Reflex grade | NINDS Myotatic Reflex Scale, 0–4 (Hallett 1993) | Verified | Verified | Verified | Editorial | Verified | 5 hand-calculated cases; 105 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |
| Spetzler-Martin | Spetzler-Martin grading system (1986), grades I–V | Verified | Verified | Verified | Editorial | Verified (secondary) | 4 hand-calculated cases; 12 combinations (all); fuzz | Scripted UI walkthrough (calculator + guide); human clinical testing pending | 2026-10-08 |

### Verified but held back (licensing review)

| Score | Calculation | Source | Tests | Reason |
|---|---|---|---|---|
| RASS | Verified | Verified | 4 hand-calculated cases retained | Virginia Commonwealth University lists RASS as a licensable technology; terms for use in a commercial app must be confirmed. Content is verified and ready to reinstate after licensing review. |

## 2. Calculation audit

All 50 implemented scores were evaluated through the production engine: **1,044,254 input combinations** (exhaustive where the input space allows; otherwise a 300,000 sample plus every extreme and one-step variant).

For every score the audit confirmed: every component's point values; reachable minimum and maximum equal the declared range; every result state is reached, and only within its stated range; every threshold boundary; missing input → incomplete; not-testable input → blocked or excluded-and-flagged as designed. **Internal calculation issues found: 0.** Full per-score tables (components, states, boundaries): [CALCULATION-AUDIT.md](CALCULATION-AUDIT.md).

Internal consistency does not prove source fidelity: the source column above and the flags below cover that.

## 3. Unresolved issues

1. **GCS-P**: The 1–8 'severe range' is not defined in the original publication (secondary sources only). Content now states this; clinician to confirm whether any band should be shown.
2. **FAST-ED**: No derivation cut-off is applied (not verified); some EMS services use question-based neglect adaptations.
3. **LAMS**: Exact item wording ('drifts down', 'falls rapidly', 'weak grip', 'no grip') confirmed in secondary material only; check against Llanes 2004.
4. **NIHSS**: UN (untestable) items contribute 0 and are flagged; NINDS does not define how UN enters the total. Convention to be confirmed by a stroke clinician.
5. **NIHSS**: Only two coma auto-scoring rules (items 8, 9) are encoded, as warnings; NINDS instructions for other items in coma not encoded.
6. **ICH Score**: Score 6: the app states no derivation patient scored 6 (abstract reports scores up to 5); some summaries list 6 as 100%. Confirm against the paper.
7. **ICH Score**: Removed unverified cohort size from content (sources give 152 and 161).
8. **Marshall**: Category is derived from findings using the standard order of precedence; confirm with a neuroradiologist for mixed-lesion edge cases.
9. **RTS**: The '<4' threshold is described in secondary sources as proposed for identifying severe injury; confirm wording.
10. **GPA**: Middle age band printed as 50–59 or 50–60 in different reproductions; implemented as 50–60 (lowest band is >60).
11. **Revised Tokuhashi**: CONFLICT: 'Metastases in the vertebral body' is ≥3/2/1 in one reproduction and ≥3/1–2/0 in two others (WJO 2016, PMC review). Implementation uses ≥3/2/1. A user textbook table (Spine Surgery and Peripheral Nerve Surgery 2025, Table 8.1) also shows ≥3/2/1, but that table mixes the 1990 and 2005 versions, so it is weak evidence. Verify against the original 2005 paper (Spine 30:2186) before clinical use. A notice in the calculator states this.
12. **Tomita**: One review table (Global Spine J 2018) gives 3 points for rapid growth; the original 2–10 range requires 4. Implementation uses 4; noted for review.
13. **SOFA**: Reproductions differ at some boundaries (dopamine ≤5 vs <5; creatinine >5.0 vs ≥5.0; one table gives platelets <25); implementation follows the Sepsis-3 table.
14. **SOFA**: PaO2/FiO2 <200 without respiratory support is not explicitly assigned in the table.
15. **Clonus**: Descriptive record, not a validated scale; clinician to confirm the wording of 'unsustained'.
16. **Gardner-Robertson**: Discordant PTA/SDS: HNO 2021 review states Gardner-Robertson assigns the better class while Silverstein assigns the poorer, and calls the rule contradictory; other sources assign the poorer class. The app reports both classes and assigns none. Confirm against the 1988 paper.
17. **Lawton-Young**: No Supp-SM threshold (e.g. ≤6) is shown: not confirmed from an accessible source in this session.
18. **Markwalder**: Originating paper: cited as Markwalder et al. J Neurosurg 1981;55:390 and Markwalder 1981 review (54:637); confirm which introduced the scale.
19. **MTS**: StrokEngine states X definitions are identical in Tardieu and MTS, including X5 'joint immovable'; some reproductions of the MTS list X0–X4 only. Confirm against Boyd & Graham 1999.
20. **MTS**: R2−R1 is reported as an absolute difference because angle conventions differ between joints.
21. **Reflex grade**: The '+' notation (1+–4+) is display convention; the NINDS paper uses plain numerals. Scales that use 5 for sustained clonus are a different version and are not combined.
22. **RASS (held)**: Licensing: VCU lists RASS as a licensable technology; confirm terms before reinstating.
23. **RASS (held)**: Terminology: 'Drowsy' sustained awakening is '>10 s' in most sources and '≥10 s' in VCU's description.

### Applies to all scores
- **Limitations, confounders and clinical-context text** is editorial (source-supported, not scoring rules) and requires clinician review.
- **Citations:** DOIs are shown only where confirmed during the project; other bibliographic details (volume, pages) need a reference check.
- **Related-score links** (`content_src/related.py`) were reviewed for clinical logic; no illogical links were found, but they remain editorial.

## 4. Scores requiring manual verification

**Calculation-affecting (must be resolved before clinical use):**
- **Revised Tokuhashi**: vertebral-body metastasis item conflict between published tables.

**Interpretation or wording (review before release):**
- **GCS-P**
- **Clonus**
- **FAST-ED**
- **GPA**
- **Gardner-Robertson**
- **ICH Score**
- **LAMS**
- **Lawton-Young**
- **MTS**
- **Markwalder**
- **Marshall**
- **NIHSS**
- **RTS**
- **Reflex grade**
- **SOFA**
- **Tomita**

**Secondary-source verification only (confirm against primary full text):** ASPECTS, FAST-ED, LAMS, pc-ASPECTS, RACE, Graeb, Fisher, Hunt & Hess, ISS, Marshall, Rotterdam, RTS, TRISS, Frankel, mJOA, Nurick, KPS, Revised Tokuhashi, Tomita, Borden, Clonus, Cognard, Engel, Gardner-Robertson, House-Brackmann, Lawton-Young, Markwalder, MAS, MRC power, MRC-SS, MTS, Plantar, Spetzler-Martin.

**Withheld (not shown in the app):** FOUR (Licensing); mGraeb (Verification); AIS (Licensing / version); ODI (Licensing); Tokuhashi (1990) (Verification); RASS (Licensing); JOA (Version); SOFA-2 (Verification); DS-GPA (Version); Sunnybrook (Verification / licensing). Reasons: [CONTENT-AUDIT.md](CONTENT-AUDIT.md).

**Planned (future queue, not implemented):** Helsinki CT, Stockholm CT, IMPACT, CRASH, SCIM III, WISCI II, RPA, Evans Index, FOHR.

## Corrections made during this audit
- ICH Score: removed an unverified cohort size from the version text.
- Hunt & Hess: Grade IV restored to the original wording ('…and vegetative disturbances').
- GCS-P: the 1–8 band now states it is not defined in the original publication.
- Revised Tokuhashi: calculator notice added about the conflicting item (scoring unchanged pending review).
- ECOG: licensing status updated to public domain (ECOG-ACRIN).
- RASS: held back pending licensing review (content and tests retained; reinstatement is a one-line change).
- Audit tooling: the calculation audit now also evaluates extremes for sampled input spaces (initially missed NIHSS maximum in a sample).
