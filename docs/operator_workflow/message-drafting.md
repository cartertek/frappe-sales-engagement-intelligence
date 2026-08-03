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


## Message wording and evidence attribution

Before drafting or revising a prospect-specific message, load the current general drafting guidance, assigned playbook guidance, applicable Signal Type guidance, prospect record, linked Signal record, and the source evidence that describes the relevant work or problem. Do not begin from the existing wording alone or infer missing responsibilities from the company category, role title, or metadata.

Drafts must sound like natural outreach, not compressed research summaries:

- Identify the actual source accurately, such as a job posting, product announcement, GitHub issue, support thread, company page, directory profile, or public complaint. Do not replace it with a vague label such as “note” or “information.”
- Explain naturally how Cartertek encountered the evidence.
- Write from the perspective of an outsider addressing someone inside the company. Use “you” and “your” where appropriate instead of detached language.
- Attribute claims to the source when Cartertek has not independently verified the underlying condition.
- Split dense ideas into short sentences with a spoken cadence; do not compress source, evidence, interpretation, and pitch into one sentence.
- Introduce several details naturally, for example with “A few things stood out.”
- Translate formal, promotional, or technical source language into normal speech without changing its meaning. Preserve necessary technical terms, but avoid mechanically repeating unusual source phrases, branded terminology, or internal shorthand.
- Summarize source evidence instead of quoting or closely imitating it unless a direct quotation is genuinely necessary. Avoid setups such as “one line stood out” or “the posting said.”
- Preserve concrete evidence rather than replacing it with generic phrases such as “technical challenges.”
- Use the company name to establish context, then shift naturally to “you” and “your.”
- Avoid language that sounds accusatory, invasive, opportunistic, or like an unsolicited audit.
- Lead with the outcome, not delivery mechanics. Do not list implementation methods, sprint structures, technical workstreams, or service components unless the recipient needs them to understand the offer.
- Interpret the source's operational meaning instead of automatically repeating broad labels such as infrastructure, platform, operations, or systems. The positioning sentence should clearly refer back to the evidence; if it could be reused unchanged for unrelated prospects, it is too generic.
- Avoid duplicate calls to action. Review the template closing before adding a prospect-specific question or meeting invitation.
- Review every revision as complete prose. Reread the full sentence, paragraph, and message to confirm pronouns, subjects, and logic remain clear; rewrite from scratch when the old structure no longer fits.
- Do not use “this work,” “this kind of work,” or “work like this” unless the preceding message clearly describes the referent.

## Rich-text body formatting

`SEI Prospect Message Draft.body` is a Frappe **Text Editor** field. Store HTML, not plain text.

When saving a rendered draft:

- Wrap each ordinary paragraph in `<p>...</p>`.
- Preserve every intentional blank line with an explicit empty block such as `<p><br></p>`.
- Do not rely on `\n` or `\n\n` to produce visible spacing.
- Do not treat adjacent `<p>` elements as equivalent to a blank line.
- Preserve template spacing semantically; do not collapse or normalize paragraph separation during conversion.
- Use `<br>` only for line breaks inside one logical block, such as a compact signature. Use `<p><br></p>` for a complete blank line between blocks.

For example:

```text
Hi {{ primary_contact_name }},

I'm the owner of Cartertek, a software engineering consultancy.

{{ message_body }}

All the best,

- Joshua
```

must be stored as:

```html
<p>Hi {{ primary_contact_name }},</p>
<p><br></p>
<p>I'm the owner of Cartertek, a software engineering consultancy.</p>
<p><br></p>
<p>{{ message_body }}</p>
<p><br></p>
<p>All the best,</p>
<p><br></p>
<p>- Joshua</p>
```

After saving, read the stored `body` back and verify that the expected `<p><br></p>` blocks remain. Do not report the draft as correctly formatted until this verification succeeds.

## Template variable validation

Before using a template through `preview_message_draft`, verify that every variable is supported by the live renderer.

An unsupported variable may be replaced with an empty string and reported as missing. Do not silently apply such a template. Update the renderer as part of the requested work or explicitly preserve and insert the intended content before saving the manual-review draft.
