# eGain configuration guide

## Current account setup

- Agent: **GridGuide**
- Agent ID: `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`
- Language: English (US)
- Uploaded source file: `gridguide-egain-source.html` (4,704 characters)
- Reviewed topics include public health/safety, service limits, emergency protocols, outage reporting, accessibility/medical support, and restoration limits.
- Welcome, demo disclaimer, safety/privacy instructions, and fictional escalation details have been configured.
- Agentic Studio exposes **Enable Actions → Custom APIs** in this account. The built-in Knowledge Search action is enabled.
- eGain demo URL: `https://aidev.egain.cloud/u0np/system/web/apps/aiagent/demo.html?agentId=0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d&backgroundUrl=https://cdn.aiagent-dev.egain.cloud/TMDEVEB50400311/screenshots/2b04fd20-c8e1-4799-8fd9-65ebd6fd5440.png`
- Public webpage: `https://egain-lake.vercel.app/`

The Test AI Agent chat spinner did not complete during earlier checks. The pre-chat UI reported no published workflows available. The report/status Custom API has not yet been added, and no persistent cloud database has been provisioned. Do not claim report-action integration or workflow tests until completed and observed.

## Setup sequence

1. Recheck the source file and generated topics/intents against `intents.md` after content changes.
2. Provision persistent Postgres for the Vercel project and configure `GRIDGUIDE_DATABASE_URL` and `GRIDGUIDE_API_KEY` as environment variables.
3. Redeploy and confirm `/healthz` reports the store configured. Confirm `/api/v1/demo/outages` is visibly synthetic.
4. Add a POST Custom API for `/api/v1/outage-reports` and optional GET for `/api/v1/outage-reports/{reference}` with bearer auth, field mapping, response handling, and timeout behavior.
5. Add an outage-report process that collects only a fictional area and issue, summarizes them, obtains explicit confirmation, and calls the API only after confirmation. Keep immediate safety cases outside the report action.
6. Update the agent's additional instructions to describe the connected action accurately: successful reports create synthetic records only and never reach a utility.
7. Test success, missing/invalid fields, authentication failure, duplicate retry, persistent lookup, downed-wire safety, and live-status deferral in Test AI Agent and the public link. Record only observed results.

## Publication record

- eGain account/agent identifier: **GridGuide / `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`**
- Public web demo: **`https://egain-lake.vercel.app/`**
- eGain demo URL: **Generated and returned by the account**
- Custom API endpoint: **Pending persistent database and Vercel API deployment**
- Test AI Agent validation: **Pending; chat spinner did not complete in prior check**
- Public-link validation: **The Vercel page returned HTTP 200 and includes the eGain widget loader; interactive rendering still needs a browser check**
