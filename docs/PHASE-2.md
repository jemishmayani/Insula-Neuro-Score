# Phase 2 report: score engine (v0.3.0)

## Architecture
The layers are score data → engine → result model → UI, as specified, with automated checks that the UI holds no scoring logic. The engine is three pure modules that run unchanged in Node (tests) and the WebView (app). See `SCORE-MODEL.md`.

## Scores implemented and what each proves
| Score | Engine paths exercised |
|---|---|
| GCS | Sum; `block` not-testable policy → not-interpretable state; severity bands |
| NIHSS | 15 items in 11 grouped components with subtotals; `exclude` policy for UN with reason lists from NINDS; consistency rules (coma: item 8 = 2, item 9 = 3); informational result with no invented severity bands |
| mRS | `select` method; functional-status states rather than severity |
| SINS | Sum of six heterogeneous components; stability categories; source-attributed referral context without a treatment instruction |
| Demo (non-clinical) | Every input type: single, dropdown, yes/no, multi (exclusive option, cap), integer, decimal, number (optional), measurement (°C/°F), not-testable |

## Tests: 222 automated checks, all passing
- **Engine unit tests (`node --test tests/engine/*.test.js`): 80 tests.**
  - The expression language, including safety against globals, the prototype chain and unknown functions.
  - Every input type: valid input, invalid input, boundaries, precision and unit conversion.
  - The validator, with 11 malformed-model cases.
  - Pipeline behaviour: precedence of invalid over missing, both not-testable policies, out-of-range guard, determinism, no mutation of inputs.
  - 46 fixture cases across the four scores: minimum, maximum, intermediate, every threshold boundary, invalid, missing and not-testable.
  - Exhaustive checks: all 120 complete GCS combinations, all 1,296 SINS combinations, and 5,000 random NIHSS examinations.
- **Calculator UI (`tests/calculator.test.py`): 44 checks.**
  - All four scores end to end through the real UI, including GCS not-testable, NIHSS UN with reason, coma warnings, and the SINS 6/7 and 12/13 boundaries.
  - Every input control, and copy text built from the result model.
  - Answers are kept in memory only (never persisted), and the guide is rendered from data.
  - Dark mode and tablet layout.
- **Shell regression (`tests/shell.test.py`): 98 checks.**
  - All Phase 1 checks still pass.
  - New checks: UI holds no score ids or rule evaluation; catalogue and content files agree; responsive sweep extended to the calculators and guides.

## Known limitations
- **NIHSS UN items.** These contribute 0 and are flagged. NINDS does not define how UN affects the total, so the app reports it transparently instead of choosing a convention silently.
- **NIHSS coma rules.** Only the verified rules (items 8 and 9) are implemented, and only as warnings. Other coma conventions were not encoded because I could not verify them from the NINDS source in this phase.
- **Unvalidated input types.** Multi, measurement and decimal inputs are tested only through the non-clinical demo; no verified score uses them yet.
- **Expressions.** Expressions are untyped; the validator checks syntax and identifiers but not type mismatches.
- **No device run.** Content has not had independent clinician review. The APK has not been run on a device in this environment.
- **Content updates** still require a rebuild. The override folder exists, but there is no delivery mechanism yet.
