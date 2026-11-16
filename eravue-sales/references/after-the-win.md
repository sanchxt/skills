# After the win: onboarding, proof, referrals, retainers

The first clients are worth far more than their fees. Each one should produce: a happy client, a testimonial, a case study, a review, a referral ask, a reel, and ideally a retainer.

## The moment they say yes

1. `leads.py update <ID> --status won --note "..."` and `growth.py deal add ...`. Record the payment with `growth.py pay` only once the money has arrived.
2. Onboarding message (same day): a thank-you, what happens next, what we need from them (logins, logo, content, access), the kickoff time.
3. Create `.growth/clients/<client-slug>.md`: scope, dates, contacts, access checklist, delivery log, results baseline (**measure the "before"**: reply time, enquiries/week, site speed, follower count). Without a baseline there's no case study.
4. Tell the CMO (daily brief): delivery time is now reserved in the week's plan. Delivery quality beats new outreach.

## During delivery

- Over-communicate: a short update every 2 days, a demo video before go-live.
- Ship early when possible ("live in 5 days" beats "live in 7").
- Ask permission early: "Mind if we share the before/after (no private data) once it's live?"

## At go-live (the high moment, so ask now)

1. **Handover:** a 3-5 minute walkthrough video plus a one-page "how to use it".
2. **Testimonial ask** (same day or the next):
   > "Really glad it's live! Would you mind sending a 2-3 line note (or a 30-sec video) on what it was like working with us and what's changed? It helps a small team like ours a lot."
   Make it easy: offer a draft from their own words for them to edit. Only their real words get published.
3. **Google review ask** with the direct review link (eravue-conversion has it).
4. **Retainer offer:** "To keep it tuned and to add [next thing], our monthly care is ₹Y. Want me to switch it on from next month?"
5. **Referral ask** (after a visible win, usually 1-2 weeks in):
   > "Who else do you know who [has the same problem]? If you intro us and they start, [thank-you: a month of care free / a referral fee the founders approved]."

## Case study (2-4 weeks after go-live, once there are results)

Save to `.growth/case-studies/<client>.md`, then hand to eravue-conversion (site page/portfolio), eravue-social (LinkedIn post + carousel), lifewithcofounders (build-in-public reel), and add it to eravue-profile.md §Proof.

```markdown
# [Client]: [result in one line, with a real number]
- Client, industry, city · what they do
- The problem (their words) · the before numbers
- What we built (plain language, 3-5 bullets, screenshots)
- Results after N weeks (only measured numbers; label estimates as estimates)
- Quote from the client (their exact words, approved by them)
- Timeline + stack
```

The client approves the final case study before it's published. No numbers they haven't confirmed.

## Monthly for every active client

- Monthly report (what we did, results, next ideas) → keeps the retainer.
- One upsell idea per month that fits their goal (never spam).
- Ask for a referral every quarter.
