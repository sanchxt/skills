# Writing and the quality gate

The project's own writing rules (from its blog skill) win on voice, structure, frontmatter and formatting. This file adds the bar every post must clear before it goes live.

## Writing

- **Answer first.** The first 2-4 sentences answer the main query, with the key number or verdict. No warm-up.
- **One reader.** Write to one segment from `.seo/audience.md`, in their words. Use their examples, currency, tools and constraints.
- **Question-shaped H2s** taken from PAA, GSC and the language bank, each opening with a 1-3 sentence answer that makes sense on its own (quotable for snippets and AI answers).
- **Evidence.** Every non-obvious fact, price or statistic has a source link or is clearly marked as the business's own experience. Prefer primary sources and figures from the last 12 months.
- **Something only this business can say**: a worked example, a realistic cost or timeline from how they actually deliver, a decision framework, a checklist, a diagram. If you can't add anything beyond the top 5 results, the topic isn't ready; pick another.
- **Useful formats**: tables for comparisons and costs, numbered steps for processes, a short "Key takeaways" block, a 3-6 question FAQ in real phrasing.
- **Internal links (3-6)**: the money page for this topic, plus related live posts, with descriptive anchors. Then add one link **to** the new post from an existing related post when the project tooling makes that safe (pull, edit, push, keeping the slug).
- **External links (1-3)** to authoritative sources.
- **Length follows intent**: usually 1,200-2,000 words for guides and comparisons. Cut padding.
- **Human voice**: plain, specific, confident. Ban list: "in today's fast-paced world", "unlock", "delve", "elevate", "game-changer", "revolutionise", "seamless", "leverage" (as a verb), "navigate the landscape", "it's important to note", "in conclusion". No emoji. Vary sentence length.
- **Metadata**: meta title with the primary keyword near the start, within the project's length limit; meta description that's benefit-led and specific; short keyword-led slug; the right existing category; existing tags reused.

## Quality gate

Run every check. Fix what you can. If something can't be fixed, don't publish: tell the user what's blocking.

**Search fit**
- [ ] Primary keyword in slug, meta title, first 100 words, one H2; no stuffing.
- [ ] Page type matches what ranks today (checked within this run).
- [ ] No live post targets the same intent (checked within this run).

**Truth**
- [ ] Every number, price, date, product feature and claim was verified in this run or comes with a source link.
- [ ] No invented clients, results, quotes, testimonials or case studies.
- [ ] Year references and "latest" claims are current.

**Usefulness**
- [ ] The opening answers the query.
- [ ] At least one original element (example, framework, table, diagram, checklist).
- [ ] FAQ answers are real answers, not teasers.

**Links and media**
- [ ] 3-6 internal links, all returning 200 (check with curl), including the relevant money page.
- [ ] External links resolve and are authoritative.
- [ ] Cover/OG generated and viewed; every image viewed, with descriptive alt text.

**Voice**
- [ ] Re-read the whole post once as the target reader. Rewrite any sentence that sounds generic or machine-written, and remove banned phrases.

**Tooling**
- [ ] Project validation (dry run) has no errors and no unexplained warnings.

## Refreshing an existing post instead

Pull the live version first (never trust a stale local file). Keep the slug and category unless they're wrong. Update facts and year, add the answer-first opening, new sections the SERP now expects, internal links and an updated FAQ. Push it as an update, keeping its published status, and report what changed.
