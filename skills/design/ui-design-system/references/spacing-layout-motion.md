# Spacing, layout, elevation & motion — reference

## 1. The spacing scale

```
4  →  xs   tight pairs (icon ↔ its label)
8  →  s    related items inside a component
12 →  sm   compact list rows
16 →  m    default screen padding, card padding, between fields
24 →  l    between groups / sections
32 →  xl   between major blocks
48 →  xxl  screen-level separation, empty-state breathing room
64 →  xxxl hero sections
```

**Proximity rule (memorise this):** the gap *inside* a group must be smaller than the gap *around*
the group. If a label is 8dp from its input, the next field must be ≥ 16dp away.

Never: 5, 7, 10, 13, 15, 18dp. If your design needs 18, your scale is wrong or the asset has built-in padding.

## 2. Layout grid
- **Mobile**: 4dp baseline grid, 16dp side margins (24dp on large phones), single column.
- **Tablet/desktop**: 12-column grid, 24dp gutters, max content width 840–1200dp for text.
- **Vertical rhythm**: components snap to 4dp; text baselines to 4dp where the platform supports it.
- **Alignment**: one left edge (or right in RTL) per column. Icon columns align on the icon centre.
- **Touch targets**: 48×48dp minimum, 8dp minimum gap between adjacent targets.
- **Thumb zones** (phone): bottom third = easy, top corners = hard. Primary actions bottom, destructive far from the thumb path.

## 3. Shape & elevation

| Token | Radius | Use |
|---|---|---|
| `shape.none` | 0 | full-bleed media |
| `shape.xs` | 4 | chips, small tags |
| `shape.s` | 8 | buttons, text fields |
| `shape.m` | 12 | cards |
| `shape.l` | 16–20 | sheets, dialogs |
| `shape.full` | 50% | avatars, FAB, pills |

Elevation levels (M3): 0 (surface), 1 (card), 2 (raised), 3 (dialog/menu), 4–5 (rare).
- In **light** theme: soft shadow, low opacity, large blur, minimal Y offset.
- In **dark** theme: elevation = **lighter surface tint**, shadows are nearly invisible.
- Never use elevation decoratively. Elevation means "this floats above and is temporary/interactive".

## 4. Motion

### Duration tokens
| Token | Duration | Use |
|---|---|---|
| `motion.instant` | 0–50ms | press feedback state change |
| `motion.short` | 100–200ms | small element fade, icon morph, ripple |
| `motion.medium` | 250–400ms | container expand, sheet, dialog |
| `motion.long` | 450–600ms | full-screen transition, complex choreography |

Anything above 600ms on a frequently repeated interaction feels broken. Exits are ~30% faster than entrances.

### Easing
| Curve | Use |
|---|---|
| `standard` (0.2, 0, 0, 1) | most on-screen movement |
| `emphasized` (M3 spatial spring) | hero transitions, expressive movement |
| `decelerate` (0, 0, 0, 1) | elements entering the screen |
| `accelerate` (0.3, 0, 1, 1) | elements leaving the screen |
| `linear` | progress indicators and continuous rotation **only** |

Springs (Compose default) beat curves for gesture-driven and spatial motion; use
`spring(dampingRatio = DampingRatioMediumBouncy, stiffness = StiffnessMediumLow)` for playful,
`Spring.DampingRatioNoBouncy` for utility.

### Motion principles
- Motion must **explain** something: origin, hierarchy, or state change. Decoration is noise.
- Shared-element / container-transform for "this became that".
- Fade-through for unrelated content swaps; fade-through = 90ms out, 210ms in.
- Never animate more than 2–3 properties simultaneously.
- Honour reduced motion: replace movement with a cross-fade, keep durations, never remove feedback entirely.

```kotlin
val reduceMotion = LocalAccessibilityManager.current?.let { /* platform check */ } ?: false
val spec = if (reduceMotion) snap() else tween(300, easing = EmphasizedEasing)
```

## 5. Component state matrix (every interactive component needs all of these)

| State | Visual treatment |
|---|---|
| Enabled | base tokens |
| Hover (pointer) | +8% state layer of `onSurface`/`primary` |
| Focused (keyboard) | visible focus ring, ≥ 3:1 contrast, 2–3dp thick |
| Pressed | +12% state layer, optional scale 0.98 |
| Dragged | +16% state layer + elevation |
| Selected | container tint + `onPrimaryContainer` text |
| Disabled | 38% opacity content, 12% container; no state layers |
| Error | error color border + helper text + icon |
| Loading | in-place indicator; keep the component's size stable |

Missing states are the #1 sign of an amateur component library.

## 6. Density & responsive behaviour
- Define exactly two densities if you need them: `comfortable` (default mobile) and `compact` (tablet/desktop tables).
- Breakpoints follow window size classes: 600dp, 840dp (see `android-compose-ui/references/adaptive-layouts.md`).
- Content reflows; it does not just scale. A phone card at 400dp wide is not a tablet card at 800dp — it becomes two columns.

## 7. Empty, loading, error states (part of the design system, not an afterthought)

| State | Must contain |
|---|---|
| Empty (first use) | illustration/icon, one-line explanation, primary action to create the first item |
| Empty (no results) | what was searched, a suggestion, a clear-filters action |
| Loading | skeleton matching the final layout (not a centred spinner) for > 300ms waits |
| Error | plain-language cause, retry action, support path for repeat failures |
| Offline | cached content + a persistent, non-blocking banner |
| Partial failure | show what loaded, mark what failed, allow retry of the failed part only |

Design these **at the same time** as the happy path, in the same component file.
