# Trend Research

## Purpose

Research current trends across all relevant angles to inform content strategy and capitalize on timely opportunities. Trends are the difference between content that's relevant and content that's invisible.

## Before Starting

1. Read `.growth/brand-profile.md` for industry/niche context and target audience
2. Check `.growth/trends/` for existing trend research this month
3. If current month's research exists, ask the user if they want a full refresh or just an update
4. Read `.growth/competitors/` to understand what competitors are doing with trends

## Research Path Selection

Before starting research, ask the user:

> "Do you want me to research trends directly with web search and Chrome DevTools MCP, or generate a deep research prompt for your preferred external research tool so you can get 10-20 pages of thorough trend analysis?"

- **Direct research** -> Continue with the methodology below.
- **External research prompt** -> Read the [deep-research-prompt.md](deep-research-prompt.md) rule file and generate an "Industry Trends" prompt. Include the brand's niche, target audience, active platforms, and known competitors from `.growth/brand-profile.md`. Request the sub-topics listed in the Industry Trends template section of that rule file. Save the prompt and instruct the user.

## Research Methodology

Research trends from ALL four angles. Use Codex web search, page fetching/opening, and Chrome DevTools MCP aggressively when current information matters.

### 1. Broad Industry & Platform Trends

These are macro-level shifts that affect everyone on social media.

**Research:**
- Recent algorithm changes on Instagram, LinkedIn, X/Twitter, Facebook
- Platform feature updates (new post types, reach changes, monetization changes)
- Content format shifts (which formats are getting boosted right now?)
- General social media marketing trends and shifts
- Changes in consumer behavior and attention patterns

**Search queries to execute:**
- `"{platform} algorithm update {current month} {current year}"`
- `"social media trends {current month} {current year}"`
- `"what's working on {platform} {current year}"`
- `"{platform} reach changes {current year}"`
- `"social media marketing trends {current quarter} {current year}"`

**Sources to check via web search or page fetching:**
- Social Media Today, Social Media Examiner, Later Blog, Hootsuite Blog
- Platform official blogs (Instagram @creators, LinkedIn blog, X/Twitter blog)
- Marketing newsletters and industry publications

### 2. Niche-Specific Trends

These are trends within the brand's specific industry/niche.

**Research:**
- Industry news and developments
- Emerging topics, debates, or conversations in the niche
- Consumer sentiment shifts — what's the audience worried about, excited about, talking about?
- New products, technologies, or approaches in the space
- Thought leadership shifts — what are industry influencers saying?

**Search queries to execute:**
- `"{industry/niche} trends {current month} {current year}"`
- `"{niche} news this week"`
- `"trending topics in {industry} {current year}"`
- `"{niche} consumer trends {current year}"`
- `"what {target audience} are talking about {current year}"`

### 3. Platform-Specific Trends

What's specifically trending on each platform the brand uses. This requires platform-native research.

**Instagram:**
- Use Chrome to browse the Explore page and trending Reels
- Trending audio/sounds for Reels
- Trending content formats (e.g., photo carousels making a comeback, text posts, collab posts)
- Trending visual aesthetics and editing styles
- Trending caption styles and structures
- Search: `"Instagram trends {current month} {current year}"`, `"trending Instagram reels audio"`

**X/Twitter:**
- Use Chrome to check Trending topics (both global and location-specific)
- Trending conversation formats (threads, quote-tweet chains, community notes engagement)
- Trending content styles (long-form tweets, image threads, polls)
- What's driving engagement in the niche on X right now
- Search: `"Twitter/X trends {current month} {current year}"`

**LinkedIn:**
- Trending post formats (document carousels, polls, video, newsletters)
- Trending professional topics and debates
- What types of content are going viral
- Algorithm preferences (what LinkedIn is boosting right now)
- Search: `"LinkedIn trends {current month} {current year}"`, `"LinkedIn algorithm {current year}"`

**Facebook:**
- Trending content in relevant groups
- Format trends (video-first, link posts, community engagement)
- Group engagement patterns
- Search: `"Facebook marketing trends {current year}"`

### 4. Cultural & Seasonal Moments

Timely content opportunities for the next 30-60 days.

**Research:**
- Upcoming holidays and observances (both major and niche-relevant)
- Awareness days and weeks (e.g., Mental Health Awareness Week, Small Business Saturday)
- Cultural moments (award shows, sporting events, pop culture events)
- Seasonal themes (weather changes, back-to-school, end-of-year, summer, etc.)
- Industry events (conferences, product launches, trade shows)
- Meme culture — current viral memes that could be adapted for the brand (only if brand tone allows it)

