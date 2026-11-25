# eravue-motion log

One line per finished video, plus lessons. Newest first. Record what was made, the look, the format, the result (views, sends, ad CTR/CPM if known) and what you'd change. Read this before planning the next video, and lean toward what worked.

## Videos

| Date | Slug | Type | Look | Formats | Where | Result | Notes |
|---|---|---|---|---|---|---|---|
| 2026-11-21 | lwc-3 | footage edit (calculator) | Editorial Paper | 9:16 | @lifewithcofounders (not posted) | n/a | "Open your calculator": CalcTape (50 + 20 = 70 leads, x 5), week/month/year loss cards, ~1,000 x ₹2,000 = ~₹20 lakh tape with a WORST CASE stamp, struck-out "reply / pick up", Part 2 + follow button. He says "~1,000 clients a year" (5 a week is ~260): flagged to the founders. Music tense, drop on "70 leads" |
| 2026-11-21 | lwc-4 | footage edit (replica) | Editorial Paper | 9:16 | @lifewithcofounders (not posted) | n/a | You vs the exact replica (VersusCards, 2 AM DM, the replica wins), "That's my job", moon + Zzz, Checklist of repetitive tasks, FlowStack + DocCards + <1m ring, CRM LedgerTable labelled DEMO, wake-up sun, comment box. Music night |
| 2026-11-21 | lwc-5 | footage edit (website chatbots) | Editorial Paper | 9:16 | @lifewithcofounders (not posted) | n/a | BrowserCard closing on "close the tab", a bad bot chat (menu chips, link, email grab), "A good AI is brilliant", 3-item Checklist ticking on cue, comment box. Music warm |
| 2026-11-21 | lwc-6 | footage edit (automation tier list) | Editorial Paper | 9:16 | @lifewithcofounders (not posted) | n/a | TierBoard S/A/B/C/F with chips dropping on "tier", "can move up" badges, F-row spotlight, AI-vs-you split for complaints, comment box. "It's awkward chasing money" is a best guess (both models hear "quoted"). Music bright |
| 2026-11-20 | ten-dms-test | footage edit (talking head + paper graphics) | Editorial Paper | 9:16, 4:5 | @lifewithcofounders (not posted) | n/a | Sanchit's own 65 s cut "10 businesses, one DM at 11 PM". Face as a photo-print card that shrinks to a bubble; a 10-tile reply tracker (row to grid match cut) with a live clock and 2 / 2 / 6 stat cards; stopwatch for the under-a-minute reply; n8n flow cards; phone with 9 chats; custom paper end card (comment AI). Original music (scripts/compose-paper.py, tempo bends per section so each section start lands on a story cue) + new SFX (key, ping, stamp, tock, lift) |
| 2026-11-16 | ig-instant-reply | demo | Midnight Glow | 9:16 | @eravuedotcom (not posted) | n/a | n8n Instagram DM auto-reply; scratch TTS voice (David, rate 3) awaiting Sanchit's take; showreel bed trimmed 2.27 s so drop hits "So we built this"; IG DM skin + RollText components added. Also a pencil-on-paper version (Sketch look, deep-orange accent, roughjs Rough/SketchFlow components) as IgInstantReplySketch-V |
| 2026-11 | demo-1-whatsapp-receptionist | demo | Midnight Glow | 16:9 | Upwork | n/a | Remotion; VO cut in Premiere; SRT captions; Pixabay "Creative Technology Showreel" (75 BPM) re-arranged so drops hit the canvas reveal |
| 2026-11 | demo-2-missed-call-text-back | demo | Midnight Glow | 16:9 | Upwork | n/a | same pipeline |
| 2026-11 | demo-3-lead-capture-follow-ups | demo | Premiere edit | 16:9 | Upwork | n/a | picture from Premiere, audio finished with finish-video.mjs |

## Lessons

