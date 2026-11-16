# Writing an Eravue post

Eravue is Sanchit and Sanchita's AI automation, web, app, CRM/ERP, design, social media, video and content studio. The blog exists to win organic traffic in India (and international) that turns into enquiries. Read `.seo/project-profile.md` and `@docs/PURPOSE.md` once per session for audience and positioning. If the topic or keyword isn't settled, run the `seo` skill for research first.

## What a good post here looks like

- **Answers the searcher's question in the first 2–3 sentences**, then earns the rest of the read. No throat-clearing intros.
- **Specific to the reader's world**: Indian SMBs and startups. Use INR price ranges, GST, WhatsApp, UPI, Indian tools and examples where relevant, but don't force India into a topic that's global.
- **Concrete numbers, ranges and examples** over adjectives. If you state a price, statistic or fact, it must be true and current. Verify recent figures on the web, and add a short "Sources" line with links for non-obvious claims. Never invent stats, clients, case studies or quotes. Eravue has no client case studies to cite yet; don't imply otherwise.
- **Plain voice**: direct, warm, no hype words ("revolutionary", "game-changer", "in today's fast-paced world", "unlock", "delve", "elevate"). Short paragraphs (1–4 sentences). Write like an expert explaining to a smart business owner.
- **Scannable**: H2 every ~200–350 words, H3 for sub-points, lists and tables where they genuinely help (comparisons, costs, checklists).
- **Length follows intent**: ~1,200–2,000 words for guides/comparisons, shorter for news or quick answers. Don't pad.

## Structure template

```markdown
---
title: "…"                      # natural headline, can exceed 60 chars
slug: "keyword-led-short-slug"
excerpt: "One or two sentences that make someone want to read it."
category: website-development   # existing slug (pnpm blog categories)
tags: [ "Primary keyword phrase", "Secondary topic" ]
metaTitle: "… | Eravue"          # ≤ 70, primary keyword near the start
metaDescription: "…"             # 140–160, benefit + keyword, no clickbait
metaKeywords: "primary keyword, variant, variant"
status: draft
---

# Title

Direct answer / hook (2–3 sentences).

## Key takeaways            ← 3–5 bullets; great for AI search (GEO) and skimmers

## H2 sections that each answer one sub-question

## FAQ                       ← 3–6 real questions (People Also Ask style), short answers

## Next step                 ← one natural line pointing to the relevant service or /contact
```

The page already adds a category-matched CTA block after the post, so keep the in-text pitch to one or two sentences.

## SEO and AI-search checklist

- Primary keyword in: slug, metaTitle (near the start), first 100 words, at least one H2, and naturally a few more times. No stuffing.
- Question-style H2/H3s where they match how people search ("How much does X cost in India?").
- Self-contained, quotable answer paragraphs under each heading (helps Google snippets and AI answers).
- **Internal links (3–6)**: other relevant published posts (`pnpm blog list --status published --limit 100`) and service pages:
  - `/service/detailed/custom-website-development`
  - `/service/detailed/web-mobile-app-development`
  - `/service/detailed/custom-crm-development`
  - `/service/detailed/custom-erp-business-systems`
  - `/service/detailed/brand-identity-uiux-design`
  - `/service/detailed/seo-digital-marketing-services`
  - `/service/detailed/social-media-marketing`
  - `/service/detailed/video-editing-content-creation`
  - `/service/detailed/ai-automation-workflows`
  - `/service/detailed/ai-customer-support-agents`
  - `/service/detailed/ai-voice-agents`
  - `/service/detailed/ai-content-production`
  - `/service/detailed/lead-generation-automation`
  - `/services`, `/contact`
  
  Verify a service slug still exists in `src/data/services/` before linking.
- 1–3 external links to authoritative sources when citing facts.
- Every image has descriptive alt text (what it shows, not "image of").
- Don't duplicate an existing post's target keyword. Update the existing post instead and tell the user.

## Updating posts

When refreshing an article (new prices, new year), update the facts, the title/meta if they contain a year, and keep the slug unless the user asks otherwise. Changing a live slug breaks its URL.
