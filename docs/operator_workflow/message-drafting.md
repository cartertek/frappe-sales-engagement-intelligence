# Message Drafting

Message drafting turns approved prospect positioning and current SEI guidance into a complete, reviewable initial outreach message. The result must be specific to the prospect, grounded in observable evidence, naturally written, accurate about the source, consistent with the assigned Playbook and Signal Types, correctly rendered through the selected template, and saved as an unsent draft for manual review.

Drafting is a record-preparation action, not an outreach, lifecycle, or CRM action. It is not a keyword-substitution exercise. Write and review each message as complete prose.

## Phase 1: Information collection

### 1. Load the complete drafting context

Before writing, load the latest version of:

- this operator guidance
- the assigned Playbook and its initial outreach guidance
- every applicable managed Signal Type and its message guidance
- the Prospect record
- completed prospect positioning
- linked Published Signals and Observed Facts
- source evidence
- selected contact and contact role
- prior touchpoints or outcomes when relevant
- selected SEI Message Template
- any existing draft being revised

Do not rely on memory from an earlier drafting round. Guidance and records may have changed.

### 2. Treat evidence loading as a mandatory gate

Do not draft until the underlying evidence has been read. A company name, role title, signal label, or summary is insufficient.

Confirm:

- what the source actually said or showed
- which details were directly observed
- which conclusions are positioning interpretations
- what work the prospect appears to need
- why outreach is timely
- why the selected contact is appropriate

If the evidence cannot support a specific message, do not fill the gap with generic assumptions.

### 3. Use the Playbook correctly

The Playbook controls the broad outreach logic. Apply it to how the source should be introduced, how the situation should be framed, how Cartertek should be positioned, the relationship to the prospect's existing plan, the appropriate offer, and what the message must avoid implying.

For Failed Hiring messages:

- identify the job posting or hiring artifact accurately
- do not say recruitment has failed
- do not sound like a recruiter
- do not imply Cartertek should replace a permanent employee
- connect Cartertek's offer to work described by the role
- make clear that Cartertek can help while the company continues hiring

### 4. Apply Signal Type positioning separately

Use Signal Type guidance to determine which aspect of the evidence should lead and which outcomes matter. Do not collapse Playbook and Signal Type guidance into one generic rule. The Playbook explains campaign logic; the Signal Type explains the particular evidence pattern. The message must reflect both.

## Phase 2: Templating

### 5. Use the message template as the outer structure

Treat the selected SEI Message Template as the message wrapper. It may supply the greeting, sender introduction, prospect-specific body placeholder, call invitation, sign-off, and subject structure.

Insert prospect-specific writing into the template. Do not add a second greeting, CTA, or signature. Preserve the latest template content unless the requested work includes changing the template itself.

Supported standard variables include:

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

### 6. Avoid duplicate calls to action

Inspect the template closing before adding a prospect-specific question. Do not ask twice for a call, conversation, reply, or meeting.

Keep a prospect-specific CTA only when it requests a meaningfully different next step. Otherwise rely on the template's existing invitation.

### 7. Preserve template whitespace exactly

`SEI Prospect Message Draft.body` is a Frappe **Text Editor** field and stores HTML.

Use ordinary paragraph blocks:

```html
<p>Paragraph content</p>
```

Represent every deliberate blank line from a template double newline with:

```html
<p><br></p>
```

Do not assume plain `\n`, `\n\n`, or adjacent `<p>` elements preserve intentional blank space. Use `<br>` only for a line break inside one logical block, such as a compact signature.

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

After saving, read the stored body back and verify that the expected `<p><br></p>` blocks remain.

### 8. Verify renderer support before using template variables

Do not assume a variable is supported because it appears in a template. Before relying on a placeholder such as `{{ message_body }}` or a subject variable:

1. inspect the template
2. inspect or exercise the live renderer or preview path
3. confirm the variable is populated
4. verify the rendered result

An unsupported variable may be replaced with an empty string and reported as missing. Do not silently save that result. Update the renderer when that work is in scope or explicitly preserve and insert the intended content before saving the manual-review draft.

### 9. Apply the subject template

Render the current subject template using the prospect-specific subject value or offer. When the template is:

```text
Consultancy offer: {{ offer }}
```

preserve the meaningful prospect-specific subject as `offer` and render the final subject from the template.

Verify that the template prefix appears exactly once, the prospect-specific subject remains meaningful, no old subject format remains, and the subject is stored on the correct draft.

## Phase 3: Body content creation

### 10. Identify and address the actual work

Reflect what the company is trying to accomplish, not merely the job title, Signal Type, or broad source category. Determine the actual work from responsibilities, pain points, stated constraints, operational consequences, process descriptions, and technical context.

The Cartertek paragraph must clearly refer to that work. If the offer sentence could be inserted unchanged into many unrelated messages, it is too generic.

### 11. Interpret source terminology instead of copying labels

Do not automatically repeat broad source terms such as `infrastructure`, `systems`, `platform`, `operations`, or `tooling`. Explain their operational meaning.

For example, identity management, device administration, knowledge systems, and AI automation may collectively indicate internal workflow automation rather than a vague infrastructure constraint. The message should demonstrate understanding, not only source fidelity.

### 12. Use technical terms only when genuinely useful

Retain a technical term when it accurately names an important technology or artifact the company uses. Translate or remove terminology that is internal jargon, awkward shorthand, unusual marketing language, unnecessary for comprehension, or unnatural for an outsider to repeat.

Ask:

> Would an informed outsider naturally use this exact phrase to describe the same thing?

A term such as `RL environment` may be necessary and natural. A distinctive phrase copied from the posting merely because it sounds specific may not be.

### 13. State the evidence source accurately

