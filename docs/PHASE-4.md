# Phase 4 report: clinical insight engine (v0.5.0)

## Principle implemented
A result is never just a number. Every calculator result shows, in order:
1. **Score**: value, E+V+M formula where applicable, state label, tone in words, scale meter
2. **Breakdown**: components and subtotals
3. **Interpretation**: what the result represents (state detail plus the meaning of the result type)
4. **Clinical context**: what the score helps describe
5. **Important considerations**
6. **Limitations**
7. **Confounders**
8. **What it does not tell you**
9. **Related scores**

## Architecture
- **`js/engine/insights.js`** is a new, pure module that runs in both Node and the WebView. It turns structured content into an `InsightSet`. No free text is generated, and no AI is used.
- **Item model.** Each item is `{ text | factor+effect, importance: major|standard, when?, on?: always|result|notTestable, guideText?, title? }`.
- **Ordering.** Within each section, items triggered by this result come first, then major items, then standard ones.
- **Shared rendering.** The calculator and the Guide render from the same content: `build()` produces the result view, `forGuide()` the Guide view.
- **Result states.** The tones are favorable, low, mild, moderate, high, critical, informational and incomplete, plus not-interpretable. Scores define their own states.
- **Semantic result types.** These are severity, deficit, classification, functional-status, disability, stability, imaging-classification, prognostic-category and informational. Each type permits only appropriate tones; for example, functional-status and disability may use only favorable or informational. The validator enforces this.
- **Signals.** Every state and insight card shows an icon, a type label, a colour and an explanation. Colour is never the only signal.

## UI components
- `InsightCard`: one item, with icon, type label, text, and tags for "Important", "Applies to this result" and "When applicable".
- `InsightSection`: a group of cards. Prioritised cards are shown first; the rest sit behind "Show N more".
- `StateCard`: one result state, for the Guide.
- **Guide cards.** The Guide uses key-warning cards (the notice plus major limitations, without repeating the notice), state cards, clinical context and consideration cards, highlighted major-limitation cards, confounder cards (factor and effect), common-mistake cards and "does not tell you" cards.

## Safety
- **Content lint.** A test fails on treatment directives or diagnostic claims in any score (intubate, administer, recommend surgery, "is normal", and similar).
- **Favourable states** must be time-bound ("at this assessment" / "at the time of assessment") and carry a cautionary detail.
- **High and critical states** must explain themselves using correlate/assess language, never instructions.
- **Specified wording.** NIHSS 0 reads "No measurable deficit on the NIHSS at the time of assessment." Severe GCS reads "Correlate with airway, respiratory, neurological and systemic assessment…".

## Tests: 313 checks, all passing
- **Engine:** 106 tests, including 17 new insight-engine tests. These cover structure, ordering, the not-testable mode, conditional evaluation, the guide view, validator rules, the tone policy, the content lint and the cautious-wording rules. Every possible input combination is checked: all 210 GCS combinations including NT, all 1,296 SINS combinations, all 7 mRS grades, and 3,000 random NIHSS examinations with UN items (more than 300 hit the UN path).
- **Calculator UI:** 109 checks, including 27 new for Phase 4. They cover result order for all four scores, icon plus label on every card, the tone stated in words, the "Show more" disclosure, the specified wording, the absence of treatment directives, contextual tagging, and Guide semantic cards for all four scores.
- **Shell regression:** 98 checks.

## Fixed during this phase
- **Share text** could contain the unfilled label template ("NIHSS 21 — NIHSS {total}"). The exhaustive sweep found it. Fixed, with a regression assertion.
- **Duplicate headings** on Guide insight sections, and the key-warnings group repeating the calculator notice. Both were found in visual review and fixed.

## Known limitations
- **The lint is pattern-based.** It catches common directive phrasing, not every possible wording, so content still needs clinician review.
- **The importance levels** (major/standard) are my editorial judgement from the sources and need clinical review.
- **No device run.** Testing used a browser at device sizes, not a physical device.
