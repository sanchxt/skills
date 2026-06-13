# Competitor Research

## Purpose

Conduct deep competitive intelligence on competitor brands to extract actionable insights. This isn't surface-level follower counting — it's understanding WHY their content works, WHAT gaps they leave open, and HOW we exploit those gaps.

## Before Starting

1. Read `.growth/brand-profile.md` to get the list of competitors and understand the brand's positioning
2. Check `.growth/competitors/` for existing research — never redo work that's already captured
3. If research exists but is older than 30 days, offer to refresh it rather than starting from scratch
4. Load competitor handles/URLs from the brand profile

## Research Path Selection

Before starting research, ask the user:

> "Do you want me to research competitors directly with web search and Chrome DevTools MCP, or generate a deep research prompt for your preferred external research tool so you can get 10-20 pages of thorough competitive analysis?"

- **Direct research** -> Continue with the methodology below.
- **External research prompt** -> Read the [deep-research-prompt.md](deep-research-prompt.md) rule file and generate a "Competitor Landscape" prompt. Include all known competitor names from `.growth/brand-profile.md`, the brand's niche and positioning, and request the sub-topics listed in the Competitor Landscape template section of that rule file. Save the prompt and instruct the user.

## Research Methodology

For each competitor, execute these phases systematically.

### Phase 1: Profile Overview

Use Chrome DevTools MCP or the available browser automation surface to visit each competitor's social media profiles on every platform they're active on.

**Capture:**
- Follower/subscriber count
- Following count
- Total posts / content volume
- Bio/description (exact text — often reveals positioning)
- Link in bio (reveals their funnel strategy)
- Verification status
- Profile aesthetic (grid layout for Instagram, banner for LinkedIn/X/Facebook)
- Posting frequency (rough estimate from recent posts)

**How:**
1. Open the competitor's profile in Chrome.
2. Inspect page text, rendered content, screenshots, console output, and network requests as needed.
3. Scroll through the feed manually through the available browser-control surface when needed.
4. Repeat for each platform.

### Phase 2: Content Analysis

Analyze their last 15-20 posts across platforms. This is where the real intelligence comes from.

**For each post, note:**
1. **Content type**: Carousel, reel, static image, story highlight, text post, thread, article, etc.
2. **Topic/theme**: What content pillar does this fall under?
3. **Hook**: The first line of caption or first 3 seconds of video — capture the exact text
4. **Engagement**: Likes, comments, saves (if visible), shares (if visible), views (for video)
5. **Caption structure**: How long? What format? Does it tell a story, list tips, ask a question?
6. **CTA**: What action do they ask for? (save, share, comment, click link, follow, etc.)
7. **Visual style**: Colors, composition, text overlay style, photography vs graphic design
8. **Hashtags**: What hashtags do they use? How many?
9. **Posting time**: When was it posted? (if visible)

**Aggregate into:**
- **Content type breakdown**: What % is carousels, reels, static, text, etc.?
- **Posting frequency**: How often per platform per week?
- **Engagement rate**: (Total engagement / Followers) x 100 — calculate per post type
- **Content pillars**: What 3-5 themes do they consistently cover?

### Phase 3: Top Performers Deep Dive

Identify their 5 best-performing posts (highest engagement relative to their average) and deeply analyze each:

1. **What was the hook?** Copy the exact text. Why did it work? Which hook formula was used?
2. **What was the format?** Why was this format effective for this topic?
3. **What was the topic angle?** Was it contrarian? Educational? Emotional? Timely?
4. **What was the visual approach?** What made someone stop scrolling?
5. **What was the CTA?** Did it drive comments? Saves? Shares?
6. **Why did it outperform?** Your strategic analysis of why THIS post resonated
7. **How can WE adapt this?** Not copy — adapt with our brand's unique voice and angle

### Phase 4: Strategy Extraction

From all the data, extract strategic patterns:

**Hook Patterns:**
- What types of hooks do they rely on? (questions, bold statements, statistics, stories, controversy, humor)
- Which hook types get the most engagement?
- Copy their top 5 hooks verbatim as reference

**CTA Patterns:**
- How do they drive engagement? What specific asks work?
- Do they use different CTAs for different content types?

**Visual Identity:**
- Color palette and how they use it across posts
- Photography style vs graphic design ratio
- Text overlay approach (font, placement, amount of text)
- Grid/feed aesthetic (does the overall feed have a cohesive look?)
- Any signature visual elements (borders, templates, recurring design elements)

**Content Strategy:**
- Content pillar mix — how do they balance education, entertainment, promotion, community?
- Do they follow trends or set them?
- How do they handle promotional content? (hard sell vs soft sell vs value-first)
- Community engagement — do they reply to comments? How? What tone?

**Growth Tactics:**
- Collaborations or cross-promotions
- Giveaways or contests
- Trending audio/format usage
- User-generated content strategy
- Email/newsletter integration
- Cross-platform content repurposing

### Phase 5: Gap Analysis

This is the most valuable output. Identify exploitable opportunities:

