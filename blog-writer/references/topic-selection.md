# Topic selection and the backlog

## Inputs

- Fresh keyword research from the `seo` skill (`.seo/keywords/master-list.md` and `research-*.md`, under 30 days old, or newer than the last site redesign).
- `.seo/audience.md` (segments, pains, language bank).
- The live post list (all statuses, from the project's CLI) and Search Console pages and queries.

## What makes a good blog topic

A blog post fits when the SERP shows guides, comparisons, how-tos, cost breakdowns or checklists ranking. If the SERP is all service or product pages, it's a landing-page job: note it for the `seo` skill and skip it here.

Prioritise topics that:
1. **Lead to a money page**: the reader's next step is a service the business sells.
2. **Match buyer stages**: cost/pricing, "X vs Y", "best way to", "is it worth", "how to choose", "examples of", "checklist", problem-aware pains.
3. **Are winnable now**: forums, small sites or thin/outdated pages in the top 10; GSC impressions at positions 8-30 that no page targets properly.
4. **Have rising or steady demand**: Trends and autocomplete presence, recent PAA questions.
5. **Fill a cluster**: support a service page with a set of linked posts, rather than one-off topics.

Skip: news that dates quickly, topics for a different audience, broad head terms the site can't rank for yet, anything a live post already covers (refresh that post instead).

## Scoring (0-5 each)

| Factor | Weight |
|--------|--------|
| Business fit (leads to a money page) | 30% |
| Buyer intent | 25% |
| Winnability today | 20% |
| Demand and trend | 15% |
| Cluster value (internal links in and out) | 10% |

## Dedupe

For each candidate: search the live post titles and slugs, run `site:{domain} {keyword}` on Google, and check GSC for pages already getting impressions for it. If one exists:
- it targets the same intent → `refresh` task on that URL (keep the slug);
- it's adjacent → a new post is fine, and link the two to each other.

## Backlog file: `.seo/content/backlog.md`

```markdown
# Blog backlog - {project}
**Refreshed:** {date}  **Research source:** {keyword research file + date}

| # | Status | Type | Primary keyword | Working title | Intent | Segment | Money page | Score | Evidence | Notes |
|---|--------|------|-----------------|---------------|--------|---------|------------|-------|----------|-------|
| 1 | queued | new | ... | ... | commercial | ... | /service/... | 4.3 | SERP: forums + 2 thin posts; GSC 40 impr @ pos 18 | |
| 2 | queued | refresh | ... | (existing) /blog/... | ... | | | 4.0 | pos 11, dated 2026 prices | |
```

Statuses: `queued` → `writing` → `published` (with URL and date) or `dropped` (with reason). Keep 8-15 queued topics. Re-score when the backlog is refreshed; re-verify the SERP for a topic right before writing it, since the backlog can be weeks old.
