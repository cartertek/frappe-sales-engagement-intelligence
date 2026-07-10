# Import and Review

Use `create_import_batch`, `dry_run_import`, `get_import_batch_status`, `get_import_batch_rows`, and `run_import` for controlled import workflows.

Run dry run first. Review row errors and duplicate outcomes. Only run the real import after the operator approves the dry run. Imports remain SEI-only and must not create CRM or ERPNext records.
