# Import and Review

Use `create_import_batch`, `dry_run_import`, `get_import_batch_status`, `get_import_batch_rows`, and `run_import` for controlled import workflows.

Run dry run first. Review row errors and duplicate outcomes. Only run the real import after the operator approves the dry run. Imports remain SEI-only and must not create CRM or ERPNext records.

## Assistant-created import rows

For assistant-created import rows, Moderate and Strong signals are allowed only when `observed_fact` directly asserts the selected managed Signal Type. If the row contains context, a job title, company scale, technical work area, or an inferred Cartertek fit instead of the signal assertion, import it as Weak and excluded from qualification, or reject the row.

Do not use `signal_claim`, `why_this_signal_type`, `why_not_weak`, or `evidence_notes` to turn a non-signal `observed_fact` into a qualifying signal.
