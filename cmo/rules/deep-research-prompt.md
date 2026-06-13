# Deep Research Prompt Generator

## Purpose

Generate comprehensive, structured research prompts designed for external deep research tools. When Codex's available web search and browser tools are not sufficient for the depth of research needed, this workflow produces a detailed prompt that can be sent to an external AI or research platform with deep research capabilities, yielding 10-20 pages of thorough analysis.

## When to Use This

- The research topic is broad and requires synthesizing dozens of sources
- The user needs competitive landscape analysis across an entire industry
- Trend research needs to go deeper than surface-level blog posts
- Audience research requires academic, behavioral, and market data
- The user explicitly asks for a deep research prompt
- Any research task where "10-20 pages of thorough analysis" would be more valuable than quick web searches

## Prompt Generation Methodology

### Step 1: Understand the Research Need

Before generating a prompt, gather context:

1. Read `.growth/brand-profile.md` for brand context
2. Read any existing research in `.growth/` that's relevant
3. Ask the user what specifically they need researched (if not already clear)
4. Determine the research category:
   - **Competitor Landscape** — deep analysis of competitive environment
   - **Industry Trends** — comprehensive trend analysis and forecasting
   - **Audience Research** — deep audience behavior, psychology, and preference analysis
   - **Platform Strategy** — deep-dive into specific platform algorithms, best practices, and opportunities
   - **Content Strategy Research** — what content formats, topics, and approaches work in the niche
   - **Market Analysis** — broader market conditions, opportunities, and threats
   - **Custom Topic** — any other research need the user specifies

### Step 2: Build the Research Prompt

A high-quality deep research prompt has these components:

#### A. Research Context Block
Provide the AI with all relevant brand context so the research is tailored, not generic:

```
## Context
- Brand: {name}
- Industry: {industry}
- Niche: {specific niche}
- Target audience: {demographics + psychographics summary}
- Active platforms: {platforms}
- Key competitors: {competitor names}
- Current positioning: {USP and brand positioning}
- Specific goals: {what the brand is trying to achieve}
```

#### B. Primary Research Question
One clear, specific question that defines the research scope:

```
## Primary Research Question
{A single, focused question that the entire research should answer}
```

#### C. Sub-Topics to Cover
Break the research into 8-15 specific sub-topics. Each should be:
- Specific enough to yield actionable findings
- Broad enough to allow for discovery of unexpected insights
- Ordered from most to least critical

```
## Required Sub-Topics
1. {Sub-topic}: {What specifically to research and why}
2. {Sub-topic}: {What specifically to research and why}
...
```

#### D. Data & Evidence Requirements
Specify what kinds of data points, statistics, and evidence to include:

```
## Data Requirements
- Include specific statistics and data points with sources
- Cite recent studies, reports, or surveys (2024-2026 preferred)
- Include real examples and case studies where relevant
- Provide quantitative data where possible (engagement rates, growth numbers, market sizes)
- Reference industry reports from {relevant sources}
```

#### E. Output Format Instructions
Tell the AI exactly how to structure its response for maximum usefulness:

```
## Output Format
- Structure the response with clear headers and sub-headers
- Lead each section with the key finding/insight, then supporting evidence
- Include a "Key Takeaways" summary at the end of each major section
- Use tables for comparative data
- Use bullet points for lists of actionable insights
- Target length: 10-20 pages of thorough analysis
- End with a "Strategic Implications" section that connects findings to actionable next steps
```

#### F. Scope Boundaries
Prevent the research from going off-track:

```
## Scope & Boundaries
- Focus on {specific geographic markets} unless global data is more relevant
- Prioritize {specific platforms} over others
- Time frame: Focus on {current year} data, reference {previous year} for trends
- Do NOT cover: {explicitly exclude irrelevant areas}
```

### Step 3: Save the Prompt

Save the generated prompt to `.growth/research-prompts/{topic-slug}.md`:

```markdown
# Deep Research Prompt: {Topic}

**Generated:** {date}
**Category:** {research category}
**Status:** Pending (waiting for external research)

---

{The complete research prompt}

---

## Instructions for User
1. Copy everything between the `---` lines above
2. Send it to the user's preferred deep research tool
3. Save the response to: `.growth/research/{topic-slug}.md`
4. Return to Codex and ask it to consume the research
```

### Step 4: Consuming External Research

When the user returns with the external research output:

1. Read the research file from `.growth/research/{topic-slug}.md`
2. Update the prompt file's status from "Pending" to "Completed — {date}"
3. Based on the research category, integrate findings into the appropriate `.growth/` files:
   - **Competitor Landscape** → Update/create files in `.growth/competitors/` and update `.growth/insights.md`
   - **Industry Trends** → Update/create `.growth/trends/{YYYY-MM}.md`
   - **Audience Research** → Update `.growth/brand-profile.md` (Target Audience section) and `.growth/insights.md`
   - **Platform Strategy** → Update `.growth/insights.md` with platform-specific strategies
   - **Content Strategy Research** → Update `.growth/insights.md` and `.growth/voice-library.md`
   - **Market Analysis** → Update `.growth/insights.md`
4. Summarize the key findings and strategic implications for the user
5. Recommend next actions based on the research (e.g., "Now let's build a content calendar based on these insights")

## Research Prompt Templates by Category

### Competitor Landscape Prompt Template

Key sub-topics to always include:
- Market positioning map of all major players
- Content strategy breakdown per competitor (formats, frequency, themes, engagement)
- Audience overlap and differentiation analysis
- Pricing and value proposition comparisons (if applicable)
- Growth trajectories and strategies that drove growth
- Gaps and whitespace opportunities in the competitive landscape
- Emerging competitors and disruptors to watch
- Best-in-class examples of social media execution in the space
- Cross-industry inspiration (brands outside the niche doing social media exceptionally well)
- Platform-by-platform competitive dynamics

### Industry Trends Prompt Template

Key sub-topics to always include:
- Macro trends reshaping the industry (technological, cultural, economic)
- Social media platform algorithm changes and their impact on the niche
- Content format trends with performance data (what's working NOW)
- Consumer behavior shifts in the target demographic
- Emerging sub-niches and micro-communities
- Technology trends affecting content creation and distribution
- Seasonal and cyclical patterns specific to the industry
- Predictions from industry leaders and analysts
- Case studies of brands that successfully rode recent trends
- Anti-trends (what's dying or oversaturated to avoid)

### Audience Research Prompt Template

Key sub-topics to always include:
- Detailed psychographic profile of the target audience
- Online behavior patterns (platforms, times, content consumption habits)
- Purchase decision journey and key touchpoints
- Pain points, frustrations, and unmet needs
- Aspirations, goals, and desired outcomes
- Content preferences by format, tone, and topic
- Community dynamics (where they gather, who they trust, how they communicate)
- Generational and demographic nuances within the audience
- Emerging audience segments to target
- Competitor audience analysis (who follows them and why)

## Quality Checks

Before saving and presenting the prompt, verify:

- [ ] Brand context is included and accurate (pulled from `.growth/brand-profile.md`)
- [ ] Primary research question is clear and focused
- [ ] Sub-topics are specific, not vague (e.g., "Instagram Reels engagement tactics for fitness brands" not "social media trends")
- [ ] Data requirements specify recency (2024-2026)
- [ ] Output format instructions will produce structured, actionable output
- [ ] Scope boundaries prevent rabbit holes
- [ ] The prompt would produce 10-20 pages of useful research, not fluff
- [ ] Existing research in `.growth/` is referenced so the external tool can build on it, not duplicate it
