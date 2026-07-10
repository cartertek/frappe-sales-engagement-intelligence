# Assistant and Script Workflow Conventions

Assistant and script workflows must use the Milestone 7 API as the stable integration boundary. Do not directly mutate DocTypes from scripts unless maintaining the app itself.

Required rules:

- Use structured API success/error envelopes.
- Use queue endpoints instead of report UI internals.
- Never send outreach automatically.
- Never create CRM records without explicit user instruction.
- Never bypass Rejected or Do Not Contact protections.
- Never create ERPNext Lead, Opportunity, Quotation, or Customer records.
- Treat reports as read-only analysis outputs, not mutation sources.

The API returns `{ ok, data, warnings, messages }` on success and `{ ok: false, error, warnings }` on failure.
