# Content inventory: keep, refresh, merge, prune

## When

After a redesign, a change of positioning or services, a traffic drop, or once or twice a year. Google judges a site partly as a whole: a pile of thin, overlapping or off-topic pages holds back the good ones, and "Crawled / Discovered - currently not indexed" growing is often the symptom.

## Build the inventory

One row per URL, from every source:

1. Live sitemap (`curl -s https://site/sitemap.xml`).
2. Search Console: indexed list, every not-indexed reason, Performance pages over 16 months.
3. The CMS (all statuses, drafts included) or route files.
4. An internal-link crawl ([../scripts/crawl-internal-links.mjs](../scripts/crawl-internal-links.mjs)) to find linked URLs that 404.

Columns: URL · type · status code · indexed? · clicks / impressions / avg position (16 mo) · main query · topic/cluster · fits current offer? (yes/partly/no) · overlaps with · internal links in · backlinks (if known) · last updated · decision · target.

## Decide

| Decision | When | Action |
|----------|------|--------|
| **Keep** | Fits the offer, unique intent, indexed or improving | Leave it; make sure it's linked from the right hub/service page |
| **Refresh** | Fits the offer and has impressions (especially position 5-30), but is dated, thin or not indexed | Update facts and year, answer-first intro, add proof, fix internal links, update date. Keep the URL. |
| **Merge** | Two or more pages target the same intent | Fold the best parts into the strongest URL (most clicks/links), 301 the others to it |
| **Prune + redirect** | Off-offer, dated news, or thin, but it has impressions, clicks or links | Remove (trash/unpublish) and 301 to the closest relevant live page |
| **Prune (404/410)** | No traffic, no links, no close equivalent, never mattered | Remove and let it 404/410; remove internal links to it |
| **Noindex** | Useful to users but not to search (thank-you pages, filters, internal search) | `noindex,follow`, keep out of the sitemap |

Rules of thumb:

- Never delete a URL with clicks or backlinks without a 301.
- Redirect to the most relevant page, not the home page.
- Prefer refreshing a URL that has history over publishing a new one on the same topic.
- Unpublished drafts don't affect SEO; clean them up only for the team's sake.
- Dated "news" and monthly-recap posts rarely deserve to live on unless they still earn traffic.
- When the offer changed, content for services you still sell stays (refresh its angle and CTAs). Content for services you dropped goes.

## Execute safely

1. Write the inventory and redirect map to `.seo/inventory/YYYY-MM-DD.md` and get the user's approval for the prune/merge list.
2. Add the redirects in code or the server first (single hop, absolute targets that return 200), deploy, and verify each with curl.
3. Then trash/unpublish content through the CMS or CLI. Use recoverable delete (trash), not permanent delete, unless told otherwise.
4. Rewrite internal links that pointed to removed URLs so they point straight at the final targets.
5. Re-crawl the site for broken links, update the sitemap, then Search Console: resubmit the sitemap, validate the 404 group, request indexing for the refreshed key pages.
6. Log it in `.seo/insights.md` and re-check indexing in 2-4 weeks.

Watch for CMS traps: editing a post without sending its slug can regenerate the URL from the title. After any bulk edit, re-check the slugs and URLs.
