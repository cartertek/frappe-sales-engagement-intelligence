# Message Drafting

Message drafting is a manual support workflow. It renders an SEI Message Template against an SEI Prospect, reports missing variables, and saves the reviewed result as an unsent row in the Prospect's **Message Drafts** table. Drafting is a record-preparation action, not an outreach, lifecycle, or CRM action.

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
6. Save each approved draft to the Prospect's **Message Drafts** table with the intended platform, sender, recipient, subject, and body.
7. Leave `sent` unchecked and `sent_on` empty. Saving a draft must not change the Prospect's lifecycle status or any other workflow status.
8. Copy and send manually outside SEI only after review. After an actual send, update the saved row and log the real interaction through the appropriate operator workflow.

Previewing or saving a message draft does not send email, create a Communication, create a task, create CRM records, mark a prospect contacted, or change lifecycle status. A saved draft is preparation only. It must remain unsent until an operator actually sends it through the intended channel.

Assistant and script implementations must also follow the rich-text storage, whitespace-preservation, and template-variable validation rules in [`../assistant_workflows/prepare-message-draft.md`](../assistant_workflows/prepare-message-draft.md).
