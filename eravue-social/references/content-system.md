# Content system

## Pillars (every post maps to one)

| Pillar | Share | Examples | Job |
|---|---|---|---|
| **Build / demo** | 35% | "I built an AI receptionist for a dental clinic in 40 minutes. Here's the flow." Screen recordings, before/after | Proof of skill, comment-for-workflow lead magnets |
| **Client and agency stories** | 25% | Real projects (with permission), what went wrong, what we learned, the founders' journey from 0 clients (honest build-in-public) | Trust, relatability |
| **Owner insights** | 25% | "The 3 messages every clinic should automate", "Why your website gets visits but no enquiries", costed examples | Authority with buyers |
| **Takes / news** | 10% | Sharp opinions on AI hype, big launches explained for owners | Reach and comments |
| **Offer** | ≤5-10% | "We're taking 3 founding clients this month: here's the deal" | Direct conversion |

Build-in-public is a genuine asset right now: "Two founders, 0 clients, going all-in. Here's week 1" is honest, and people root for it. Never fake traction.

## Weekly calendar (cash sprint default)

| Day | LinkedIn | X | Instagram |
|---|---|---|---|
| Mon | Sanchit: build/demo | demo clip + 3-5 replies | LWC reel (build) |
| Tue | Sanchita: client/agency story | 2 posts + replies | @eravuedotcom proof post |
| Wed | Sanchit: owner insight | thread from Mon's build | LWC reel (news/take) |
| Thu | Sanchita: lesson/process | replies | @eravuedotcom collab reel |
| Fri | Sanchit: take or offer | weekly build recap | LWC reel (build-in-public) |
| Sat/Sun | optional: week recap | light | stories: behind the scenes |

Plus daily: 10-15 meaningful comments on ICP/prospect posts (engage mode), and replies to every comment within the first hour of each post.

## Calendar file format (`.growth/content-plan/YYYY-MM.md`)

```markdown
## Nov 12 (Wed)
### LinkedIn · Sanchit · insight · status: draft | approved | posted (C0012)
Hook A: ...
Hook B: ...
Body: ...
CTA: ...
Visual: (screenshot / carousel outline / none)
Repurpose: X thread Thu; IG caption for @eravuedotcom
```

## Writing rules

- **Hook first line:** a specific result, number, mistake or contrarian claim. No "In today's world...".
- **Short lines, plain words, one idea per post.** Read it aloud: if it sounds like a brochure, rewrite it.
- **Specific beats impressive:** "a 4-chair dental clinic in Gurgaon" beats "a healthcare client".
- **CTA matched to the job:** proof → "DM me 'DEMO'"; insight → a question to the reader; offer → the link or WhatsApp.
- **LinkedIn:** text posts with a clear hook, document/carousel posts for frameworks, native video for demos. Put links in the first comment if testing shows link posts get less reach (verify current behaviour monthly).
- **X:** short, opinionated; build threads with a video/GIF; most growth comes from good replies to bigger accounts in AI/automation/founder circles.
- **Instagram @eravuedotcom:** carousels for case studies (problem → build → result), demo reels, Collab with @lifewithcofounders.
- **Repurpose everything:** one build → reel (LWC) → LinkedIn video/post → X thread → @eravuedotcom carousel → blog (only if it targets a commercial keyword, via blog-writer).

## Comment-for-lead loop

"Comment WORKFLOW and I'll send it" posts only when the founders really send the thing. Every commenter who fits the ICP becomes a warm lead: add them to the tracker (`leads.py add --channel linkedin --kind inbound ...`) and send the promised item with a soft question about their business.

## Learning loop

Weekly: rank last week's posts by saves + DMs + profile visits (not likes). Write 3 lessons into the calendar file's header and into `.growth/strategy.md` §Learnings if durable. Feed reel lessons to `~/.claude/skills/lifewithcofounders/log.md`.
