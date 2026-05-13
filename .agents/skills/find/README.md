# find

Skill discovery and workflow router for the full marketing toolkit.

## What it does

Maps any marketing goal — vague or specific — to the right skill(s) in the right order. Covers all 40+ installed skills. Returns a direct recommendation, not a list of possibilities.

Use it when you don't know which skill to reach for, or when your goal spans multiple skills and you need a sequenced workflow.

## How to invoke

```
/find                             # describe your goal after invoking
/find I want to grow signups
/find how do I launch a new feature
/find what skill should I use for my landing page
/find I need to run Google Ads
```

## What you get back

- **Single-skill match** — one clear recommendation with the invocation command
- **Multi-skill workflow** — ordered sequence of skills with why each step matters
- **Quick-match** — instant routing when the goal maps to an obvious skill

## Example

**You:** `/find I want to run Google Ads for my SaaS product`

**Claude:**
> ## Recommended Skill: `paid-ads`
> Best fit for campaign structure, targeting, and budget strategy.
>
> **Invoke it with:** `/paid-ads`
>
> ## Supporting Skills
> - `/ad-creative` — generate all headline and description variations
> - `/page-cro` — optimize the page your ads land on
> - `/ab-test-setup` — design a valid creative test
> - `/analytics-tracking` — attribution and reporting

## See also

- [`SKILL.md`](./SKILL.md) — full LLM-facing instructions and skill catalog
