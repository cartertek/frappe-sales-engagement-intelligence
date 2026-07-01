# Milestone 1 Acceptance Checklist

Milestone 1 is complete when the target Frappe/ERPNext/Frappe CRM environment confirms:

- [x] The standalone `crm` app is installed.
- [x] `list-apps` shows `crm`.
- [x] `sales_engagement_intelligence` is installed.
- [x] `migrate` succeeds.
- [x] ERPNext still loads.
- [x] Frappe CRM loads.
- [x] Frappe CRM and ERPNext coexist without obvious routing or permission conflicts.
- [x] CRM Lead and CRM Deal exact DocType names are identified.
- [x] CRM task, note, call-log, email-template, and activity records are identified where present.
- [x] The CRM to ERPNext quotation/customer path is documented.
- [x] The Sales Engagement and Intelligence module exists.
- [x] The workspace exists and does not duplicate Frappe CRM lead/deal views.
- [x] Baseline custom roles exist.
- [x] Role/workspace fixtures are filtered to app-owned records.
- [x] A backup has been created and its location is known.
- [x] No outbound outreach automation has been enabled.
- [x] Milestone 2 can begin with Frappe CRM Lead / Deal as the target.

## Notes

- Standalone Frappe CRM target DocTypes are documented in `docs/frappe-crm-baseline.md`.
- Site/environment and backup baseline are documented in `docs/site-environment-baseline.md`.
- Browser smoke test was completed by the operator after the SEI desktop/icon fixes.
- ERPNext CRM `Lead` / `Opportunity` still exist on the site, but M2 targets standalone Frappe CRM `CRM Lead` / `CRM Deal`.
