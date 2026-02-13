# Next-Steps Action Plan — Kaleo Church Website

Version: 1.0
Author: Dev Team (automated)
Date: 2026-02-12

Overview
--------

This document is a comprehensive, prioritized action plan for turning the repository into a fully-functional, modern, accessible, and maintainable church website. It covers strategy, content, technical implementation, infrastructure, monitoring, and handoff. The plan is intentionally practical: each section includes concrete tasks, estimated effort, acceptance criteria, and implementation notes.

Executive summary
-----------------

Goals
- Provide clear public information (who we are, when/where, how to connect, service times).
- Make giving and connecting as frictionless and secure as possible.
- Ensure discoverability and SEO for core content (sermons, events, service info).
- Provide reliable, accessible UX across devices and assistive tech.
- Enable a maintainable workflow for content updates and deployments.

High-level phases
1. Audit & quick fixes (meta, favicon, sitemap, accessibility anchors) — done or in-progress.
2. Core UX: navigation, contact, giving, live-stream, plan-your-visit pages.
3. Integrations: Church Center links, giving integration guidance, streaming embed.
4. Infrastructure: build + deploy automation, monitoring, backups.
5. Polish: OG images, structured data (JSON-LD), SEO, analytics, accessibility sweep.
6. Handoff: README, contributor guide, editing instructions.

How to use this document
------------------------

Treat each sub-section as a self-contained ticket. Implement in small merges and run the build/tests after each. The repo now contains an initial working site; the plan focuses on completing and hardening the site for production.

Contents
--------

1. Audit & Prioritization
   - Inventory pages and external dependencies.
   - Identify pages requiring content updates (staff bios, location information, upcoming events).
   - Acceptance: A prioritized ticket list mapped to files in `src/pages` or `content`.

2. Site Metadata & SEO (Immediate)
   - Ensure every page has descriptive <title>, <meta description>, canonical URLs, and Open Graph tags.
   - Add `sitemap.xml` endpoint (done) and `robots.txt` (done).
   - Add structured data for Organization and LocalBusiness (JSON-LD) on relevant pages.
   - Acceptance: `npm run build` completes and `sitemap.xml` returns expected URLs.

3. Accessibility & Usability
   - Add skip links (done), ensure keyboard navigation for nav and submenus, add ARIA attributes.
   - Ensure color contrast meets WCAG AA (check color tokens), adjust if required.
   - Acceptance: no critical accessibility failures in automated scan (axe-core or similar).

4. Contact & Forms (Core)
   - Provide a Church Center link (already present) and a fallback in-site contact form.
   - Implement a secure server-side endpoint to accept contact submissions and email/stash them for staff.
   - Provide rate-limiting and spam protection (honeypot / token / recaptcha integration guidance).
   - Acceptance: Submissions persist in a secure data store and staff receives a notification (email or webhook).

5. Giving
   - Keep Church Center giving link as primary (done). Add a friendly in-site page describing giving options and FAQ.
   - Provide developer guidance for adding Stripe (if the church prefers) and secure token handling — do not collect card data directly in the site.
   - Acceptance: Give page links to Church Center and docs updated.

6. Live Stream
   - Embed YouTube live stream or link to watch page; ensure mobile playback and keyboard access.
   - Add a dedicated `/live-stream` page with next stream time and recording links.
   - Acceptance: Live stream loads and plays on desktop and mobile.

7. Events & Calendar
   - Use Church Center calendar for authoritative events. Mirror a basic listing for SEO and on-site discoverability.
   - Acceptable approach: fetch events server-side at build time or via an API route when possible; fallback to Church Center link.
   - Acceptance: Events page shows upcoming events and links to Church Center details.

8. Sermons & Media
   - Ensure sermon pages include meta description, published date, preacher, series, scripture tags.
   - Add RSS/Podcast feeds for sermons if audio exists (link to `listen` canonical URL).
   - Acceptance: Sermon pages render proper Open Graph and JSON-LD for CreativeWork.

9. Jobs & Team
   - Keep job descriptions as PDFs (already linked). Add structured metadata for job posts and a job board page.
   - Add staff bios with sanitized images and contact links.
   - Acceptance: Staff pages render and PDFs download.

10. Performance & Hosting
    - Use modern static hosting (Vercel, Netlify, GitHub Pages for static output). For API endpoints choose Vercel Functions or Netlify Functions.
    - Add GitHub Actions to build and run tests. Optionally deploy to a staging branch.
    - Acceptance: CI builds on PRs and deploys to staging.

