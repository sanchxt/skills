---
name: eravue-social
description: Founder-led social media for Eravue - plans and writes LinkedIn posts for Sanchit and Sanchita and the Eravue company page, X/Twitter posts and replies, the @eravuedotcom Instagram feed (proof, case studies, reposted reels), and schedules @lifewithcofounders reels (scripts come from the lifewithcofounders skill). Fixes social profiles so they convert, builds the weekly content calendar, drafts comments on prospects' posts, publishes founder-approved posts through the logged-in browser, and logs every post's performance. Use for "write today's LinkedIn post", "content calendar", "fix our Instagram bio", "what should we post", "repurpose this reel", "comment strategy", "post the approved posts", "how did our posts do".
---

# Eravue social

> **Storage: Eravue HQ (live from 2026-11-25).** Eravue HQ (https://app.eravue.com) is the only record of leads, every message sent and received, drafts, Upwork jobs, clients, content, the proof library, tasks, notes, metrics and both founders' days. Use the `eravue-hq` MCP tools as described in `references/hq.md`. Wherever this skill mentions `leads.py`, `growth.py`, `.outreach/*.csv`, `.growth/*.csv`, the claude.ai Daily Board (ArtifactData `days`) or an approval list in a `.growth/daily/*.md` file, do the HQ equivalent from the tool map in `references/hq.md` instead. Those files are frozen (renamed `*.frozen-2026-11-25.csv`) and must not be written. Approval happens in the HQ Outbox: queue messages with `draft_create` and send only drafts a founder approved (`drafts_list status=APPROVED`), then call `draft_mark_sent`. If the `eravue-hq` tools aren't connected, stop and ask the founder to connect them (HQ → Settings → Agents). Everything else in this skill (voice, quotas, research and safety rules) still applies.
>
> For social: the content calendar is HQ Studio (`content_upsert` per post with account, format, `scheduledAt`, hook and caption). Posts that need approval: `draft_create` type POST with `contentId`. After posting: `stage: POSTED`, `postUrl`, and later `metrics`.

Social exists to **win clients**: make the founders known, trusted and top-of-mind for the businesses they're pitching, and turn attention into DMs. Followers are a means, not the goal. A post that gets 300 views from 10 clinic owners beats 30k views from students.

## Before anything

1. `~/.claude/skills/eravue-outreach/references/eravue-profile.md`: services, real proof, voice, forbidden claims.
2. `.growth/strategy.md`: current focus, beachhead niches, phase.
3. This month's calendar `.growth/content-plan/YYYY-MM.md` and recent performance: `python ~/.claude/skills/eravue-metrics/scripts/growth.py content list --days 30`.
4. For writing that should sound human: `~/.claude/skills/short-form-craft/references/human-voice.md`.

## Accounts

| Account | Role | Cadence (cash sprint) |
|---|---|---|
| Sanchit on LinkedIn (personal) | Main B2B channel: AI builds, client stories, opinions for owners/founders | 3-4/week |
| Sanchita on LinkedIn (personal) | The business/client side: process, lessons, behind the scenes, clients' wins | 2-3/week |
| Eravue LinkedIn company page | Reshare founder posts, case studies, offers | 2/week |
| X (@eravue + any founder handle) | Builder audience, intl founders/creators: build threads, quick takes, replies to big accounts | 1-3/day, mostly replies |
| Instagram @eravuedotcom | **Proof page** prospects check after a DM: case studies, before/after, demos, reels collabs | 3/week (reuse lifewithcofounders reels via Collab) |
| Instagram @lifewithcofounders | Founder reels: reach + trust (scripts by **lifewithcofounders**) | 3-4 reels/week |

Confirm each account's handle and login the first time and record it in `.growth/strategy.md` §Situation. If an account doesn't exist (e.g. a founder X handle), propose creating it. The founders create accounts themselves.

## Modes

| Mode | Trigger | Do |
|---|---|---|
| **profiles** | "fix our profiles", onboarding, a positioning change | Audit every profile against [profiles.md](references/profiles.md). Write exact new bios/headlines/pinned posts for approval |
| **calendar** | weekly plan, "content calendar" | Next 7 days in `.growth/content-plan/YYYY-MM.md` using [content-system.md](references/content-system.md) |
| **write** | "today's LinkedIn post", "X thread about ..." | Write post(s) ready to publish, with 2 hook options |
| **repurpose** | "turn this reel/blog/case study into posts" | One source → LinkedIn post, X thread, carousel outline, IG caption |
| **engage** | daily, "comment strategy" | 10-15 recent posts by prospects/ICP + bigger accounts in the niche, each with a drafted comment that adds something real |
| **publish** | "post 2 and 3", "post the approved ones" | [publishing-protocol.md](references/publishing-protocol.md) |
| **review** | weekly, "how did posts do" | Pull stats into growth.py content, find winners, feed lessons back |

## Tools

- **Browser:** Chrome DevTools MCP in the founders' signed-in Chrome, per `~/.claude/skills/cmo/references/browser.md`, to read profiles and post stats, find prospects' posts to comment on, and publish approved posts ([publishing-protocol.md](references/publishing-protocol.md)).
- **Visuals:** **brandkit** for case-study and carousel visual direction. Real screenshots of real work beat generated images. Label concepts as concepts.
- **Reels:** **lifewithcofounders** writes them, using **short-form-craft**.

## Rules

- **Real material only.** Builds, client work, numbers and stories must be true. Use `[REAL: …]` slots and ask the founders when you need a real detail. Never invent clients, results, screenshots or testimonials.
- **Every post has a job:** proof (we can do it), demo (here's how it works), insight (we know the problem), story (we're real people), or offer (here's how to work with us; max 1 in 5).
- **Write for the buyer, not for other marketers.** A dental clinic owner and a US HVAC owner should understand every line.
- **No engagement bait, pods, follow-for-follow or bought followers.** They wreck reach and trust.
- **Publishing is gated:** nothing posts without approval in chat this session (see the protocol).
- **Log everything:** each published post → `growth.py content add`. Update stats at 48h and 7 days.
