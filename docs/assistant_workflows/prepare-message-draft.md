# Prepare Message Draft

Use `preview_message_draft(prospect, template)` to render a manual-review draft.

The endpoint returns subject, body, missing variables, resolved variables, and safety flags. It does not send email, create a Communication, create a task, create CRM records, or change lifecycle status.

Scripts may display or save the preview for human review. They must not auto-send or bulk-send the result.

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
