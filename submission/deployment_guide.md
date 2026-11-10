# Deployment guide

## Local Docker run

1. Install Docker Desktop and start the Linux engine.
2. From the repository root, run `docker compose up --build`.
3. Confirm `http://localhost:8000/healthz` returns `status: ok` and open `/docs`.
4. Submit one report with the example request in the root README. Confirm the response includes the demo disclosure and then retrieve it by reference.
5. Data persists in the named `gridguide-data` volume across container restarts.

## Hosted API and database

The Vercel project serves the demo page at `https://egain-lake.vercel.app/`. The repository exposes FastAPI through root `main.py`; Vercel's Python runtime supports FastAPI.

Before reports can be saved from eGain, provision managed Postgres from Vercel Marketplace (Neon or another Postgres provider), then add its connection string to Vercel as `GRIDGUIDE_DATABASE_URL`. Set a long random `GRIDGUIDE_API_KEY` in Vercel and store the same secret in the eGain Custom API authentication settings. Never commit secrets. Redeploy after setting environment variables. Report writes and lookups fail closed until the persistent database is configured.

## eGain hosted action

In Agentic Studio → Enable Actions → Custom APIs, create a POST action for `https://egain-lake.vercel.app/api/v1/outage-reports`, with JSON request fields `service_area` and `issue_type`, `Content-Type: application/json`, and bearer authentication. Require explicit user confirmation in the report workflow before calling it. Map the successful receipt fields, and treat non-2xx results as failures. Add a separate GET action for `/api/v1/demo/outages` only if sample records are needed; keep their synthetic status label visible.

Test health, report success, invalid input, bad/missing authentication, idempotent retry, and persistent lookup before describing the action as connected. This hosted API remains a fictional demonstration and is not a real utility integration.
