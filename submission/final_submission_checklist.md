# Final submission checklist

## Local assets prepared

- [x] Original fictional utility concept and alternatives documented.
- [x] English source knowledge articles drafted with authoritative public references.
- [x] Intents, pre-chat, process workflows, actions, safety, and escalation specified.
- [x] Supporting API and local automated test cases written.
- [x] GridGuide agent configured in eGain; public demo page deployed.
- [x] Submission description and one-minute demo script drafted.

## Required before submission

Official deadline: **November 15, 2026 at 11:59 PM Pacific Time** (November 16 at 1:29 PM India time). Confirm the live rules page before the deadline in case the organizer changes it: https://www.egain.com/ai-agent-hackathon/

Official form: https://www.egain.com/ai-agent-hackathon-project-submission/

- [x] Local API test suite and Docker smoke test completed (see testing report; rerun before final hand-in if code changes).
- [x] Provision persistent cloud Postgres and deploy the FastAPI app on Vercel; live health reports `report_store: configured`.
- [x] Connect the synthetic report API through eGain Custom APIs; successful eGain calls returned receipts `GG-E8552A6085` and `GG-B5C218F450`.
- [ ] Fix the failed confirmation gate in eGain: a normal outage request created `GG-10025D02E7` immediately without asking first. Connect the outage intent to a process workflow that summarizes the area/category, waits for a separate yes, and only then calls the API. Verify “No” creates no report.
- [ ] Complete remaining eGain behavior checks: decline, invalid or missing fields, action failure, live-status deferral, medical/accessibility, and safety response quality.
- [x] Capture the eGain demo URL and public Vercel page URL.
- [ ] Test the interactive agent through the published Vercel page and record only observed outcomes. API health and synthetic status were verified directly; that does not verify the embedded chat.
- [ ] Record the one-minute video showing a grounded answer, workflow, actual action if connected, and safety triage.
- [ ] Add participant/team information, video URL, reviewer instructions, and asset disclosure to the submission form.
- [ ] Confirm eligibility and read both submission-form confirmations carefully. Do not affirm workflow testing or intent connection until observed in eGain and the published demo.

**Status:** The report API works, but the eGain report flow currently fails the confirmation safeguard: it created a record immediately from a normal request. Fix and retest the intent-connected process before presenting the report workflow as safe or submitting. The published embedded chat, remaining behavior tests, video, form, and eligibility checks also remain.
