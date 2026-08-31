# Research to Import

Use import batches when research produces structured prospect or signal rows. Use the templates in `docs/import_templates/` for prospect-only imports, signal-only imports, and prospect-with-initial-signal imports.

1. Create an SEI Import Batch with source type, source arena, source URL, import kind, mode, and import file.
2. Run a dry run first. Dry run validates rows, duplicate handling, and expected actions without creating or updating SEI records.
3. Review SEI Import Batch Row outcomes, especially failed rows, skipped duplicates, missing required fields, and evidence warnings.
4. Fix source data or import settings.
5. Run the real import only after dry run results are acceptable.

Imports create or update SEI records only. They do not create Frappe CRM records, ERPNext records, emails, Communications, tasks, or outreach.

## Assistant-created signal rows

Assistant-created import rows must follow the signal evaluation standard in `docs/operator_workflow/signal_evaluation.md`. A Moderate or Strong signal requires at least one Observed Facts row containing a complete verbatim source sentence. The flat CSV accepts one `observed_fact` column and creates one row; add further facts through the managed table or API when needed to support all claims. Put all paraphrase and interpretation in `signal_claim`. If the facts do not support the signal, import it as Weak or reject it before import.

The Import Batch `source_arena` is provenance metadata. Source Arena values are managed through `SEI Signal Source Arena`, and imports automatically create a missing managed value when needed. During Combined Prospect + Initial Signal and Signal Only imports, a row-level `source_arena` is written to `SEI Signal.source_arena`; when the row leaves it blank, the Import Batch `source_arena` is used as the default. This is distinct from the Signal Type's Research Arena.
