# Kaleo Church Website Rebuild

Static Astro site that preserves the Kaleo Church information architecture and destinations from `kaleoalaska.org` while applying a clean, consistent presentation.

## Stack

- Astro (static)
- Centralized config/data in `src/config/site.ts`
- Reusable UI components in `src/components`

## Project Structure

- `src/pages` route files
- `src/components` reusable blocks (nav, footer, hero, list/grid)
- `src/layouts` base shell
- `src/config/site.ts` navigation + canonical external/document links
- `docs/content-map.md` legacy/new route and parity map
- `docs/brand-style.md` visual system

## Prerequisites

- **Node.js**: Version 20.x or higher.
- **npm**: Version 10.x or higher.

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hotredsam/Church-Site.git
   cd Church-Site
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run locally**:
   ```bash
   npm run dev
   ```

4. **Open the site**:
   Navigate to `http://localhost:4321`.

## Production Build

```bash
npm run build
npm run preview
```

## Sync Live Parity Data

```bash
npm run sync:legacy
npm run sync:content-map
```

These commands pull the live sitemap and generate:
- `src/content/legacy-pages.json` (text + outbound/doc/video links for missing pages)
- `docs/content-map.md` (full coverage and per-page link inventory)

## QA Checklist

- Verify top-level nav parity: Home, About, Get Connected, Grow, Events, Give.
- Validate all Church Center links open correct destinations.
- Validate all PDF links open directly.
- Test mobile nav and dropdown behavior.
- Check route compatibility for legacy paths (`/jd-*`, `/josh-sawyer`, `/upcoming-events`, etc.).
- Run `npm run build` without errors.

## Copy Workflow

Copy cleanup was performed with local Ollama model (`glm-4.7-flash:latest`) while preserving factual meaning and avoiding invented details.
