# Show HN submission — copy/paste ready

## Title (max 80 chars; current 74)

```
Show HN: I audited 100 AI agent companies. Almost none are agent-discoverable
```

**Alternative titles** (in case the above feels too pointed):

- `Show HN: 100-AI-agent audit – 99 of 100 fail agent-readability checks` (66 chars)
- `Show HN: An open audit of 100 AI agent projects' machine-readability` (70 chars)
- `Show HN: Most AI agent companies aren't readable by AI agents` (60 chars)

## URL field

```
https://github.com/omskykhal/agent-discoverability-audit-2026
```

(Link directly to the repo; HN treats the repo README as the canonical landing page. Do not also paste the repo URL into the text body — HN penalizes duplicates.)

## Text body (HN limit ~2000 chars; current ~1800)

```
I'm not a developer. I went down the rabbit hole of "can I sell things to AI agents instead of humans" and ran into a basic question: how does one agent even find another? There are at least four competing standards (llms.txt, /.well-known/ai-agent.json, A2A agent-card.json, UCP manifest) and almost no public data on adoption.

So I ran a single-pass HTTP audit against 100 of the most-cited AI agent companies, frameworks, marketplaces, and registries. 10 checks per target, 100 points possible. Polite crawler, public files only, 1 req/sec per host, identifying UA. Code, data, methodology all in the repo.

Headline numbers:
- Average score: 6.3 / 100
- 99 / 100 fall in the "Mostly invisible" tier (≤39)
- 1 / 100 crosses 40 points: Tavily, at 50
- 0 / 100 publish machine-readable pricing
- 1 / 100 publish an A2A agent-card.json (Tavily again)
- 0 / 100 publish a UCP manifest
- 48 / 100 have llms.txt — the only standard with real adoption, and it's a human-SEO artifact

Some specific findings I didn't expect:
- LangChain, LlamaIndex, CrewAI, AutoGen, HuggingFace, Anthropic's marketing site: all 0/100
- A2A Registry — whose entire purpose is to index A2A-compliant agents — does not publish an agent-card.json itself
- Moltbook, "a social network for AI agents," scored 10/100
- Crypto-agent projects (Bittensor, Olas, Virtuals, Fetch.ai, etc., n=10) averaged 2.0/100. The cohort that has been loudest about agent-to-agent commerce has the worst public surface for it.
- The single 50-pointer (Tavily, a search API) is the only project to publish both /.well-known/agent.json AND /.well-known/agent-card.json

Limitations and what I'm not claiming: in the repo. Happy to be wrong on specifics — issue link in the README. The dataset is CC BY 4.0; rerun, dispute, fork.

What I want from this thread: corrections on specific scores, cases where the file lives at a non-standard path I missed, and your honest take on whether agent-discoverability is a real problem or a standards-body fantasy.
```

## Comment-response tone guide

You will get four kinds of comments. How to handle each:

### 1. "Your check for X is wrong, my project actually publishes Y at Z"

**Best response:**

> Thanks — that's exactly the kind of correction I wanted. Opening an issue at <repo>/issues with the URL and check number, and rescanning. If it's at a non-standard path, I'll add the path to the v0.2 fallback list.

Then *actually* open the issue, rescan that target, and post the corrected score in a follow-up comment. This converts a critic into the credibility for everyone else watching.

### 2. "This is meaningless — adoption is low because the standards are new"

**Best response:**

> Agreed; that's literally the point of the report. The standards are new, adoption is low, and there's an open question whether it ever gets high. The data is the snapshot, not the verdict. I'll rerun this in 6 months and we'll see if it moved.

Don't argue. The comment is right. The report's value is the *measurement*, not a normative claim.

### 3. "This is just llms.txt drama / SEO garbage"

**Best response:**

> Half the score (50 of 100 points) comes from non-llms.txt checks that target machine-to-machine commerce, not human SEO. The headline that llms.txt is the only standard with traction is a finding, not a thesis.

### 4. "You should build the tool to fix this"

**Best response:**

> That's the test I'm running with this post. If a critical mass of people ask, I'll build it. If they don't, I won't. Drop your email here and I'll ping you only if it ships: https://tally.so/r/yP0KaB?source=hn

This is the conversion moment. Waitlist URL is live. Use the `?source=hn` parameter so HN-driven sign-ups can be tracked separately.

## Timing

Best HN performance windows for technical content (Pacific Time):
- **Tuesday or Wednesday, 8:00–10:00 AM PT** — strongest historical engagement
- Avoid Friday afternoon, weekends, US holidays, and any day a major platform (OpenAI/Anthropic/Google) ships news

If submitted at the right window and the title clicks, expect first hour to determine whether it makes the front page. Be at the keyboard for the first 60 minutes after submission to respond to early comments.

## Single rule

**Do not edit the post after submission.** HN will mark it "edited" and some moderators downvote edits. If you spot an error, post a follow-up comment correcting yourself.
