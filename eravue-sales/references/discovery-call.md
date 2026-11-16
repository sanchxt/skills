# Discovery calls, follow-ups and objections

## Getting the call

When a lead replies with interest, the reply has one job: a time. Offer two specific slots ("Thu 11am or Fri 4pm IST?"), or WhatsApp voice call for Indian SMB owners, who often prefer it to Zoom. Keep it at 15-20 minutes. If they want info first, send a 2-minute demo video plus the one relevant proof, then ask for the slot again.

## Call prep file: `.growth/sales/<ID>.md`

```markdown
# L0007 · Smile Dental, Gurgaon · call Thu 2026-11-14 11:00 IST · Sanchit
## What we know (with sources)
- Site: ..., Instagram: ..., Google rating 4.6 (212 reviews), "call for appointment" only, no WhatsApp link
- Signal that started this: ...
## Likely pains (to confirm, not assume)
## Questions (in order)
## Offer to steer toward + price (from offers.md, status)
## Demo to show (link)
## Likely objections + answers
## Desired outcome of the call
```

## Call structure (15-20 min)

1. **Frame (1 min):** "15 minutes: I'll ask about how enquiries come in today, then show you what we'd do, and you decide if it's worth a next step. Fair?"
2. **Situation (4 min):** How do customers reach you? Who replies, and how fast? What happens after 8pm or on Sundays? What tools do you use (WhatsApp, Excel, CRM)?
3. **Pain + cost (4 min):** How many enquiries a week? How many go cold? What's a customer worth to you? "So roughly how much is slipping through each month?" Let them do the maths. Use their number in the proposal.
4. **Vision (2 min):** "If every enquiry got a reply in a minute and a follow-up until they booked, what would that change?"
5. **Show (3-4 min):** a short demo of the exact thing (screen share or the demo video).
6. **Decision process (1 min):** Who else decides? When would you want this live? Any budget in mind?
7. **Close the next step (1 min):** "I'll send a one-page plan with a fixed price by tomorrow 6pm. If it makes sense, we can start Monday and have it live within a week." Book the follow-up time on the call.

Founder tone: plain, honest, curious. Saying "honestly, you don't need AI for this, here's the simple fix" builds trust and often wins the deal anyway.

## After the call (same day)

- `leads.py update <ID> --status proposal|replied|lost --next-due ... --note "..."` with the key facts (pain, numbers, decision-maker, timeline).
- Thank-you message with a 3-line recap of what they said, then the proposal within 24 hours.
- Follow-ups after the proposal: day 2 (a useful extra, like an idea or example), day 5 (a direct question: "should I hold the Monday start slot?"), day 10 (a polite close: "should I close this out for now?").

## Objections

| They say | Respond (adapt; never pushy) |
|---|---|
| "Too expensive" | "Compared to what? If it saves even one customer a month at ₹X, it's paid for itself." Then offer a smaller scope (Quick Start) rather than a discount on the same scope. |
| "Send me details / I'll think about it" | "Of course. What would you need to see to say yes or no?" Send the proposal and book the follow-up time now. |
| "We already use WhatsApp / have someone" | "Great, we'd build on that, not replace it. Where does it break today: nights, follow-ups, tracking?" |
| "AI will sound robotic / annoy customers" | Show the demo. The AI handles the first reply and qualifies; humans take over. They control the wording. |
| "We tried an agency before and it failed" | Ask what went wrong. Offer a 7-day sprint with a fixed price and a visible result before any retainer. |
| "You're new / no big clients" | "True, that's why you get the two founders directly, a fixed price, and we only get paid the second half when it works." Show the products they built. |
| "Not now" | Ask when. Set a dated follow-up. Offer something free and useful in the meantime (a mini audit). |
| International: "Can you work in our time zone?" | Yes. Name the overlap hours and give an async update cadence. |
