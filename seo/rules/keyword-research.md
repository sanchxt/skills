# Keyword Research

## Purpose

Research, classify, cluster, and prioritize keywords using current search behavior. The output must identify terms that can realistically rank and drive business outcomes, not just a long keyword list.

## Before Starting

1. Read `.seo/project-profile.md` for niche, geography, audience, competitors, seed topics, and goals.
2. Read `.seo/keywords/master-list.md` and relevant cluster files if they exist.
3. Treat keyword research older than 30 days as stale for active campaigns.
4. Use `.growth/brand-profile.md` when available for audience language and positioning.
5. Ask for missing target geography, product/service focus, and conversion goal if absent.

## Mandatory Current Research

Do not invent keyword demand. Use current research sources available in the session:

- Google SERPs through Chrome DevTools MCP, Chrome plugin, browser automation, or web browsing.
- Google Autocomplete, People Also Ask, Related Searches, and SERP features.
- Google Trends at `trends.google.com` for seasonality, geography, rising queries, and term comparisons.
- Competitor pages and `site:` searches.
- Public keyword lists, forums, Reddit, Quora, YouTube suggestions, marketplace/category pages, and industry glossaries where relevant.
- User-provided Search Console, Analytics, Ahrefs, Semrush, Moz, Screaming Frog, or CSV exports when available.

When paid metric data is unavailable, use ranges and labels:

- **Estimated volume:** very low, low, medium, high, very high.
- **Difficulty:** easy, moderate, hard, very hard.
- **Evidence:** SERP quality, domain strength of ranking pages, freshness, content depth, forum presence, weak pages ranking, local pack, ads, and SERP volatility.

## Keyword Types To Capture

Every serious keyword set must include:

- **Short-tail keywords:** broad head terms, usually high volume and high difficulty.
- **Long-tail keywords:** specific queries with clearer intent and easier ranking paths.
- **Question keywords:** People Also Ask and natural-language queries.
- **Commercial investigation keywords:** "best", "top", "reviews", "vs", "alternatives", "pricing", "comparison".
- **Transactional keywords:** "buy", "book", "hire", "near me", "service", "consultant", "software", "tool", "demo".
- **Local keywords:** city, region, "near me", and service-area modifiers when relevant.
- **Problem-aware keywords:** symptoms, pains, use cases, mistakes, templates, checklists.
- **Competitor/alternative keywords:** only when ethically and legally appropriate.

## Research Workflow

### 1. Seed Expansion

Start with the user's seed topics and expand with:

- Autocomplete variants: `{seed} a-z`, `best {seed}`, `{seed} for {audience}`, `{seed} vs`, `how to {seed}`, `what is {seed}`, `{seed} cost`, `{seed} near me`.
- PAA questions from multiple seed SERPs.
- Related Searches from Google.
- Competitor blog/category/page titles.
- Forums and community language.
- Google Trends related topics and rising queries.

### 2. SERP Intent Validation

For every priority keyword, review the current SERP. Record:

- Dominant content type: landing page, product page, category page, blog post, guide, listicle, comparison, local pack, video, tool, forum thread.
- Dominant intent: informational, navigational, commercial investigation, transactional, local, mixed.
- SERP features: featured snippet, PAA, local pack, shopping, video, image pack, AI/overview features if visible, forums.
- Ranking page quality and freshness.
- Whether the keyword should target a new page, existing page, brief, article, product/category page, or local page.

If the SERP intent conflicts with the user's assumed content type, say so and recommend the page type that matches the SERP.

### 3. Google Trends Review

Use Trends when comparing terms, choosing terminology, checking seasonality, or validating "current active keywords":

- Compare 2-5 close keyword variants.
- Set the correct geography and timeframe.
- Note rising vs declining terms.
- Capture seasonal peaks and publishing lead time.
- Use related queries/topics to find emerging long-tail opportunities.

### 4. Clustering

Cluster by shared intent and SERP overlap, not by superficial wording. One page should target one intent cluster.

For each cluster, identify:

- Pillar keyword.
- Supporting long-tail keywords.
- High-intent terms.
- PAA/question set.
- Required page type.
- Existing URL or planned URL.
- Internal links to and from related pages.

### 5. Prioritization

Score each keyword or cluster:

| Factor | Weight |
|--------|--------|
| Business relevance | 30% |
| Conversion/high-intent potential | 25% |
| Ranking opportunity | 20% |
| Search demand/trend | 15% |
| Content or technical readiness | 10% |

Priority labels:

- **Now:** high business value, clear intent, plausible ranking path, can be executed soon.
- **Next:** useful but needs supporting content, links, or site improvements.
- **Later:** authority-building or difficult head terms.
- **Skip:** weak intent, poor fit, too broad, misleading, or not commercially useful.

## Output Template

Store the master output in `.seo/keywords/master-list.md`:

```markdown
# {Project Name} - Master Keyword Research

**Last Updated:** {date}
**Target Geography:** {geo}
**Sources Used:** {Google SERP, Trends, competitor pages, exports, etc.}

## Executive Summary
- **Highest-value opportunity:** {cluster/keyword}
- **Fastest quick wins:** {keywords}
- **Long-term authority plays:** {clusters}
- **Terms to avoid:** {keywords and why}

## Priority Keywords
| Keyword | Type | Intent | Est. Demand | Difficulty | Business Value | Priority | Target Page |
|---------|------|--------|-------------|------------|----------------|----------|-------------|
| {keyword} | {short-tail/long-tail/question/commercial/transactional/local} | {intent} | {range} | {level} | {1-5} | {Now/Next/Later/Skip} | {URL/new page} |

## Topic Clusters
### {Cluster Name}
- **Pillar keyword:** {keyword}
- **Intent:** {intent}
- **Recommended page type:** {page type}
- **Primary URL:** {existing/planned}
- **Why this matters:** {business case}

| Keyword | Type | Intent | Priority | Use |
|---------|------|--------|----------|-----|
| {keyword} | {type} | {intent} | {priority} | {H2/FAQ/article/page} |

## People Also Ask / Question Bank
| Question | Source Keyword | Intent | Recommended Use |
|----------|----------------|--------|-----------------|
| {question} | {keyword} | {intent} | {FAQ/H2/brief/article} |

## Trends Notes
| Compared Terms | Winner | Trend/Seasonality | Action |
|----------------|--------|-------------------|--------|
| {terms} | {term} | {note} | {recommendation} |

## Competitor Gaps
| Keyword/Topic | Competitor Ranking Page | Our Status | Action |
|---------------|-------------------------|------------|--------|
| {keyword} | {URL} | {missing/weak/existing} | {create/update/skip} |
```
