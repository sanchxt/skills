# Formats, platforms and accounts

## One story, several layouts

Build each video once as scenes, then render **one composition per format** that passes a `layout` prop (`"v"` 9:16, `"f"` 4:5, `"h"` 16:9). Scenes read positions and sizes from the layout, and stack, scale or crop *their own elements*. They never crop the frame. A phone mockup beside a canvas in 16:9 becomes phone-over-canvas, or alternating shots, in 9:16.

```ts
export const LAYOUTS = {
  v: { w: 1080, h: 1920, safe: { top: 220, bottom: 480, left: 90, right: 120 } },
  f: { w: 1080, h: 1350, safe: { top: 90, bottom: 220, left: 80, right: 80 } },
  h: { w: 1920, h: 1080, safe: { top: 80, bottom: 110, left: 120, right: 120 } },
} as const;
```

Register them in `Root.tsx` as `<Slug>-V`, `<Slug>-F`, `<Slug>-H`, sharing `durationInFrames` from the timing.

## Platform specs (working targets, late 2026)

| Destination | Ratio / size | Length | Notes |
|---|---|---|---|
| Instagram Reels (organic, @eravuedotcom / @lifewithcofounders) | 9:16, 1080×1920 | 30–45 s sweet spot (up to 3 min allowed) | Hook in the first 1–2 s. Cover frame chosen, centre 3:4 crop safe for the profile grid |
| Meta ads (Reels, Stories, Feed) | 9:16 master + 4:5 1080×1350 for feed (+1:1 optional) | 15–30 s | Hook must read with sound off; captions burned in; no logo in first 3 s; 3 hook variants; end card with CTA 2–3 s |
| YouTube long / Upwork / website / LinkedIn | 16:9, 1920×1080 | 60–150 s | Can be longer and calmer; chapter labels ("02 — The brain") help |
| LinkedIn feed | 4:5 or 1:1 performs well; 16:9 ok | 30–90 s | Professional tone; captions essential |
| YouTube Shorts | 9:16 | ≤ 60 s ideal | Same master as Reels |

Platforms change their UI often. Refresh these numbers with a search when this file is more than about 6 months old.

## Safe zones (9:16)

On 1080×1920, keep text and key UI out of:
- **Top 220 px** (account name, "Reels" header, ad label);
- **Bottom 480 px** (caption text, audio label, CTA button on ads, progress bar);
- **Right 120 px** (like, comment, share, save buttons);
- **Left 90 px** (margin).

That leaves roughly a 870×1220 core. Captions go just above the bottom zone (captions.md). Backgrounds and non-essential motion can run full-bleed.

Build a `<SafeZone layout />` overlay component (semi-transparent red over the no-go areas) toggled by a `showSafe` prop, and always render QA stills with it on once.

## Export

```bash
pnpm remotion render src/index.ts <Comp> out/<slug>/<slug>-v-v1.mp4 --codec h264 --pixel-format yuv420p --crf 17 --audio-bitrate 320k
node scripts/master.mjs out/<slug>/<slug>-v-v1.mp4        # -> ...-master.mp4 at -14 LUFS / -1 dBTP
```

- H.264, **yuv420p** (Remotion's default with JPEG frames is `yuvj420p`, so pass `--pixel-format yuv420p`), CRF 16–18, 30 fps, AAC 48 kHz.
- 60 fps only for heavy Kinetic Type or fast camera work, where it's visibly smoother.
- File naming: `<slug>-<v|f|h>-v<N>.mp4`, for example `missed-call-textback-v-v2.mp4`.

## Covers and thumbnails

- Reels: design a cover frame (often the hook frame with the headline) at 1080×1920, with the headline inside the centre 1080×1440 so the profile grid's 3:4 crop keeps it.
- Render it as a still: `pnpm stills <Comp> <frame>`.
- YouTube/Upwork: a 1280×720 thumbnail from the 16:9 composition (big 3–5 word headline, one visual, high contrast).

## Which account gets what

| Account | Fit | Notes |
|---|---|---|
| **@eravuedotcom** (brand) | Demos, offers, case studies, Bento recaps, news explainers in brand looks | CTA: "DM us" / "eravue.com". Posting via the `eravue-social` skill after approval |
| **@lifewithcofounders** (founders on camera) | Motion graphics as **inserts** (2–6 s) inside founder talking videos, or "how we built it" breakdowns with a face-cam bubble; the AI-news lane can use Editorial Paper inserts | Scripts come from the `lifewithcofounders` skill; the founders' faces and voices lead, and graphics support them |
| **Meta ads** | Offer ads (Kinetic, Bento), demo cut-downs, case-study proof | Campaign decisions via `cmo`. Make 3 hooks × 1 body; keep a sound-off variant |
| **YouTube / LinkedIn / Upwork / website** | Full 16:9 walkthroughs (like the 3 demos), case studies | Upwork portfolio plan: `D:\projects\eravue-portfolio\.growth\upwork\portfolio.md` |

Repurposing a long demo: take its strongest 30–45 s (the hook + reveal + one result), write a new 2 s hook, re-lay it out for 9:16, and re-time the music. Don't just trim the 16:9.
