# Message Drafting

Message drafting is a manual support workflow. It renders an SEI Message Template against an SEI Prospect and reports missing variables.

Supported variables:

- `{{ prospect_name }}`
- `{{ website }}`
- `{{ source_arena }}`
- `{{ signal_summary }}`
- `{{ qualification_explanation }}`
- `{{ thesis }}`
- `{{ offer }}`
- `{{ asset_url }}`
- `{{ primary_contact_name }}`
- `{{ primary_contact_role }}`

Workflow:

1. Assign a playbook when useful.
2. Apply playbook defaults only if you want blank offer, guidance, contact notes, or suggested template filled conservatively. Message thesis context is derived from linked signal types.
3. Choose or create a message template.
4. Use Preview Message Draft.
5. Review missing variables, tone, accuracy, source evidence, Do Not Contact status, and channel fit.
6. Copy and send manually outside SEI only after review.

Preview Message Draft does not send email, create a Communication, create a task, create CRM records, or change lifecycle status.
