# Keyword Research

## Purpose

Find the searches and AI prompts that real buyers use right now, classify them (short-tail, long-tail, questions, commercial, local, conversational), cluster them by intent, and decide which page should own each cluster. The output is a prioritised map of pages, not a long list of words.

## Before starting

1. Read `.seo/project-profile.md`. Confirm the current offer, audience and geography against the live site. If the business has repositioned, old keyword files are history, not input.
2. Read `.seo/keywords/master-list.md` and check its date. Older than 30 days, or older than the last redesign: refresh it.
3. Pull fresh Search Console queries (last 3 and 16 months) before anything else ([search-console.md](search-console.md)). They show what Google already associates with the site.

## Sources, in order of trust

Record every source and date in `.seo/keywords/research-YYYY-MM-DD.md`.

1. **The site's own Search Console queries:** real demand with real positions. Mine striking-distance queries (position 5-20), conversational questions and unexpected topics.
2. **Live Google results (Chrome DevTools MCP):** search each seed in a fresh tab with the target country and language (`https://www.google.com/search?q=...&gl=in&hl=en`). Capture: page types ranking, who ranks, AI Overview present and which sources it cites, People Also Ask (expand a few to load more), "People also search for", related searches, local pack, video/forum results.
3. **Google Autocomplete:** [../scripts/autocomplete.mjs](../scripts/autocomplete.mjs) expands seeds with a-z, question words and modifiers through Google's public suggest endpoint (set `gl`/`hl`). Fast and current. Long seeds often return nothing; use 2-3 word seeds with `--deep`.
4. **Google Trends (`trends.google.com`, via Chrome):** compare 2-5 phrasings in the target geography over 12 months and 5 years; read Rising related queries; note seasonality. Use it to choose wording ("AI chatbot" vs "AI agent" vs "AI assistant") and to spot rising topics.
5. **AI engines as research tools:** ask ChatGPT / Perplexity / Gemini how a buyer would phrase the problem, what they'd compare, and which brands they'd recommend. Treat this as phrasing ideas and a competitor list, not volume data.
6. **Communities:** Reddit, Quora, niche forums, YouTube comments, LinkedIn posts. Search `site:reddit.com {topic}` on Google, and the sites themselves. Copy real phrasing, objections and price questions.
7. **Competitors:** their service pages, blog categories, titles and FAQs (see [competitor-seo.md](competitor-seo.md)).
8. **Paid tools, if the user has them** (Ahrefs, Semrush, Google Keyword Planner via the user's Ads account, Bing Keyword Research in Bing WMT): use them for volume and difficulty. If you're working in the user's signed-in browser, use what's there; never sign up or enter payment details.

Without a paid tool, estimate and label:

- **Demand:** very low / low / medium / high, from autocomplete presence, Trends interest, GSC impressions, PAA density, ads on the SERP.
- **Difficulty:** easy / moderate / hard / very hard, from who ranks (forums and small sites = easier; big brands, directories, marketplaces = harder), content quality and freshness, and SERP features crowding the page.
- **Evidence:** one line on why.

Never present a guessed number as a measured search volume.

## Keyword types to cover

- **Short-tail / head terms:** broad, high demand, hard ("AI automation agency"). Usually targeted by the home or pillar pages, for the long term.
- **Long-tail:** specific, clearer intent, easier ("WhatsApp AI chatbot for clinics in India"). Usually the fastest wins.
- **Question keywords:** PAA, "how / what / why / is / can / should". Feed FAQs, H2s and answer-first sections.
- **Conversational / AI-prompt queries:** full-sentence asks, the way people talk to ChatGPT or AI Mode ("what's the cheapest way to automate appointment reminders for my salon?"). Often visible in GSC as long queries. Target with answer-first sections and the GEO prompt panel.
- **Commercial investigation:** best, top, vs, alternatives, reviews, pricing, cost, comparison.
- **Transactional:** hire, agency, company, services, near me, quote, consultant.
- **Local:** city, region, "near me", when the business serves a location.
- **Problem-aware:** symptoms and pains ("missed calls losing customers", "too much manual data entry").
- **Brand and competitor:** brand plus misspellings; competitor alternatives, only where fair and accurate.

## Workflow

1. **Seeds:** from the offer (each service, the problems it fixes, the industries served), GSC queries, and competitors.
2. **Expand:** autocomplete, PAA, related searches, Trends rising queries, communities.
3. **Validate intent on the live SERP** for every candidate priority term: what page type ranks, whether an AI Overview answers it outright (informational queries with full AI answers send fewer clicks, so favour terms where buyers still click: commercial, local, tool or provider choices), and whether the business can credibly produce the best page.
4. **Cluster by SERP overlap:** if two keywords show mostly the same top results, they belong on one page. One page per intent cluster.
5. **Map to pages:** existing URL (refresh/optimise) or new page (service page, comparison, guide, tool, location page). Note cannibalisation.
6. **Score and prioritise:**

| Factor | Weight |
|--------|--------|
| Business relevance (sells a current service) | 30% |
| Conversion intent | 25% |
| Ranking feasibility for this site today | 20% |
| Demand and trend direction | 15% |
| Effort / readiness | 10% |

Labels: **Now** (high value, feasible, can ship soon) · **Next** (needs supporting content or authority) · **Later** (head terms, authority plays) · **Skip** (off-offer, weak intent, unwinnable).

## Output

`.seo/keywords/research-YYYY-MM-DD.md` (raw findings and sources) and an updated `.seo/keywords/master-list.md`:

```markdown
# {Project} - Keyword Map
**Last updated:** {date}  **Geography/language:** {geo}  **Sources:** {GSC, Google SERP (gl=..), Autocomplete, Trends, ...}

## Summary
- Biggest opportunity: ...
- Quick wins (striking distance / long-tail): ...
- Long-term plays: ...
- Dropped from previous research and why: ...

## Clusters
### {Cluster} -> {target URL or new page type}
- Intent: ...  Page type ranking now: ...  AI Overview: {yes/no, cites ...}
| Keyword | Type | Intent | Demand (est.) | Difficulty | Evidence | Priority |
|---------|------|--------|---------------|------------|----------|----------|

## Question / prompt bank
| Question or prompt | Source | Use (FAQ / H2 / new page / GEO panel) |

## Trends notes
| Terms compared | Geo, period | Winner / direction | Decision |
```
