# Codex Skills

Private backup and source repository for manually created Codex skills.

This repository intentionally contains only the user-created skills from:

```text
C:\Users\tpbea\.codex\skills
```

Excluded sources:

- `.system` skills bundled by Codex
- plugin cache skills
- generated runtime caches, databases, and workspace output

## Skills

| Folder | Skill name | Purpose |
| --- | --- | --- |
| `brandkit` | `brandkit` | Premium brand kit and visual identity generation. |
| `bug-finder` | `bug-finder` | Rigorous implementation review and bug finding. |
| `cmo` | `cmo` | CMO-style marketing, social strategy, and content workflows. |
| `gpt-tasteskill` | `gpt-taste` | Advanced UX/UI and GSAP motion direction. |
| `grill-me` | `grill-me` | Relentless design and plan interrogation. |
| `image-to-code-skill` | `image-to-code` | Image-first website implementation guidance. |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | Premium mobile app screen image direction. |
| `imagegen-frontend-web` | `imagegen-frontend-web` | Premium website design reference generation. |
| `instagram-opportunity-finder` | `instagram-opportunity-finder` | Instagram prospect discovery and compliant outreach prep. |
| `interview` | `interview` | Persistent clarification and requirement gathering. |
| `minecraft-shorts-producer` | `minecraft-shorts-producer` | Minecraft Shorts ideation, ElevenLabs scripts, production direction, packaging, and growth testing. |
| `reddit-demand-capture` | `reddit-demand-capture` | Reddit demand capture research and compliant response drafting. |
| `reddit-opportunity-finder` | `reddit-opportunity-finder` | Fresh Reddit lead and pain-point discovery. |
| `saas-ideation` | `saas-ideation` | Current-market SaaS and app ideation for solo builders. |
| `seo` | `seo` | SEO strategy, audits, keyword research, and content planning. |
| `taste-skill` | `design-taste-frontend` | Senior UI/UX design engineering guidance. |
| `twitter-opportunity-finder` | `twitter-opportunity-finder` | X/Twitter opportunity discovery and outreach prep. |
| `viral-story-shorts` | `viral-story-shorts` | Retention-focused short-form story scripting, production, packaging, and iteration guidance. |

## Layout

Each top-level directory is one Codex skill. Supporting instructions live inside that skill directory in `references`, `rules`, `agents`, or `scripts` folders when present.

To restore a skill, copy its directory into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skill-folder C:\Users\tpbea\.codex\skills\
```
