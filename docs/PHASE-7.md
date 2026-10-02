# Phase 7 report: Guide experience (v0.8.0)

## Structure: every Guide, 14 sections
Overview · Purpose · Intended population · When to use · Calculation · Interpretation · Clinical context · **Limitations** · Confounders · Common mistakes · What it does not tell you · Related scores · Version · Sources.
Sections have stable anchors (`#g-overview` … `#g-sources`). Every Guide is generated from score data by `Calculator.guideHTML`, and scores still under review use the same 14-section shell.

## Limitations are prominent
- **At the top:** the Overview opens with **Key warnings and limitations** (the calculator notice plus every major limitation) and a **See all N limitations →** link.
- **Early in the order:** the full Limitations section is 8th of 14, directly after clinical context, not near the end.
- **Visually distinct:** limitations appear as limitation cards, with major items highlighted and tagged "Important". Their contents-list chip is warning-coloured.

## Visual hierarchy
- **Overview:** a highlight box, an "At a glance" fact table (result type, range, components, version, category, review status) and the key-warnings cards.
- **Calculation:** numbered steps, a "Method" information box, and component tables with headers. Plain numeric inputs share one compact table, and point bands are shown as ranges.
- **Interpretation:** a result-type card and one state card per result state.
- **Insight sections:** context, consideration, limitation, confounder (factor and effect) and "does not tell you" cards, plus warning cards for common mistakes.
- **Paragraphs:** none is longer than 420 characters in any Guide; this is enforced by a test.

## Navigation
- **Top:** a **Calculate** button and a **Related scores →** jump link.
- **Bottom:** **Calculate this score**.
- **Both** replace the history entry, so Back never alternates between Guide and Calculator. Both are tested on all 41 guides, including the 12 under review.

## Related scores
- **Directly related:** a curated list per score in `content_src/related.py` (`RELATED`), with the reason for each link (e.g. "Outcome after brain injury"). It is kept in one file so the relationships can be clinically reviewed together.
- **Clinical clusters** (`content/related.json`, 13 clusters): Level of consciousness, SAH grading, Spinal metastases, Acute stroke assessment, Prehospital LVO screens, TIA, ICH, TBI, Trauma severity, Functional outcome, Spinal cord injury, Cervical myelopathy, Neurocritical care. A cluster doesn't repeat scores already listed directly.
- **Links:** each related row opens that score's Guide, and also offers a **Calculate** shortcut when a calculator exists. Under-review scores show their badge and open to their review reason.
- **Specified examples, all verified by test:**
  - GCS → GCS-P, FOUR, GOSE
  - SAH → Hunt & Hess, WFNS, Fisher, Modified Fisher
  - Spinal metastases → SINS, Revised Tokuhashi, Tomita, KPS
  - Stroke → NIHSS, ASPECTS, mRS

## Guide search
- **Fields:** name, abbreviation, category, specialty and keywords. Keywords come from aliases, category keywords, subcategory and cluster titles, and are generated into the catalogue at build time.
- **Match reasons:** results beyond the score's own names show why they matched, e.g. "matched keyword" or "matched specialty".
- **Examples:** "SAH" returns exactly Hunt & Hess, WFNS, Fisher and Modified Fisher. "hemorrhage" and "haemorrhage" both find the ICH scores, and "LVO" finds RACE, LAMS and FAST-ED.

## Tests: all passing
- **`tests/guide.test.py`: 30 checks.**
  - Section order, limitations placement, paragraph length and hierarchy elements across all 29 guides.
  - Top and bottom navigation on all 41 guides.
  - **All 258 related links in all 41 guides clicked**: each opens the correct score, and Back returns to the originating Guide.
  - The specified related examples, ten search scenarios, and small-phone (light) and tablet (dark) layouts.
- **Regression:** engine 221, calculator 109, shell 99, library 73, Home 69.

## Build note
This phase's work was completed across two sessions. The uncommitted `content_src/related.py` was accidentally overwritten at the start of the second session. The 13 clinical clusters were restored verbatim from the earlier build output (`content/related.json`), and the restoration was confirmed by regenerated search keywords matching the earlier catalogue exactly (e.g. Hunt & Hess). The curated per-score `RELATED` map was added in the second session.

## Known limitations
- Splitting prose into steps and points is sentence-based. Content authors should keep "How to perform" as one instruction per sentence.
- Cluster membership is editorial and needs clinical review.
- Tested in Chromium at device sizes, not on a physical device.
