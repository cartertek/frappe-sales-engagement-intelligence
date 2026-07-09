# Workflow API

Methods:

- `recalculate_qualification(prospect)`
- `apply_lifecycle(prospect)`
- `apply_lifecycle_suggestion(prospect)` legacy alias
- `mark_ready_for_crm_conversion(prospect)`
- `mark_rejected(prospect, reason=None)` manager-only
- `mark_do_not_contact(prospect, reason=None)` manager-only
- `reopen_prospect(prospect)` manager-only

These endpoints delegate to the M3 qualification and lifecycle services and preserve protected-state behavior.
