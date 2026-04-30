# I audited 100 of the most well-known AI agent companies. Almost none of them are discoverable to other agents.

> Headline numbers (full data in [`/data/results.csv`](../data/results.csv)):
>
> - **Average score: 6.3 / 100**
> - **99 of 100** projects fall in the "Mostly invisible" tier (≤39/100)
> - **1 of 100** crosses 40 points: Tavily, at 50/100
> - **0 of 100** have machine-readable pricing
> - **0 of 100** publish a UCP manifest
> - **1 of 100** publishes an A2A `agent-card.json`
> - **1 of 100** publishes an `ai-agent.json` manifest
> - **48 of 100** publish `llms.txt` — the only standard with measurable adoption, and it's a *human-SEO* artifact, not an agent-commerce one

## What was audited

A 10-item checklist covering the public files an autonomous agent would actually look for before deciding whether to read, transact with, or hand work off to another agent:

| # | Check | Points |
|---|---|---|
| 1 | `/llms.txt` | 10 |
| 2 | `/skill.md` | 10 |
| 3 | `/.well-known/ai-agent.json` (or legacy `agent.json`) | 15 |
| 4 | `/.well-known/agent-card.json` (A2A) | 15 |
| 5 | `/.well-known/ucp/manifest.json` (UCP) | 10 |
| 6 | OpenAPI auto-discoverable at root | 10 |
| 7 | Named capabilities with descriptions | 10 |
| 8 | Input/output schemas | 10 |
| 9 | Machine-readable pricing | 5 |
| 10 | Contact + auth + rate-limit declared | 5 |

Public files only. 1 request per second per host. 10s timeout, one retry on transient failure. Identifying User-Agent. Full method: [`/checklist/audit-checklist.md`](../checklist/audit-checklist.md). Scanner code: [`/scanner/scanner.py`](../scanner/scanner.py).

## Targets

100 projects spanning agent frameworks (LangChain, LlamaIndex, CrewAI, AutoGen, Mastra, Pydantic AI, BeeAI, CamelAI, LangGraph), agent products (Devin, Lindy, MultiOn, Adept, Cursor, Replit, Bolt.new, Lovable, Manus, v0, Sweep, Open Interpreter, Aider, Anthropic Computer Use), platforms (Voiceflow, Stack AI, Vellum, Dify, n8n, Botpress, Langflow, Flowise), memory layers (Mem0, Letta, Zep), observability (Helicone, LangSmith, AgentOps, Langfuse, Phoenix, Athina, Patronus), browser tools (Browser Use, BrowserBase, Stagehand, AgentQL, Hyperbrowser, ScrapeGraphAI), search APIs (Tavily, Exa, SerpAPI), voice agents (Vapi, Bland.ai, Retell, Synthflow), sales agents (11x, Ema), customer-support agents (Decagon, Sierra, Ada, Maven AGI, Forethought), enterprise search (Glean, Hebbia), MCP registries (mcp.so, Smithery, Pulse MCP), agent-economy infrastructure (Agentic.Market, Fetch.ai Agentverse, Nevermined, A2A Registry, Moltbook), crypto-agent projects (Olas, Virtuals, Story, ElizaOS, Bittensor, SingularityNET, Ocean, Theoriq, ChainGPT, Fetch.ai), and inference infra (HuggingFace, Together AI, Replicate, Hyperbolic, Modal, E2B, Continue, Cline).

Full list: [`/data/targets.csv`](../data/targets.csv).

## Results

### Score distribution

| Bucket | Count |
|---|---|
| 0 | 50 |
| 1–19 | 41 |
| 20–39 | 8 |
| 40–59 | 1 |
| 60–79 | 0 |
| 80+ | 0 |

Half the field scored zero. Ninety-one percent scored ≤19. The single project that crossed 40 was Tavily, at 50.

### Per-check pass rates

| Check | Pass rate |
|---|---|
| `llms.txt` | **48%** |
| `skill.md` | 9% |
| `ai-agent.json` | **1%** |
| A2A `agent-card.json` | **1%** |
| UCP manifest | **0%** |
| OpenAPI auto-discoverable | 1% |
| Capability clarity | 1% |
| I/O schemas | 1% |
| Pricing metadata | **0%** |
| Contact + auth + rate-limit | **0%** |

