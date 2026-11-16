---
name: eravue-metrics
description: Eravue's growth scoreboard and tracking. Pulls and records every growth number in one ledger - revenue and MRR, won clients and payments, the outreach funnel (touches, replies, calls, proposals, wins), website visitors and conversions from the self-hosted Umami, Google Search Console clicks, Instagram/LinkedIn/X/Google Business Profile followers and post performance - and prints the scoreboard. Use for "how are we doing", "scoreboard", "update the numbers", "log a new client / payment", "track this post", weekly growth reports, or whenever another Eravue skill (cmo, eravue-outreach, eravue-social, eravue-sales, seo) needs to record or read a metric.
---

# Eravue metrics

One ledger, one script. If a number isn't in `.growth/`, it didn't happen. Every other Eravue skill writes its results here, and `/cmo` decides from here.

```bash
G=~/.claude/skills/eravue-metrics/scripts/growth.py   # junction to the repo; data always in D:\projects\eravue-portfolio\.growth\
python $G pull all            # Umami (7d + 28d) + outreach funnel + money -> today's values
python $G report --brief      # headline scoreboard; drop --brief for everything, add --save to keep a copy
```

## What lives where

| File | What | Written by |
|---|---|---|
| `.growth/metrics.csv` | `date,metric,value,source,note` time series. One value per metric per day (re-running replaces it). | `pull`, `record` |
| `.growth/deals.csv` | Won clients: setup fee, monthly retainer, status | `deal add/update` (eravue-sales on a win) |
| `.growth/payments.csv` | Cash actually received | `pay` |
| `.growth/content.csv` | Every post, reel, article, with views/saves/follows/leads | `content add/update` (eravue-social, blog-writer) |
| `.growth/targets.json` | Goals with deadlines | `target` (cmo) |
| `.growth/config.json` | SSH host, Umami website id, bot countries | edit by hand |
| `.outreach/leads.csv`, `log.csv` | The lead tracker (owned by eravue-outreach's `leads.py`) | read by `pull leads` |

## Automatic pulls

- **`pull umami`**: SSHes to the VPS (`sanchxt@46.62.153.22`, key auth, read-only SQL against the `umami-db` container). No dashboard login needed. Records pageviews, visitors, `visitors_human` (excludes `bot_countries`, default SG and CN, which were ~80% of sessions in Nov 2026), India visitors, visits from search / AI assistants / social, every custom event (`site.event.<name>_<n>d`), and `site.conversions_<n>d` (form submits + WhatsApp, phone, email and book-call clicks).
- **`pull leads`**: furthest stage each lead has reached (contacted → replied → call_booked → proposal → won), plus last-7-day touches, replies, calls, wins and due follow-ups.
- **`pull money`**: MRR per currency, cash in last 30 days and all-time, active clients.

If SSH fails, say so and record nothing for Umami. Never estimate.

## Manual pulls (browser): do these in the weekly review

Use Chrome DevTools MCP (`mcp__chrome-devtools__*`, load with ToolSearch), following the shared rules in `~/.claude/skills/cmo/references/browser.md`. Open your own background tab with `new_page`, read with `evaluate_script`/`take_snapshot`, close it when done. Never touch the user's other tabs. Google tools use account slot **/u/2/**. Never type passwords. At a login wall, ask the user to sign in.

| Source | Where | Record as |
|---|---|---|
| Search Console | `https://search.google.com/u/2/search-console/performance/search-analytics?resource_id=https%3A%2F%2Feravue.com%2F&num_of_days=28` (the `seo` skill has page scripts in `scripts/gsc-snippets.md`) | `search.gsc_clicks_28d`, `search.gsc_impressions_28d`, `search.gsc_position_28d`, `search.indexed_pages` |
| Instagram | `instagram.com/<handle>/`: `meta[name=description]` gives followers/posts | `social.ig_eravuedotcom.followers`, `social.ig_lifewithcofounders.followers`, `.posts` |
| Instagram insights | Professional dashboard (needs that account logged in) | `social.ig_<handle>.reach_30d`, `.profile_visits_30d`, `.link_clicks_30d` |
| LinkedIn | personal profiles + company page `linkedin.com/company/eravue` | `social.li_sanchit.followers`, `social.li_sanchita.followers`, `social.li_company.followers`, `social.li_sanchit.impressions_7d` |
| X | `x.com/eravue` and founder handles | `social.x_<handle>.followers` |
| Google Business Profile | Google Maps listing / business.google.com (slot /u/2) | `social.gbp.reviews`, `social.gbp.rating`, `social.gbp.calls_28d`, `social.gbp.website_clicks_28d` |
| Reddit | founder account | `social.reddit_<user>.karma` |

```bash
python $G record social.ig_eravuedotcom.followers=373 social.ig_lifewithcofounders.followers=167 --source instagram
python $G record search.gsc_clicks_28d=6 search.gsc_impressions_28d=410 --source gsc
```

Metric names: lowercase, dotted, `<area>.<thing>[_window]`, areas `money`, `pipeline`, `site`, `search`, `social`, `content`, `ops`. Reuse existing names (`python $G report` lists them). Never invent a new spelling for an existing metric.

## Money (the numbers that matter most)

```bash
python $G deal add --client "Emson Designs" --lead L0004 --service website --market IN --channel instagram \
  --currency INR --setup 15000 --monthly 2999          # status defaults to active if monthly > 0, else one_off
python $G pay D0001 7500 --note "50% advance"          # record cash only when it has actually arrived
python $G deal update D0001 --status ended --note "paused after 3 months"
python $G deal list
```

Also mark the lead `won` in the outreach tracker (`leads.py update L0004 --status won`) so the funnel and the money agree.

## Content performance

```bash
python $G content add --platform instagram --account lifewithcofounders --format reel --pillar how-to \
  --title "AI receptionist in 10 min" --url https://www.instagram.com/reel/...
python $G content update C0003 --views 4200 --saves 61 --follows 18 --profile-visits 140 --leads 1
python $G content list --days 30
```

Update performance 48 hours and 7 days after posting. `--leads` counts DMs/enquiries that mention or came from that post.

## Targets

```bash
python $G target money.mrr_inr 25000 --by 2026-12-31 --label "MRR (INR)"
python $G target                       # show progress
```

`/cmo` owns targets. Don't change them without the founders agreeing.

## Reading the numbers honestly

- `site.visitors_*` is mostly bots. Use `visitors_human`, and treat even that as rough.
- Tiny numbers swing wildly. With fewer than ~20 events, report counts, not percentages or "+200%".
- Conversion tracking was missing from 2026-11-06 (redesign) until it is restored (see eravue-conversion). Zero conversions in that window means not measured, not no interest.
- A metric that wasn't pulled this week shows its old date in the report. Say it's stale rather than presenting it as current.
