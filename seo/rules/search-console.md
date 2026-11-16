# Search Console and Bing Webmaster Tools

## Purpose

Find out what search engines actually crawl, index, rank and show for the site, then fix the causes. This is the highest-signal data you have: start here before keyword research or writing.

## Access

1. Open a background tab with Chrome DevTools MCP: `https://search.google.com/u/0/search-console`. If the property isn't there, try `/u/1/`, `/u/2/`... and confirm the account email in the header. Note the working slot and property type (URL-prefix `https://site.com/` or domain `sc-domain:site.com`) in `.seo/project-profile.md`.
2. Report URLs (replace `{u}` and `{rid}` with the slot and URL-encoded property):
   - Overview `https://search.google.com/u/{u}/search-console?resource_id={rid}`
   - Performance `.../performance/search-analytics?resource_id={rid}&num_of_months=3` (add `&breakdown=page` for pages)
   - Page indexing `.../index?resource_id={rid}`; indexed list `.../index/drilldown?resource_id={rid}&pages=ALL_URLS`
   - Sitemaps `.../sitemaps?resource_id={rid}`, Removals `.../removals?...`, Links `.../links?...`, Core Web Vitals `.../core-web-vitals?...`
   - URL Inspection has no stable deep link: type the URL into the top "Inspect any URL" box and press Enter.
3. GSC is a single-page app with several hidden `[role=main]` panels. Read the **visible** one; extraction scripts are in [../scripts/gsc-snippets.md](../scripts/gsc-snippets.md). Tables default to 10 rows: switch "Rows per page" to 100+ or page through.
4. Bing Webmaster Tools: `https://www.bing.com/webmasters`. If the site isn't verified there, suggest importing it from GSC (one click for the user). Bing matters beyond Bing itself: Copilot and several AI assistants ground answers in Bing's index.
5. Save raw pulls to `.seo/gsc/YYYY-MM-DD/` (performance.md, indexing.md, ai.md).

## What to pull every time

- **Performance, last 3 months and last 28 days:** totals, top queries (clicks, impressions, CTR, position), top pages, countries, devices. Compare to the previous period.
- **Page indexing:** indexed count, every "why not indexed" reason with its URL list.
- **Sitemaps:** status, last read, discovered count vs URLs actually in the live sitemap.
- **AI / generative reports:** Search Console has a separate generative-AI performance view (AI Overviews, AI Mode, Discover AI) that is rolling out gradually. Look for it in the Performance section or a banner. If it isn't available for this property, say so. Bing WMT has an "AI Performance" report (Copilot citations, grounding queries, cited pages).
- **Manual actions and security issues:** must be empty.
- **Links:** top linked pages and linking sites (sanity check; not a backlink tool).

## Diagnosing indexing reasons

| Reason | Usually means | Fix |
|--------|---------------|-----|
| Not found (404) | Deleted, renamed or mistyped URL that is still linked or remembered | If the URL ever had value or links, 301 it to the closest live page. Fix internal links that point to it. Then "Validate fix". A 404 for junk that was never real can stay 404. |
| Soft 404 | Thin or empty page, or a redirect to an irrelevant page | Add real content, return a real 404/410, or redirect to a truly equivalent page |
| Alternate page with proper canonical tag | Parameter or duplicate URLs (`?tag=`, `?ref=`, `?utm_`) correctly canonicalised | Usually fine. Act only if a real page is wrongly canonicalised elsewhere. |
| Duplicate, Google chose different canonical | Near-duplicate pages, or canonical/internal-link signals conflict | Consolidate content, align canonical, internal links and sitemap on one URL |
| Page with redirect | URL redirects | Fine if intended. Make sure the sitemap and internal links use the final URL. |
| Crawled - currently not indexed | Google saw it and judged it not worth indexing yet: thin, overlapping, low value, weak internal links, or a site-wide quality/trust deficit | Improve or merge the page, add internal links from strong pages, prune weak siblings. Requesting indexing alone rarely helps. |
| Discovered - currently not indexed | Google knows the URL but hasn't crawled it: low crawl priority, too many low-value URLs, new site | Strengthen internal links from crawled pages, keep sitemaps clean, cut URL bloat, request indexing for the most important few |
| Excluded by noindex / Blocked by robots.txt | Intentional or a mistake | Confirm intent; remove the directive if the page should rank |
| Server error (5xx) / Redirect error | Hosting or redirect-loop problems | Fix immediately; check server logs |

For each important URL, use URL Inspection to see the last crawl, referring pages, the user-declared vs Google-selected canonical, and a live test.

## Reading performance data

- **Striking distance:** queries at average position 5-20 with impressions are the fastest wins. Improve the ranking page (title, intro answer, sections, internal links) rather than writing a new page.
- **CTR gaps:** pages with impressions and position under 10 but low CTR need better titles and descriptions.
- **Wrong page ranking:** if a query lands on a blog post but the commercial page should rank (or the reverse), fix internal links, anchors and on-page focus. Merge if two pages compete for one intent (cannibalisation).
- **Junk and test queries:** long operator-laden queries (`"x" -site:reddit.com ...`) come from scrapers and AI tools. Ignore them for demand, but note them as signs that LLM pipelines are fetching your pages.
- **Conversational queries** (full questions, "is X a good choice for...") show what people ask AI-style; feed them into keyword research and FAQs.
- **Brand queries** (name plus misspellings): track as a brand-demand metric.

## Actions inside Search Console

Ask the user once for a described batch, then do it:

- **Sitemaps:** resubmit after big changes. Remove sitemaps that no longer exist. One sitemap index is enough for small sites.
- **Validate fix:** only after the fix is live and verified with curl. It starts a re-crawl of that issue group and takes days to weeks.
- **Request indexing:** for the most important new or changed URLs only. There is a small daily quota (about 10). Use it for money pages, not every post. Requesting again does not move a URL up the queue.
- **Removals:** temporary hiding only (about 6 months). Use it for urgent private or sensitive leaks, never as a substitute for 301/404/noindex.
- **Change of address:** only for domain moves.

Always verify the live fix first: `curl -s -o /dev/null -w "%{http_code} %{redirect_url}" URL` for each affected URL.

## After a redesign

1. Export every URL Google knows: the indexed list, every not-indexed reason list, and Performance pages over 16 months.
2. Check each one live (status plus redirect target) and against the new sitemap.
3. Any old URL with impressions, clicks or backlinks gets a single-hop 301 to its closest new equivalent. Never chain redirects, and don't send everything to the home page (Google treats that as a soft 404).
4. Make sure no internal link, sitemap entry or canonical points to an old URL.
5. Resubmit the sitemap, validate the 404 group, request indexing for the key new pages, then re-check in 1-2 weeks.

## Output

Save `.seo/gsc/YYYY-MM-DD/indexing.md` and `performance.md` with raw tables, then an action list:

```markdown
## Search Console review - {date}
**Property:** {property} (account slot /u/{n}/)
**Indexed / not indexed:** {n} / {n}  **Clicks / impressions (3 mo):** {n} / {n}  **Avg position:** {n}

| Priority | Issue | URLs | Cause | Fix | Status |
|----------|-------|------|-------|-----|--------|
```
