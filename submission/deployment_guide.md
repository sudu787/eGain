# Deployment guide

## Local Docker run

1. Install Docker Desktop and start the Linux engine.
2. From the repository root, run `docker compose up --build`.
3. Confirm `http://localhost:8000/healthz` returns `status: ok` and open `/docs`.
4. Submit one report with the example request in the root README. Confirm the response includes the demo disclosure and then retrieve it by reference.
5. Data persists in the named `gridguide-data` volume across container restarts.

## Hosted API and database

The Vercel project serves the demo page at `https://egain-lake.vercel.app/`. The repository exposes FastAPI through root `main.py`; Vercel's Python runtime supports FastAPI.

The hosted database and report endpoint are configured. The live `GET https://egain-lake.vercel.app/api/healthz` response reports `report_store: configured`, and eGain has successfully created demo report receipts. Keep the managed Postgres URL in Vercel as `GRIDGUIDE_DATABASE_URL` and the matching bearer secret as `GRIDGUIDE_API_KEY`; retain the secret in eGain's credential store and never commit it.

## eGain hosted action

In Agentic Studio → Enable Actions → Custom APIs, the POST action for `https://egain-lake.vercel.app/api/v1/outage-reports` is configured with JSON fields `service_area` and `issue_type` and bearer authentication. Successful eGain calls returned receipts. Confirm the report workflow asks for explicit user confirmation before calling it, maps the returned receipt, and treats non-2xx results as failures. The separate `/api/v1/demo/outages` endpoint returns synthetic data only.

**Current account behavior:** A normal report request bypassed the confirmation step and created `GG-10025D02E7`. Treat this as a failed safety test. Do not record or present the report workflow as ready until the outage intent is routed through a separate-turn confirmation process and a decline is verified to create no record.

Health, synthetic status disclosure, and two successful eGain report calls have been observed. Invalid input, bad/missing authentication, idempotent retry from eGain, persistent lookup from eGain, and the public embedded chat still need end-to-end checks. This hosted API remains a fictional demonstration and is not a real utility integration.
