# Actions

## Create outage report (fictional demo action)

**Purpose:** persist a synthetic report record in the GridGuide database and return a receipt. Local development uses SQLite; cloud deployment uses managed Postgres. The action does not notify an actual utility or dispatch a crew.

**Trigger:** Report an outage intent, after the user reviews the area and issue and explicitly confirms.

**eGain Custom API description:** “Create a fictional demo outage report only after the user has reviewed the service area and issue category and then explicitly confirmed in a separate reply. The initial request is not confirmation. If the user declines or is unclear, do not call this action. The report is not sent to a real utility.”

**Suggested sample questions:** Use confirmed follow-up utterances such as “Yes, create the demo report for North Ridge with no power.” Do not use initial-request examples as action triggers until the separate confirmation gate is implemented and tested.

**Method/path:** `POST /api/v1/outage-reports`  
**Headers:** `Content-Type: application/json`, `Authorization: Bearer <secret>`; optional `Idempotency-Key` with 8–128 allowed characters.  
**JSON body:** `{"service_area":"North Ridge","issue_type":"no_power"}`

Allowed service areas: `North Ridge`, `Cedar Park`, `Riverbend`, `Old Town`.  
Allowed issue types: `no_power`, `partial_power`, `flickering_lights`, `other`.

Success returns a `GG-XXXXXXXXXX` reference, `created_at`, and a demo-only notice. A repeated key with the same values returns the same receipt; using the same key with different values returns `409`. Invalid choices return `422`; a storage problem returns `503`. The agent must never announce success unless it received a successful response.

**eGain connection status:** The authenticated Custom API is configured against `https://egain-lake.vercel.app/api/v1/outage-reports` with method `POST` and the JSON body above. The user observed successful eGain calls returning references `GG-E8552A6085` and `GG-B5C218F450`. A later natural-language request created `GG-10025D02E7` immediately without first asking for confirmation. The API connection works; the confirmation safeguard currently fails and must be fixed in eGain before recording or submitting the report workflow. Map `reference`, `service_area`, `issue_type`, `created_at`, `status`, and `demo_notice`; treat non-2xx responses as failure. The report action is a fictional demo write and is not a real utility integration. The separate sample-status endpoint `GET https://egain-lake.vercel.app/api/v1/demo/outages` returns synthetic data only. Never place credentials in this repository.
