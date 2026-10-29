---
name: Primer
colors:
  surface: '#111319'
  surface-dim: '#111319'
  surface-bright: '#36393f'
  surface-container-lowest: '#0b0e13'
  surface-container-low: '#191c21'
  surface-container: '#1d2025'
  surface-container-high: '#272a30'
  surface-container-highest: '#32353a'
  on-surface: '#e1e2e9'
  on-surface-variant: '#d6c4b0'
  inverse-surface: '#e1e2e9'
  inverse-on-surface: '#2e3036'
  outline: '#9e8e7c'
  outline-variant: '#514536'
  surface-tint: '#ffb956'
  primary: '#ffc16c'
  on-primary: '#462b00'
  primary-container: '#e8a33d'
  on-primary-container: '#5f3c00'
  inverse-primary: '#835400'
  secondary: '#bbc7da'
  on-secondary: '#263140'
  secondary-container: '#3e4a59'
  on-secondary-container: '#adb9cc'
  tertiary: '#99d3ff'
  on-tertiary: '#00344e'
  tertiary-container: '#63b9f3'
  on-tertiary-container: '#00486a'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffddb5'
  primary-fixed-dim: '#ffb956'
  on-primary-fixed: '#2a1800'
  on-primary-fixed-variant: '#643f00'
  secondary-fixed: '#d7e3f7'
  secondary-fixed-dim: '#bbc7da'
  on-secondary-fixed: '#101c2a'
  on-secondary-fixed-variant: '#3c4857'
  tertiary-fixed: '#c9e6ff'
  tertiary-fixed-dim: '#8bceff'
  on-tertiary-fixed: '#001e2f'
  on-tertiary-fixed-variant: '#004b6f'
  background: '#111319'
  on-background: '#e1e2e9'
  surface-variant: '#32353a'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.25rem
  space-2xs: 0.25rem
  space-xs: 0.5rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.25rem
  space-xl: 1.5rem
  space-2xl: 2rem
  space-3xl: 2.5rem
---

## Brand & Style

This design system establishes a high-performance, focused environment tailored for mobile-first productivity, reference, and rapid execution. Crafted specifically for portrait interaction, the brand personality projects technical confidence, quiet precision, and utilitarian luxury. 

The aesthetic is grounded in **Technical Modernism**—an intersection of minimalist utility and purposeful contrast. Instead of relying on decorative flourishes, visual authority is achieved through razor-sharp typographic pacing, atmospheric dark surfaces, and high-visibility amber accents that direct intent without fatigue.

Target users include engineers, operators, and analysts who require rapid data absorption and zero-friction navigation in high-cognitive-load situations. The interface evokes a sense of calculated calm, tactile control, and focused speed.

## Colors

The palette employs deep obsidian bases accented by radiant amber, calibrated strictly for reduced eye strain in dark environments while exceeding WCAG AAA contrast standards for key interaction elements.

- **Background (`#0E1116`)**: An absolute deep-tone slate, grounding the root viewport and framing surfaces without harsh pure-black clip.
- **Surface / Card (`#161B22`)**: Elevated substrate for data containers, sheets, and interactive cards.
- **Border / Outline (`#222A35`)**: Precise structural delimiter used to define cards, inputs, and segment dividers at 1px line weights.
- **Text Primary (`#E6EAF0`)**: Crisp, cool off-white ensuring effortless legibility across all body copy and primary metrics.
- **Text Secondary / Muted (`#9AA6B8`)**: Low-chroma steel slate reserved for supporting labels, meta information, and placeholder content.
- **Accent / Brand (`#E8A33D`)**: High-luminance warm amber reserved strictly for critical focal points: active states, primary CTAs, notifications, and key data points.

Never use pure white `#FFFFFF` for body text to avoid halation effects against the deep background. Amber is applied sparingly; overusing the accent across non-interactive decorations diminishes its navigational value.

## Typography

Typography relies entirely on **Inter**, configured for immediate glanceability and tight vertical scan efficiency. Micro-adjustments in letter-spacing compensate for variable rendering in high-contrast dark environments.

- **Display & Headlines (`display-lg`, `headline-lg`, `headline-md`)**: Feature tight negative tracking (`-0.02em` to `-0.01em`) to create a cohesive editorial header hierarchy that anchors view layouts.
- **Body (`body-lg`, `body-md`, `body-sm`)**: Neutral tracking with relaxed line height (140%–150%) prevents text crowding on handheld displays.
- **Labels & Metas (`label-lg`, `label-md`, `label-caps`)**: Pushed to medium and semibold weights with slightly expanded tracking to maintain clarity on high-density displays. `label-caps` is formatted exclusively in uppercase for category tags, micro-badges, and column labels.

## Layout & Spacing

The mobile layout is engineered around an iPhone standard portrait canvas (390×844pt) using a fluid column infrastructure constrained by absolute perimeter rules:

