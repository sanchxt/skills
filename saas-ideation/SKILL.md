---
name: saas-ideation
description: Deep current-market SaaS, consumer app, micro-SaaS, website, and AI product ideation for solo indie builders who want fast recurring revenue. Use when the user asks for profitable SaaS ideas, quick-money app ideas, recurring revenue project ideas, market validation, blue-ocean opportunities, online research-backed startup ideas, solo-founder product selection, or go-to-market plans for AI-built projects.
---

# SaaS Ideation

Use this skill to find and evaluate realistic, solo-buildable software products that could generate recurring revenue quickly. Treat the work as market research plus founder judgment, not brainstorming.

## Operating Rules

- Browse the web unless the user explicitly forbids it. The task depends on current demand, competition, pricing, platform shifts, and recent customer pain.
- Use primary or high-signal sources where possible: official product/pricing pages, app marketplaces, review sites, Reddit/communities, job boards, Google Trends or equivalent trend signals, keyword tools, public directories, competitor changelogs, marketplaces, funding/product-launch sites, and credible industry reports.
- Cite sources with links and dates or access timing when available.
- Do not claim any idea is guaranteed to make money. State confidence, evidence strength, risk, and what must be validated before building.
- Optimize for the user's constraints: solo indie, AI-assisted development, low upfront spend, quick path to paid users, recurring revenue, and a realistic marketing channel the user can run alone.
- Ask concise questions before researching when missing facts would materially change the outcome, such as target geography, skills, available weekly hours, budget ceiling, preferred niches, existing audience, risk tolerance, or platforms the user refuses to use.
- If the user says urgency matters, prioritize cash speed over novelty. Favor painful business workflows, compliance-adjacent chores, creator/operator utilities, paid templates plus SaaS hybrids, and narrowly scoped B2B tools with obvious buyers.
- Avoid ideas that depend on large ad budgets, regulated financial/medical/legal outcomes without expert oversight, enterprise sales cycles, heavy data licensing, expensive infrastructure, or app-store virality as the main acquisition plan.

## Research Workflow

1. Clarify constraints only if needed.
   - Ask at most 3 questions at a time.
   - If the user explicitly says to proceed without questions, make assumptions and label them.

2. Build a research map.
   - Identify 3-6 opportunity zones to investigate.
   - Include both "common but still monetizable" ideas and less obvious underserved-market ideas.
   - Define the buyer, painful job, likely budget owner, and why the pain is urgent.

3. Search deeply and currently.
   - Gather evidence for demand, pain intensity, willingness to pay, competition, pricing, platform/channel fit, and recent trend movement.
   - Use multiple source types per finalist idea. Do not rely on a single article or generic market-size claim.
   - When subagents are permitted by the active Codex tool policy and the user has allowed parallel/delegated work, use them for independent research lanes such as competitor pricing, community pain mining, keyword/trend analysis, and marketplace/app-store scans.
   - Use Chrome or browser automation when a source requires interaction, login state, screenshots, marketplace filtering, or rendered-page inspection.

4. Separate evidence from inference.
   - Label direct findings, inferred demand, assumptions, and unknowns.
   - Prefer exact competitor prices, review complaints, recent community posts, search phrases, and buyer quotes over vague TAM statements.

5. Score every serious candidate.
   - Read `references/research-rubric.md` when scoring ideas.
   - Score each idea on usefulness, speed to first revenue, recurring potential, competition, differentiation, build complexity, platform fit, solo marketing ease, upfront cost, and risk.
   - Penalize ideas that are interesting but slow to monetize.

6. Recommend a short list.
   - Present 5-10 researched ideas unless the user requested a different count.
   - Include 1-3 highest-conviction picks and explain why they beat the rest.
   - For each top pick, provide a wedge MVP, pricing, buyer persona, first marketing channel, validation test, 7-day launch plan, and build risks.

## Output Format

Use this structure unless the user requests another format:

```markdown
## Assumptions
- ...

## Research Signals
- Source-linked bullets grouped by market/opportunity zone.

## Ranked Ideas
| Rank | Idea | Buyer | Platform | Price | Revenue speed | Build difficulty | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Top Picks
### 1. Idea name
- Pain:
- Evidence:
- MVP:
- Why someone pays:
- Pricing:
- Platform:
- Solo marketing:
- First 7 days:
- Validation test:
- Risks:
- Kill criteria:

## Do First
- The single best next action to validate money quickly.
```

## Quality Bar

- Keep researching until the recommendations are backed by concrete, current evidence or until a clear blocker is reached.
- Do not stop at generic ideas like "AI resume builder" without a specific buyer, wedge, channel, and reason the user can win despite competition.
- Prefer small paid workflows over broad consumer apps unless consumer distribution is unusually clear.
- Include hard negatives. If an idea looks tempting but weak, say why.
- Make the final advice decisive: tell the user what to try first, what to ignore, and what evidence would change the recommendation.
