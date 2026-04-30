# Agent Discoverability Audit Checklist (v0.1)

A 10-item, 100-point rubric for assessing whether an AI agent project can be discovered, parsed, and transacted with by *other* AI agents.

All checks operate on **publicly served files only** (well-known paths, root-level standard files, public docs). No authentication, no scraping behind login walls.

## Checks

| # | Item | Path / Source | Points | Pass criterion |
|---|---|---|---|---|
| 1 | `llms.txt` exists | `/llms.txt` | 10 | HTTP 200, `text/plain` or `text/markdown`, > 0 bytes |
| 2 | `skill.md` exists | `/skill.md` | 10 | HTTP 200, markdown, contains at least one fenced code or example block |
| 3 | AI agent manifest | `/.well-known/ai-agent.json` | 15 | HTTP 200, valid JSON, has `name` and `description` |
| 4 | A2A agent card | `/.well-known/agent-card.json` | 15 | HTTP 200, valid JSON, has `name` and at least one `skill` or `capability` |
| 5 | UCP manifest | `/.well-known/ucp/manifest.json` (also accept `/.well-known/ucp`) | 10 | HTTP 200, valid JSON, has required UCP fields |
| 6 | OpenAPI / Swagger doc | `/openapi.json`, `/openapi.yaml`, `/swagger.json`, `/api-docs`, or linked from homepage | 10 | HTTP 200, parseable as OpenAPI 3.x |
| 7 | Capability description clarity | Any of: agent-card.json `skills[]`, ai-agent.json `capabilities[]`, skill.md sections | 10 | At least 3 named capabilities with one-line descriptions |
| 8 | Input/output schema | Any of: OpenAPI schemas, agent-card.json `inputSchema`/`outputSchema`, MCP tool definitions | 10 | At least one endpoint with both input and output schemas defined |
| 9 | Pricing / payment metadata | Any of: ai-agent.json `pricing`, x402 `402 Payment Required` advertisement, public pricing page in machine-readable form | 5 | Pricing exists in any machine-parseable form |
| 10 | Contact / auth / rate-limit info | Any of: ai-agent.json `contact` / `auth`, OpenAPI `securitySchemes`, public rate-limit doc | 5 | Auth method named AND contact channel named AND rate limit stated |

**Total: 100 points**

## Score → Tier

| Score | Tier | Interpretation |
|---|---|---|
| 80 – 100 | **Agent-discoverable** | Another agent can find, understand, and transact with this one autonomously |
| 60 – 79 | **Partially ready** | Discoverable but missing structured payment or schema info |
| 40 – 59 | **Weakly discoverable** | Has *some* metadata; another agent would need human-style scraping |
| 0 – 39 | **Mostly invisible** | No standard discovery files; effectively human-only |

## Methodology rules (to keep the audit honest)

1. Single fetch per check, 10-second timeout.
2. User-Agent: `AgentDiscoverabilityAudit/0.1 (+https://github.com/<TBD>/agent-discoverability-audit-2026)` — identifies the bot, gives a contact path.
3. Respect `robots.txt` for the well-known paths (most allow them by default).
4. 1 request per second per host. No parallel hammering.
5. Each check records: URL fetched, HTTP status, response time (ms), bytes, pass/fail, raw error if any.
6. If the project is a GitHub-only repo with no live host → mark all hosted-file checks as N/A and exclude from percentile stats; report separately.
7. Re-test failures once after a 30-second cooldown before recording a fail (transient errors).

## Out-of-scope for v0.1

- Quality of capability descriptions (only existence is checked)
- Schema correctness depth (only presence, not validation against MCP/A2A spec)
- Live API actually responding to a real call
- Trust / reputation signals
- Crypto wallet readiness

These are candidates for v0.2 if the v0.1 audit lands.

## Open questions to resolve before D2 (scanner build)

1. Should `agent.json` (without `ai-` prefix, the older Anthropic convention) be accepted as a fallback for check #3? → tentative YES, log which variant was found.
2. For check #4, should we also accept the legacy `/.well-known/agent.json` A2A path? → tentative YES, with a `legacy_path: true` flag.
3. How to handle projects that publish their manifest under a subpath (e.g. `/agent/.well-known/...`)? → for v0.1, only check root `/.well-known/`. Note as limitation.