- **Screen Margins**: Fixed at **20px (`1.25rem`)** outer horizontal padding, providing a breathable, stable frame away from bezel edges.
- **Grid Layout**: A 4-column fluid mobile grid with **16px (`1rem`)** gutters governs interior dashboard and list arrangements.
- **Vertical Rhythm**: Built upon a strict 4px/8px modular scale. Spacing tokens standardise internal module padding (`space-md`, `space-lg`) and component stacks (`space-sm`, `space-md`).
- **Touch Ergonomics**: All interactive elements (buttons, segmented controls, row targets) maintain a mandatory minimum hit target of **48px** along the vertical axis, preserving accessibility and one-handed thumb interaction within the lower thumb zone.

## Elevation & Depth

This design system avoids blurry, heavy dropshadows in favor of **structural tonal layering** and **low-contrast micro-outlines**:

- **Layer 0 (Canvas Base)**: `#0E1116` — The foundational dark floor.
- **Layer 1 (Card & Section Containers)**: `#161B22` with a 1px solid border of `#222A35`. This flat separation maintains visual crispness without muddying dark-theme rendering.
- **Layer 2 (Floating Modals & Bottom Sheets)**: `#1B222B` surface accompanied by a subtle, ambient directional wash: `0 12px 32px -4px rgba(0, 0, 0, 0.60)` bounded by a 1px top border of `#2D3746`.
- **Active & Highlight Depth**: Rather than elevation shadows, interactive surfaces express state changes through outline brightness increments (e.g., transitions from `#222A35` to `#E8A33D`) and micro-shifts in background luminosity.

## Shapes

Form geometry emphasizes clean geometric harmony between nested and sibling elements:

- **Cards & Primary Modules**: Standardized to **16px radius (`rounded-lg`)**, softening large structural footprints while aligning with standard mobile viewport curvature.
- **Interactive Controls & Inputs**: Form elements, action buttons, and segmented pickers feature a dedicated **12px radius**, creating a nested relationship inside 16px container frames.
- **Tags & Status Badges**: Small inline tags use **6px to 8px radius (`rounded-sm` / `rounded-md`)**, preserving crispness at smaller pixel footprints.
- **Avatars & Floats**: Absolute round forms (`rounded-full`) are reserved exclusively for circular indicators, toggle thumbs, and user profile badges.

## Components

### Buttons
- **Primary Button**: Solid `#E8A33D` background, `#0E1116` semibold text. Height: 48px minimum. Border radius: 12px. Pressed state: 90% opacity with scale down to `0.98`.
- **Secondary Button**: Background `#161B22`, 1px border `#222A35`, `#E6EAF0` text. Pressed state: background shifts to `#1C232C`.
- **Ghost/Tertiary**: Transparent background, `#9AA6B8` text, hover/press reveals subtle `#161B22` pill surface. Minimum height: 48px.

### Inputs & Text Fields
- Container height: 48px. Background: `#161B22`. Border: 1px solid `#222A35`. Radius: 12px.
- Typography: `body-md` in `#E6EAF0`, placeholder text in `#9AA6B8`.
- Focus state: Border dynamically shifts to `#E8A33D` with a subtle 1px internal highlight; no fuzzy halo glow.

### Cards
- Surface: `#161B22`. Border: 1px solid `#222A35`. Radius: 16px. Padding: 16px or 20px.
- Visual hierarchy: Headers utilize `headline-sm` with optional right-aligned metadata in `label-caps` (`#9AA6B8`).

### Lists & Row Items
- Minimum row height: 56px to ensure rapid touch target acquisition.
- Separators: 1px bottom border using `#222A35`, inset by 20px to match canvas margins.
- Chevron / Trailing indicators styled in `#9AA6B8`. Active tap states provide instant feedback via a `#161B22` background flash.

### Chips & Badges
- Filter Chips: Height: 36px (wrapped in 48px touch boundary). Radius: 8px. Background: `#161B22`, border: `#222A35`. When active: Border and text become `#E8A33D`, background shifts to `#E8A33D` at 12% opacity.
- Status Badges: Height: 24px. Radius: 6px. Padding: 4px 8px. Text: `label-caps`. Amber tone for pending/primary alerts, muted slate for neutral status.

### Checkboxes & Radios
- Size: 22×22px target bounded inside a 48×48px tap container.
- Unchecked: 1.5px border `#222A35`, background transparent.
- Checked: Solid `#E8A33D` fill with `#0E1116` vector checkmark or nested dot indicator. Radius: 6px for checkboxes, 50% for radio buttons.

### Bottom Navigation & Action Bar
- Fixed bottom sheet anchored above mobile home indicator. Height: 64px + safe area padding.
- Background: `#0E1116` with 85% alpha backdrop blur (20px blur) and 1px top border `#222A35`.
- Active tabs illuminated in `#E8A33D`; inactive tabs in `#9AA6B8`.