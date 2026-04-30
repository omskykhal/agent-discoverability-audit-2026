"""
Agent Discoverability Audit Scanner v0.1

Reads targets from ../data/targets.csv and runs the 10-item checklist
defined in ../checklist/audit-checklist.md against each target.

Output:
  ../data/results.csv     — flat per-target scoring (one row per target)
  ../data/results.json    — full nested results with per-check evidence

Polite crawling rules:
  - 10s timeout per request
  - 1 request per second per host
  - One retry after 30s on transient failure (5xx, timeout)
  - Identifying User-Agent with contact path
  - Public files only (well-known paths, root standard files)
"""

from __future__ import annotations

import csv
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urljoin

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

USER_AGENT = (
    "AgentDiscoverabilityAudit/0.1 "
    "(+https://github.com/omskykhal/agent-discoverability-audit-2026)"
)
TIMEOUT_SECS = 10
RETRY_DELAY_SECS = 30
PER_HOST_DELAY_SECS = 1.0

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGETS_CSV = REPO_ROOT / "data" / "targets.csv"
RESULTS_CSV = REPO_ROOT / "data" / "results.csv"
RESULTS_JSON = REPO_ROOT / "data" / "results.json"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

# host -> last-fetch-monotonic-time (for per-host rate limiting)
_LAST_FETCH: dict[str, float] = {}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    check_id: int
    name: str
    points_max: int
    points_awarded: int
    passed: bool
    url_attempted: str
    http_status: int | None = None
    response_time_ms: int | None = None
    bytes_received: int | None = None
    notes: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class TargetResult:
    id: int
    name: str
    url: str
    category: str
    total_score: int
    tier: str
    checks: list[CheckResult] = field(default_factory=list)
    error: str | None = None


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _polite_get(url: str, *, retry: bool = True) -> tuple[requests.Response | None, str | None]:
    """GET a URL with per-host rate limiting and one retry on transient errors.

    Returns (response_or_None, error_message_or_None).
    """
    host = urlparse(url).netloc
    now = time.monotonic()
    last = _LAST_FETCH.get(host, 0.0)
    wait = PER_HOST_DELAY_SECS - (now - last)
    if wait > 0:
        time.sleep(wait)

    try:
        resp = SESSION.get(url, timeout=TIMEOUT_SECS, allow_redirects=True)
        _LAST_FETCH[host] = time.monotonic()
        return resp, None
    except requests.RequestException as exc:
        _LAST_FETCH[host] = time.monotonic()
        if retry:
            time.sleep(RETRY_DELAY_SECS)
            return _polite_get(url, retry=False)
        return None, f"{type(exc).__name__}: {exc}"


def _try_paths(base_url: str, paths: list[str]) -> tuple[requests.Response | None, str, str | None]:
    """Try each path under base_url, return the first 2xx response.

    Returns (response_or_None, last_url_attempted, error_or_None).
    """
    last_err: str | None = None
    last_url = ""
    for p in paths:
        url = urljoin(base_url.rstrip("/") + "/", p.lstrip("/"))
        last_url = url
        resp, err = _polite_get(url)
        if resp is not None and 200 <= resp.status_code < 300:
            return resp, url, None
        if err is not None:
            last_err = err
    return None, last_url, last_err


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_llms_txt(base_url: str) -> CheckResult:
    url = urljoin(base_url.rstrip("/") + "/", "llms.txt")
    t0 = time.monotonic()
    resp, err = _polite_get(url)
    rt = int((time.monotonic() - t0) * 1000)

    if resp is None:
        return CheckResult(1, "llms.txt", 10, 0, False, url, None, rt, None,
                           f"network error: {err}")

    ct = resp.headers.get("content-type", "").lower()
    is_text = ct.startswith("text/") or "markdown" in ct or "plain" in ct
    body_len = len(resp.content or b"")
    passed = (
        resp.status_code == 200
        and (is_text or body_len > 0)
        and body_len > 0
    )
    return CheckResult(
        1, "llms.txt", 10, 10 if passed else 0, passed, url,
        resp.status_code, rt, body_len,
        f"content-type={ct or 'none'}, bytes={body_len}",
    )


