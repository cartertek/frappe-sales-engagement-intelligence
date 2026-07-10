# Prepare Message Draft

Use `preview_message_draft(prospect, template)` to render a manual-review draft.

The endpoint returns subject, body, missing variables, resolved variables, and safety flags. It does not send email, create a Communication, create a task, create CRM records, or change lifecycle status.

Scripts may display or save the preview for human review. They must not auto-send or bulk-send the result.
