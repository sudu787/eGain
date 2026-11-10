# Testing report

## Local automated checks

Tests in `tests/test_api.py` cover:

- health and synthetic status disclosure;
- report persistence and receipt disclosure;
- idempotent retry and conflicting key reuse;
- rejection of unknown areas and unexpected personal-data fields;
- storage failure returning a recoverable `503`.

**Result:** `docker build -f Dockerfile.test -t gridguide-tests .` succeeded after adding Postgres support; `docker run --rm gridguide-tests` completed with **5 passed**. Starlette emitted one deprecation warning about its `httpx`-based TestClient. The tests ran in Python 3.12 inside Docker and exercised the local SQLite path. The new Postgres and bearer-auth paths have not yet been exercised.

**Container smoke check:** `docker compose up -d --build` succeeded. `GET /healthz`, `GET /api/v1/demo/outages`, report creation, and receipt lookup all returned the expected results. The sample feed identified itself as synthetic/non-live; the report returned and then retrieved reference `GG-BEEBEB45DD` with the demo-only disclosure. This is a fictional local database record, not a utility submission.

## eGain validation

**Observed:** GridGuide exists in Agentic Studio with agent ID `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`. The public demo URL is `https://aidev.egain.cloud/u0np/system/web/apps/aiagent/demo.html?agentId=0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d&backgroundUrl=https://cdn.aiagent-dev.egain.cloud/TMDEVEB50400311/screenshots/2b04fd20-c8e1-4799-8fd9-65ebd6fd5440.png`. A user tested the downed-power-line question in the widget; the answer gave keep-away/no-touch and emergency guidance, then added an irrelevant generic statement about not sending screenshots. The Vercel page returned HTTP 200 and its HTML contains the eGain chat loader. The Test AI Agent panel had previously remained on a spinner. The report action, public API, persistent cloud database, and report workflow are still pending.

The following must be tested in Test AI Agent and through the published link before making a completion claim:

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

Record actual date, account agent, build/version, each result, and published demo URL after testing. Do not mark pending cases as passed.
