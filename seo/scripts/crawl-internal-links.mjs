#!/usr/bin/env node
/**
 * Find broken or redirecting internal links across a site.
 *
 *   node crawl-internal-links.mjs https://example.com            # reads /sitemap.xml
 *   node crawl-internal-links.mjs https://example.com urls.txt   # or a file of URLs, one per line
 *
 * For every page it collects same-site <a href> targets, requests each unique target
 * once (without following redirects) and prints every non-200 target with the pages
 * that link to it. Also lists sitemap URLs that nothing links to (orphans).
 */
import { readFileSync } from "node:fs";

const [origin, file] = process.argv.slice(2);
if (!origin) {
  console.error("Usage: node crawl-internal-links.mjs https://site.com [urls.txt]");
  process.exit(1);
}
const site = new URL(origin).origin;
const SKIP = /\.(webp|png|jpe?g|gif|svg|ico|css|js|mjs|xml|txt|pdf|woff2?|mp4)$/i;

async function sitemapUrls() {
  const xml = await (await fetch(`${site}/sitemap.xml`)).text();
  const locs = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].trim());
  const nested = locs.filter((u) => u.endsWith(".xml"));
  if (nested.length === 0) return locs;
  const pages = locs.filter((u) => !u.endsWith(".xml"));
  for (const sm of nested) {
    const inner = await (await fetch(sm)).text();
    pages.push(...[...inner.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].trim()));
  }
  return pages;
}

const pages = file ? readFileSync(file, "utf8").split(/\r?\n/).filter(Boolean) : await sitemapUrls();
const linkedFrom = new Map();

for (const page of pages) {
  let html = "";
  try {
    html = await (await fetch(page)).text();
  } catch {
    console.log(`FETCH FAILED ${page}`);
    continue;
  }
  for (const m of html.matchAll(/href="([^"]+)"/g)) {
    let url;
    try {
      url = new URL(m[1], page);
    } catch {
      continue;
    }
    if (url.origin !== site || SKIP.test(url.pathname) || url.pathname.startsWith("/_")) continue;
    const path = url.pathname;
    if (!linkedFrom.has(path)) linkedFrom.set(path, new Set());
    linkedFrom.get(path).add(new URL(page).pathname);
  }
}

const problems = [];
for (const [path, sources] of linkedFrom) {
  const res = await fetch(site + path, { redirect: "manual" });
  if (res.status !== 200) {
    const loc = res.headers.get("location");
    problems.push(`${res.status} ${path}${loc ? ` -> ${loc}` : ""}\n    linked from: ${[...sources].slice(0, 8).join(", ")}${sources.size > 8 ? ` (+${sources.size - 8})` : ""}`);
  }
}

const orphans = pages.map((p) => new URL(p).pathname).filter((p) => !linkedFrom.has(p));

console.log(`Crawled ${pages.length} pages, ${linkedFrom.size} unique internal targets.\n`);
console.log(problems.length ? `Non-200 internal links (${problems.length}):\n${problems.join("\n")}` : "No broken or redirecting internal links.");
console.log(orphans.length ? `\nSitemap URLs with no internal links (${orphans.length}):\n${orphans.join("\n")}` : "\nNo orphan sitemap URLs.");
