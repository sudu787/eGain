# Testing report

## Local automated checks

Tests in `tests/test_api.py` cover:

- health and synthetic status disclosure;
- report persistence and receipt disclosure;
- idempotent retry and conflicting key reuse;
- rejection of unknown areas and unexpected personal-data fields;
- storage failure returning a recoverable `503`.

**Result:** `docker build -f Dockerfile.test -t gridguide-tests .` succeeded after adding Postgres support; `docker run --rm gridguide-tests` completed with **5 passed**. Starlette emitted one deprecation warning about its `httpx`-based TestClient. The automated suite ran in Python 3.12 inside Docker and exercised the local SQLite path. Separately, the hosted eGain action successfully created two reports; that confirms successful production-path calls but does not replace automated Postgres failure, auth rejection, or retry tests.

**Container smoke check:** `docker compose up -d --build` succeeded. `GET /healthz`, `GET /api/v1/demo/outages`, report creation, and receipt lookup all returned the expected results. The sample feed identified itself as synthetic/non-live; the report returned and then retrieved reference `GG-BEEBEB45DD` with the demo-only disclosure. This is a fictional local database record, not a utility submission.

## Hosted API validation

**Verified 2026-11-10:** `GET https://egain-lake.vercel.app/api/healthz` returned `status: ok`, `environment: demonstration`, and `report_store: configured`. `GET https://egain-lake.vercel.app/api/v1/demo/outages` returned sample records with `data_type: synthetic demonstration data; not live utility status`.

## eGain validation

**Observed in the user's eGain account:** GridGuide exists in Agentic Studio with agent ID `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`. The eGain demo URL is `https://aidev.egain.cloud/u0np/system/web/apps/aiagent/demo.html?agentId=0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d&backgroundUrl=https://cdn.aiagent-dev.egain.cloud/TMDEVEB50400311/screenshots/2b04fd20-c8e1-4799-8fd9-65ebd6fd5440.png`. The user tested downed-wire guidance; it gave keep-away/no-touch and emergency guidance, with one irrelevant generic sentence that should be removed from the agent response. The user tested the configured report action and supplied two successful receipts: `GG-E8552A6085` for North Ridge / `no_power`, and `GG-B5C218F450` for Cedar Park / `partial_power`. Each response disclosed that it was stored for demonstration only and not sent to a utility.

The public Vercel page and API endpoints are reachable. An interactive test of the embedded widget on the public page has not been evidenced yet. Earlier Test AI Agent spinner issues are historical; current test-panel behavior is not confirmed.

The following eGain behaviors remain unverified and should be tested in Test AI Agent and through the published link:

1. Grounded answer: refrigerator and freezer guidance with FDA source.
2. Grounded answer: downed power-line safety; verify immediate guidance and escalation precede routine intake.
3. Report path: valid sample area/category, confirmation, returned receipt.
4. Missing and invalid input: re-prompt with allowed choices; no action before confirmation.
5. User declines: ensure no action call.
6. Action failure/timeout: no fabricated receipt; contact choices shown.
7. Repeat report request: idempotent behavior if connector supports the key.
8. Unknown restoration estimate: disclose lack of live utility access.
9. Medical-device dependence: no sensitive detail request or medical advice; offer urgent and human routes.
10. Both escalation options are visible and clearly fictional/unmonitored.

Record actual date, account agent, build/version, each result, and published demo URL after testing. Do not mark pending cases as passed. The two successful receipts above confirm the action path for those inputs only; they do not prove confirmation/decline handling, invalid-input handling, action-failure behavior, idempotent retries, or the embedded public chat.
