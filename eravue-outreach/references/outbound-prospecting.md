# Outbound prospecting: businesses that don't know they need Eravue yet

Outbound works when every message shows you looked at *their* business. The formula: **find a good-fit business → spot one visible, fixable gap → open with that gap and a small free thing.**

Work the sources in this order of speed to money.

---

## 1. Warm network and past clients (do this first; highest close rate)
- **Past clients:** upsell, check in and ask for referrals. Always as **warm** leads.

| Client | Upsell idea |
|---|---|
| Emson Designs | Enquiry follow-up automation, Instagram content |
| Bestor | Ad creatives, social media, WhatsApp support |
| DevLabs Alliance | Lead follow-up for course enquiries, chat agent, CRM |
| Astro Shades (astrologer) | WhatsApp booking, reminders, payment links, consultation follow-ups |
| Caketastic | Order-taking chat agent on Instagram/WhatsApp |

- **Personal network:** ask the founders for a list (family businesses, friends' employers, college network, LinkedIn connections who own businesses). Draft a personal message asking for **introductions**, not for a sale: "Who do you know who's drowning in WhatsApp enquiries?"
- Track as `--kind warm --channel whatsapp|linkedin|email|in-person`.

## 2. Google Maps local businesses (India and international)
- **Build lists:** search "<niche> in <area>" on Google Maps in the browser, or have the founders export from Outscraper (about $3 per 1,000 records, first 500 free) and `import` the CSV.
- **Prioritise:**
  - Rating 4.0+ with 30+ reviews: real business, real demand.
  - Owner-led.
  - At least one visible gap.

  Skip chains and franchises.
- **Gap audit** (2-4 minutes per business; capture evidence, not guesses):
  - **Website:** none, Linktree only, slow on mobile (check `https://pagespeed.web.dev/analysis?url=<site>`), not mobile-friendly, no WhatsApp or call button, broken form, no SSL.
  - **Reviews:** complaints about "never pick up", "slow response", "no reply on WhatsApp". These mean voice agents or chat agents.
  - **Hours:** short hours plus phone-first, so after-hours enquiries are lost.
  - **Instagram:** last post date, "DM for price", unanswered comments.
  - **Booking:** no online booking for appointment businesses.
- **Mystery-shop speed test** (optional, strongest for chat agents and lead follow-up):
  - Send one genuine-sounding, simple enquiry from a founder's own WhatsApp.
  - Log the send time and reply time in `--notes`.
  - Always disclose in the follow-up that it was a test from Eravue (see [compliance.md](compliance.md)).
  - At most 10-15 a day, one-to-one, never bulk.
- **In-person visits (Delhi NCR):** the founders are local and full-time, which is a real edge. Pick a cluster (a market or street with 8-10 targets: clinics, salons, studios, showrooms). For each, prepare a printed 1-page gap audit (what we noticed + one fix + a QR code to a WhatsApp chat with UTM `utm_source=visit`). Visit off-peak, ask for the owner, take 2 minutes, leave the page. Track as `--kind outbound --channel in-person` and follow up on WhatsApp the same day with what was discussed.

## 3. Instagram businesses and creators
- **Discovery:**
  - Location and hashtag pages (#gurgaoninteriors, #delhibakery, #dentistdelhi).
  - `site:instagram.com "<niche>" "<city>"`.
  - The "suggested accounts" of a good prospect.
  - Competitors' tagged clients.
- **Audit:**
  - Is the offer clear from the bio in 5 seconds?
  - Posting consistency and Reels usage.
  - Quality of creatives.
  - Unanswered comments.
  - The bio link: where does it go, and does it convert?
- **Fit:**
  - social-media, video-editing and ai-content for weak content.
  - ai-chat-agents for "DM for price" and unanswered comments.
  - website for Linktree-only accounts.
- **Contact surface:** DM (from a founder or the @eravuedotcom account), the public email button or the website form.

## 4. Spending and hiring signals (warmest outbound)
- **Meta Ad Library** (`https://www.facebook.com/ads/library/`): find brands in a niche or country running ads. Few or stale creatives → ai-content. Ads pointing to WhatsApp → lead-followup.
- **Job posts** on Naukri, LinkedIn Jobs, Indeed and Internshala for roles Eravue replaces or supports:

| Job post for | Pitch |
|---|---|
| Video editor, social media executive, graphic designer | Content services |
| Telecaller, receptionist, customer support | Voice and chat agents |
| Data entry, MIS, back-office | ai-automation |
| Web developer (at a non-tech company) | website or apps |

  Pitch: "Before you hire full-time, we can cover this as a monthly service, starting this week."
- **Funding or launch news:** Inc42, Entrackr, YourStory funding roundups; X and LinkedIn launch posts. Newly funded startups need websites, apps and content fast.

## 5. LinkedIn decision-makers (B2B, India and international)
- Search people by title (Founder, Owner, Director, Marketing Head) plus industry plus location. The Sales Navigator free trial helps if the founders start one.
- Look at their recent posts for a hook. The company website gives the gap.
- Connection note under 300 characters, no pitch; the pitch goes in the second message after they accept.

## 6. International cold email (US/UK/AU)
- **Niches:** home services, dental, med-spa, real-estate agents, law firms (lead intake), coaches and creators.
- **Lists:**
  - Google Maps (Outscraper) for local businesses.
  - Apollo's free tier for people at companies.
  - Always verify emails before sending (Apollo or similar verification).
- **Sending setup (the founders do this):**
  - A separate domain (not eravue.com) with 2-3 inboxes.
  - Warm-up for 2-3 weeks.
  - A tool like Instantly or Smartlead.
  - 30-50 emails per inbox per day at most.
- **You prepare:** the lead list (imported to the tracker), one specific first line per lead, and a 3-step sequence. See [messaging.md](messaging.md) and the email rules in [compliance.md](compliance.md).

## 7. Partners (one partner = many clients)
- **White-label:** marketing agencies (India, US, UK) that sell ads or SMM but can't build automation, websites or apps. Find them on Clutch, GoodFirms, Google ("digital marketing agency <city>") and LinkedIn. Pitch: "Your clients ask for WhatsApp bots / websites / AI. We build them under your name; you keep the client."
- **Referral partners:**
  - CAs and accountants: their SME clients need automation.
  - Web designers and freelancers: overflow and AI work.
  - Meta-ads freelancers: their leads need follow-up.
  - CRM and software resellers.
  - Pitch: 10-15% referral commission (the founders confirm the rate).
- Track as `--kind partner`. One good partner is worth more than 50 cold leads, so follow up carefully.

## 8. Directories (set once, check monthly)
- A free Clutch profile, a free GoodFirms listing, and a Google Business Profile for Eravue.
- Remind the founders to set these up if they haven't. Don't do it for them (it involves accepting terms and creating accounts).

---

## Prospect record checklist
For each outbound lead, capture:
- name or business
- location
- url: website or profile
- the public contact surface (email, phone, @handle)
- **one** gap with evidence (`--signal`)
- the specific opener (`--angle`)
- service
- market
- score

Business emails and phones listed publicly for business enquiries are fine to record. Don't dig for personal numbers or private emails.
