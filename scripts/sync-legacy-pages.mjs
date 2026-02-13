import fs from "node:fs/promises";
import path from "node:path";

const SITE = "https://www.kaleoalaska.org";
const ROOT = process.cwd();
const PAGES_DIR = path.join(ROOT, "src", "pages");
const OUTPUT = path.join(ROOT, "src", "content", "legacy-pages.json");

function decodeEntities(text) {
  return text
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}

function cleanText(html) {
  const stripped = html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, " ")
    .replace(/<svg[\s\S]*?<\/svg>/gi, " ")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<\/h[1-6]>/gi, "\n")
    .replace(/<li[^>]*>/gi, "- ")
    .replace(/<[^>]+>/g, " ");

  return decodeEntities(stripped)
    .replace(/\r/g, "")
    .split("\n")
    .map((line) => line.replace(/\s+/g, " ").trim())
    .filter(Boolean)
    .join("\n")
    .trim();
}

function toRouteFromFile(relPath) {
  const noExt = relPath.replace(/\\/g, "/").replace(/\.astro$/, "");
  if (noExt.includes("[...") || noExt.includes("[") || noExt === "404") return null;
  if (noExt === "index") return "/";
  if (noExt.endsWith("/index")) {
    return `/${noExt.slice(0, -"/index".length)}`;
  }
  return `/${noExt}`;
}

async function listAstroRoutes(dir, prefix = "") {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const out = [];
  for (const e of entries) {
    const rel = path.join(prefix, e.name);
    const abs = path.join(dir, e.name);
    if (e.isDirectory()) {
      out.push(...(await listAstroRoutes(abs, rel)));
      continue;
    }
    if (!e.name.endsWith(".astro")) continue;
    const route = toRouteFromFile(rel);
    if (route) out.push(route);
  }
  return out;
}

function uniq(items) {
  return [...new Set(items)];
}

function extractUrls(xml) {
  return uniq(Array.from(xml.matchAll(/<loc>(.*?)<\/loc>/g)).map((m) => m[1].trim()));
}

function extractMatches(regex, html) {
  return Array.from(html.matchAll(regex)).map((m) => m[1]).filter(Boolean);
}

