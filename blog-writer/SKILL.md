---
name: blog-writer
description: End-to-end SEO blog autopilot for the project you're working in. Works out the business and target audience, uses the `seo` skill for fresh keyword research, picks the best topic (or refreshes an existing post instead), writes a researched, answer-first article with internal links and a cover image, runs a quality gate, and publishes it live through the project's own blog tooling (e.g. `eravue-blog` / `pnpm blog`). Use when the user says "write a blog", "write N blogs", "publish a post about X", "blog autopilot", "/blog-writer", or wants SEO articles researched and shipped without hand-holding.
---

# Blog writer

You turn "write a blog" into a published post that can rank and bring in leads, for whichever project you're working in. You orchestrate three things that already exist, and don't duplicate them:

- the **`seo` skill**: research method, freshness rules, keyword research, content-writing and GEO rules;
- the **project's publishing route**: a project skill and/or CLI (for eravue.com: the `eravue-blog` skill and `pnpm blog`);
- the **project's writing rules**: voice, structure and image style, usually inside that project skill.

## Defaults (the user's standing choices)

- **One post per run.** If the user names a number ("write 3 blogs"), write that many, each going fully through the pipeline before the next starts.
- **Publish live automatically** once the quality gate passes. Don't ask for approval. Stop and ask only when a gate check fails and you can't fix it yourself, or when publishing would overwrite or unpublish an existing post.
- **Images: branded cover/OG plus SVG diagrams only.** Make an extra (AI) image only when the user asks for one, using the hand-off flow in [references/images.md](references/images.md). Never drive ChatGPT or other image tools yourself.
- **Runs only when invoked.** No scheduled or recurring runs unless the user sets one up.
- If the user gives a topic or keyword, skip topic selection but still validate it (step 4) and research it (step 5).

## Pipeline

Keep a short checklist of these steps in your task list so the user can follow along.

### 1. Load the project
Follow [references/project-setup.md](references/project-setup.md):
- Read `README.md`, `CLAUDE.md`/`AGENTS.md`, `.seo/project-profile.md`, and `.seo/blog-writer.md` (this skill's per-project config).
- If `.seo/blog-writer.md` is missing, discover the publishing route and create it. If no publishing route exists, write the post as a markdown file and tell the user it isn't published.
- Load the project's publishing skill (e.g. `Skill: eravue-blog`) so its CLI, writing and image rules are in context.
- Check credentials work with a read-only call (e.g. `pnpm blog list --limit 1`). On an auth error, stop and tell the user.

### 2. Know the audience
Read `.seo/audience.md`. If it's missing, older than 90 days, or predates the last change to the project profile, rebuild it per [references/audience.md](references/audience.md) from the live site, the profile and fresh community research.

### 3. Keep a researched topic backlog
Read `.seo/content/backlog.md`. If it's missing, older than 30 days, older than the newest keyword research, or has fewer than 3 `queued` topics, refresh it: **invoke the `seo` skill** (Skill tool, `seo`, with args like `keyword research for blog topics: <business, audience, geography>; feed .seo/content/backlog.md`) and follow its keyword-research rules, including the Search Console pull. Then score and dedupe topics per [references/topic-selection.md](references/topic-selection.md).

### 4. Pick the topic and decide new vs refresh
Take the top `queued` topic (or the user's topic). Before writing, check:
- the live post list and Search Console: does a live post already target this intent? If so, **refresh that post** (keep its slug) instead of creating a competitor;
- the live SERP today (Chrome DevTools MCP, correct country): is a blog post the right page type, and can this site credibly produce the best answer?
Drop or re-queue topics that fail, and say why in the backlog.

### 5. Research the post
Follow the `seo` skill's content-writing and GEO rules ([~/.claude/skills/seo/rules/content-writing.md](~/.claude/skills/seo/rules/content-writing.md), [geo-ai-search.md](~/.claude/skills/seo/rules/geo-ai-search.md)):
- the top 5-8 ranking pages, PAA questions, whether an AI Overview appears and what it cites;
- the same question in at least one AI assistant (ChatGPT or Perplexity), noting cited sources;
- current facts with sources (prices, stats, tool features, policies) dated within the last 12 months where it matters.
Write a compact brief to `.seo/content/briefs/<slug>.md`: keyword set, intent, angle, outline, facts with source links, internal links, CTA.

### 6. Write
Follow [references/writing-and-qa.md](references/writing-and-qa.md) together with the project's writing rules (the project's rules win on voice, structure and format). Save the article where the project expects it (Eravue: `.seo/content/articles/YYYY-MM-DD-<slug>.md`).

### 7. Images
Cover/OG via the project's cover command, plus SVG diagrams only where a picture explains better than text. If the user asked for an extra image, follow the hand-off flow in [references/images.md](references/images.md). Look at every image file before publishing.

### 8. Quality gate, then publish
Run every check in [references/writing-and-qa.md](references/writing-and-qa.md#quality-gate). Then use the project's validation command (Eravue: `pnpm blog push <file> --dry-run`) and fix all errors and warnings. Then publish (Eravue: `pnpm blog push <file> --publish`).

### 9. Verify and record
- Open the live URL (curl or the browser): 200, title, H1, cover image, internal links resolve, appears on the blog index.
- Update `.seo/content/backlog.md` (status `published`, URL, date) and add one line to `.seo/insights.md`.
- Don't request indexing in Search Console unless the user asks; sitemap, IndexNow and internal links handle discovery.

### 10. Report
Tell the user: live URL, target keyword and why it was chosen (the evidence), what was refreshed vs new, any facts you couldn't verify and left out, and what's next in the backlog.

## Hard rules

- No invented facts, statistics, quotes, clients, results or case studies. If you can't verify it, cut it.
- Never publish two posts targeting the same intent; refresh instead.
- Never change the slug of a live post, unpublish or delete posts as part of this pipeline. Suggest those changes instead.
- Don't paste secrets (tokens, API keys) into files, prompts or chat.
- If a step needs the user (login wall, CAPTCHA, missing token, an image they're providing), stop at that step, say exactly what you need, and resume from there when they reply.
