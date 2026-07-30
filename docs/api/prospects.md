# Prospect API

Methods:

- `create_prospect(payload)`
- `update_prospect(prospect, payload)`
- `get_prospect(prospect)`
- `get_prospect_summary(prospect)`
- `find_prospects(filters=None, limit=50)`

Generic create/update ignores restricted workflow and CRM-link fields such as `qualification_status`, `lifecycle_status`, `crm_lead`, `crm_deal`, `do_not_contact`, and `rejected_reason`. Use workflow or CRM endpoints for those actions.

Workflow-relevant updates trigger qualification/lifecycle recalculation where appropriate. Protected prospects require manager access for API updates.

## Prospect identity and naming

`prospect_name` is the canonical public name of the organization or entity represented by the Prospect. It is not a descriptive research label. Do not append product names, platforms, systems, migrations, initiatives, locations, signals, or other discovery context. Store those details in Signals, metadata, source notes, or positioning fields.

Use organization-level identity values for `website` and `normalized_domain` when available, and search for an existing Prospect representing the organization before creating a new record. Different products or initiatives owned by one organization normally belong to the same Prospect; create separate Prospects only for genuinely separate legal or operating entities that should be tracked independently.

## Preview message draft

Use `sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_message_draft` to render an SEI Message Template against an SEI Prospect for manual review.

Inputs:

- `prospect`: SEI Prospect name.
- `template`: SEI Message Template name.

The response follows the structured API envelope and returns `subject`, `body`, `missing_variables`, resolved `variables`, and safety flags. This endpoint does not send outreach, create a Communication, create CRM records, or change lifecycle status.
