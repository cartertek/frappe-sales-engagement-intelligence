# Create Prospect and Signal

Use `create_prospect` to create an SEI Prospect, then `add_signal` to attach evidence.

Required pattern:

1. Before any database write, open the exact URL that will be stored and confirm that it contains the expected entity, the expected document or role, and every complete verbatim quotation and its matching source metadata that will be stored in `observed_facts`. Search snippets, cached text, ATS APIs, job feeds, and reconstructed URLs do not satisfy this requirement.
2. Create the prospect with name, website, source arena, source URL, offer if known, and notes. Do not set a direct prospect thesis; thesis membership is derived from the prospect's signals through each signal type's linked thesis.
3. Create a short descriptive signal name that identifies the specific observed event, condition, or evidence; do not use only the prospect name or Signal Type.
4. Build `observed_facts` before choosing a qualifying strength. Supply a list of fact rows, each containing one verbatim quotation plus that fact's `evidence_basis`, `evidence_specificity`, `source_url`, and `source_date`. One fact is required; add multiple facts whenever needed to support all claims. Do not paraphrase or splice separate passages into one fact.
5. Put any paraphrase or interpretation in `signal_claim`. If the listed `observed_facts` does not directly support the selected Signal Type, add the signal as Weak, set it excluded from qualification, and explain the evidence gap. Do not create it as Moderate or Strong.
6. Add a signal with the descriptive name, signal type, strength, fact rows, structured evidence fields, and counts-toward-qualification only when the evidence standard is met. Do not send `evidence_basis`, `evidence_specificity`, `source_url`, or `source_date` as Signal-level fields.
7. Read the returned structured envelope and warnings.
8. Read the stored signal and confirm that every `observed_facts` row exactly matches the verified quotation and its own source URL, source date, evidence basis, and specificity. Do not substitute, reconstruct, normalize, or replace the source URL during record creation.
9. Do not create CRM records unless the user explicitly instructs a manager action.

Do not use this workflow to send outreach or bypass protected statuses.


Each Observed Facts row stores its own `source_url`, `source_date`, `evidence_basis`, and `evidence_specificity`. At least one fact must supply any value required for the signal; multiple facts may use different sources and evidence classifications.

## Fact-level evidence metadata

`evidence_basis`, `evidence_specificity`, `source_url`, and `source_date` belong to each Observed Facts row, not to the Signal. Classify and cite each fact independently. When a rule requires one of these values, the signal satisfies the rule when at least one fact row supplies the required value. Do not copy a source classification across unrelated facts merely to satisfy validation.
