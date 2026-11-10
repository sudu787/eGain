# GridGuide demonstration API

Local base URL: `http://localhost:8000`. OpenAPI UI: `/api/docs`. The public page is `https://egain-lake.vercel.app/`; its API uses the same host.

## `GET /healthz`

Returns `{ "status": "ok", "environment": "demonstration" }`.

## `GET /api/v1/demo/outages`

Returns fixed sample outage entries with `data_type` set to “synthetic demonstration data; not live utility status”. Do not present these values as real conditions.

## `POST /api/v1/outage-reports`

Creates a fictional report record. Requires JSON fields `service_area` and `issue_type`; extra fields are rejected. Supported areas: North Ridge, Cedar Park, Riverbend, Old Town. Supported issue types: `no_power`, `partial_power`, `flickering_lights`, `other`.

An optional `Idempotency-Key` header (8–128 alphanumeric or `._:-` characters) makes retries safe for the same payload. Same key/different payload returns `409`. Success returns a `GG-` reference and explicit demo disclosure. `422` means invalid input, `400` invalid idempotency key, `409` key conflict, and `503` report storage unavailable. The API never returns a successful receipt when persistence fails.

## `GET /api/v1/outage-reports/{reference}`

Looks up a stored synthetic receipt by its reference. Returns `404` when absent and `503` if storage is unavailable.

## Data and security constraints

No account, address, name, phone, email, payment, or medical fields are accepted. The API is for a fictional hackathon demo only. Do not expose it as a production utility endpoint. Set `GRIDGUIDE_API_KEY` on the host and configure eGain to send `Authorization: Bearer <same-secret>` for report creation and receipt lookup. Requests fail with `401` if the key is configured but missing or wrong. Set `GRIDGUIDE_DATABASE_URL` to a managed Postgres connection string for cloud deployment. On Vercel, report writes and lookups fail with `503` until this persistent database is configured; the API never reports an ephemeral SQLite write as saved. Configure an exact `GRIDGUIDE_ALLOWED_ORIGINS` value only if browser-based access is required; leave blank for server-to-server use.
