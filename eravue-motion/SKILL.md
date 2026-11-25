---
name: eravue-motion
description: Make Eravue's motion-graphics videos end to end - automation/product demos, AI and tech news explainers, case studies, tutorials and service ads - for @eravuedotcom, @lifewithcofounders, Meta ads, YouTube, LinkedIn and Upwork. Covers the brief, script and storyboard, seven visual "looks" (Midnight Glow, Editorial Paper, Kinetic Type, Liquid Glass, Terminal, Bento, Sketch), typography and colour, motion rules, captions, analysing and cleaning Sanchit's voiceover (measured EQ, de-ess, compression, loudness), AI voices, background music chosen, cut to the beat and ducked, syncing animation to words and beats, 9:16/4:5/16:9 versions, QA and the final loudness master. Built on Remotion (React video) in D:\projects\eravue-motion. Use for "/eravue-motion", "make a motion graphics video", "turn this into a reel/ad", "clean up my voiceover", "add music/captions", "make a vertical version", or any new Eravue explainer or demo video.
---

# Eravue motion

> **Storage: Eravue HQ (live from 2026-11-25).** Eravue HQ (https://app.eravue.com) is the only record of leads, every message sent and received, drafts, Upwork jobs, clients, content, the proof library, tasks, notes, metrics and both founders' days. Use the `eravue-hq` MCP tools as described in `references/hq.md`. Wherever this skill mentions `leads.py`, `growth.py`, `.outreach/*.csv`, `.growth/*.csv`, the claude.ai Daily Board (ArtifactData `days`) or an approval list in a `.growth/daily/*.md` file, do the HQ equivalent from the tool map in `references/hq.md` instead. Those files are frozen (renamed `*.frozen-2026-11-25.csv`) and must not be written. Approval happens in the HQ Outbox: queue messages with `draft_create` and send only drafts a founder approved (`drafts_list status=APPROVED`), then call `draft_mark_sent`. If the `eravue-hq` tools aren't connected, stop and ask the founder to connect them (HQ → Settings → Agents). Everything else in this skill (voice, quotas, research and safety rules) still applies.
>
> For motion: each video is a Studio item (`content_upsert`, format MOTION or DEMO_VIDEO, `slug`, `localPath` of the final render, `driveUrl` once uploaded, stage as it moves). Demos meant for outreach also go in the library (`asset_add` type DEMO_VIDEO with niches and services). Keep `log.md` for lessons only.

Motion-graphics videos for Eravue (Sanchit and Sanchita's AI, automation, web and app agency). The goal is videos that look *expensive and calm*: one clear idea at a time, everything keyed to the voice, music that moves with the story. They should make a business owner think "these people are ahead, I want that". They get posted organically and run as ads.

The gold standard so far is the three Upwork demos in `D:\projects\eravue-automations\videos` (Remotion, the Midnight Glow look). Their stills are in `out/stills/`, and the finished files are in `E:\video-edits\LifeWithCofounders\upwork-demos\`. Look at a few stills before you design anything, and match or beat that bar.

## Where things live

| What | Where |
|---|---|
| Studio (Remotion project, one folder per video) | `D:\projects\eravue-motion`. **Its `KIT.md` is the catalog of everything already built** (components, 46 caption styles, 39 transitions, sounds, voice profiles, looks, commands). Read it first, every time. Setup notes: [references/studio-setup.md](references/studio-setup.md) |
| Raw recordings, music masters, finished files | `E:ideo-edits\eravue-motion\<slug>\` (never in git) |
| Pipeline commands (in the studio) | `pnpm new` · `pnpm voice:profile` · `pnpm compose` · `pnpm stills` · `pnpm ship`; older single-step tools (`voice`, `vo:sync`, `beats`, `music`, `master`) still work. Copies of the scripts are in this skill's `scripts/` as a backup only; the studio's are the live ones |
| ReelStudio (`D:\projects\SOCIAL MEDIA\short-form-quick-edits`) | Source of the caption + transition engines, fonts and the voice chain/profiles. Vendored with `pnpm sync:reel`; never edit `src/vendor/` |
| What worked / didn't | [log.md](log.md). Read it before planning, add to it after each video |

## The workflow

**Don't rebuild what exists.** The studio already does setup, voice, timing, captions, transitions, music, SFX, formats, mastering and delivery. Each one is a command or a prop. The work in a new video is the story, the storyboard, and only the animations the kit doesn't have yet. Before anything else, read `D:\projects\eravue-motion\KIT.md` and [log.md](log.md). Don't re-explore the repo or re-read every reference: open a reference only when its step needs it.

A video starts from **a recording or clip** (most common), or from **a script** that Sanchit records to. Ask which if it isn't obvious.

1. **Brief.** Settle these. Ask only for what you can't infer, and use the defaults below for the rest:
   - video type;
   - account and platforms, which set the formats and the end-card handle;
   - look;
   - length;
   - voice profile;
   - caption style;
   - CTA;
   - what's real. Never invent clients, numbers or results.
2. **Start it:** `pnpm new <slug> <clip|voice> --look <id> --voice <profile|keep> --handle @<account> [--formats v,f]`. This one command:
   - copies the media and cleans the voice with a ReelStudio profile;
   - word-times it;
   - runs a second-model cross-check into `vo/<slug>/check.md`;
   - scaffolds `src/videos/<slug>/<Name>.tsx` + `cues.ts` with ClipFrame, Captions, LookBg, EndCard, music, SFX and SafeZone wired, and registers `<Name>-V/-F`;
   - writes the music plan.

   Then read `check.md`, fix spellings in `script.json`, and run `pnpm vo:align <slug>`. Ask the user about any word the two models disagree on that matters (names, numbers, tools).

   *Script-first:* write `script.json` with the beats ([references/story.md](references/story.md), [references/attention.md](references/attention.md), the `short-form-craft` skill), have him record, then `pnpm new`.
3. **Storyboard.** One row per beat: words → what's on screen (name the kit pieces) → ClipFrame framing → caption/text → music moment → SFX. Get the user's OK; it's the cheapest place to change things. Mark which visuals the kit lacks: those are the only new code.
4. **Cues.** In `cues.ts`, name each moment as `cue(beat, word)`. Never hard-code frames.
5. **Build.** Scenes go in `<Name>.tsx` from kit pieces plus the look's tokens ([references/looks.md](references/looks.md), [references/motion.md](references/motion.md), [references/type-color.md](references/type-color.md)).
   - **A missing piece that could be reused goes into the kit:** `src/components/<area>/`, exported from `index.ts`, shown on a kit sheet, then `pnpm kit:catalog`.
   - Extend shared pieces with new optional props; never change existing behaviour or regenerate shared assets.
   - Formats: re-compose with the `layout` prop, never crop ([references/formats.md](references/formats.md)).
6. **Captions and transitions** are one value each. Pick them from KIT.md, or look at the `CaptionSheet-V` / `TransitionSheet-V` compositions.
7. **Music.** Two options ([references/music-sfx.md](references/music-sfx.md)):
   - **Original (default, cleared for ads):** set the story moments (drop, lift, breakdown, back, outro) and the mood in `music/compositions/<slug>.plan.json`, then run `pnpm compose <slug>`. It fits the tempo so the drops land on those lines, registers the licence and builds the ducked bed.
   - **Licensed track:** `pnpm beats` → `music/beds.json` → `pnpm music <slug>`.

   SFX: `[frame, name, gain]` cues; `pnpm sfx` only fills missing sounds.
8. **QA.** Check `pnpm stills <Name>-V <frames> --safe` at every beat change and look at them yourself before any full render. Then go through [references/qa.md](references/qa.md): sync, facts, licence, safe zones, phone-size read.
9. **Ship.** `pnpm ship <slug>` renders every format, converts to yuv420p, masters to -14 LUFS / -1 dBTP, checks the specs, writes a contact sheet and copies `<slug>-<v|f|h>-vN-final.mp4` to `E:ideo-edits\eravue-motion\<slug>\`. Look at the contact sheet. Hand over the files, a cover frame, the post caption, and for ads 2–3 hook variants. Posting goes through `eravue-social` or `cmo`, only after the founders approve.
10. **Log.** Add a row and any lesson to [log.md](log.md). If you built a new kit piece, say so there.

## Defaults (when the brief doesn't say)

| Thing | Default |
|---|---|
| Format | 9:16 1080×1920 master; add 4:5 1080×1350 for ads and 16:9 1920×1080 for YouTube/LinkedIn/Upwork |
| Length | Reels 30–45 s; ads 15–30 s; long walkthroughs 60–150 s |
| Look | Midnight Glow for demos and automation; Editorial Paper for news and opinion; Kinetic Type for ads and hooks; Bento for offers and results; Terminal for tutorials; Sketch for teardowns and before/after; Liquid Glass for premium launches |
| Fonts | The look's pair (max 2 families + 1 mono) |
| Accent | Eravue orange `#fca311` unless the look says otherwise. One accent per frame |
| Frame rate | 30 fps (60 only for heavy kinetic type) |
| Voice | Sanchit; `--voice default` (measured clean-up), `keep` if it was already cleaned in ReelStudio; stem at -16 LUFS |
| Music | Original (`pnpm compose`, mood to fit), about 18–24 dB under the voice, ducked, drop on the reveal |
| Captions | Paper over footage: `paper-card`; paper over graphics: `editorial`; dark vertical: `chunk`; 16:9: `minimal`. Any of the 39 `reel:*` presets on request |
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

- [references/attention.md](references/attention.md): what the platforms reward, idea size, formats that hold attention, the first 1.5 s, re-hooks, midpoint, endings, length, hook testing, and the pre-storyboard checklist
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
- [references/studio-setup.md](references/studio-setup.md): how the studio is set up (temp on D:, ReelStudio vendoring, footage + original music). The kit itself is in the studio's KIT.md
