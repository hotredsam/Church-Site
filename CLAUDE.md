# Kaleo Church Website (Clear Project)

Static Astro site rebuild for Kaleo Church (kaleoalaska.org). Preserves the original information architecture -- all pages, navigation paths, outbound links, and downloadable documents from the legacy site -- while applying a clean, consistent visual design with warm tones and green accents.

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | Astro | ^5.2.0 |
| Language | TypeScript (config) | via tsconfig.json |
| Templating | Astro components (.astro) | -- |
| Styling | Vanilla CSS (global.css) | -- |
| Fonts | Lora (serif headings), Source Sans 3 (body) | Google Fonts |
| Node.js | Required | 20.x+ |
| npm | Required | 10.x+ |

## Project Structure

```
Clear Project/
  astro.config.mjs        # Astro config (site: kaleoalaska.org)
  tsconfig.json            # TypeScript config
  package.json             # Scripts: dev, build, preview, check, sync:*
  CODEX_GUIDE.md           # Original build prompt/spec for this project
  docs/
    brand-style.md         # Color palette, typography, component reference
    content-map.md         # Legacy URL -> new route parity map
  src/
    config/
      site.ts              # Navigation structure, footer links, external URLs
    layouts/
      BaseLayout.astro     # HTML shell with header/footer
    components/
      Header.astro         # Sticky nav with desktop dropdown and mobile expand
      Footer.astro         # Footer with quick links
      Hero.astro           # Gradient hero section
      PageHeader.astro     # Consistent page intro block
      CardGrid.astro       # Feature/child-page cards
      LinkList.astro       # Outbound link listings
      DocumentList.astro   # Grouped PDF/document links
      LegacyContent.astro  # Fallback for unmigrated legacy pages
    content/
      legacy-pages.json    # Scraped text + links from legacy site
      link-health.json     # Link validation results
      site-data.json       # Structured site data
    pages/
      index.astro          # Homepage
      [...slug].astro      # Catch-all for legacy route compatibility
      sitemap.xml.ts       # Dynamic sitemap generation
      about/               # About section pages
      get-connected/       # Ministry connection pages
      grow/                # Spiritual growth pages (sermons, baptism, etc.)
      give/                # Giving (external redirect)
      events/              # Events and calendar
      live-stream/         # Live stream page
      jobs/                # Job description pages
      resources/           # Resource pages
    styles/
      global.css           # Global styles with CSS custom properties
  scripts/
    sync-legacy-pages.mjs  # Pulls live sitemap, generates legacy-pages.json
    generate-content-map.mjs # Generates docs/content-map.md
    check-links.mjs        # Link health checker
  public/                  # Static assets (images, favicons)
```

## Build & Run

```bash
npm install
npm run dev              # Start Astro dev server at http://localhost:4321
npm run build            # Production build to dist/
npm run preview          # Preview production build
npm run check            # Astro type checking
```

### Sync Scripts (content parity)

```bash
npm run sync:legacy      # Refresh legacy-pages.json from live site
npm run sync:content-map # Regenerate content-map.md
npm run check:links      # Validate all outbound links
```

## Brand Style

- **Colors**: Warm paper bg `#f4efe7`, dark green primary `#144e4a`, accent `#a4632d`
- **Typography**: Lora (headings), Source Sans 3 (body), 1rem base with 1.6 line-height
- **Border radius**: 14px global token
- **Spacing**: 3.2rem desktop sections, 2.2rem mobile

See `docs/brand-style.md` for the complete visual reference.

## Code Patterns

- **Single source of truth for nav**: All navigation links and external URLs live in `src/config/site.ts`. Do NOT hardcode URLs in page files.
- **Component-driven pages**: Pages compose reusable components (Hero, PageHeader, CardGrid, LinkList, DocumentList). New pages should use the same components.
- **Catch-all routing**: `[...slug].astro` handles legacy URLs that do not have dedicated page files, rendering content from `legacy-pages.json`.
- **External links preserved**: Church Center links (giving, connect card, baptism forms) are external redirects. Do NOT try to rebuild those features.
- **Sermons/Live Stream**: These link to the church's media provider. Do NOT attempt to host or scrape sermon audio/video.
- **Copy cleanup**: Page copy was cleaned up using a local Ollama model (GLM 4.7 Flash). Factual meaning was preserved; no content was invented.

## Important Files -- Do NOT Modify Without Understanding

- `src/config/site.ts` -- Central config for all navigation, footer links, and external URLs. Breaking this breaks the entire site nav.
- `src/layouts/BaseLayout.astro` -- HTML shell applied to every page. Changes here affect all pages.
- `src/content/legacy-pages.json` -- Machine-generated from sync scripts. Do NOT hand-edit; re-run `npm run sync:legacy` instead.
- `docs/content-map.md` -- Auto-generated parity map. Regenerate with `npm run sync:content-map`.
- `CODEX_GUIDE.md` -- Original project spec. Keep for reference; do not delete.

## QA Checklist (from README)

- Verify top-level nav parity: Home, About, Get Connected, Grow, Events, Give.
- Validate all Church Center links open correct destinations.
- Validate all PDF links open directly.
- Test mobile nav and dropdown behavior.
- Check route compatibility for legacy paths (`/jd-*`, `/josh-sawyer`, `/upcoming-events`, etc.).
- Run `npm run build` without errors.

## Gotchas and Warnings

- Do NOT invent church details (theology, events, staff info, addresses, schedules). Only rephrase existing content.
- Do NOT add Tailwind or another CSS framework. The project uses vanilla CSS with a deliberate design system.
- The `[...slug].astro` catch-all is critical for legacy URL support. Removing it will break old bookmarks and search engine links.
- Several pages exist at both legacy paths (e.g., `/jd-kaleo-kids-director`) and new paths (`/jobs/jd-kaleo-kids-director`). Both must work.
- The site target is `https://www.kaleoalaska.org` (set in `astro.config.mjs`). Update this if deploying to a different domain.
- There is a `.github/` directory indicating CI/CD may be configured. Check workflows before pushing breaking changes.
