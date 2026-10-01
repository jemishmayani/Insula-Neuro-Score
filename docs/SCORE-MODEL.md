# Score model, engine and result model (Phase 2)

```
content/scores/<id>.json  ──►  js/engine (expr · inputs · engine)  ──►  ResultModel  ──►  js/calculator.js (UI)
        score data                 pure functions, no DOM                plain object        renders only
```

The UI layer (`app.js`, `ui.js`, `calculator.js`) contains no scoring rules. Automated tests fail if it references a specific score id, or evaluates expressions, scoring rules or interpretation rules.

## Score model

| Field | Type | Notes |
|---|---|---|
| `id`, `name`, `abbreviation`, `aliases[]` | string | `id` is lower-case |
| `category`, `subcategory`, `specialties[]` | string | `category` must match the catalogue |
| `version {label, detail}` | object | Exact published version implemented |
| `contentVersion`, `lastReviewed` (YYYY-MM-DD), `reviewStatus` | string | Content versioning |
| `purpose`, `intendedPopulation` | string | |
| `components[] {id, label, inputs[], showSubtotal?}` | | Groups inputs for the breakdown and subtotals. Every input belongs to exactly one component. |
| `inputDefinitions[]` | | See input types below |
| `scoringRules[] {id, expr}` | | Derived variables, evaluated in order |
| `calculationMethod` | | `type`: `sum` \| `select` (+`input`) \| `expression` (+`expression`). Also: `range {min,max}`, `display` and `share` templates, and `notTestablePolicy`: `block` (no total) or `exclude` (0 points + warning). |
| `notTestable {label, summary, detail, display, share}` | | Presentation used with the `block` policy |
| `consistencyRules[] {when, severity, message, inputs[]}` | | Instrument rules linking items. `warning` is reported; `error` blocks the result. |
| `interpretationRules[] {when?, state}` | | First match wins. A rule without `when` is the fallback. |
| `resultStates[] {id, tone, label, range, summary, detail}` | | `tone` ∈ normal, low, mild, moderate, high, critical, informational, incomplete, not-interpretable. Text fields are templates. |
| `clinicalInsights[] {when?, on?, text}` | | `on`: `always` \| `result` \| `notTestable` |
| `limitations[]` | string or `{when, text}` | Conditional limitations are shown first |
| `confounders[]`, `commonErrors[]`, `whatItDoesNotTellYou[]` | string | |
| `relatedScores[] {id, relation}` | | |
| `guideSections {what, whenUseful, howToCalculate, clinicalContext}` | | Prose. The other guide sections are generated from the model. |
| `sources[] {citation, doi?, url?}`, `licensing {status, note}` | | At least one source is required |

### Input types (`inputDefinitions[].type`)
| Type | Answer format | Notes |
|---|---|---|
| `single` | option value | Radio list; options `{value, label, points, code?, detail?}` |
| `dropdown` | option value | Same data as `single`, rendered as a select |
| `yesno` | `"yes"` / `"no"` / boolean | `points {yes, no}`, `labels` |
| `multi` | array of values | `exclusive` options, `minSelected`, `maxSelected`, `maxPoints`, `pointsMode: "count"` |
| `number` / `integer` / `decimal` | number or string | `min`, `max`, `unit`, `decimals`. Optional `pointBands[] {min?, max?, points}`. Comma decimals accepted; exponents rejected. |
| `measurement` | `{value, unit}` | `units[] {id, label, factor, offset}`; `min`/`max` apply to the canonical (first) unit |
| any + `notTestable {label, code, requireReason?, reasons[]?}` | `{nt: true, reason?}` | When `reasons` is given, only those reasons are accepted |

All inputs are required unless `required: false`.

### Expression variables
For each input `x`, expressions can use:
- `x`: the points
- `x_value`: the normalised value
- `x_code`: the display code
- `x_nt`: whether the input was marked not testable

Also available:
- each component id, holding that component's subtotal
- each scoring-rule id
- `total`, `nt_count`, `missing_count` and `answered_count`

Functions: `min max abs round floor ceil clamp between isnull coalesce roman signed fixed`.

## Engine pipeline (`calculate(score, answers)`)
1. Validate and normalise every input (invalid → `status: invalid`; missing → `incomplete`).
2. Compute component scores.
3. Compute the total using the method. A value outside `range` is a calculation error, never a result.
4. Build the breakdown.
5. Apply consistency rules, then interpretation rules, to choose the result state.
6. Fill the interpretation templates.
7. Select contextual insights.
8. Select limitations, contextual ones first.
9. Attach related scores.

`validateScore(model)` checks:
- required fields
- input definitions
- that components partition the inputs exactly
- every expression parses and references only known identifiers
- state references and tones
- ranges and sources

The app validates each score again at load time and refuses to run an invalid one.

## Result model
```js
{ scoreId, version, status: "complete" | "incomplete" | "invalid" | "not-interpretable",
  total, display, range: {min, max}, values: {...derived},
  state: { id, tone, label, range, summary, detail }, interpretation: { summary, detail },
  breakdown: [{ componentId, label, subtotal, items: [{ inputId, label, short, status, display, code, points, reason, error }] }],
  errors: [{ inputId, message }], warnings: [{ message, inputs }], missing: [inputId], notTestable: [inputId],
  insights: [text], limitations: [{ text, contextual }], related: [{ id, relation }], shareText }
```

## Adding a score
1. Verify the criteria, version and licensing against primary sources.
2. Add it to `content_src/build_scores.py` (or write the JSON directly).
3. Add `tests/engine/fixtures/<id>.fixture.json` covering minimum, maximum, intermediate, every threshold boundary, invalid input, missing input and not-testable input. A test fails if any implemented score has no fixture.
4. Run `node --test tests/engine/*.test.js`. No UI changes are required.
