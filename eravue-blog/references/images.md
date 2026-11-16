# Images for Eravue posts

Put all local images for a post in `.seo/content/images/<slug>/` (gitignored; the uploaded copies live on the CDN). Reference them with relative paths from the post file. `push` uploads them and rewrites the paths to CDN URLs.

**Always look at each image (Read the file) before pushing.** Fix anything clipped, misspelled, off-brand or illegible.

## 1. Cover + OG image (every post)

```bash
pnpm blog cover --file .seo/content/articles/<file>.md
```

Produces a 1600×900 cover and a 1200×630 OG image in the site's style (Instrument Serif title, Geist Mono labels, dot grid) and links both in the frontmatter. Tones: `night` (dark), `signal` (lime), `paper` (cream). The default tone is picked per category so a category keeps a consistent look; override with `--tone`. Use `--eyebrow` to change the small top-right label (default: the category name). If the title is very long, the text shrinks to fit; check it's still readable.

A cover can also be an AI image (section 3) when a strong visual helps, but keep the generated OG image so social cards stay on-brand.

## 2. SVG diagrams (when a picture explains better than text)

Good uses: process flows, architecture, comparisons, cost breakdowns, timelines, decision trees. Don't add decorative SVGs.

Write the SVG by hand and save it as `.seo/content/images/<slug>/<name>.svg`. Embed it with `![Descriptive alt text](../images/<slug>/<name>.svg)`.

**Rules (the upload rejects anything else):**
- No `<script>`, `<foreignObject>`, `<iframe>`/`<embed>`/`<object>`, `<a>`, `on*=` attributes, `javascript:`, `<!DOCTYPE>`/`<!ENTITY>`, CSS `@import`.
- `href`/`xlink:href` only to in-document ids (`#arrow`) or embedded `data:image/png;base64,...`. CSS `url()` only to `#ids`.
- Max 1MB.

**Style so it matches the site:**
- `viewBox` around `0 0 1200 675` (16:9) or `0 0 1200 800`. Set `width="1200"` and the matching `height`, and keep it legible at 360px wide: body text ≥ 22px in viewBox units, labels ≥ 18px, max ~6–8 words per box.
- Colours: ink `#141414`, muted `#5f5b53`, paper `#f3efe6`, paper-2 `#ebe6da`, line `#d6d0c4`, signal (accent, use sparingly) `#d7ff3d`, night `#0d0d10`. Use a paper or white background so it sits well in the article.
- Fonts: `font-family="Geist, ui-sans-serif, system-ui, sans-serif"` for labels, `"Instrument Serif", Georgia, serif` for an optional headline. Fonts inside an `<img>` SVG come from the viewer's system, so keep text simple and leave padding for wider fallback fonts.
- Rounded rects (`rx="16"`), 2px strokes, arrows via a `<marker>` defined in `<defs>`.
- Include `<title>` inside the SVG matching the alt text.

To check it renders, convert to PNG and look at it:
```bash
node -e "require('sharp')('in.svg').png().toFile('preview.png')"
```

## 3. AI-generated images (only when the user asks for one)

By default a post gets the cover/OG image plus SVG diagrams only. Add an AI image only when the user asks.

### Route A: hand-off through the image inbox (default)

The user generates the image in their own ChatGPT. Don't open ChatGPT or drive it yourself.

1. Write the prompt (guidance below) and send it to the user in a code block, with the drop folder **`image-inbox/` at the repo root** and a suggested filename (e.g. `clinic-whatsapp-bot.png`). Say `Landscape 3:2 aspect ratio` in the prompt unless another shape fits better.
2. Carry on with the rest of the post while you wait, but don't publish until the image is in (or the user says to go without it).
3. When the user says it's there, take the matching file(s) from `image-inbox/`, Read each to check it, and **move** it to `.seo/content/images/<slug>/<descriptive-name>.<ext>`. Reference it with a relative path and descriptive alt text. `push` uploads it, converts it to WebP and resizes it.
4. If it's wrong (garbled text, a logo, off-topic), say what's wrong and give an adjusted prompt.
5. Never put anything private in prompts (client names, contact details, unreleased plans).

### Route B: OpenAI API (only if `OPENAI_API_KEY` is set in `.env.blog` and the user asks for it)

```bash
pnpm blog image --prompt "..." --out .seo/content/images/<slug>/<name>.png --size 1536x1024
```

Prompt guidance:
- Describe a concrete scene or object tied to the section's point (e.g. "a small Indian bakery owner checking orders on a tablet at the counter, morning light"), plus style: "editorial photography, natural light, muted warm palette, shallow depth of field".
- Add "no text, no logos, no watermarks". Generated text is usually garbled; put words in the article or an SVG instead.
- Avoid real people, brands, trademarks and lookalikes of real products.
- Route B only: `--quality high` for covers/hero images, `medium` for inline images.

Use 0–2 AI images per post. Every image needs alt text.