The story is in the gap between checks 1 and 2. `llms.txt` — a standard primarily promoted as a way for ChatGPT and Claude to cite your site — has cleared 48% adoption. Every other standard, including the ones designed *specifically* for agent-to-agent discovery and commerce, is in the low single digits or at zero.

### Top 10 scorers

| Score | Project | Category |
|---|---|---|
| 50 | **Tavily** | tools (search API) |
| 30 | **Agentic.Market** | marketplace (x402) |
| 20 | SuperAGI | framework |
| 20 | Fixie | platform |
| 20 | LangSmith | observability |
| 20 | A2A Registry | registry |
| 20 | Bolt.new | product |
| 20 | mcp.so | registry |
| 20 | BrowserBase | tools |
| 10 | (14-way tie) | various |

### Category averages

| Category | n | Avg score |
|---|---|---|
| marketplace | 2 | 15.0 |
| registry | 4 | 15.0 |
| tools | 10 | 12.0 |
| infra | 5 | 10.0 |
| platform | 8 | 7.5 |
| voice | 4 | 7.5 |
| observability | 7 | 7.1 |
| memory | 3 | 6.7 |
| support | 3 | 6.7 |
| framework | 13 | 4.6 |
| product | 27 | 3.3 |
| **crypto-agent** | **10** | **2.0** |
| **payments** | **1** | **0.0** |

The most striking line in this table is the bottom three. Crypto-agent projects — the cohort that has spent the last 18 months loudly insisting that AI agents will transact onchain with each other — score worse than the human-facing customer-support category. The single agent-payments infrastructure project audited (Nevermined) scored zero.

## Notable cases

### The single outlier: Tavily (50/100)

Tavily, a search API marketed explicitly for AI agents, is the only project in the 100 that publishes both an `ai-agent.json` (at the legacy `/.well-known/agent.json` path) and an A2A `agent-card.json`. The card declares 5 named skills (`web-search`, `content-extract`, `web-crawl`, `site-map`, `deep-research`), each with descriptions and examples. They cover both legacy and current well-known paths — a small detail that suggests someone actually thought about it.

They still don't have machine-readable pricing or a complete contact/auth/rate-limit declaration. The 50 ceiling is real.

### The Coinbase entry: Agentic.Market (30/100)

Agentic.Market's `llms.txt` reads like a vending-machine manual: *"Browse and call x402-enabled services — no API keys, no accounts, pay per request."* It exposes a 600+ service catalog over a documented HTTP API. It is the only project of the 100 whose public surface is built around the assumption that the reader is a wallet-equipped agent, not a human evaluating a SaaS.

It still scored 30 because it doesn't publish an `ai-agent.json` or A2A card. The deeper reason is probably that Agentic.Market is itself the *registry*; it doesn't need to advertise on standards designed to point at registries.

### The standard-setting registry that doesn't implement its own standard

A2A Registry's stated purpose is to index live A2A-compliant agents. Its own root domain scored 20/100 and does not publish an `agent-card.json` at the well-known path. It indexes a standard it does not, at the time of this audit, implement.

### The social network that bots can't read

Moltbook — *"a social network for AI agents"* — scored 10/100. It publishes a `skill.md` describing how human developers can integrate Moltbook identity into their own apps; it does not publish anything an autonomous agent could parse to decide whether and how to engage with the platform itself.

### The famous frameworks at zero

LangChain (0/100), LlamaIndex (0/100), CrewAI (0/100), AutoGen (0/100), HuggingFace (0/100), Anthropic's own marketing site (0/100). The four most-cited names in agent development, plus the largest model hub, plus the company that authored MCP, all scored zero against agent-native discoverability checks. These are the population *most* invested in the agent ecosystem; they have done the least, on their public domains, to make their own products legible to it.

### The crypto-agent paradox

Bittensor, SingularityNET, Ocean Protocol, Story Protocol, Virtuals Protocol, Theoriq, ChainGPT, ElizaOS, Olas/Autonolas, Fetch.ai — the crypto-agent cohort averages 2.0/100. Of ten projects, eight scored 0 and two scored 10. Not one publishes anything an agent could read to decide whether to pay it. The marketing thesis these projects sell is the same thesis our checklist tests for. The marketing thesis and the public surface are not in the same room.

