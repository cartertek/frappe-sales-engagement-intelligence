# Create Prospect and Signal

Use `create_prospect` to create an SEI Prospect, then `add_signal` to attach evidence.

Required pattern:

1. Create the prospect with name, website, source arena, source URL, offer if known, and notes. Do not set a direct prospect thesis; thesis membership is derived from the prospect's signals through each signal type's linked thesis.
2. Write `observed_fact` before choosing a qualifying strength. It must be a verbatim quotation copied from the source, contain at least one complete sentence, and directly support the selected Signal Type. Do not paraphrase or combine separate passages.
3. Put any paraphrase or interpretation in `signal_claim`. If the quoted `observed_fact` does not directly support the selected Signal Type, add the signal as Weak, set it excluded from qualification, and explain the evidence gap. Do not create it as Moderate or Strong.
4. Add a signal with signal type, strength, evidence basis, source URL, source date, structured evidence fields, and counts-toward-qualification only when the evidence standard is met.
5. Read the returned structured envelope and warnings.
6. Do not create CRM records unless the user explicitly instructs a manager action.

Do not use this workflow to send outreach or bypass protected statuses.
