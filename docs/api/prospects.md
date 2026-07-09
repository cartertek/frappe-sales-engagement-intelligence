# Prospect API

Methods:

- `create_prospect(payload)`
- `update_prospect(prospect, payload)`
- `get_prospect(prospect)`
- `get_prospect_summary(prospect)`
- `find_prospects(filters=None, limit=50)`

Generic create/update ignores restricted workflow and CRM-link fields such as `qualification_status`, `lifecycle_status`, `crm_lead`, `crm_deal`, `do_not_contact`, and `rejected_reason`. Use workflow or CRM endpoints for those actions.

Workflow-relevant updates trigger qualification/lifecycle recalculation where appropriate. Protected prospects require manager access for API updates.
