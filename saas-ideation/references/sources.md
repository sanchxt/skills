# Source playbook

What to open, how to query it, and what each signal proves. Replace `<kw>` with a niche or job (e.g. "invoice", "shopify reviews", "youtube thumbnails"). Fetch with `scripts/read_page.sh "<url>"` unless noted. Log every query in `D:\projects\saas-ideas\sources-log.md`.

## Pain phrases (use them across every source)

`"is there a tool"`, `"is there an app"`, `"is there a way to"`, `"I would pay"`, `"I'd pay for"`, `"shut up and take my money"`, `"looking for a tool"`, `"alternative to"`, `"tired of"`, `"hate doing"`, `"spend hours"`, `"every week I have to"`, `"manually"`, `"spreadsheet"` + `"nightmare"`, `"too expensive"`, `"cancelled my subscription"`, `"wish it could"`, `"switched from"`, `"anyone built"`.

## Communities (pain + language buyers use)

| Source | URL pattern | Proves |
| --- | --- | --- |
| Reddit search | `https://www.reddit.com/search/?q=<phrase>+<kw>&sort=new&t=year` or `/r/<sub>/search/?q=...&restrict_sr=1&sort=new&t=year` | Recent pain, how often, reply count = resonance. The JSON endpoints are blocked; read the rendered page. Open the top threads and read the comments: "+1, same" replies are extra signals. |
| Good subs | r/SaaS, r/smallbusiness, r/Entrepreneur, r/shopify, r/ecommerce, r/realtors, r/freelance, r/agency, r/marketing, r/PPC, r/SEO, r/YouTubers, r/NewTubers, r/podcasting, r/Etsy, r/AmazonSeller, r/msp, r/sysadmin, r/accounting, r/Bookkeeping, r/Teachers, r/consulting, r/webdev, r/nocode, r/sales, r/RealEstateInvesting, r/photography, r/weddingplanning, r/restaurateur, r/dentistry, r/lawfirm, r/Notion, r/excel | Niche operators who pay for tools. |
| Hacker News | `https://hn.algolia.com/?q=<phrase>&dateRange=pastYear&type=comment` and "Ask HN" | Technical buyers, dev tooling pain. |
| X / Twitter | `https://x.com/search?q=%22is%20there%20a%20tool%22%20<kw>%20min_faves%3A5&f=live` | Fresh pain, founder chatter. Logged-in session needed. |
| Indie Hackers | `https://www.indiehackers.com/search?q=<kw>` | What small products earn and why. |
| Facebook groups, Discord, Slack | Only if already joined in the user's browser | Niche operators; skip if login or joining is needed. |

### Reddit: what actually works (learned 2026-11-09)

- **Best yield:** a subreddit's recent listing, `https://www.reddit.com/r/<sub>/top/?t=month` (or `/new/`), read with this JS expression (3rd arg of `read_page.sh`). It returns comment count, score, title, date and permalink for each post:
  `[...document.querySelectorAll('shreddit-post')].map(p=>p.getAttribute('comment-count')+'c '+p.getAttribute('score')+'v | '+p.getAttribute('post-title')+' | '+(p.getAttribute('created-timestamp')||'').slice(0,10)+' | '+p.getAttribute('permalink')).join('\n')`
- **Subreddit search** (`/r/<sub>/search/?q=...`) works but often surfaces old posts; check the dates.
- **Don't use:** site-wide `reddit.com/search` (it returns unrelated new posts), the `.json` endpoints (blocked), or `site:reddit.com` web searches (they returned nothing).
- **Reading a thread** (post + top 30 comments with scores):
  `(document.querySelector('shreddit-post')?.innerText||'').slice(0,2500)+'\n----\n'+[...document.querySelectorAll('shreddit-comment')].slice(0,30).map(c=>'['+c.getAttribute('score')+'] '+(c.querySelector('[slot="comment"]')?.innerText||'').replace(/\s+/g,' ').slice(0,350)).join('\n')`
- Set `PYTHONIOENCODING=utf-8` when post-processing output on Windows; emoji crash cp1252.

