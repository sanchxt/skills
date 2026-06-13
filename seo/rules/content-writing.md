# Content Writing

## Purpose

Create SEO briefs and full articles that can rank, satisfy search intent, and convert qualified readers. Do not write from generic knowledge alone. Every serious article must be driven by current SERP analysis and keyword research.

## Before Starting

1. Read `.seo/project-profile.md`.
2. Read `.seo/keywords/master-list.md` or the relevant cluster file.
3. Read an existing `.seo/content/briefs/{slug}.md` when present.
4. Read `.growth/brand-profile.md` and `.growth/voice-library.md` if available.
5. If there is no brief, create one first or create it inline before drafting.

## Mandatory SERP Analysis

Before writing a brief or article, research the current SERP for the primary keyword and 2-5 close variants:

- Analyze top 5-10 ranking pages.
- Identify the dominant content type and intent.
- Estimate word count range and content depth.
- Capture common H2/H3 subtopics.
- Capture PAA questions and snippet formats.
- Note SERP features: featured snippet, video, images, local pack, product results, forums.
- Identify gaps: outdated stats, weak examples, missing steps, poor UX, no original data, shallow explanations, no buyer guidance.
- Decide the content angle that makes the piece better than what ranks now.

If the SERP is mostly transactional or commercial landing pages, do not force a blog post. Recommend the matching page type.

## High-Intent Content Standards

Prioritize content that can move a reader toward a valuable action:

- Include a clear target persona and problem.
- Map sections to awareness stage: problem-aware, solution-aware, product-aware, or ready to buy.
- Include comparison, pricing, selection criteria, use cases, mistakes, examples, templates, checklists, or decision frameworks where intent calls for them.
- Add internal CTAs naturally, not as filler.
- Connect informational articles to commercial pages through internal links.

## Word Count Guidance

Set word count from SERP depth and intent, not a fixed rule:

| Content Type | Typical Range |
|--------------|---------------|
| Definition/glossary | 800-1,500 words |
| How-to guide | 1,500-3,000 words |
| Commercial comparison | 2,000-3,500 words |
| Best/list article | 2,000-4,500 words |
| Pillar/ultimate guide | 3,000-6,000+ words |
| Case study | 1,200-2,500 words |
| Local service page | 800-1,800 words |
| Product/category SEO page | 700-1,500 words plus supporting FAQs |

Exceed competitors only when added depth improves usefulness. Do not pad.

## Brief Requirements

Every brief must include:

- Primary keyword, secondary keywords, long-tail keywords, and PAA questions.
- Search intent and awareness stage.
- Recommended page type.
- Target word count with reason.
- SERP summary from current top results.
- Required sections and optional sections.
- Featured snippet target format.
- Internal links to include and pages that should link back.
- External sources to cite.
- Differentiated angle.
- E-E-A-T requirements: author notes, proof, sources, screenshots, examples, original data, or expert input.
- Conversion path or CTA.

## Article Structure

Use this baseline, adapted to SERP intent:

```markdown
---
title: "{SEO title under 60 characters when possible}"
description: "{Meta description under 160 characters}"
slug: "{keyword-focused-slug}"
date: "{YYYY-MM-DD}"
last_updated: "{YYYY-MM-DD}"
author: "{author}"
target_keyword: "{primary keyword}"
secondary_keywords:
  - "{keyword}"
long_tail_keywords:
  - "{keyword}"
search_intent: "{intent}"
awareness_stage: "{stage}"
cluster: "{cluster}"
target_word_count: {count}
---

# {H1 with primary keyword or close variant}

{Intro that names the problem, matches intent, includes the primary keyword naturally in the first 100 words, and explains what the reader will get.}

## {Main section}

{Answer directly, then expand.}

## {Main section}

{Use examples, data, tables, screenshots, or steps where useful.}

## FAQs

### {PAA question}

{Direct answer in 40-60 words when targeting snippets.}

## Conclusion

{Summarize the decision/action and include a relevant CTA.}
```

## Keyword Use

- Primary keyword: title, H1 or close variant, first 100 words, at least one H2 where natural, conclusion, slug.
- Secondary keywords: section headings and body copy where they fit.
- Long-tail keywords: FAQs, H2/H3s, examples, and subtopics.
- Avoid keyword stuffing. If a sentence sounds unnatural, rewrite it.
- Use semantic terms and entity coverage that top SERP pages demonstrate.

## Quality Bar

Before delivering, verify:

- The content type matches the SERP.
- The article answers the primary query quickly.
- The outline covers must-have subtopics from current top results.
- There is at least one differentiated asset or angle.
- The piece includes E-E-A-T signals.
- Metadata is click-worthy and within practical limits.
- Internal links support topic clusters and conversion paths.
- External citations are authoritative and current.
- Headings form a clean hierarchy.
- The CTA matches intent.

## Content Brief Template

Store briefs in `.seo/content/briefs/{slug}.md`:

```markdown
# Content Brief: {Title}

**Primary Keyword:** {keyword}
**Secondary Keywords:** {list}
**Long-Tail Keywords:** {list}
**Questions/PAA:** {list}
**Search Intent:** {intent}
**Awareness Stage:** {stage}
**Recommended Page Type:** {page type}
**Target Word Count:** {count and rationale}
**Target Audience:** {audience}
**Cluster:** {cluster}

## SERP Analysis
| Ranking Page | Type | Strengths | Weaknesses | Notes |
|--------------|------|-----------|------------|-------|
| {URL} | {type} | {strength} | {gap} | {note} |

## Content Angle
{Why our page can be better or more useful than current ranking pages.}

## Required Outline
1. {H2} - {what to cover and keywords to include}
2. {H2} - {what to cover and keywords to include}

## Featured Snippet / PAA Targets
| Question | Answer Format | Placement |
|----------|---------------|-----------|
| {question} | {paragraph/list/table} | {section} |

## Internal Links
| Link To | Anchor Text | Purpose |
|---------|-------------|---------|
| {URL} | {anchor} | {pillar/conversion/supporting} |

## Sources
- {source}

## CTA
{Conversion path appropriate to intent.}
```
