# SEI API and Script Interface

Milestone 7 exposes Sales Engagement and Intelligence (SEI) workflow operations through explicit Frappe whitelisted methods under:

```text
sales_engagement_intelligence.sales_engagement_and_intelligence.api
```

All API methods return a structured envelope:

```json
{
  "ok": true,
  "data": {},
  "warnings": [],
  "messages": []
}
```

Expected failures return:

```json
{
  "ok": false,
  "error": {"code": "VALIDATION_ERROR", "message": "...", "details": {}},
  "warnings": []
}
```

The API does not send outreach, does not perform background CRM conversion, does not create ERPNext Lead / Opportunity / Quotation / Customer records, and does not depend on Milestone 6 report code. Queue endpoints query SEI DocTypes directly.

## Endpoint groups

- Prospects: create, update, fetch, summarize, search.
- Signals: add, update, list, duplicate-check.
- Workflow: qualification recalculation, lifecycle application, ready/rejected/do-not-contact/reopen actions.
- CRM conversion: preview, duplicate search, explicit manager-gated create/link/sync actions.
- Imports and hygiene: import batch creation, dry-run, real import, status/rows, SEI duplicate checks, selected recalculation.
- Queues: operational queue fetches from SEI DocTypes.
- Interaction attribution: create and fetch attribution records.

See the other files in this directory for group-specific details.