def check_skill_md(base_url: str) -> CheckResult:
    url = urljoin(base_url.rstrip("/") + "/", "skill.md")
    t0 = time.monotonic()
    resp, err = _polite_get(url)
    rt = int((time.monotonic() - t0) * 1000)

    if resp is None:
        return CheckResult(2, "skill.md", 10, 0, False, url, None, rt, None,
                           f"network error: {err}")

    if resp.status_code != 200:
        return CheckResult(2, "skill.md", 10, 0, False, url,
                           resp.status_code, rt, len(resp.content or b""),
                           "not 200")

    body = resp.text
    has_block = ("```" in body) or ("    " in body and any(line.startswith("    ") for line in body.splitlines()))
    body_len = len(resp.content or b"")
    passed = body_len > 0 and has_block
    return CheckResult(
        2, "skill.md", 10, 10 if passed else 0, passed, url,
        resp.status_code, rt, body_len,
        f"has_code_block={has_block}, bytes={body_len}",
    )


def check_ai_agent_json(base_url: str) -> tuple[CheckResult, dict | None]:
    paths = ["/.well-known/ai-agent.json", "/.well-known/agent.json"]
    t0 = time.monotonic()
    resp, url, err = _try_paths(base_url, paths)
    rt = int((time.monotonic() - t0) * 1000)

    if resp is None:
        return (
            CheckResult(3, "ai-agent.json", 15, 0, False, url, None, rt, None,
                        f"all variants failed: {err}"),
            None,
        )

    try:
        data = resp.json()
    except ValueError:
        return (
            CheckResult(3, "ai-agent.json", 15, 0, False, url,
                        resp.status_code, rt, len(resp.content or b""),
                        "invalid JSON"),
            None,
        )

    if not isinstance(data, dict):
        return (
            CheckResult(3, "ai-agent.json", 15, 0, False, url,
                        resp.status_code, rt, len(resp.content or b""),
                        "JSON is not an object"),
            None,
        )

    has_name = bool(data.get("name"))
    has_desc = bool(data.get("description"))
    passed = has_name and has_desc
    return (
        CheckResult(
            3, "ai-agent.json", 15, 15 if passed else 0, passed, url,
            resp.status_code, rt, len(resp.content or b""),
            f"name={has_name}, description={has_desc}, variant={url.rsplit('/', 1)[-1]}",
            evidence={k: v for k, v in data.items() if k in
                      ("name", "description", "capabilities", "pricing", "contact",
                       "auth", "authentication", "endpoints", "skills")},
        ),
        data,
    )


def check_agent_card_json(base_url: str) -> tuple[CheckResult, dict | None]:
    paths = ["/.well-known/agent-card.json", "/.well-known/agent.json"]
    t0 = time.monotonic()
    resp, url, err = _try_paths(base_url, paths)
    rt = int((time.monotonic() - t0) * 1000)

    if resp is None:
        return (
            CheckResult(4, "agent-card.json", 15, 0, False, url, None, rt, None,
                        f"all variants failed: {err}"),
            None,
        )

    try:
        data = resp.json()
    except ValueError:
        return (
            CheckResult(4, "agent-card.json", 15, 0, False, url,
                        resp.status_code, rt, len(resp.content or b""),
                        "invalid JSON"),
            None,
        )

    if not isinstance(data, dict):
        return (
            CheckResult(4, "agent-card.json", 15, 0, False, url,
                        resp.status_code, rt, len(resp.content or b""),
                        "JSON is not an object"),
            None,
        )

    has_name = bool(data.get("name"))
    skills = data.get("skills") or data.get("capabilities") or []
    has_caps = isinstance(skills, list) and len(skills) > 0
    passed = has_name and has_caps
    return (
        CheckResult(
            4, "agent-card.json", 15, 15 if passed else 0, passed, url,
            resp.status_code, rt, len(resp.content or b""),
            f"name={has_name}, skills={len(skills) if isinstance(skills, list) else 0}",
            evidence={k: v for k, v in data.items() if k in
                      ("name", "skills", "capabilities", "endpoints", "auth")},
        ),
        data,
    )


def check_ucp_manifest(base_url: str) -> CheckResult:
    paths = ["/.well-known/ucp/manifest.json", "/.well-known/ucp"]
    t0 = time.monotonic()
    resp, url, err = _try_paths(base_url, paths)
    rt = int((time.monotonic() - t0) * 1000)

    if resp is None:
        return CheckResult(5, "ucp manifest", 10, 0, False, url, None, rt, None,
                           f"all variants failed: {err}")

    try:
        data = resp.json()
        passed = isinstance(data, dict) and len(data) > 0
    except ValueError:
        passed = False
    return CheckResult(
        5, "ucp manifest", 10, 10 if passed else 0, passed, url,
        resp.status_code, rt, len(resp.content or b""),
        "valid JSON object" if passed else "missing or invalid",
    )


