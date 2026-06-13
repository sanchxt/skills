# X/Twitter Search Patterns

## Core Operators

- Exact phrase: `"project management"`
- Any word: `(notion OR airtable OR spreadsheet)`
- Exclude word/operator: `-jobs`, `-hiring`, `-filter:replies`
- Account author: `from:username`
- Replies to account: `to:username`
- Mentioning account: `@username`
- Hashtag: `#buildinpublic`
- Language: `lang:en`
- Date range: `since:2026-06-01 until:2026-06-07`
- Minimum likes: `min_faves:100`
- Minimum reposts: `min_retweets:25`
- Minimum replies: `min_replies:10`
- Replies only: `filter:replies`
- Exclude replies: `-filter:replies`
- Links only: `filter:links`
- Exclude reposts/retweets: `-filter:retweets`

X API-style operators may also appear in docs and tools:

- Links/media: `has:links`, `has:images`, `has:videos`
- Exclude replies/retweets: `-is:reply`, `-is:retweet`
- Verified authors: `is:verified`

When X.com web search rejects or ignores an operator, retry with the older web operator form (`filter:` / `min_faves:`) or remove the operator and narrow with dates.

## Direct Search URLs

Use URL-encoded queries:

```text
https://x.com/search?q=<encoded-query>&src=typed_query&f=live
https://x.com/search?q=<encoded-query>&src=typed_query&f=top
```

Use `f=live` for chronological freshness and `f=top` for popular posts.

## Pain-Language Query Templates

Replace bracketed text with product-specific concepts:

```text
"any tool for" [workflow] lang:en since:YYYY-MM-DD -filter:retweets
"what do you use for" [workflow] lang:en since:YYYY-MM-DD
"looking for" ([tool] OR [workflow]) lang:en since:YYYY-MM-DD
"recommend" ([tool] OR [category]) lang:en since:YYYY-MM-DD
"I hate" [competitor] lang:en since:YYYY-MM-DD
"switching from" [competitor] lang:en since:YYYY-MM-DD
[competitor] (expensive OR slow OR broken OR annoying OR "not working") lang:en since:YYYY-MM-DD
"how do I" [problem] lang:en since:YYYY-MM-DD
"struggling with" [problem] lang:en since:YYYY-MM-DD
"is there a way to" [problem] lang:en since:YYYY-MM-DD
```

## High-Engagement Discovery

Use engagement floors to find public pain with reach:

```text
[problem] min_faves:100 since:YYYY-MM-DD lang:en -filter:retweets
[category] "what do you use" min_replies:10 since:YYYY-MM-DD lang:en
[competitor] (bad OR broken OR expensive) min_faves:50 since:YYYY-MM-DD lang:en
```

For the most popular posts in a niche:

1. Search a broad concept with `f=top`.
2. Add `since:` and `until:` for a tight date window.
3. Add `min_faves:` or `min_retweets:` only after confirming results exist.
4. Exclude reposts and broad spam terms.
5. Inspect replies to popular posts for sharper lead opportunities.

## Reply Opportunity Discovery

Replies often contain the best demand signal:

```text
[problem] filter:replies since:YYYY-MM-DD lang:en
to:[competitor_handle] (help OR broken OR issue OR refund OR alternative) since:YYYY-MM-DD lang:en
@[competitor_handle] (alternative OR "not working" OR expensive) since:YYYY-MM-DD lang:en
```

When recommending outreach, prefer direct replies to recent, unresolved questions over replies under viral posts with hundreds of competing comments.

## Noise Filters

Add these only when needed:

```text
-jobs -hiring -giveaway -airdrop -crypto -nsfw -adult -casino
-filter:retweets
-filter:links
```

Do not over-filter at the start. Remove noise after you see the first result set.
