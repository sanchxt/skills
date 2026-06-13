# Brand Setup

## Purpose

Collect and organize all essential information about a brand/client to enable effective social media strategy. The brand profile is the foundation — every other action depends on it.

## Process

When setting up a new brand, collect information in manageable batches. Use Codex's native user-input tool when it is available and useful for constrained choices; otherwise ask concise plain chat questions. Don't overwhelm with all questions at once.

### Batch 1: Core Identity

Ask these first — they define who the brand is:

- **Brand name**: Official name and any common abbreviations or handles
- **Industry/Niche**: Primary industry and specific niche within it (e.g., "Fitness" → "Home workout equipment for busy professionals")
- **USP (Unique Selling Proposition)**: What makes this brand different? Why should anyone care? What's the one thing competitors can't claim?
- **Brand tone of voice**: How does the brand speak? Provide examples:
  - Professional but approachable
  - Witty, bold, and unapologetic
  - Warm, educational, and encouraging
  - Luxury, aspirational, and exclusive
  - Casual, fun, and relatable
  - Authoritative and data-driven
- **Brand colors**: Primary, secondary, and accent colors (hex codes if available)
- **Typography preferences**: Font style direction (serif for traditional/luxury, sans-serif for modern/clean, display for bold/creative, etc.)

### Batch 2: Target Audience

Ask these next — they define who we're talking to:

- **Demographics**: Age range, gender split, primary locations, income level, education level
- **Psychographics**: Interests, values, lifestyle, hobbies, beliefs
- **Pain points**: What problems does the audience have that the brand solves?
- **Aspirations**: What does the audience want to achieve or become?
- **Where they hang out online**: Which platforms, what accounts they follow, what content they consume
- **Content consumption habits**: Do they prefer short-form video, long-form text, carousels, stories, podcasts?

### Batch 3: Social Media Details

Ask these to define the execution parameters:

- **Active platforms**: Which platforms to focus on (Instagram, X/Twitter, LinkedIn, Facebook, TikTok, YouTube, etc.)
- **Social handles**: Current handles on each platform
- **Current follower counts**: Per platform (if existing accounts; "new account" if starting fresh)
- **Posting frequency goal**: How often per platform per week (be realistic)
- **Content type preferences**: What formats does the client prefer or have capacity to create?
  - UGC (user-generated content)
  - Carousels / slide decks
  - Reels / short-form video
  - Static image posts
  - Stories
  - Text-first posts / threads
  - Live sessions
  - Articles / long-form
- **Primary goal**: What's the #1 objective? (brand awareness, follower growth, engagement, leads, sales, community building)
- **Secondary goals**: Any other objectives
- **Timeline**: Any deadlines or milestones (e.g., "launch in 2 weeks", "hit 10K followers by Q3")

### Batch 4: Competitive Landscape

Ask these to map the playing field:

- **Direct competitors**: 3-5 brands competing for the same audience (names and social handles if known)
- **Aspirational brands**: Brands whose social media presence they admire (can be different industry)
- **Anti-inspirations**: Brands or content styles they explicitly do NOT want to be like, and why
- **Perceived competitive advantage**: What do they believe they do better than competitors on social?

## Brand Profile Template

After collecting all information, store it in `.growth/brand-profile.md`:

```markdown
# {Brand Name} — Brand Profile

**Created:** {date}
**Last Updated:** {date}

## Identity
- **Name:** {brand name}
- **Handles:** {platform: @handle, ...}
- **Industry:** {industry}
- **Niche:** {specific niche}
- **USP:** {unique selling proposition — one clear sentence}
- **Tone of Voice:** {description with examples of how the brand speaks}
- **Brand Colors:**
  - Primary: {color + hex}
  - Secondary: {color + hex}
  - Accent: {color + hex}
- **Typography:** {font style preferences and direction}

## Target Audience
- **Demographics:** {age, gender, location, income, education}
- **Psychographics:** {interests, values, lifestyle}
- **Pain Points:** {what problems they have — be specific}
- **Aspirations:** {what they want to achieve/become}
- **Online Behavior:** {platforms, times, accounts they follow, content preferences}

## Social Media
- **Platforms:** {list with handles and current follower counts}
- **Posting Frequency:** {per platform per week}
- **Content Types:** {preferred formats ranked by priority}
- **Primary Goal:** {#1 objective with timeline}
- **Secondary Goals:** {other objectives}

## Competitive Landscape

### Direct Competitors
| Competitor | Handles | Why They Compete |
|-----------|---------|-----------------|
| {name} | {handles} | {brief description} |

### Aspirational Brands
| Brand | Handles | What We Admire |
|-------|---------|---------------|
| {name} | {handles} | {what about their social we like} |

### Anti-Inspirations
- {brand/style}: {why we want to avoid this}

### Our Edge
{What we believe we do better — our angle}

## Notes
{Any additional context, constraints, preferences, or important details}
```

## Updating a Brand Profile

When the user wants to update an existing brand profile:

1. Read the existing `.growth/brand-profile.md`
2. Ask what they want to update, presenting the major profile sections as options when a selectable-question tool is available
3. Collect the new information
4. Update the relevant section(s) and change the "Last Updated" date
5. If competitors changed, flag that competitor research files may need refreshing
6. If audience or goals changed, flag that the content strategy may need revisiting

## Edge Cases

- **Multiple brands in one directory**: Not recommended. Each brand should have its own project directory with its own `.growth/` folder. If the user insists, use `.growth/{brand-name}/` subdirectories.
- **Brand pivot/rebrand**: Create a fresh profile but archive the old one as `.growth/brand-profile-archive-{date}.md` for reference.
- **Incomplete information**: It's OK to start with partial data. Note what's missing in the Notes section and flag it when those details become relevant (e.g., "We don't have competitor handles yet — needed before competitor research").
