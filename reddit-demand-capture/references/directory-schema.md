# Directory Schema

Use this file when creating or updating `.reddit-growth/`.

## Directory Layout

```text
.reddit-growth/
|-- project-profile.md
|-- activity-log.md
|-- insights.md
|-- subreddits/
|   `-- {subreddit}.md
|-- rules/
|   `-- {subreddit}.md
|-- searches/
|   `-- {YYYY-MM-DD}-{topic}.md
|-- opportunities/
|   `-- {YYYY-MM-DD}-{subreddit}-{slug}.md
|-- drafts/
|   `-- {YYYY-MM-DD}-{subreddit}-{format}.md
|-- posted/
|   `-- {YYYY-MM-DD}.md
`-- rejected/
    `-- {YYYY-MM-DD}.md
```

## File Purposes

### `project-profile.md`

Keep durable project context:

- Product name and URL.
- Offer summary.
- Target customer.
- Core pains solved.
- Competitors and alternatives.
- Approved positioning.
- Claims to avoid.
- Conversion goal.

### `subreddits/{subreddit}.md`

Track community-fit notes:

- Audience.
- Typical thread types.
- Common objections or pain language.
- Tone guidance.
- Participation opportunities.
- Last reviewed date.

### `rules/{subreddit}.md`

Track promotion safety:

- Rule summary.
- Link policy.
- Self-promotion policy.
- Vendor-mention policy.
- Survey/DM policy.
- Recent mod enforcement observations.
- Final classification.
- Last reviewed date.

### `searches/{date-topic}.md`

Store search artifacts:

- Query strings used.
- Subreddits searched.
- What surfaced repeatedly.
- Threads worth revisiting.
- Negative results.

### `opportunities/{date-subreddit-slug}.md`

Store one opportunity per file:

- URL.
- Subreddit.
- Post title.
- Timestamp.
- Opportunity type.
- Why it is a fit.
- Rule classification.
- Recommended response format.
- Risk notes.
- Draft status.

### `drafts/{date-subreddit-format}.md`

Store draft copy and variants:

- Primary draft.
- Safer draft.
- No-link draft.
- Notes on disclosure and CTA.

### `posted/{date}.md`

Store a running dated log of what actually got posted:

- Subreddit and thread URL.
- Final copy.
- Posting time.
- Account used, if the user tracks that.
- Early performance or reactions.

### `rejected/{date}.md`

Store opportunities explicitly avoided:

- URL.
- Rejection reason.
- Rule conflict, poor fit, thread too old, backlash risk, or low intent.

## Naming Rules

1. Use lowercase file names.
2. Replace spaces with hyphens.
3. Keep one opportunity per file.
4. Append dates in ISO format.
5. Update existing files when the same subreddit or recurring topic is revisited.

## Staleness Rules

- Opportunity files older than 14 days should usually be refreshed.
- Rules files older than 30 days should usually be re-checked.
- If a subreddit changes its pinned threads or rules, refresh immediately.
