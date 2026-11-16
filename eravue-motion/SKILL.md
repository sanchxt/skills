---
name: eravue-motion
description: Make Eravue's motion-graphics videos end to end - automation/product demos, AI and tech news explainers, case studies, tutorials and service ads - for @eravuedotcom, @lifewithcofounders, Meta ads, YouTube, LinkedIn and Upwork. Covers the brief, script and storyboard, seven visual "looks" (Midnight Glow, Editorial Paper, Kinetic Type, Liquid Glass, Terminal, Bento, Sketch), typography and colour, motion rules, captions, analysing and cleaning Sanchit's voiceover (measured EQ, de-ess, compression, loudness), AI voices, background music chosen, cut to the beat and ducked, syncing animation to words and beats, 9:16/4:5/16:9 versions, QA and the final loudness master. Built on Remotion (React video) in D:\projects\eravue-motion. Use for "/eravue-motion", "make a motion graphics video", "turn this into a reel/ad", "clean up my voiceover", "add music/captions", "make a vertical version", or any new Eravue explainer or demo video.
---

# Eravue motion

Motion-graphics videos for Eravue (Sanchit and Sanchita's AI, automation, web and app agency). The goal is videos that look *expensive and calm*: one clear idea at a time, everything keyed to the voice, music that moves with the story. They should make a business owner think "these people are ahead, I want that". They get posted organically and run as ads.

The gold standard so far is the three Upwork demos in `D:\projects\eravue-automations\videos` (Remotion, the Midnight Glow look). Their stills are in `out/stills/`, and the finished files are in `E:\video-edits\LifeWithCofounders\upwork-demos\`. Look at a few stills before you design anything, and match or beat that bar.

## Where things live

| What | Where |
|---|---|
| Studio (Remotion project, one folder per video) | `D:\projects\eravue-motion` (set up 2026-11-16). Layout, commands, and every reusable component already built (kit sheets SketchKit-V and UiKit-V): [references/studio-setup.md](references/studio-setup.md) |
| Raw recordings, music masters, big media | `E:\video-edits\eravue-motion\<slug>\` (never in git) |
| This skill's tools (no npm deps, need full ffmpeg on PATH) | `scripts/voice.mjs`, `scripts/beats.mjs`, `scripts/master.mjs` (copied into the studio's `scripts/`) |
| What worked / didn't | [log.md](log.md). Read it before planning, add to it after each video |

## The workflow

A new video can start from **a script** (Claude drafts, Sanchit records to it) or from **a recording** (Sanchit records freely and hands over the audio, plus a transcript if he has one). Ask which if it isn't obvious. Both paths meet at step 4.

1. **Brief.** Settle these. Ask only for what you can't infer, and use the defaults below for the rest:
   - video type (demo, news, case study, tutorial, offer ad);
   - account and platforms, which set the formats;
   - look;
   - length;
   - voice: Sanchit, an AI voice, or none;
   - caption style;
   - CTA;
   - what's real: which client, numbers and screens exist. Never invent them.
2. **Script and story.** Use the structure for the video type in [references/story.md](references/story.md). Write the spoken words with the `short-form-craft` skill (hooks, retention, human voice), and use `lifewithcofounders` when it's for that account. Split the script into **beats**: one sentence or idea each, with ids like `h1`, `p1`, `r1`. Save it as `vo/<slug>/script.json`.
3. **Storyboard.** Make a table with one row per beat: words → what's on screen → the hero motion → caption/text → music moment (intro, build, drop, breakdown, outro) → SFX. Show it to the user and get an OK before building. It's the cheapest place to change things.
4. **Voice.** For a recording, run `node scripts/voice.mjs analyze <raw>`, then `process`, and have the user listen to the A/B file before going further. For an AI voice, or to coach a re-record, see [references/voice.md](references/voice.md). Never publish the robotic scratch TTS.
5. **Timing.** Get word-level timestamps: `pnpm vo:sync` (Subtitle Edit's Faster-Whisper-XXL, already installed, nothing downloaded), Premiere SRT, the user's transcript, or ElevenLabs alignment. Build `timing.json` from them. Every animation is keyed to `cue(beat, word)`, never to hard-coded frames, so a new take re-times the whole video. See [references/sync.md](references/sync.md).
6. **Music.** Pick a track for the look and pace, and log its license. Run `node scripts/beats.mjs <track>` to get the BPM, the grid and where the drops fall. Arrange it so the drop lands on the reveal and the outro under the CTA, then build the ducked bed. See [references/music-sfx.md](references/music-sfx.md).
7. **Build.** Write the Remotion scenes using the look's tokens ([references/looks.md](references/looks.md)), the motion rules ([references/motion.md](references/motion.md)) and the type/colour rules ([references/type-color.md](references/type-color.md)). Make one composition per format, sharing scenes through a layout prop. *Re-compose* each format, never crop: [references/formats.md](references/formats.md).
8. **Captions.** Use the style the brief picked from [references/captions.md](references/captions.md). The default is chunks with accent words for vertical, and the minimal dim-to-bright line for 16:9.
9. **QA and master.** Go through [references/qa.md](references/qa.md): contact-sheet stills, safe-zone overlay, a phone-size read, sync spot-checks, the facts, the license. Then run `node scripts/master.mjs out/<file>.mp4` to reach -14 LUFS / -1 dBTP with the specs checked. Show the user stills and the file before calling it done.
10. **Deliver.** Hand over the files (`<slug>-<format>-v<N>.mp4`), a cover frame, the post caption, and for ads 2–3 hook variants. Posting goes through `eravue-social` (organic) or `cmo` (ads), and only after the founders approve. Add a line to [log.md](log.md).

## Defaults (when the brief doesn't say)

| Thing | Default |
|---|---|
| Format | 9:16 1080×1920 master; add 4:5 1080×1350 for ads and 16:9 1920×1080 for YouTube/LinkedIn/Upwork |
| Length | Reels 30–45 s; ads 15–30 s; long walkthroughs 60–150 s |
| Look | Midnight Glow for demos and automation; Editorial Paper for news and opinion; Kinetic Type for ads and hooks; Bento for offers and results; Terminal for tutorials; Sketch for teardowns and before/after; Liquid Glass for premium launches |
| Fonts | The look's pair (max 2 families + 1 mono) |
| Accent | Eravue orange `#fca311` unless the look says otherwise. One accent per frame |
| Frame rate | 30 fps (60 only for heavy kinetic type) |
| Voice | Sanchit, male target curve, stem at -16 LUFS |
| Music | Instrumental, about 18–24 dB under the voice, ducked, drop on the reveal |
| Captions | Vertical: chunk + accent words. 16:9: minimal line, dim-to-bright |
| Final audio | -14 LUFS integrated, -1 dBTP |
| Export | H.264, yuv420p, CRF 16–18, AAC 320 kbps 48 kHz, `+faststart` |

## Hard rules

- **True or it doesn't ship.** Demos are labelled as demos. Never imply a workflow runs on a service it doesn't really run on. No invented clients, numbers, testimonials or results: leave `[REAL: ...]` slots and ask. News facts are verified with a search, and the source and date go in the notes. Shown on screen too when it's a claim.
- **Music must be licensed for the use.** Log every track in `music/LICENSES.md` (source, license, date, whether it's OK for organic and for ads). If a free license doesn't clearly cover paid ads, don't use the track in an ad. Use a cleared one or add music in Meta's Sound Collection at upload.
- **Vertical is rebuilt, not cropped.** Every format gets its own layout inside the safe zones.
- **No logo in the first 3 seconds of ads or Reels.** The brand appears at the end card, or as a small watermark after the hook.
- **Motion serves the words.** One hero movement per beat, nothing moving that doesn't mean something, nothing flashing more than 3 times a second.
- **Nothing gets posted, sent or paid for without a clear yes from the founders.**
- **Keep the voice his voice.** Processing corrects problems in small, capped moves. If a take needs more than that, say so and suggest a re-record with the recording guide.

## Reference index

- [references/story.md](references/story.md): structures per video type, hooks, CTAs, storyboard format, ad variants
- [references/looks.md](references/looks.md): the seven looks, each with palette tokens, fonts, texture, motion, captions, music and use cases
- [references/motion.md](references/motion.md): easing and spring presets, durations, staggers, entrances, transitions, camera, what to avoid
- [references/type-color.md](references/type-color.md): sizes per format, pairing, tracking, contrast, colour roles
- [references/captions.md](references/captions.md): seven caption styles with specs, chunking and emphasis rules
- [references/voice.md](references/voice.md): what a good voiceover sounds like, recording on phone or USB mic, reading the analysis, the processing chain, AI voices
- [references/music-sfx.md](references/music-sfx.md): choosing and licensing music, beat maps, arranging, ducking, SFX
- [references/sync.md](references/sync.md): word timings from any source, cues, beat snapping, re-timing
- [references/formats.md](references/formats.md): platform specs, safe zones, per-format layouts, export, covers, which account gets what
- [references/qa.md](references/qa.md): the pre-ship checklist and the aesthetic critique
- [references/studio-setup.md](references/studio-setup.md): creating and running the studio repo
