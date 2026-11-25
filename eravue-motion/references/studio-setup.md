# The studio: D:\projects\eravue-motion

One Remotion project for every Eravue motion video. It shares looks, components and scripts, with one folder per video. It was set up on 2026-11-16 from the demos repo (`D:\projects\eravue-automations\videos`), which stays as is for the Upwork demos. Its README.md has the commands, and its CLAUDE.md the house rules.

## What's there

```
eravue-motion/
  package.json            pnpm; remotion + every @remotion/* pinned to the SAME version (4.0.543): never mix versions
  .npmrc                  pnpm store + cache on D: (shared with eravue-automations)
  remotion.config.ts      h264, crf 17, jpeg 95, yuv420p, 320k audio, concurrency 4
  src/
    index.ts, Root.tsx    formats(id, Component, frames, ["v","f","h"]) registers <Id>-V / -F / -H
    theme.ts              FPS + Midnight c/font for the components ported from the demos
    looks/                types.ts (Look type, BRAND) + midnight paper kinetic glass terminal bento sketch, index.ts (all; LookSheet only)
    lib/                  anim.ts (ease, pop, win, riseStyle, typed), timing.ts (makeCues, captionWords), measure.ts (textBox, useFontsReady, trackFont),
                          beats.ts (beatTimes, downbeats, snapToBeat, arrangedBeats), layout.ts (LAYOUTS, safeRect, VideoProps), fx.ts
    components/           Background Beam CallScreen Canvas Cards Chat Phone Sfx (Midnight, from the demos), SafeZone, Grain
                          Rough (roughjs: Rough, arrow, roundRect, WriteOn, Highlight, Tape, PENCIL), SketchFlow (pencil n8n canvas),
                          InstaDM (InstaChat, LockScreen, IgIcon: Instagram DM / iOS lock-screen skins), RollText (odometer/clock roll)
                          Glass (MeshBg, GlassCard), TerminalWindow, Bento (BentoGrid), CountUp, EndCard
      sketch/             the hand-drawn kit; import everything from components/sketch (index.ts barrel)
      captions/           ChunkAccent (+ makeChunks), MinimalLine, styles.tsx (KaraokePill, KineticWords, EditorialLine, TerminalLine)
    videos/_look-sheet/   LookSheet: every look in every format; a reference and smoke test, not a post
    videos/_kit-sheet/    SketchKit-V and UiKit-V: every reusable component on one page each (reference + smoke test)
    videos/<slug>/        one folder per video: scenes, script.json, timing.json, captions.json
  public/brand, public/sfx, public/<slug>/ (vo.wav, bed.wav; git-ignored)
  vo/<slug>/              words.json, captions.srt, srt-beats.json, cuts.json, voice.json, beats.json, scratch.tsv
  music/                  beds.json (defaults, tracks registry, beds per slug), LICENSES.md
  scripts/                paths.mjs (where every file of a slug lives) + voice beats master audio-lib (this skill)
                          + align sync-vo srt-words captions music-bed vo-from-cuts finish-video voice-chain stills sfx
                            scratch-vo.ps1 premiere-cuts.py (ported to the per-slug layout)
```

**Built (reuse these; see them all in `pnpm stills SketchKit-V 60 180 300 420 540 660 760 830` and `pnpm stills UiKit-V 70 190 310 400 520 580 700 820 940`, 4 s per page):**

