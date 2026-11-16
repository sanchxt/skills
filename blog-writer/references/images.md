# Images

## Always

- **Cover + OG image** with the project's cover command (Eravue: `pnpm blog cover --file <post.md>`).
- **SVG diagrams** only where a picture explains better than text (process, comparison, cost breakdown, decision tree), following the project's SVG rules.
- Look at every generated file (Read it; render SVGs to PNG to check) before publishing.

## Extra images, only when the user asks

Don't open ChatGPT or any image tool yourself. Hand off instead:

1. Decide where the image goes in the post and what it must show.
2. Write the prompt. Use the project's prompt guidance if it has any; otherwise: concrete scene tied to the section's point, editorial photography or clean illustration style, natural light, muted palette, "no text, no logos, no watermarks", no real people or brands, aspect ratio (landscape 3:2 by default).
3. Send the user, in one message:
   - the prompt in a code block, ready to paste into ChatGPT;
   - the exact drop location: the image inbox from `.seo/blog-writer.md` (Eravue: `image-inbox/` at the repo root);
   - a suggested filename (e.g. `whatsapp-bot-clinic.png`). Any name is fine; if several images are coming, ask them to use the suggested names.
4. Continue with the rest of the pipeline (writing, cover, gate) while you wait, but don't publish a post that's missing a requested image. If the user wants it published without the image, they'll say so.
5. When the user says it's there: find the newest image file(s) in the inbox, Read them to check they match, then move them (not copy) to the post's image folder (Eravue: `.seo/content/images/<slug>/<descriptive-name>.<ext>`). Reference them from the markdown with a relative path and descriptive alt text. The upload step converts and resizes them.
6. If the image is wrong (garbled text, off-topic, a logo), tell the user what to change and give an adjusted prompt.

The inbox should be empty after each run. Leave files you didn't use there and mention them.
