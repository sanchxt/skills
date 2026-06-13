---
name: reddit-opportunity-finder
description: Find fresh Reddit posts and comments where real users are describing pain points that a product, website, SaaS, app, agency, service, newsletter, or project can help with. Use when Codex is asked to find Reddit leads, demand-capture opportunities, customer conversations, posts to reply to, comment links for promotion, subreddits where prospects are active, or outreach angles for a user-provided product summary. Prioritize recent and active posts/comments, respect subreddit rules, and never post, DM, vote, or interact unless the user explicitly asks.
---

# Reddit Opportunity Finder

## Overview

Find Reddit conversations where the user's product can be introduced later in a helpful, transparent way. Return clean links, relevance notes, recency context, and outreach angles; do not engage with Reddit users unless separately authorized.

## Operating Rules

- Prefer fresh opportunities: recent posts/comments, active threads, and discussions where a reply would not feel stale.
- Ask for missing product context only when the request does not include enough information to infer target users, pain points, or categories.
- Use the user's requested browser/tooling when specified. If they request Chrome or Chrome DevTools, use the Chrome plugin/tools when available; if unavailable, say so before falling back.
- Use Reddit itself, search engines with `site:reddit.com`, and subreddit search as complementary sources.
- Do not comment, DM, upvote, join communities, save posts, report, or otherwise interact.
- Avoid deceptive astroturfing. Recommend transparent outreach that discloses affiliation when linking the user's product.
- Treat mental-health, crisis, medical, legal, financial hardship, and highly vulnerable situations as "do not promote" unless the user explicitly asks for a non-promotional support response.
- Check subreddit rules before recommending outreach in a subreddit with visible self-promotion restrictions.

## Workflow

1. Capture product context:
   - Product name, URL, summary, target users, core pain points, geography/language constraints, and disallowed audiences.
   - Derive a persistent product/campaign key from the product name or URL unless the user provides a specific campaign name.
   - Desired output count and whether posts, comments, or both are acceptable.
   - Preferred freshness window. If unspecified, default to the last 30 days first, then expand to 90 days, then evergreen threads only if needed.

2. Build pain-language query clusters:
   - Translate product features into user complaints, alternatives, failed workflows, "how do I", "any app for", "struggling with", and "what do you use" phrasing.
   - Read `references/search-patterns.md` when more query templates are needed.

3. Discover and prioritize subreddits:
   - Start from obvious product-category communities, then adjacent role, problem, workflow, tool-comparison, student/professional, and hobby communities.
   - Favor active communities with recent posts and visible discussion depth.
   - Read `references/subreddit-discovery.md` for category prompts.

4. Search fresh-first:
   - Search recent posts first, then recent comments inside relevant posts.
   - Use search engine recency filters when available.
   - Prefer direct comment permalinks when a comment contains the pain point.
   - Exclude deleted/removed/locked content unless the surviving thread is still actionable.

5. Qualify each lead:
   - Score relevance, recency, reply fit, rule risk, and sensitivity.
   - Read `references/lead-rubric.md` for the scoring rubric and output field definitions.
   - Keep weak market-research links separate from reply-worthy opportunities.

6. Produce the deliverable:
   - For CSV-backed results, first run `scripts/normalize_reddit_leads.py` to dedupe, validate, and sort candidates.
   - Then run the persistent lead memory filter before presenting results, using `python C:\Users\tpbea\.codex\lead_memory\lead_memory.py filter --platform reddit --product "<product or campaign>" --input <normalized.csv> --fresh-output <fresh.csv> --repeats-output <repeats.csv> --record-found`.
   - Present only fresh leads from `<fresh.csv>` by default.
   - Include the skipped-repeat summary printed by the memory filter, for example: "Skipped 12 previously seen leads: 7 found, 3 ignored, 2 replied."
   - Return a Markdown table by default.
   - For large lists, save a CSV and/or Markdown report in the workspace `outputs/` directory if the user requested a file or the result is too large for chat.
   - Include outreach angle notes, but do not draft mass comments unless asked.

## Persistent Lead Memory

Use `C:\Users\tpbea\.codex\lead_memory\lead_memory.py` to avoid recommending the same Reddit post or comment again for the same product/campaign across future Codex chats.

- Initialize the database if needed with `python C:\Users\tpbea\.codex\lead_memory\lead_memory.py init`.
- The default database is `C:\Users\tpbea\.codex\lead_memory\leads.sqlite3`.
- Memory is product-aware: the same URL can be fresh for one product and previously seen for another.
- Hide previously seen leads by default. Keep repeat details in the repeats CSV and mention only the summary in the user-facing answer.
- When the user says they commented on, shortlisted, ignored, or avoided a Reddit lead, record it with `python C:\Users\tpbea\.codex\lead_memory\lead_memory.py mark --platform reddit --product "<product or campaign>" --url "<url>" --status commented|shortlisted|ignored|avoided --note "<optional note>"`.
- Do not infer that the user commented unless they explicitly say so. Leads shown to the user are recorded as `found`; later outreach actions require a `mark` update.

## Freshness Policy

Default order:

1. Last 7 days: best for direct outreach.
2. Last 30 days: strong default.
3. Last 90 days: acceptable when the pain is specific and the thread still has activity.
4. Older evergreen threads: include only in a separate "market research / lower priority" section or when the requested count cannot be reached otherwise.

When the user asks for 80-100 links, do not pad with poor matches. Report the qualified count and explain whether expanding freshness, broadening audiences, or including weaker research links would be needed.

## Outreach Guidance

For each promising lead, provide a short suggested angle:

- Validate the user's pain in plain language.
- Offer one useful workflow, checklist, or decision criterion before mentioning the product.
- Disclose affiliation when linking: "I built/work on..." or "I'm involved with..."
- Tailor the reply to the thread; do not reuse one generic promotional comment.
- If subreddit rules restrict promotion, recommend a no-link helpful answer or mark the lead as "do not promote."

## Output Fields

Use these columns for CSV/Markdown deliverables:

- `url`
- `type` (`post` or `comment`)
- `subreddit`
- `title_or_context`
- `date_or_age`
- `pain_category`
- `evidence_summary`
- `relevance_score` (`1`-`5`)
- `freshness_score` (`1`-`5`)
- `outreach_fit` (`reply-worthy`, `research-only`, `avoid`)
- `rule_risk` (`low`, `medium`, `high`, `unknown`)
- `sensitivity_risk` (`low`, `medium`, `high`)
- `suggested_angle`
- `notes`

Use `scripts/normalize_reddit_leads.py` to dedupe, validate, and sort CSV outputs when handling many links. Then filter the normalized CSV through persistent lead memory before showing the final deliverable.

## Resources

- `references/search-patterns.md`: query formulas and pain-language expansion.
- `references/subreddit-discovery.md`: subreddit discovery prompts and community categories.
- `references/lead-rubric.md`: scoring, exclusion criteria, and final output standards.
- `scripts/normalize_reddit_leads.py`: CSV dedupe/sort/validation helper.

## Stop And Ask

Stop and ask the user before continuing only when:

- Product/audience context is too vague to search responsibly.
- The requested browser/tool access is unavailable and fallback browsing would materially change the workflow.
- Login, age gates, quarantined communities, or restricted content block useful progress.
- The user asks for posting/commenting/DMs but has not confirmed the exact action.
- Reaching the requested count requires lowering quality, expanding beyond Reddit, or targeting sensitive communities.
