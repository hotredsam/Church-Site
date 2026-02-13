You are Codex running with full permissions.



GOAL

Build a new, clean, readable, consistent-theme website project for Kaleo Church (current site: https://www.kaleoalaska.org/). The new site must preserve the same information architecture and user destinations: all pages, outbound links, and downloadable documents (PDFs) that exist on the current site should be present and reachable from the same kinds of nav paths.



IMPORTANT: Use my locally installed model via Ollama for any copy cleanup or rewriting while preserving meaning:

\- Model: GLM 4.6

\- Use: `ollama run <your-glm-4.6-model-name>` (or `ollama list` to find the exact name), and pipe page copy into it to produce improved, clearer wording.

\- Do NOT invent theology, events, staff details, addresses, phone numbers, or schedules—only rephrase/simplify what is already on the current site.



WHAT TO BUILD (a “little website project”)

\- Make a modern static site (Astro + Tailwind preferred; acceptable: Next.js + Tailwind).

\- Fully responsive, accessible (semantic HTML, keyboard nav, good contrast), fast, and SEO-friendly.

\- Clean, consistent theme: one typography system, one color palette, consistent spacing, consistent button/link styles.

\- Keep the church’s “classic, straightforward” vibe: clear headings, readable paragraphs, minimal fluff.



CONTENT \& PARITY REQUIREMENTS

1\) Crawl the current site and produce a `docs/content-map.md` that lists:

&nbsp;  - Every page URL you found

&nbsp;  - Its new route in the new site

&nbsp;  - All outbound links on that page

&nbsp;  - All document/PDF links on that page

2\) Replicate the top-level navigation structure (Home, About, Get Connected, Grow, Events, Give) and the main child pages under each.

3\) Preserve all “Church Center” links (connect card, giving, baptisms, etc.) as external links exactly (don’t rebuild those apps; just link to them).

4\) Preserve Sermons / Live Stream destinations as links or embeds, but don’t attempt to scrape/host their media library—just present it nicely and send users to the official source.

5\) For pages that include PDF role descriptions or other documents, include them as direct links (same URLs) grouped and labeled cleanly.



PAGES TO PRIORITIZE (ensure these exist with excellent UX)

\- Home

\- About + (Plan Your Visit, Staff \& Leadership, What We Believe, Our Story)

\- Get Connected + (Contact/Connect Card, K-Groups, Kaleo Kids, Kaleo Student Ministry, Men’s Ministry, Church Center App)

\- Grow + (Sermons, Bible Reading Plan, Prayer, Baptism, Membership, Serve, Re|Engage)

\- Events (Upcoming Events / calendar)

\- Give (external)



IMPLEMENTATION DETAILS

\- Create a clear project structure with `/src/pages`, `/src/components`, `/src/layouts`, and `/src/content` if using Astro.

\- Create reusable components: Header/Nav (desktop + mobile), Footer, Hero, CTA blocks, PageHeader, CardGrid, LinkList, DocumentList.

\- Add a single source of truth config file for navigation + footer links (e.g., `src/config/site.ts`).

\- Put all “canonical” URLs (original URLs, external URLs, pdf URLs) in config/data files so they’re easy to maintain.

\- Include a simple site search (optional but nice) for page titles using a small client-side index.

\- Add `README.md` with setup + dev + build + deploy instructions.



DELIVERABLES

\- Working site project in this repo.

\- `docs/content-map.md` (url parity map).

\- `docs/brand-style.md` (palette, typography, components, usage).

\- Run/build instructions and a final quick QA checklist.



START NOW

1\) Crawl and enumerate the current site pages + key links/docs.

2\) Generate the content map.

3\) Scaffold the project.

4\) Implement pages + shared layout + nav/footer.

5\) Use GLM 4.6 (via Ollama) to polish the copy while keeping meaning.

6\) Final pass: check nav parity, link parity, document links, mobile layout, and build succeeds.



