# Prepare Message Draft

Use `preview_message_draft(prospect, template)` to render a manual-review draft.

The endpoint returns subject, body, missing variables, resolved variables, and safety flags. It does not send email, create a Communication, create a task, create CRM records, or change lifecycle status.

Scripts may display or save the preview for human review. They must not auto-send or bulk-send the result.

## Message wording and evidence attribution

Before drafting or revising a prospect-specific message, load the current general drafting guidance, assigned playbook guidance, applicable signal-type guidance, prospect record, linked signal record, and the source evidence that describes the relevant work or problem. Do not begin from the existing wording alone or infer missing responsibilities from the company category, role title, or metadata.

Drafts must sound like natural outreach, not compressed research summaries. Apply these rules across all research arenas and source types:

- Identify the actual source accurately, such as a job posting, product announcement, GitHub issue, support thread, company page, directory profile, or public complaint. Do not replace it with a vague label such as “note” or “information.”
- Explain naturally how Cartertek encountered the evidence.
- Write from the perspective of an outsider addressing someone inside the company. Use “you” and “your” where appropriate instead of detached language.
- Attribute claims to the source when Cartertek has not independently verified the underlying condition.
- Do not compress the source, evidence, interpretation, and pitch into one long sentence. Split dense ideas into short sentences with a spoken cadence.
- Introduce a list before presenting several details, using natural setup such as “A few things stood out.”
- Translate formal, promotional, or technical source language into normal speech without changing its meaning. Do not reuse source jargon merely because it is specific. Preserve technical terms when they identify an actual technology or domain concept, but avoid copying unusual phrases, internal shorthand, branded terminology, or awkward constructions unless they are necessary for accuracy and would sound natural in ordinary conversation. Repetition of distinctive source language is a strong sign that the message is paraphrasing too mechanically.
- Summarize source evidence instead of quoting it or closely imitating its wording unless a direct quotation is genuinely necessary. Outreach should sound like the sender understood the source, not like they are analyzing or reciting it. Avoid setups such as “one line stood out,” “the posting said,” or polished source-language constructions that read like quotations. Extract the relevant facts and restate them in ordinary conversational language.
- Preserve concrete evidence rather than replacing it with generic phrases such as “technical challenges.”
- Use the company name to establish context, then shift naturally to “you” and “your.”
- Avoid language that sounds accusatory, invasive, opportunistic, or like an unsolicited audit.
- Lead with the outcome, not the delivery mechanics. Outreach should assume Cartertek is professionally capable without explaining how the work would be executed. Avoid listing implementation methods, sprint structures, technical workstreams, or service components unless the recipient needs that detail to understand the offer. State the relevant result Cartertek can help create and leave the execution approach implicit.
- Interpret the source's operational meaning instead of repeating its category labels. Job postings and other source material often use broad terms such as infrastructure, platform, operations, or systems. Do not reuse those labels automatically. Identify the concrete problems described beneath them and express Cartertek's relevance in language that reflects what the work actually involves. The positioning sentence should clearly refer back to the evidence paragraph; if it could be reused unchanged for many unrelated prospects, it is probably too generic.
- Avoid duplicate calls to action. Before adding a prospect-specific question or meeting invitation, review the template closing. Do not ask for a conversation, call, or reply twice in the same message. Keep a prospect-specific CTA only when it adds a meaningfully different next step; otherwise rely on the template’s existing invitation.
- Review every revision as complete prose, not as a local word substitution. Reread the full sentence, paragraph, and message to confirm that pronouns have clear referents, each clause has an intelligible subject, and the logic remains natural from beginning to end. Rewrite the sentence from scratch when the existing structure no longer fits the intended meaning.

## Rich-text body formatting

`SEI Prospect Message Draft.body` is a Frappe **Text Editor** field. Treat its stored value as HTML, not plain text.

When saving a rendered draft:

- Wrap each ordinary paragraph in `<p>...</p>`.
- Preserve every intentional blank line from the source template with an explicit empty block such as `<p><br></p>`.
- Do not rely on `\n` or `\n\n` characters to produce visible line breaks in the form.
- Do not treat adjacent `<p>` elements as equivalent to a blank line. Frappe may display adjacent paragraphs without the empty line represented by a double newline in the template.
- Preserve template spacing semantically. Do not normalize, collapse, or otherwise rewrite the template's paragraph separation while converting it to HTML.
- Use `<br>` only for line breaks that belong inside one logical block, such as lines within a compact signature. Use `<p><br></p>` for a complete blank line between blocks.

For example, this plain-text template fragment:

```text
Hi {{ primary_contact_name }},

I'm the owner of Cartertek, a software engineering consultancy.

{{ message_body }}

All the best,

- Joshua
```

should be stored as HTML with explicit empty paragraphs:

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

After saving, read the stored `body` value back and verify that the expected `<p><br></p>` blocks are present. Do not report the draft as correctly formatted until this verification succeeds.

## Template variable validation

Before using a template through `preview_message_draft`, verify that every variable in the template is supported by the live renderer.

An unsupported variable may be replaced with an empty string and reported as missing. Do not silently apply a template containing unsupported variables. Either update the renderer as part of the requested work or explicitly preserve and insert the intended content before saving the manual-review draft.
