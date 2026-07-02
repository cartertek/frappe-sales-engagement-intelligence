# Milestone 2 Data Model

Milestone 2 implements the Sales Engagement and Intelligence data foundation upstream of Frappe CRM.

The app stores Cartertek-specific pre-CRM intelligence:

- Prospect research
- Signal evidence
- Observed vs. inferred evidence distinction
- Signal strength
- Qualification preparation fields
- Outreach thesis and offer alignment
- Supporting assets
- Thin attribution back to Frappe CRM activity records

Frappe CRM remains the owner of qualified leads, deals, lead/deal activity, notes, tasks, calls, email templates, pipeline views, assignments, and follow-up behavior.

ERPNext remains downstream for quotation, customer, accounting, and ERP records.

## Implemented DocTypes

- `SEI Prospect`
- `SEI Signal`
- `SEI Thesis`
- `SEI Asset`
- `SEI Interaction Attribution`

## Frappe CRM Link-Back Fields

Milestone 2 adds informational engagement intelligence context fields to Frappe CRM records through an idempotent patch.

### CRM Lead

- `sei_prospect`
- `sei_source_arena`
- `sei_thesis`
- `sei_qualification_summary`

### CRM Deal

- `sei_prospect`
- `sei_source_arena`
- `sei_thesis`
- `sei_primary_signal`

These fields are navigation and context fields only. They do not create conversion behavior.

## Seed Thesis Records

The app seeds these canonical Cartertek outreach thesis records:

- Agency Technical Reinforcement
- Project Rescue
- Post-Launch Stabilization
- Hiring-Gap Substitution
- Workflow Integration
- AI Workflow Implementation
- Production-Readiness Cleanup
- Technical Diagnostic / Second Set of Eyes

## Basic Validation Boundary

Milestone 2 only includes basic data-validity checks:

- `SEI Prospect.website` populates `normalized_domain`.
- `SEI Prospect.do_not_contact` forces lifecycle status to `Do Not Contact`.
- `SEI Prospect.qualification_status = Do Not Contact` checks `do_not_contact` and sets lifecycle status to `Do Not Contact`.
- `SEI Prospect.manual_qualification_override` requires `manual_qualification_reason`.
- `SEI Signal` warns when an inferred signal is marked as counting toward qualification.

The qualification engine belongs to Milestone 3.

## Default Conversion Decisions for Milestone 3

### Default CRM Lead Status

Default CRM Lead status: **New**

Reason: a converted SEI Prospect is entering Frappe CRM as a qualified or prepared lead, but Frappe CRM should still own the lead activity lifecycle after conversion.

### Default CRM Deal Status

Default CRM Deal status/stage: **first active/open stage in the installed Frappe CRM pipeline**

Reason: Milestone 2 must not assume a site-specific deal pipeline. Direct deal creation should only happen after positive interest, meeting booking, or a commercial conversation, and Milestone 3/4 conversion logic should resolve the installed pipeline stage at runtime.

### Default Conversion Shape

Recommended default conversion shape:

- Create `CRM Lead + CRM Organization` when company identity is known.
- Create `CRM Contacts` only when a specific person or contact path has been verified.
- Create `CRM Deal` only after positive interest, meeting booked, or commercial conversation.

Milestone 2 does not implement conversion actions.

## Explicit Non-Goals Preserved

Milestone 2 does not implement:

- Qualification scoring engine
- Lifecycle automation
- CRM conversion buttons
- CRM Lead creation logic
- CRM Deal creation logic
- CRM Organization creation logic
- CRM Contacts creation logic
- Combined CSV importer
- Reports or dashboard charts
- REST/API endpoints
- Scheduled follow-up jobs
- Sequence templates
- Research task queues
- Playbooks
- Email automation
- AI message generation
- Automatic ERPNext quotation/customer behavior
- ERPNext Lead / Opportunity conversion path

## Runtime Validation Required

The source changes must still be validated in a real bench/container environment:

```bash
bench --site <site-name> backup --with-files
bench --site <site-name> migrate
bench build
bench restart
```

Confirm after migration:

- The five engagement intelligence DocTypes exist.
- The CRM Lead and CRM Deal custom fields exist.
- The thesis seed records exist.
- The Sales Engagement and Intelligence workspace shows the engagement intelligence DocTypes.
- ERPNext still loads.
- Frappe CRM still loads.
- No automatic outreach sending is enabled.
- No ERPNext Lead / Opportunity conversion path exists.
