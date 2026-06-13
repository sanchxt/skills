---
name: reddit-demand-capture
description: Research Reddit for customer-acquisition and market-demand opportunities around a product, startup, website, agency, app, SaaS, service, or company. Use when Codex needs to find relevant subreddits, inspect subreddit rules, search recent and active Reddit posts or comment threads, identify compliant opportunities to join the conversation, draft transparent high-value comments or posts, maintain a persistent Reddit research cache, or prepare human-reviewed Reddit outreach without repeating the same research every session.
---

# Reddit Demand Capture

## Overview

Help the user turn Reddit into a durable source of qualified attention without drifting into spam, fake community participation, or rule-evasion. Research first, check rules before every recommendation, produce a small number of high-fit opportunities, and draft replies or posts that are genuinely useful even if the product is never mentioned.

## Non-Negotiables

1. Be helpful before being promotional.
2. Be transparent about affiliation whenever the draft mentions the user's company, product, website, or service.
3. Read the relevant subreddit rules before recommending a comment or post.
4. Do not try to bypass anti-promotion rules with disguised self-promotion, fake neutrality, burner personas, vote manipulation, or bait designed to hide affiliation.
5. If rules prohibit self-promotion, links, vendor mentions, or solicitation, do not force the promotion. Either produce a non-promotional helpful reply or mark the subreddit or thread as unsuitable.
6. If a community member independently asks for more detail, re-check the rules before suggesting a follow-up response. If the rules still prohibit linking or promotion, say so and do not suggest a workaround.
7. Prefer a few strong, high-intent opportunities over mass posting.
8. Require human review before any live Reddit action.

Read [references/compliance.md](references/compliance.md) when deciding whether a subreddit or thread is safe for outreach.

## Startup Behavior

When invoked, first determine the working mode:

- **Research mode:** Find subreddits, rules, recurring pain points, and live opportunities.
- **Draft mode:** Turn approved opportunities into comments, posts, or DM-safe follow-ups.
- **Refresh mode:** Update stale subreddit, rules, or opportunity research in the cache.
- **Execution support mode:** Prepare the browser context and final review package for the user before they post.

If the user's prompt is broad, ask up to 3 direct questions:

1. What product, site, company, or offer are we promoting?
2. What outcome matters most: leads, sales, signups, demo bookings, newsletter subscribers, or awareness?
3. Do they want subreddit discovery, live opportunity finding, comment drafting, original post drafting, or a full workflow?

If the project already has a `.reddit-growth/` directory, treat it as the source of truth and ask only about missing context.

## Tooling Order

Use the strongest available tooling in this order:

1. **Chrome DevTools MCP** for Reddit page inspection when it is available.
   - Use page snapshots to inspect subreddit rules, pinned posts, thread content, timestamps, and comment context.
   - Use screenshots when the visual layout matters or when Reddit collapses rule content.
   - Use network or console inspection only when Reddit content is failing to load or infinite-scroll behavior blocks inspection.
2. **Web search** for broad discovery and current subreddit or thread search.
   - Search queries should target recent, active, and relevant conversations rather than broad vanity mentions.
3. **Chrome plugin or authenticated browser tooling** only when logged-in behavior is needed for final user-reviewed execution.
4. **Local file tools** to maintain the persistent cache.

If Chrome DevTools MCP tools are not already exposed, use tool discovery to find them before falling back to more generic browsing.

## Persistent Data Directory

Store persistent work in `.reddit-growth/` in the current working directory so future runs do not repeat research.

Run `scripts/init_reddit_growth_workspace.py` if the directory does not exist and the user wants persistent Reddit work.

Directory layout:

```text
.reddit-growth/
|-- project-profile.md
|-- activity-log.md
|-- insights.md
|-- subreddits/
|   `-- {subreddit}.md
|-- rules/
|   `-- {subreddit}.md
|-- searches/
|   `-- {YYYY-MM-DD}-{topic}.md
|-- opportunities/
|   `-- {YYYY-MM-DD}-{subreddit}-{slug}.md
|-- drafts/
|   `-- {YYYY-MM-DD}-{subreddit}-{format}.md
|-- posted/
|   `-- {YYYY-MM-DD}.md
`-- rejected/
    `-- {YYYY-MM-DD}.md
```

Read [references/directory-schema.md](references/directory-schema.md) before creating or updating these files.

## Workflow

### 1. Load or Create Project Context

Read `.reddit-growth/project-profile.md` if it exists. If not, collect or infer:

- Product or service name.
- One-sentence description.
- ICP and buyer intent.
- Primary customer pains.
- Categories, competitor names, alternative tools, and problem phrases.
- Allowed claims, prohibited claims, approved URLs, and compliance constraints.
- Offer type: SaaS, agency, marketplace, newsletter, content site, app, local service, or ecommerce.
- Preferred conversion event.

If the user is vague, anchor the research on pains and buyer moments, not on brand slogans.

### 2. Check the Existing Cache Before Researching

Read existing subreddit, rules, search, and opportunity files before starting fresh work.

Refresh stale items:

- Treat thread and opportunity research older than 14 days as stale.
- Treat subreddit rules and culture notes older than 30 days as stale.
- Refresh immediately if the subreddit has new pinned posts, automod guidance, wiki updates, or rule changes.

### 3. Build the Search Map

Generate search inputs from the product and customer pains:

- Core category terms.
- Problem and frustration phrases.
- Competitor and alternative names.
- Comparison phrases such as "vs", "alternative", "replace", or "looking for".
- Buying-intent phrases such as "recommend", "tool for", "need help", "best way", or "what do you use".
- Situational phrases tied to workflows, budgets, skill level, geography, or industry.

