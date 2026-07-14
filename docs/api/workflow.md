# Workflow API

Methods:

- `recalculate_qualification(prospect)`
- `apply_lifecycle(prospect)`
- `apply_lifecycle_suggestion(prospect)` legacy alias
- `mark_ready_for_crm_conversion(prospect)` — explicitly marks a prospect ready when CRM readiness requirements pass; otherwise returns a structured checklist of met/unmet requirements.
- `mark_rejected(prospect, reason=None)` manager-only
- `mark_do_not_contact(prospect, reason=None)` manager-only
- `reopen_prospect(prospect)` manager-only

These endpoints delegate to the M3 qualification and lifecycle services and preserve protected-state behavior. Lifecycle suggestions never set Ready for CRM Conversion; that lifecycle state is only set by the explicit `mark_ready_for_crm_conversion` action.
