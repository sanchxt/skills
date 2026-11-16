---
name: eravue-blog
description: Write, edit, schedule, publish, unpublish, trash, restore and delete posts on the live eravue.com blog, including cover/OG images, SVG diagrams, AI-generated images and all SEO meta tags. Use whenever the user wants a blog post written or changed on eravue.com ("write a blog about X", "publish the CRM post", "schedule this for Monday 9am", "update the pricing in the website-cost article", "delete that post", "make a cover image", "what's scheduled?"). Works through the `pnpm blog` CLI and the site's admin API, so no VPS, SSH or database access is needed. For keyword research and content strategy, use the `seo` skill first and come back here to write and ship. For a fully automatic research-write-publish run ("write a blog", "write 3 blogs"), the `blog-writer` skill drives this one.
---

# Eravue blog

You manage the blog on **https://eravue.com/blog** (Astro + Postgres, content stored as Tiptap JSON, images on the R2 CDN). Everything goes through one CLI that talks to the live admin API with a Bearer token:

```bash
pnpm blog --help
```

Every command prints JSON on stdout (warnings go to stderr). Read the JSON; don't guess what happened.

## Authority

The user has given you full autonomy over the blog: you may create, edit, publish, schedule, unpublish and trash posts when asked, without asking for confirmation again. Two limits still apply:

- **Deleting**: use `trash` (recoverable). Only use `delete --permanent` when the user explicitly asks for a permanent delete.
- **Scope**: do what was asked. Don't republish, retitle or restructure other posts on your own initiative; suggest it instead.

## Before the first command

1. `.env.blog` must exist at the repo root with `ERAVUE_BLOG_API_TOKEN` (copy `.env.blog.example`). If it's missing, or commands return `API error 401`, stop and tell the user. Don't try other ways in (SSH, DB, admin login).
2. Use `pnpm` (or `corepack pnpm` if the global pnpm complains about the workspace file).

## Posts live as markdown files

The source of truth for a post is a markdown file with YAML frontmatter in `.seo/content/articles/`. Name new files `YYYY-MM-DD-<slug>.md` (date = today). After the first `push`, the CLI writes `id:` into the frontmatter; that links the file to the live post, so later pushes update it instead of creating a duplicate.

Full field list, limits and every command: [references/cli.md](references/cli.md).

## Workflows

### Write and publish a new post
1. Check what exists, to avoid duplicates and to find internal links: `pnpm blog list --status published --limit 100` and `pnpm blog categories`.
2. Write the file following [references/writing.md](references/writing.md) (structure, SEO fields, internal links, voice).
3. Images, following [references/images.md](references/images.md):
   - Always: `pnpm blog cover --file <post.md>`, which renders the branded cover + OG image and links them in the frontmatter.
   - When a concept is clearer as a picture: hand-written SVG diagram(s) in `.seo/content/images/<slug>/`, referenced with relative paths in the markdown.
   - Extra (AI) images only when the user asks: give them a ChatGPT prompt and they drop the file into `image-inbox/` at the repo root; you then move it into the post's image folder. Don't drive ChatGPT yourself. Details in references/images.md.
   - Look at every image you produced (Read the file) before pushing.
4. Validate: `pnpm blog push <file> --dry-run`. Fix every error; fix warnings unless there's a reason not to.
5. Ship: `pnpm blog push <file> --publish` (or `--draft`, or `--schedule 2026-11-20T09:00:00+05:30`). Local images are uploaded and their paths rewritten to CDN URLs automatically.
6. Report the live URL from the output. If published, open it (`get_page_text` on the URL, or curl) to confirm it renders.

### Edit an existing post
1. Find it: `pnpm blog list` / `pnpm blog get <slug>`.
2. Get the current text: if a linked file exists in `.seo/content/articles/` (matching `id` or `slug`), `pnpm blog pull <slug> --force` refreshes it from live, which is safer than trusting a possibly stale file. Otherwise `pnpm blog pull <slug>` creates one.
3. Edit the file, then `pnpm blog push <file>`. The post keeps its status unless you change `status`.
4. Older article files in `.seo/content/articles/` have no `id`. Pushing one whose slug is already live fails on purpose; re-run with `--adopt` only if that file really is the source for that post.

### Schedule / publish / unpublish / delete
- `pnpm blog schedule <slug> <ISO date with offset>`: always include the offset; the user is in India, so use `+05:30` unless told otherwise. The server publishes within a minute of the time.
- `pnpm blog publish <slug>`, `pnpm blog unpublish <slug>` (back to draft).
- `pnpm blog trash <slug>` → recoverable; `pnpm blog restore <slug>` → back as draft.
- `pnpm blog delete <slug> --permanent` → irreversible; only on explicit request.
- After changing status with these commands, a linked local file still has the old `status`. The next `push` refuses to take a live post down unless the file says `published` (or you pass `--allow-unpublish`), so set `status:` in the file to match.

### Status overview
`pnpm blog list` (counts by status + posts), `pnpm blog list --status scheduled`.

## Gotchas
- `metaTitle` is used as the full `<title>` with no suffix added: max 70 chars, include "| Eravue" yourself if it fits.
- Category must already exist (`pnpm blog categories`). The five with tailored end-of-post CTAs are `website-development`, `app-development`, `crm-erp`, `digital-marketing`, `social-media`; prefer them. Create a new one only when none fits: `createCategory: true` in frontmatter, or `pnpm blog category:create --name "..."`.
- Unknown tags are created automatically; reuse existing tag names (`pnpm blog tags`) instead of near-duplicates.
- Headings: the page renders the title as H1; body `#` headings become H2, and H5/H6 become H4. Use `##`–`####`.
- Only what the editor supports survives: standard markdown, plus `<u>`, `<mark>` and the YouTube embed form in references/cli.md. Other HTML (layout divs, inline `<svg>`, styles, scripts) is dropped, so SVGs must be separate image files.
- Text colour and alignment set in the admin editor can't be represented in markdown; `pull` warns when a post has them, and a push of that file would remove them. Tell the user before pushing such a post.
