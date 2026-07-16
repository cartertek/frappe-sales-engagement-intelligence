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

1. Import or manually create prospects and signals.
2. Review import rows, duplicate warnings, and missing evidence.
3. Review queues: Needs Research, Find Contact, Qualified, Ready for CRM Conversion, Rejected, and Do Not Contact.
4. Confirm qualification, lifecycle, observed/inferred evidence, and contact path.
5. Assign a playbook and choose the offer and asset. Confirm the relevant theses are represented by the prospect's linked signal types.
6. Preview a message draft from a message template.
7. Send manually outside SEI only after review.
8. Explicitly create or link Frappe CRM Lead, Organization, Contact, and Deal records when appropriate.
9. Log interaction attribution.
10. Use reports to evaluate sources, theses, assets, offers, channels, and outcomes.

## Evidence-first research flow

1. Find a candidate source.
2. Copy at least one complete source sentence verbatim into Observed Fact. Do not paraphrase or combine passages.
3. Put any paraphrase or interpretation in Signal Claim, then compare the quoted Observed Fact against the managed Signal Type definition.
4. Check obvious disqualifiers.
5. Assign strength conservatively.
6. Record the evidence note and structured evidence fields.
7. Let qualification and lifecycle logic advance only evidence-backed signals.
8. Use reviewer feedback to improve future evaluation.

## Where rules live

Signal Type-specific rules live in the managed SEI Signal Type records.

Operator docs explain the research and evaluation workflow. They do not duplicate Signal Type definitions. Where type-specific criteria are needed, refer to the managed SEI Signal Type definition.

## Responsibility boundaries

SEI owns research, qualification, lifecycle queues, playbooks, templates, draft preview, attribution, import batches, API support, and reporting.

Frappe CRM owns sales execution records: CRM Lead, CRM Organization, Contact, CRM Deal, CRM notes, CRM tasks, and sales workspaces.

ERPNext records are not created by SEI. SEI does not create ERPNext Lead, Opportunity, Quotation, Customer, or Customer-facing commercial records.

## Required safety checks

Before outreach or CRM conversion, confirm the prospect is not Rejected and not Do Not Contact. Draft preview does not change lifecycle status, create a Communication, or send email. Imports do not create CRM records. Reports are read-only.

## Related pages

- [Research workflow](research_workflow.md)
- [Signal evaluation](signal_evaluation.md)
- [Review feedback](review_feedback.md)
- [AI-assisted research](ai_assisted_research.md)
- [Research to import](research-to-import.md)
- [Prospect review](prospect-review.md)
- [Qualification](qualification.md)
- [CRM conversion](crm-conversion.md)
- [Message drafting](message-drafting.md)
- [Interaction attribution](interaction-attribution.md)
- [Reporting feedback loop](reporting-feedback-loop.md)
- [Data hygiene](data-hygiene.md)
- [Import templates](../import_templates/README.md)
- [API documentation](../api/README.md)
