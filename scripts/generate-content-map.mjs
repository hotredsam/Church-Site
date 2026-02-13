import fs from "node:fs/promises";
import path from "node:path";

const ROOT = process.cwd();
const SITE = "https://www.kaleoalaska.org";
const PAGES_DIR = path.join(ROOT, "src", "pages");
const LEGACY_JSON = path.join(ROOT, "src", "content", "legacy-pages.json");
const OUT = path.join(ROOT, "docs", "content-map.md");

function routeFromFile(relPath) {
  const noExt = relPath.replace(/\\/g, "/").replace(/\.astro$/, "");
  if (noExt.includes("[...") || noExt.includes("[") || noExt === "404") return null;
  if (noExt === "index") return "/";
  if (noExt.endsWith("/index")) return `/${noExt.slice(0, -6)}`;
  return `/${noExt}`;
}

async function listAstroRoutes(dir, prefix = "") {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const out = [];
  for (const entry of entries) {
    const rel = path.join(prefix, entry.name);
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...(await listAstroRoutes(abs, rel)));
      continue;
    }
    if (!entry.name.endsWith(".astro")) continue;
    const r = routeFromFile(rel);
    if (r) out.push(r);
  }
  return out;
}

function uniq(items) {
  return [...new Set(items)];
}

function mdList(items) {
  if (!items || items.length === 0) return "- None";
  return items.map((i) => `- ${i}`).join("\n");
}

async function main() {
  const sitemapXml = await (await fetch(`${SITE}/sitemap.xml`)).text();
  const sitemapUrls = uniq(Array.from(sitemapXml.matchAll(/<loc>(.*?)<\/loc>/g)).map((m) => m[1].trim()));
  const sitemapRoutes = sitemapUrls
    .filter((u) => u.startsWith(SITE))
    .map((u) => {
      const p = new URL(u).pathname.replace(/\/$/, "");
      return p || "/";
    });

  const existingRoutes = new Set(await listAstroRoutes(PAGES_DIR));
  const legacy = JSON.parse(await fs.readFile(LEGACY_JSON, "utf8"));
  const legacyMap = new Map(legacy.map((r) => [r.route, r]));
  const allRoutes = uniq([...sitemapRoutes, ...legacy.map((r) => r.route)]).sort((a, b) => a.localeCompare(b));

  const tableRows = allRoutes
    .map((route) => {
      const sourceUrl = `${SITE}${route === "/" ? "/" : route}`;
      const implementedVia = existingRoutes.has(route) ? "Dedicated Astro page" : legacyMap.has(route) ? "Legacy catch-all mirror" : "Missing";
      const newRoute = route;
      return `| \`${sourceUrl}\` | \`${newRoute}\` | ${implementedVia} |`;
    })
    .join("\n");

  const detailSections = allRoutes
    .map((route) => {
      const record = legacyMap.get(route);
      const sourceUrl = `${SITE}${route === "/" ? "/" : route}`;
      const outbound = record ? record.outboundLinks : [];
      const docs = record ? record.documentLinks : [];
      const videos = record ? record.videoLinks : [];
      const images = record ? record.imageLinks ?? [] : [];
      return `### \`${route}\`\nSource: ${sourceUrl}\n\nOutbound Links\n${mdList(outbound)}\n\nDocument/PDF Links\n${mdList(docs)}\n\nVideo Links\n${mdList(videos)}\n\nImage Links\n${mdList(images)}\n`;
    })
    .join("\n");

  const missingCount = allRoutes.filter((route) => !existingRoutes.has(route) && !legacyMap.has(route)).length;
  const extraRoutes = allRoutes.filter((route) => !sitemapRoutes.includes(route)).length;
  const doc = `# Kaleo Content Map\n\nCrawl date: ${new Date().toISOString().slice(0, 10)}\nSource: ${SITE}\n\n## Coverage Summary\n\n- Sitemap URLs discovered: ${sitemapRoutes.length}\n- Extra routes discovered from internal crawling: ${extraRoutes}\n- Total routes tracked: ${allRoutes.length}\n- Dedicated Astro routes: ${[...existingRoutes].filter((r) => allRoutes.includes(r)).length}\n- Legacy mirrored routes: ${legacy.length}\n- Missing routes: ${missingCount}\n\n## Route Parity\n\n| Current URL | New Route | Implementation |\n|---|---|---|\n${tableRows}\n\n## Links/Files/Videos/Images By Page\n\n${detailSections}\n`;

  await fs.mkdir(path.dirname(OUT), { recursive: true });
  await fs.writeFile(OUT, doc, "utf8");
  console.log(`wrote=${OUT}`);
  console.log(`sitemap_routes=${sitemapRoutes.length}`);
  console.log(`total_routes=${allRoutes.length}`);
  console.log(`missing=${missingCount}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
