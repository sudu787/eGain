# eGain configuration guide

## Current account setup

- Agent: **GridGuide**
- Agent ID: `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`
- Language: English (US)
- Source file previously uploaded: `gridguide-egain-source.html`. The repository version now includes a separate-turn confirmation gate; it has **not** been confirmed as uploaded to eGain after this revision.
- Reviewed topics include public health/safety, service limits, emergency protocols, outage reporting, accessibility/medical support, and restoration limits.
- Welcome, demo disclaimer, safety/privacy instructions, and fictional escalation details have been configured.
- Agentic Studio exposes **Enable Actions → Custom APIs** in this account. The built-in Knowledge Search action is enabled, and a bearer-authenticated POST Custom API for demo report creation has returned successful receipts.
- eGain demo URL: `https://aidev.egain.cloud/u0np/system/web/apps/aiagent/demo.html?agentId=0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d&backgroundUrl=https://cdn.aiagent-dev.egain.cloud/TMDEVEB50400311/screenshots/2b04fd20-c8e1-4799-8fd9-65ebd6fd5440.png`
- Public webpage: `https://egain-lake.vercel.app/`

The user supplied successful eGain action results for `GG-E8552A6085` (North Ridge / `no_power`) and `GG-B5C218F450` (Cedar Park / `partial_power`). A later ordinary request (“I have no power in North Ridge. Please report it.”) immediately created `GG-10025D02E7` without asking for confirmation. This is a failed safeguard. The pre-chat UI previously reported no published workflows available. Configure and connect an explicit-confirmation process to the outage intent before claiming the report workflow is safe or ready to submit.

## Setup sequence

1. Keep the uploaded source file and generated topics/intents aligned with `intents.md` after any content changes.
2. Preserve the configured persistent Postgres and `GRIDGUIDE_API_KEY` settings in Vercel; never expose the secret in the repository or demo.
3. Keep the authenticated POST Custom API for `/api/v1/outage-reports` configured with JSON fields `service_area` and `issue_type`; successful eGain report calls are confirmed.
4. Fix the observed failure by routing the report intent through a process that repeats the fictional area/category, explains the demo-only write, asks a confirmation question, and pauses for the next user turn before calling the action. A first request is not confirmation.
5. Test explicit yes and no responses, missing/invalid fields, action failure, duplicate behavior if supported, safety priority, live-status deferral, and the public embedded chat. Record only observed outcomes.

## Required account repair after the failed confirmation test

1. In **Personalize and Publish → Conversation Behavior**, add the mandatory separate-turn confirmation instructions from `agent_instructions.md`. The current agent skipped this gate even though the repository already specified confirmation.
2. In **Enable Actions → Custom APIs → Create Demo Outage Report**, change the description to the confirmation-gated wording in `actions.md`. Replace direct initial-request sample questions with confirmed follow-up examples such as “Yes, create the demo report for North Ridge with no power.”
3. In the report intent/workflow settings, route the report request through a process that gathers the area and issue, states the demo-only consequence, asks whether to proceed, waits for the next user message, and calls the API only after a clear yes. A first-turn request must not invoke the action.
4. Retest with a new conversation. First request: “I have no power in North Ridge. Please report it.” Expected: a confirmation question and no `GG-` receipt. Reply “No”; expected: no API call. Start another conversation, repeat the request, then reply “Yes”; expected: one new demo receipt. If the action fires on the first message, the fix has not worked.

Keep the verified endpoint, bearer credential, and request fields `service_area` / `issue_type` unchanged while fixing the turn order; the API action itself has already succeeded.

## Publication record

- eGain account/agent identifier: **GridGuide / `0f41dd94-ba0f-4e1d-8f26-8796e56c7a5d`**
- Public web demo: **`https://egain-lake.vercel.app/`**
- eGain demo URL: **Generated and returned by the account**
- Custom API endpoint: **Configured; successful report calls observed, returning `GG-E8552A6085` and `GG-B5C218F450`**
- Hosted report store: **Configured; live health endpoint reports `report_store: configured`**
- Test AI Agent validation: **Report action success observed; normal request bypassed confirmation and created `GG-10025D02E7`. Confirmation safeguard failed; remaining cases are listed in `testing_report.md`.**
- Public-link validation: **Page/API are reachable; interactive widget/action test through the embedded public page remains unverified**
