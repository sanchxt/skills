# Music and SFX

Music sets the pace and the feeling, and tells the viewer when something important happens (the drop). Under a voiceover it must stay *under*: felt, not listened to.

## Choosing a track

- **Instrumental only** under voice. Vocals fight the narration.
- **Mood by look** (looks.md), **tempo by pace**: talky explainers 75–100 BPM, ads and kinetic 105–128 BPM. A track at about half or double the speech's rhythm feels natural.
- **Arc:** a soft intro (under the hook), a build, a clear drop or lift (for the reveal), a quieter breakdown (under the explanation), a second lift (for the result), and an outro that can end cleanly (under the CTA). Tracks with a visible structure in a waveform are easiest to arrange.
- **Avoid** busy lead melodies in 1–4 kHz (the speech range), heavy sub-bass that eats phone speakers, and famous-sounding tracks (Content ID).
- Shortlist 2–3 tracks, run `beats.mjs` on each, and pick the one whose sections fit the storyboard with the fewest edits.

## Sources and licensing (free first)

| Source | Notes |
|---|---|
| **Pixabay Music** (current choice) | Pixabay Content License: free for commercial use, credit optional. Save the download page URL. Some tracks are registered with Content ID by their authors, which can cause claims on YouTube. Keep the license page and download proof. Before using a track in **paid ads**, re-read the license page for that use |
| **Meta Sound Collection** (in Instagram / Facebook) | The only library business accounts can use in-app. Meta says it's cleared for commercial use, including ads on Meta. Add music at upload instead of baking it in when unsure |
| **YouTube Audio Library** | Fine for YouTube. Terms outside YouTube are less clear, so don't use it for Meta ads |
| **Free Music Archive / ccMixter** | Only CC-BY or CC0 tracks (no NC = non-commercial, no ND if you re-arrange). Credit as required |
| Paid later (Epidemic, Artlist, Soundstripe) | Cleared for ads; consider once ads scale |

**Every track goes in the studio's `music/LICENSES.md`:**

```
| track | artist | source URL | license | downloaded | organic OK | ads OK | credit text |
```

If "ads OK" isn't a clear yes, the track is organic-only. Music files live outside the repo (`E:\video-edits\eravue-motion\music\`), and generated beds in `public/` are git-ignored.

## Beat map: `node scripts/beats.mjs <track> [--json beats.json] [--bpm N]`

It prints BPM, the first beat, the beat and bar length, and a bar-by-bar energy table with **DROP**, **BREAKDOWN** and **OUTRO** markers, plus where each build starts. Tested on the Pixabay showreel track: 74.99 BPM, with drops at beats 16 and 80, a breakdown at 64 and the outro at 128, matching the hand-made map.

- If the BPM is half or double what you feel, re-run with `--bpm` (the phase is still detected).
- Confirm the drop by ear. If it feels early or late, nudge `firstBeat` by ±0.05–0.1 s.

## Original music (default): `pnpm compose <slug>`

Eravue owns the result (it is synthesised, with no samples), so it is cleared for ads too. Run `pnpm compose <slug> --init` (or let `pnpm new` do it), then edit `music/compositions/<slug>.plan.json`:
- **moments:** `drop` (required: drums in), `lift` (the arp joins: build or reveal), `breakdown` (drums out: the reflective line), `back`, `outro` (under the CTA), `final` (the last chord). Each one is a beat id, `beat:word`, or seconds.
- **mood:** `night` / `warm` / `bright` / `tense`.
- **why:** what each moment lands on.

`pnpm compose <slug>` then:
- searches 72–96 BPM and the offset so bar lines land on those moments (the drop exactly; it warns if another moment is more than 0.25 s off);
- writes the arrangement to `music/compositions/<slug>.json` and renders it with `compose-lofi.py` to `E:/video-edits/eravue-motion/music/<slug>-original.wav`;
- registers the track in `beds.json` and `LICENSES.md`, and builds the ducked `public/<slug>/bed.wav`.

