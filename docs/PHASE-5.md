# Phase 5 report: personalized Home (v0.6.0)

## Home
- **Order:** Search, then Favorite scores, Favorite guides, Recently used calculators, Recently viewed guides, Priority scores, Priority groups. Users can reorder or hide sections (Settings → Home layout), so priority scores can be placed above everything else.
- **Rows:** each Home row opens one view, and a labelled second button opens the other ("Guide" or "Calculate"), so both are one tap away.
- **Empty states:** every section has a title, guidance and an action where useful, for example "No favorite scores yet. Add a score to Favorites for one-tap access." with a **Browse calculators** button.

## Favorites
- **Separate lists.** The star on a calculator adds to **Favorite scores**; the star on a guide adds to **Favorite guides**. Stars in Calculate and Guide lists follow the list's context.
- **Managing.** Favorites can be edited inline on Home (reorder or remove) or in Settings, which also has pickers.

## Recents (local only)
- **When recorded.** Calculators are recorded only when a calculation is **completed**, including GCS with a component non-testable. Opening or partially filling a calculator does not count. Guides are recorded when opened.
- **What is kept.** The score id and the time only, never inputs. The list is newest first, without duplicates, and capped at 10. Rows show relative time ("Calculated 2 min ago").
- **Clearing.** Each Home section has **Clear**; Settings → History shows counts and offers per-list and **Clear all history**. Every clear can be undone.

## Priority system
- **Promoting.** Promote a score from its screen ("Add to Home priority") or a category from its screen ("Add group to Home"), or use the pickers in Settings.
- **Arranging.** Reorder scores and categories inline on Home (Edit, then ↑ ↓ ✕, then Done) or in Settings. Removing an item from Home can be undone.
- **Hiding.** Hide a category from its screen or in Settings. Hidden categories are left out of the Calculate and Guide lists and of Home, but their scores remain searchable.

## Startup screen
Home, Calculate or Guide. The choice is remembered across restarts.

## Storage: schema v3
`ins.store.v3` holds favorites, favoriteGuides, recentCalc and recentGuide (`{id, at}`), priorityScores, priorityGroups, hiddenGroups, groupOrder, homeSections, theme, highContrast and startup. Earlier versions migrate automatically:
- **v2 → v3.** Recents gain timestamps (shown without a time when unknown). A default layout moves to the Phase 5 order; a customised layout is kept, with Favorite guides inserted after Favorite scores.
- **v0.1 → v3.** Pinned scores become priority scores, and old favorite guides become favorite guides.

## Performance
- **Catalogue only.** Home and search use only the lightweight catalogue, with an index and search keys built once at load.
- **On-demand documents.** Score and guide documents load only when opened, into a cache of at most 12. Search renders at most 50 rows.
- **Measured** with a synthetic **2,034-score** library:

| Measure | Result | Limit |
|---|---|---|
| Home ready | 214 ms | < 1,500 ms |
| Home re-render (120 favorites, 10 recents) | 20 ms | < 150 ms |
| Search, worst keystroke | 8.5 ms | ≤ 50 ms |
| Score documents fetched at startup | 0 | 0 |
| Document cache after opening 20 calculators | 12 | ≤ 12 |

## Tests: all passing
- `tests/home.test.py`, **69 checks**: Home order and empty states, separate favorites with both views reachable, recents semantics, cap and privacy, Clear and Undo, priority scores placed above everything with inline reorder, focus and remove, priority groups promote, reorder and hide, startup screen, persistence across restarts, two v2 migration paths, large-library performance, and small-phone and tablet layouts.
- **Updated suites:** shell regression (99), calculator UI (109) and engine (106).

## Known limitations
- Reordering uses ↑/↓ buttons (accessible, keyboard-friendly), not drag-and-drop.
- Recents migrated from v2 have no timestamp, so they show without a time.
- Testing ran in Chromium at device sizes, not on a physical device.
