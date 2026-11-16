# Operating rhythm

```bash
G=~/.claude/skills/eravue-metrics/scripts/growth.py
L=~/.claude/skills/eravue-outreach/scripts/leads.py
```

## Daily (`/cmo`, or the scheduled morning run)

Aim: the founders open one file and know exactly what to approve and do today. Target ~30 minutes of their approval time for a full day of output.

1. **Numbers.** `python $G pull all`, then `python $G report --brief`. Note anything that moved.
2. **Hot stuff first** (money is closest here):
   - `python $L due`: replies come first, then overdue follow-ups.
   - Ask eravue-instagram to check its threads for replies (follow-up mode) if Instagram leads are open.
   - Any lead at `replied`, `call_booked` or `proposal` gets a next step from **eravue-sales** today (reply draft, call prep, proposal, nudge).
3. **Today's plan.** Read this week's plan (`.growth/plan/YYYY-Www.md`). Pick today's batches from it and size them with the quotas in [playbook.md](playbook.md). Default full-time day:
   - **eravue-outreach daily**: inbound hunt + outbound prospects for both markets, 50/50 IN/INTL, plus warm-network and partner touches.
   - **eravue-instagram batch**: within its current ramp cap.
   - **eravue-social**: today's founder post(s) drafted for LinkedIn/X, plus the comment list (10-15 posts by prospects to comment on).
   - **lifewithcofounders**: a reel script on the days the calendar says (3-4 per week).
   - **eravue-conversion / seo / blog-writer**: only the task this week's plan names. Usually one per day at most.
4. **Approval queue.** Collect every item that needs sending, posting, deploying or spending into one numbered list at the top of the daily file. Each item gets: number, type (DM/email/post/deploy/spend), where, who, and a link to the full draft. Nothing in the queue goes out until a founder approves it in chat.
5. **Founder tasks.** List the things only humans can do today (calls, recording reels, a voice note to a warm contact, meetings), each with a time estimate.
6. **Write** `.growth/daily/YYYY-MM-DD.md` (template below) and show a short summary in chat: the queue count, the top 3 founder tasks, and one line on the numbers.

On a **scheduled run**, stop after step 6. On an interactive run, wait for approvals, then run **send** through each owning skill's protocol, log every touch (`leads.py update <id> --touch`, `growth.py content add`), and append the results to the daily file.

### Daily file template

```markdown
# 2026-11-12 (Wed): CMO daily brief

## Approve these (reply "send 1-7", "send all", "edit 3: ...", "skip 5")
| # | Type | Channel | To / where | Lead | Draft |
|---|------|---------|------------|------|-------|
| 1 | DM | Instagram @eravuedotcom | @studioxyz | L0012 | .outreach/instagram/2026-11-12.md#1 |
| 2 | Post | LinkedIn (Sanchit) | feed | - | .growth/content-plan/2026-11.md#nov-12 |

## Founders today (est. time)
- [ ] 11:00 Discovery call with L0007 (30m). Prep: .growth/sales/L0007.md
- [ ] Record reel "AI receptionist in 10 min" (45m). Script: ...
- [ ] Send voice notes to 5 warm contacts (20m). List + drafts below

## Numbers (vs 7 days ago)
MRR ₹0 · touches 7d 34 (+34) · replies 7d 3 · calls 7d 1 · human visitors 7d 24 · site conversions 7d 1

## Replies and hot leads
...

## Work done by the CMO team today
- Outreach: 12 new leads (6 IN / 6 INTL), files...
- Social: ...

## Notes / decisions needed
- (anything the founders must decide; ask once, record in decisions.md)

## Results (filled after sending)
- Sent 1-6 at 12:40. #7 skipped (founder edit pending).
```

## Weekly (Monday, or the first run 7+ days after the last review)

1. **Manual pulls** (eravue-metrics §Manual pulls): GSC, Instagram x2, LinkedIn, X, GBP. Record them.
2. `python $G report --save`, then compare with last week's saved report.
3. **Funnel review by channel** (`python $L stats`): touches → replies → calls → proposals → wins per channel and per service. Where does it leak?
   - Low reply rate (under ~5% cold, under ~20% warm): the message or the targeting is wrong. Hand eravue-outreach a rewrite brief with the losing drafts.
   - Replies but no calls: the CTA or the follow-up is weak (eravue-sales).
   - Calls but no wins: the offer, price or proof is weak (eravue-sales, offers.md).
4. **Experiments**: judge every one past its end date in `.growth/experiments.md`: scale, iterate or kill. Start the next ones (max one per channel).
5. **Content review**: top and bottom posts by saves, follows and leads (`growth.py content list --days 7`). Feed the winners back to eravue-social and lifewithcofounders (their `log.md`).
6. **Write next week's plan** `.growth/plan/YYYY-Www.md`:

```markdown
# Week 2026-W47 (Nov 16-22)
## Last week: what happened
Numbers table (this week / last week). 3 bullets: worked, didn't, surprised us.
## This week's ONE focus
## Targets (activity, then outcomes)
touches 250 · replies 15 · calls 5 · proposals 2 · won 1 · posts LI 5 / X 7 / reels 3
## Channel plan (who / quota / day)
## Experiments running
## Founder asks (decisions needed this week)
```

7. Update `strategy.md` §Learnings with anything durable.
8. Tell the founders in 5 lines: the number that matters, the biggest leak, the plan, what you need from them.

## Monthly (every ~30 days)

1. Re-research with live sources: competitor agencies' offers and prices, what's working for agency client acquisition now, platform rule changes (Instagram/LinkedIn limits, Gmail/Outlook sender rules, Upwork changes), new AI tools to sell. Use WebSearch (several in one turn) and the browser. Save to `.growth/research/YYYY-MM.md` with sources.
2. Re-rank channels with the month's real funnel data ([channels.md](channels.md)). Move time and budget to the winners.
3. Refresh `strategy.md`: phase, focus, ICPs, allocation, targets (founders approve target changes).
4. Review offers and pricing with eravue-sales: win rate, objections heard, price pushback.
5. Check the budget spend against results ([budget.md](budget.md)).