Read [references/opportunity-research.md](references/opportunity-research.md) for query patterns and scoring.

### 4. Discover Candidate Subreddits

Use search to find likely subreddits. Favor communities where:

- The pain is discussed repeatedly.
- Recommendation requests happen naturally.
- The moderation style is predictable.
- Real practitioners gather, not just hobby lurkers.
- Recent posts still receive comments.

For each candidate subreddit:

1. Open the subreddit.
2. Inspect the rules, sidebar, pinned posts, wiki links, and recent mod posts.
3. Record whether the subreddit is:
   - `allowed-with-link`
   - `allowed-no-link`
   - `allowed-name-only`
   - `discussion-only`
   - `research-only`
   - `do-not-use`
4. Capture tone notes and recurring post formats.

If the rules are ambiguous, assume the stricter interpretation and record the uncertainty.

### 5. Inspect Live Opportunities

Within approved subreddits, look for:

- Recent recommendation requests.
- Help threads where the product solves the exact problem.
- "What tool should I use?" posts.
- Comparison threads.
- Complaint or pain threads.
- Build-in-public or stack-sharing posts where the product fits naturally.
- Comment chains where the main post is broad but a specific comment reveals stronger purchase intent.

Prefer threads that are:

- Recent enough for the reply to still be seen.
- Active enough that people are reading.
- Specific enough that a helpful answer can stand on its own.
- Close enough to the product's true value that the mention will not feel forced.

Do not pitch into unrelated or weak-fit threads just because they are popular.

### 6. Score and Select Opportunities

Score each candidate on:

1. Intent strength.
2. Product fit.
3. Rule safety.
4. Thread freshness.
5. Current comment activity.
6. Ability to help without overselling.
7. Risk of backlash.

Prioritize the top 3-5 opportunities, not a giant list. Save the losers in `rejected/` with a short reason so they are not reconsidered next time.

### 7. Draft the Right Kind of Contribution

Choose the safest format that still creates value:

- **Helpful comment without brand mention** when the rule environment is sensitive and the advice alone is useful.
- **Transparent comment with product mention** when the rules allow naming a solution and the fit is strong.
- **Transparent comment without a link** when the rules allow discussion but dislike links.
- **Original value-first post** only when the subreddit supports this format and the post can stand as a real contribution.

Drafting rules:

1. Start by solving the user's problem.
2. Match the subreddit tone and detail level.
3. Mention the product only when it adds real value.
4. Disclose affiliation plainly when relevant.
5. Avoid hype, fake scarcity, and generic startup language.
6. Avoid copying the same comment structure across multiple threads.
7. If links are restricted, do not engineer curiosity or bait the reader into asking for a URL. Provide the best self-contained answer you can.
8. If someone later asks for the name or link, verify the rules again before drafting a reply.

Read [references/drafting-playbook.md](references/drafting-playbook.md) for response frameworks and templates.

### 8. Prepare the Review Package

Before any live action, present a concise review package:

- Subreddit and rule classification.
- Direct links to the thread or post under consideration.
- Why this is a fit.
- Risks or caveats.
- Recommended draft.
- Backup draft with lower promotional intensity.
- Whether the draft includes a product name, URL, or no mention at all.

If the user wants help posting live, stop for confirmation after the final draft is approved.

### 9. Log the Outcome

After the user posts or declines:

- Record what was attempted in `.reddit-growth/activity-log.md`.
- Save the final copy in `drafts/` or `posted/`.
- Add outcomes and lessons to `.reddit-growth/insights.md`.
- Mark subreddits or formats that performed poorly so future runs deprioritize them.

## Chrome DevTools MCP Guidance

When Chrome DevTools MCP is available, prefer it for close inspection of Reddit because it gives better page-state awareness than plain search results.

Use it to:

- Snapshot subreddit rule pages and sidebars.
- Inspect pinned posts and moderator guidance.
- Read full thread context before drafting.
- Verify timestamps, vote velocity cues, comment depth, and whether the conversation is still active.
- Capture screenshots for the user's review package.

Use authenticated browser tooling only when the session must interact with a logged-in Reddit account. If logged-in tooling is unavailable, stop at research and drafts.

## What Not to Do

- Do not recommend astroturfing, fake personas, karma farming, or stealth promotion.
- Do not advise the user to ignore moderator guidance.
- Do not assume that "no explicit rule against it" means promotion is welcome.
- Do not recommend DMs unless the subreddit explicitly allows that behavior and the user specifically wants it.
- Do not optimize only for visibility; optimize for trust and conversion quality.
- Do not reuse stale subreddit assumptions without re-checking them.

## First-Run Checklist

When using this skill for a new product:

1. Initialize `.reddit-growth/`.
2. Create or update the project profile.
3. Identify 10-20 candidate subreddits.
4. Classify each subreddit's promotion tolerance.
5. Find 10-15 live opportunities.
6. Shortlist the top 3-5.
7. Draft the safest high-value responses.
8. Present the review package.

## References

- [references/compliance.md](references/compliance.md): Rule interpretation, disclosure, and anti-spam guardrails.
- [references/directory-schema.md](references/directory-schema.md): Persistent cache structure and file templates.
- [references/opportunity-research.md](references/opportunity-research.md): Search patterns, opportunity scoring, and recency heuristics.
- [references/drafting-playbook.md](references/drafting-playbook.md): Comment and post frameworks for different subreddit rule profiles.
