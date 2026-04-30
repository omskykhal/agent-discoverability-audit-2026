# Reddit submissions — copy/paste ready

## Where to post

Submit in **this order, with at least 24 hours between**. Do not cross-post simultaneously — most subs flag that as spam.

| Order | Subreddit | Why | Self-promo rules |
|---|---|---|---|
| 1 | r/LocalLLaMA | High-signal AI dev audience, receptive to data + open source | Must contribute, not pitch. OK if frame is data/findings. |
| 2 | r/MachineLearning | Stricter; demands rigor. Use `[D]` Discussion flair, not `[N]` News | No self-promo at all. Frame as discussion of standards landscape. |
| 3 | r/AI_Agents | Smaller, friendlier, fewer karma requirements | Self-promo allowed when accompanied by data |
| 4 | r/programming | High volume, low signal. Last because biggest variance | OK if technical |

## r/LocalLLaMA submission

### Title (Reddit limit 300 chars; below is 96)

```
I audited 100 AI agent companies' websites for "agent-discoverability". 99 of 100 fail. Open dataset.
```

### Flair

`Discussion` (or `Resources` if available)

### Body

```
TL;DR I ran a 10-item, 100-point HTTP audit against 100 of the most-cited AI agent companies, frameworks, marketplaces, and registries to see how machine-readable their public surfaces are to *other* AI agents. Average score: 6.3/100. Only 1 project (Tavily, 50/100) crossed 40. Repo with code, data, full methodology: https://github.com/omskykhal/agent-discoverability-audit-2026

**What I checked**

10 public files / metadata fields an autonomous agent might look for:

- `/llms.txt`, `/skill.md`
- `/.well-known/ai-agent.json`, `/.well-known/agent-card.json` (A2A), `/.well-known/ucp/manifest.json`
- Auto-discoverable OpenAPI
- Named capabilities with descriptions
- Input/output schemas
- Machine-readable pricing
- Contact + auth + rate-limit declared

**Headline numbers**

- 99/100 in "Mostly invisible" tier (≤39)
- 50/100 scored exactly 0
- 48/100 publish llms.txt — the *only* standard with adoption
- 1/100 publishes A2A `agent-card.json` (Tavily)
- 1/100 publishes `ai-agent.json` (Tavily)
- 0/100 publish UCP manifest
- 0/100 publish machine-readable pricing
- 0/100 declare contact + auth + rate-limit at the standard fields

**Some specific results that surprised me**

- LangChain, LlamaIndex, CrewAI, AutoGen, HuggingFace: all 0/100
- A2A Registry — whose stated purpose is to index A2A-compliant agents — does not publish an agent-card.json
- Crypto-agent cohort (n=10: Bittensor, Olas, Virtuals, ElizaOS, Fetch.ai, etc.) averaged 2.0/100. The category most aggressively marketing agent-to-agent commerce has the worst surface for it.
- The single 50-pointer is a search API (Tavily), the one company in the dataset that *sells data to agents* and clearly knows agents are reading

**What I'm not claiming**

- That low adoption is bad. There may be no economic pressure to adopt yet.
- That my checklist is the right one. Suggestions welcome — issue link in the repo.
- That this proves anything about underlying capability. It only measures what's at the public root domain.

**What I'm asking**

1. Run the scanner on your own URL and tell me where the score is wrong.
2. Tell me what you think the *actual* problem is — if any.
3. Specifically: does anyone here actually need their agent to be discoverable to other agents *today*? Or is this all theater for 2027?

If a tool that fixes the missing manifest files and submits to the major registries would be useful to you, I'm collecting interest here: https://tally.so/r/yP0KaB?source=reddit (no newsletter, ping only if it ships).

Code MIT, data CC BY 4.0. Reproduce, dispute, fork.
```

## r/MachineLearning submission

### Title

```
[D] Audit of 100 AI agent projects' adherence to agent-discoverability standards (llms.txt, ai-agent.json, A2A agent-card.json, UCP). 99/100 score below 40.
```

### Flair

`[D] Discussion`

### Body

Use the same body as r/LocalLLaMA, but **strip the calls to action** at the bottom (no "tell me what you think", no "if you'd pay for this"). r/ML is allergic to anything that looks promotional. Replace the "What I'm asking" section with:

```
**Open questions for discussion**

1. Is the right adoption-measurement frame "manifest exists at well-known path" or something else (e.g., presence of MCP server, OpenAPI completeness, tool-use compatibility tests)?
2. The crypto-agent cohort underperforming is the most surprising finding for me. Is this a measurement artifact (their agents live elsewhere, e.g., on-chain or in agent registries, not at the marketing domain) or a real gap?
3. The Aiia ai-agent.json spec, the A2A agent-card.json, and Anthropic's MCP server descriptors all overlap. Is convergence likely, or do we live with three+ standards indefinitely?
```

## r/AI_Agents submission

Same as r/LocalLLaMA. Smaller community, more personal tone OK.

## Cross-platform rules

- Wait at least 24 hours between subreddits
- Do not link from one Reddit thread to another (auto-removed by some bots)
- Do not link to your HN submission from Reddit, or vice versa, in the body — it reads as karma manipulation. If asked in comments, post the link there.
- If a mod removes your post, do not resubmit. Message the mod once politely; if no response in 48h, move on.

## Engagement window

The first **2 hours** after submission determine the post's fate on Reddit. Be at the keyboard. Reply to every comment in those 2 hours, even one-line ones, even hostile ones (especially hostile ones — measured replies to hostility convert lurkers).

## What success looks like

| Sub | "It worked" threshold |
|---|---|
| r/LocalLLaMA | 100+ upvotes, 30+ comments |
| r/MachineLearning | 50+ upvotes, 15+ comments (high bar) |
| r/AI_Agents | 30+ upvotes, 10+ comments |
| r/programming | Variable; aim for 50+ |
