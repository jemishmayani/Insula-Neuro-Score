# Phase 3 report: first four scores (v0.4.0)

## Source verification (done before implementation, not from memory)
| Score | Verified against | Notes |
|---|---|---|
| GCS | Glasgow structured approach (glasgowcomascale.org; Teasdale et al. 2014), reproduced in several trial protocols | Criteria wording, NT definitions, and the rule that no total is given if any component is non-testable |
| NIHSS | NINDS NIH Stroke Scale PDF (updated Feb 2024), fetched directly | All 15 item definitions; UN only on 5a/5b/6a/6b/7/10; item 11 never untestable; coma rules for items 8 and 9; item 9 = 3 only if mute and following no one-step commands; ataxia absent if paralysed |
| mRS | van Swieten 1988 standard wording, consistent across multiple trial protocols | Variant wordings that add "neurological" are not mixed in |
| SINS | Fisher et al. Spine 2010 (SOSG); Fourney et al. JCO 2011; AJR 2014 reliability study | Components, points, categories, the referral threshold of ≥7, and two published worked examples |

## Delivered per score
- **Calculator:** all components, validation, breakdown, a score-specific result type and state, interpretation, insights, limitations, reset, copy/share, and an Open guide button.
- **Guide:** 15 sections, in Phase 3 order, generated from the score data.
- **GCS:** E, V and M recorded individually. "E + V + M =" appears above the total, both in the card and in the phone result bar. A non-testable component is recorded as NT, with an optional listed reason, and is never scored as 1; when any component is NT, no total is reported.
- **NIHSS:** item and component breakdown with subtotals. A persistent notice says it is not a complete neurological examination, with limitations on where it under-represents impairment (posterior circulation, a score of 0, right hemisphere). There are 4 verified NINDS consistency warnings, and no invented severity bands.
- **mRS:** shown as "Functional status" on a 0–6 position scale in a neutral blue tone, not a red/green severity colour. A notice says it is a functional outcome scale, not a severity score.
- **SINS:** shown as a "Stability category" on a 0–6 / 7–12 / 13–18 meter. A notice says it is an assessment tool, not a surgical decision. The ≥7 threshold is described as the authors' referral threshold, not a decision to operate.

## Model additions (generic, data-driven)
- `resultPresentation {type, typeLabel, meter}`: `severity` | `deficit` | `functional-status` | `stability-category` | `classification` | `informational`
- `calculationMethod.formula`: a template shown before the total
- `calculatorNotice {tone, title, message}`
- `min`/`max` on result states, which drive the scale meter

## Tests: all passing
- **Engine:** 89 tests (`node --test tests/engine/*.test.js`). These include 50 manually verified cases, each recording its hand calculation and source, plus exhaustive checks of all GCS and SINS combinations and 5,000 random NIHSS examinations.
- **Calculator UI:** 82 checks (`tests/calculator.test.py`). They cover all four calculators end to end, Guide ↔ Calculate for each score, light and dark mode, a 320px small phone and a tablet.
- **Shell regression:** 98 checks (`tests/shell.test.py`).

## Fixed during this phase
- `.tone-informational` was never defined: an edit in Phase 2 failed silently on a whitespace mismatch. Informational results, including NIHSS, had no colour. Visual review found it. It is fixed, with two regression tests: every engine tone must have a style, and the rendered card must have a colour.

## Known limitations
- **Manual testing scope.** Manual testing used a scripted browser at phone and tablet sizes, with screenshot review. The APK has not been run on a physical device or emulator here.
- **Clinician review.** Content is still pending independent clinician review.
- **NIHSS UN.** UN items contribute 0 and are flagged, because NINDS does not define how UN enters the total. Only the four verified NINDS rules are encoded, and as warnings, not auto-scoring.
- **mRS timepoint.** The timepoint (pre-morbid, discharge, follow-up) is advised in the insights but not captured as a field.