## Money-already-moving signals

| Source | URL pattern | Proves |
| --- | --- | --- |
| Upwork jobs | `https://www.upwork.com/nx/search/jobs/?q=<kw>&sort=recency` | Paid manual work. Recurring postings for the same task = productizable. Note budgets. |
| Fiverr | `https://www.fiverr.com/search/gigs?query=<kw>` | Gig counts + "X orders in queue" + review counts show buyer volume. |
| Acquire.com / Flippa | `https://acquire.com/` (browse), `https://flippa.com/search?filter[property_type]=saas` | Tiny SaaS / extensions with real MRR: copy the category, not the product. |
| TrustMRR / open startups | `https://trustmrr.com/` | Verified revenue of small products. |
| Product Hunt | `https://www.producthunt.com/search?q=<kw>` | Competitors, launch comments asking for missing features. |
| Gumroad discover | `https://gumroad.com/discover?query=<kw>` | One-time digital products with sales counts or ratings. |

## Hated / weak incumbents (wedge finding)

| Source | How | Proves |
| --- | --- | --- |
| G2 / Capterra | Product reviews page, filter to 1-3 stars; read "What do you dislike" | Specific gaps, price complaints, segment underserved. |
| Chrome Web Store | `https://chromewebstore.google.com/search/<kw>`; open listing -> reviews (sort recent), note users, rating, "Updated" date | Big installs + low rating or stale update = replaceable. |
| Shopify App Store | `https://apps.shopify.com/search?q=<kw>`; open app -> reviews filtered by 1-2 stars | Merchants pay monthly already; complaints are your spec. |
| WordPress.org plugins | `https://wordpress.org/plugins/search/<kw>/`; support forum + "Last updated" + active installs | Abandoned plugins with big install bases. |
| Figma / Notion / Webflow / Framer marketplaces | Search `<kw>`, check paid templates/plugins & reviews | Design/ops prosumers who pay for small things. |
| App Store / Play Store | Reviews of top apps in niche, 1-2 star | Consumer pain (only pursue if distribution is clear). |
| Trustpilot | `https://www.trustpilot.com/review/<domain>` | Billing/support anger at incumbents. |
| GitHub issues | `https://github.com/search?q=<kw>+is%3Aissue+sort%3Areactions-%2B1-desc&type=issues` | Most-wanted features maintainers won't build. |

## Demand / search intent

| Source | How | Proves |
| --- | --- | --- |
| Google autocomplete | Run `read_page.sh "https://www.google.com/search?q=<kw>+for"` or query suggestions via `https://suggestqueries.google.com/complete/search?client=firefox&q=<kw>%20for` | Long-tail "X for Y" demand. |
| Google SERP | `"<kw> alternative"`, `"<kw> vs"`, `"best <kw> for <segment>"` | Comparison intent = buyers shopping. Weak SERPs (forums, thin pages ranking) = SEO gap. |
| Google Trends | `https://trends.google.com/trends/explore?date=today%2012-m&q=<kw>` | Rising vs. dying. |
| Keyword volume | Free tiers (Ahrefs free keyword generator, Google Keyword Planner if the user has an account) | Rough volume; treat as directional. |
| Similarweb | `https://www.similarweb.com/website/<domain>/` | Competitor traffic size, top channels. |

## Platform-shift radar

Check recent (last 90 days) changes that create urgent migrations:
- Changelogs and blogs of big platforms in the niche (Shopify, Google, Meta, YouTube, OpenAI, Notion, Stripe, Chrome extension policies).
- `"<product> shutting down"`, `"<product> price increase"`, `"sunset"`, `"deprecated"`, `"new requirement"`, `"compliance deadline"` searches, sorted by recent.
- New AI model or API capabilities (video, voice, vision, agents) that make a previously hard workflow cheap. Pair them with a pain you already have evidence for; never start from the tech.

## Recording a signal

```
- [Seen 2026-11-09] r/shopify (merchant, ~$20k/mo store): "spend 3 hours every Monday matching refunds to..." - 41 upvotes, 23 comments - <link>
```
