# Captions

Most short-form is watched with the sound off, so captions carry the message for half the audience. They must be readable, in sync, and stay out of the way of the visuals. All styles are driven by the same word timings (`timing.json` words with `t`), so they're always in sync.

The user picks the style per video. If they don't: **A** for 9:16 and 4:5, **B** for 16:9.

## The styles

**A. Chunk + accent words (vertical default)**
- 2–4 words at a time (≤ 22 characters), centred, 1 line (2 max), in the look's sans at weight 700. Size 54–68 px (9:16).
- Key words (results, numbers, names, the noun that matters) are in the look's accent colour. At most 1 accent word per chunk, and not every chunk.
- Entrance: a 4–6 frame pop (scale 0.92 → 1 with opacity, `firm` spring). The active word sits at full opacity, the rest at about 85%.
- No box. Shadow `0 3px 14px rgba(0,0,0,.6)`, or a 3 px dark stroke via `paint-order: stroke` on light backgrounds.

**B. Minimal line, dim-to-bright (16:9 default; the current demos)**
- One centred line at the bottom, no box. Upcoming words wait at about 34% opacity and brighten as spoken. The line rises in with a slight blur and drifts out.
- Uses a soft bottom gradient only while a line is on screen. Montserrat 500 or the look's sans at 34–40 px.
- Built: `src/components/Subtitles.tsx` in the demos repo, `captions/MinimalLine.tsx` in the studio.

**C. Karaoke pill**
- A line of 3–6 words, with a rounded accent pill sliding behind the active word (the pill moves word to word with a `pop` spring). Energetic and readable. Good for tutorials and Bento.

**D. Kinetic big words (Kinetic Type look, hooks)**
- 1–3 words fill the frame, centre or upper-middle, in sync with speech or the beat. This replaces the caption track, so don't add another.
- Use it only for hooks and ads. A full 45 s of this is tiring unless the look is Kinetic.

**E. Editorial lower third (Paper look)**
- A serif (Instrument Serif 48–56 px in vertical), ink on cream, left-aligned in a column, 1–2 lines.
- The key word gets a highlighter sweep (`rgba(252,163,17,.38)`) as it's spoken.

**F. Terminal (Terminal look)**
- Mono, `> ` prefix, typed in at speech pace with a block cursor. Green or amber for the key word.

**G. None**
- For music-only cuts, where on-screen text already says everything, or for founder videos where the edit adds its own captions.

## Placement and safe zones

- 9:16 vertical: the caption block's **bottom edge sits 420–520 px above the frame bottom**, centred, within 90 px side margins. Reels UI (caption text, buttons, progress bar) covers roughly the bottom 310–480 px and the right 120 px. Never place captions in the top 220 px.
- If a scene's important UI is in the caption lane, move captions to the upper-middle third for that scene (a per-scene `captionLane: "low" | "high"` prop). Never cover what's being explained.
- 4:5: bottom 220–300 px. 16:9: bottom 70–90 px (line style).

## Chunking rules

- Break at phrase boundaries: after commas and conjunctions, before prepositions when needed. Never split "₹1,500", "24/7", "9 AM", a name, or a number from its unit.
- Minimum 0.25 s per chunk on screen. If the speech is faster, merge chunks rather than flicker.
- A chunk leaves when the next starts. In a pause longer than 0.4 s, it holds up to 0.35 s after its last word, then fades.
- Drop the final full stop and comma of each chunk. Keep "?" and "!" only if they matter.
- Fix spelling from the script or transcript, never from whisper's guess (brand words especially).
- Numbers as digits; "and" for "&" unless it's a brand name.

## Emphasis selection (style A, C, E)

Pick, in order:
1. numbers and results ("3 minutes", "40%", "₹8,000");
2. the outcome noun ("booked", "replied", "lost");
3. names of tools or brands when they're the point (n8n, Claude);
4. contrast words ("never", "every", "instantly").

At most about 1 in 3 chunks gets an accent. When everything is emphasised, nothing is.

## Implementation notes

- The SRT → `captions/<slug>.json` pipeline exists (`scripts/captions.mjs` in the demos repo). It merges short lines and fixes n8n and 24-hour times, and a `show` override changes on-screen text without touching the SRT.
- For style A, chunk from `timing.json` words directly (true word times beat SRT estimates).
- Built in the studio (2026-11-16): A `ChunkAccent` and B `MinimalLine` (`captions/ChunkAccent.tsx`, `MinimalLine.tsx`); C `KaraokePill`, D `KineticWords`, E `EditorialLine`, F `TerminalLine` (`captions/styles.tsx`). They all take `{ frame, chunks, look, layout, lane?, size? }`, with chunks from `makeChunks(words, accentWords, opts)`. Pass the style's preset as `opts` (`KARAOKE_CHUNKS` 6 words/30 chars, `KINETIC_CHUNKS` 3/18, `EDITORIAL_CHUNKS` 8/38, `TERMINAL_CHUNKS` 6/30; the default is 4/22 for style A). See them in `pnpm stills UiKit-V 700 820 940 1060`.
- KaraokePill and KineticWords measure words, so the fonts must load first. They handle that themselves (`useFontsReady`), but any new measured style must do the same (see studio-setup.md, "Measuring text").
