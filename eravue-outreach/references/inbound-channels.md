# Inbound channels: people asking for help right now

Inbound leads are the fastest money: the person already wants to hire. Work them hottest first:
1. **Explicit hiring posts:** "[Hiring]", "looking for an editor", job posts with a budget.
2. **Recommendation requests:** "any agency for...", "who do you use for...".
3. **Pain posts:** "I can't keep up with...". Help first; the pitch is optional.

Freshness targets:
- Upwork and X: under 72 hours.
- Reddit, LinkedIn and forums: under 7 days, up to 30 if the thread is still active.
- Older items are research only.

Fill the `[need]` placeholders from [service-signals.md](service-signals.md). For every community you check, record its rules in `.outreach/communities.md` so they aren't re-checked every session (re-check after 30 days).

---

## Reddit
**Search** (use the signed-in browser from SKILL.md, i.e. Claude in Chrome or Chrome DevTools; WebSearch `site:reddit.com` as backup):
- Hiring boards, newest first: `https://www.reddit.com/r/forhire/search/?q=flair%3AHiring&restrict_sr=1&sort=new`. Do the same for r/hiring, r/jobbit, r/freelance_forhire, r/HireaWriter, r/DesignJobs, r/gameDevClassifieds (for editing and design).
- Site-wide, last week: `https://www.reddit.com/search/?q=%22looking+for%22+%22video+editor%22&sort=new&t=week`
- Inside a sub: `https://www.reddit.com/r/smallbusiness/search/?q=whatsapp+automation&restrict_sr=1&sort=new&t=month`
- WebSearch shapes:
  - `site:reddit.com "[Hiring]" "video editor"`
  - `site:reddit.com/r/smallbusiness "what do you use" "[need]"`
  - `site:reddit.com "recommend" "agency" "[need]"`

**Communities to try** (verify activity and rules first; adapt to the service):
- **Hiring:** r/forhire, r/hiring, r/jobbit, r/freelance_forhire, r/DesignJobs, r/HireaWriter
- **Owners:** r/smallbusiness, r/Entrepreneur, r/startups, r/SaaS, r/indianstartups, r/StartUpIndia, r/ecommerce, r/shopify
- **Niches:** r/realtors, r/RealEstate, r/Dentistry, r/HVAC, r/Plumbing, r/salons, r/fitness business subs, r/interiordesign (pain only)
- **Creators:** r/NewTubers, r/PartneredYoutube, r/youtubers, r/podcasting, r/TikTokhelp
- **Tools:** r/n8n, r/automation, r/AI_Agents, r/zapier, r/nocode, r/gohighlevel (as of Apr 2026 r/n8n bans self-promotion; hiring posts only, answer only if allowed)

**How to engage:**
- **On [Hiring] posts:** follow the post's own instructions (DM, comment "PM'd", email). Draft a short, specific pitch with portfolio links.
- **On advice threads:** use the rule ladder in [compliance.md](compliance.md). Default to genuinely helpful advice, with Eravue mentioned only if allowed and disclosed.
- **Avoid:** threads older than 30 days, locked or removed posts, and r/forhire posts whose budget looks like an obvious scam.

## X (Twitter)
**Search** at `https://x.com/search?q=<encoded>&src=typed_query&f=live` (Latest). Use `f=top` for high-engagement threads.

Queries (add `since:YYYY-MM-DD` for the last 3-7 days):
```
("looking for" OR "need" OR "hiring") ("video editor" OR "thumbnail designer" OR "reels editor") -filter:retweets lang:en
("looking for" OR "anyone know") ("n8n" OR "make.com" OR "zapier") (expert OR dev OR freelancer) -filter:retweets
("recommend" OR "looking for") ("web developer" OR "webflow" OR "framer" OR "landing page") -filter:retweets
("looking for" OR "need") ("AI agent" OR "chatbot" OR "voice agent") (build OR developer) -filter:retweets
("need a" OR "hiring a") ("social media manager" OR "ghostwriter" OR "content creator") -filter:retweets
"my developer" (ghosted OR disappeared OR quit) -filter:retweets
```
- Add noise filters only if needed: `-jobs -giveaway -crypto -airdrop -nft`.
- Check the replies under popular "who's a good editor/dev?" posts; they often contain more leads.
- Reply publicly only if the reply itself helps; otherwise note "DM if open" (only if their DMs are open and the post invites it).

