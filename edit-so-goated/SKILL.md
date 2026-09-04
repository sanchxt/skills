---
name: edit-so-goated
description: Research, plan, script, package, and improve EditSoGoated short-form videos about real people, athletes, musicians, film/TV/game talent, and fictional characters. Use for timely story scouting, concise ElevenLabs-ready voiceover stories, music-led edits with no voiceover, clip/song/hook planning, or analytics-led revisions for YouTube Shorts, Instagram Reels, and TikTok; do not use for unrelated long-form videos or generic social posts.
---

# EditSoGoated

Create source-aware short-form edits that earn three viewer decisions: **stop, stay, and act**. Support two equal production formats:

- **Voiceover story:** a compact transformation or hidden-context story narrated over purposeful clips, dialogue, music, and a payoff-aligned drop.
- **Music-led edit:** no narrator; the first-frame visual/text, clip progression, sound, beat structure, transitions, and final image carry the idea.

Never promise virality or treat a duration, retention rate, cut frequency, hashtag count, posting time, or audio as a universal algorithm hack.

## Route the request

Infer the mode from the prompt and do not force a voiceover deliverable into a music-led request.

- **Scout:** find current or evergreen subjects and angles. Read [references/scouting-and-sourcing.md](references/scouting-and-sourcing.md). If the user does not choose a format, score and label suitability for both formats.
- **Story:** create or revise a voiceover-led short. Read [references/hooks-and-attention.md](references/hooks-and-attention.md), [references/voiceover-stories.md](references/voiceover-stories.md), and the sourcing reference. Read [references/eleven-v3-voiceover.md](references/eleven-v3-voiceover.md) before delivering narration.
- **Short / clip edit / aesthetic edit / no voiceover:** create a music-led edit. Read [references/hooks-and-attention.md](references/hooks-and-attention.md), [references/music-led-edits.md](references/music-led-edits.md), and the sourcing reference.
- **Clips, songs, timestamps, effects, or full timeline:** also read [references/production-music-and-rights.md](references/production-music-and-rights.md).
- **Growth, diagnosis, testing, or performance revision:** read [references/analytics-and-iteration.md](references/analytics-and-iteration.md).
- **Research rationale or strategy audit:** read [references/research-foundation.md](references/research-foundation.md) for the evidence trail behind the hook, duration, attention, originality, and platform recommendations.
- **Full package:** use the relevant schema in [references/deliverable-templates.md](references/deliverable-templates.md).

If the user names only a subject and asks for “ideas,” default to two compact concepts: one voiceover story and one music-led edit. If they say “Scout,” return researched candidates rather than finished scripts. If they say “Story,” default to voiceover. If they say “Short,” “Clips,” “edit,” “song edit,” or “no voiceover,” default to music-led.

## Research before creating

Browse current sources for real-world facts, developing stories, release schedules, public interest, platform rules, trend claims, songs, clip URLs, and availability. For fictional subjects, verify canon and distinguish what the work shows from interpretation or fan theory. Treat wikis, Reddit, fan edits, and existing Shorts/Reels/TikToks as discovery or audience evidence, not sole support for material or sensitive claims.

Build a small claim ledger when facts matter. Resolve contradictions, use dates, attribute personal accounts, and omit low-confidence claims. Link the material sources in production notes, never inside paste-ready narration.

For “trending now,” verify recency, why interest is rising, and the relevant country/platform. Do not label an audio or person trending from memory.

## Choose the right format before drafting

Score candidates on both 0–10 scales from the scouting reference:

- **STORY:** Stakes, Turn, Outcome, Recognition, Yield of proof.
- **EDIT:** Iconicity, Dynamic motion, Emotional contrast, Track/drop fit, source-rights viability.

Prefer scores of 8–10 for the corresponding format. A candidate can be `Story-first`, `Edit-first`, `Works for both`, or `Weak—replace it`. Fame alone does not make a good story, and a strong biography does not guarantee enough visual motion for a music-led edit.

## Duration defaults are hypotheses, not rules

Use the shortest version that preserves the promised payoff.

- **Voiceover story default:** 25–40 seconds, usually about 65–100 narrated words at an emotionally natural pace. Offer a 15–25 second cutdown when the arc survives it. Use 40–55 seconds only when an extra beat or authentic clip materially strengthens the payoff.
- **Music-led default:** 8–20 seconds. Use 20–35 seconds when a longer build, dialogue fragment, transformation, or second drop earns its duration.

Never solve length by rushing the voice or cutting so quickly that shots become illegible. If the user requests another duration, honor it and adjust scope.

## Shared creative standard

- Make the subject or universal conflict legible immediately.
- Pair recognition with a truthful tension, reversal, contrast, or destination.
- Give every line, shot, text card, effect, and sound a function.
- Change visuals when information, emotion, motion, scale, source, or musical phrase changes—not because a timer demands it.
- Pay off the exact opening promise. A hook that wins the stop but loses trust is a failed hook.
- Place at most one natural CTA after the payoff, or move it to the caption/pinned comment when an in-video CTA would damage the aesthetic.
- Design for share value: awe, recognition, hidden context, identity, an emotional gift, or a genuinely defensible conversation.
- Preserve a recognizable channel grammar while varying the substance enough that videos do not feel mass-produced.

## Default deliverables

### Voiceover story

Unless the user narrows the request, provide:

1. recommended angle and verified factual/canon spine;
2. three materially different truthful hooks, including a recommended first frame;
3. one fenced ElevenLabs-ready narration block containing audible text only;
4. word count and estimated natural duration;
5. semantic beat/clip plan, music rise and drop placement, caption emphasis, and rights-safe fallback;
6. platform-native packaging and one CTA when requested;
7. sources and uncertainty/rights notes.

### Music-led edit

Unless the user narrows the request, provide:

1. concept, target emotion, and the micro-arc;
2. three hook packages, each pairing a first visual with optional 3–8 word text;
3. recommended edit style and transition/effect grammar;
4. current song candidates only after verification, with exact versions, rights/availability caveats, and one recommended track;
5. a track-specific beat map: hook, build, turn, drop/proof, ending/loop;
6. clip map with shot purpose, action/motion matching, caption/dialogue use, and source leads;
7. platform-native packaging, comment prompt, and cover/first-frame text;
8. sources and rights-safe alternatives.

Do not output an ElevenLabs block in music-led mode unless the user explicitly asks for dialogue, narration, or a hybrid version.

## Guardrails

- Never fabricate a quote, timestamp, URL, lyric, scene, motive, award, score, date, diagnosis, trend, or private thought.
- Do not use a cloned celebrity/character voice or imply endorsement.
- Do not treat credit, crop, pitch/speed changes, borders, effects, or “no copyright intended” as permission.
- Prefer licensed, permissioned, public-domain, creator-owned, official press, or in-product remix assets; state when rights remain unknown.
- Keep story framing and editing substantially original. AI narration plus scraped clips or the same effect template is not enough by itself.
- Handle trauma, death, abuse, health, minors, allegations, and other sensitive material without speculation or shock exploitation.
- Do not manufacture errors, hostility, humiliation, or false dilemmas merely to generate comments.
