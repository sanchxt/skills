# Upwork: profile, catalog and the daily proposal routine

**Researched:** 2026-11-11 · **Sources:** [levelupupwork.com (specialized profiles removed)](https://www.levelupupwork.com/blog/upwork-specialized-profiles-removed-what-to-do), [levelupupwork.com checklist](https://www.levelupupwork.com/blog/upwork-profile-optimization-checklist-2026), [up-bro.com](https://up-bro.com/blog/upwork-profile-optimization-2026), [freelancingnetwork.org](https://www.freelancingnetwork.org/upwork-profile-optimization-2026-niche-density-skills-and-the-end-of-specialized-profiles/), [fulltimenomad.com](https://www.fulltimenomad.com/upwork-profile-not-approved/), [Upwork: profile types](https://support.upwork.com/hc/en-us/articles/34486700887059-What-are-the-profile-types-on-Upwork-and-how-are-they-different), [Upwork: agency profile](https://www.upwork.com/resources/how-to-craft-an-impressive-agency-profile-on-upwork), [Upwork: Rising Talent](https://www.upwork.com/resources/how-to-get-rising-talent-badge), [Upwork: boosted proposals](https://www.upwork.com/resources/how-to-boost-proposal), [golance.com fees](https://golance.com/blogs/upwork-fees-explained-2026).

Mostly third-party guides, so **verify against the live profile editor before writing** (field limits, skill count, catalog options). If anything below doesn't match what the editor shows, trust the editor and update this file. Re-check after 90 days.

## What changed in 2026 (verify)
- **Specialized profiles were retired** (reported 2026-05-28). There is one main profile now. Its title and overview carry the search weight.
- **Project Catalog** is the way to present several fixed-price offers: each item has its own title, description, tiers and search surface.
- Title: about 70 characters. Overview: the first ~250 characters show in search and decide the click. Skills: 15-20 slots (sources disagree).
- Connects cost $0.15 each; a proposal costs about 6-32 Connects depending on the job. Freelancer Plus is about $19.99/month for 100 Connects. Boosting a proposal costs extra Connects (auction).

## Account plan
1. **Sanchit's freelancer profile first.** An agency profile needs an owner with a linked freelancer profile, and early jobs build that profile's history. Use real name, real photo, accurate location (India), and pass identity verification.
2. **Eravue agency profile later**, once there are 2-3 completed jobs: name, logo, tagline, overview, Sanchita added as a member. Agencies may get a Rising Talent badge by invitation, so check eligibility in the account.
3. One person, one account. Never a second account.

## Getting approved
New profiles are sometimes rejected or held, usually for incomplete profiles, vague broad positioning, crowded generic categories ("web developer") or rates far off the market. So:
- Pick a **specific niche** in the title and category (AI automation / workflow automation is less crowded than generic web development).
- Fill **everything**: photo, title, overview, skills, rate, portfolio (3+ items), employment (Eravue co-founder), education, languages (honest levels), linked LinkedIn/GitHub.
- Set the hourly rate inside the range Upwork suggests for the category.
- If rejected: read the reason, improve the weakest part (usually portfolio or overview), resubmit, or contact Upwork support. Don't create a new account.

## Profile copy (write to `.growth/upwork/profile.md`; the founders paste it in)

**Title** (keyword first, under 70 chars), options like:
- "AI Automation Expert | n8n, Make, WhatsApp & AI Agents"
- "AI Automation & Lead Follow-up | n8n, Zapier, AI Chatbots"

**Overview** structure:
1. **Hook, ~250 chars:** the outcome for the buyer. "I build AI automations that answer every lead in under a minute and follow up until they book, plus the fast websites and dashboards around them."
2. **What I build** (4-6 bullets in buyers' words): WhatsApp/Instagram/website AI chat agents · lead capture → CRM → follow-up flows (n8n, Make, Zapier) · AI voice receptionists and missed-call text-back · fast websites and landing pages · internal tools and dashboards.
3. **Proof (real only):** past clients (Emson Designs, Bestor, DevLabs Alliance, Astro Shades, Caketastic, Yoop), the 3 AI products built and run (Note Me Please, MyContent, Daysfold), and "30+ businesses helped".
4. **How I work:** a fixed scope before starting, daily updates, a short handover video, founders do the work themselves.
5. **CTA:** "Message me with what you want automated. I'll reply with a quick plan."

**Skills** (fill all slots, most relevant first): n8n, Make.com, Zapier, AI Chatbot Development, AI Agent Development, WhatsApp API, Workflow Automation, API Integration, OpenAI API, Voice AI / AI receptionist, CRM Development, GoHighLevel (only if the founders can deliver it), Landing Page, Website Development, Astro / React, Next.js, JavaScript, Python. Check each against what the founders can really deliver.

**Rate:** lower-middle of Upwork's suggested range for the category during the sprint. Raise after 3 five-star reviews. Fixed-price jobs follow `eravue-sales/references/offers.md` (international table).

**Portfolio items** (3-6, only real work, each with problem → what we built → result if measured, plus screenshots): Emson Designs website, Note Me Please, MyContent, Daysfold, Yoop landing page, plus one automation demo the founders build (a WhatsApp lead follow-up flow in n8n, recorded). A demo is fine as long as it's labelled as a demo.

**Intro video** (optional, 60-90 s script): who you are → what you build for whom → a 10-second screen clip of a real automation → how to start.

## Project Catalog (2-4 items, from APPROVED international offers only)

| Catalog item | Tiers (example structure; prices from offers.md) |
|---|---|
| "I will set up a missed-call text-back and AI receptionist for your business" | Basic: text-back only · Standard: + AI FAQ answers · Premium: + booking + CRM ($299 setup anchor) |
| "I will build an n8n/Make automation for your leads or workflow" | 1 workflow · 2-3 workflows · full lead pipeline |
| "I will build a fast landing page or 5-page website in 7 days" | 1 page · 5 pages ($499 anchor) · 5 pages + CRM/WhatsApp integration |
| "I will edit 8 short-form videos per month" | 4 · 8 ($199/mo anchor) · 16 |

Gap (2026-11-11): offers.md has no fixed international price for a single automation workflow (only the $150 paid discovery). Propose tier prices to the founders before publishing that catalog item.

Each item: a keyword-first title, a description (problem → what's included → timeline → what we need from you), clear revision limits and delivery days, and real screenshots.

## Daily proposal routine (inside eravue-outreach daily/hunt)
1. **Find:** [inbound-channels.md](inbound-channels.md) §Upwork searches, newest first, in the founders' Chrome via DevTools MCP.
2. **Filter:** posted <24h, <10-15 proposals, payment verified, scope fits an offer, no red flags (unpaid "test tasks", off-platform requests). Note the Connects cost.
3. **Dedupe + track:** `leads.py check <job url>`, then `add --channel upwork --kind inbound --signal "<budget, scope>" --notes "connects: N"`.
4. **Draft:** proposal per [messaging.md](messaging.md) (under 150 words, their goal → 3 steps → 1 proof link → one smart question), screening answers, suggested bid (fixed: inside their budget and at or above our floor; first 3 jobs may go slightly lower to earn reviews), and a Loom script for the top 1-2 jobs.
5. **Approval list:** in the daily brief, list each job with link, Connects cost and bid. The **founders submit** (it spends Connects). Then `leads.py update <ID> --touch --note "proposal submitted, N connects"`.
6. **Boosting:** not in month 1 unless a job is a perfect fit and fresh. Judge boosts by interviews per Connect spent.
7. **Track outcomes:** interview/message → `replied`; call → `call_booked`; offer → `proposal`; hired → `won` + `growth.py deal add --channel upwork`. Weekly: proposals sent, Connects spent, views, interviews, hires (`growth.py record social.upwork.proposals_7d=... social.upwork.connects_spent_7d=... social.upwork.interviews_7d=...`).

## Rules (Upwork terms; breaking them gets accounts suspended)
- **No automated edits on Upwork, even with founder approval** (2026-11-16): while the CMO was editing skills via DevTools MCP, Upwork's bot protection started returning 403 on `findSkills` after a few automated inputs. Read-only checks of the profile are fine. Every edit, proposal and message is done by hand by the founders, with copy from us.
- No contact details or off-platform links/payment talk before a contract exists; keep communication on Upwork until hired.
- Never ask for or offer anything in exchange for feedback, and never review-swap. Asking a happy client to leave honest feedback at the end is fine.
- Proposals are written for each job, never copy-paste spam.
- Don't misstate location, skills, language level or experience.
