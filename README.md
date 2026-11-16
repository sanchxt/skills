# Skills

Backup and source repository for Sanchit's personal Claude Code skills, an exact mirror of:

```text
C:\Users\Sanchit\.claude\skills
```

The `cmo` and `eravue-*` skills are symlinks locally (their source lives in the eravue-portfolio repo under `.claude/skills/`); they are copied here as plain folders.

These were originally Codex skills, migrated to Claude Code in November 2026. Earlier Codex versions, and skills that have since been removed locally, remain in git history.

## Eravue agency skills

| Folder | Purpose |
| --- | --- |
| `cmo` | Eravue's CMO and head of growth: plans, channel and budget decisions, delegates to the sub-skills below, weekly reviews. |
| `eravue-outreach` | Finding clients and drafting outreach (Reddit, X, LinkedIn, Upwork, Google Maps, email, WhatsApp) with a lead tracker. |
| `eravue-instagram` | Instagram prospecting, profile audits, cold DMs, sending approved DMs. |
| `eravue-sales` | Offers and pricing, discovery calls, objections, proposals, closing, onboarding, upsells. |
| `eravue-social` | Founder-led LinkedIn, X and Instagram: content calendar, posts, profile fixes, publishing approved posts. |
| `eravue-conversion` | Site conversion tracking (Umami), CRO fixes, Google Business Profile, directories, reviews. |
| `eravue-metrics` | Growth scoreboard and ledger: revenue, funnel, site, search and social numbers. |
| `eravue-blog` | Write, schedule and publish posts on the eravue.com blog through its CLI. |
| `eravue-motion` | Motion-graphics videos end to end (Remotion): script, looks, motion, captions, voice, music, formats, QA, master. |
| `blog-writer` | SEO blog autopilot: research, pick a topic, write, quality gate, publish. |
| `seo` | SEO + AI-search strategy: audits, Search Console, keyword research, content, links. |

## Short-form content skills

| Folder | Purpose |
| --- | --- |
| `short-form-craft` | Shared engine: format menu, hook archetypes, retention and pacing, human-voice / anti-AI-tells pass, scroll-test critic, platform notes. Every account skill reads it. |
| `founderspawn` | FounderSpawn YouTube Shorts: multi-voice VC skits, real VC clip cuts, brainrot narration, horror over gameplay. |
| `editsogoated` | EditSoGoated hard edits: angle, hook frame, song, beat map, clip list. |
| `lifewithcofounders` | LifeWithCofounders Instagram: AI-native founders, news breakdowns, how-to-build-it, build-in-public. |
| `sanchitafeels` | SanchitaFeels: text reels, voiceover lists, psychology, theories. |
| `sanchitwtf` | sanchitwtf: AI experiments, "how I made this" tutorials, community series. |
| `dailygoatgame` | Gaming Shorts planning (inactive account). |
| `boss-lobbies-fish-voiceover` | Gaming voiceover scripts for TTS (inactive account). |

Each account skill has a `log.md`. Add post results there so the skill learns what works.

## Research and other skills

| Folder | Purpose |
| --- | --- |
| `instagram-opportunity-finder` | Instagram prospect discovery and compliant outreach prep. |
| `reddit-demand-capture` | Reddit demand-capture research and response drafting. |
| `reddit-opportunity-finder` | Fresh Reddit lead and pain-point discovery. |
| `twitter-opportunity-finder` | X/Twitter opportunity discovery. |
| `saas-ideation` | Validated product ideas for a solo AI-assisted builder. |
| `brandkit` | Premium brand kit and visual identity generation. |
| `chrome-devtools-cli` | Chrome DevTools CLI usage. |
| `grill-me` | Relentless design and plan interrogation. |
| `interview` | Persistent clarification and requirement gathering. |

## Restore

Copy a skill folder into your Claude Code skills directory:

```powershell
Copy-Item -Recurse .\skill-folder C:\Users\Sanchit\.claude\skills\
```
