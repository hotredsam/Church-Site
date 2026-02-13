# Brand Style

## Direction

- Tone: classic, straightforward, clear.
- Visual character: warm paper background with subtle green accents.
- Interaction: simple transitions and readable hierarchy.

## Colors

- `--bg`: `#f4efe7`
- `--surface`: `#fffaf2`
- `--surface-soft`: `#f8f2e8`
- `--text`: `#21190f`
- `--muted`: `#5a4f43`
- `--line`: `#d8c8b3`
- `--primary`: `#144e4a`
- `--primary-soft`: `#e3efee`
- `--accent`: `#a4632d`

## Typography

- Headings: `Lora` (serif)
- Body: `Source Sans 3` (sans-serif)
- Scales:
  - Page title: responsive clamp (`~1.9rem` to `3rem`)
  - Body: base `1rem` with `1.6` line-height

## Components

- `Header`: sticky nav with desktop dropdown and mobile-expanded child links.
- `Footer`: quick links + core external destinations.
- `Hero`: gradient section with concise call-to-actions.
- `PageHeader`: consistent intro block for internal pages.
- `CardGrid`: reusable feature and child-page cards.
- `LinkList`: outbound destination listing.
- `DocumentList`: grouped PDF/document links.

## Spacing + Rhythm

- Section spacing: `3.2rem` desktop, `2.2rem` mobile.
- Card padding: `~1rem to 1.2rem`.
- Border radius: `14px` global token.

## Accessibility

- Semantic landmarks (`header`, `nav`, `main`, `footer`).
- High-contrast text/link colors against warm surfaces.
- Keyboard-usable menu via `:focus-within` and standard links.