*Hand-drawn / paper kit* (`src/components/sketch/`, built 2026-11-16; import from `components/sketch`). Everything draws on from `at`, is deterministic by `seed`, and takes `boil` (re-seed every N frames once drawn, for a live pencil wobble).
- **Rough** (`components/Rough.tsx`): `Rough` draws roughjs shapes (rect, ellipse, line, curve, path) in sequence; `arrow()`, `roundRect()`, `WriteOn` (handwriting reveal), `Highlight`, `Tape`, `PENCIL`.
- **Marks that fit their text** (`Marks.tsx`): `<Mark kind="circle|box|underline|double|squiggle|strike|cross|highlight" font={...}>word</Mark>` measures its children and sizes the mark to them (pass `w`/`h` for non-text). Give it the same font spec as the text.
- **Arrows**: `<SketchArrow from to kind="curve|straight|elbow|loop" bend double head />`; the head pops after the shaft. `connect(boxA, boxB)` gives edge-to-edge points between two rects.
- **Doodles**: `<Doodle kind="star|sparkle|burst|ticks|check|x|exclaim|heart|moon|brace-right|brace-down" x y size fill />`. Raw shape builders are in `shapes.ts`.
- **Paper pieces** (`Paper.tsx`): `PaperBg` (mottle, vignette, grain; `ruled`/`grid` options), `TapedCard` (tape top/corners/none), `StickyNote`, `SketchPhone`, `SketchAvatar`, and `ScreenshotMarkup`: a real screenshot, desaturated, slowly drifting, zooming between `focus` rects, with Marks/Arrows as children in image pixels (they ride the zoom).
- **Charts & counts** (`Charts.tsx`): `SketchBars` (hachure bars, one `hero` bar in the accent), `SketchLine`, `Tally` (tally marks), `HandCount` (CountUp in the hand font). Real numbers only.
- **Transitions** (`Transitions.tsx`): `PageTurnOut` and `EraseOut` wrap the outgoing scene (render the next one underneath); `ScribbleWipe` covers the frame with strokes, so swap scenes at its midpoint (paper colour = a wipe that paints over; pencil grey = scribbled out).
- **SketchFlow**: the n8n canvas in pencil (same nodes/edges/`camAt` camera as `Canvas`, `lit` rings, marker `flows`).
- **Pencil SFX**: `pencil` (scribble), `marker` (squeak), `paper` (rustle), `tape` (rip), `page` (turn) in `public/sfx` (made by `pnpm sfx`), played with `<Sfx>`.
- Palette: the Sketch look with `accent: BRAND.orangeDeep` (one marker colour per frame; red only for problems). First used in `videos/ig-instant-reply/IgInstantReplySketch.tsx`, which predates the kit and keeps local copies of the paper pieces; new videos use the kit.

