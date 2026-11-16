# Local presence: Google Business Profile, directories, reviews

## Google Business Profile (the founders set it up roughly; it needs a tune-up)

Use Chrome DevTools MCP in the founders' Chrome, Google account slot **/u/2/** (e.g. `https://business.google.com/u/2/` or search "Eravue" on Google Maps while signed in). Read first. Every edit is an account change: propose exact values in `.growth/conversion/gbp-YYYY-MM-DD.md`, get approval, then edit or hand the text to the founders.

Checklist (re-verify Google's current fields and guidelines when auditing; they change):
- [ ] Business name exactly "Eravue" (no keyword stuffing; that violates guidelines and risks suspension).
- [ ] Primary category that matches the core offer (check the available categories, e.g. "Software company", "Website designer", "Marketing agency", "Internet marketing service") plus relevant secondary categories.
- [ ] Service area (Delhi NCR cities) if there's no public office address. Don't show a home address unless the founders want to.
- [ ] Phone/WhatsApp, website with UTM (`?utm_source=gbp&utm_medium=listing`), hours, opening date.
- [ ] Services list with descriptions (mirror the site's services; "starting from" prices only if APPROVED).
- [ ] Description (750 chars): who you help, outcomes, proof, location served.
- [ ] Photos: logo, cover, founders, work screenshots, team at work. Add new ones monthly.
- [ ] Posts: weekly (repurpose LinkedIn/IG content: offers, case studies, updates).
- [ ] Q&A: seed with real common questions (if the feature is still available).
- [ ] Messaging/chat enabled if available, routed to a founder's phone.
- [ ] Review link: create the short "ask for review" link and save it in `.growth/strategy.md` §Situation.

Track in eravue-metrics: `social.gbp.reviews`, `social.gbp.rating`, `social.gbp.calls_28d`, `social.gbp.website_clicks_28d`, `social.gbp.views_28d`.

## Reviews (honest only)

- Ask every past client (Emson Designs, Bestor, DevLabs Alliance, Astro Shades, Caketastic, Yoop) for a Google review now. The founders send a personal WhatsApp with the direct link. Draft the messages for them.
- Ask every new client at go-live (eravue-sales after-the-win).
- **Never** write reviews for clients, offer payment or discounts for reviews, review-swap, or post from fake accounts. That breaks Google's policies and consumer-protection rules, and gets the listing suspended.
- Reply to every review within 48 hours (draft replies for approval).

## Free directory listings

Umami shows referral visits from goodfirms.co and designrush.com, so listings already exist or are being picked up. Audit and complete them (free tiers only during the sprint):

| Directory | Why | Notes |
|---|---|---|
| Clutch | Most-checked agency directory by international buyers | Reviews are verified by Clutch calls with clients: ask happy clients |
| GoodFirms | Already sending visits | Complete the profile, portfolio items, ask for reviews |
| DesignRush | Already sending visits | Complete the profile |
| LinkedIn company page | B2B trust | Owned by eravue-social |
| Bing Places | Free, imports from GBP | Quick win |
| Justdial / Sulekha (India) | Indian SMB owners search there | Expect sales calls *to* you; consider carefully, ask the founders |
| Upwork / Contra agency profile | Marketplace inbound | Owned by eravue-outreach |

Same name, address/area, phone and website everywhere (NAP consistency). Record each listing URL and status in `.growth/conversion/listings.md`.