11. Monitoring & Analytics
    - Add basic telemetry/instrumentation: privacy-minded Google Analytics (or Plausible), uptime monitoring, error reporting.
    - Acceptance: Event tracking for key actions (visit, play live stream, open connect card, submit contact form).

12. Security & Privacy
    - Audit forms and third-party links; produce a privacy notice page referencing Church Center’s data handling.
    - Add instructions for rotating API keys, and for using environment variables for secrets in CI.
    - Acceptance: No secrets in repo, documented env vars.

Implementation plan (detailed tasks)
----------------------------------

Phase A — Quick wins (0.5–1 day)
- Add missing favicons and meta tags (done).
- Add sitemap endpoint (done).
- Add skip link and basic mobile nav (done).

Phase B — Contact & Give (1–2 days)
- Implement contact fallback form (serverless API route + storage and optional email webhook).
  - Acceptance tests: submission returns 200 and stored record.
- Improve Give page with FAQ and secure guidance.

Phase C — Deploy & CI (0.5–1 day)
- Add GitHub Actions to build and (optionally) deploy.

Phase D — SEO & OG images (1–2 days)
- Create share images, update OG tags, add JSON-LD.

Phase E — Accessibility, testing, and polish (1–2 days)

Detailed tickets & dev notes
---------------------------

Ticket 1: Contact fallback form
- Files to add:
  - `src/pages/get-connected/contact-fallback.astro` (UI form)
  - `src/pages/api/contact.ts` (API route)
  - `data/contacts.json` (storage during early deployment or for review)
- Requirements:
  - Form fields: name, email, phone (optional), message, honeypot hidden field.
  - Validate server-side for required fields and basic email format.
  - Append to `data/contacts.json` with timestamp and remote IP (if available). Do not expose IP publicly; restrict log access.
  - If `EMAIL_WEBHOOK_URL` env var is present, POST submission to that webhook (for staff notifications).
  - Rate limit: basic per-IP in-memory or via token; provide guidance for production rate-limiting via platform provider.

Ticket 2: Give page improvements
- Add contextual content, FAQ, and contact for giving support.
- Do not collect card data; link to Church Center giving using `canonical.giving`.

Ticket 3: CI / Deploy workflow
- Add `.github/workflows/ci.yml` to build and optionally deploy to GitHub Pages or Vercel.

Ticket 4: OG images and structured data
- Add a small script to generate OG images (or provide static images in `public/og/`).
- Add Organization and LocalBusiness JSON-LD in `BaseLayout`.

Ticket 5: Accessibility sweep
- Run `axe` or similar; fix headings, landmark roles, images alt text, forms labels.

Operational notes
-----------------

- Secrets: add guidance for `EMAIL_WEBHOOK_URL`, `DEPLOY_KEY`, `ANALYTICS_ID` and how to store them.
- Platform choice: recommend Vercel if serverless functions are needed, or Netlify if preferred.

Acceptance criteria for overall project
------------------------------------

1. Site builds (`npm run build`) with no warnings that block output.
2. `sitemap.xml` and `robots.txt` are present.
3. Contact form submissions reach staff (webhook) or are safely stored for review.
4. Give page points to Church Center and is clear about security.
5. CI runs on PRs and runs build + basic tests.

Appendices
----------

Appendix A — Contact form sample JSON record
```
{
  "id": "2026-02-12T14:00:00Z-1",
  "name": "Jane Doe",
  "email": "jane@example.org",
  "phone": "(907) 555-0101",
  "message": "I want to learn about getting connected.",
  "source": "/get-connected/contact-fallback",
  "timestamp": "2026-02-12T14:00:00Z"
}
```

Appendix B — Suggested GitHub Actions CI (high level)
- Run `npm ci` or `npm install`.
- Run `npm run build`.
- Run a11y and lint checks.
- Optionally deploy on merge to `main`.

Appendix C — Privacy guidance
- Add a short privacy page describing what data is collected via Church Center and via the fallback contact form (name, email, message). Include retention policy and contact for data requests.

Closing notes
-------------

This document is intentionally actionable. I will now begin implementing the highest-priority, low-risk items: (A) adding the contact fallback form UI and the server-side endpoint that stores submissions and optionally forwards them to a webhook. After that I'll implement the CI workflow and produce the handoff README.

— End of plan