*Other looks:*
- **Glass** (`Glass.tsx`): `MeshBg` (drifting blurred blobs from the look's colours) + `GlassCard` (frosted card, `p` entrance, `sheenAt` light sweep).
- **TerminalWindow**: macOS-style window; `lines` typed at `TYPE_CPS` (`cmd` with prompt, `out`, `comment`, or coloured `segs`), blinking cursor, `hl` line highlight.
- **BentoGrid** (`Bento.tsx`): cards on a cols x rows grid with spans, staggered entrance, `tint`, `liftAt`/`liftOff` and `expandAt`/`collapseAt` (one card grows over the grid).
- **CountUp**: tabular numerals, en-IN grouping (₹1,50,000), prefix/suffix, decimals.
- **EndCard**: logo (dark/light by look), headline + expressive second line, CTA pill (a pencil box on Sketch), handle. The only place the logo appears in Reels/ads.
- **Caption styles** (`captions/styles.tsx`): `KaraokePill`, `KineticWords`, `EditorialLine`, `TerminalLine`, each fed by `makeChunks(words, accents, <STYLE>_CHUNKS)` (chunk presets exported next to them).
- **Instagram DM + iOS lock screen** skins (`InstaDM.tsx`) and **RollText**.
- **Shared cues per video:** keep `T` in `videos/<slug>/cues.ts` so every style of one video re-times from the same `timing.json`.

**Measuring text** (anything sized to a word): use `textBox()` from `lib/measure` and call `useFontsReady()` at the top of that component. Every look registers its fonts with `trackFont(loadFont(...))`; do the same in any new look. Don't call `@remotion/layout-utils`' `measureText` directly: Google fonts arrive after the first render and it caches that first (fallback-font) width, which made marks come out short and kinetic words overflow. Looks load `latin` + `latin-ext` so ₹ renders in the brand font.

**2026-11-20: the kit merge.** Everything reusable now goes through `src/components/index.ts`, and the studio's KIT.md is the live catalog. Use it instead of the lists above.
- **Footage:** `ClipFrame` + `framings`.
- **Captions:** one `Captions` component with 7 eravue styles + 39 ReelStudio presets.
- **Transitions:** `Blend`/`Accent`/`Overlay`/`TransitionSound`, 39 ReelStudio presets.
- **Editorial paper pieces**, plus `LookBg`.
- **Vendoring:** ReelStudio's engines are copied by `pnpm sync:reel` into `src/vendor/`.
- **Temp files:** Remotion temp goes to `.tmp/` on D: (`scripts/tmp-dir.mjs`), because C: is nearly full.

## Starting a new video

`pnpm new <slug> <clip|voice> --look paper --voice default --handle @x` does all the setup. Then fix `script.json` from `vo/<slug>/check.md` and run `pnpm vo:align`. Write `cues.ts`, build the scenes from the kit, and run `pnpm compose <slug>` (original music fitted to the story moments), `pnpm stills`, then `pnpm ship <slug>`. Details are in the studio's KIT.md and README.md.

## Commands

```bash
pnpm voice analyze "<raw>"                      # report + suggested chain
pnpm voice process "<raw>" public/<slug>/vo.wav # clean + level to -16 LUFS, writes .ab.wav to listen to
pnpm vo:sync <slug>                              # word timings via large-v3-turbo (GPU; --engine xxl = Subtitle Edit medium.en) -> timing.json
pnpm vo:scratch -Id <slug>; pnpm vo:align <slug> # robotic placeholder for timing only
pnpm vo:cuts <slug> "<raw>"                      # rebuild VO from Premiere cuts (vo/<slug>/cuts.json)
pnpm vo:srt <slug>; pnpm captions <slug>         # timing / caption lines from vo/<slug>/captions.srt
pnpm beats "<track>" --json vo/<slug>/beats.json # tempo, grid, drops
pnpm music <slug>                                # bed from music/beds.json
pnpm studio                                      # live preview
pnpm stills <Comp> 0 60 300 --safe [--full]      # QA stills into out/stills/
pnpm render <Comp> out/<slug>/<slug>-v-v1.mp4    # config already sets h264/yuv420p/crf 17
pnpm master out/<slug>/<slug>-v-v1.mp4           # -14 LUFS / -1 dBTP + spec check
pnpm finish <slug> in.mp4 out.mp4                # audio treatment for a Premiere-edited video
```

## If it ever needs rebuilding

Copy `.npmrc`, `tsconfig.json` and the package versions from the demos repo; copy the demos' `src/lib`, `src/components`, `public/sfx` and logos; copy this skill's `scripts/*.mjs`; recreate the looks from looks.md; then `pnpm install`. Optional, ask first: Remotion's official agent skills in the studio (`npx skills add remotion-dev/skills`, see remotion.dev/docs/ai/skills).

## Licence

Remotion is free for individuals and companies of up to 3 people. Eravue qualifies while it's 3 or fewer. Above that it needs a Remotion Company License (check remotion.dev/docs/license for current pricing).

## Tools that must exist

- Full **ffmpeg/ffprobe** on PATH (installed via winget: Gyan.FFmpeg 8.x, includes loudnorm, sidechaincompress, deesser, afftdn, silenceremove).
- Node 20+ (installed: v26) and pnpm (installed: 10).
- Python: `premiere-cuts.py` (stdlib only); `whisper-turbo.py` runs with ReelStudio's venv (`D:\projects\SOCIAL MEDIA\short-form-quick-edits\.venv`: faster-whisper + CUDA 12 wheels). Model: large-v3-turbo in `E:\.cache\hub` (`HF_HOME=E:\.cache`).
- Subtitle Edit (`D:\Subtitle Edit`) with Purfview Faster-Whisper-XXL + medium.en as the fallback for word timings (`--engine xxl`; `WHISPER_XXL_DIR` overrides the folder).
