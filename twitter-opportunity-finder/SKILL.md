---
name: twitter-opportunity-finder
description: Find fresh X/Twitter posts, replies, and high-engagement conversations where real users are describing pain points that a product, website, SaaS, app, agency, service, newsletter, or project can help with. Use when Codex is asked to find Twitter/X leads, customer conversations, popular tweets to study, reply opportunities, search operators, demand-capture opportunities, outreach angles, or compliant ways to market a product on X. Prioritize recent and active posts/replies, use X Advanced Search and search-bar operators, and never post, DM, like, repost, follow, or otherwise interact unless explicitly authorized.
---

# Twitter Opportunity Finder

## Overview

Find X/Twitter conversations where the user's product can be introduced later in a helpful, transparent way. Return clean links, relevance notes, recency context, engagement context, and outreach angles; do not engage with X users unless separately authorized.

## Operating Rules

- Prefer fresh opportunities: recent posts, recent replies, active threads, and high-engagement posts where a reply would not feel stale.
- Ask for missing product context only when the request does not include enough information to infer target users, pain points, categories, or excluded audiences.
- Use the user's requested browser/tooling when specified. If they request Chrome or Chrome DevTools, use the Chrome plugin/tools when available; if unavailable, say so before falling back.
- Use X.com search, X Advanced Search, direct search URLs, and search engines with `site:x.com` / `site:twitter.com` as complementary sources.
- Do not post, reply, DM, like, repost, quote, bookmark, follow, subscribe, join Communities, report, or otherwise interact.
- Avoid deceptive astroturfing. Recommend transparent outreach that discloses affiliation when linking the user's product.
- Treat mental-health, crisis, medical, legal, financial hardship, and highly vulnerable situations as "do not promote" unless the user explicitly asks for a non-promotional support response.
- Prefer human review before any outreach on X; X is fast-moving and public, so bad-fit promotion can damage reputation quickly.

## Workflow

1. Capture product context:
   - Product name, URL, summary, target users, core pain points, geography/language constraints, competitors, disallowed audiences, and whether the user wants posts, replies, or both.
   - Derive a persistent product/campaign key from the product name or URL unless the user provides a specific campaign name.
   - Desired output count and whether they want reply-worthy leads, market-research links, viral examples, or content/positioning ideas.
   - Preferred freshness window. If unspecified, default to the last 7 days first, then 30 days, then 90 days.

2. Build pain-language query clusters:
   - Translate product features into user complaints, alternatives, failed workflows, "how do I", "any tool for", "I hate", "struggling with", "what do you use", "recommendations", "looking for", and competitor-switching language.
   - Read `references/search-patterns.md` when more query templates or operators are needed.

3. Search X fresh-first:
   - Start with direct search URLs using `f=live` for latest results and `f=top` for high-engagement results.
   - Use X Advanced Search at `https://x.com/search-advanced` when UI fields are easier than writing operators.
   - Use narrow date windows (`since:YYYY-MM-DD until:YYYY-MM-DD`) and engagement floors (`min_faves:`, `min_retweets:`, `min_replies:`) to find popular posts without drowning in noise.
   - Prefer direct post URLs and direct reply URLs when available.

4. Inspect replies and conversation fit:
   - For high-engagement posts, inspect replies for buyers describing sharper pain than the original post.
   - Look for unresolved questions, tool requests, vendor complaints, workflow bottlenecks, and founder/operator threads.
   - Avoid replying to obvious ragebait, political pile-ons, scams, harassment threads, tragedy, or sensitive personal distress.

5. Qualify each lead:
   - Score relevance, recency, engagement, reply fit, sensitivity, and outreach risk.
   - Read `references/lead-rubric.md` for scoring criteria and output field definitions.
   - Keep weak or stale links separate as market research.

6. Produce the deliverable:
   - For CSV-backed results, first run `scripts/normalize_twitter_leads.py` to dedupe, validate, and sort candidates.
   - Then run the persistent lead memory filter before presenting results, using `python C:\Users\tpbea\.codex\lead_memory\lead_memory.py filter --platform twitter --product "<product or campaign>" --input <normalized.csv> --fresh-output <fresh.csv> --repeats-output <repeats.csv> --record-found`.
   - Present only fresh leads from `<fresh.csv>` by default.
   - Include the skipped-repeat summary printed by the memory filter, for example: "Skipped 12 previously seen leads: 7 found, 3 ignored, 2 replied."
   - Return a Markdown table by default.
   - For large lists, save a CSV and/or Markdown report in the workspace `outputs/` directory if the user requested a file or the result is too large for chat.
   - Include outreach angle notes, but do not draft mass replies unless asked.

## Persistent Lead Memory

