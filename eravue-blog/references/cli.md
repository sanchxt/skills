# `pnpm blog` reference

Config comes from `.env.blog` (gitignored) at the repo root:

| Variable | Purpose |
| --- | --- |
| `ERAVUE_BLOG_API_URL` | `https://eravue.com` (or `http://localhost:4321` against `pnpm dev`) |
| `ERAVUE_BLOG_API_TOKEN` | Must equal `BLOG_API_TOKEN` on the server (GitHub secret) |
| `OPENAI_API_KEY` | Only for `pnpm blog image` |
| `OPENAI_IMAGE_MODEL` | Defaults to `gpt-image-1` |

`<ref>` below is a post's slug or numeric id.

## Post commands

| Command | What it does |
| --- | --- |
| `list [--status all\|draft\|scheduled\|published\|trashed] [--page N] [--limit N]` | Posts + counts per status. `all` excludes trash. Limit max 100. |
| `get <ref>` | Metadata only (no body), including live URL, category, tags, meta fields. |
| `pull <ref> [--out file] [--force]` | Writes the live post to markdown. Default path: the linked file in `.seo/content/articles/` (matched by `id`, then `slug`), else `.seo/content/articles/<slug>.md`. Won't overwrite without `--force`. |
| `push <file> [--publish \| --draft \| --schedule <iso>] [--adopt] [--allow-unpublish] [--dry-run]` | Validates, uploads local images, then creates or updates. Writes `id`, `slug`, `status`, `publishedAt` back into the file. |
| `publish <ref> [--at <iso>]` | Publish now. `--at` sets the displayed publish date (backdating). |
| `schedule <ref> <iso>` | Must be in the future. Include an offset, e.g. `2026-11-20T09:00:00+05:30`. |
| `unpublish <ref>` | Back to draft (page 404s). |
| `trash <ref>` / `restore <ref>` | Recoverable delete / bring back as draft. |
| `delete <ref> --permanent` | Irreversible. |

`push` decides create vs update like this:
1. File has `id` → update that post (error if it no longer exists).
2. No `id`, slug not taken → create.
3. No `id`, slug taken → error, unless `--adopt` (then it overwrites that post and records the `id`).

Safety rails in `push`: it refuses to turn a **published** post into draft/scheduled unless you pass `--allow-unpublish`. Validation errors (lengths, missing files, past schedule) stop it before anything is sent.

## Media commands

| Command | What it does |
| --- | --- |
| `cover --file <post.md> [--tone night\|signal\|paper] [--eyebrow "..."]` | Renders `<slug>-cover.webp` (1600×900) and `<slug>-og.webp` (1200×630) into `.seo/content/images/<slug>/` and sets `coverImage`/`ogImage` in the file. Eyebrow defaults to the category; tone defaults to a stable pick per category. |
| `cover --title "..." [--eyebrow ...] [--tone ...] [--out-dir dir]` | Same, without a post file. |
| `image --prompt "..." --out <file.png> [--size 1536x1024\|1024x1024\|1024x1536] [--quality low\|medium\|high]` | OpenAI Images API → PNG. Converted to WebP on upload. |
| `upload <file> [--max-width 800\|1200\|1600\|2000]` | Uploads one image and prints its CDN URL. Raster → WebP resized to fit max-width (default 1200). SVG stored as-is after a safety check. |

You rarely need `upload` directly: `push` uploads any local path in `coverImage`, `ogImage` or a markdown image (`![alt](./images/x.svg)`), caches duplicates, and rewrites the file with CDN URLs. Local paths resolve relative to the post file.

## Taxonomy

`categories`, `tags`, `category:create --name "..." [--slug ...] [--description "..."]`.

## Frontmatter fields

| Field | Notes |
| --- | --- |
| `title` | Required (or a leading `# Title` in the body). Max 255. A leading body H1 equal to the title is removed automatically. |
| `slug` | Optional; derived from the title. Lowercase-hyphenated, short, keyword-led. Changing the slug of a live post changes its URL (old URL 404s), so avoid that. |
| `excerpt` | 1–2 sentences, ≤ ~200 chars. Shown on cards and as the lede under the title. |
| `category` | Category slug or name. Must exist unless `createCategory: true`. Empty string clears it. |
| `tags` | List of names. Unknown ones are created. |
| `metaTitle` | ≤ 70 chars (hard limit). Used verbatim as `<title>`. |
| `metaDescription` | ≤ 170 chars (hard limit), aim for 140–160. |
| `metaKeywords` | Comma-separated string. |
| `coverImage` | CDN URL or local path (uploaded at 1600px). |
| `ogImage` | CDN URL or local path (uploaded at 1200px). Falls back to coverImage. |
| `author` | Defaults to "Eravue". |
| `canonicalUrl` | Only for content republished from elsewhere. |
| `status` | `draft` \| `published` \| `scheduled`. Omit to leave unchanged on update (new posts default to draft). |
| `scheduledAt` | Required when `status: scheduled`. ISO with offset. |
| `publishedAt` | Display/publish date. Set automatically on first publish. |
| `id` | Written by the CLI. Don't invent or edit it. |

Empty strings clear a field on update (e.g. `coverImage: ""` removes the cover).

## Markdown that renders

Headings `##`–`####`, paragraphs, **bold**, *italic*, ~~strike~~, `code`, links, bullet/numbered (nested) lists, blockquotes, fenced code blocks with a language, `---`, images `![alt](src "optional title")`, GFM tables, hard line breaks (`\` at line end), `<u>underline</u>`, `<mark>highlight</mark>`, and YouTube embeds:

```html
<div data-youtube-video><iframe src="https://www.youtube.com/watch?v=VIDEO_ID"></iframe></div>
```

Links to other Eravue pages should be root-relative (`/blog/<slug>`, `/service/detailed/<slug>`, `/contact`); they open in the same tab. External links open in a new tab automatically.

## API (for reference)

All routes accept `Authorization: Bearer <token>` (or the admin cookie).
`GET /api/admin/posts?status=&page=&limit=` · `GET /api/admin/posts?slug=` · `GET /api/admin/posts/:id` · `POST /api/admin/posts` · `PUT /api/admin/posts/:id` · `DELETE /api/admin/posts/:id[?permanent=true]` · `POST /api/admin/posts/:id/{publish,unpublish,restore}` · `POST /api/admin/upload` (multipart `file`, optional `maxWidth`) · `GET|POST /api/admin/categories` · `GET /api/admin/tags`.
POST/PUT bodies accept `markdown`, `category` (slug/name), `createCategory`, and `tags` (names) in addition to `content`/`categoryId`/`tagIds`.
