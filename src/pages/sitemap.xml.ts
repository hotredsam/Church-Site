import { canonical, nav } from "../config/site";

export async function GET() {
  const base = canonical.org.replace(/\/$/, "");
  const paths = new Set<string>();

  // include homepage
  paths.add("/");

  // include nav entries and top-level children
  nav.forEach((item) => {
    paths.add(item.href);
    if (item.children) item.children.forEach((c) => paths.add(c.href));
  });

  // common static paths
  [
    "/live-stream",
    "/give",
    "/about",
    "/get-connected",
    "/grow",
    "/events",
    "/advent-resources",
  ].forEach((p) => paths.add(p));

  const urls = Array.from(paths).map((p) => {
    const loc = base + (p === "/" ? "" : p);
    return `  <url>\n    <loc>${loc}</loc>\n  </url>`;
  }).join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`;

  return new Response(xml, {
    headers: { "Content-Type": "application/xml" },
  });
}