## Interpretation

The cleanest way to read this dataset:

> **The standards exist. The adoption does not. The category that *should* lead — agent infrastructure for agent customers — is barely distinguishable from the category that *shouldn't have to* — chatbot products selling to humans.**

A more careful reading: the only standard with adoption (`llms.txt`, 48%) is the one that pays off in *human* search behavior — it makes ChatGPT and Claude cite your site. The standards that pay off in *agent* commerce — `ai-agent.json`, A2A `agent-card.json`, UCP, machine-readable pricing — pay off only when there are agents on the other end with budgets, and there aren't, yet, in any volume. Adoption is following economic gravity, not standards-body wishful thinking.

Two implications:

1. **Agent-native commerce is real on paper, not in production.** The `0%` machine-readable-pricing rate is the most damning number in the report. No autonomous agent can decide to pay any of these companies without a human in the loop, because none of them have published a price an agent could parse.

2. **There is a real, measurable gap between the projects that *say* they are agent infrastructure and the public surface they actually present.** This is not unique to AI — it happened with mobile in 2010 and APIs in 2007. The question is whether the gap closes from the standard side (more `ai-agent.json` adoption) or from the integration side (frameworks like LangChain shipping `agent-card.json` generators by default in their `langchain new` template).

## Limitations

- One-time, unauthenticated HTTP fetch from each project's root domain. Some agent manifests may live on subdomains or behind authenticated paths we did not test.
- Some audited projects (e.g., AutoGen on github.io) are documentation hosts for libraries; the library itself is not a deployed agent. Penalizing them for not publishing manifests at their docs root is fair only insofar as those docs are how the project advertises itself to the world.
- "Machine-readable pricing" was scored only when present in a structured manifest field (`pricing`, `price`, etc.). Projects that publish prices on a human-readable `/pricing` page were not credited.
- Ten-second timeout, single retry. A handful of network failures may have cost a check or two; the underlying signal — that 91% scored ≤19 — is not sensitive to single-check noise.
- The audit is a snapshot from late April 2026. We expect this number to look meaningfully different in 6–12 months. We will rerun the audit at that point.

## What this means for builders

If you ship an agent-facing product or piece of infrastructure, the cheapest credibility move you can make in 2026 is:

1. Add `/llms.txt`. Most of you already have. The other half: it's a 10-line file. Today.
2. Add `/.well-known/ai-agent.json` with `name`, `description`, `capabilities`, `pricing`, `contact`. The Aiia spec at [aiia.ro/spec/ai-agent-json](https://aiia.ro/spec/ai-agent-json/) is a 5-minute read.
3. Add `/.well-known/agent-card.json` if you advertise yourself as A2A-compatible. Currently: 1 of 100 audited projects do. If you do, you are immediately top decile.
4. Publish prices in machine-readable form. Currently: 0 of 100. If you do, you are unique.

You will not get marketing lift from this in 2026. You will, plausibly, get a measurable edge in 2027 when agent-driven traffic becomes a non-zero fraction of B2B API calls.

## Want to know if this becomes a tool?

I'm running a 14-day test to see if anyone actually wants a tool that fixes the missing manifest files and submits agents to the major registries. If that would be useful to you, drop your email: **[tally.so/r/yP0KaB](https://tally.so/r/yP0KaB)**. I'll only email you if it ships. No newsletter, no spam.

If you don't want to share an email but want to vote with a star, that also works: [⭐ this repo](https://github.com/omskykhal/agent-discoverability-audit-2026).

## Reproducing

The full dataset, scanner, and methodology are in this repository under MIT (code) and CC BY 4.0 (data, reports). To run the audit on your own URL:

```bash
git clone https://github.com/omskykhal/agent-discoverability-audit-2026
cd agent-discoverability-audit-2026
python scanner/scanner.py
```

Edit `data/targets.csv` to add or remove targets. Re-run.

To dispute a score: open an issue with the URL and the specific check you believe was misclassified. We will recheck and update.

## Contact

- Issues / corrections: https://github.com/omskykhal/agent-discoverability-audit-2026/issues
- Author: [@omskykhal](https://github.com/omskykhal)
