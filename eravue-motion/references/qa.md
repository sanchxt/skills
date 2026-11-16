# QA before anything ships

Render stills first (fast), fix, then render the full video, then master. Show the user stills and the final file. Don't call it done on a render you haven't looked at.

## Contact sheet

Render stills at: frame 0, the hook's last frame, every scene's hero moment (`cue + 10`), the reveal, every number, the result, the CTA and the end card. With `showSafe: true` render the 9:16 at least once. Look at them all (Read the images).

## Checklist

**Story and truth**
- [ ] Frame 0 is moving, says something, and works as a cover. No logo in the first 3 s (ads and Reels).
- [ ] Every claim is true; demos are labelled; news facts verified, with source and date in the notes.
- [ ] No invented clients or numbers; no real personal data or API keys on screen.
- [ ] CTA is specific, and the thing promised ("comment WORD") is ready to send.

**Visual**
- [ ] Squint test: the most important thing in each frame is obvious.
- [ ] One accent per frame; the look's tokens only; at most 2 families + mono.
- [ ] Text readable at phone size (view stills at 1/3 size). Sizes ≥ type-color.md minimums.
- [ ] Nothing in the safe-zone no-go areas (9:16); captions never cover what's being explained.
- [ ] Margins and alignment consistent (8 px grid); nothing touching the frame edge by accident.
- [ ] On-screen text stays up for its reading time (0.6 s + 0.25 s/word).
- [ ] No dead frames over about 1.5 s; no more than 3 things moving at once.
- [ ] No flashing over 3 per second.
- [ ] Spelling: n8n, WhatsApp, Claude, eravue.com, client names; numbers formatted consistently.

**Sync**
- [ ] 5 spot-checks (hook, reveal, a number, result, CTA): visuals land on their word.
- [ ] Captions match the audio word-for-word (spelling from the script).
- [ ] Scene changes land on downbeats where intended; the music ends cleanly.

**Audio**
- [ ] Founder approved the voice A/B (or it's an AI voice, levelled only).
- [ ] Music under the voice is felt, not fighting: listen once on a phone speaker, once on earbuds.
- [ ] Music license logged in `music/LICENSES.md`; "ads OK" is yes if this is an ad.
- [ ] `node scripts/master.mjs <file> --check`: -14 LUFS ± 0.5, ≤ -1 dBTP, H.264 yuv420p, correct size and fps. Then master it.
- [ ] No clicks at the edit points, and no music cut off mid-phrase at the end.

**Delivery**
- [ ] Files named `<slug>-<v|f|h>-v<N>.mp4`, plus cover stills.
- [ ] Post caption drafted (hand to `eravue-social`); ad variants listed for `cmo`.
- [ ] `log.md` updated.

## Aesthetic critique (do this honestly, then fix)

Pretend you're a senior motion designer seeing it for the first time:
1. What's the first thing my eye goes to in each frame? Is it the right thing?
2. Where did I get bored or confused? (Usually: too long on one frame, or two ideas at once.)
3. Which moves feel cheap or random? Remove them rather than replace them.
4. Does it feel like *one* look from start to finish?
5. Would a business owner screenshot or send this? If not, what one change would make them?

List the top 3 fixes, make them, and re-render the affected stills.