1. **Content gaps**: Topics or angles they're NOT covering that our audience would value
2. **Format gaps**: Content types they're not using that perform well on the platform
3. **Audience gaps**: Segments of the audience they're not serving that we can
4. **Quality gaps**: Areas where their execution is weak (poor visuals, weak hooks, inconsistent posting)
5. **Platform gaps**: Platforms they're not on or underinvesting in
6. **Engagement gaps**: Are they bad at community management? Do they ignore comments?
7. **Positioning gaps**: Angles or USPs they're not claiming that we can own
8. **Timing gaps**: Are there posting times or days they're missing?

For each gap, define: what's the gap, why does it exist, and how specifically should we exploit it.

### Phase 6: Adaptable Strategies

For each competitor's winning strategy, create an "adapted version" for our brand:

- **Their approach**: What they do
- **Why it works**: The underlying principle
- **Our adaptation**: How we do it with our voice, audience, and positioning
- **Expected impact**: What we think this will do for us

## Competitor Research Template

Store each competitor in `.growth/competitors/{competitor-name}.md`:

```markdown
# {Competitor Name} — Competitive Analysis

**Researched:** {date}
**Platforms analyzed:** {list}

## Profile Overview

| Platform | Handle | Followers | Posts | Avg Engagement Rate |
|----------|--------|-----------|-------|-------------------|
| Instagram | @xxx | {count} | {count} | {rate}% |
| X/Twitter | @xxx | {count} | {count} | {rate}% |
| LinkedIn | {name} | {count} | {count} | {rate}% |
| Facebook | {name} | {count} | {count} | {rate}% |

**Bio/Positioning:** {their bio text and what it reveals about positioning}
**Link Strategy:** {what their link-in-bio points to}

## Content Strategy

- **Content Pillars:**
  1. {pillar} — {%} of content — {description}
  2. {pillar} — {%} of content — {description}
  3. {pillar} — {%} of content — {description}
  4. {pillar} — {%} of content — {description}

- **Posting Frequency:** {per platform per week}

- **Content Mix:**
  | Format | % of Content | Avg Engagement |
  |--------|-------------|----------------|
  | {type} | {%} | {avg} |

- **Best Posting Times:** {observed patterns}

## Top Performing Content

### 1. {Post description}
- **Platform:** {platform}
- **Type:** {format}
- **Hook:** "{exact hook text}"
- **Engagement:** {likes}/{comments}/{saves}
- **Why it worked:** {analysis}
- **How we adapt:** {our version with our voice}

### 2. {Post description}
{repeat structure}

### 3. {Post description}
{repeat structure}

### 4. {Post description}
{repeat structure}

### 5. {Post description}
{repeat structure}

## Hook Patterns
- **Most used:** {hook type} — "{example}"
- **Best performing:** {hook type} — "{example}"
- **Patterns:**
  - {pattern}: "{example}"
  - {pattern}: "{example}"
  - {pattern}: "{example}"

## CTA Patterns
- {CTA type}: "{example}" — used for {context}
- {CTA type}: "{example}" — used for {context}

## Visual Identity
- **Color scheme:** {description}
- **Photography style:** {description}
- **Graphic design style:** {description}
- **Text overlays:** {description}
- **Grid/feed aesthetic:** {description}

## Hashtag Strategy
- **Branded:** {list}
- **Niche:** {list}
- **Broad:** {list}
- **Avg hashtags per post:** {number}

## Growth Tactics
- {tactic 1}: {description}
- {tactic 2}: {description}

## Gaps & Opportunities
1. **{Gap type}:** {description} → **Our play:** {how we exploit it}
2. **{Gap type}:** {description} → **Our play:** {how we exploit it}
3. **{Gap type}:** {description} → **Our play:** {how we exploit it}

## Strategies to Adapt
1. **Their approach:** {what they do}
   **Why it works:** {principle}
   **Our adaptation:** {our version}

2. **Their approach:** {what they do}
   **Why it works:** {principle}
   **Our adaptation:** {our version}

## Key Takeaways
1. {takeaway — most important strategic insight}
2. {takeaway}
3. {takeaway}
```

## Refreshing Research

When refreshing existing competitor research:

1. Read the existing `.growth/competitors/{name}.md` file
2. Visit their profiles again via Chrome
3. Focus on what's CHANGED since last research:
   - New follower counts (calculate growth rate)
   - New top-performing posts
   - Strategy shifts (new content types, new pillars, rebranding)
   - New tactics they've adopted
4. Update the existing file — don't create a new one
5. Update the "Researched" date
6. Add a "Changes Since Last Research" section at the top noting what shifted

## Multi-Competitor Synthesis

After researching all competitors, create a synthesis in `.growth/insights.md` (or update the existing one) with:

- **Industry content benchmarks**: Average engagement rates, posting frequency, content mix across all competitors
- **Universal patterns**: What ALL competitors are doing (table stakes for the industry)
- **Differentiators**: What sets each apart
- **Biggest collective gap**: The opportunity NO competitor is addressing
- **Our strategic positioning**: How we differentiate from ALL of them, not just one
