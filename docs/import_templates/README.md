# SEI Import Templates

These templates support Milestone 5 SEI-only intake. They create or update **SEI Prospect** and **SEI Signal** records only. They do not create, update, inspect, or deduplicate against Frappe CRM or ERPNext CRM records.

## Files

- `sei_prospect_import_template.csv` — prospect-only research list import.
- `sei_signal_import_template.csv` — additional signal import for existing prospects.
- `sei_prospect_with_initial_signal_template.csv` — common combined workflow: one prospect plus its first signal per row.

## Required columns

Prospect creation requires `prospect_name` and at least one context field: `website`, `source_url`, `source_arena`, or `primary_contact_email`.

Signal creation requires `signal_type`, `signal_strength`, `evidence_basis`, and `evidence_notes`. In the combined template these are prefixed as `initial_signal_*`.

Signal-only import must match an existing prospect by `prospect_name`, `prospect_website`, or `prospect_normalized_domain`; it will not create a prospect.

## Allowed values

Use the Select values configured on the current SEI DocTypes. Common values include:

- Prospect Type: `Agency`, `Startup`, `SMB`, `Enterprise`, `Ecosystem Partner`, `Directory Lead`, `Community Lead`, `Procurement Lead`, `Referral Partner`, `Other`.
- Signal Type: `Failed Recruitment`, `Technical Distress`, `Launch Aftermath`, `Agency Overflow`, `Ecosystem Adjacency`, `Vendor`, `Directory Presence`, `Community Request`, `Procurement Visibility`, `Credibility`, `Referral Signal`, `Reactivation Signal`, `Other`.
- Signal Strength: `Weak`, `Moderate`, `Strong`.
- Evidence Basis: `Observed`, `Inferred`.

## Dates and booleans

Dates should use `YYYY-MM-DD`. Boolean fields accept `1`, `0`, `true`, `false`, `yes`, `no`, `y`, or `n`.

## Thesis resolution

Prospect thesis is not imported as a direct field. A prospect's thesis list is derived from its linked signal types: `SEI Signal.signal_type -> SEI Signal Type.thesis`. Legacy `sei_thesis` / `thesis` columns are accepted only for validation/backward compatibility and are not stored on the prospect.

## Duplicate detection

Prospect duplicates are checked only against `SEI Prospect`, in this order: `normalized_domain`, exact `website`, `primary_contact_email`, exact `prospect_name`, and `source_url`.

Signal duplicates are checked only against `SEI Signal` by `prospect + source_url`, then by `prospect + signal_type + source_date`.

## Dry run

Dry run parses rows, validates required data, resolves managed signal types, detects SEI duplicates, classifies intended actions, and writes row outcomes to the import batch. It creates no prospects, no signals, and no CRM records.

## Import behavior

Import modes are:

- `Create Only` — create new records; skip duplicates.
- `Update Existing` — update matched records; fail/skip rows with no match.
- `Create or Update` — create new records and update matched records.
- `Dry Run` — preview only.

After real imports, affected prospects are recalculated through the Milestone 3 qualification and lifecycle services. Protected `Do Not Contact` and `Rejected` behavior is preserved. Ordinary imports should not be used to bypass workflow rules.

## Row errors

Each row is recorded under `SEI Import Batch Row` with status, action, created or matched SEI links, raw row JSON, and error text.

## What import does not do

Milestone 5 import does not query or mutate CRM Lead, CRM Deal, CRM Organization, CRM Contacts, ERPNext Lead, ERPNext Opportunity, ERPNext Quotation, or ERPNext Customer. It also does not send outreach, run scheduled imports, scrape websites, expose external APIs, or run playbook automation.