def check_openapi(base_url: str) -> tuple[CheckResult, dict | None]:
    paths = ["/openapi.json", "/openapi.yaml", "/swagger.json", "/api-docs",
             "/api/openapi.json", "/v1/openapi.json"]
    t0 = time.monotonic()
    resp, url, err = _try_paths(base_url, paths)
    rt = int((time.monotonic() - t0) * 1000)

    if resp is None:
        return (
            CheckResult(6, "openapi/swagger", 10, 0, False, url, None, rt, None,
                        f"all variants failed: {err}"),
            None,
        )

    try:
        data = resp.json()
        is_openapi = isinstance(data, dict) and (
            "openapi" in data or "swagger" in data or "paths" in data
        )
    except ValueError:
        # YAML support is out of scope for v0.1
        is_openapi = False
        data = None

    return (
        CheckResult(
            6, "openapi/swagger", 10, 10 if is_openapi else 0, is_openapi, url,
            resp.status_code, rt, len(resp.content or b""),
            f"recognized={is_openapi}",
        ),
        data if is_openapi else None,
    )


def check_capability_clarity(
    ai_agent: dict | None,
    agent_card: dict | None,
    skill_md_passed: bool,
) -> CheckResult:
    capabilities: list[Any] = []
    if isinstance(ai_agent, dict):
        c = ai_agent.get("capabilities")
        if isinstance(c, list):
            capabilities.extend(c)
    if isinstance(agent_card, dict):
        for key in ("skills", "capabilities"):
            c = agent_card.get(key)
            if isinstance(c, list):
                capabilities.extend(c)

    named_with_desc = 0
    for cap in capabilities:
        if isinstance(cap, str) and cap.strip():
            named_with_desc += 1
        elif isinstance(cap, dict):
            name = cap.get("name") or cap.get("id") or cap.get("title")
            desc = cap.get("description") or cap.get("summary") or cap.get("doc")
            if name and desc:
                named_with_desc += 1

    passed = named_with_desc >= 3 or (skill_md_passed and named_with_desc >= 1)
    return CheckResult(
        7, "capability clarity", 10, 10 if passed else 0, passed,
        "(derived)", None, None, None,
        f"named_capabilities={named_with_desc}, skill_md={skill_md_passed}",
    )


def check_io_schema(
    openapi: dict | None,
    agent_card: dict | None,
) -> CheckResult:
    has_in = False
    has_out = False

    if isinstance(openapi, dict):
        paths = openapi.get("paths")
        if isinstance(paths, dict):
            for _path, methods in paths.items():
                if not isinstance(methods, dict):
                    continue
                for _m, op in methods.items():
                    if not isinstance(op, dict):
                        continue
                    if op.get("requestBody") or op.get("parameters"):
                        has_in = True
                    if op.get("responses"):
                        has_out = True
                    if has_in and has_out:
                        break
                if has_in and has_out:
                    break

    if isinstance(agent_card, dict):
        skills = agent_card.get("skills") or agent_card.get("capabilities") or []
        if isinstance(skills, list):
            for s in skills:
                if isinstance(s, dict):
                    if s.get("inputSchema") or s.get("input_schema") or s.get("inputs"):
                        has_in = True
                    if s.get("outputSchema") or s.get("output_schema") or s.get("outputs"):
                        has_out = True

    passed = has_in and has_out
    return CheckResult(
        8, "io schema", 10, 10 if passed else 0, passed,
        "(derived)", None, None, None,
        f"input_schema={has_in}, output_schema={has_out}",
    )


def check_pricing_metadata(
    ai_agent: dict | None,
    agent_card: dict | None,
) -> CheckResult:
    has_pricing = False
    for src in (ai_agent, agent_card):
        if isinstance(src, dict):
            if src.get("pricing") or src.get("price") or src.get("cost"):
                has_pricing = True
                break
            # nested in skills?
            skills = src.get("skills") or src.get("capabilities") or []
            if isinstance(skills, list):
                for s in skills:
                    if isinstance(s, dict) and (s.get("pricing") or s.get("price")):
                        has_pricing = True
                        break
    return CheckResult(
        9, "pricing metadata", 5, 5 if has_pricing else 0, has_pricing,
        "(derived)", None, None, None,
        f"pricing_field_found={has_pricing}",
    )


def check_contact_auth_ratelimit(
    ai_agent: dict | None,
    openapi: dict | None,
) -> CheckResult:
    has_auth = False
    has_contact = False
    has_ratelimit = False

    if isinstance(ai_agent, dict):
        if ai_agent.get("auth") or ai_agent.get("authentication"):
            has_auth = True
        if ai_agent.get("contact"):
            has_contact = True
        if ai_agent.get("rateLimit") or ai_agent.get("rate_limit") or ai_agent.get("limits"):
            has_ratelimit = True

    if isinstance(openapi, dict):
        components = openapi.get("components") or {}
        if isinstance(components, dict) and components.get("securitySchemes"):
            has_auth = True
        info = openapi.get("info") or {}
        if isinstance(info, dict) and info.get("contact"):
            has_contact = True

    passed = has_auth and has_contact and has_ratelimit
    return CheckResult(
        10, "contact/auth/rate-limit", 5, 5 if passed else 0, passed,
        "(derived)", None, None, None,
        f"auth={has_auth}, contact={has_contact}, ratelimit={has_ratelimit}",
    )


