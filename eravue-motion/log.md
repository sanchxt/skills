# eravue-motion log

One line per finished video, plus lessons. Newest first. Record what was made, the look, the format, the result (views, sends, ad CTR/CPM if known) and what you'd change. Read this before planning the next video, and lean toward what worked.

## Videos

| Date | Slug | Type | Look | Formats | Where | Result | Notes |
|---|---|---|---|---|---|---|---|
| 2026-11-16 | ig-instant-reply | demo | Midnight Glow | 9:16 | @eravuedotcom (not posted) | n/a | n8n Instagram DM auto-reply; scratch TTS voice (David, rate 3) awaiting Sanchit's take; showreel bed trimmed 2.27 s so drop hits "So we built this"; IG DM skin + RollText components added. Also a pencil-on-paper version (Sketch look, deep-orange accent, roughjs Rough/SketchFlow components) as IgInstantReplySketch-V |
| 2026-11 | demo-1-whatsapp-receptionist | demo | Midnight Glow | 16:9 | Upwork | n/a | Remotion; VO cut in Premiere; SRT captions; Pixabay "Creative Technology Showreel" (75 BPM) re-arranged so drops hit the canvas reveal |
| 2026-11 | demo-2-missed-call-text-back | demo | Midnight Glow | 16:9 | Upwork | n/a | same pipeline |
| 2026-11 | demo-3-lead-capture-follow-ups | demo | Premiere edit | 16:9 | Upwork | n/a | picture from Premiere, audio finished with finish-video.mjs |

## Lessons

- 2026-11-16: Text measured on the first render uses the fallback font, because Google fonts load asynchronously and only join `document.fonts` once they arrive. `@remotion/layout-utils`' `measureText` caches that wrong width, and Remotion waits for the fonts without re-rendering, so marks came out short and kinetic words overflowed. Use `textBox` + `useFontsReady` from `lib/measure` (looks register fonts with `trackFont`). Also, the Google `latin` subset has no ₹; looks now load `latin-ext` too.
- 2026-11-16: In bash, never put markdown with backticks inside a double-quoted `node -e "..."` string: the backticks run as commands (one created a stray file). Write the text with the Write tool and splice it from a file.
- 2026-11-16: `Config.setPixelFormat("yuv420p")` in remotion.config.ts did NOT stop a yuvj420p output with JPEG frames, and neither did `--pixel-format yuv420p` on the CLI (4.0.543). Convert after rendering: `ffmpeg -i in.mp4 -vf "scale=in_range=full:out_range=tv,format=yuv420p" -c:v libx264 -crf 17 -c:a copy`.
- 2026-11-16: Windows SAPI scratch TTS fires one word event per sub-sound of "11:48 PM" / "n8n"; align.mjs now drops consecutive duplicates. Phone mockups below about 1.0 scale are unreadable in 9:16, so show the key chat as a big standalone bubble card instead.
- Sanchit's raw takes (phone, 2026-11) measure about -21 LUFS with a clean noise floor (about -69 dBFS) but a dark, bottom-heavy tone: +8 dB at 125–160 Hz and -8 dB of air against the male target. The measured chain cuts about 3 dB at 140 Hz and about 1.3 dB at 250 Hz, and adds about 1.5 dB at 3.5 kHz plus a 3 dB air shelf. The founders liked the earlier hand-tuned version (-3 dB at 250 Hz, +3 dB at 3.5 kHz, +2.5 dB shelf), which moved the same way.
- The beat finder reproduces the hand-made map of the Pixabay showreel track (75 BPM, drops at beats 16 and 80, breakdown at 64, outro at 128). Its grid puts the first beat at 0.23 s, where the drop's hit really is. The earlier hand value of 0.37 s landed the drop about 0.15 s late.
- Remotion's default output is `yuvj420p`. Render with `--pixel-format yuv420p` for uploads.
