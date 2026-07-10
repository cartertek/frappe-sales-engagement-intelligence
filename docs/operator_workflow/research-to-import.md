# Research to Import

Use import batches when research produces structured prospect or signal rows. Use the templates in `docs/import_templates/` for prospect-only imports, signal-only imports, and prospect-with-initial-signal imports.

1. Create an SEI Import Batch with source type, source arena, source URL, import kind, mode, and import file.
2. Run a dry run first. Dry run validates rows, duplicate handling, and expected actions without creating or updating SEI records.
3. Review SEI Import Batch Row outcomes, especially failed rows, skipped duplicates, missing required fields, and evidence warnings.
4. Fix source data or import settings.
5. Run the real import only after dry run results are acceptable.

Imports create or update SEI records only. They do not create Frappe CRM records, ERPNext records, emails, Communications, tasks, or outreach.
