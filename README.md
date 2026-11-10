# GridGuide

GridGuide is a fictional electric-utility customer-service agent concept for the eGain AI Agent Hackathon. eGain is the intended customer-facing channel. This repository contains original English knowledge content, eGain configuration materials, and a small supporting API for a verifiable demonstration action.

The API writes outage reports to a local SQLite database during local runs and can use managed Postgres in the cloud. It returns a receipt, but it is **not** sent to an electric utility, does not dispatch crews, and does not create a real service request. The outage-status endpoint returns synthetic records only. Never describe those records as live status.

## Run the API

Requires Docker Desktop with the Linux engine running.

```powershell
docker compose up --build
```

Then open `http://localhost:8000/api/docs`. Health is available at `/healthz` (and `/api/healthz`); the synthetic status feed is `/api/v1/demo/outages`.

Run the isolated API test suite with:

```powershell
docker build -f Dockerfile.test -t gridguide-tests .
docker run --rm gridguide-tests
```

To create a demo report:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/outage-reports `
  -ContentType 'application/json' `
  -Headers @{ 'Idempotency-Key' = 'demo-run-0001' } `
  -Body '{"service_area":"North Ridge","issue_type":"no_power"}'
```

The same key and same values return the original receipt, preventing an accidental duplicate. Reusing the key with different values returns `409`. Supported areas and issue values are documented in `submission/api_documentation.md`.

## eGain status

The GridGuide agent is configured in eGain, and the public demo page is https://egain-lake.vercel.app/. The agent has uploaded knowledge and safety instructions. The authenticated eGain Custom API report action has returned successful demo receipts, including `GG-E8552A6085` and `GG-B5C218F450`. These are fictional records and are not sent to a utility.

## Hosted API

The Vercel project serves this FastAPI app and the static `index.html` page from this repository. The live health endpoint currently reports `report_store: configured`; the eGain action has successfully created reports. Keep the managed Postgres connection in Vercel as `GRIDGUIDE_DATABASE_URL` and the bearer secret as `GRIDGUIDE_API_KEY`; configure the matching bearer credential in eGain. Do not commit either value. Vercel function storage is not used for durable records.

See [submission/eGain_configuration.md](submission/eGain_configuration.md) for the account checklist and [submission/final_submission_checklist.md](submission/final_submission_checklist.md) for remaining work.
