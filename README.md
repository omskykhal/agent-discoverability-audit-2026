# agent-discoverability-audit-2026

> Auditing whether ~100 publicly-listed AI agent projects are actually discoverable by *other* agents.

## The hypothesis

**AI agent developers experience their agents being undiscoverable to other agents as a real, painful problem.**

This repository is the public artifact of a one-week test of that hypothesis. It contains the methodology, the raw dataset, the scanner code, and the findings — open for review, criticism, and reproduction.

See [`hypothesis.md`](./hypothesis.md) for the full statement and the Go/No-Go gate.

## What we measure

Each target is scored 0–100 against a 10-item checklist covering the public discoverability standards an autonomous agent would actually look for:

- `llms.txt`, `skill.md`
- `/.well-known/ai-agent.json`, `/.well-known/agent-card.json` (A2A)
- `/.well-known/ucp/manifest.json` (UCP)
- OpenAPI / Swagger documentation
- Capability descriptions, input/output schemas
- Pricing / payment metadata
- Contact, auth, and rate-limit information

Full rubric: [`checklist/audit-checklist.md`](./checklist/audit-checklist.md).

## Status

| Phase | Status |
|---|---|
| D1 — Hypothesis, checklist, target seed list | done |
| D2 — Scanner script | pending |
| D3 — Run audit on ~100 targets | pending |
| D4 — Deep-dive 20 cases | pending |
| D5 — Findings write-up | pending |
| D6 — Repo cleanup, dataset publish | pending |
| D7 — Public release (Show HN, Reddit, X) | pending |

## How to read this repo

| Path | Contents |
|---|---|
| `hypothesis.md` | What we are testing and how we will decide we were wrong |
| `checklist/audit-checklist.md` | The 10-item, 100-point rubric |
| `data/targets.csv` | The list of audited projects (seed: 35) |
| `data/results.csv` | Per-target scoring output (populated D3) |
| `scanner/scanner.py` | The auditing script (built D2) |
| `reports/findings.md` | Human-readable analysis (written D5) |

## Methodology principles

1. Public files only — no scraping, no auth bypass, no rate-limit abuse.
2. Identifiable User-Agent with contact path.
3. 1 request per second per host.
4. Failures retried once after 30 seconds.
5. Raw data published alongside findings — anyone can reproduce or dispute the conclusions.

If you are listed in `targets.csv` and want to be removed, opted out, or notified before publication, open an issue at https://github.com/omskykhal/agent-discoverability-audit-2026/issues.

## License

- Code: [MIT](./LICENSE)
- Data and reports: [CC BY 4.0](./LICENSE-DATA)

## Contributing

This is a one-week solo audit, not a long-running project. PRs adding more target URLs or fixing scanner bugs are welcome until the report is published. After publication the repo will be maintained as a reference dataset only.
