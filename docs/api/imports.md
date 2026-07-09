# Import and Hygiene API

Methods:

- `create_import_batch(payload)`
- `dry_run_import(batch)`
- `run_import(batch)` manager-only
- `run_import_batch(batch, dry_run=1)` compatibility wrapper
- `reset_import_batch_to_draft(batch)` manager-only
- `get_import_batch_status(batch)`
- `get_import_batch_rows(batch, filters=None)`
- `find_duplicate_sei_prospects(filters=None)`
- `find_duplicate_sei_signals(filters=None)`
- `backfill_normalized_domains(limit=None, dry_run=True)` manager-only
- `recalculate_selected_prospects(prospects)` manager-only
- `apply_lifecycle_to_selected_prospects(prospects)` manager-only

Import endpoints are SEI-only. Dry-run creates rows but no Prospect/Signal records. Real import creates or updates only SEI records and does not query or mutate Frappe CRM or ERPNext records.
