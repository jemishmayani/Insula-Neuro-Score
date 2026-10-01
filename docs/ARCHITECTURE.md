# Architecture (Phase 1 shell)

## Native shell
`MainActivity` hosts a WebView that serves `assets/` from a private origin, `https://app.insula.local/`. Every other request is blocked, so the app cannot make network calls.

Other native behaviour:
- **Rotation.** Orientation changes are handled without recreating the activity, so route and state survive rotation.
- **Text size.** Follows the system font scale.
- **System bars.** Status and navigation bars match the app theme.
- **Content override.** A file at `<filesDir>/content-override/<path>` replaces bundled `content/<path>`. This is reserved for future content updates.

## Design system
| Layer | File | Rule |
|---|---|---|
| Tokens | `css/tokens.css` | The only file with colour values. Defines semantic colours (success, warning, moderate, high concern, critical, error, info, neutral, primary), each with a container colour, for light, dark and high-contrast themes, plus type, spacing, radius, sizing and motion scales. |
| Styles | `css/components.css` | Tokens only. A test fails if a colour literal appears outside `tokens.css`. |
| Components | `js/ui.js` | AppBar, IconButton, BottomNavigation (becomes a rail on tablets and landscape phones), SearchBar, StatusBadge, ScoreCard, CardList, CategoryCard, ResultCard, SectionCard, PrimaryButton, SecondaryButton, Toggle, Segmented, EmptyState, InfoBanner, WarningBanner, ErrorState, LoadingState, Section. |

Status is always conveyed by **colour + icon shape + text label**. The Settings → Design system screen renders every component and tone for review.

## Navigation model
- **Tabs.** Home, Calculate and Guide in the bottom navigation (a rail at ≥840px, or on landscape phones). Settings is in the top-right of the app bar.
- **Routes.**
  - Tab roots: `#/home`, `#/calculate`, `#/guide`
  - Category lists: `#/<tab>/c/<category>`
  - Score detail: `#/<tab>/s/<score>`
  - Settings: `#/settings`, plus `#/settings/pick/<list>` and `#/settings/gallery`
- **Calculate/Guide toggle.** Replaces the history entry, so Back never alternates between the two views.
- **Back** (`window.handleBack`, called by the Android back button), in order:
  1. Pop in-app history.
  2. Otherwise go to the logical parent (detail → category → tab root).
  3. From a tab root, go to the startup tab.
  4. From the startup tab root, exit the app.
- Switching tabs resets the in-tab stack. Scroll position is restored when going back.

## Persistence (`js/store.js`)
One versioned record, `ins.store.v2`, in localStorage. It holds:
- theme and high contrast
- startup screen
- favourites
- priority scores and priority groups
- recent calculators and recent guides (10 each)
- hidden groups and group order
- Home section order and visibility

Safeguards:
- Every write is sanitised.
- Corrupt data falls back to defaults.
- Unknown ids are pruned when the catalogue changes.
- v0.1.0 preferences (`ins.prefs`) are migrated once.

No patient data is stored.
