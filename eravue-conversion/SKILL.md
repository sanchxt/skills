---
name: eravue-conversion
description: Turns eravue.com visitors and local searchers into enquiries, and proves it with tracking. Owns conversion tracking (Umami events for forms, WhatsApp, phone, email and CTA clicks, UTM links), conversion-rate fixes on the site (CTAs, proof, contact flow, offer and landing pages, case-study pages), Google Business Profile, free directory listings (Clutch, GoodFirms, DesignRush) and review collection. Use for "are we tracking leads", "why no enquiries from the site", "add a landing page for the WhatsApp offer", "improve the contact page", "add a case study page", "fix our Google Business Profile", "get reviews", "list us on Clutch", UTM links for campaigns, or a site conversion audit.
---

# Eravue conversion

The site and the Google listing are where every channel lands: a DM prospect checks the site, an Upwork client clicks the portfolio, a local owner finds the Maps listing. Your job is to make each of those visits more likely to become a WhatsApp message, call or form, and to **measure it**.

## Before anything

1. Read `CLAUDE.md` in the repo (pnpm, ast-grep `asg`, SOLID/modular code, accessibility, ask before assuming) and `.seo/project-profile.md` (stack, routes, deploy).
2. `~/.claude/skills/eravue-outreach/references/eravue-profile.md`: proof you may use and claims to avoid.
3. `.growth/strategy.md`: current offers and beachheads (landing pages follow these).
4. The numbers: `python ~/.claude/skills/eravue-metrics/scripts/growth.py pull umami && python ~/.claude/skills/eravue-metrics/scripts/growth.py history site.conversions_7d`.

## Modes

| Mode | Do |
|---|---|
| **audit** | Check tracking works ([tracking.md](references/tracking.md) §Verify), then walk the key pages against [cro.md](references/cro.md). Output a ranked fix list in `.growth/conversion/audit-YYYY-MM-DD.md` (impact × effort). |
| **tracking** | Add or repair events, generate UTM links for a campaign. |
| **fix** | Implement approved CRO changes in the codebase. |
| **landing** | Build an offer or niche landing page (e.g. `/whatsapp-lead-follow-up-for-clinics`) from the approved offer in eravue-sales `offers.md`. |
| **case-study** | Turn `.growth/case-studies/<client>.md` into a site page + portfolio entry, once the client has approved it. |
| **local** | Google Business Profile, directories, reviews ([local-presence.md](references/local-presence.md)). |

## Shipping site changes

- Work in the repo with the project's conventions: Astro 5 + React islands + Tailwind 4, data in `src/data/`, constants in `src/config/site.ts`, SEO via `SeoHead` + `src/lib/seo/`. Reuse components. Keep pages accessible (labels, focus states, contrast) and responsive.
- Verify locally: `pnpm build`, then preview with the `.claude/launch.json` dev server and the browser tools. Check the change, the console, mobile width, and that tracking events fire (§Verify in tracking.md).
- **Deploys need approval:** pushing to `main` deploys to the VPS via the "Deploy to VPS" workflow. Show the diff summary and ask before committing and pushing. Commit style: see `memory/feedback_commit_style.md` in the repo if present.
- After the deploy: re-verify on https://eravue.com and add a dated line to `.growth/strategy.md` §Learnings or the audit file, so later changes in conversion rate can be attributed.

## Tools

- **Browser:** per `~/.claude/skills/cmo/references/browser.md`. Chrome DevTools MCP for Google Business Profile, directory dashboards and Search Console (slot `/u/2/`). The built-in browser preview (`.claude/launch.json`, name `eravue-dev`) for checking local site changes.
- **Design and build:** landing and case-study pages are built inside the existing design system and components. No one-off styles that break the site.
- **Code search:** ast-grep (`asg`) for structural searches, per CLAUDE.md.

## Principles

- **Measure first.** No CRO change without tracking that can show whether it worked.
- **Small samples:** at Eravue's traffic (tens of humans a week), A/B tests can't reach significance. Make clear best-practice fixes, then watch conversions per 100 human visitors over weeks.
- **One primary action per page.** WhatsApp for India, "book a call" for international, with the form as the alternative.
- **Proof near every CTA.** Real client names/logos, the Emson testimonial, products built. No invented stats or reviews.
