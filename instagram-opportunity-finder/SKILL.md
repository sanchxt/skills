---
name: instagram-opportunity-finder
description: Find Instagram accounts for compliant outreach from a user's brand, agency, creator, founder, or personal account. Use when Codex is asked to discover Instagram prospects, audit brand or creator profiles, inspect bio links or websites, identify content/business/marketing gaps, draft tailored DM/comment/email outreach, track outreach status, or build a persistent SQLite database of Instagram accounts for a product, service, agency, newsletter, SaaS, creator offer, or founder-led sales motion.
---

# Instagram Opportunity Finder

## Overview

Find public Instagram accounts that may be good-fit prospects for the user's product, service, brand, or founder account. Audit each account and its bio link or website when available, then return prioritized outreach opportunities with specific gaps, service fit, and tailored outreach copy.

## Operating Rules

- Use only public information unless the user explicitly asks to use a logged-in browser session they control.
- Do not DM, comment, follow, like, save, report, join broadcast channels, or otherwise interact with Instagram accounts unless separately authorized and given exact copy/action confirmation.
- Avoid deceptive outreach. Draft messages that disclose relevant affiliation when offering the user's product or service.
- Prefer quality over volume. Do not pad results with weak-fit accounts when the requested count cannot be reached responsibly.
- Treat minors, medical distress, legal hardship, mental-health crises, financial vulnerability, grief, and other sensitive situations as `avoid` for promotional outreach.
- Respect platform limitations, robots/login walls, rate limits, and account privacy. If Instagram blocks useful inspection, use search snippets, official websites, linked pages, or ask before switching to logged-in Chrome.
- Never recommend scraping private accounts, bypassing login gates, evading rate limits, or collecting non-public contact information.
- Keep outreach human-reviewed. Mark generated messages as drafts, not sent messages.

## Workflow

1. Capture campaign context:
   - User's brand/founder account handles, product/service summary, website, target customers, geography/language constraints, price point, proof points, disallowed audiences, and outreach channel preference.
   - Derive a persistent campaign key from the brand/account/product name unless the user provides one.
   - Ask for missing context only when the offer, target customer, or outreach constraints are too vague to qualify accounts responsibly.

2. Build prospect clusters:
   - Translate the offer into likely account categories, niches, business models, creator types, follower ranges, locations, and pain signals.
   - Read `references/discovery-playbook.md` when more discovery paths or query patterns are needed.

3. Discover accounts:
   - Use Instagram search, public profile pages, hashtags, location pages, search engines with `site:instagram.com`, creator directories, marketplace listings, brand websites, podcasts/newsletters, and competitor/customer ecosystems.
   - If the user authorizes logged-in account context, inspect public followers/following/commenters only for fit signals; do not interact.
   - Prefer accounts that are active, have a commercial or creator intent, and show visible gaps the user's offer can credibly improve.

4. Audit each account:
   - Capture username, profile URL, display name, bio, account type, visible location, website/bio link, follower range if visible, activity recency, content themes, offer, audience, and contact surfaces.
   - Inspect linked websites, link-in-bio pages, stores, booking pages, newsletters, portfolios, or lead forms when available.
   - Read `references/account-audit-rubric.md` for scoring and evidence standards.

5. Qualify outreach:
   - Score ICP fit, urgency, business value, outreach fit, sensitivity risk, and personalization depth.
   - Identify what the account lacks: bio clarity, website conversion, content positioning, SEO, landing page quality, design quality, offer packaging, analytics, paid ads, email capture, booking flow, creator monetization, or brand consistency.
   - Mark weak accounts as `research-only`, `not-fit`, or `avoid`.

6. Draft outreach:
   - Read `references/outreach-guidance.md` when drafting DMs, comments, or emails.
   - Make the message specific to visible evidence from the account or website.
   - Lead with a useful observation or micro-suggestion before mentioning the user's service.
   - Keep DMs concise; keep comments non-salesy and public-safe; use email only when a public business email or website contact form is available.

7. Store and filter results:
   - For CSV-backed results, first run `scripts/normalize_instagram_leads.py` to normalize usernames, dedupe accounts, validate fields, and sort candidates.
   - Then filter through the persistent Instagram database:
     `python C:\Users\tpbea\.codex\skills\instagram-opportunity-finder\scripts\instagram_lead_memory.py filter --campaign "<campaign>" --input <normalized.csv> --fresh-output <fresh.csv> --repeats-output <repeats.csv> --record-found`
   - Present only fresh accounts from `<fresh.csv>` by default.
   - Include the skipped-repeat summary printed by the memory filter, for example: "Skipped 8 previously seen Instagram accounts: 5 found, 2 ignored, 1 contacted."
   - Save large CSV/Markdown deliverables in the workspace `outputs/` directory when requested or too large for chat.

## Persistent Instagram Database

Use `scripts/instagram_lead_memory.py` for a separate SQLite database dedicated to Instagram outreach.

- Initialize with:
  `python C:\Users\tpbea\.codex\skills\instagram-opportunity-finder\scripts\instagram_lead_memory.py init`
- Default database:
  `C:\Users\tpbea\.codex\instagram_lead_memory\instagram_leads.sqlite3`
- Campaign-aware uniqueness: the same username can be fresh for one campaign and previously seen for another.
- Leads shown to the user are recorded as `found` only when `--record-found` is used.
- When the user says they contacted, shortlisted, ignored, avoided, or received a reply from an account, record it:
  `python C:\Users\tpbea\.codex\skills\instagram-opportunity-finder\scripts\instagram_lead_memory.py mark --campaign "<campaign>" --username "<username>" --status contacted|replied|shortlisted|ignored|avoided|not-fit --note "<optional note>"`
- Do not infer contact. Only mark `contacted` or `replied` when the user explicitly says it happened.

## Output Fields

Use these columns for CSV/Markdown deliverables:

- `username`
- `profile_url`
- `display_name`
- `account_type` (`brand`, `creator`, `founder`, `agency`, `local-business`, `community`, `other`)
- `niche`
- `location`
- `website_url`
- `followers`
- `activity_recency`
- `discovered_from`
- `evidence_summary`
- `content_gap_summary`
- `website_gap_summary`
- `service_fit_summary`
- `icp_fit_score` (`1`-`5`)
- `urgency_score` (`1`-`5`)
- `business_value_score` (`1`-`5`)
- `outreach_fit` (`dm-worthy`, `comment-worthy`, `email-worthy`, `research-only`, `not-fit`, `avoid`)
- `sensitivity_risk` (`low`, `medium`, `high`)
- `suggested_dm`
- `suggested_comment`
- `suggested_email`
- `notes`

## Resources

- `references/discovery-playbook.md`: discovery channels, query patterns, and prospect cluster prompts.
- `references/account-audit-rubric.md`: scoring rubric, exclusion rules, and audit checklist.
- `references/outreach-guidance.md`: outreach copy constraints and message patterns.
- `scripts/normalize_instagram_leads.py`: CSV dedupe, username/profile URL normalization, validation, and sorting helper.
- `scripts/instagram_lead_memory.py`: SQLite database initializer, fresh/repeat filter, status marker, and exporter.

## Stop And Ask

Stop and ask the user before continuing only when:

- The offer or target audience is too vague to qualify accounts.
- Useful inspection requires logged-in Instagram access and the user has not authorized using a logged-in browser session.
- Instagram blocks access and fallback sources would materially reduce confidence.
- The user asks to send DMs/comments/follows/likes but has not confirmed the exact action.
- Reaching the requested count would require weak matches, sensitive audiences, private accounts, or non-compliant scraping.
