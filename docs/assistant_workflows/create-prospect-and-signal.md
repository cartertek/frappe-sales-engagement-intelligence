# Create Prospect and Signal

Use `create_prospect` to create an SEI Prospect, then `add_signal` to attach evidence.

Required pattern:

1. Before any database write, open the exact URL that will be stored and confirm that it contains the expected entity, the expected document or role, and the complete verbatim `observed_fact` quotation. Search snippets, cached text, ATS APIs, job feeds, and reconstructed URLs do not satisfy this requirement.
2. Create the prospect with name, website, source arena, source URL, offer if known, and notes. Do not set a direct prospect thesis; thesis membership is derived from the prospect's signals through each signal type's linked thesis.
3. Write `observed_fact` before choosing a qualifying strength. It must be a verbatim quotation copied from the source, contain at least one complete sentence, and directly support the selected Signal Type. Do not paraphrase or combine separate passages.
4. Put any paraphrase or interpretation in `signal_claim`. If the quoted `observed_fact` does not directly support the selected Signal Type, add the signal as Weak, set it excluded from qualification, and explain the evidence gap. Do not create it as Moderate or Strong.
5. Add a signal with signal type, strength, evidence basis, source URL, source date, structured evidence fields, and counts-toward-qualification only when the evidence standard is met.
6. Read the returned structured envelope and warnings.
7. Read the stored signal and confirm that its `source_url` and `observed_fact` exactly match the URL and quotation verified together before creation. Do not substitute, reconstruct, normalize, or replace the source URL during record creation.
8. Do not create CRM records unless the user explicitly instructs a manager action.

Do not use this workflow to send outreach or bypass protected statuses.
