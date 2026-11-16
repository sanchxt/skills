# Motion rules

Good motion graphics feel **inevitable**: every movement explains something, arrives with the word, then gets out of the way. Cheap ones move everything, all the time, in different ways.

## Principles

1. **One hero move per beat.** Each sentence gets one main movement (a reveal, a camera move, a data pulse). Everything else is still or drifting quietly.
2. **Hierarchy through motion.** The most important element moves first, biggest, longest. Secondary elements follow with a stagger and smaller moves.
3. **Lead the word slightly.** A visual should *arrive* as the word is heard. Start its entrance 2–4 frames before the cue, so that most of the movement is done on the word. Text that is spoken can appear with the word; text that adds information needs reading time (below).
4. **Consistency.** A video uses 2–4 move types, repeated. The same kind of thing always enters the same way.
5. **Continuity.** Prefer camera moves and transforms over cuts inside a scene. Objects that persist (a phone, a node graph) stay put while the camera travels. Match cuts between scenes (a card becomes the next scene's background).
6. **Never dead, never busy.** No frame is completely frozen for more than about 1.5 s: keep a subtle drift, a breathing glow, or slow camera push of 1–2% scale over a few seconds. But never more than about 3 independent movements at once.
7. **Physics feel.** Things have weight: use ease-out for arrivals, ease-in for exits, springs for UI-like elements. Linear only for continuous things (rotation, scroll, progress bars, drift).

## Easing presets (cubic-bezier)

| Name | Curve | Use |
|---|---|---|
| `out` (default arrival) | `0.22, 1, 0.36, 1` (ease-out-quint-ish) | entrances, camera settles, reveals |
| `in` (exit) | `0.55, 0, 0.75, 0.2` | exits; exits are faster than entrances |
| `inOut` | `0.65, 0, 0.35, 1` | camera moves between two points, morphs |
| `snap` | `0.16, 1, 0.3, 1` | Kinetic Type slams, highlight boxes |
| `soft` | `0.33, 0, 0.2, 1` | Liquid Glass, Paper |

These match `ease()` / `win()` in the existing `src/lib/anim.ts`. Keep using those helpers.

## Spring presets (Remotion `spring`, at 30 fps)

| Name | Config | Feel |
|---|---|---|
| `pop` (default UI) | damping 14, stiffness 140, mass 0.8 | quick, tiny overshoot: bubbles, chips, nodes |
| `firm` | damping 20, stiffness 170, mass 0.9 | no visible overshoot: cards, panels |
| `heavy` | damping 22, stiffness 90, mass 1.1 | Liquid Glass, large objects |
| `bouncy` | damping 9, stiffness 160, mass 0.7 | only for a single playful accent (an emoji, a like). Never for text |

## Durations (frames at 30 fps)

| Movement | Frames | Seconds |
|---|---|---|
| Micro (tick, highlight, colour change) | 6–9 | 0.2–0.3 |
| Small element entrance (chip, word, icon) | 10–14 | 0.33–0.47 |
| Card / panel entrance | 14–20 | 0.47–0.67 |
| Exit | about 70% of the entrance | |
| Camera move between areas | 24–40 | 0.8–1.3 |
| Scene transition | 12–24 (Kinetic: 6–10; Glass: 24–36) | |
| Stagger between siblings | 2–4 (lists, cards); 1–2 (letters); 4–6 (lines of text) | |
| Count-up of a number | 18–30 | |
| Typewriter | 30–45 chars/s | |

**Reading time** for on-screen text that is *not* spoken at the same moment is 0.6 s + 0.25 s per word, minimum. A 6-word label needs 2.1 s on screen.

## Entrance catalogue (pick 2–3 per video)

- **Blur-rise:** opacity 0 → 1, translateY 24 → 0, blur 8 → 0 px. The house default (Midnight Glow).
- **Mask reveal:** text slides up from behind a clipping line (`overflow: hidden` on a line wrapper). Editorial and Kinetic.
- **Scale-in:** 0.94 → 1 + opacity. Cards and Bento.
- **Draw-on:** SVG `strokeDashoffset` for lines, edges, underlines, circles, chart axes. Sketch and Paper.
- **Typewriter:** text grows by characters, with a cursor. Terminal and chat bubbles.
- **Pop:** spring scale 0 → 1 with `pop` preset. Chips, badges, notification bubbles.
- **Count-up:** numbers ease from 0 (or from the "before" value) to the target.
- **Word-by-word:** per-word stagger of blur-rise or mask. Short headlines only (7 words or fewer).

Exits: fade + small move in the direction of travel (or blur-out), at 70% of the entrance time. Many elements don't need an exit: the camera moves away or the scene cuts.

## Transitions catalogue

| Transition | When |
|---|---|
| **Camera travel** (pan/zoom across one big canvas) | Same "world" (a workflow canvas, a dashboard). Best and smoothest |
| **Zoom-through** (scale an element up until it fills the frame, then it *is* the next scene) | Diving into detail (a node opens into its settings, a card into its story) |
| **Match cut** | Shape or position continuity between scenes |
| **Mask wipe** (a shape or line sweeps across) | Section changes in Paper and Bento |
| **Push** (old slides out as new slides in, same direction) | Lists of steps, tutorials |
| **Hard cut on a downbeat** | Kinetic Type, music-led edits, hook → body |
| **Whip / motion-blur pan** | Energy moments only, 1–2 per video. Use `@remotion/motion-blur` `<CameraMotionBlur>` sparingly (it is slow to render) |
| **Fade through black** | Almost never; only the end card |

Put scene changes on a **music downbeat** when it's close (within about 4 frames). See sync.md.

## Camera

Treat the composition as a camera over a larger world. Store `{x, y, zoom}` keyframes keyed to cues and interpolate with `inOut`. Add a 1–2% slow push during long explanations. Shake only for a single impact in Kinetic Type (2–4 px, 4–6 frames, decaying). Depth: layers move at different rates (parallax 0.3 / 0.6 / 1.0).

## Text in motion

- Animate **lines or words**, not letters, for anything longer than about 3 words.
- Never rotate body text. Never use 3D flips for text.
- Big headline on screen: hold it still for at least the reading time once it has landed.
- Numbers: tabular numerals, counting up, units appearing after the number lands.
- Highlights: an accent sweep behind a word (highlighter) or colour change, timed to the spoken word.

## Things that make it look cheap (avoid)

- Bounce or elastic on everything; spinning or flying text; default "zoom in" on every element.
- More than one accent colour fighting for attention; rainbow gradients; neon everywhere.
- Every word of a sentence animating in a different way.
- Transitions from template packs (star wipes, glitch on everything, light leaks on every cut).
- Elements that move but mean nothing; constant shake; dead frames over 2 s.
- Captions covering the UI being explained.
- Motion that ignores the voice (a reveal 1 s after the word it illustrates).
- Flashing faster than 3 times a second (also a photosensitivity risk).

## Remotion specifics

- Everything derives from `useCurrentFrame()`. No CSS transitions, no `Math.random()` (use `random(seed)` from `remotion`), no time-based JS.
- Use `<Sequence>` / `<Series>` for scenes and `premountFor` on heavy ones. `<Img>`, `<OffthreadVideo>` and `<Audio>` come from `remotion`.
- Fonts: `loadFont()` from `@remotion/google-fonts/<Name>`, loading only the needed weights and subsets.
- Motion blur for fast moves: `@remotion/motion-blur`. Paths and morphs: `@remotion/paths`. Shapes: `@remotion/shapes`. Transitions: `@remotion/transitions` (`TransitionSeries` with `fade`, `slide`, `wipe`, or custom presentations).
- Render stills often (`pnpm stills <Comp> <frames…>`) and look at them. It's faster than rendering the whole video.
- If the official Remotion agent skills are installed in the studio (`.claude/skills/remotion-best-practices`), follow them for API details.
