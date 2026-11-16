# Sending protocol (Phase 2)

Only run this after a founder has approved specific entries **in chat, this session**. If anything here doesn't match what you see on screen, stop and ask.

## 1. Browser setup

### Preferred: Chrome DevTools MCP attached to the founders' Chrome

Check whether the tools exist: `ToolSearch` query `chrome-devtools` (tools look like `mcp__chrome-devtools__navigate_page`). If they're missing, tell the founders to do this once:

1. In Chrome (version 144 or newer), open `chrome://inspect/#remote-debugging` and turn on remote debugging.
2. Add the server to Claude Code (user scope, works in every project):
   ```bash
   claude mcp add chrome-devtools --scope user -- npx -y chrome-devtools-mcp@latest --autoConnect
   ```
3. Restart Claude Code (or start a new session). On first use, Chrome shows a dialog asking to allow the connection: click **Allow**.

`--autoConnect` attaches to the founders' normal Chrome profile, where Instagram is already logged in. Never use `--isolated` or `--headless` for sending: those profiles have no login.

Tools used here (all page tools need `pageId` from `list_pages` / `new_page`):

| Tool | Use |
|---|---|
| `list_pages`, `new_page` (`url`, `background`), `select_page` | Open one working tab; leave the founders' other tabs alone |
| `navigate_page` (`pageId`, `url`) | Go to a profile or inbox |
| `take_snapshot` (`pageId`) | Read the page; gives element `uid`s. Prefer it over screenshots |
| `click` (`pageId`, `uid`) | Message button, composer, Send |
| `type_text` (`pageId`, `text`, optional `submitKey`) | Type into the focused composer. **Don't pass `submitKey`**: send separately after checking |
| `press_key` (`pageId`, `key`) | `Shift+Enter` for a line break, `Enter` to send, `Control+A` then `Backspace` to clear |
| `wait_for` (`pageId`, `text`: array, `timeout`) | Wait for the thread or the sent message to appear (case-sensitive) |
| `evaluate_script` (`pageId`, `function`) | Read-only checks (e.g. the composer's text) and scrolling. Never to click or send |
| `take_screenshot` | Only when the snapshot is unclear |

### Fallback: Chrome DevTools CLI

If the MCP server isn't available, use the `chrome-devtools` CLI (see the chrome-devtools-cli skill) attached to the same Chrome:
```bash
chrome-devtools start --autoConnect --headless=false
```
Same steps, same checks. If neither works, stop and give the founders the approved DMs to paste by hand, then record what they confirm they sent.

## 2. Pre-flight (once per session)

1. `new_page` → `https://www.instagram.com/` in a new tab. `take_snapshot`.
2. Confirm you're logged in and **which account** (the profile link in the left nav shows the username). If it isn't the account the founders named, stop and ask.
3. Read `D:\projects\eravue-portfolio\.outreach\instagram\account.md` for the sender account, today's cap and any recent warnings. If it's missing or the account details are unknown, ask the founders: how old is the account, has it ever been restricted? Then fill it in.
4. Count today's sends: entries with `**Status:** sent` in today's batch file(s) plus any other Instagram touches logged today in `.outreach/log.csv`. Remaining = cap − sent. If the approved list is longer than what's left, send the highest scores first and say what's held for tomorrow.
5. First Phase 2 run in a session: remind the founders once that automated actions are against Instagram's terms and carry some risk of restriction, which the low pace keeps small.

## 3. Daily caps and pacing

| Account state | Cold DMs per day (incl. follow-ups) |
|---|---|
| Week 1 of sending, or account under 3 months / few posts | 5 |
| Week 2, no warnings | 10 |
| Week 3+, no warnings (default) | 15 |
| Account 1+ year old, 3+ clean weeks, founders ask for more | up to 25 |

- **Gap between sends:** 2-4 minutes, varied (e.g. 140s, 210s, 170s). Use the gap to open and check the next profile. If a wait is needed, use whatever wait the environment allows (a backgrounded `sleep`, a Monitor, or slow verification work). Never send two DMs back to back.
- **Hourly limit:** no more than 8 sends in any 60 minutes.
- **After a warning:** stop for 48 hours, then restart at half the previous cap. Write it in account.md.
- Record the current cap and ramp week in account.md after each sending day.

## 4. Sending one DM

For each approved entry, in order:

1. **Re-read the entry.** Status must be `approved`. Copy the DM text exactly as approved (including any founder edits).
2. **Dedupe again:** `python $S check "@handle"`. If it now shows as contacted or `do_not_contact`, skip and say why.
3. **Open the profile:** `navigate_page` → `https://www.instagram.com/<handle>/`, then `take_snapshot`.
   - Confirm the username on the page **exactly** matches the entry. Instagram sometimes redirects or shows "Sorry, this page isn't available"; if so, mark `failed` (account gone) and move on.
4. **Open the thread:** `click` the **Message** button.
   - No Message button? Go to `https://www.instagram.com/direct/new/`, type the handle in the search box, pick the account whose username matches exactly, then click **Chat**. If it still isn't possible (DMs closed), mark `failed: DMs closed` and suggest email/WhatsApp via eravue-outreach.
5. **Check the thread is empty.** `take_snapshot`. If there's any earlier message from either side, **don't send**: mark `held: existing thread` and show the founders what's there.
6. **Type:** `click` the composer (textbox labelled like "Message..."), then `type_text` with the approved text and no `submitKey`.
   - Approved text with line breaks: type each line, with `press_key` `Shift+Enter` between lines (plain `Enter` sends).
7. **Verify before sending.** `take_snapshot` (or `evaluate_script` reading the composer's text). The composer must contain exactly the approved text, and the thread header must show the right account.
   - Mismatch (autocorrect, emoji swapped, text cut off, wrong recipient): clear with `press_key` `Control+A` then `Backspace` and retry once. Still wrong → stop, mark `failed: composer mismatch`, tell the founders.
8. **Send:** `press_key` `Enter` (or `click` the Send button).
9. **Confirm:** `wait_for` with the first ~25 characters of the message (`timeout` ~10000), then `take_snapshot`. The message bubble must be there with no "Couldn't send" / "Failed" / retry icon.
10. **Watch for warnings** in the snapshot after every send (list below). If any appear, stop the whole batch now.
11. **Log immediately:**
    ```bash
    python $S update L0012 --status contacted --touch --note "IG DM sent via DevTools; approved by Sanchit in chat"
    ```
    In the batch file: `**Status:** sent HH:MM`. For a follow-up, the same `--touch` (status stays `contacted`).
12. Wait 2-4 minutes, then the next entry.

## 5. Stop conditions (stop the whole batch, don't retry today)

Stop and tell the founders if you see any of:
- "Try again later", "We restrict certain activity to protect our community", "Action blocked", "You can't message this account right now", "We limit how often you can do certain things"
- A login page, "Confirm it's you", "Suspicious login attempt", a two-factor prompt, a CAPTCHA or "Help us confirm you're a person". Never fill these in; the founders handle them.
- The logged-in account changed, or a page you don't understand
- The same failure twice in a row
- Any popup asking to accept terms, change settings, or connect apps (don't click it)

Then: write the warning and time in account.md, mark remaining entries `approved (not sent: stopped)`, and report.

## 6. After the batch

- Report: sent / skipped / failed with reasons, and today's remaining cap.
- Remind the founders: most replies arrive within an hour and nearly all within a day. Replies show in the inbox thread. Fast answers matter most.
- **Checking replies** (on request or in follow-up mode): open `https://www.instagram.com/direct/inbox/`, `take_snapshot`, open threads with tracked handles, and read. Reading is fine; any reply you draft needs approval like a first DM. Update the tracker with `--status replied --note "..."`.
- Don't mark anything as read, delete, archive, mute or block threads unless a founder asks.

## 7. What you never do in Phase 2

- Send anything not approved in this chat, or change approved text without asking.
- Like, follow, comment, reply to stories, react, or accept/decline message requests unless a founder asks for that exact action.
- Use `evaluate_script` to click, type or send, or run loops that act on many accounts.
- Change account settings, log in or out, or deal with security prompts.
