# Subagent brief: delegated Instagram lead research (Sonnet or any model)

Use this when the CMO or eravue-instagram hands lead-finding to background subagents (e.g. `model: sonnet`). Give each subagent this whole file plus its own scope (industries, cities, quota, output path). The orchestrator (the main session) reviews everything before it reaches the tracker, the batch file or the founders' sheet.

Written 2026-11-17 after the first Sonnet run (5 agents, 54 leads, 48 kept). The mistakes it made are listed at the bottom; `scripts/check_dms.py` now catches every mechanical one.

## Role and limits
- You FIND, AUDIT and DRAFT. Never send, like, follow, comment, DM, save, or change anything on any site. Read-only at human pace.
- Never run `leads.py add` or `update`. Only `leads.py check "@handle"` (read-only dedupe). The orchestrator adds leads after review.
- Read first: `~/.claude/skills/eravue-outreach/references/eravue-profile.md` (services, proof, voice), `references/profile-audit.md`, `references/dm-playbook.md`, `references/finding-accounts.md`.

## Offers that can be fulfilled the same day
The founders have 3 recorded n8n demo videos. Prefer angles one of them answers, and name it in `ready`:
1. AI lead responder (instant reply to a new enquiry, qualifies, follows up)
2. Missed-call text-back + SMS/WhatsApp receptionist
3. WhatsApp AI receptionist (FAQs, qualify, book)
Other offers: a free 1-page homepage/landing mockup (no website), a free 20-sec reel re-edit (weak reels).

## Browser (shared Chrome via Chrome DevTools MCP)
- ToolSearch `select:mcp__chrome-devtools__new_page,mcp__chrome-devtools__navigate_page,mcp__chrome-devtools__evaluate_script,mcp__chrome-devtools__take_snapshot,mcp__chrome-devtools__close_page,mcp__chrome-devtools__wait_for,mcp__chrome-devtools__type_text`
- Other agents share the browser. Open ONE page with `new_page`, pass its `pageId` on every call, never `select_page`, never touch or close other pages. **Close your page before you finish, also when stopping early.**
- Read pages with `evaluate_script` returning trimmed text (og:description, header innerText, alt text of the first ~12 grid posts, highlight titles, post `<time datetime>`). Strip URLs before returning (`.replace(/https?:\/\/\S+/g,'[link]')`). No screenshots unless stuck. No Instagram internal API fetches.
- Pace: 20-40 s between Instagram profile loads, one profile at a time, no scripted loops or scrolling scripts.
- Stop at once and report on any warning, login wall, checkpoint or CAPTCHA. Do not retry.
- Run at most 3 agents at once on one Instagram account.

## Finding (what worked on 2026-11-17)
1. Meta Ad Library, short 2-3 word local queries ("car detailing delhi", "solar panel installation pune"):
   `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&is_targeted_country=false&media_type=all&q=<query>&search_type=keyword_unordered`
   Long or quoted queries return nothing. Skip chains, franchises, portals (99acres, Housing, Spinny), big brands.
2. Advertiser → handle: type the name into the Instagram search box on /explore (type_text, read result links), or open a Google search `<name> instagram` and read instagram.com anchors. Confirm the match (city or ad text fits) before auditing.
3. `explore/search/keyword` returns posts, not accounts. Hashtag pages `/explore/tags/<tag>/` work.
4. Productive niches on 2026-11-17: gyms/fitness/yoga/pilates studios, rooftop solar, car detailing/PPF, caterers, wedding planners, JEE/NEET coaching, kids' play centres, IVF clinics, dietitians. Low yield: packers and movers, driving schools, used cars, CA/tax, preschools, kids coding, jewellery, travel (wrong cities).