Use `C:\Users\tpbea\.codex\lead_memory\lead_memory.py` to avoid recommending the same X/Twitter post or reply again for the same product/campaign across future Codex chats.

- Initialize the database if needed with `python C:\Users\tpbea\.codex\lead_memory\lead_memory.py init`.
- The default database is `C:\Users\tpbea\.codex\lead_memory\leads.sqlite3`.
- Memory is product-aware: the same URL can be fresh for one product and previously seen for another.
- Hide previously seen leads by default. Keep repeat details in the repeats CSV and mention only the summary in the user-facing answer.
- When the user says they replied to, shortlisted, ignored, or avoided an X/Twitter lead, record it with `python C:\Users\tpbea\.codex\lead_memory\lead_memory.py mark --platform twitter --product "<product or campaign>" --url "<url>" --status replied|shortlisted|ignored|avoided --note "<optional note>"`.
- Do not infer that the user replied unless they explicitly say so. Leads shown to the user are recorded as `found`; later outreach actions require a `mark` update.

## X Search Mechanics

- Use the search tabs intentionally:
  - `Top` / `f=top`: ranked by X; best for popular posts, viral framing, and high-engagement pain.
  - `Latest` / `f=live`: chronological; best for fresh reply opportunities.
  - `People`, `Media`, and `Lists`: useful for influencer/source discovery, visual proof, and niche list research.
- Use Advanced Search fields for:
  - Words: all words, exact phrase, any words, excluded words, hashtags, language.
  - Accounts: `from:`, `to:`, and mentions.
  - Filters: replies, links, only replies, only posts with links.
  - Engagement: minimum replies, likes, and reposts.
  - Dates: from, to, or a date range.
- Prefer typed operators once you know the target query; they are faster, shareable, and easy to save.
- X search can be inconsistent. If a query returns too little, remove one operator at a time, switch from `Top` to `Latest`, broaden the date window, then lower engagement floors.
- For official API-backed research, X API search supports keyword/phrase/hashtag/user/content/language/reply/retweet operators, but access and query limits differ from X.com search.

## Freshness Policy

Default order:

1. Last 24-72 hours: best for direct replies.
2. Last 7 days: strong default for active conversations.
3. Last 30 days: acceptable when pain is specific or engagement is high.
4. Last 90 days: use for market research or evergreen pain only.
5. Older posts: include only in a separate "viral examples / market research" section.

When the user asks for many links, do not pad with poor matches. Report the qualified count and explain whether expanding freshness, lowering engagement floors, or broadening audiences would be needed.

## Marketing Guidance

For each promising lead, provide a short suggested angle:

- Validate the user's problem in the language they used.
- Offer one useful workflow, checklist, example, or decision criterion before mentioning the product.
- Disclose affiliation when linking: "I built/work on..." or "I'm involved with..."
- Tailor the reply to the post or thread; do not reuse one generic promotional reply.
- Prefer no-link replies when the account is new, the thread is crowded, or the product mention would feel abrupt.
- For popular posts, consider using the thread as content inspiration instead of direct promotion: quote the pain, explain a useful solution pattern, and only mention the product if it naturally fits.

## Output Fields

Use these columns for CSV/Markdown deliverables:

- `url`
- `type` (`post`, `reply`, `quote`, `profile`, or `research`)
- `author_handle`
- `date_or_age`
- `query_used`
- `pain_category`
- `evidence_summary`
- `engagement_summary`
- `relevance_score` (`1`-`5`)
- `freshness_score` (`1`-`5`)
- `engagement_score` (`1`-`5`)
- `outreach_fit` (`reply-worthy`, `research-only`, `avoid`)
- `sensitivity_risk` (`low`, `medium`, `high`)
- `suggested_angle`
- `notes`

Use `scripts/normalize_twitter_leads.py` to dedupe, validate, and sort CSV outputs when handling many links. Then filter the normalized CSV through persistent lead memory before showing the final deliverable.

## Resources

- `references/search-patterns.md`: X/Twitter search operators, query formulas, and demand-capture patterns.
- `references/lead-rubric.md`: scoring, exclusion criteria, and output standards.
- `scripts/normalize_twitter_leads.py`: CSV dedupe/sort/validation helper.

## Stop And Ask

Stop and ask the user before continuing only when:

- Product/audience context is too vague to search responsibly.
- The requested browser/tool access is unavailable and fallback browsing would materially change the workflow.
- Login, rate limits, search blocks, CAPTCHA, age gates, protected accounts, or restricted Communities block useful progress.
- The user asks for posting/replying/DMing/liking/reposting/following but has not confirmed the exact action.
- Reaching the requested count requires lowering quality, expanding beyond X/Twitter, or targeting sensitive communities.