## LinkedIn
Use the signed-in browser (Claude in Chrome or Chrome DevTools). Post search, newest first, past week:
`https://www.linkedin.com/search/results/content/?keywords=%22looking%20for%20a%20video%20editor%22&datePosted=%22past-week%22&sortBy=%22date_posted%22`

Keyword ideas:
- "looking for a video editor", "looking for an agency", "recommend a web developer"
- "need help with automation", "looking for a freelancer" + "[need]"
- "hiring social media manager", "any recommendations" + "CRM"

Also check:
- **LinkedIn Jobs:** "contract" or "freelance" roles for editing, social media, web dev or automation. Many companies would take an agency instead.
- **Founder posts** announcing a funding round or launch: an outbound-style lead.

Engage with a comment that adds value, or a connection note (300 characters max). Never use automation tools on LinkedIn: account-ban risk.

## Upwork (fast first revenue and reviews)
Use the founders' signed-in Chrome via Chrome DevTools MCP (see `~/.claude/skills/cmo/references/browser.md`). Never submit a proposal or spend Connects: draft only, and the founders submit. Profile, Project Catalog, bidding and tracking: [upwork.md](upwork.md).
- Newest jobs: `https://www.upwork.com/nx/search/jobs/?q=n8n&sort=recency`. Repeat with: make.com, zapier, whatsapp chatbot, AI agent, voice agent, video editor, youtube editor, reels, shopify, webflow, landing page, website redesign, social media manager, logo design, CRM, gohighlevel.
- **Prioritise:**
  - Posted under 24h, with under 10-15 proposals.
  - Payment verified, and the client has spent money before.
  - Clear scope.

  A new client with no hires is fine if the scope is clear.
- **Skip:** "test task" requests for large unpaid work, off-platform payment requests and vague "build me Uber".
- Note the Connects cost in `--notes`. Proposal format is in [messaging.md](messaging.md).

## Other marketplaces and boards
- **Contra, Freelancer.com, PeoplePerHour, Truelancer (India), Fiverr Buyer Briefs:** same rules as Upwork.
- **Hacker News:** the monthly "Ask HN: Freelancer? Seeking Freelancer?" thread. Search `site:news.ycombinator.com "Seeking Freelancer"`. Read the "SEEKING FREELANCER" posts.
- **Indie Hackers:** posts asking for devs or designers; founders looking for MVP help.
- **Wellfound:** contract and part-time roles at startups (web, app, design, content).
- **Craigslist (US) "computer gigs" and "creative gigs":** small jobs, so watch for scams.
- **Quora / Quora Spaces:** answer "how do I automate X / best agency for Y" questions helpfully, with disclosed affiliation. Slow, but it compounds.

## Facebook groups and Discord/Slack communities
- **Facebook:** Indian groups are big for small-business and startup hiring (for example local business owner groups and "startup India" style groups) and creator groups. Join with the founders' own accounts; the user does the joining. Search inside a group for "looking for", "need", "recommend".
- **Discord:** creator, YouTube-editing and startup servers often have #hiring or #jobs channels. Only read channels the founders have legitimately joined.
- **Threads (Meta):** search "looking for video editor", "need a website" and so on; same approach as X.

## What to record for each inbound lead
- `--channel`: reddit, x, linkedin, upwork, contra, hn, facebook, discord, threads, quora, other
- `--kind inbound`; `--url`: permalink to the exact post or comment
- `--signal`: their need in one line, with the budget if stated
- `--angle`: the specific helpful thing to open with
- `--score`: per [qualification.md](qualification.md)
