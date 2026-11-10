# eGain configuration guide

## Current account setup

- Agent: **GridGuide**
- Agent ID: `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`
- Language: English (US)
- Uploaded source file: `gridguide-egain-source.html` (4,704 characters)
- Reviewed topics include public health/safety, service limits, emergency protocols, outage reporting, accessibility/medical support, and restoration limits.
- Welcome, demo disclaimer, safety/privacy instructions, and fictional escalation details have been configured.
- Agentic Studio exposes **Enable Actions → Custom APIs** in this account. The built-in Knowledge Search action is enabled, and a bearer-authenticated POST Custom API for demo report creation has returned successful receipts.
- eGain demo URL: `https://aidev.egain.cloud/u0np/system/web/apps/aiagent/demo.html?agentId=0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d&backgroundUrl=https://cdn.aiagent-dev.egain.cloud/TMDEVEB50400311/screenshots/2b04fd20-c8e1-4799-8fd9-65ebd6fd5440.png`
- Public webpage: `https://egain-lake.vercel.app/`

The user supplied successful eGain action results for `GG-E8552A6085` (North Ridge / `no_power`) and `GG-B5C218F450` (Cedar Park / `partial_power`). The Vercel health endpoint currently reports the report store as configured. The pre-chat UI previously reported no published workflows available, so do not claim a published pre-chat or explicit-confirmation workflow unless it is now observed in the account. Several failure and safety cases remain to be tested.

## Setup sequence

1. Keep the uploaded source file and generated topics/intents aligned with `intents.md` after any content changes.
2. Preserve the configured persistent Postgres and `GRIDGUIDE_API_KEY` settings in Vercel; never expose the secret in the repository or demo.
3. Keep the authenticated POST Custom API for `/api/v1/outage-reports` configured with JSON fields `service_area` and `issue_type`; successful eGain report calls are confirmed.
4. Verify the actual account workflow requires explicit confirmation before action. The successful action tests do not by themselves prove that guardrail.
5. Test missing/invalid fields, user decline, authentication/service failure, duplicate behavior if supported, safety priority, live-status deferral, and the public embedded chat. Record only observed outcomes.

## Publication record

- eGain account/agent identifier: **GridGuide / `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`**
- Public web demo: **`https://egain-lake.vercel.app/`**
- eGain demo URL: **Generated and returned by the account**
- Custom API endpoint: **Configured; successful report calls observed, returning `GG-E8552A6085` and `GG-B5C218F450`**
- Hosted report store: **Configured; live health endpoint reports `report_store: configured`**
- Test AI Agent validation: **Report action success observed; remaining behavior cases are listed in `testing_report.md`**
- Public-link validation: **Page/API are reachable; interactive widget/action test through the embedded public page remains unverified**
