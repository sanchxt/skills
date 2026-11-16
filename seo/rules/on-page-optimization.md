# On-Page Optimization

## Purpose

Optimize existing or planned pages for the keyword cluster and intent they should own. Recommendations must be implementable: title, meta description, headings, schema, content additions, images, URLs, and internal links.

## Before Starting

1. Read `.seo/project-profile.md`.
2. Read `.seo/keywords/master-list.md` or relevant cluster research.
3. Inspect the current live page when one exists.
4. Review current SERP results for the target keyword before recommending structure.
5. Pull the page's queries from Search Console (Performance, filter by page). Optimise for the queries it already gets impressions for, especially at positions 5-20, as well as the target keyword.

## Optimization Standards

- Title tag: unique, click-worthy, primary keyword near the front, usually under 60 characters.
- Meta description: unique, value-led, keyword included naturally, usually under 160 characters.
- H1: one per page, aligned with intent, not necessarily identical to title.
- Headings: clear hierarchy, covers required SERP subtopics, includes secondary terms naturally.
- URL: short, lowercase, hyphenated, keyword-relevant, stable.
- Content: satisfies intent quickly, covers must-have sections, includes proof and examples.
- Schema: choose by page type: Organization (with `sameAs`), WebSite, Service, LocalBusiness/ProfessionalService, Article/BlogPosting (with a real author), Product/SoftwareApplication, BreadcrumbList, VideoObject, Review only for genuine third-party reviews. Before promising a rich result, check Google's current structured-data docs: several types have been limited or dropped (FAQ rich results went to a narrow set of sites, HowTo rich results were removed). FAQPage markup can still help machines read the page, but don't sell it as a SERP feature. Markup must match visible content.
- Answer-first: the first paragraph (and each question-style H2) gives a direct 1-3 sentence answer that a snippet or AI answer could quote. See [geo-ai-search.md](geo-ai-search.md).
- Freshness: visible "Updated" date when the content really changed; current-year facts.
- Images: descriptive filenames, useful alt text, compressed, dimensions set, lazy loaded below fold.
- Internal links: 3-5 contextual outgoing links and recommended incoming links from relevant existing pages.
- Conversion path: CTA matches awareness stage and page type.

## Output Template

````markdown
## On-Page Optimization - {URL or Page}

**Target Keyword Cluster:** {cluster}
**Primary Keyword:** {keyword}
**Secondary/Long-Tail Keywords:** {keywords}
**Search Intent:** {intent}
**Recommended Page Type:** {type}

### Title Tag
- **Current:** {current}
- **Recommended:** {new} ({chars} chars)
- **Reason:** {why}

### Meta Description
- **Current:** {current}
- **Recommended:** {new} ({chars} chars)
- **Reason:** {why}

### H1 and Heading Structure
```text
H1: {heading}
H2: {section}
  H3: {subsection}
```

### Content Additions
- {section or paragraph to add}
- {proof/source/example/table/FAQ to add}

### Schema
```json
{recommended JSON-LD or schema notes}
```

### Internal Linking
| Direction | Page | Anchor Text | Reason |
|-----------|------|-------------|--------|
| To this page | {URL} | {anchor} | {reason} |
| From this page | {URL} | {anchor} | {reason} |

### Images
| Placement | Image Idea | Alt Text | Notes |
|-----------|------------|----------|-------|
| {section} | {idea} | {alt} | {format/size} |

### Implementation Priority
1. {highest-impact action}
2. {next action}
3. {next action}
````
