# Eleven v3 voiceover default

Use this reference whenever delivering or revising narration for ElevenLabs.

Unless the user specifies a different TTS model or requests untagged copy, deliver voiceover as a single Eleven v3-ready block.

- Use square-bracket audio tags sparingly and only for audible vocal delivery, such as `[whispers]`, `[thoughtful]`, `[sighs]`, `[excited]`, `[softly]`, or `[building emotion]`. Place each immediately before or after the passage it affects.
- Do not use non-audible or production directions such as `[music]`, `[standing]`, `[cut to]`, or `[smiles]`. Keep music and visuals outside the voiceover block.
- Do not use SSML `<break>` tags: Eleven v3 does not support them. Use natural sentence structure, line breaks, em dashes, and ellipses for pacing.
- Use punctuation intentionally: ellipses add pause and weight; occasional capitalization adds emphasis. Do not over-capitalize or tag every line.
- Spell dates, numbers, abbreviations, and symbols in their intended spoken form when ambiguity could hurt delivery (for example, `twenty twenty-three`, not `2023`).
- For names likely to be mispronounced, optionally use v3's slash-wrapped IPA syntax, for example `/kɛ hwi kwɑn/`. Apply it only to the word or phrase requiring control, include stress markers where useful, and advise testing because pronunciation is not perfectly consistent across voices.
- Choose a voice whose natural character matches the desired delivery. For expressive tags, recommend Creative or Natural stability; Robust may respond less to direction. Do not promise a tag will override an incompatible voice.
- Keep the text genuinely narratable. The tags and punctuation are performance cues, not a substitute for a causal, paced script.

After the script, state the model assumption and give a compact starting recommendation: a voice that matches the intended tone, Natural stability for balanced delivery, and a test generation before locking the edit.

Source: [ElevenLabs, “Best practices: Prompting Eleven v3”](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices#prompting-eleven-v3), accessed August 29, 2026.
