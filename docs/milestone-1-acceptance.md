# Milestone 1 Acceptance Checklist

Milestone 1 is complete when the target ERPNext environment confirms all of the following:

- [ ] The app exists under `apps/sales_engagement_intelligence`.
- [ ] The app is installed on the target ERPNext site.
- [ ] `bench --site <site-name> list-apps` shows `sales_engagement_intelligence`.
- [ ] `bench --site <site-name> migrate` completes successfully.
- [ ] The module `Sales Engagement and Intelligence` exists.
- [ ] The workspace `Sales Engagement and Intelligence` exists or imports from fixture cleanly.
- [ ] The roles `Sales Engagement Manager` and `Sales Engagement User` exist.
- [ ] The app scaffold is committed to Git.
- [ ] Fixtures for roles/workspace are exported or intentionally maintained as source fixtures.
- [ ] ERPNext CRM object boundaries are documented.
- [ ] Backup creation has been tested with `bench --site <site-name> backup --with-files`.
- [ ] No outbound email automation has been created or enabled.
- [ ] The app is ready for Milestone 2 DocType implementation.

## Not Included in Milestone 1

Do not add these until Milestone 2 or later:

- Outreach Prospect
- Outreach Signal
- Outreach Thesis
- Outreach Asset
- Outreach Touchpoint
- Qualification engine
- Lifecycle engine
- CRM conversion buttons
- CSV import workflow
- Reports
- API endpoints
- Email sending automation
- Sequence templates
- Playbooks
- Research task queues
