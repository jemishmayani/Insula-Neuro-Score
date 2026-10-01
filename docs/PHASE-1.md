# Phase 1 report: app shell and design system (v0.2.0)

## Built
- **Screens.** Home, Calculate, Guide and Settings, with Settings reached from the app bar.
- **Home.**
  - Search across names, abbreviations, topics and categories.
  - Priority scores, priority groups, favourites, recent calculators and recent guides.
  - Every section has an empty state and can be reordered or hidden.
- **Calculate and Guide.**
  - Search, a category grid, and score lists.
  - A shared score-detail shell with a Calculate | Guide toggle.
  - The calculator shell has input placeholders, a ResultCard, Reset and Open guide.
  - The guide shell has a 15-section table of contents, section cards, and "Calculate this score →".
- **Settings.**
  - Theme (System/Light/Dark) and high contrast.
  - Startup screen (Home/Calculate/Guide).
  - Home layout order and visibility.
  - Favourites and priority scores and groups: reorder, remove, add via pickers.
  - Score-group order and visibility.
  - Clear recents, reset, and a design-system gallery.
- **Design system.** 16 required components plus helpers, and a token system with semantic colours for light, dark and high contrast.
- **Responsive layout.** Small and large phones, landscape (navigation rail), and tablets (rail, wide grids, two-pane detail).
- **Persistence.** Versioned, sanitised, pruned when the catalogue changes, and migrated from v0.1.0.
- **Placeholder data.** 34 real score names in 9 categories, each clearly badged "Placeholder". No scoring criteria.

## Tests (`tests/shell.test.py`): 95 passed, 0 failed
- **Static.**
  - No colour literals outside tokens.
  - A single local fetch and no other network APIs.
  - All 16 components present.
  - Catalogue is placeholder-only.
- **Navigation.**
  - Tabs, category → detail, and the Calculate↔Guide toggle.
  - The Back chain: detail → category → tab root → startup tab → exit.
  - Deep-link back, app-bar back, and the unknown-route error state.
- **State.**
  - Favourites: toggle, persistence across reload, and shown on Home.
  - Recents and priority toggles.
  - Reordering of priority scores, Home sections and groups, with persistence and focus following the moved item.
  - Hidden groups and pickers.
- **Themes.**
  - Light, dark, System (including reacting to a live device change), high contrast, and persistence.
- **Startup.**
  - Startup preference applied on launch, and Back behaviour from it.
- **Robustness.**
  - v0.1.0 migration and corrupt-storage fallback.
  - Catalogue failure shows an ErrorState that recovers on Retry; a LoadingState shows during slow loads.
- **Responsive.** At 320×568, 430×932, 844×390 landscape, 820×1180 and 1366×1024:
  - no horizontal overflow on 8 screens;
  - correct bottom navigation or rail;
  - touch targets ≥ 40px;
  - accessible names on all controls;
  - no JS errors.
- **Rotation.** Route and state survive; the layout switches to the rail and back.

## Known issues
- Tested in Chromium at device viewports. The APK is built and signature-verified, but it has not been run on a physical device or emulator in this environment. Hardware Back, system-bar colours and the system font scale need on-device confirmation.
- Error and high concern share the red family. They are distinguished by icon (✕ circle vs octagon) and label.
- Reordering uses up/down buttons, which are accessible. Drag-and-drop is not implemented.

## Recommended next phase
Phase 2: restore the score engine from `engine-preview` behind the shell components, then implement the first verified score set.
