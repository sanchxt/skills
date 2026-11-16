# Conversion tracking

## Event taxonomy (Umami custom events)

| Event | Fires when | Props |
|---|---|---|
| `lead-form-submit` | Contact form submitted **successfully** (server returned success) | `services` (comma list), `page` |
| `whatsapp-click` | Any link to `wa.me` / `api.whatsapp.com` | `location` (hero, fab, footer, contact, blog-cta, service...), `page` |
| `phone-click` | Any `tel:` link | `location`, `page` |
| `email-click` | Any `mailto:` link | `location`, `page` |
| `book-call-click` | Any link to `/contact` (the primary "Book a free call" CTA) | `location`, `page` |
| `cta-click` | Other marked CTAs (`data-track="..."` overrides the name) | `location`, `label` |
| `outbound-click` | Links to Eravue's products or socials | `target` |

`growth.py pull umami` counts `lead-form-submit`, `whatsapp-click`, `phone-click`, `email-click` and `book-call-click` (plus the legacy pre-redesign names) as **conversions**.

Historical names (before the 2026-11-06 redesign): `contact-form-submit`, `whatsapp-chat-click`, `nav-contact-click`, `cta-book-free-call`, `social-click-*`. They still exist in the data. Don't reuse them for new events.

## Implementation pattern (single responsibility, no per-button wiring)

One delegated click listener in `src/components/seo/Analytics.astro` (loaded on every page in production) classifies clicks by `href`:
- `wa.me` / `api.whatsapp.com` → `whatsapp-click`
- `tel:` → `phone-click`
- `mailto:` → `email-click`
- same-origin `/contact` → `book-call-click`
- an element with `data-track="name"` → that name (explicit override)
- `location` comes from the closest ancestor's `data-track-location`, else the nearest landmark (`header`, `footer`, `main section[id]`), else `"page"`.

The contact form fires `lead-form-submit` itself after a successful response (`src/components/contact/ContactForm.astro`), because only it knows the result.

Umami loads lazily (on idle). Queue events fired before `window.umami` exists and flush them once it loads, or clicks from fast visitors are lost.

## UTM links

Every link to eravue.com that the CMO team puts in bios, posts, DMs, emails and proposals carries UTMs, so Umami can attribute visits:

```
https://eravue.com/contact?utm_source=instagram&utm_medium=bio&utm_campaign=profile
https://eravue.com/?utm_source=linkedin&utm_medium=post&utm_campaign=2026-11-ai-receptionist
https://eravue.com/portfolio?utm_source=outreach&utm_medium=dm&utm_campaign=ig-interior-ncr
```

Sources: instagram, linkedin, x, reddit, upwork, email, whatsapp, gbp, directory name. Mediums: bio, post, dm, email, proposal, listing. Campaign: a short slug. Umami's UTM report (and `website_event.utm_*` columns) shows them.

## Verify

1. Locally: `pnpm build && pnpm preview` won't load Umami (prod-only and needs env), so verify the listener by stubbing in the browser console: `window.umami = { track: (n, p) => console.log('track', n, p) }`, then click each link type and confirm the logs.
2. On production after deploy: click each CTA type once in a normal browser, then check the DB:
   ```bash
   ssh sanchxt@46.62.153.22 "docker exec umami-db psql -U umami -d umami -At -c \"select event_name, created_at from website_event where event_type=2 and created_at > now() - interval '15 minutes' and event_name not in ('scroll-depth','web-vital') order by created_at desc\""
   ```
3. Note the test clicks in `.growth/strategy.md` §Learnings (date + "N test events") so they aren't counted as leads.

## Umami dashboard access

The founders' Umami login is theirs: never type it. The SSH/DB route needs no login. If they want dashboard access back and forgot the password, guide them to reset it on the VPS (Umami docs: update the `user` table password with a bcrypt hash, or use the CLI in the container) and let them run the command.
