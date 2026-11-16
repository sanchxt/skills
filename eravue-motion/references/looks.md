# The seven looks

A look is a complete visual system: palette, fonts, texture, motion personality, caption style, music mood and SFX. Pick **one per video** and don't mix them. (A Sketch annotation layer over a Midnight Glow demo is the only allowed combination.) In the studio each look is a file in `src/looks/<look>.ts` exporting `{ c, font, motion, caption, texture }`. Scenes read tokens from it and never hard-code colours.

All fonts below ship in `@remotion/google-fonts` (free for commercial use). Load only the weights you use.

**Eravue orange `#fca311`** is the brand accent. Keep it as the accent wherever the look allows, so the account feels like one brand across looks. Where it clashes (on cream, it's too light for text), use the darker brand-orange variant given, or keep orange for shapes and highlights only.

---

## 1. Midnight Glow (current house style)

**Use for:** automation and AI-agent demos, "how this system works", n8n/Claude/WhatsApp flows. The Upwork demos are the reference.

| Token | Value |
|---|---|
| bg / bg2 | `#070b16` / `#0c1324` (radial glow from top: `#16244a` at about 35% opacity) |
| surface / surface2 | `#111a2e` / `#16213a` |
| line / line2 | `rgba(255,255,255,.08)` / `.14` |
| text / dim / faint | `#eef2fb` / `#93a0bd` / `#5b6785` |
| accent | `#fca311` (orange); secondary `#6fa8ff` (blue), `#a78bfa` (purple); semantic `#25d366` ok, `#ff5d5d` alert |

- **Fonts:** Geist 400–700 (UI, headlines), Instrument Serif *italic* for the one emotional word ("AI *receptionist*"), Geist Mono 400–500 for labels, tech words and timestamps.
- **Texture:** faint dot grid (24 px pitch, 4–6% opacity), a soft vignette, a coloured glow behind the active element (`box-shadow: 0 0 40px <accent>55`), and a corner glow in a second hue at 10–15%.
- **Motion:** blur-rise entrances (opacity + 24 px rise + 8 px blur), standard springs, and a slow camera pan and zoom across a large canvas. Data pulses travel along node edges, and a node lights up when it's spoken about. Phone mockups with real-looking chat bubbles typing in.
- **Captions:** minimal dim-to-bright line (16:9), chunk + accent (9:16).
- **Music:** airy tech or showreel, 75–100 BPM, soft synth pads with a clear drop.
- **SFX:** soft pop on bubbles, tick on node lighting, airy whoosh on camera moves, ding on success.
- **Don't:** neon overload. Keep it to at most 2 glowing things at once, and the rest dim.

## 2. Editorial Paper (minimal)

**Use for:** AI and tech news explainers, opinions and "what this means for you", case-study stories, thought leadership. It feels like a well-designed magazine.

| Token | Value |
|---|---|
| bg | `#f3eee4` (warm cream); alt panel `#ebe4d6` |
| surface | `#fbf8f2` (cards), hairline `rgba(20,18,16,.14)` |
| ink / dim / faint | `#141210` / `#5f584e` / `#9a9184` |
| accent | `#d9480f` (deep brand orange, readable on cream); highlighter `rgba(252,163,17,.38)` |
| secondary | `#1f3a5f` (ink blue) for charts and links |

- **Fonts:** Instrument Serif (headlines, large, regular and italic) or Newsreader for longer serif text; Inter Tight 400–600 for body and labels; IBM Plex Mono for dates, sources and figure numbers ("FIG. 02").
- **Texture:** paper grain (SVG `feTurbulence` noise, 5–7% multiply), hairline rules, a 12-column grid with visible margins, small caps labels, footnote numbers and source lines ("Source: Reuters, 14 Nov 2026").
- **Motion:** calm and precise. Mask-wipe reveals line by line, underlines that draw, highlighter strokes swept behind words, and charts that draw their axes and then their data. Ease-out-quint over 18–24 frames. No bounce, no glow, no blur-rise (use a clean mask or fade instead). Page-turn or slide transitions between "sections".
- **Captions:** editorial lower third (serif, ink on cream, highlighter on the key word).
- **Music:** minimal piano, soft lo-fi or light pizzicato, 80–95 BPM. Understated.
- **SFX:** paper slide, pen scratch on underlines, a soft typewriter key for dates. Very quiet.
- **Don't:** use pure white, or more than one accent. Big serif headlines need tight tracking (-2%).

## 3. Kinetic Type

**Use for:** ads, hooks, offer videos, punchy news hooks, music-led text-only cuts for sound-off placements.

| Token | Value |
|---|---|
| bg | `#0a0a0a` (near black; pure `#000` allowed here), invert frames `#f5f5f0` |
| text | `#f5f5f0` |
| accent | `#fca311`, or for a sharper ad energy `#d4ff3f` (electric lime). Choose one |
| dim | `#6b6b6b` |

- **Fonts:** Inter Tight 800–900 or Archivo Black for slam words; Instrument Serif italic for the one contrast word; JetBrains Mono for small labels. Optionally Anton or Bebas Neue for very tall condensed stacks (vertical).
- **Texture:** none, or subtle film grain (3%). Big negative space and the type is the image.
- **Motion:** words land **on the beat** (use `beats.mjs`): scale punch 1.12 → 1 in 6–8 frames, mask slide-ups, word swaps on downbeats, stacked lines that build. Snap the camera zoom on drops. Inverted flash frames are allowed but used sparingly (≤ 2 per second, never strobing). Hold the key line for at least 1 s.
- **Captions:** the type *is* the caption (style D, kinetic big words). Don't add a second caption track.
- **Music:** punchy, 105–128 BPM, clear kick, drops.
- **SFX:** hits and impacts on slams (quiet), riser into a drop, a short whoosh on swaps.
- **Don't:** animate every word differently. Use 2–3 move types total, repeated with rhythm.

## 4. Liquid Glass (premium, Apple-like)

**Use for:** premium service offers, product or feature launches, "the future of X", brand films.

| Token | Value |
|---|---|
| bg | dark: `#0b1020` with slow-moving mesh blobs `#3b5bdb`, `#7c5cff`, `#fca311` at 25–40% under heavy blur. Light alt: `#eef1f7` with pastel blobs |
| glass card | fill `rgba(255,255,255,.07)`, `backdrop-filter: blur(28px) saturate(140%)`, border `1px rgba(255,255,255,.18)`, top highlight gradient `rgba(255,255,255,.22)→0` |
| text / dim | `#f4f6fb` / `rgba(244,246,251,.62)` |
| accent | `#fca311` used sparingly, as glows and small dots |

- **Fonts:** Inter Tight or Geist (SF-like neutrality) 300–600. Big light headlines (300) with one bold word. Geist Mono for small specs.
- **Texture:** depth. Use 3 parallax layers (bg blobs, glass cards, foreground text), depth-of-field blur on far layers, soft shadows (`0 30px 80px rgba(0,0,0,.35)`), specular sweeps across cards.
- **Motion:** slow and weighty. Springs with high damping (`damping 22, mass 1.1, stiffness 90`), cards that scale 0.96 → 1 with opacity, a slow camera dolly with parallax, and blobs that drift continuously (sin-based, period 8–12 s). Transitions take 24–36 frames: push-through-glass or soft zoom-blur.
- **Captions:** chunk + accent, or minimal line with a soft glass pill behind it.
- **Music:** ambient electronic or cinematic minimal, 85–105 BPM, wide pads, a gentle swell instead of a hard drop.
- **SFX:** soft glassy chimes, low swells. Barely there.
- **Performance:** `backdrop-filter` is expensive to render. Keep it to 3 or fewer glass elements per frame, and pre-render static blurred backgrounds as images.

## 5. Terminal / Dev

**Use for:** tutorials, "here's how to build this", prompts, code, API and automation internals, the "comment WORD for the workflow" lane.

| Token | Value |
|---|---|
| bg / panel | `#0d0f12` / `#15181d`, window chrome `#1d2127` with 3 dots |
| text / dim | `#d6dde6` / `#7a8594` |
| syntax | green `#3fdc85`, amber `#ffb547`, blue `#61afef`, purple `#c792ea`, red `#ff6b6b` |
| accent | amber `#ffb547` (close to brand orange) or `#fca311` |

- **Fonts:** JetBrains Mono 400–700 for almost everything; Geist 600 for the rare big title.
- **Texture:** optional scanlines at 2–3%, and a slight phosphor glow on the prompt line. Rounded window panels on a plain dark field.
- **Motion:** typewriter at 30–45 chars/s, with a blinking block cursor (on/off every 16 frames at 30 fps). Output prints line by line. Use instant cuts, highlight boxes that snap around the important line, zoom-ins on code, and a split screen (code left, result right) in 16:9 that stacks in 9:16.
- **Captions:** terminal style (mono, with `>` prefix and cursor), or chunk + accent in mono.
- **Music:** lo-fi, minimal techno or synthwave, 90–120 BPM.
- **SFX:** soft mechanical key clicks (randomised, quiet), an enter thunk, a success chime.
- **Don't:** show real API keys, emails or client data in "code". Use obvious placeholders.

## 6. Bento Product Grid

**Use for:** "what we do" service overviews, case-study results, feature lists, monthly recaps, offer ads with 3–6 points.

| Token | Value |
|---|---|
| bg | `#09090b` (dark) or `#f5f5f7` (light, Apple-store feel) |
| card | dark `#141418` / light `#ffffff`, radius 28–36, gap 16–24 px, border `1px rgba(255,255,255,.06)` |
| text / dim | `#fafafa` / `#a1a1aa` (dark); `#111` / `#6e6e73` (light) |
| accent | `#fca311` for the hero stat; one tint per card is too much, so tint at most 1 card |

- **Fonts:** Geist or Inter Tight 500–700. **Big tabular numerals** (`font-variant-numeric: tabular-nums`) for stats; Geist Mono for small captions inside cards.
- **Texture:** clean. Each card holds one idea: a stat, an icon plus a line, a mini UI, or a tiny chart.
- **Motion:** cards enter with a 3–4 frame stagger (scale 0.94 → 1, opacity, 12 px rise). Numbers count up with an ease-out. A card **expands to fill the frame** (layout morph) to dive into its detail, then collapses back. Gentle hover-like lifts on the card being spoken about.
- **Captions:** chunk + accent.
- **Music:** upbeat modern tech, 100–120 BPM.
- **SFX:** soft clicks per card, a ding on the hero stat.
- **Layout:** 9:16 uses 2 columns × 3–4 rows; 16:9 uses 3–4 columns × 2 rows; 4:5 uses 2 × 3.

## 7. Sketch Annotations

**Use for:** website/Instagram/funnel teardowns ("3 things killing your enquiries"), before/after, walkthroughs of real tools and screens, Upwork-style audits. It feels human and unpolished on purpose.

| Token | Value |
|---|---|
| base | real screenshots or screen recordings, slightly desaturated (`saturate(.85)`), on `#f6f3ee` paper or `#111` dark |
| marker red | `#ff4d4d`; ink blue `#2f6bff`; highlighter yellow `rgba(255,214,0,.45)` |
| accent | `#fca311` marker for the "fix" |

- **Fonts:** Caveat 600–700 or Kalam for handwritten notes, Permanent Marker for one shouty word, Inter Tight for clean body text.
- **Texture:** grain (5%), slightly imperfect strokes (use `roughjs` for SVG paths with a fixed `seed`, so frames are deterministic), tape or sticky-note shapes.
- **Motion:** strokes draw on (`strokeDashoffset`) in 10–16 frames, circles overshoot their start point, arrows draw and then their head pops. For a hand-made feel, a "boil": redraw the stroke with a new seed every 3–4 frames, with very little roughness. Zoom-ins on the problem area, with a Ken Burns drift on stills.
- **Captions:** chunk + accent, with the accent word in marker colour, or no captions when notes carry the message.
- **Music:** indie, acoustic or lo-fi, 85–100 BPM.
- **SFX:** marker squeak (quiet), paper tap, pop on sticky notes.
- **Don't:** annotate everything. Use 1–3 marks per screen, and show the fix right after the problem.
- **Pencil-on-paper variant (built):** the whole video drawn in graphite on off-white paper, not only marks over screenshots: pencil phone and workflow, handwritten labels, taped white cards for real UI, Eravue deep orange as the single marker colour. Reference: `IgInstantReplySketch-V` in the studio. The reusable hand-drawn kit (marks that fit text, arrows, doodles, paper/sticky/taped cards, screenshot markup, sketch charts, paper transitions, pencil SFX) is in `src/components/sketch/`, shown in the `SketchKit-V` sheet and listed in studio-setup.md.

---

## Choosing quickly

| Video | First choice | Alternative |
|---|---|---|
| Automation/agent demo | Midnight Glow | Liquid Glass (premium client pitch) |
| AI/tech news | Editorial Paper | Kinetic Type (hook) → Paper (body) as a *cut*, not a mix |
| Case study / results | Bento | Editorial Paper |
| Tutorial / how-to | Terminal | Midnight Glow |
| Offer / service ad | Kinetic Type | Bento, Liquid Glass |
| Teardown / audit | Sketch | Editorial Paper |
| @lifewithcofounders inserts | match the founder video's palette: neutral Midnight or Paper, kept short (2–6 s inserts) | none |

Rotate looks across the feed so the grid doesn't feel samey. Within a **series**, keep one look, so people recognise it.