- 2026-11-21: lwc-3..6 added six kit boards (editorial/Boards.tsx: CalcTape, TierBoard, Checklist, VersusCards, LedgerTable, BrowserCard; EditorialKit-V pages 7-8). Gotchas:
  - `pnpm vo:align <slug>` alone looks for a scratch.tsv; for a real voice pass the words: `node scripts/align.mjs <slug> vo/<slug>/words.json`.
  - align.mjs matches by nearest word, so changing the word count (whisper "tls" -> script "tier list") made every later beat drift by seconds. Check timing.json after any such fix; a Levenshtein (DP) alignment fixed it.
  - `cue(beat, "s")` prefix-matches ("s" -> "same", "a" -> "asking"): key single letters to a neighbouring word ("tier") and keep them out of caption ACCENTS.
  - Whisper hallucinated "To be continued..." at the very end of lwc-3 (three words on one timestamp); drop words like that.
  - Both models agreed 100% on all four takes and still wrote "tls" and "it's quoted": agreement is not proof. Re-decode unclear spans with large-v3 and an initial_prompt of the topic words (ReelStudio's faster-whisper needs the audio passed as a numpy array; its av version breaks file decoding).
  - Cards that pop over the top area must start after the ClipFrame move ends (key + about 10 frames), or they collide with the polaroid mid-move.

- 2026-11-20: Merged everything into one kit (KIT.md in the studio). The pieces:
  - `pnpm new` scaffolds a video, `pnpm ship` delivers it;
  - `pnpm voice:profile` uses ReelStudio's voice profiles;
  - `pnpm compose` fits original music to story moments (it reproduced lwc-2's hand plan exactly);
  - captions and transitions are props backed by ReelStudio's engines.

  New videos should only need new animations. Anything reusable goes into the kit, never only into a video folder. Shared assets must not be regenerated destructively: another session's `pnpm sfx` once rewrote every sound, so it now only fills missing ones.

- 2026-11-20: Remotion copies public/ into the OS temp folder on every bundle (256 MB) and on every still/render call, so a 99 MB working video in public/ filled the C: drive (7 MB free) after a few stills runs. Shrink the working video (crf 20, about 45 MB), set TEMP/TMP to a folder on E: before running Remotion (E:/video-edits/eravue-motion/env.sh), render all stills in one stills.mjs call per composition, and delete stale remotion-* folders in %TEMP% if it happens.
- 2026-11-20: For music that must hit story moments exactly, do not fit the story to a fixed-tempo track: compose-paper.py takes sections with their real start/end seconds and a beat count, so tempo bends 92-108 BPM and every section start is on a cue. Place SFX for the exact word hits.

- 2026-11-18: The first batch of 10 VO scripts was rejected as flat. Seven of them used the same container (pain → "so we built this" → 3 steps → DM us), and they were feature demos, not ideas a stranger stops for. Rewritten as 10 different formats (viewer challenge, calculator, quiz, tier list, experiment, rewind story, 5-second test, result → build, take, ad). Write with references/attention.md, and never ship a batch where formats repeat.

- 2026-11-16: Text measured on the first render uses the fallback font, because Google fonts load asynchronously and only join `document.fonts` once they arrive. `@remotion/layout-utils`' `measureText` caches that wrong width, and Remotion waits for the fonts without re-rendering, so marks came out short and kinetic words overflowed. Use `textBox` + `useFontsReady` from `lib/measure` (looks register fonts with `trackFont`). Also, the Google `latin` subset has no ₹; looks now load `latin-ext` too.
- 2026-11-16: In bash, never put markdown with backticks inside a double-quoted `node -e "..."` string: the backticks run as commands (one created a stray file). Write the text with the Write tool and splice it from a file.
- 2026-11-16: `Config.setPixelFormat("yuv420p")` in remotion.config.ts did NOT stop a yuvj420p output with JPEG frames, and neither did `--pixel-format yuv420p` on the CLI (4.0.543). Convert after rendering: `ffmpeg -i in.mp4 -vf "scale=in_range=full:out_range=tv,format=yuv420p" -c:v libx264 -crf 17 -c:a copy`.
- 2026-11-16: Windows SAPI scratch TTS fires one word event per sub-sound of "11:48 PM" / "n8n"; align.mjs now drops consecutive duplicates. Phone mockups below about 1.0 scale are unreadable in 9:16, so show the key chat as a big standalone bubble card instead.
- Sanchit's raw takes (phone, 2026-11) measure about -21 LUFS with a clean noise floor (about -69 dBFS) but a dark, bottom-heavy tone: +8 dB at 125–160 Hz and -8 dB of air against the male target. The measured chain cuts about 3 dB at 140 Hz and about 1.3 dB at 250 Hz, and adds about 1.5 dB at 3.5 kHz plus a 3 dB air shelf. The founders liked the earlier hand-tuned version (-3 dB at 250 Hz, +3 dB at 3.5 kHz, +2.5 dB shelf), which moved the same way.
- The beat finder reproduces the hand-made map of the Pixabay showreel track (75 BPM, drops at beats 16 and 80, breakdown at 64, outro at 128). Its grid puts the first beat at 0.23 s, where the drop's hit really is. The earlier hand value of 0.37 s landed the drop about 0.15 s late.
- Remotion's default output is `yuvj420p`. Render with `--pixel-format yuv420p` for uploads.
