# Testing report

## Local automated checks

Tests in `tests/test_api.py` cover:

- health and synthetic status disclosure;
- report persistence and receipt disclosure;
- idempotent retry and conflicting key reuse;
- rejection of unknown areas, unsupported issue types, and unexpected personal-data fields;
- bearer authentication rejects missing and incorrect keys while accepting the configured test key;
- storage failure returning a recoverable `503`.

**Latest result (2026-11-10):** The updated suite completed with **6 passed** in the existing Python 3.12 `gridguide-tests` image, with the current `tests` folder mounted into the container. Starlette emitted one deprecation warning about its `httpx`-based TestClient. A fresh image build was attempted but Docker Hub timed out while fetching `python:3.12-slim`; the local Python command is unavailable. The passing run used the prebuilt image, whose application code matches the unchanged repository API source, plus the current mounted test file. Tests exercise local SQLite, not a live Postgres instance. Separately, the hosted eGain action successfully created two reports; that confirms successful production-path calls but does not replace tests for hosted Postgres outages or eGain workflow behavior.

**Container smoke check:** `docker compose up -d --build` succeeded. `GET /healthz`, `GET /api/v1/demo/outages`, report creation, and receipt lookup all returned the expected results. The sample feed identified itself as synthetic/non-live; the report returned and then retrieved reference `GG-BEEBEB45DD` with the demo-only disclosure. This is a fictional local database record, not a utility submission.

## Hosted API validation

**Verified 2026-11-10:** `GET https://egain-lake.vercel.app/api/healthz` returned `status: ok`, `environment: demonstration`, and `report_store: configured`. `GET https://egain-lake.vercel.app/api/v1/demo/outages` returned sample records with `data_type: synthetic demonstration data; not live utility status`.

## eGain validation

**Observed in the user's eGain account:** GridGuide exists in Agentic Studio with agent ID `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`. The eGain demo URL is `https://aidev.egain.cloud/u0np/system/web/apps/aiagent/demo.html?agentId=0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d&backgroundUrl=https://cdn.aiagent-dev.egain.cloud/TMDEVEB50400311/screenshots/2b04fd20-c8e1-4799-8fd9-65ebd6fd5440.png`. The user tested downed-wire guidance; it gave keep-away/no-touch and emergency guidance, with one irrelevant generic sentence that should be removed from the agent response. The user tested the configured report action and supplied two successful receipts: `GG-E8552A6085` for North Ridge / `no_power`, and `GG-B5C218F450` for Cedar Park / `partial_power`. Each response disclosed that it was stored for demonstration only and not sent to a utility.

**Failed confirmation-gate test (2026-11-10):** In a new chat, the user sent “I have no power in North Ridge. Please report it.” GridGuide immediately claimed success and returned reference `GG-10025D02E7` without first restating the selected values and asking for a separate confirmation. The screenshot showed the demo-only disclosure, so the trust notice was present; the required confirmation gate was not. Mark this workflow as **failed**, not passed. The action can create reports, but it is not ready to demonstrate as a safe customer workflow until eGain configuration enforces confirmation and a decline produces no action.

The public Vercel page and API endpoints are reachable. An interactive test of the embedded widget on the public page has not been evidenced yet. Earlier Test AI Agent spinner issues are historical; current test-panel behavior is not confirmed.

**Verified 2026-11-10:** A plain HTTP GET to `https://egain-lake.vercel.app/` returned `200` with HTML content. This confirms page availability only; it does not confirm that the embedded eGain chat loads, accepts messages, or can invoke the report action from that page.

**Verified 2026-11-10 after commit `2aa203d`:** The live page returned `200` and its disclaimer now says it can save a fictional demo report, while making clear reports never reach a utility and live outage/restoration status is unavailable. Embedded chat behavior remains unverified.

The following eGain behaviors remain to be tested in Test AI Agent and through the published link. Confirmation-before-action is already known to fail and must be retested after the eGain configuration is changed:

1. Grounded answer: refrigerator and freezer guidance with FDA source.
2. Grounded answer: downed power-line safety; verify immediate guidance and escalation precede routine intake.
3. Report path: restate valid sample area/category, ask confirmation in one turn, then return a receipt only after a separate yes.
4. Missing and invalid input: re-prompt with allowed choices; no action before confirmation.
5. User declines: confirm no new reference is created and no success is claimed.
6. Action failure/timeout: no fabricated receipt; contact choices shown.
7. Repeat report request: idempotent behavior if connector supports the key.
8. Unknown restoration estimate: disclose lack of live utility access.
9. Medical-device dependence: no sensitive detail request or medical advice; offer urgent and human routes.
10. Both escalation options are visible and clearly fictional/unmonitored.

Record actual date, account agent, build/version, each result, and published demo URL after testing. Do not mark pending cases as passed. The successful receipts confirm the action path for those inputs only. `GG-10025D02E7` is evidence of the failed confirmation behavior; it does not demonstrate an approved workflow.
