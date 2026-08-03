# API and Script Workflows

The operator workflow is the single source of procedural guidance for people, assistants, and scripts. Automated clients use the Milestone 7 API as the stable integration boundary; they must not mutate DocTypes directly unless they are maintaining the app itself.

## Required conventions

- Use structured API success and error envelopes.
- Use queue endpoints instead of depending on report UI internals.
- Treat reports as read-only analysis outputs, not mutation sources.
- Never send outreach automatically.
- Never create CRM records without explicit user instruction.
- Never bypass Rejected or Do Not Contact protections.
- Never create ERPNext Lead, Opportunity, Quotation, Customer, or other ERPNext commercial records.

Successful API calls return `{ ok, data, warnings, messages }`. Failures return `{ ok: false, error, warnings }`.

## Research and signal publication

Use the draft-to-published workflow in [Research workflow](research_workflow.md), [Signal evaluation](signal_evaluation.md), and [AI-assisted research](ai_assisted_research.md). Create a Draft Signal when a distinct research assertion becomes plausible, use it as the durable research record, and publish only after exact-source verification and the post-save evidence audit succeed.

For a supported path, search for an existing organization-level Prospect before creating one. `prospect_name` must use the organization's canonical public name; product, platform, migration, initiative, location, and signal context belong on the Signal or in prospect metadata and notes.

Only Published Signals may feed qualification, lifecycle progression, playbook derivation, contact research, or message drafting. Do not create CRM records unless the user explicitly requests the manager-controlled action.

## Imports

Use `create_import_batch`, `dry_run_import`, `get_import_batch_status`, `get_import_batch_rows`, and `run_import` for controlled imports.

Always run a dry run first, review row errors and duplicate outcomes, and run the real import only after operator approval. Imports remain SEI-only and must not create CRM or ERPNext records. Assistant-created rows follow the evidence requirements in [Research to import](research-to-import.md).

## Message drafts

Use `preview_message_draft(prospect, template)` to render a manual-review draft. The endpoint returns the subject, body, missing variables, resolved variables, and safety flags; it does not send outreach or change prospect state.

Save each reviewed prospect-specific result as an unsent row in `SEI Prospect.message_drafts`, following [Message drafting](message-drafting.md). A saved draft is not evidence that outreach occurred.

## CRM conversion

Use `get_ready_for_crm_conversion_queue`, `preview_crm_conversion`, and `find_crm_duplicates` before any create or link action. Manager-only create/link endpoints may be used only after explicit user instruction. Follow [CRM conversion](crm-conversion.md) and preserve all protected-status failures and structured error envelopes.

## Reporting review

Use reports for human analysis and API queue endpoints for scriptable queues. Reporting workflows may summarize patterns, blockers, quality issues, and suggested human next actions, but must not mutate report results, create CRM records, or send outreach.

## Fact-level evidence metadata

`evidence_basis`, `evidence_specificity`, `source_url`, and `source_date` belong to each Observed Facts row, not to the Signal. Classify and cite each fact independently. When a rule requires one of these values, the Signal satisfies the rule when at least one fact row supplies the required value. Do not copy a source classification across unrelated facts merely to satisfy validation.
