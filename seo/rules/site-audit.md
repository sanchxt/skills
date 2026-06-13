# Site Audit

## Purpose

Audit technical SEO, indexability, page performance, on-page quality, and internal linking. Findings must be specific, reproducible, and prioritized by impact.

## Before Starting

1. Read `.seo/project-profile.md`.
2. Read previous `.seo/audits/` reports if present.
3. Ask for priority pages when unknown, or audit homepage plus 5-20 important pages based on navigation, sitemap, and user goals.
4. Use live browser inspection when the site is accessible.

## Mandatory Checks

### Crawlability and Indexation

- HTTPS and canonical host consistency.
- `robots.txt` and sitemap availability.
- No accidental `noindex`, `nofollow`, blocked resources, redirect loops, 4xx/5xx errors.
- Canonicals are present and self-referential or intentionally consolidated.
- Important pages are included in sitemap and internally linked.

### Metadata and Content Structure

- Unique title tags and meta descriptions.
- One H1 per page.
- Logical H2/H3 structure.
- Keyword and intent alignment.
- Thin, duplicate, outdated, or cannibalized content.
- E-E-A-T signals: author, sources, trust markers, last updated dates, reviews, credentials.

### Technical and Performance

- Core Web Vitals: LCP, INP, CLS.
- Mobile responsiveness and viewport behavior.
- Image size, dimensions, lazy loading, modern formats, and alt text.
- JS rendering risks and crawlable navigation.
- Structured data JSON-LD and rich result eligibility.
- Hreflang, pagination, faceted navigation, or parameter issues when relevant.

### Internal Links and Architecture

- Orphan or low-linked pages.
- Important pages deeper than 3 clicks.
- Weak or generic anchor text.
- Missing pillar-cluster relationships.
- Broken internal links.

## Browser / DevTools Usage

Use Chrome DevTools MCP, Chrome plugin, browser automation, or web tools when available to inspect:

```javascript
document.title
document.querySelector('meta[name="description"]')?.content
[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => [h.tagName, h.textContent.trim()])
document.querySelector('link[rel="canonical"]')?.href
[...document.querySelectorAll('img')].map(img => ({src: img.src, alt: img.alt, loading: img.loading}))
[...document.querySelectorAll('a[href]')].map(a => ({href: a.href, text: a.textContent.trim()}))
[...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent)
document.querySelector('meta[name="robots"]')?.content
```

Use PageSpeed Insights or Lighthouse-style data when available. If unavailable, explain the limitation and still audit visible performance risks.

## Severity

- **Critical:** blocking crawl/index/ranking or breaking key pages.
- **High:** materially reducing rank potential or CTR.
- **Medium:** meaningful optimization gaps.
- **Low:** polish or minor hygiene.

## Output Template

Store in `.seo/audits/{YYYY-MM-DD}.md`:

```markdown
# SEO Audit - {Website}

**Date:** {date}
**Pages Audited:** {count}
**Sources/Tools:** {browser, PageSpeed, sitemap, SERP, etc.}

## Executive Summary
- **Overall health:** {score or qualitative}
- **Biggest ranking blocker:** {finding}
- **Fastest quick win:** {finding}
- **Highest-leverage strategic fix:** {finding}

## Priority Fixes
| Priority | Severity | Issue | Pages | Impact | Fix | Effort |
|----------|----------|-------|-------|--------|-----|--------|
| 1 | {Critical/High} | {issue} | {URLs} | {impact} | {specific fix} | {S/M/L} |

## Page Findings
### {URL}
| Element | Status | Finding | Recommendation |
|---------|--------|---------|----------------|
| Title | {pass/warn/fail} | {current} | {fix} |
| Meta description | {status} | {current} | {fix} |
| H1/headings | {status} | {finding} | {fix} |
| Canonical/indexing | {status} | {finding} | {fix} |
| Content/intent | {status} | {finding} | {fix} |
| Internal links | {status} | {finding} | {fix} |
| Images | {status} | {finding} | {fix} |
| Schema | {status} | {finding} | {fix} |
| Performance | {status} | {finding} | {fix} |

## Technical Notes
- **Robots.txt:** {finding}
- **Sitemap:** {finding}
- **Core Web Vitals:** {finding}
- **Structured data:** {finding}
- **Mobile:** {finding}

## Next Actions
1. {specific fix}
2. {specific fix}
3. {specific fix}
```
