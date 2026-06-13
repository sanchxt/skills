# Performance Analysis

## Purpose

Analyze post performance data to extract actionable insights, update the voice library, and continuously improve the content strategy. Every post is a data point — the goal is to learn from every single one.

## Data Collection

The user will provide performance data through one or more of these methods:

1. **Screenshots**: Analytics dashboard screenshots from Instagram Insights, LinkedIn Analytics, X Analytics, Facebook Insights, or third-party tools (Later, Hootsuite, Buffer, etc.)
2. **Manual input**: User dictates or types metrics for each post
3. **Pasted data**: Copy-paste from analytics exports or spreadsheets
4. **Chrome browser**: If the user is logged into their social accounts, use Chrome to visit analytics pages directly and extract data

### Key Metrics Per Post

Collect as many of these as available:

| Metric | What It Tells Us | Priority |
|--------|-----------------|----------|
| **Reach** | Unique accounts that saw the post | HIGH |
| **Impressions** | Total views including repeats | MEDIUM |
| **Likes** | Basic approval signal | MEDIUM |
| **Comments** | Depth of engagement | HIGH |
| **Saves** | Content value signal (IG) | HIGH |
| **Shares** | Virality signal | HIGH |
| **Engagement Rate** | (Total engagement / Reach) x 100 | HIGH |
| **Follower growth** | Net new followers from post | HIGH |
| **Profile visits** | Interest in the brand | MEDIUM |
| **Link clicks** | Conversion intent | HIGH (if applicable) |
| **Watch time / completion rate** | Video quality signal | HIGH (for video) |
| **Story replies** | Deep engagement | MEDIUM |
| **Hashtag reach** | Discovery effectiveness | LOW |

### Account-Level Metrics (Monthly)

| Metric | Tracks |
|--------|--------|
| Total follower growth (net) | Overall growth trajectory |
| Follower growth rate (%) | Growth velocity |
| Average engagement rate | Content quality trend |
| Total reach / impressions | Visibility trend |
| Best performing content type | Format optimization |
| Best performing day/time | Scheduling optimization |
| Audience demographics shifts | Targeting accuracy |

## Analysis Framework

### 1. Individual Post Analysis

For each post with data, evaluate:

**Performance Score:**
- Calculate engagement rate: (likes + comments + saves + shares) / reach x 100
- Compare to the brand's average engagement rate
- Label: Significantly above average / Above average / Average / Below average / Significantly below average

**Element Breakdown:**
- **Hook effectiveness**: Did the hook drive engagement? Compare similar topics with different hooks.
- **Content type impact**: How does this format compare to other formats?
- **Topic resonance**: Did this topic resonate better or worse than similar topics?
- **Visual impact**: Did the visual style stand out? Compare engagement of different visual approaches.
- **CTA effectiveness**: Did the CTA drive the desired action? (comments for comment CTA, saves for save CTA, etc.)
- **Timing**: Was it posted at an optimal time? How does same-topic content perform at different times?
- **Hashtag performance**: If hashtag reach data is available, which sets drove more discovery?

### 2. Pattern Recognition

Across all posts in the analysis period, identify patterns:

**Content Type Ranking:**
| Type | Posts | Avg Reach | Avg Engagement Rate | Avg Saves | Best For |
|------|-------|-----------|-------------------|-----------|----------|
| Carousel | {n} | {avg} | {avg}% | {avg} | {insight} |
| Reel | {n} | {avg} | {avg}% | {avg} | {insight} |
| Static | {n} | {avg} | {avg}% | {avg} | {insight} |
| etc. | | | | | |

**Content Pillar Ranking:**
| Pillar | Posts | Avg Engagement Rate | Best Performer | Worst Performer |
|--------|-------|-------------------|----------------|-----------------|
| Educational | {n} | {avg}% | {description} | {description} |
| etc. | | | | |

**Hook Type Ranking:**
| Hook Type | Posts | Avg Engagement | Best Example |
|-----------|-------|----------------|-------------|
| Question | {n} | {avg} | "{example}" |
| Bold statement | {n} | {avg} | "{example}" |
| etc. | | | |

