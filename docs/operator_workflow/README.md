# SEI Operator Workflow

This guide is the operating manual for the completed Sales Engagement Intelligence system. The system supports research intake, signal evidence, qualification, playbook guidance, manual message drafting, explicit Frappe CRM conversion/linking, interaction attribution, reporting, API/script workflows, and data hygiene.

The system does not send outreach automatically. Operators draft and send messages manually through the appropriate channel after reviewing the prospect, signal evidence, playbook, and safety status.

## Evidence-first principle

A signal is not what the source reminds us of.
A signal is what the source directly supports.

Use this order:

1. Observed evidence first.
2. Inference second.
3. Qualification last.

Cartertek fit is not signal evidence. A company can look like a good prospect, or describe work Cartertek could do, without proving a managed SEI Signal Type.

## End-to-end flow

1. Create Draft Signals as soon as plausible research paths appear, including before a Prospect exists.
2. Fill and revise each draft while researching its path.
3. Delete drafts whose paths are disproven.
4. For a supported path, create or identify the Prospect, link the draft, complete it, and publish the Signal.
5. Review import rows, duplicate warnings, and missing evidence.
6. Review queues: Needs Research, Research Complete, Find Contact, Ready for CRM Conversion, Rejected, and Do Not Contact.
7. Confirm qualification, lifecycle, observed/inferred evidence, and contact path.
8. Develop prospect positioning from the Prospect's Published Signals, managed Signal Types, Playbook, and source evidence.
9. Choose the applicable offer, asset, contact, and message template.
10. Draft the message, review it, and save the approved result as an unsent row in the Prospect's Message Drafts table. Saving the draft must not change lifecycle status or mark the draft sent.
11. Manually send the message through the intended channel. Only after an actual send should the saved draft be marked sent and the real interaction be logged.
12. Explicitly create or link Frappe CRM records when appropriate and use reports to evaluate outcomes.

## Evidence-first research flow

1. Find a plausible research path and create a Draft Signal immediately; a Prospect is not required yet.
2. Add source candidates, complete quotations, source metadata, analysis, and uncertainty to the draft as research proceeds.
3. Put paraphrase or interpretation in Signal Claim and compare the facts against the managed Signal Type definition.
4. Check disqualifiers and revise the draft whenever new evidence changes the path.
5. Delete the draft if the path is disproven.
6. If supported, create or identify the Prospect, link the draft, complete all publication requirements, and publish it.
7. Let qualification and lifecycle logic advance only Published Signals.
8. Use reviewer feedback to improve future evaluation.

## Where rules live

Signal Type-specific rules live in the managed SEI Signal Type records.

Operator docs explain the research and evaluation workflow. They do not duplicate Signal Type definitions. Where type-specific criteria are needed, refer to the managed SEI Signal Type definition.

## Responsibility boundaries

SEI owns research, qualification, lifecycle queues, playbooks, templates, draft preview, attribution, import batches, API support, and reporting.

Frappe CRM owns sales execution records: CRM Lead, CRM Organization, Contact, CRM Deal, CRM notes, CRM tasks, and sales workspaces.

ERPNext records are not created by SEI. SEI does not create ERPNext Lead, Opportunity, Quotation, Customer, or Customer-facing commercial records.

## Required safety checks

Before outreach or CRM conversion, confirm the prospect is not Rejected and not Do Not Contact. Draft preview and draft saving do not change lifecycle status, create a Communication, mark a prospect contacted, or send email. Save reviewed drafts in the Prospect's Message Drafts table with `sent` unchecked and `sent_on` empty. Imports do not create CRM records. Reports are read-only.

## Related pages

- [Research workflow](research_workflow.md)
- [Signal evaluation](signal_evaluation.md)
- [Review feedback](review_feedback.md)
- [AI-assisted research](ai_assisted_research.md)
- [Research to import](research-to-import.md)
- [Prospect review](prospect-review.md)
- [Prospect identity and contact research](identity-contact-research.md)
- [Qualification](qualification.md)
- [CRM conversion](crm-conversion.md)
- [Prospect positioning](prospect-positioning.md)
- [Message drafting](message-drafting.md)
- [Interaction attribution](interaction-attribution.md)
- [Reporting feedback loop](reporting-feedback-loop.md)
- [Data hygiene](data-hygiene.md)
- [Import templates](../import_templates/README.md)
- [API and script workflows](api-script-workflows.md)
- [API documentation](../api/README.md)


Each Observed Facts row stores its own `source_url`, `source_date`, `evidence_basis`, and `evidence_specificity`. At least one fact must supply any value required for the signal; multiple facts may use different sources and evidence classifications.

## Fact-level evidence metadata

`evidence_basis`, `evidence_specificity`, `source_url`, and `source_date` belong to each Observed Facts row, not to the Signal. Classify and cite each fact independently. When a rule requires one of these values, the signal satisfies the rule when at least one fact row supplies the required value. Do not copy a source classification across unrelated facts merely to satisfy validation.