**Search queries:**
- `"social media holidays {current month} {current year}"`
- `"awareness days {current month} {next month} {current year}"`
- `"{industry} events {current month} {current year}"`
- `"content calendar holidays {current month} {current year}"`

### 5. Google Trends Analysis

Use Chrome DevTools MCP, browser access, or page fetching to check Google Trends:

1. Search for the brand's core keywords — check interest over time
2. Check "Trending Now" and "Recently Trending" for relevant topics
3. Look at "Related Queries" — both "Top" and "Rising" for content angle ideas
4. Compare search interest between different content angles to pick winners
5. Check geographic interest for location-targeted content

**How to access:**
- Navigate to `trends.google.com` via Chrome
- Or fetch/open Google Trends URLs when available
- Search for 3-5 core keywords related to the brand's niche

## Trend Research Template

Store in `.growth/trends/{YYYY-MM}.md`:

```markdown
# Trend Research — {Month Year}

**Researched:** {date}
**Brand:** {brand name}
**Industry:** {industry/niche}

## Platform Algorithm & Format Updates

### What's Changed
- {platform}: {update and its impact}
- {platform}: {update and its impact}

### What's Getting Boosted Right Now
- {platform}: {format/content type getting extra reach}

## Platform-Specific Trends

### Instagram
- **Hot formats:** {what's working right now}
- **Trending audio:** {notable trending sounds relevant to the niche}
- **Content styles:** {visual and caption trends}
- **Engagement tactics:** {what's driving comments/saves/shares}

### X/Twitter
- **Hot formats:** {threads, quote tweets, polls, etc.}
- **Trending topics:** {relevant trending conversations}
- **Engagement patterns:** {what's getting traction}

### LinkedIn
- **Hot formats:** {document posts, video, text, polls}
- **Trending topics:** {professional trends and debates}
- **Content styles:** {what's resonating}

### Facebook
- **Hot formats:** {video, groups, community features}
- **Trending in groups:** {relevant group conversations}

## Niche-Specific Trends
| Trend | Description | Relevance to Brand | Content Angle |
|-------|-------------|-------------------|---------------|
| {trend} | {what's happening} | {why it matters to us} | {how to create content around it} |

## Cultural & Seasonal Calendar (Next 30-60 Days)
| Date | Event/Moment | Relevance | Content Idea |
|------|-------------|-----------|-------------|
| {date} | {event} | {HIGH/MED/LOW} | {specific content angle} |

## Google Trends Insights
- **Rising searches:** {relevant keywords gaining momentum}
- **Declining searches:** {keywords/topics losing interest — avoid}
- **Related queries to explore:** {new angles from related searches}
- **Geographic hotspots:** {locations where interest is highest}

## Actionable Opportunities

### High Priority (Act This Week)
1. **{opportunity}:** {how to capitalize} — Why now: {urgency reason}
2. ...

### Medium Priority (Plan for This Month)
1. **{opportunity}:** {how to capitalize}
2. ...

### Low Priority (Keep on Radar)
1. **{opportunity}:** {worth watching for later}
2. ...

## Content Angles Unlocked by Trends
1. **{angle}:** {description} — Platform: {where to use it} — Format: {recommended format}
2. ...
3. ...

## Trends to Avoid
- {trend}: {why to skip it — off-brand, oversaturated, risky, etc.}
```

## Refresh Protocol

- **Fast-moving niches** (tech, fashion, culture): Refresh every 1-2 weeks
- **Steady niches** (B2B, education, professional services): Monthly refresh is sufficient
- When refreshing, update the existing month's file rather than creating a new one
- Add a "Last Updated" timestamp and note what changed
- If a trend from earlier in the month is now dead, mark it as such rather than deleting it (learning what didn't last is valuable)

## Connecting Trends to Strategy

After completing trend research, always produce a "So What?" section that translates trends into specific content ideas. Raw trend data is useless — the value is in the strategic application:

- "Carousel posts are getting 2x reach on Instagram this month" → Plan 3 carousel posts this week, convert existing content into carousel format
- "Awareness week for {topic} is coming up on {date}" → Create a 3-post series starting 2 days before
- "{Trending audio} is blowing up on Reels" → Create a Reel using this audio with our brand's angle by {date}
