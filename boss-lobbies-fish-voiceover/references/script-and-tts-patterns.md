# Short-form scripts and Fish Audio S2.1 Pro

Use this reference to select the structure and TTS treatment. Treat it as a retention-testing guide, not a claim that one format wins universally.

## Research anchors

- YouTube says Shorts recommendations use viewer choice, average view duration, and average percentage viewed. Use these to compare similar scripts and lengths. <https://support.google.com/youtube/answer/11914225>
- TikTok creative guidance treats the first three to six seconds as the hook window and recommends value early, then a clear message and CTA. Adapt its ad-creative findings to organic content. <https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads>
- Fish Audio S2 supports natural-language square-bracket controls rather than S1 parenthesis tags. Controls are learned text cues, not a fixed command list. <https://docs.fish.audio/developer-guide/models-pricing/models-overview>

## Hook selection

Choose one engine. Name the game, mode, item, map, boss, rank, or mechanic before the hook becomes vague.

| Engine | Best use | Shape | Do not use when |
|---|---|---|---|
| Visible payoff | Camo, drop, round clear, rare reward, rank | `This is what happens when [specific action].` | The payoff is absent from the footage. |
| Mistake | Beginner route, challenge, loadout choice | `Stop doing [specific thing] in [mode].` | The right way is merely an opinion stated as fact. |
| Contradiction | Weird mechanic, surprising test | `This looks useless. It is not.` | The reveal has no real proof. |
| Time pressure | Official patch, expiring event, known reset | `[Specific thing] changes after [verified timing].` | Timing is a rumor or has already changed. |
| Curiosity question | Hidden location, method explanation | `Have you seen this spot on [map]?` | The answer takes too long to begin. |

Avoid `Today we are`, empty superlatives, a logo intro, and hooks unrelated to the actual game.

## Personality without generic hype

Give the narrator a point of view when the footage is funny, surprising, or satisfying. Build a comic premise from a visible detail, then make two or three reaction beats feel like they came from the same person watching the clip. The gameplay should be the joke, not a list of kills and rewards.

| Angle | Shape | Footage requirement |
|---|---|---|
| Playful comparison | `Ol' Tessie is not a truck anymore. She is a zombie bouncer.` | The comparison must describe the visible result. |
| Friendly warning | `Leave the left-side gap, unless you want to trap yourself with the zombies.` | Show the mistake and consequence. |
| Cocky reveal | `This is the most illegal-looking parking job on Ashes of the Damned.` | Show the unusual parking position immediately. |
| Shared-player frustration | `The horde finally learned how to queue. Bad news for them.` | Show the resulting pile-up before the line. |
| Addicted disbelief | `Why would I ever leave this lobby?` | Show a streak, easy kill chain, or visible progression before the line. |
| Mock-serious flex | `Leaving would be irresponsible.` | Show a sustained advantage that makes the exaggeration playful. |

Do not begin with `reported`, `patched`, `verify`, `Boss Services`, or a product outcome unless that is the actual subject of the video. Do not force a joke into every sentence, but do not settle for one throwaway joke followed by a plain inventory of gameplay events.

## Reliable Short structure

For a 22-35 second gameplay Short:

1. **0-2s - hook/proof:** Show the outcome, danger, or surprising location; say one sharp claim.
2. **2-6s - context:** Name the game, mode/map, and exactly what the viewer will learn.
3. **6-22s - proof:** Deliver two or three visual beats. Add a new fact, action, or consequence per beat.
4. **22-30s - payoff/caveat:** Show the result. Put a reported/current-build caveat in a readable on-screen label or caption; say it aloud only when it changes the viewer's understanding of the result.
5. **Last 2-3s - one close:** Use a gameplay punchline, follow/comment prompt, or a requested matching CTA.

For a 15-22 second clip, remove the setup beat and use one clear proof beat. For a 36-50 second clip, add only a test, comparison, or caveat that materially proves the conclusion.

## Emotion map

Let the selected Fish voice supply its own identity. Drive the delivery through a real narrative turn.

| Clip type | Emotional arc | Useful S2 cue shapes |
|---|---|---|
| Verified glitch/hidden route | intrigued -> precise -> satisfied | `[quick, intrigued]`, `[more focused]`, `[small, satisfied laugh]` |
| Reported/untested method | intrigued -> precise -> satisfied; reserve caveat for on-screen status unless it is the reveal | `[quick, intrigued]`, `[more focused]`, `[small, satisfied laugh]` |
| Patch/update | alert -> helpful -> confident | `[alert, clear]`, `[quick emphasis]`, `[confident]` |
| Grind/reward | empathetic -> motivating -> satisfied | `[you know the pain]`, `[encouraging]`, `[satisfied]` |
| Service CTA | useful -> warm optional close | `[warm, confident]` |

Use one primary tone at a time. Put a cue before the hook, the real reveal, or a requested CTA. Avoid a cue before every sentence, exaggerated shouting, nervous filler, and sound effects that compete with gameplay.

### ElevenLabs performance cues

When the brief asks for personality, expressions, or ElevenLabs formatting, include two to four short square-bracket cues in the copy/paste script. Make the cues describe an audible delivery shift rather than a production instruction.

| Beat | Useful cue shapes |
|---|---|
| Addicted or astonished hook | `[excited, can't believe it]`, `[hooked, amused]` |
| Visible absurdity | `[quick laugh]`, `[laughing]`, `[slightly incredulous]` |
| Cocky payoff | `[playfully cocky]`, `[small, satisfied laugh]` |
| Engagement close | `[low, conspiratorial]`, `[direct, inviting]` |

Write around the cue so the emotion is evident even if the engine ignores it. Preview the first cue and the CTA; remove brackets only if that particular voice speaks them aloud.

## TTS writing checklist

- Prefer one idea per sentence and one breath-sized line per beat.
- Use punctuation for real pauses; do not manufacture pauses with repeated dots or exclamation marks.
- Preserve on-screen spelling separately if it differs from the spoken form.
- Use only `[]` for S2/S2.1 natural-language cues. Do not mix in S1-style parenthesis tags.
- Preview the hook, personality line, and payoff before exporting. Check that the voice does not say a cue aloud and that the personality line sounds conversational rather than scripted.
- Fix pronunciation in the text first. Use Fish Audio phoneme controls only if an important name still reads incorrectly. <https://docs.fish.audio/developer-guide/core-features/fine-grained-control>
