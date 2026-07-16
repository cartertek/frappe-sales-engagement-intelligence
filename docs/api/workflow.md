# Workflow API

Methods:

- `recalculate_qualification(prospect)`
- `apply_lifecycle(prospect)`
- `apply_lifecycle_suggestion(prospect)` legacy alias
- `mark_ready_for_crm_conversion(prospect)` — explicitly marks a prospect ready when CRM readiness requirements pass; otherwise returns a structured checklist of met/unmet requirements.
- `mark_not_ready_for_crm_conversion(prospect)` — clears CRM handoff approval and recomputes the pre-handoff lifecycle.
- `mark_rejected(prospect, reason=None)` manager-only
- `mark_do_not_contact(prospect, reason=None)` manager-only
- `reopen_prospect(prospect)` manager-only

These endpoints delegate to the M3 qualification and lifecycle services and preserve protected-state behavior. A Qualified prospect remains Qualified until `mark_ready_for_crm_conversion` approves CRM handoff. The action sets Find Contact when contact information is missing, or Ready for CRM Conversion when contact information exists. A Find Contact prospect automatically advances to Ready for CRM Conversion when contact information is later added.
