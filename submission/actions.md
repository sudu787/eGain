# Actions

## Create outage report (fictional demo action)

**Purpose:** persist a synthetic report record in the GridGuide database and return a receipt. Local development uses SQLite; cloud deployment uses managed Postgres. The action does not notify an actual utility or dispatch a crew.

**Trigger:** Report an outage intent, after the user reviews the area and issue and explicitly confirms.

**Method/path:** `POST /api/v1/outage-reports`  
**Headers:** `Content-Type: application/json`, `Authorization: Bearer <secret>`; optional `Idempotency-Key` with 8–128 allowed characters.  
**JSON body:** `{"service_area":"North Ridge","issue_type":"no_power"}`

Allowed service areas: `North Ridge`, `Cedar Park`, `Riverbend`, `Old Town`.  
Allowed issue types: `no_power`, `partial_power`, `flickering_lights`, `other`.

Success returns a `GG-XXXXXXXXXX` reference, `created_at`, and a demo-only notice. A repeated key with the same values returns the same receipt; using the same key with different values returns `409`. Invalid choices return `422`; a storage problem returns `503`. The agent must never announce success unless it received a successful response.

**eGain connection status:** Agentic Studio exposes a Custom API action form in the trial account. Connection to the public API is pending persistent database provisioning and action configuration. Use `https://egain-lake.vercel.app/api/v1/outage-reports`, method `POST`, JSON body with the two fields above, and bearer authentication. Map `reference`, `service_area`, `issue_type`, `created_at`, `status`, and `demo_notice`; treat non-2xx responses as failure. A separate sample-status action can use `GET https://egain-lake.vercel.app/api/v1/demo/outages`; its results are synthetic only. Never place credentials in this repository.
