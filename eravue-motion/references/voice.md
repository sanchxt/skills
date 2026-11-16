# Voice: performance, recording, analysis, processing

The voice sells the video more than the visuals. A clear, confident, well-paced voice over average graphics beats the reverse.

## What a good voiceover sounds like

**Sound**
- Close and intimate, as if talking to one person 50 cm away. No room echo, no hiss, no hum.
- Full but not boomy, clear but not harsh. S's present but not spitty; no pops on P/B.
- Consistent: the same distance, level and tone from first line to last, across sessions.
- Loud enough on a phone speaker *and* comfortable in earbuds. That comes from levels, not shouting.

**Performance**
- **Pace by format:** Reels and ads 160–185 wpm; explainers 140–160; tutorials 130–150. Vary it: speed up through context, slow down on the point.
- **Energy:** modern, confident, slightly excited to tell you. Smile on the hook (it can be heard). Not "announcer voice".
- **Stress one word per sentence**, the one that carries the meaning ("it *books* the appointment").
- **Pause before reveals and numbers** (0.3–0.6 s), then hit the number.
- **Land sentences:** end statements with a downward inflection (no upspeak), but keep energy into the next line.
- **Conversational:** contractions, short sentences (≤ 15 words), no read-aloud "and also furthermore".
- **Hook:** record it 3 times with different energy and pick the best one. It's 80% of the result.
- Talk to one specific person (a clinic owner, a founder), not "an audience".

## Recording guide

**Phone (main setup)**
- App: iPhone Voice Memos with *Settings → Voice Memos → Audio Quality → Lossless*; Android: a recorder that saves WAV, or the highest-quality option. Turn off any "noise reduction" or "enhance" in the app if possible (it causes warbles). Airplane mode.
- Room: soft and small (a bedroom with curtains, sofa cushions, or a wardrobe of clothes). Never a kitchen, bathroom or empty room. Fan and AC off.
- Position: phone on a stand or a stack of books, **not in hand** (handling noise). Bottom mic 15–20 cm from the mouth, slightly to the side (off-axis), so breaths and P's don't hit it directly. Keep the same position every session (mark it).
- Record 5 seconds of silence first (room tone; the analysis uses it to measure noise), then the script. If a line goes wrong, pause, say it again from the start of the sentence, and keep going. Retakes get cut later.
- Phones add a bass boost when close (proximity effect). That's the "bottom-heavy" tone the analysis usually finds in these recordings, and why the chain trims around 140 Hz.

**USB mic**
- 48 kHz, 24-bit if the software allows. Gain so peaks land around -12 to -6 dBFS (never clipping).
- 10–15 cm away, with a pop filter or slightly off-axis. Check whether the mic is side-address (you talk into its side) or end-address.
- Same room rules. Monitor with headphones for hum or buzz.

**Takes to deliver:** the raw file as recorded (no app processing), plus the script if it was read. If it was free-form, a transcript helps but isn't required (whisper transcribes it).

## Analysis: `node scripts/voice.mjs analyze <file> [--voice male|female]`

It reads the file locally (nothing uploaded) and prints:

| Line | What it means | Good |
|---|---|---|
| loudness | integrated LUFS, true peak, LRA (loudness range) of the raw take | raw -26 to -16 is normal; TP < -1; LRA under 8 is even delivery |
| noise | noise floor (quietest frames), speech level, SNR, and where the noise floor ends up after levelling to -16 | floor after levelling ≤ -60 dBFS is great; -60 to -50 is fine with denoise; above -45, re-record |
| tone vs target | per region, dB above or below a male (or female) speech target curve: rumble 63–100, warmth 125–160, mud 200–315, nasal 1–1.6k, presence 2.5–4k, S-band 5–6.3k, air 8–10k | within ±2 is natural. Large + means too much of that region, large – means too little |
| sibilance | how loud the loudest S's are vs typical vowels | ≤ 0 dB is fine; above 0 is spitty |
| plosive frames | share of speech with sudden sub-90 Hz bumps (pops, handling, table knocks) | under about 10% |
| clipped samples | digital overload | 0; anything audible means re-record |
| pacing | share of time speaking, pauses ≥ 0.7 s, and wpm if word timings are given | see pace targets above |

The target curve is shaped on the long-term average speech spectrum for male or female speakers, with a small "polished voiceover" lift in presence and air. It's a reference: the script corrects only part of any difference and caps every move, so it stays the same voice.