Name the source as what it actually was: a job posting, founder post, GitHub issue, product announcement, support discussion, company page, directory profile, public complaint, or another observed artifact.

Do not describe a job posting as a “note” or replace a known source with vague language.

### 14. Write from the perspective of an outsider

The sender is outside the organization and addressing someone inside it. Prefer `your deployment process`, `your internal workflows`, `your team`, or `your production environment` over detached wording. Use the company name to establish context, then transition naturally to `you` and `your`.

### 15. Use conversational source introductions

The opening should sound like a normal explanation of why Cartertek is reaching out.

Natural:

> I came across an AirOps job posting that mentioned you were having some problems with your deployment process.

Stilted:

> I saw in an open AirOps job posting that operational constraints were affecting deployment reliability.

Avoid compressed research-summary language.

### 16. Split dense evidence into multiple sentences

Do not force the source, issue, supporting evidence, interpretation, and offer into one sentence. A useful sequence is:

1. identify the source and central problem
2. describe the relevant details
3. explain Cartertek's relevance in a separate paragraph

### 17. Introduce lists conversationally

When several details follow, explain why they are being listed. Use language such as:

> A few things stood out:

Do not suddenly present a polished list of extracted details without an introduction.

### 18. Summarize source evidence; do not quote or imitate it

Do not quote job-posting language or reproduce it in quotation-like prose unless an exact quotation is genuinely necessary. Avoid close analysis of how the source was written, promotional phrases copied from the employer, distinctive metaphors, and setups such as “one line stood out.”

Extract useful facts and restate them in ordinary language. The email should sound like the sender understood the source, not like the sender is reviewing it.

### 19. Keep references explicit

Terms such as `this work`, `work like this`, `constraints like these`, or `processes like these` must have a clear antecedent in the preceding prose. The recipient should not need to infer the referent from a job title or an external source.

### 20. Lead with outcomes, not delivery mechanics

Assume Cartertek's professional competence. Do not explain capability through lists of implementation sprints, workstreams, automation tasks, technical cleanup activities, development methods, or delivery stages.

Focus on outcomes such as keeping critical work moving, making a process easier to repeat, reducing dependence on manual coordination, improving internal workflows, or creating a reliable production process. Leave the implementation approach implicit unless it is necessary to understand the offer.

### 21. Avoid exaggerated claims

Do not extend the message beyond what the evidence supports. Avoid unsupported claims about the entire engineering organization, all permanent hiring, company-wide technical weakness, severe urgency, or work Cartertek has not established it can or should perform.

Keep the message bounded to the observed situation.

### 22. Avoid templated keyword substitution

Do not reuse a sentence from another prospect and substitute company-specific nouns. Draft the intended meaning first, then choose a sentence structure that fits it.

A borrowed structure may create unclear pronouns, mismatched subjects, illogical causal relationships, awkward hiring references, or language that sounds mass-produced. Rewrite from scratch when the existing frame does not fit the prospect.

### 23. Review the complete sentence, paragraph, and message

After every draft or revision:

1. read the entire sentence
2. read the entire paragraph
3. read the complete message

Confirm that every pronoun has a clear referent, every clause has a clear subject, causal relationships make sense, the positioning paragraph follows from the evidence paragraph, references are explicit, the hiring context is attached to the correct subject, and the message reads naturally from beginning to end.

Do not validate a revision merely by checking the words that changed.

## Phase 4: Finalization

### 24. Save the draft in the correct SEI location

Save the reviewed message under:

```text
SEI Prospect
-> Outreach
-> Message Drafts
```

Populate the intended platform, sender, recipient, subject, body, suggested template, and attribution fields. Leave `sent` unchecked and `sent_on` empty.

Previewing or saving a draft does not send email, create a Communication, create a task, create CRM records, mark a prospect contacted, or change lifecycle status. Send manually outside SEI only after operator review. After an actual send, update the saved row and log the real interaction through the appropriate workflow.

### 25. Set the sender field uniformly

Set `from_user` to the designated sender for every draft in the batch. Verify first that the email belongs to a valid Frappe user, apply it consistently, and read the values back to confirm no draft was missed.

Do not confuse `from_user` with `modified_by`; verify both independently.

### 26. Final quality-control checklist

#### Context

- current drafting documentation loaded
- correct Playbook loaded
- correct Signal Type guidance loaded
- completed prospect positioning loaded
- source evidence read
- correct contact selected
- current template loaded

#### Evidence and positioning

- source named accurately
- claims attributed to the source
- observed facts separated from inference
- actual work identified
- signal timing distinguished from offer substance
- Cartertek relevance follows from the evidence
- continued hiring or the existing company plan represented correctly
- no implication that Cartertek replaces a permanent role

#### Writing

- natural outsider perspective
- conversational source introduction
- dense evidence split into readable sentences
- lists introduced naturally
- no direct quotation or pseudo-quotation
- no unnecessary source jargon
- technical terms used only where natural and necessary
- no generic category label where operational language is available
- no vague reference to `this work`
- outcome emphasized over implementation method
- no exaggerated claims
- no templated noun substitution
- clear subjects, pronouns, and clause relationships
- complete message coherent as prose
- one CTA only

#### Template and storage

- correct template assigned
- subject template rendered correctly
- platform set correctly
- sender field set
- HTML paragraphs stored correctly
- every deliberate blank line stored as `<p><br></p>`
- current template closing present
- signature correct
- draft remains unsent

#### Readback verification

After saving, read back the subject, body, template assignment, platform, contact, sender, draft status, and `modified_by`.

Confirm that the intended wording is present, superseded wording is absent, blank-line blocks are preserved, subject formatting appears exactly once, no unrelated content changed, and attribution is correct.

A draft is complete only after the stored record has been read back and verified.
