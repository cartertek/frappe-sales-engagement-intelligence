# Research, Draft, and Publish a Signal

Use a Draft Signal as the durable working record for each plausible research path. The draft may exist before an SEI Prospect. Create or identify the Prospect only after the path remains supported, then attach and publish the completed Signal.

Required pattern:

1. As soon as a plausible path appears, create a Draft Signal. Do this even when the Prospect has not been created and even when most Signal fields are still unknown.
2. Keep one draft per distinct research path. Fill it incrementally with candidate facts, exact URLs, source dates, evidence classifications, analysis, possible Signal Type, disqualifiers, and uncertainty.
3. Before treating any fact as verified, open its exact source URL and confirm the expected entity, document or role, and complete verbatim quotation. Search snippets, cached text, ATS APIs, job feeds, and reconstructed URLs are discovery context only.
4. Revise the draft whenever later evidence changes the interpretation. Remove unsupported facts rather than preserving them to justify the path.
5. If the path is disproven, delete the Draft Signal. Do not create a Prospect for a failed path.
6. If the path remains supported, create or identify the Prospect and link the Draft Signal to it.
7. Finish the Signal: give it a descriptive name, complete the Observed Facts rows and their fact-level metadata, select the managed Signal Type and strength, complete the structured analysis, and check all disqualifiers and guardrails.
8. Publish the Signal. Publication must succeed through the normal required-field and evidence validation; do not bypass it or set status directly.
9. Read the stored Published Signal and confirm every fact and source field matches the verified evidence. Only then may the Signal feed qualification, lifecycle, playbook derivation, or message context.
10. Do not create CRM records unless the user explicitly instructs a manager action.

Do not use this workflow to send outreach or bypass protected statuses.


Each Observed Facts row stores its own `source_url`, `source_date`, `evidence_basis`, and `evidence_specificity`. At least one fact must supply any value required for the signal; multiple facts may use different sources and evidence classifications.

## Fact-level evidence metadata

`evidence_basis`, `evidence_specificity`, `source_url`, and `source_date` belong to each Observed Facts row, not to the Signal. Classify and cite each fact independently. When a rule requires one of these values, the signal satisfies the rule when at least one fact row supplies the required value. Do not copy a source classification across unrelated facts merely to satisfy validation.
