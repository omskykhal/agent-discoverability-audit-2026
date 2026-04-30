# X (Twitter) thread — copy/paste ready

7-tweet thread. Each tweet is under 280 chars. Post them as a reply chain (not separate tweets).

**Posting**: paste tweet 1, post. Click "Add another tweet" or reply to your own post with tweet 2. Continue.

**Best timing**: Tuesday or Wednesday, 9–11 AM Eastern Time (matches the US tech-Twitter window). Avoid Mondays (low engagement) and Fridays after noon (everyone's checked out).

---

## 1/7 — Hook

```
I audited 100 of the most well-known AI agent companies for one thing: are they discoverable to *other* AI agents?

99 of 100 failed.

Here's the data, the methodology, and the part nobody is talking about. 🧵
```

(258 chars)

---

## 2/7 — The setup

```
The premise is simple. If agents are going to transact with each other, they need to be able to find each other and parse what each other does.

There are at least 4 standards for this:
• llms.txt
• /.well-known/ai-agent.json
• A2A agent-card.json
• UCP manifest

Adoption?
```

(280 chars)

---

## 3/7 — The numbers

```
Average score across 100 projects: 6.3 / 100.

• 50 scored 0
• 91 scored ≤ 19
• 1 scored above 40 (Tavily, 50)

Per-check pass rates:
• llms.txt: 48%
• ai-agent.json: 1%
• A2A agent-card.json: 1%
• UCP: 0%
• machine-readable pricing: 0%
```

(279 chars)

---

## 4/7 — The punchline

```
The only standard with measurable adoption is llms.txt — the one promoted as "make ChatGPT cite your site."

The standards designed for *agent-to-agent commerce* sit at 0–1%.

Adoption is following human SEO incentives. Not agent-economy incentives.
```

(257 chars)

---

## 5/7 — The receipts

```
0/100 scores from companies that should be most invested in this:

• LangChain
• LlamaIndex
• CrewAI
• AutoGen
• HuggingFace
• Anthropic's marketing site

A2A Registry — whose entire purpose is to index A2A-compliant agents — does not publish an agent-card.json itself.
```

(280 chars)

---

## 6/7 — The crypto-agent cohort

```
The most surprising finding: crypto-agent projects (n=10, including Bittensor, Olas, Virtuals, Fetch.ai, ElizaOS) averaged 2.0/100.

The category that has been loudest about agents transacting onchain has the worst public surface for an agent to actually do that.
```

(270 chars)

---

## 7/7 — The repo + waitlist

```
Full data, scanner code, methodology:
github.com/omskykhal/agent-discoverability-audit-2026

If a tool to fix the missing files + auto-submit to registries would be useful: tally.so/r/yP0KaB?source=twitter

Code MIT, data CC BY 4.0. If you scored low and disagree, open an issue.
```

(279 chars)

---

## Optional follow-up tweets (post as separate replies to thread, NOT as part of the 7)

### Tweet 8 — engagement bait, post 30 min after thread

```
The single 50-pointer was Tavily — a search API.

Search APIs are the one category that *already* knows agents are reading them. Their incentives are aligned today.

Most other categories' incentives kick in only when agent-driven traffic becomes a non-zero fraction of B2B API calls.
```

### Tweet 9 — for replies asking "so what?"

```
Two implications worth thinking about:

1. Agent-native commerce is real on paper, not in production. 0/100 publish prices an agent could parse.
2. Frameworks (LangChain et al.) shipping agent-card.json templates by default would close most of this gap in a quarter.
```

---

## Tagging strategy

**Don't @ companies in the main thread.** It reads as picking a fight and the algorithm de-amplifies.

**Do @ them in replies if questioned**, e.g., if someone asks "what does LangChain say?" — then it's organic to tag @LangChainAI.

**Do tag** the standards-body / spec authors in tweet 7's reply, as a courtesy:
- @aiia_ro (ai-agent.json)
- @googlecloud (A2A)
- (no UCP author handle is widely known)

This signals you respect the work even while measuring its uptake.

---

## What to do if it goes viral

| Threshold | Action |
|---|---|
| 100+ likes in first hour | Pin to profile. Reply to every quote-tweet within 30 min. |
| 1k+ likes | Add a follow-up tweet at 24h: "Update: ran the scanner on N more requested URLs since posting. Results: …" — keeps thread alive |
| Tech press DMs | Reply within 4 hours. Direct them to the GitHub repo, not your personal email. |
| Hostile quote-tweet from a company you scored low | Do NOT escalate. Reply once, calmly, with the URL/check that produced the score and an offer to rescan. Then disengage. |

---

## What to do if it dies (most likely outcome)

Most threads don't take off. If yours doesn't:

1. Do not delete it. Threads sometimes get rediscovered weeks later.
2. Do not repost the same thread under a different framing within 30 days.
3. Wait for a relevant news event (a new spec release, a major framework adding agent-card support, etc.) and reply to *that* news with a link to your data. Newsjacking has a 10x higher hit rate than fresh threads.
