# Hypothesis

## The single hypothesis we are testing

> **AI agent developers experience their agents being undiscoverable to other agents as a real, painful problem — painful enough that they would adopt a tool to fix it.**

## Why this hypothesis matters

If TRUE → there is a market for an "agent discoverability" toolchain (audit, manifest generation, registry submission automation).

If FALSE → the problem exists only in our heads. We move on without burning months on a product no one wants.

## How we will test it

A single public artifact, published once, measured for 7 days:

1. Audit ~100 publicly-listed AI agent projects against a 10-item discoverability checklist.
2. Publish the raw dataset, scanner code, and findings as an open GitHub repository.
3. Write up the findings as one blog post / Show HN submission with the headline: *"I audited 100 AI agent projects. Most are invisible to other agents."*
4. Watch the response.

Total budget: 18 hours of work over 7 days. $0 cash.

## D14 Go / No-Go gate

Measured 14 days after the GitHub repo + blog post go public.

| Signal | Go threshold |
|---|---|
| GitHub stars on the audit repo | ≥ 30 |
| Email waitlist sign-ups (single-field form on the post) | ≥ 20 |
| Inbound DM / comment of the form *"if you build this as a tool, I'd use it"* | ≥ 1 |

**Decision rule:** ≥ 2 of 3 signals met → proceed to product MVP. ≤ 1 signal met → archive the repo as a portfolio piece, return to ideation.

## What we are explicitly NOT doing during this validation

- Buying a domain
- Picking a product name
- Writing any backend / SaaS code
- Setting up payments
- Touching crypto, x402, USDC, or any agent-economy plumbing
- Promising a launch date

These all wait until the gate is passed.

## Honest priors

- P(GitHub ≥ 30 stars) ≈ 35%
- P(≥ 20 email sign-ups) ≈ 25%
- P(≥ 1 strong inbound interest message) ≈ 40%
- P(2 of 3 signals → Go) ≈ 25–30%

A failed test is a successful test. Either outcome saves months.