A hand-written `<slug>.json` with no plan is rendered as it is. `"engine": "paper"` (marimba with a tempo per section, absolute times) goes through `compose-paper.py`. Use a licensed track (below) only when the brief needs a specific sound.

## Arranging to the story (`music/beds.json` + `scripts/music-bed.mjs`)

The track is cut into whole-beat segments `[fromBeat, toBeat)` and joined with 50 ms crossfades that land exactly on beats, so edits are inaudible:

```json
"demo1": {
  "trimStart": 0,
  "segments": [[null, 60], [56, 96], [128, null]],
  "why": "drop on the canvas reveal (13.2 s), breakdown under Follow-ups (54.8 s), second drop on 'Answer, qualify, book' (67.6 s), outro as the voice ends"
}
```

How to plan it:
1. From the storyboard, list the story moments with their times from `timing.json`: the reveal, the explanation start, the result line, the CTA.
2. From the beat map, list the music moments: drop 1, breakdown, drop 2, outro.
3. Choose segments so each music moment lands on its story moment, within half a beat. Loop intro bars to lengthen a hook, skip bars to shorten a section, and always cut on bar lines (multiples of 4 beats from a section start) so phrasing stays musical.
4. Write a `why` line per bed. When the voice changes, re-check against it.
5. The script prints where each join lands. Compare it to the cue times.

Alternatively, shift the *video* timing slightly to the music (a scene change moved by ≤ 4 frames to a downbeat). See sync.md.

## Mix under the voice (what music-bed.mjs does)

- Level the music to **-27 LUFS** before ducking.
- **Voice dip:** a wide -6 dB cut at 2.5 kHz (w 1.5) in the music, so the words sit on top.
- **Sidechain ducking** keyed from the voice: threshold 0.03, ratio 4, attack 15 ms, release 500 ms, knee 4, RMS detection. Music comes up in pauses and dips under speech. That gives about 18–24 dB under the voice.
- Fade in 0.3 s, fade out 1.5 s, bed length = voice + 3 s tail (the end card).
- Busy or dense track, or a factual-heavy video: go quieter (-29 to -30). Sparse ambient track: -25 is fine.
- **Music-only versions** (sound-off ads, Kinetic Type): no ducking, the master goes straight to -14 LUFS.
- The final mix is mastered by `master.mjs` (-14 LUFS, -1 dBTP).

## Sync rules with music

- Big scene changes and reveals land on **downbeats** (bar starts) when within about 4 frames. Small accents (a chip pops, a number ticks) can sit on any beat.
- **Don't cut on every beat.** It's exhausting. Use downbeats for structure and beats for occasional accents. Kinetic Type is the exception (word slams on beats).
- Start a transition 2–4 frames *before* the beat, so the arrival lands on it.
- Risers lead into drops: put the reveal's build-up (camera pull-back, dimming) on the riser.
- End the video on a musical ending (the outro's last hit or a fade on a bar line), not mid-phrase.

## SFX

- Subtle, sparse, matched to the look (looks.md). One sound per *meaningful* event, never per element.
- Level: about 12–18 dB under the voice. You should notice them only if they're removed.
- Whooshes start 3–6 frames before the movement they accompany. Risers 1–2 bars before a drop.
- The demos repo generates clean UI sounds (`scripts/sfx.mjs`: pop, tick, ding, whoosh, sent, ring, thud) and places them via `src/components/Sfx.tsx`. Reuse it and add look-specific ones (key clicks, glass chimes) the same way. The studio's copy also makes the paper/pencil set: `pencil` (graphite scribble, under a drawing mark), `marker` (squeak, under a highlighter or marker stroke), `paper` (rustle, card or note entering), `tape` (rip, taped card landing) and `page` (page turn, under `PageTurnOut`). Keep them low; they're texture, not hits.
- Every SFX can be toggled off with `withSfx: false`.
