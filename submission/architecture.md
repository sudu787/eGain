# Architecture

```text
Resident
  │
  ▼
eGain AI Agent (customer-facing knowledge, intents, pre-chat, workflows, escalation)
  │ supported REST/API action connection when available
  ▼
GridGuide FastAPI service ── SQLite demonstration report store
  └── synthetic outage sample feed (never live utility status)
```

## Components

- **eGain AI Agent:** the only planned customer-facing conversational agent. It hosts imported knowledge, reviewed intents, pre-chat, process workflows, escalation choices, and the published demo experience.
- **FastAPI support service:** validates a fictional service area and issue category, persists a report record, and returns a reference. It does not integrate with a utility, dispatch crews, or verify power status.
- **SQLite:** local durable store for synthetic report receipts. The database stores only a fictional service area, an issue category, timestamp, reference, and optional idempotency key.
- **Docker Compose:** reproducible local run using a named data volume. Public hosting is required before eGain can call the API from a hosted account.

## Data flow and trust boundaries

The customer first sees the agent’s urgent-safety path. Routine requests can go through pre-chat and an intent-connected workflow. For a report, eGain should require an explicit confirmation step before invoking the action. The API accepts only allowlisted service-area and issue-type values; it rejects additional fields. A successful response is proof only that the demonstration record was saved. The agent must quote the demo notice and receipt reference. If the API is unavailable, the agent must say the report was not saved and present escalation options.

No authentication system is implemented because the API accepts no account-specific lookup and contains no real customer data. Before any real utility use, replace the demo boundary with utility authorization, operational integration, security review, privacy review, and incident handling. Do not expose this demo API as a production service.
