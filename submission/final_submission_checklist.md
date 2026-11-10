# Final submission checklist

## Local assets prepared

- [x] Original fictional utility concept and alternatives documented.
- [x] English source knowledge articles drafted with authoritative public references.
- [x] Intents, pre-chat, process workflows, actions, safety, and escalation specified.
- [x] Supporting API and local automated test cases written.
- [x] GridGuide agent configured in eGain; public demo page deployed.
- [x] Submission description and one-minute demo script drafted.

## Required before submission

- [x] Local API test suite and Docker smoke test completed (see testing report; rerun before final hand-in if code changes).
- [x] Provision persistent cloud Postgres and deploy the FastAPI app on Vercel; live health reports `report_store: configured`.
- [x] Connect the synthetic report API through eGain Custom APIs; successful eGain calls returned receipts `GG-E8552A6085` and `GG-B5C218F450`.
- [ ] Complete remaining eGain behavior checks: confirmation/decline, invalid or missing fields, action failure, live-status deferral, medical/accessibility, and safety response quality.
- [x] Capture the eGain demo URL and public Vercel page URL.
- [ ] Test the interactive agent through the published Vercel page and record only observed outcomes. API health and synthetic status were verified directly; that does not verify the embedded chat.
- [ ] Record the one-minute video showing a grounded answer, workflow, actual action if connected, and safety triage.
- [ ] Add participant/team information, video URL, reviewer instructions, and asset disclosure to the submission form.
- [ ] Confirm the entry meets eligibility and official submission deadline.

**Status:** Core demo is working: the agent, hosted persistent report API, and eGain report action are configured; eGain has returned successful demo report receipts. Submission is not complete until remaining behavior tests are recorded, the published embedded chat is checked, the demo video and form are completed, and eligibility/deadline are confirmed.
