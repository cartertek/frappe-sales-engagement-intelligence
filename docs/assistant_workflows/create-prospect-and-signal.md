# Create Prospect and Signal

Use `create_prospect` to create an SEI Prospect, then `add_signal` to attach evidence.

Required pattern:

1. Create the prospect with name, website, source arena, source URL, offer if known, and notes. Do not set a direct prospect thesis; thesis membership is derived from the prospect's signals through each signal type's linked thesis.
2. Add a signal with signal type, strength, evidence basis, source URL, source date, evidence notes, and counts-toward-qualification.
3. Read the returned structured envelope and warnings.
4. Do not create CRM records unless the user explicitly instructs a manager action.

Do not use this workflow to send outreach or bypass protected statuses.