## Processing: `node scripts/voice.mjs process <raw> <out.wav> [options]`

Chain order (each step only if the analysis calls for it):

1. **High-pass** 80 Hz (95 Hz if rumble or pops) removes rumble and handling.
2. **Denoise** with `afftdn`, only when the noise floor would end up above -62 dBFS after levelling; 12 dB reduction, 18 if noisier. Over-denoising sounds "underwater" or robotic. If you hear that, lower `nr` or skip it.
3. **Corrective cuts**: boom 140 Hz (≤ -3 dB), mud at the worst of 200/250/315 Hz (≤ -5), nasal 1.15 kHz (≤ -3), harsh 3.2 kHz (≤ -3).
4. **Compression**: gentle, 2:1 (3:1 if LRA > 8), threshold about 4 dB above the speech level, 8 ms attack, 140 ms release. It evens out the delivery without pumping.
5. **Clarity boosts**: presence 3.5 kHz (≤ +4), air shelf from 8 kHz (≤ +3). No air boost on band-limited (phone-codec) recordings, because it only lifts hiss.
6. **De-esser**: light whenever highs were boosted, stronger when S's measure hot.
7. **Level**: static gain to the target (stem -16 LUFS), a -2 dBFS peak limiter, re-measured until within ±0.3 LU.

Options: `--lufs -16`, `--tighten 0.45` (shortens pauses over about 0.6 s to 0.45 s; do it *before* timing and captions), `--no-eq`, `--eq-strength 0.7` (0–1), `--voice female`, `--words timing.json` (to report wpm).

It writes `<out>.wav` (48 kHz, 24-bit mono), `<out>.ab.wav` and `<out>.voice.json` (before and after numbers + the chain).

**Always listen to the A/B** (10 s raw → gap → 10 s processed, both at the same loudness, because louder always sounds "better") on a phone speaker *and* earbuds. Listen for:
- boomy or muddy → raise eq-strength, or the cut;
- harsh or spitty S's → the de-esser isn't strong enough;
- thin → the high-pass is too high, or too much was cut at 140;
- underwater or robotic → too much denoise;
- pumping → the compression threshold is too low.

If something is off, adjust and re-run. The chain is printed, so you can tweak it by hand.

**Editing the take.** Do this before processing, or in Premiere:
- Remove retakes and false starts, "um/uh" and long hesitations. Whisper's word timings show where.
- Keep breaths but turn them down (-8 to -12 dB) rather than cutting them. Fully breathless speech sounds robotic.
- Natural pauses are 0.25–0.45 s between sentences, and up to 0.6 s before a reveal.
- The Premiere route still works: cut in Premiere, export SRT, `premiere-cuts.py` → `vo-from-cuts.mjs` (in the demos repo) rebuilds the cut from the raw file. Point it at this chain.

**Loudness targets**

| Stem / mix | Target |
|---|---|
| Voice stem | -16 LUFS, peaks ≤ -2 dBFS |
| Music bed under voice | about -27 LUFS before ducking (ends about 18–24 dB under the voice) |
| Final mix, all platforms | -14 LUFS integrated, ≤ -1 dBTP (`master.mjs`) |
| Music-only cut (no voice) | -14 LUFS |

-14 LUFS / -1 dBTP is the widely used working target for Reels, TikTok and YouTube. Instagram publishes no official spec, so treat it as a convention and re-check in a year.

## AI voices

**When:** quick drafts to test a script's timing, ad variants (several hooks), versions in other languages or accents, or when Sanchit can't record. Not for "founder speaking" content unless it's his own cloned voice and he has OK'd that specific use.

- **ElevenLabs:** returns character-level timestamps alongside the audio, so use them for timing instead of whisper (`@remotion/elevenlabs` has helpers). Fish Audio S2 is also an option (see the `boss-lobbies-fish-voiceover` skill for its tagging style).
- **Script for TTS:** write numbers as words where the model stumbles, use commas and full stops for pacing, and use the model's emotion and pace tags sparingly.
- **Processing:** AI voices are already clean. Use `--no-eq` (or just levelling to -16). Never denoise them.
- **Disclosure:** Meta labels or may require disclosure of realistic AI-generated or altered content in ads. Check Ads Manager's AI disclosure setting when running ads with a synthetic voice.
- Keep the API key out of files and chat. The founders enter it themselves.
