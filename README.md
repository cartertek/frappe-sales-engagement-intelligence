# Sales Engagement and Intelligence

Custom Frappe app for a sales engagement and outreach intelligence workflow.

Frappe CRM is the primary CRM layer. ERPNext is the downstream ERP layer.

This app must not implement automatic cold email sending, AI auto-send behavior, or any scheduled outreach sender in v1.

## App Identity

- Human-facing name: **Sales Engagement and Intelligence**
- Frappe app/package name: `sales_engagement_intelligence`
- Frappe module name: **Sales Engagement and Intelligence**
- Module package path: `sales_engagement_intelligence/sales_engagement_and_intelligence`

## Milestone 1 Scope

This repository implements the Milestone 1 foundation:

- Installable Frappe app scaffold
- Module shell for future outreach DocTypes
- Workspace fixture shell
- Baseline role fixtures
- Filtered fixture export strategy
- CRM boundary documentation
- Site/environment baseline checklist
- Backup and migration workflow documentation
- No-auto-send policy

Milestone 1 intentionally did **not** implement the outreach data model.


## Milestone 2 Scope

This repository now includes the Milestone 2 engagement intelligence data model source files:

- `SEI Prospect`
- `SEI Signal`
- `SEI Thesis`
- `SEI Asset`
- `SEI Interaction Attribution`
- Informational engagement intelligence custom fields for `CRM Lead` and `CRM Deal`
- Seed records for the canonical Cartertek outreach theses

Milestone 2 remains schema/data-model only. It does not create CRM conversion buttons, CRM records, outreach sending, reports, API endpoints, qualification automation, or ERPNext Lead / Opportunity conversion paths.

## Install

From the bench environment:

```bash
bench get-app https://github.com/cartertek/frappe-sales-engagement-intelligence.git
bench --site <site-name> install-app sales_engagement_intelligence
bench --site <site-name> migrate
bench --site <site-name> list-apps
```

Expected `list-apps` output includes:

```text
sales_engagement_intelligence
```

## Development Loop

For Python, app, or fixture changes:

```bash
bench --site <site-name> migrate
bench build
bench restart
```

For DocType/config changes created through the ERPNext UI:

```bash
bench --site <site-name> export-fixtures
git status
git add .
git commit -m "<change description>"
```

## Fixtures

`hooks.py` uses filtered fixtures for only the Milestone 1 baseline records:

- `Role`
  - `Sales Engagement Manager`
  - `Sales Engagement User`
- `Workspace`
  - `Sales Engagement and Intelligence`

The fixture strategy should stay narrow. Add fixture doctypes only when the app actually owns those records.

## Backup Reminder

Before Milestone 2 creates custom DocTypes, confirm that the target site can be backed up and restored:

```bash
bench --site <site-name> backup --with-files
```

Confirm backup files are created under:

```text
sites/<site-name>/private/backups/
```

Record the restore approach before applying data model migrations to a real site.

## No-Auto-Send Policy

This app must not create or enable:

- Scheduled cold email senders
- Bulk outreach jobs
- AI-generated message auto-send behavior
- Auto-send workflows
- Background jobs that send outreach

ERPNext email account configuration should be left unchanged unless a later milestone explicitly requires read/logging integration.

## Documentation

- [ERPNext CRM Boundary](docs/crm-boundary.md)
- [Site and Environment Baseline](docs/site-environment-baseline.md)
- [Milestone 1 Acceptance Checklist](docs/milestone-1-acceptance.md)
- [Milestone 2 Data Model](docs/milestone-2-data-model.md)
