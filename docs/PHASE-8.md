# Phase 8 report: final UX and performance (v0.9.0)

## Responsiveness and accessibility audit
`tests/audit.py` renders 13 key screens on **5 devices × 3 text sizes × 3 themes = 585 renders**:
- **Devices:** small Android 360×640, large Android 412×915, tablet 800×1280, tablet landscape 1280×800 and phone landscape 915×412.
- **Text sizes:** 100%, 130% and 200%.
- **Themes:** light, dark and dark high-contrast.

On every render it checks for horizontal overflow, clipped text, overlapping controls, touch targets under 44 px, controls without accessible names, and WCAG AA text contrast. **Final result: 0 findings, 0 JS errors.**

### Issues found and fixed
| Issue | Fix |
|---|---|
| **Landscape phone at 200% text:** the calculator's input column collapsed to one character wide (vertical text; options could not be tapped) | The two-pane layout is now space-aware: panes stack whenever both don't fit at the current text size |
| Sticky result bar tied to a width breakpoint | The bar now appears whenever the result panel is out of view, on any layout (IntersectionObserver) |
| Bar's hidden state was wiped by every update | The observer's state is kept and re-applied |
| Screen-entry animation used `transform`, briefly pinning the fixed result bar inside the content (flicker on open) | The animation is opacity only |
| Related-score chips and the warning group overflowed at 200% text | Content now wraps |
| Number-input steppers shrank to 28 px on landscape phones at large text | Steppers keep their full touch size |
| Secondary actions (chips, Clear, jump links) at 44 px or less | Raised to 48 dp |
| Teal UI accent below 3:1 on white; filled buttons below 4.5:1 | Separate accessible tokens for UI accents (3.6:1) and filled buttons (5.1:1) |
| Fixed-layout breakdown table took column widths from a spanning row | Explicit column widths; a short points cell |
| Design-system demo showed a stray sticky result bar | Demo calculator runs without the bar |
| Expanded "Show N more" kept its label | Now reads "Show fewer" when open |

## Calculator UX
- **Auto-calculation:** no submit step. Selection state is clearly shown, the result value is large, and the sticky result bar appears whenever the result is off-screen.
- **Fewer taps:** after a choice, the next unanswered question scrolls into view. Focus is never moved, and smooth scrolling is off under reduced motion.
- **Easy reset with Undo:** one stray tap can no longer wipe a full NIHSS.
- **Easy Guide access:** a "Guide" button in the result actions, plus the Calculate | Guide toggle.
- **Keyboard:** number fields show "Next" on the keyboard. Enter moves to the next field, and closes the keyboard on the last one.
- **No loading flash:** the loading indicator appears only if loading takes longer than about 220 ms.

## Navigation
Tested in `tests/journey.test.py`:
- Home → Calculate and Home → Guide.
- Calculate → Guide and Guide → Calculate, at the top and bottom of every Guide.
- Related score → score.
- Back returns to the correct previous location. The Calculate/Guide toggles never add history, and Back from the startup root exits.

## Animation
Only subtle screen fades (opacity, 140 ms) and small state transitions. Everything is disabled under `prefers-reduced-motion`, which is tested.

## Error handling
All of these are tested, and none crashes the app:
- **Missing score file (404):** error state with a way out; the rest of the app keeps working.
- **Corrupt JSON, or content failing validation:** the same.
- **Corrupted preferences:** reset to defaults.
- **Engine robustness:** fuzzed with more than 43,000 malformed answer sets across 29 scores (never throws).
- **Unsupported input types and null results:** reported as invalid.
- **Script parsing:** every shipped script and JSON file must parse, checked by the engine suite after one broken edit was caught during this phase.

## Performance
4× CPU throttling (mid-range Android approximation), median of 3 runs; see [PERFORMANCE.md](PERFORMANCE.md):

| Measure | Median | Worst | Budget |
|---|---|---|---|
| Cold start (Home ready) | 575 ms | 642 ms | 2,500 ms |
| Tab navigation | 30 ms | 32 ms | 200 ms |
| Search keystroke | 11 ms | 12 ms | 60 ms |
| Calculation update | 40 ms | 45 ms | 50 ms |
| Guide open (first) | 105 ms | 140 ms | 900 ms |
| Guide open (repeat) | 90 ms | 91 ms | 350 ms |
| Home render | 21 ms | 24 ms | 200 ms |

Calculation update has the smallest margin: about 5 ms of headroom in the worst case under 4× throttling, on NIHSS, where every answer changes the result. If future scores make the result panel heavier, this should be re-measured.

**Reducing recomputation:**
- The result panel is rebuilt only when the result changes.
- Generated Guides are cached per score, since content is immutable within a session.

## Dark mode: manual inspection
Every main screen was captured in dark mode at 412×915 and inspected by eye: Home, Calculate, GCS (high concern), SINS (stability), mRS (functional status), NIHSS Guide (limitation cards), Settings, and an under-review score. Text, result colours, warning and limitation cards, tables, icons, dividers, toggles and disabled controls all remained readable. The automated audit also checks WCAG AA text contrast in dark and dark high-contrast themes on all 13 audited screens.

## Final user journey
Run on a **phone (412×915)** and a **tablet (1280×800)**, all steps passing:

Launch → Home → search "GCS" → calculate → enter E2 V3 M4 → result **9** (Moderate) → insight → expand limitations → Guide (from the result) → related score (GCS-P) → Back → favorite GCS-P (calculator) → Home shows the favorite and the recent calculation → dark theme + startup "Guide" → **restart** (new browser context; only device storage carried over) → opens on Guide, dark theme, favorite kept, calculator inputs not persisted.

## Tests: all passing
- Engine 226 (includes robustness fuzzing and asset parsing).
- Calculator 109.
- Journey 59.
- Perf 7.
- Guide 30.
- Library 73.
- Home 69.
- Shell 99.
- Audit: 585 renders, 0 findings.

## Process note
Phase 8 was completed across sessions. Work was checkpointed in WIP commits, and the working tree was inspected before each change, so no earlier work was overwritten.

## Known limitations
- **Not tested on real devices.** Testing used Chromium at device sizes, with text scaling emulated by root font size, CPU throttling, and reduced-motion emulation. A pass on real Android hardware (WebView text zoom, the system back gesture, the on-screen keyboard and TalkBack) is still recommended before release.
- **Shared red.** "Error" and "high concern" use the same red family. They are distinguished by icon and label.
- **Clinical review.** All clinical content remains pending independent clinician review.
