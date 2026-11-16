# Syncing animation to the voice and the music

Two clocks drive every video: **the words** (primary) and **the beat** (secondary). Nothing is placed at a hard-coded frame number. That's what lets a new take, a tightened pause or a different track re-time the whole video for free.

## The timing file

Every video has `src/videos/<slug>/timing.json` (in the demos repo it's `src/timing/<id>.json`):

```json
{ "id": "demo1", "audio": "vo/demo1.wav", "duration": 82.333,
  "beats": [ { "id": "i1", "start": 0,
               "words": [ { "w": "this", "t": 0 }, { "w": "whatsapp", "t": 0.626 }, ... ] }, ... ] }
```

Words are normalised (lowercase, letters and digits only). Beats come from `script.json` (`{ id, text }` per beat). `align.mjs` matches the transcript's words to the script's beats in order. A slightly reworded sentence moves to the nearest match.

## Getting word timings (pick by source)

| Source | How | Accuracy |
|---|---|---|
| **Single take (+ script)** | `pnpm vo:sync <slug> [audio]`: transcribes locally with **Subtitle Edit's Faster-Whisper-XXL** (`D:\Subtitle Edit\SpeechToText\Purfview-Faster-Whisper-XXL`, medium.en, already installed, about 3.7× real time), writes `vo/<slug>/words.json` and timing.json. Nothing is downloaded. Fallback only if Subtitle Edit is gone: `--engine whispercpp` (downloads about 150 MB once) | about 50 ms per word |
| **Recording-first, no script** | `pnpm vo:sync <slug> <audio>` writes `script.json` with one beat per sentence from the transcript. Fix spelling and beat ids, remove retakes (repeated sentences show up as duplicate beats), then `pnpm vo:align <slug> vo/<slug>/words.json` | about 50 ms |
| **Recording + transcript from the user** | Put their text in `script.json` (their transcript wins for spelling and beats; one beat per sentence if they gave no split), then `pnpm vo:sync` for the times | about 50 ms |
| **Premiere edit + SRT** | Put the SRT at `vo/<slug>/captions.srt` and the caption→beat map at `vo/<slug>/srt-beats.json`, then `pnpm vo:srt <slug>`. Words are spread inside each caption by word length | about 200 ms (fine for soft effects; use vo:sync for tight sync) |
| **ElevenLabs voice** | Use the character alignment it returns (convert to word starts) | exact |
| **Scratch TTS** (timing placeholder before recording) | `pnpm vo:scratch` + `pnpm vo:align`. Never published | exact for the scratch |

medium.en is the installed model, and it's good on names. Don't pass another `--model` unless the user agrees, because Faster-Whisper-XXL would download it. Always fix spelling from the script, never trust whisper for "n8n", "Claude" or client names.

If the voice was tightened (`voice.mjs --tighten`) or re-edited, re-run the timing step. Timings belong to one exact audio file.

## Cues in scenes

```ts
const { cue, end } = makeCues(timing);       // src/lib/timing.ts
cue("b4")                 // frame where beat b4 starts
cue("b4", "calendar")     // frame where "calendar" is spoken in b4 (first match)
cue("b4", "the", 2)       // third "the" in b4
cue("b4", undefined, 0, -0.1)  // 0.1 s before b4 starts
```

Rules:
- Entrances start **2–4 frames before** the word (`cue(...) - 3`), so the arrival lands on it.
- A visual that *illustrates* a word appears on that word; one that *answers* a question appears after the question ends.
- Scene boundaries usually sit at a beat start, minus about 6 frames for the transition.
- Exits are keyed to the next beat (or the next scene's cue), never to "start + N seconds".
- `cue()` throws if a word isn't found. That's deliberate, so a changed script breaks loudly instead of silently mis-timing. Fix the cue word.

## Snapping to the music

Load the bed's beat grid (from `beats.mjs --json` plus the arrangement in `beds.json`, mapped to video time) and snap *non-voice* events, such as scene changes, camera moves and Kinetic Type slams:

```ts
// beats: video-time seconds of each beat in the arranged bed; downbeats: every 4th
export const snapToBeat = (frame: number, beatsSec: number[], fps: number, maxShift = 4) => {
  let best = frame;
  for (const b of beatsSec) {
    const f = Math.round(b * fps);
    if (Math.abs(f - frame) <= maxShift && Math.abs(f - frame) < Math.abs(best - frame)) best = f;
  }
  return best;
};
```

- Snap only within ±4 frames (±0.13 s). Further than that, the voice sync suffers. Rearrange the music instead.
- Never snap word-illustrating entrances away from their word by more than 2 frames.
- Kinetic Type (music-led): the beat is primary. Words land on beats, and the VO (if any) is placed to match.

## When things change

| Change | Re-run |
|---|---|
| New or edited voice take | voice.mjs process → timing (vo:sync / align) → captions → music-bed (length and ducking depend on the voice) → stills check |
| Script wording changed | edit script.json → re-record or scratch → timing → fix any `cue()` that throws |
| Different music | beats.mjs → beds.json segments → music-bed |
| New format (9:16 from 16:9) | nothing in timing; layout only |

## Sync QA

Spot-check 5 moments (hook, reveal, a number, the result, the CTA) by rendering stills at `cue - 2` and `cue + 6`, and watch the full render once with sound. If a reveal feels late, it's usually the entrance starting *on* the word instead of 2–4 frames before.