function normalizeUrl(href, base) {
  const cleaned = decodeEntities(String(href).trim())
    .replace(/^['"]+|['"]+$/g, "")
    .replace(/^&quot;|&quot;$/g, "");
  if (!cleaned || /^javascript:/i.test(cleaned) || /^mailto:/i.test(cleaned) || /^tel:/i.test(cleaned)) {
    return null;
  }
  try {
    return new URL(cleaned, base).toString();
  } catch {
    return null;
  }
}

function isDoc(url) {
  return /\.(pdf|doc|docx|ppt|pptx|xls|xlsx|zip)(\?|#|$)/i.test(url);
}

function isVideoUrl(url) {
  return /(youtube\.com|youtu\.be|vimeo\.com)/i.test(url);
}

function firstSrcsetUrl(srcset) {
  if (!srcset) return null;
  const first = srcset.split(",")[0]?.trim();
  if (!first) return null;
  return first.split(/\s+/)[0]?.trim() || null;
}

function pathFromUrl(u) {
  const url = new URL(u);
  const p = url.pathname.replace(/\/$/, "") || "/";
  const segments = p.split("/").map((seg, idx) => {
    if (idx === 0) return "";
    try {
      return encodeURIComponent(decodeURIComponent(seg));
    } catch {
      return encodeURIComponent(seg);
    }
  });
  return segments.join("/") || "/";
}

async function fetchText(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  const res = await fetch(url, { signal: controller.signal });
  clearTimeout(timeout);
  if (!res.ok) {
    throw new Error(`${res.status} ${url}`);
  }
  return res.text();
}

async function main() {
  const sitemap = await fetchText(`${SITE}/sitemap.xml`);
  const seedUrls = extractUrls(sitemap).filter((u) => u.startsWith(SITE));
  const discovered = new Set(seedUrls);
  discovered.add(`${SITE}/sermons`);

  const crawlQueue = [`${SITE}/sermons`];
  const crawled = new Set();
  const maxSermonPages = 180;

  while (crawlQueue.length > 0 && crawled.size < maxSermonPages) {
    const current = crawlQueue.shift();
    if (!current || crawled.has(current)) continue;
    crawled.add(current);

    try {
      const html = await fetchText(current);
      const hrefs = extractMatches(/<a[^>]+href=["']([^"']+)["']/gi, html)
        .map((h) => normalizeUrl(h, current))
        .filter(Boolean);

      for (const href of hrefs) {
        const u = new URL(href);
        if (u.origin !== SITE) continue;
        if (!u.pathname.startsWith("/sermons")) continue;
        if (!/^\/sermons(\/|$)/.test(u.pathname)) continue;
        const normalizedPath = pathFromUrl(u.toString());
        const normalized = `${u.origin}${normalizedPath}`;
        if (!discovered.has(normalized)) {
          discovered.add(normalized);
          crawlQueue.push(normalized);
        }
      }
    } catch {
      // Continue; we still keep previously discovered URLs.
    }
  }

  const urls = [...discovered];
  const pageRoutes = new Set(await listAstroRoutes(PAGES_DIR));

  const records = [];
  for (const url of urls) {
    const route = pathFromUrl(url);
    if (pageRoutes.has(route)) continue;

    try {
      const html = await fetchText(url);
      const title = decodeEntities((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] || route).trim());

      const hrefs = extractMatches(/<a[^>]+href=["']([^"']+)["']/gi, html)
        .map((h) => normalizeUrl(h, url))
        .filter(Boolean);
      const iframeSrc = extractMatches(/<iframe[^>]+src=["']([^"']+)["']/gi, html)
        .map((h) => normalizeUrl(h, url))
        .filter(Boolean);
      const imgSrc = extractMatches(/<img[^>]+src=["']([^"']+)["']/gi, html)
        .map((h) => normalizeUrl(h, url))
        .filter(Boolean);
      const imgDataSrc = extractMatches(/<img[^>]+data-src=["']([^"']+)["']/gi, html)
        .map((h) => normalizeUrl(h, url))
        .filter(Boolean);
      const imgSrcset = extractMatches(/<img[^>]+srcset=["']([^"']+)["']/gi, html)
        .map((set) => firstSrcsetUrl(set))
        .filter(Boolean)
        .map((h) => normalizeUrl(h, url))
        .filter(Boolean);
      const cssBgUrls = extractMatches(/url\((['"]?)(https?:\/\/[^'")]+)\1\)/gi, html)
        .map((h) => normalizeUrl(h, url))
        .filter(Boolean);

      const imageLinks = uniq([...imgSrc, ...imgDataSrc, ...imgSrcset, ...cssBgUrls]).filter(
        (l) => !isDoc(l)
      );
      const allLinks = uniq([...hrefs, ...iframeSrc, ...imageLinks]);
      const outboundLinks = allLinks.filter((l) => !l.includes("kaleoalaska.org"));
      const documentLinks = allLinks.filter((l) => isDoc(l));
      const videoLinks = uniq(allLinks.filter((l) => isVideoUrl(l)));
      const text = cleanText(html);

      records.push({
        route,
        sourceUrl: url,
        title,
        text,
        outboundLinks: uniq(outboundLinks),
        documentLinks: uniq(documentLinks),
        videoLinks,
        imageLinks
      });
    } catch (err) {
      records.push({
        route,
        sourceUrl: url,
        title: route,
        text: "",
        outboundLinks: [],
        documentLinks: [],
        videoLinks: [],
        imageLinks: [],
        error: String(err)
      });
    }
  }

  records.sort((a, b) => a.route.localeCompare(b.route));
  await fs.mkdir(path.dirname(OUTPUT), { recursive: true });
  await fs.writeFile(OUTPUT, `${JSON.stringify(records, null, 2)}\n`, "utf8");

  console.log(`sitemap_urls=${seedUrls.length}`);
  console.log(`sermon_urls_discovered=${urls.filter((u) => u.includes("/sermons")).length}`);
  console.log(`total_urls_processed=${urls.length}`);
  console.log(`existing_routes=${pageRoutes.size}`);
  console.log(`generated_legacy_records=${records.length}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
