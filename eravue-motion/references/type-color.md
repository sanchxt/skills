# Typography and colour

## Type sizes (px at the composition size)

These are minimums for comfortable reading on a phone. Vertical video is watched on a 6-inch screen, so err bigger.

| Role | 9:16 (1080×1920) | 4:5 (1080×1350) | 16:9 (1920×1080) |
|---|---|---|---|
| Hero headline (3–7 words) | 96–150 | 88–130 | 72–120 |
| Kinetic slam word | 160–280 | 140–240 | 140–220 |
| Section title / card title | 56–72 | 52–64 | 40–56 |
| Body / card text | 40–52 | 38–48 | 30–40 |
| Captions | 54–68 (chunk style); 46–52 (line style) | 50–60 | 34–40 |
| Labels, mono tags, sources | ≥ 28 | ≥ 26 | ≥ 20 |
| UI inside a phone mockup | Scale the mockup so chat text is ≥ 28 on the final frame, or zoom the camera in | | |

Phone check: render a still, view it at 1/3 size (about 360 px wide for vertical). If you squint to read it, it's too small.

## Pairing rules

- At most **2 families + 1 mono** per video, as given by the look.
- Contrast pairs work: a neutral grotesk (Geist, Inter Tight) with an expressive serif italic (Instrument Serif) for one emotional word per headline. Not every headline needs the serif.
- Weight does the hierarchy before size and colour do: 400 body, 500–600 UI, 700–900 headlines (Kinetic only for 800+).
- Mono marks "machine" things: tool names, code, numbers in tables, timestamps, source lines.

## Spacing and setting

- Tracking: display sizes (≥ 72 px) get -2% to -4% (`letterSpacing: "-0.03em"`); body 0; small caps or mono labels +4% to +10%.
- Line height: headlines 1.0–1.1; body 1.3–1.45; captions 1.15–1.2.
- Line length: headline lines of 3–4 words in vertical; body ≤ 32 characters per line in vertical, ≤ 60 in 16:9.
- Numbers: `fontVariantNumeric: "tabular-nums"` anywhere they change or align.
- Write "n8n", "WhatsApp", "Claude", "ChatGPT", "eravue.com" exactly. Use 24-hour times or "9 AM" consistently, and digits for numbers.
- Spacing grid: multiples of 8 px. Outer margins 64–96 px (vertical, inside the safe zone), 80–120 px (16:9).
- Align to a grid. Left-aligned text reads faster than centred for anything longer than one line, except captions and single hero lines.

## Colour

- **Roles, not colours.** Every look defines `bg, surface, line, text, dim, faint, accent` (+ semantic `ok, warn, alert`). Scenes only use roles.
- **One accent per frame.** The accent marks *the* thing being talked about. If two things are accented, neither is.
- **60-30-10:** background 60%, surfaces and secondary 30%, accent ≤ 10%.
- **Dark looks aren't pure black** (`#070b16`, `#0d0f12`, `#09090b`), except Kinetic Type. Pure white text on near-black is fine. Use `#eef2fb`-ish to avoid glare.
- **Contrast:** body text ≥ 4.5:1 against its background, large text ≥ 3:1. Dim text is for secondary information only, never for the thing being said.
- **Saturated colours on dark** read as glow. Use them for small elements and lights, not big fills.
- **Semantic colour:** green = success or sent, red = problem or alert, amber = waiting or attention. Don't use red for decoration.
- **Gradients:** subtle, same-family hues (navy → indigo), or mesh blobs in the Glass look. No rainbow gradients.
- **Brand:** Eravue orange `#fca311` (accent), deep orange `#d9480f` on light backgrounds, logos in `D:\projects\eravue-automations\videos\public\eravue-logo-{dark,light}.webp` (copied into the studio's `public/brand/`).

## Captions and text on busy backgrounds

Use a soft bottom gradient, a text shadow (`0 2px 18px rgba(0,0,0,.7)`), or a pill behind the text. Never put plain text on a mid-tone busy image.
