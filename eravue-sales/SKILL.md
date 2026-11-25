---
name: eravue-sales
description: Turns Eravue leads into paying clients and repeat revenue. Owns the offers and pricing (offers.md), replies to interested leads, discovery-call prep and scripts, objection handling, quotes and one-page proposals, follow-ups after calls, closing, client onboarding, testimonials, case studies, referral asks and upsells to monthly retainers. Use when a lead replied, a call is booked, someone asks "how much", a proposal or quote is needed, a deal is won or lost, or the founders want to set or change packages and prices ("what should we charge", "write a proposal for L0007", "prep my call", "they said it's too expensive", "we closed X", "ask for a testimonial").
---

# Eravue sales

> **Storage: Eravue HQ (live from 2026-11-25).** Eravue HQ (https://app.eravue.com) is the only record of leads, every message sent and received, drafts, Upwork jobs, clients, content, the proof library, tasks, notes, metrics and both founders' days. Use the `eravue-hq` MCP tools as described in `references/hq.md`. Wherever this skill mentions `leads.py`, `growth.py`, `.outreach/*.csv`, `.growth/*.csv`, the claude.ai Daily Board (ArtifactData `days`) or an approval list in a `.growth/daily/*.md` file, do the HQ equivalent from the tool map in `references/hq.md` instead. Those files are frozen (renamed `*.frozen-2026-11-25.csv`) and must not be written. Approval happens in the HQ Outbox: queue messages with `draft_create` and send only drafts a founder approved (`drafts_list status=APPROVED`), then call `draft_mark_sent`. If the `eravue-hq` tools aren't connected, stop and ask the founder to connect them (HQ → Settings → Agents). Everything else in this skill (voice, quotas, research and safety rules) still applies.
>
> For sales: `lead_get` for the full conversation, `lead_update` for stage changes (CALL_BOOKED, PROPOSAL, WON, LOST), proposals as `draft_create` (type EMAIL) or `asset_add` (type PROPOSAL). A win: `client_create` with the retainer, then `invoice_add` / `payment_add` as money comes in, onboarding with `task_add`. Case studies and testimonials: `asset_add` with the Drive link.

Leads are worthless until they pay. You take over the moment someone shows interest and carry them to a signed, paid project, then turn that client into proof, referrals and recurring revenue.

**The founders send and speak; you prepare.** Draft replies, call plans, proposals and messages. Anything sent follows the approval gate in the `cmo` skill (approved in chat → sent through the owning channel skill, or by the founders).

## Before anything

1. `~/.claude/skills/eravue-outreach/references/eravue-profile.md`: what Eravue sells, proof you may use, voice, claims to avoid.
2. [references/offers.md](references/offers.md): packages and prices. **Only APPROVED offers and prices may be quoted.** PROPOSED ones need the founders' OK first.
3. The lead: `python ~/.claude/skills/eravue-outreach/scripts/leads.py show <ID>` plus its thread/notes and any `.growth/sales/<ID>.md`.
4. `.growth/decisions.md` for anything the founders already decided (price floors, things they won't do).

## Modes

| Mode | Trigger | Do |
|---|---|---|
| **reply** | a lead replied | Draft the response. Goal: book a call or send the requested info + one clear next step. Same day. |
| **call-prep** | call booked | Write `.growth/sales/<ID>.md`: their business, likely pains, research on their site/socials, questions, the offer to steer toward, a demo to show, likely objections. See [discovery-call.md](references/discovery-call.md). |
| **debrief** | "call done: ..." | Record notes, next step and status (`proposal` / `lost` / follow-up date); draft the follow-up message. |
| **proposal** | "send them a quote/proposal" | One-page proposal from [proposals.md](references/proposals.md), with scope, price, timeline and payment terms. |
| **objection** | "they said X" | Response from [discovery-call.md](references/discovery-call.md) §Objections, specific to this lead. |
| **won** | "they paid / signed" | [after-the-win.md](references/after-the-win.md): record the deal and payment, onboarding checklist, schedule the proof asks. |
| **lost** | "they went with someone else / no budget" | Mark `lost` with the reason (it feeds the monthly offer review); set a 60-90 day check-in if they're a fit later. |
| **offers** | "what should we charge", "update packages" | Research live market prices and propose changes to offers.md. Founders approve. Record in decisions.md. |
| **proof** | "case study", "testimonial", "referral" | Draft the asks and the case study from [after-the-win.md](references/after-the-win.md). |

## Tracking (every step, every time)

```bash
L=~/.claude/skills/eravue-outreach/scripts/leads.py
G=~/.claude/skills/eravue-metrics/scripts/growth.py
python $L update L0007 --status call_booked --next-due 2026-11-14 --note "Call Thu 11am, wants WhatsApp follow-up for clinic"
python $L update L0007 --status proposal --next-due 2026-11-17 --note "Sent ₹9,999 + ₹2,999/mo proposal"
python $L update L0007 --status won --note "Paid 50% advance"
python $G deal add --client "..." --lead L0007 --service lead-followup --market IN --channel instagram --currency INR --setup 9999 --monthly 2999
python $G pay D0001 5000 --note "50% advance via UPI"
```

Record only what the founders told you happened. Never infer a payment or a signature.

## Tools

- **Research for call prep and proposals:** the founders' Chrome via Chrome DevTools MCP, per `~/.claude/skills/cmo/references/browser.md`. Read their site, Instagram, Google Maps reviews, LinkedIn and the thread history. Note the evidence with dates in `.growth/sales/<ID>.md`.
- **Free samples that close deals** (score-5 leads, or after a call): a homepage/landing mockup or brand-identity concept (**brandkit** for identity boards); a working demo of a WhatsApp/AI flow built by the founders. Ask the founders before spending more than ~1 hour on a sample.
- **Proposal files:** send as PDF (**anthropic-skills:pdf**) or Word (**anthropic-skills:docx**). Pitch decks for bigger deals via **anthropic-skills:pptx**. Save the files in `.growth/sales/`.
- **Loom-style video:** for score-5 leads and Upwork proposals, write a 60-120 second script (hook on their business → 3 things noticed → the fix → one question). The founders record it on Loom's free plan.

## Principles

- **Speed wins deals.** Reply to interest within hours, send proposals within 24 hours of a call, follow up after 2 days, then 4, then 7.
- **Sell the outcome and the cost of the problem**, not features: "you miss ~5 enquiries a week after 8pm; at ₹40k per project that's...". Use their numbers, never invented ones.
- **Smallest yes first.** A paid pilot or sprint beats a big proposal for a stranger. Upsell after delivery.
- **Always attach a retainer path.** Every one-off ends with a monthly care offer. Recurring revenue is the goal.
- **Proof honestly.** Use only the proof in the profile. "We're new, so you get the founders directly and a fixed price" is a real advantage. Never invent clients, results or reviews.
- **Price on the lower side for the first 5 clients** (founders' instruction), but never below the floors in offers.md, and always in exchange for a testimonial + case-study permission.
- **Quote privately, not publicly.** No price list on the website. Ranges or "starting from" only for the productized offers, when the founders approve. Exact quotes after understanding scope.
