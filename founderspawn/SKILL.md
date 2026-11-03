---
name: founderspawn
description: Write YouTube Shorts for FounderSpawn, Sanchit's gaming channel - scripted Discord/voice-chat skits with multiple AI voices over gameplay, real voice-chat funny moments over games like Rocket League or Minecraft, brainrot comedy, and horror or twist stories narrated by AI (ElevenLabs) over gameplay. Use for FounderSpawn ideas, multi-voice skit scripts, narration scripts, clip-cutting plans, hooks and titles.
---

# FounderSpawn

A YouTube Shorts gaming channel. The picture is gameplay (Minecraft, Rocket League, whatever is running) and the audio is AI voices or real voice chat. Nothing is sacred: Sanchit is testing formats to find what pops. Treat each idea as a bet and keep the mix varied until `log.md` shows a winner.

**Before writing, read** `../short-form-craft/SKILL.md` (the sibling skill folder) plus its `references/hooks.md`, `references/human-voice.md` and `references/critic.md`. Read `log.md` here and lean toward whatever has worked.

## The bar

Shorts is decided in the first second (viewed vs. swiped), then by how much of the video people watch. Gamers have seen every template, so the content has to feel like it came from *inside* gaming culture: fast, chaotic, a bit unhinged, and genuinely funny or genuinely creepy. Polite, tidy or "writerly" is death here.

- Gameplay is already moving on frame one, with 3–7 words of burned-in hook text.
- The first line of audio is already mid-chaos.
- Something escalates every few seconds.
- End on the punchline, the scream or the twist. Hard cut. Loops are gold.

## Formats

**1. Scripted VC skits (multiple AI voices).** A fake Discord call between 2–4 friends over gameplay, voiced with different ElevenLabs voices. **The topic can be literally anything**, not just gaming:
- **Gamer situations pushed to absurd:** someone thinks they're muted, 900 ping, the friend who's "almost there" for 20 minutes, a hardcore death that turns into a loot fight, someone's mom joining the call.
- **Pure brainrot wordplay:** misheard words and logic loops that spiral. "UK" heard as "you okay?", "Who's on first"-style confusion, someone taking every sentence literally, an argument about something that doesn't matter.
- **Everyday chaos:** ordering food together, someone's crush coming online, a group project, a dare that escalates.
- **Absurd hypotheticals argued dead seriously:** "would you fight one horse-sized duck…", "is a hot dog a sandwich", "could you beat a chicken in a fight".

The gameplay underneath doesn't need to match the topic.

Rules:
- each character has one clear trait (the panicker, the loot goblin, the calm one who's secretly worst);
- people talk over each other, cut each other off and scream;
- 3–4 escalations, then a button (callback or reversal);
- 20–45 seconds;
- give each character a voice note (age and energy) for ElevenLabs.

**2. Real VC funny moments.** Clips from Sanchit's own sessions. Here "the script" is the cut plan:
- start 0.5–1s before the setup line;
- hook text describes the *situation*, not the punchline ("he thought he was muted");
- captions on every line, with the funniest word emphasised;
- cut every silence longer than about 0.4s;
- end on the laugh peak or the stunned silence.
Ask what's in the clip if it isn't clear, and never invent lines for real clips. If he describes a moment, also pitch a scripted remake of it as a format-1 skit.

**3. Brainrot narration.** An AI narrator over gameplay with meme or GIF inserts. Absurd everyday stories, unhinged "facts", POV chaos, gamer rage. Slang and memes only where they hit. The joke has to work without them.

**4. Horror or twist stories.** AI narrator over gameplay. One anomaly, rules the viewer can track, escalation that gets personal, and a last line that flips the first. Original fiction only.

When asked for ideas, give a varied spread across formats unless the user names one or the log shows a winner. Lead with the strongest premise, not the safest. **Every idea gets the full treatment:** hooks, the complete script with every line, voice notes and a gameplay plan. Never a premise card.

## Voiceover format (ElevenLabs v3)

- **Skits:** use one code block per character, in line order, or one block with `NAME:` labels if the user generates per line. List each character's voice (age, energy, accent) once above.
- **Narration:** one code block containing only the spoken words plus a few audio tags.
- **Tags:** only where they change the performance, e.g. `[shouting]`, `[whispers]`, `[panicking]`, `[laughs]`, `[sighs]`, `[sarcastic]`, `[deadpan]`. Use punctuation for timing: `...` for a pause, a dash for being cut off.
- After the block, give the word count, about how many seconds (words ÷ 2.7), and a one-line direction.

## Footage

Sanchit records alone in Minecraft Creative, using the Flashback mod for camera replays, plus other games. Default to reusable gameplay plus a few inserts that land specific beats (a death screen, a chat message, a sign). For skits, gameplay that roughly matches the situation (a death, a grave, a goal) helps a lot. Keep shots to what one person can record.

## Output

Use the format from short-form-craft. Per video:
- 3–5 hook options (burned-in text plus the first line of audio);
- the script or cut plan;
- the voice notes;
- the gameplay plan;
- a Shorts title of under about 60 characters that doesn't spoil the punchline.

## Example that sets the bar

**VC skit: "hardcore funeral", about 35s.** Hook text: `he died 4 seconds ago`. Gameplay: three players standing around a fresh grave, then one wearing different boots.
Voices: KABIR (panicky, cracking), JAY (smug loot goblin), ARYAN (fake-calm).
```
KABIR: [panicking] guys guys GUYS I'm on half a heart where are you—
[death sound]
ARYAN: ...he's gone.
JAY: [sighs] Kabir was a real one.
ARYAN: He'd want us to keep going.
JAY: He would. He'd also want us to split his diamonds.
ARYAN: Obviously.
JAY: So I'll take them, since I was closest to him—
ARYAN: You called him a liability ten minutes ago.
JAY: Closest geographically.
KABIR: [shouting] I'M IN SPECTATOR. I CAN HEAR YOU.
ARYAN: [whispers] he can hear us.
JAY: [loudly] Kabir! We were just saying how much we miss you.
KABIR: You're wearing my boots.
JAY: [beat] ...they were on the floor.
```
Why it works: the death happens in the first second, grief turns into greed, the stakes rise when he can hear them, and the button is a visual callback (the boots).

**VC brainrot wordplay: "where you from", about 20s.** Hook text: `bro asked one question`. Any gameplay underneath.
Voices: DEV (chill, confused), OLLIE (polite British), SAM (joins late, neutral).
```
DEV: Where you from?
OLLIE: I'm from the UK.
DEV: Yeah I'm alright. But where are you from?
OLLIE: ...the UK.
DEV: Bro I SAID I'm fine. Where. Are. You. From.
OLLIE: [slowly] U. K.
DEV: [beat] ...thank you for asking. Genuinely. Nobody ever asks.
SAM: Yo, what's going on?
DEV: He keeps asking if I'm okay.
SAM: Are you okay?
DEV: [crying] NO.
OLLIE: ...I'm from England.
DEV: [instantly fine] Oh nice. Never been.
```
Why it works: the misunderstanding is clear by the third line, each repeat escalates the emotion, and the button snaps back to normal.

## Logging results

When results come in, append them to `log.md` (date, premise, format, hook, length, views, viewed-vs-swiped or % viewed, subs, takeaway). Re-read it before ideating, and say when a suggestion comes from it.
