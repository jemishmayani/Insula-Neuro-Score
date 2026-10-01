# Architecture

## Layers

1. **Native shell** (`MainActivity.java`). A WebView that serves the bundled UI from a private origin, `https://app.insula.local/`, via `shouldInterceptRequest`. Every other network request is blocked, so the app is offline by construction. A small JavaScript bridge provides copy, share, opening external links (source DOIs) and system-bar theming. Text zoom follows the system font scale.
2. **Content override.** A file at `<filesDir>/content-override/<path>` takes precedence over `assets/content/<path>`. This allows a future signed content-update mechanism to replace individual score files without an app release.
3. **Score engine** (`engine.js`). Generic and UI-agnostic.
4. **UI** (`app.js`). Hash router with Home, Calculate (list and calculator), Guide (list and guide) and Settings screens. Calculators and guides render entirely from score data.

## Score schema (`content/scores/<id>.json`)

| Field | Purpose |
|---|---|
| `id`, `name`, `abbreviation`, `aliases[]` | Identity and search |
| `category`, `specialty[]` | Grouping |
| `version {label, detail}` | Exact published version implemented |
| `contentVersion`, `lastReviewed`, `reviewStatus` | Content versioning |
| `purpose`, `intendedPopulation` | Guide sections 2–3 |
| `inputs[]` | `choice` (options with `points`, optional `code`, `detail`, `nt`) or `number` (`min`, `max`, `integer`, optional `link` to another score) |
| `values[] {id, expr}` | Derived values, evaluated in order |
| `primary`, `range`, `display`, `share` | Result value and templates (`{expr}` placeholders) |
| `notTestable` | Behaviour when any `nt` option is selected (e.g. GCS: no total) |
| `states[] {when, state, label, range, summary, detail}` | First match wins. `state` ∈ normal, low, mild, moderate, high, critical, info, incomplete |
| `insights[] {when?, whenNotTestable?, text}` | Conditional clinical insight |
| `limitations[]`, `confounders[]`, `commonErrors[]`, `doesNotTellYou[]` | Guide sections 9–12 |
| `related[]` | Score ids |
| `sources[] {citation, doi?, url?}`, `licensing {status, note}` | Evidence and reproduction status |
| `guide {what, whenUseful, howToCalculate, clinicalContext}` | Guide prose |

### Expression language
Numbers, `'strings'`, identifiers (input ids, earlier value ids), `+ - * / %`, comparisons, `== !=`, `&& || !`, `?:`, parentheses and whitelisted functions: `min max abs round floor ceil clamp between roman signed isnull`. Parsed by a recursive-descent parser. There is no `eval` and no access to globals. Arithmetic involving a missing value yields null.

### Result states
Each state renders with a distinct colour, a distinct icon shape and a text label, so meaning never depends on colour alone. Classifications, prognostic models and sedation scales can use `info` or other non-severity states where severity framing would be misleading.

### Validation
`ScoreEngine.validate()` runs when each score is loaded and in tests. It checks required fields, input definitions, expression syntax and state names.
