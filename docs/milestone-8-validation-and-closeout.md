# Milestone 8 Validation and Closeout Matrix

Milestone 8 completes the SEI outreach operating system. Use this matrix for final production closeout.

## Production-safe runtime validation

- Run `bench migrate --skip-search-index`.
- Validate `/desk/prospecting` and `/desk/engagement-reports` route availability.
- Run `sales_engagement_intelligence.setup.validate_milestone_6_workspace_reports`.
- Run `sales_engagement_intelligence.setup.validate_milestone_8_workspace_items`.
- Smoke test report execution from Engagement Reports.
- Smoke test API endpoints for prospect creation, signal creation, queues, CRM preview, and message draft preview.
- Scan recent backend logs for migration, workspace, report, and API errors.

Do not treat `bench build` inside the production backend container as required runtime validation. Build validation belongs in CI, image build, or a designated non-production environment.

## CI / image build validation

- Python compile for app modules.
- Static tests for DocType JSON, report registration, API registration, workspace metadata, and prohibited automation boundaries.
- Fixture and DocType JSON validity.
- Report registration tests.
- API registration tests.
- Image build where applicable.
- `bench build` only in CI, image build, or non-production validation.

## Browser/UI validation

Validate the following in Desk:

- Prospecting workspace.
- Engagement Reports workspace.
- SEI Prospect form.
- SEI Import Batch form.
- SEI Playbook form.
- SEI Message Template form.
- CRM Lead SEI tab.
- CRM Deal SEI tab.
- Message draft preview dialog.
- Conversion preview/create/link dialogs.
- Report shortcuts.
- Workspace/sidebar rendering.

## API/script validation

Validate structured success/error envelopes for:

- `create_prospect`.
- `add_signal`.
- Workflow actions.
- Queue endpoints.
- Import dry run and execution.
- CRM preview and conversion/linking endpoints.
- Interaction attribution.
- `preview_message_draft`.
- Permission-negative cases.

## End-to-end scenarios

1. Import a prospect list with dry run, then real import. Confirm SEI Prospect and SEI Signal creation, qualification recalculation, lifecycle update, import row outcomes, and no CRM creation.
2. Assign a playbook, apply defaults, and preview a message draft. Confirm thesis/offer/guidance fills blank fields only, missing variables are reported, no message is sent, and lifecycle does not change.
3. Mark a qualified prospect ready for CRM conversion, preview duplicates, and explicitly create/link CRM Lead, Organization, Contact, and Deal where appropriate. Confirm no ERPNext records are created.
4. Create SEI Interaction Attribution and confirm attribution appears in reports.
5. Use API examples for prospect, signal, queues, draft preview, and CRM preview. Confirm structured envelopes and protections.
6. Run data hygiene utilities and review report outputs. Confirm utilities operate safely and reports do not mutate records.

## Safety audit

Confirm all prohibited automation remains absent:

- No automatic cold email sending.
- No bulk outreach sending.
- No AI auto-send.
- No automatic LinkedIn sending.
- No contact-form automation.
- No automatic CRM conversion from import or qualification.
- No ERPNext Lead, Opportunity, Quotation, Customer creation.
- Do Not Contact and Rejected protections cannot be bypassed through UI or API.
- Manager-only conversion actions remain protected.
- Reports are read-only.
- Imports remain SEI-only.
- Draft preview does not send a message or create a Communication.

## Completion definition

Milestone 8 is complete when migration, workspace validators, report smoke tests, API smoke tests, browser validation, end-to-end scenario validation, log scan, and this safety audit all pass, and the final implementation status is committed and merged.
