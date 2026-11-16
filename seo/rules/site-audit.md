# Site Audit

## Purpose

Audit crawlability, indexability, redirects, internal links, performance, structured data and on-page basics. Every finding must be reproducible (URL plus how you checked) and prioritised by impact. Fix what you can directly when you have repo access and approval.

## Before starting

1. Read `.seo/project-profile.md` and the latest `.seo/audits/` file.
2. Pull Search Console indexing data first ([search-console.md](search-console.md)). It tells you where to look.
3. If you have the repo, read how routing, metadata, canonicals, sitemap, robots and redirects are generated. Fixes belong in code, not one-off patches.

## Checks

### Crawl and index

- `robots.txt`: reachable, not blocking important paths or CSS/JS, sitemap declared, AI crawler policy deliberate ([geo-ai-search.md](geo-ai-search.md)).
- Sitemap: returns 200, only canonical 200 URLs (no redirects, 404s, noindex or parameter URLs), lastmod truthful, count matches the real page count.
- Every important page: status 200, self-canonical, indexable, in the sitemap, linked internally.
- One host and protocol (https, www or not), one trailing-slash policy; the alternatives 301 to it.
- Parameter and filter URLs (`?tag=`, `?page=`, `?ref=`, `?utm_`) canonicalised or noindexed so they don't bloat the index.
- Old URLs (from GSC, old sitemaps, backlinks) 301 in a single hop to the closest live page.

### Internal links

- Run [../scripts/crawl-internal-links.mjs](../scripts/crawl-internal-links.mjs) over the sitemap: every internal link that doesn't return 200, and which pages contain it.
- Orphans: sitemap URLs with no internal links in.
- Click depth: money pages within 2-3 clicks of the home page.
- Hubs: service/pillar pages link to their supporting articles and back, with descriptive anchors.

### Rendering and performance

- Key content and links present in the server HTML (`curl`), not only after JavaScript.
- Core Web Vitals: field data from the Search Console CWV report or PageSpeed Insights (CrUX). With no field data, use Lighthouse lab data (Chrome DevTools MCP `lighthouse_audit` / `performance_start_trace`) and label it lab data.
- Mobile layout at 360-414px; images sized, compressed, modern formats, lazy below the fold; fonts not blocking.

### On-page basics (each template plus key pages)

- Unique title and meta description of sensible length; one H1; logical H2/H3.
- Intent matches the queries the page gets in GSC.
- Visible authorship, dates, contact and business details (trust).
- Structured data valid (Rich Results Test or Schema.org validator via Chrome) and matching visible content.

### Quality and duplication

- Thin, overlapping or off-offer pages: send them to [content-inventory.md](content-inventory.md).
- Cannibalisation: several URLs ranking for the same query in GSC.

## Useful in-page script

Run with `evaluate_script` on any page:

```javascript
() => ({
  title: document.title,
  description: document.querySelector('meta[name="description"]')?.content,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  robots: document.querySelector('meta[name="robots"]')?.content,
  h: [...document.querySelectorAll('h1,h2,h3')].map(h => `${h.tagName} ${h.textContent.trim()}`).slice(0, 40),
  schemaTypes: [...document.querySelectorAll('script[type="application/ld+json"]')].flatMap(s => { try { const j = JSON.parse(s.textContent); return (j['@graph'] || [j]).map(x => x['@type']); } catch { return ['INVALID JSON']; } }),
  imgsNoAlt: [...document.querySelectorAll('img')].filter(i => !i.alt).map(i => i.src).slice(0, 20),
  internalLinks: new Set([...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => h.startsWith(location.origin))).size,
})
```

For many URLs at once, use curl plus node instead of the browser (see [../scripts/](../scripts/)).

## Severity

- **Critical:** blocks crawling/indexing or breaks key pages (noindex on money pages, 5xx, robots block, redirect loops).
- **High:** materially limits ranking or CTR (404s with links/traffic, missing redirects after a redesign, broken internal links, duplicate titles on key pages, slow LCP on mobile).
- **Medium:** optimisation gaps.
- **Low:** polish.

## Output

`.seo/audits/YYYY-MM-DD.md`:

```markdown
# SEO Audit - {site} - {date}
**Pages checked:** {n}  **Tools:** {GSC, curl crawl, Lighthouse, ...}

## Summary
- Biggest blocker: ...
- Fixed during this audit: ...
- Needs the user: ...

## Findings
| # | Severity | Issue | URLs / template | Evidence | Fix | Effort | Status |
```
