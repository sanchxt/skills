# GEO: visibility in AI search and assistants

## Purpose

Get the brand and its pages cited or recommended when people ask Google AI Overviews / AI Mode, ChatGPT, Perplexity, Gemini, Copilot or Claude about the problems the business solves. GEO (generative engine optimisation; also called AEO or LLMO) sits on top of SEO, not instead of it: AI systems mostly retrieve from search indexes, so a page that isn't indexed and trusted won't be cited.

## First, re-check the facts

This field changes fast and is full of vendor claims. Before advising, run a few current searches (e.g. "Google AI features site owners documentation", "AI Overviews AI Mode changes {current month year}", "ChatGPT search citations sources study {year}") and prefer:

1. Google Search Central docs and blog (developers.google.com/search). Google's position has been that AI Overviews / AI Mode use normal SEO eligibility (indexed, snippet-eligible) with no special markup or files required. Re-verify that this still holds.
2. Official engine docs (OpenAI's crawler/bot docs, Perplexity's, Microsoft's Bing Webmaster blog).
3. Peer-reviewed or well-documented studies (e.g. the 2024 GEO paper by Aggarwal et al.: adding citations, statistics and quotations improved visibility, while keyword stuffing did not).
4. Vendor studies, only as hypotheses, with the sample and date stated.

Write what you verified, and when, into `.seo/geo/notes.md`.

## Measure first: the prompt panel

You can't improve what you don't track. Build `.seo/geo/prompt-panel.md` with 15-30 prompts real buyers would type, in their own words:

- Category: "best {service} for {audience} in {city/country}", "who can build {thing} for my {business type}"
- Problem: "how do I {pain the service fixes}", "is it worth {doing X} for a small business"
- Comparison: "{option A} vs {option B} for {use case}", "alternatives to {competitor}"
- Cost: "how much does {service} cost in {country}"
- Brand: "what is {brand}", "is {brand} good for {use case}", "{brand} reviews"

Take them from GSC conversational queries, People Also Ask, Reddit/Quora threads and sales calls.

Run each prompt in a fresh, logged-out-style session where possible, via Chrome DevTools MCP: Google (look for an AI Overview, and try AI Mode), ChatGPT (search on), Perplexity, Gemini, Copilot. Record in `.seo/geo/results-YYYY-MM-DD.md`:

| Prompt | Engine | Brand mentioned? | Our URL cited? | Competitors cited | Sources cited (domains) | Notes |

Re-run monthly. Also check the generative-AI view in Search Console and Bing WMT's AI Performance report when available, and AI referrals in analytics (chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com).

AI answers vary between runs. Run important prompts 2-3 times and record a rate, not a single yes/no.

## What gets content cited

Apply to every page you write or refresh:

- **Answer first.** Open each page and each H2 section with a 1-3 sentence direct answer to the question it targets, then expand. Make definitions standalone: "X is ...".
- **Specific, sourced facts.** Numbers, prices, timelines, named tools, dates, each with a source or "from our projects". Vague claims don't get quoted.
- **Quotable structure.** Descriptive question-style H2/H3s, short paragraphs, bulleted steps, comparison tables, a brief FAQ that uses real phrasings.
- **Original material.** First-hand examples, mini case studies, screenshots, your own data or benchmarks. This is what AI can't get elsewhere, and what earns citations and links.
- **Freshness you can see.** Visible "Updated {date}", current-year facts, outdated stats replaced. Don't fake freshness by bumping dates.
- **One clear page per question.** Don't scatter the same answer across five thin posts; consolidate.
- **Named, credible authors** with a short bio and links to their profiles.

## What gets the brand recommended

AI assistants recommend brands they see described consistently across the web, not just on the brand's own site:

- **Entity consistency:** same name, one-line description, services, location and founders on the site, Google Business Profile, LinkedIn, Crunchbase, directories and social bios. `Organization` schema with `sameAs` links to those profiles.
- **Third-party mentions:** reviews (Google, Clutch, G2 or the niche equivalent), listicles and "best X" roundups, partner and client sites, podcasts, guest posts, press. Find which domains the engines cite for your prompts (from the prompt panel) and work to be mentioned there.
- **Community presence:** genuinely helpful answers on Reddit, Quora, LinkedIn and YouTube, where engines often source answers. Disclose affiliation; never spam.
- **Clear service and pricing pages:** engines lift "what it costs" and "who it's for" straight from them.

## Technical access for AI crawlers

- `robots.txt` should not block the crawlers you want citing you. Check the current user-agent names in each vendor's docs (e.g. OAI-SearchBot / ChatGPT-User / GPTBot, PerplexityBot, ClaudeBot / Claude-SearchBot, Bingbot, Googlebot; Google-Extended controls Gemini training, not Search). Decide training vs search access deliberately with the user.
- Key content must be in server-rendered HTML, not only injected by JavaScript. Many AI fetchers don't run JS.
- Submit to Bing (Bing WMT plus IndexNow). Bing's index feeds Copilot and other assistants.
- `llms.txt`: optional and cheap, but no major engine has confirmed using it. Never prioritise it over the items above.
- Schema (Organization, Service, Article, FAQ, Product/SoftwareApplication, BreadcrumbList) helps machines understand the page. It must match visible content.

## Output

- `.seo/geo/prompt-panel.md` (living) and `results-YYYY-MM-DD.md` (each run).
- A GEO action list: pages to restructure answer-first, facts to add, entity and profile fixes, mention targets (domains the engines cite), technical fixes.
