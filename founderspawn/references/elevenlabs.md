# ElevenLabs-Ready Narration

The default deliverable is one finished voiceover the user can paste directly into ElevenLabs without deleting directions.

## Copy-Ready Block

Put only spoken words in one plain-text code block. Keep headings, timestamps, shot notes, captions, emphasis notes, word counts, and settings outside it.

Default to plain narration that works across ElevenLabs models. Do not insert audio tags, SSML, bracketed emotions, or stage directions unless the user explicitly names a model and asks for them. Very short prompts can produce unstable delivery, so create enough sentence-level context for the voice to understand the emotion.

## Length And Pace

Use these as editing guides, not padding targets:

- 15–22 seconds: about 42–65 words
- 23–35 seconds: about 65–100 words
- 36–50 seconds: about 100–145 words, only for a real story or multi-stage test.
- Longer stories: estimate from the actual word count at a plausible roughly 140–180 words per minute, allowing pauses. A 250-word tragedy is not a 45-second script. Use the requested duration and selected voice delivery rather than imposing a universal short cap.

Prefer natural text near the intended duration over cramming extra words into a faster setting. A reasonable starting speed is 1.0; suggest a modest increase only when the selected voice stays clear. ElevenLabs supports roughly 0.7–1.2 speed, but extremes may reduce quality.

## Text Shaping

- Use periods for clean beat changes and commas for tiny pauses.
- Use an em dash or ellipsis at most once when the hesitation or interruption has meaning.
- Spell out awkward symbols, abbreviations, coordinates, or version numbers when pronunciation would otherwise fail.
- Punctuate for how the line should sound, not for visual decoration.
- Avoid all-caps as a substitute for writing an emphatic sentence.
- Keep proper nouns and Minecraft item names consistent.

## Delivery Direction Outside The Block

Provide one compact line with:

- mood;
- approximate speed;
- the one word or phrase to emphasize;
- where to slow down or pause before the payoff.

If the user identifies Eleven v3 and wants expressive tags, create a separately labeled v3-ready block and use tags sparingly. Do not mix v3 tags with SSML break tags.

## Final Listening Pass

Before delivery, silently read the script aloud. Fix tongue tangles, repeated sentence openings, accidental rhymes, ambiguous pronouns, breathless lists, and any wording a real player would not naturally say.
