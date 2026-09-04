# Eleven v3 voiceover

Use whenever delivering or revising narration for ElevenLabs v3. If the user names another model or wants clean untagged text, honor that instead.

Deliver one fenced block containing only paste-ready narration.

- Use square-bracket delivery tags sparingly and only for audible vocal behavior, such as `[whispers]`, `[thoughtful]`, `[softly]`, `[sighs]`, or `[building emotion]`.
- Do not include `[music]`, `[cut to]`, `[smiles]`, timestamps, editor notes, headings, citations, or other non-audible directions in the block.
- Eleven v3 does not support SSML break tags. Shape pacing with sentence structure, line breaks, em dashes, ellipses, and occasional capitalization.
- Spell dates, numbers, abbreviations, and symbols as they should be spoken when pronunciation is ambiguous.
- For difficult names, optionally use slash-wrapped IPA only around the relevant word and advise a test generation.
- Match the voice and stability to the emotional delivery. Use Natural as a balanced starting point; test before locking picture.
- Tags and punctuation cannot rescue a crowded or weakly causal script. Preserve natural phrasing and breathing room.

After the fenced block, state the model assumption, word count, estimated duration, and a compact voice/stability starting recommendation.

Primary reference: [ElevenLabs, “Best practices: Prompting Eleven v3”](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices#prompting-eleven-v3). Verify current model behavior when it matters.
