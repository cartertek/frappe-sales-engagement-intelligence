# Create Prospect and Signal

Use `create_prospect` to create an SEI Prospect, then `add_signal` to attach evidence.

Required pattern:

1. Before any database write, open the exact URL that will be stored and confirm that it contains the expected entity, the expected document or role, and all complete verbatim quotations that will be stored in `observed_facts`. Search snippets, cached text, ATS APIs, job feeds, and reconstructed URLs do not satisfy this requirement.
2. Create the prospect with name, website, source arena, source URL, offer if known, and notes. Do not set a direct prospect thesis; thesis membership is derived from the prospect's signals through each signal type's linked thesis.
3. Create a short descriptive signal name that identifies the specific observed event, condition, or evidence; do not use only the prospect name or Signal Type.
4. Build `observed_facts` before choosing a qualifying strength. Supply a list of fact rows, each containing a verbatim quotation of at least one complete source sentence. One fact is required; add multiple facts whenever needed to support all claims. Do not paraphrase or splice separate passages into one fact.
5. Put any paraphrase or interpretation in `signal_claim`. If the listed `observed_facts` does not directly support the selected Signal Type, add the signal as Weak, set it excluded from qualification, and explain the evidence gap. Do not create it as Moderate or Strong.
6. Add a signal with the descriptive name, signal type, strength, evidence basis, source URL, source date, structured evidence fields, and counts-toward-qualification only when the evidence standard is met.
7. Read the returned structured envelope and warnings.
8. Read the stored signal and confirm that its `source_url` and every `observed_facts` row exactly match the verified URL and quotations verified together before creation. Do not substitute, reconstruct, normalize, or replace the source URL during record creation.
9. Do not create CRM records unless the user explicitly instructs a manager action.

Do not use this workflow to send outreach or bypass protected statuses.
