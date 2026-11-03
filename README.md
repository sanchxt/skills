# Skills

Private backup and source repository for Sanchit's personal Claude Code skills, mirrored from:

```text
C:\Users\Sanchit\.claude\skills
```

These were originally Codex skills. They were migrated to Claude Code in November 2026: Codex-only `agents/openai.yaml` files were removed and Codex-specific wording and paths were updated. Earlier Codex versions remain in git history.

## Short-form content skills (rebuilt from scratch, Nov 2026)

| Folder | Purpose |
| --- | --- |
| `short-form-craft` | Shared engine: format menu, hook archetypes, retention and pacing, human-voice / anti-AI-tells pass, scroll-test critic, platform notes. Every account skill reads it. |
| `founderspawn` | FounderSpawn YouTube Shorts: multi-voice VC skits (about anything), real VC clip cuts, brainrot narration, horror over gameplay. ElevenLabs v3 formatting. |
| `editsogoated` | EditSoGoated hard edits: angle, hook frame, song, beat map, clip list. |
| `lifewithcofounders` | LifeWithCofounders Instagram: AI-native founders. Big news breakdowns, result → how to build it, build-in-public, takes, series. Owns business-helping builds. |
| `sanchitafeels` | SanchitaFeels: explore-grade text reels, voiceover lists, psychology with a jolt, theories. Varied beyond Indian-relatable. |
| `sanchitwtf` | sanchitwtf: AI experiments, "how I made this" tutorials, "I Build What You Comment" series. |

Each account skill has a `log.md`. Add post results there so the skill learns what works.

## Other skills

| Folder | Skill name | Purpose |
| --- | --- | --- |
| `boss-lobbies-fish-voiceover` | `boss-lobbies-fish-voiceover` | Voiceover scripts (inactive account). |
| `brandkit` | `brandkit` | Premium brand kit and visual identity generation. |
| `bug-finder` | `bug-finder` | Rigorous implementation review and bug finding. |
| `chrome-devtools-cli` | `chrome-devtools-cli` | Chrome DevTools CLI usage. |
| `cmo` | `cmo` | CMO-style marketing, social strategy, and content workflows. |
| `dailygoatgame` | `dailygoatgame` | Gaming Shorts planning (inactive account). |
| `gpt-tasteskill` | `gpt-taste` | Advanced UX/UI and GSAP motion direction. |
| `grill-me` | `grill-me` | Relentless design and plan interrogation. |
| `image-to-code-skill` | `image-to-code` | Image-first website implementation guidance. |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | Premium mobile app screen image direction. |
| `imagegen-frontend-web` | `imagegen-frontend-web` | Premium website design reference generation. |
| `instagram-opportunity-finder` | `instagram-opportunity-finder` | Instagram prospect discovery and compliant outreach prep. |
| `interview` | `interview` | Persistent clarification and requirement gathering. |
| `reddit-demand-capture` | `reddit-demand-capture` | Reddit demand capture research and response drafting. |
| `reddit-opportunity-finder` | `reddit-opportunity-finder` | Fresh Reddit lead and pain-point discovery. Note: references a `lead_memory.py` that is not in this repo. |
| `saas-ideation` | `saas-ideation` | Current-market SaaS and app ideation for solo builders. |
| `seo` | `seo` | SEO strategy, audits, keyword research, and content planning. |
| `taste-skill` | `design-taste-frontend` | Senior UI/UX design engineering guidance. |
| `twitter-opportunity-finder` | `twitter-opportunity-finder` | X/Twitter opportunity discovery. Note: references a `lead_memory.py` that is not in this repo. |

## Restore

Copy a skill folder into your Claude Code skills directory:

```powershell
Copy-Item -Recurse .\skill-folder C:\Users\Sanchit\.claude\skills\
```