# ---------------------------------------------------------------------------
# Per-target driver
# ---------------------------------------------------------------------------

def tier_for(score: int) -> str:
    if score >= 80:
        return "Agent-discoverable"
    if score >= 60:
        return "Partially ready"
    if score >= 40:
        return "Weakly discoverable"
    return "Mostly invisible"


def audit_target(row: dict[str, str]) -> TargetResult:
    base = row["url"].strip()
    if not base.startswith(("http://", "https://")):
        base = "https://" + base

    print(f"[{row['id']}] {row['name']} <{base}>", flush=True)

    checks: list[CheckResult] = []
    error: str | None = None

    try:
        c1 = check_llms_txt(base)
        checks.append(c1)

        c2 = check_skill_md(base)
        checks.append(c2)

        c3, ai_agent_data = check_ai_agent_json(base)
        checks.append(c3)

        c4, agent_card_data = check_agent_card_json(base)
        checks.append(c4)

        c5 = check_ucp_manifest(base)
        checks.append(c5)

        c6, openapi_data = check_openapi(base)
        checks.append(c6)

        c7 = check_capability_clarity(ai_agent_data, agent_card_data, c2.passed)
        checks.append(c7)

        c8 = check_io_schema(openapi_data, agent_card_data)
        checks.append(c8)

        c9 = check_pricing_metadata(ai_agent_data, agent_card_data)
        checks.append(c9)

        c10 = check_contact_auth_ratelimit(ai_agent_data, openapi_data)
        checks.append(c10)
    except Exception as exc:
        error = f"audit aborted: {type(exc).__name__}: {exc}"

    total = sum(c.points_awarded for c in checks)
    return TargetResult(
        id=int(row["id"]),
        name=row["name"],
        url=base,
        category=row.get("category", ""),
        total_score=total,
        tier=tier_for(total),
        checks=checks,
        error=error,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if not TARGETS_CSV.exists():
        print(f"missing {TARGETS_CSV}", file=sys.stderr)
        return 1

    with open(TARGETS_CSV, encoding="utf-8") as f:
        targets = list(csv.DictReader(f))

    print(f"auditing {len(targets)} targets\n", flush=True)

    results: list[TargetResult] = []
    for row in targets:
        try:
            results.append(audit_target(row))
        except Exception as exc:
            print(f"  hard error on {row.get('name', '?')}: {exc}", flush=True)
            results.append(TargetResult(
                id=int(row.get("id", 0)),
                name=row.get("name", ""),
                url=row.get("url", ""),
                category=row.get("category", ""),
                total_score=0,
                tier="error",
                error=str(exc),
            ))

    # Write results.csv (flat)
    with open(RESULTS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        header = ["id", "name", "url", "category", "total_score", "tier"]
        for i in range(1, 11):
            header.append(f"check{i}_passed")
            header.append(f"check{i}_points")
        header.append("error")
        writer.writerow(header)
        for r in results:
            row = [r.id, r.name, r.url, r.category, r.total_score, r.tier]
            for i in range(1, 11):
                ck = next((c for c in r.checks if c.check_id == i), None)
                row.append("Y" if (ck and ck.passed) else "N")
                row.append(ck.points_awarded if ck else 0)
            row.append(r.error or "")
            writer.writerow(row)

    # Write results.json (full evidence)
    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, indent=2, ensure_ascii=False)

    # Console summary
    n = len(results)
    avg = sum(r.total_score for r in results) / n if n else 0
    tiers = {"Agent-discoverable": 0, "Partially ready": 0,
             "Weakly discoverable": 0, "Mostly invisible": 0, "error": 0}
    for r in results:
        tiers[r.tier] = tiers.get(r.tier, 0) + 1

    print("\n" + "=" * 60)
    print(f"Scanned: {n} targets")
    print(f"Average score: {avg:.1f} / 100")
    print("Tier distribution:")
    for t, count in tiers.items():
        if count:
            print(f"  {t:25s} {count:3d}  ({count*100/n:.0f}%)")
    print(f"\nResults written to:\n  {RESULTS_CSV}\n  {RESULTS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
