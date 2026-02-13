import fs from "node:fs/promises";
import path from "node:path";

const ROOT = process.cwd();
const LEGACY_JSON = path.join(ROOT, "src", "content", "legacy-pages.json");
const REPORT_JSON = path.join(ROOT, "src", "content", "link-health.json");
const REPORT_MD = path.join(ROOT, "docs", "link-health.md");

function uniq(items) {
  return [...new Set(items.filter(Boolean))];
}

function normalize(url) {
  try {
    const u = new URL(url);
    u.hash = "";
    return u.toString();
  } catch {
    return null;
  }
}

async function checkUrl(url) {
  const start = Date.now();
  try {
    const res = await fetch(url, { method: "HEAD", redirect: "follow" });
    const ms = Date.now() - start;
    if (res.ok) return { url, ok: true, status: res.status, ms };

    const res2 = await fetch(url, { method: "GET", redirect: "follow" });
    return { url, ok: res2.ok, status: res2.status, ms: Date.now() - start };
  } catch (err) {
    return { url, ok: false, status: 0, ms: Date.now() - start, error: String(err) };
  }
}

async function pool(items, worker, concurrency = 14) {
  const out = [];
  let i = 0;
  const runners = Array.from({ length: Math.min(concurrency, items.length) }, async () => {
    while (i < items.length) {
      const idx = i++;
      out[idx] = await worker(items[idx]);
    }
  });
  await Promise.all(runners);
  return out;
}

async function main() {
  const data = JSON.parse(await fs.readFile(LEGACY_JSON, "utf8"));
  const links = uniq(
    data.flatMap((r) => [
      ...(r.outboundLinks || []),
      ...(r.documentLinks || []),
      ...(r.videoLinks || []),
      ...(r.imageLinks || [])
    ])
  )
    .map(normalize)
    .filter(Boolean);

  const results = await pool(links, checkUrl, 12);
  const ok = results.filter((r) => r.ok);
  const bad = results.filter((r) => !r.ok);

  const payload = {
    checkedAt: new Date().toISOString(),
    totals: {
      links: results.length,
      ok: ok.length,
      failed: bad.length
    },
    results
  };

  await fs.writeFile(REPORT_JSON, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

  const topBad = bad.slice(0, 200).map((r) => `- ${r.url} (status=${r.status}${r.error ? ` error=${r.error}` : ""})`).join("\n") || "- None";
  const md = `# Link Health\n\nChecked: ${payload.checkedAt}\n\n- Total links: ${results.length}\n- OK: ${ok.length}\n- Failed: ${bad.length}\n\n## Failed Links (up to 200)\n\n${topBad}\n`;
  await fs.writeFile(REPORT_MD, md, "utf8");

  console.log(`links=${results.length} ok=${ok.length} failed=${bad.length}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
