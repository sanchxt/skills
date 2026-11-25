# Eravue HQ for agents (shared skill reference)


Eravue HQ (https://app.eravue.com) is the **only source of truth** for both founders: today's timetable and floors, every lead and every message sent, the approval Outbox, Upwork jobs, clients (Kilo, TrackBudget) and their commitments, content in production, the proof library, tasks, notes and decisions, and the metrics ledger. Agents reach it through the `eravue-hq` MCP server (tools below). The founders see every change in the app, tagged "agent".

If the `eravue-hq` tools aren't available in the session, stop and tell the founder to connect it (Settings → Agents in HQ gives the one-line `claude mcp add` command). Never fall back to the old CSVs after cutover: they are frozen.

## Rules

1. **Check before you add.** `lead_check` (or `lead_create`, which refuses duplicates) before adding anyone. Duplicates are matched by Instagram handle, website, phone, email and business name. Use `force: true` only when the founder says it's a different business.
2. **Nothing is sent without a founder's approval.** Agents write messages with `draft_create` (one or many). They land in the Outbox as PENDING. Agents can't approve or skip. After a founder approves, an agent may send it (e.g. through the logged-in browser) and then must call `draft_mark_sent` with the exact text sent. That logs the touch, advances the stage and schedules the follow-up.
3. **Log what actually happened, exactly.** Every message sent outside the Outbox → `touch_log` with the exact text. Every reply → `touch_log` with `type: "REPLY", direction: "IN"` and what they said. Replies jump to the top of both founders' Today and notify them.
4. **Follow-ups are automatic.** Gaps of 3, 4 and 7 days after each message, then stop. Use `followups_due` to see who's due (replies first). Override with `nextFollowUpAt` only when the person asked for a specific time.
5. **Floors count themselves.** New messages, follow-ups, video pitches, walk-ins, Upwork proposals, replies and calls are counted from touches. Don't `day_increment` those (it would double count). Use `day_increment` only for things HQ can't see: reels shot or edited, FounderSpawn shorts, and client commitments (`commitment_log` for Kilo X/Reddit comments and TrackBudget posts, with the link).
6. **Numbers go in the ledger.** Every metric you pull (followers, GSC clicks, Umami visits, ad spend) → `metric_record` with a dotted key (`social.ig_eravuedotcom.followers`, `search.gsc_clicks_28d`, `web.umami_visitors_7d`, `ops.spend_inr`) and the source.
7. **Decisions and briefs are notes.** Founder decisions → `note_add` with `kind: "DECISION"`. The daily brief → `note_add` titled `Daily brief YYYY-MM-DD`, tag `daily-brief` (the approval items themselves go in the Outbox, not in the note).
8. **People are slugs:** `sanchit` or `sanchita`. Dates are `YYYY-MM-DD` (IST); the work day rolls over at 4 AM IST.

## Tool map (old way → HQ)

| Before | Now |
|---|---|
| `leads.py check` | `lead_check` |
| `leads.py add` / bulk add | `lead_create` / `lead_create_many` |
| `leads.py update`, status changes | `lead_update` (stage: NEW, SHORTLISTED, CONTACTED, REPLIED, CALL_BOOKED, PROPOSAL, WON, LOST, NO_REPLY, DO_NOT_CONTACT) |
| `leads.py touch`, log.csv | `touch_log` (or `draft_mark_sent` for Outbox drafts) |
| `leads.py due` | `followups_due` |
| `leads.py list/show` | `lead_search`, `lead_get` (full history) |
| approval queue in `.growth/daily/*.md` | `draft_create` (Outbox), then `drafts_list status=APPROVED` to see what may be sent |
| Daily Board (ArtifactData `days`) | `today`, `day_get`, `week_summary`, `day_update` (ticks, note, day type) |
| `growth.py add-metric`, metrics.csv | `metric_record`; `scoreboard` to read |
| deals.csv / payments.csv | `client_get` (retainer, invoices, payments); `invoice_add`, `invoice_update`, `payment_add` to record them (bookkeeping only) |
| content.csv, content-plan | `content_list`, `content_upsert` (stage IDEA → SCRIPT → PRODUCTION → EDIT → READY → SCHEDULED → POSTED) |
| `.growth/upwork/` notes | `upwork_list`, `upwork_upsert` (status SUBMITTED logs the proposal touch) |
| "which demo do we send?" | `asset_search` (by niche/service), `asset_used` after sending |
| decisions.md | `notes_list kind=DECISION`, `note_add` |
| anything else | `search` (everything), `capture` (paste a link, get a lead), `activity_recent`, `notifications_list`, `delete` (only when a founder asks) |

## A daily run, the HQ way

1. `today` → who hit which floors yesterday (debt is already added), what's due, what's in the Outbox.
2. `followups_due` → draft replies first, then follow-ups, with `draft_create`.
3. Find new prospects; `lead_check` each; `lead_create_many` the good ones with `signal` and `angle`; `draft_create` one message per lead (`reason` = the signal, `assignee` = whose account sends it, `batch` = `YYYY-MM-DD <channel> batch`).
4. `metric_record` anything pulled; `note_add` the brief.
5. Tell the founders in one line: "N drafts in the Outbox, M follow-ups due, X replies waiting."
