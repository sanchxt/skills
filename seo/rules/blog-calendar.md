# Blog Content Calendar

## Purpose

Plan a calendar that builds topical authority and captures high-intent search demand. A calendar without current keyword research is guessing.

## Before Starting

1. Read `.seo/project-profile.md`.
2. Read `.seo/keywords/master-list.md` and relevant cluster files.
3. Read `.seo/competitors/` and `.seo/insights.md` if present.
4. Check existing `.seo/content/calendar-*.md` for continuity.
5. If keyword research is missing or stale, perform or refresh keyword research first.

## Planning Rules

- Prioritize clusters that combine business value, ranking feasibility, and content depth.
- Include short-tail authority pages, long-tail quick wins, high-intent commercial posts, and supporting FAQs.
- Every planned article must have a target keyword, secondary keywords, intent, page type, target word count, internal links, and CTA.
- Build around 2-4 topic clusters per quarter unless the user asks for a smaller sprint.
- Publish pillar pages before or early in supporting content.
- Include refreshes of existing content when they are faster than new content.
- Leave reactive slots for trending keywords only when the niche changes quickly.

## High-Intent Mix

Each calendar should intentionally balance:

- **Quick wins:** low/moderate difficulty long-tail keywords.
- **Commercial posts:** best, vs, alternatives, pricing, reviews, templates, checklists.
- **Pillar content:** broad authority-building pages.
- **Support content:** FAQs, how-to guides, definitions, use cases.
- **Refreshes:** pages close to ranking or with decaying traffic.
- **Conversion support:** articles that internally link to service/product/demo/booking pages.

## Word Count Planning

Set each article's target word count from SERP analysis. Use these defaults only as starting points:

- Long-tail how-to: 1,200-2,500.
- Commercial comparison: 2,000-3,500.
- Best/list article: 2,000-4,500.
- Pillar guide: 3,000-6,000+.
- Local article/service support: 800-1,800.
- Refresh/update: scope depends on gap analysis.

## Output Template

Store in `.seo/content/calendar-{YYYY-QN}.md`:

```markdown
# Blog Content Calendar - {Quarter} {Year}

**Project:** {project}
**Created:** {date}
**Publishing Cadence:** {cadence}
**Primary Goal:** {goal}

## Strategy
- **Focus clusters:** {clusters}
- **Quick wins:** {topics}
- **Commercial/high-intent priorities:** {topics}
- **Pillar pages:** {topics}
- **Refresh priorities:** {URLs}

## Calendar
| Date | Title | Primary Keyword | Intent | Type | Word Count | Cluster | CTA | Priority |
|------|-------|-----------------|--------|------|------------|---------|-----|----------|
| {date} | {title} | {keyword} | {intent} | {type} | {count} | {cluster} | {CTA} | {Now/Next} |

## Article Details
### {Title}
- **Primary keyword:** {keyword}
- **Secondary/long-tail keywords:** {keywords}
- **SERP intent:** {intent}
- **Target word count:** {count and rationale}
- **Content angle:** {differentiation}
- **Internal links from this article:** {URLs}
- **Existing pages that should link to it:** {URLs}
- **Brief status:** {needed/created}
- **Expected outcome:** {traffic/leads/rankings/authority}

## Internal Linking Plan
| New/Updated Page | Links To | Anchor Text | Direction |
|------------------|----------|-------------|-----------|
| {page} | {target} | {anchor} | {to/from/both} |

## Measurement Plan
- Rankings to track: {keywords}
- Conversion events: {events}
- Review cadence: {weekly/monthly}
```
