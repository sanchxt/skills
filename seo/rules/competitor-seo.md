# Competitor SEO Analysis

## Purpose

Identify which domains currently win the SERPs we care about, why they win, where they are weak, and how to beat them with better pages, clusters, technical execution, and links.

## Before Starting

1. Read `.seo/project-profile.md`.
2. Read `.seo/keywords/master-list.md` if present.
3. Check existing `.seo/competitors/`.
4. If SEO competitors are unknown, identify them from current SERPs, not only business intuition.

## Research Workflow

### 1. Identify Search Competitors

- Search the top target keywords.
- Record recurring domains in top 10 results.
- Separate direct business competitors from SEO competitors.
- Choose 3-5 primary SEO competitors.

### 2. Keyword and Content Gaps

For each competitor, inspect:

- Blog/resource categories.
- Service/product/category pages.
- Ranking content formats.
- Topics they cover that we do not.
- Keywords where our content exists but is weaker.
- Keywords where forums, old pages, or thin content rank.

### 3. Content Quality Benchmark

Review top pages for:

- Intent match.
- Word count and depth.
- Heading structure.
- Freshness.
- Examples, screenshots, data, tools, templates, and media.
- E-E-A-T signals.
- Internal links and conversion paths.
- Schema and SERP features.

### 4. Backlink and Authority Signals

Research:

- Who cites, mentions, interviews, lists, or links to competitors.
- Their linkable assets.
- Guest posts, PR, podcasts, studies, tools, and resource pages.
- Link gaps that are relevant and ethical to pursue.

### 5. SERP Feature Opportunities

Capture:

- Featured snippets.
- People Also Ask.
- Local packs.
- Image/video packs.
- Product/shopping features.
- Forums or community results.

Recommend the format needed to win each opportunity.

## Output Template

Store per-competitor analysis in `.seo/competitors/{competitor-domain}.md` and update `.seo/insights.md` for synthesis.

```markdown
# {Competitor Domain} - SEO Analysis

**Analyzed:** {date}
**Domain:** {domain}
**Competitor Type:** {direct business/search/content/local}

## Overview
- **Authority level:** {low/medium/high/very high}
- **Primary ranking formats:** {formats}
- **Content strengths:** {strengths}
- **Content weaknesses:** {weaknesses}

## Keyword / Topic Gaps
| Topic or Keyword | Their Page | Intent | Our Status | Recommended Action |
|------------------|------------|--------|------------|--------------------|
| {keyword} | {URL} | {intent} | {missing/weak/strong} | {create/update/skip} |

## Pages To Beat
| Competitor Page | Why It Ranks | Weakness | Our Angle |
|-----------------|--------------|----------|-----------|
| {URL} | {reason} | {gap} | {angle} |

## Backlink Opportunities
| Source | Links/Mentions | Why Relevant | Action |
|--------|----------------|--------------|--------|
| {site} | {competitor/page} | {reason} | {pitch/asset/PR} |

## SERP Feature Opportunities
| Keyword | Current Feature Owner | Format | How We Compete |
|---------|----------------------|--------|----------------|
| {keyword} | {domain} | {snippet/PAA/video/local} | {plan} |

## Action Items
1. {specific action}
2. {specific action}
3. {specific action}
```