## Qualify (all must be true)
- Owner-led small or medium business; not a chain, franchise HQ, portal, agency (competitor) or personal account.
- **You read the date of the newest organic post** and it is within 60 days. Record it as `last_post` (YYYY-MM-DD). An active ad does not replace this.
- A gap one of our offers fixes, seen with your own eyes (quote it): "DM/call to book" only, no website or only Linktree/Maps/Drive/Facebook link, phone numbers in captions, unanswered price comments, several branches on one number.
- Not sensitive: no occult/spell-casting/black magic, gambling, loans, crypto, adult. Hospitals and multi-branch labs usually have in-house marketing: skip. Clinics are fine, but never mention treatments, conditions, bodies or patients.
- Score 4-5; 3 only with a reason in `verify`. Followers < ~150 only if an ad is running.

## DM rules (check_dms.py enforces the mechanical ones)
- 120-230 characters; **exactly one question mark in the whole DM**: the closing ask. Describe the scenario as a statement ("a parent who DMs at 11pm usually waits till morning."), not a question.
- First person "I/my". Never "we/our/us" except inside a quoted ad line.
- Open with a greeting: "hi <First name>," if a name is visible, else "hi <Brand> team," (brand capitalised, never "hi team brand"). Then "hope you're doing well!".
- Say "free" once: "I can make a free 1-page mockup, no strings attached." Never "a free mockup, free, no strings attached".
- Offer, don't claim: "I can make / I have a 1-min demo". Never "I made you / I built a flow for you" (nothing exists yet).
- No links, @mentions, phone numbers, prices or ₹ amounts (quote their ad line without the number). No generic compliments ("lovely", "amazing"); a specific observation instead. No guesses stated as facts ("enquiries must pour in").
- A and B use different hooks/offers (e.g. A = observation → gap → free mockup; B = scenario → demo video). Not the same sentence reworded.
- Hinglish is fine when their captions are Hinglish.

## Output
JSON array, plain UTF-8 (no BOM), written with Python `open(path, "w", encoding="utf-8")` and `json.dump(..., ensure_ascii=False)`, never with PowerShell `>`/`Out-File` (that corrupted "·" and "₹" into "Â·" and "â‚¹"). Rewrite the whole file after every lead.
```json
{"h":"handle","name":"","niche":"","service":"ai-chat-agents|lead-followup","loc":"","score":4,
 "via":"Meta Ad Library: 'query'","signal":"followers, posts; ad ('quoted line'); bio/link facts","angle":"",
 "A":["A · formula","text"],"B":["B · formula","text"],"ready":"demo video 1/2/3 or mockup/re-edit","reply":"",
 "verify":"what you could not confirm","last_post":"2026-11-14","ad_text":"quoted ad line or ''"}
```

## Before you hand back (required)
```bash
python ~/.claude/skills/eravue-instagram/scripts/check_dms.py <your-output.json>
```
Fix every ERROR and re-run until it prints PASS. Treat warnings as things to fix unless you have a reason. Your final message states the PASS line, the lead count, industries, queries that worked/failed, warnings seen, and open `verify` items. Quality over count: return fewer leads rather than weak ones.

## Mistakes from the 2026-11-17 Sonnet run (don't repeat)
| Mistake | How often | Now |
|---|---|---|
| Two questions in one DM | ~11 of 108 DMs | checker error |
| "free ... free, no strings attached" | ~30 DMs | checker error |
| PowerShell-written file: "Â·" / "â‚¹" mojibake | 2 agents | checker error + output rule |
| Phone number pasted into a DM | 1 | checker error |
| "we/us" outside a quote | 2 | checker error |
| "hi team wisda" / "hi team carcuro" | 3 | checker error |
| "I made a simple auto-reply flow" (claimed a sample that didn't exist) | 1 | checker error |
| Leads with no post date read ("last post not read") | ~20 | `last_post` required, ≤60 days |
| Weak or off-limits leads kept (spell-casting tarot, dormant page, hospital, big club, multi-branch lab) | 6 of 54 | qualify rules + sensitive-word check |
| Generic compliments / guesses ("lovely", "must pour in") | 3 | checker warning |
| Stopped agents left their tabs open | 3 tabs | close your page on any exit |