**Timing Patterns:**
| Day | Avg Engagement | Best Time | Notes |
|-----|---------------|-----------|-------|
| Monday | {avg} | {time} | {pattern} |
| etc. | | | |

**Visual Style Patterns:**
| Style | Posts | Avg Engagement | Notes |
|-------|-------|----------------|-------|
| {style} | {n} | {avg} | {what worked} |

### 3. Competitive Benchmarking

If competitor data exists in `.growth/competitors/`:
- Compare our engagement rate to competitor averages
- Compare our growth rate to competitor estimated growth
- Identify content types where we outperform vs. underperform
- Note strategies competitors use successfully that we haven't tried

### 4. Audience Insight Extraction

From the data, infer:
- **What topics does our audience care about most?** (highest saves and shares indicate genuine interest)
- **How does our audience prefer to consume content?** (format preferences by engagement)
- **When is our audience most active?** (timing data)
- **What emotional triggers resonate?** (hook analysis)
- **What action is our audience most willing to take?** (CTA effectiveness)

### 5. Actionable Recommendations

Every analysis must conclude with specific, prioritized recommendations:

**Do More Of** (what's working — double down):
- {specific recommendation with data backing}
- {specific recommendation with data backing}

**Do Less Of** (what's underperforming — cut or fix):
- {specific recommendation with data backing}
- {specific recommendation with data backing}

**Experiment With** (new approaches suggested by the data):
- {experiment with hypothesis — "Based on X performing well, try Y"}
- {experiment with hypothesis}

**Optimize** (small tweaks that could improve results):
- {timing adjustment}
- {hashtag changes}
- {CTA refinements}
- {visual style shifts}

**Strategic Shifts** (bigger changes if needed):
- {any fundamental strategy changes the data suggests}

## Post-Analysis Actions

After completing the analysis, ALWAYS do these:

### 1. Update Voice Library
Read `.growth/voice-library.md` and:
- Add top-performing hooks with engagement data
- Add effective CTAs with context
- Update visual patterns (what worked, what didn't)
- Move underperformers to the "What Doesn't Work" section
- Update the learnings log

### 2. Update Insights
Read `.growth/insights.md` (or create it) and:
- Add new strategic learnings
- Update audience behavior insights
- Note any shifts in what works vs. previous months
- Record experiments and their results

### 3. Update Metrics History
Read `.growth/metrics.md` (or create it) and append a new entry with the current date and all account-level metrics collected during this analysis. See the **Metrics History File** section below for the format.

### 4. Save the Report
Store in `.growth/analytics/{YYYY-MM}.md`

## Analytics Report Template

```markdown
# Performance Analysis — {Month Year}

**Brand:** {brand name}
**Period:** {start date} to {end date}
**Analyzed:** {date}
**Data Source:** {where the data came from}

## Account Overview

| Metric | This Period | Previous Period | Change | Trend |
|--------|-----------|----------------|--------|-------|
| Followers | {count} | {count} | {+/- n} ({%}) | {up/down/flat} |
| Avg Engagement Rate | {%} | {%} | {+/- pp} | {up/down/flat} |
| Total Reach | {count} | {count} | {+/- n} ({%}) | {up/down/flat} |
| Total Impressions | {count} | {count} | {+/- n} ({%}) | {up/down/flat} |
| Avg Saves/Post | {count} | {count} | {+/- n} | {up/down/flat} |
| Avg Shares/Post | {count} | {count} | {+/- n} | {up/down/flat} |

## Content Performance by Type
{table from pattern recognition above}

## Content Performance by Pillar
{table from pattern recognition above}

## Top 5 Performing Posts

### 1. {Post description}
- **Date:** {date} | **Platform:** {platform} | **Type:** {format}
- **Hook:** "{hook text}"
- **Engagement:** {likes} likes, {comments} comments, {saves} saves, {shares} shares
- **Reach:** {reach} | **Engagement Rate:** {rate}%
- **Visual Style:** {brief description}
- **Why it worked:** {detailed analysis}
- **Voice library update:** {what was added to the library from this post}

### 2. ...
{repeat}

## Bottom 3 Performing Posts

### 1. {Post description}
- **Date:** {date} | **Platform:** {platform} | **Type:** {format}
- **Hook:** "{hook text}"
- **Engagement:** {metrics}
- **Why it underperformed:** {analysis — be specific and honest}
- **Lesson:** {actionable takeaway}

### 2. ...
{repeat}

## Hook Performance Analysis
{hook type ranking table}

**Best performing hook formula this period:** {formula with example}
**Worst performing hook formula this period:** {formula with example}

## Timing Analysis
{day/time patterns}
**Recommended posting schedule update:** {any changes to suggest}

## Competitive Benchmark
{comparison to competitor data if available}

## Key Insights
1. {most important insight — backed by data}
2. {second insight}
3. {third insight}

## Recommendations for Next Period

### Do More Of
- {recommendation}: {data backing}

### Do Less Of
- {recommendation}: {data backing}

### Experiment With
- {experiment}: {hypothesis based on data}

### Optimize
- {specific tweak}: {expected impact}

## Voice Library Updates Made
- **Hooks added:** {list}
- **CTAs added:** {list}
- **Visual patterns updated:** {list}
- **Learnings logged:** {list}

## Insights File Updates Made
- {what was added to insights.md}
```

## Metrics History File

`.growth/metrics.md` is a centralized time-series log of account-level metrics across all platforms. It provides a single place to see growth over time without digging through individual monthly reports.

### Format

```markdown
# Metrics History

Centralized log of account-level metrics across all platforms. Updated during performance analysis or via "Log Metrics" action.

## Entries

### {YYYY-MM-DD}

**Source:** {Performance Analysis / Manual Log / Chrome Browser}

| Platform | Followers | Following | Posts | Avg Engagement Rate | Notes |
|----------|-----------|-----------|-------|-------------------|-------|
| Instagram | {count} | {count} | {count} | {rate}% | {any notable changes} |
| X/Twitter | {count} | {count} | {count} | {rate}% | |
| LinkedIn | {count} | {count} | {count} | {rate}% | |
| TikTok | {count} | {count} | {count} | {rate}% | |
| YouTube | {count} | {count} | {count} | {rate}% | |
| Facebook | {count} | {count} | {count} | {rate}% | |

**Period highlights:** {brief note on what happened since last entry — e.g., "Viral reel gained 2.3K followers", "Steady organic growth", "Launched on TikTok"}

---
```

### Rules

- New entries are **prepended** (newest first) so the most recent data is always at the top
- Only include platforms the brand is active on (check `.growth/brand-profile.md`)
- If exact engagement rate isn't available, note "N/A" rather than guessing
- The "Notes" column captures anything notable: follower spikes/drops, platform changes, viral posts, etc.
- "Period highlights" gives quick context for what drove the numbers

### Standalone "Log Metrics" Flow

When the user selects "Log Metrics" from the Analysis & Data menu:

1. Read `.growth/brand-profile.md` to get the list of active platforms and handles
2. Ask the user how they want to provide the data:
   - **Manual input** — they'll type/dictate the numbers
   - **Chrome browser** — if they're logged into their social accounts, use Chrome browser automation to visit each profile and extract current follower counts and other visible metrics
   - **Screenshots** — they'll provide screenshots of their profile pages or analytics dashboards
3. Collect the metrics for each active platform
4. Read `.growth/metrics.md` (or create it if first time)
5. Prepend a new entry with today's date and all collected metrics
6. If previous entries exist, calculate and display the change since last entry:
   - Follower growth (absolute and %)
   - Engagement rate change
   - Any notable shifts
7. Present a brief summary to the user showing their growth trajectory

## First-Time Analysis (No Historical Data)

If this is the first performance analysis for the brand:
1. Establish baselines — these numbers ARE the baseline, not compared to anything
2. Focus on identifying initial patterns rather than trends
3. Set benchmarks for next month's comparison
4. Note the starting point for all key metrics
5. Suggest 2-3 experiments for the next month based on initial data
