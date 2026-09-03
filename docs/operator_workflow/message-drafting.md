# Message Drafting

Message drafting is **Stage 2** of the ordered [Initial Outreach](initial-outreach.md) process. Begin only after prospect positioning is complete and has passed its completion gate.

Message drafting turns approved prospect positioning and current SEI guidance into a complete, reviewable initial outreach message. The result must be specific to the prospect, grounded in observable evidence, naturally written, accurate about the source, consistent with the assigned Playbook and Signal Types, correctly rendered through the selected template, and saved as an unsent draft for manual review.

Drafting is a record-preparation action, not an outreach, lifecycle, or CRM action. It is not a keyword-substitution exercise. Write and review each message as complete prose.

Compliance requires actively applying every applicable review gate in this document to the completed message. A draft is not compliant merely because it generally reflects the guidance. If any required gate fails, revise the message and rerun the required review before saving it.

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

Structured SEI fields such as `signal_summary`, `offer`, thesis or positioning fields, qualification explanations, and prior Prospect drafts are context inputs only. Prospect-specific body copy must be independently composed from the underlying evidence and approved positioning rather than pasted, lightly paraphrased, or mechanically transformed from those fields or another Prospect draft. If substantial wording or structure can be traced directly to one of those inputs, rewrite it from scratch.

Do not draft by converting structured SEI fields into prose. `signal_summary`, `offer`, thesis or positioning fields, qualification explanations, and prior Prospect drafts are context inputs only. Do not paste them, lightly paraphrase them, or mechanically transform them into message copy. Read the underlying evidence and completed positioning, determine the intended meaning, and compose the message independently. If substantial wording or structure can be traced directly to one of those fields or to another Prospect's draft, rewrite it from scratch.

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
- `{{ research_arena }}`
- `{{ signal_summary }}`
- `{{ qualification_explanation }}`
- `{{ thesis }}`
- `{{ offer }}`
- `{{ asset_url }}`
- `{{ primary_contact_name }}`
- `{{ primary_contact_role }}`

Renderer support does not make every variable appropriate for prospect-facing body copy. Internal structured fields such as `signal_summary`, `qualification_explanation`, `thesis`, and `offer` are context inputs unless the active standard template explicitly requires one for a narrowly defined purpose. Their availability does not authorize direct insertion or light paraphrase into prospect-facing prose.

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

The Cartertek paragraph must clearly refer to that work. Convert the evidence into the prospect's actual buyer use case: explain what now needs to happen, who needs it, and how Cartertek would participate. Do not substitute adjacent capabilities such as integrations, automation, reporting, or migration support for the specific work the prospect would be hiring Cartertek to perform. If the offer sentence could be inserted unchanged into many unrelated messages, it is too generic.

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

### 15. Introduce the source before discussing what it revealed

The recipient should immediately understand why a source, issue, post, announcement, or other artifact has entered the conversation. On its first mention, introduce it from the sender's outsider perspective rather than beginning as though the recipient already knows which artifact Cartertek is referring to.

Usually this requires only a few words integrated into the same sentence, such as `I saw`, `I found`, `I read`, `I was reading`, or `I came across`. Choose whatever wording is natural for the particular source and message; these are examples, not a required formula or template.

Prefer:

> I saw a {{company}} issue describing the {{problems you are having}}.

Over:

> Your {{company}} issue describes the {{problems you are having}}.

The introduction should **not add a separate setup sentence or additional source summary**. Its purpose is only to orient the recipient to how the observed problem came to Cartertek's attention. Continue to mention only the minimum evidence necessary to establish the reason for outreach.

Do not mechanically reuse the same introductory phrase across prospects. The source introduction should fit naturally into the independently composed message. Avoid compressed research-summary language.

### 16. Split dense evidence into multiple sentences

Do not force the source, issue, supporting evidence, interpretation, and offer into one sentence. A useful sequence is:

1. identify the source and central problem
2. describe the relevant details
3. state directly what Cartertek could do about the observed problem

### 17. Use evidence selectively; do not retell the prospect research

Use evidence to establish why Cartertek is reaching out, not to retell the prospect's own situation. The recipient already knows the underlying problem. Mention only the minimum evidence necessary to make the reason for outreach recognizable and credible. Detailed evidence belongs in SEI, not in the initial message. If the message spends more words explaining what the source said than stating what Cartertek could directly do about the problem, rewrite it.

### 18. Default to prose; use lists only when necessary

Initial outreach should normally be written as natural prose. Do not convert source evidence, qualifications, technical details, benefits, proposed work, or observations into a list merely because several items exist. Use a list only when the information is genuinely clearer as distinct parallel items and cannot be expressed naturally and concisely in prose. The existence of three or more details is not, by itself, a reason to use a list. When a list is genuinely necessary, introduce it conversationally and keep it brief.

### 19. Summarize source evidence; do not quote or imitate it

Do not quote job-posting language or reproduce it in quotation-like prose unless an exact quotation is genuinely necessary. Avoid close analysis of how the source was written, promotional phrases copied from the employer, distinctive metaphors, and setups such as “one line stood out.”

Extract useful facts and restate them in ordinary language. The email should sound like the sender understood the source, not like the sender is reviewing it.

### 20. Keep references explicit

Terms such as `this work`, `that implementation`, `the issue`, `the transition`, `work like this`, `constraints like these`, or `processes like these` must have a clear and nearby antecedent in the preceding prose. The recipient should not need to infer the referent from a job title, an external source, or a broad prior paragraph. When the work has not already been named precisely, name it instead of using shorthand.

### 21. State Cartertek's role directly

Determine internally why Cartertek is relevant, but do not write the message as though answering the question `Why is Cartertek relevant?` The prospect-facing sentence should state Cartertek's participation directly in the situation. The reader should understand Cartertek's relevance from what Cartertek is offering to do, not from meta-language about fit, usefulness, opportunity, contribution, or relevance.

Prefer direct constructions such as `Cartertek could help reduce...`, `Cartertek could build...`, `Cartertek could take on...`, `Cartertek could improve...`, or another concrete action verb that fits the prospect.

Avoid constructions such as `This is where Cartertek is a good fit`, `A useful role for Cartertek would be`, `The opportunity for Cartertek is`, `Cartertek would be relevant here because`, or similar answer-shaped language.

### 22. Use active voice

Write prospect-facing prose in active voice. Name the actor and action directly instead of hiding responsibility behind passive constructions. This applies to evidence descriptions, Cartertek's offer, and outcome statements. Rewrite passive phrasing when an active construction can express the same supported claim accurately.

### 23. Lead with outcomes, not delivery mechanics

Assume Cartertek's professional competence. Do not explain capability through lists of implementation sprints, workstreams, automation tasks, technical cleanup activities, development methods, or delivery stages.

Focus on outcomes such as keeping critical work moving, making a process easier to repeat, reducing dependence on manual coordination, improving internal workflows, or creating a reliable production process. Leave the implementation approach implicit unless it is necessary to understand the offer.

### 24. Avoid exaggerated claims

Do not extend the message beyond what the evidence supports. Avoid unsupported claims about the entire engineering organization, all permanent hiring, company-wide technical weakness, severe urgency, or work Cartertek has not established it can or should perform.

Keep the message bounded to the observed situation. Avoiding overcommitment means narrowing the scope, certainty, and outcome to what the evidence supports; it does **not** mean making the prose passive, tentative, abstract, or noncommittal. State the bounded offer directly with active language. Control overcommitment by narrowing **what Cartertek is claiming or offering to do**, not by weakening **how clearly the message says it**.

Do not add unnecessary hedging such as `Cartertek may be able to`, `There may be an opportunity for Cartertek to`, `A possible area where Cartertek could contribute`, or `This looks like something Cartertek might be able to help with` when a direct bounded construction such as `Cartertek could help`, `Cartertek could build`, `Cartertek could take on`, or `Cartertek could improve` expresses the same supported claim.

### 25. Apply internal guardrails silently

Do not verbalize drafting constraints, rejected alternatives, or internal safety checks in the message unless the prospect actually raised them. Phrases such as `without a wholesale rebuild`, `without replacing your team`, `rather than a complete overhaul`, or `not suggesting the product is broken` introduce ideas that were not part of the prospect context and expose the drafting process.

Apply constraints through the scope of the proposal itself. When the work must remain bounded, describe the specific work Cartertek is proposing and omit larger, riskier, or disallowed alternatives instead of naming them.

### 26. Avoid one-sentence paragraphs

Treat one-sentence paragraphs as a warning sign during review. When a paragraph contains only one sentence, first consider splitting a dense sentence into two or more natural sentences, or combining it with a related paragraph so the thought develops conversationally.

Keep a one-sentence paragraph only when the sentence is intentionally brief and gains emphasis from standing alone. Do not use isolated one-sentence paragraphs as the default structure for evidence and offer sections.

### 27. Avoid templated keyword substitution

Do not reuse a sentence from another prospect and substitute company-specific nouns. Draft the intended meaning first, then choose a sentence structure that fits it.

A borrowed structure may create unclear pronouns, mismatched subjects, illogical causal relationships, awkward hiring references, or language that sounds mass-produced. Rewrite from scratch when the existing frame does not fit the prospect.

### 28. Keep the message concise, non-repetitive, and non-diagnostic

Each sentence must advance the message. Do not restate the signal in the Cartertek paragraph using different terminology. When several related facts establish one broader condition, synthesize them instead of listing every fact individually.

Do not diagnose an exact root cause or prescribe an exact remediation from public evidence unless the source itself establishes it. Public evidence may support a problem area, constraint, or desired outcome; it usually does not establish that a specific architecture, component, configuration, integration, data model, or engineering change is required.

Reach Cartertek's direct offer quickly. The source reference exists only to establish why the outreach is timely. Do not make the recipient read a paragraph of evidence analysis before learning why Cartertek is contacting them.

Initial outreach should read like the opening of a conversation, not a statement of work, technical assessment, delivery proposal, or procurement response. Detailed methodology, workstreams, validation plans, milestones, ownership boundaries, and implementation sequencing belong after discovery.

Stop once the message has established the relevant situation, what Cartertek could directly do, and the appropriate next step supplied by the message or template. Do not continue merely to explain inferred root causes, implementation approach, validation method, rollout path, scaling consequences, or every downstream business benefit.

### 29. Review the complete sentence, paragraph, and message

After every draft or revision:

1. read the entire sentence
2. read the entire paragraph
3. read the complete message

Confirm that every pronoun has a clear referent, every clause has a clear subject, causal relationships make sense, the positioning paragraph follows from the evidence paragraph, references are explicit, the hiring context is attached to the correct subject, and the message reads naturally from beginning to end.

Do not validate a revision merely by checking the words that changed.

## Phase 4: Finalization

### 30. Save the draft in the correct SEI location

Save the reviewed message under:

```text
SEI Prospect
-> Outreach
-> Message Drafts
```

Populate the intended platform, sender, recipient, subject, body, suggested template, and attribution fields. Leave `sent` unchecked and `sent_on` empty.

Previewing or saving a draft does not send email, create a Communication, create a task, create CRM records, mark a prospect contacted, or change lifecycle status. Send manually outside SEI only after operator review. After an actual send, update the saved row and log the real interaction through the appropriate workflow.

### 31. Set the sender field uniformly

Set `from_user` to the designated sender for every draft in the batch. Verify first that the email belongs to a valid Frappe user, apply it consistently, and read the values back to confirm no draft was missed.

Do not confuse `from_user` with `modified_by`; verify both independently.

### 32. Final quality-control checklist

Apply this checklist independently to **every individual message**, including every message in a batch. A successful review of one draft does not validate the structure, wording, or offer framing of any later draft. Never treat a previously approved message as a reusable frame that bypasses review.

Before a draft can pass final review, apply these hard-fail gates:

- **Implementation-mechanics gate:** if the message contains unnecessary implementation mechanics, delivery stages, technical task lists, validation procedures, or similar delivery-plan detail, it fails. Rewrite it to focus on the work or outcome.
- **Invented-scope gate:** if the message invents a project boundary, engagement structure, ownership area, workstream, or scope that the evidence and positioning do not establish, it fails. Rewrite it with a bounded, evidence-supported offer direction.
- **Templated-structure gate:** if the message's sentence pattern or overall structure could be reused for another Prospect by swapping company, signal, or offer details, it fails. Rewrite it from the intended meaning rather than reusing the frame.
- **Research-summary gate:** if the message retells the source or spends more words explaining the evidence than establishing Cartertek's relevance, it fails. Retain only the evidence needed to justify outreach.
- **Unintroduced-source gate:** if the message begins discussing an external source or observed artifact as though it were already shared context—such as `your issue`, `the post`, `the RFC`, or `the report`—without first naturally establishing that Cartertek saw, found, read, encountered, or otherwise became aware of it, it fails. Introduce the source within the existing evidence sentence without adding unnecessary setup or a separate research-summary sentence.
- **Premature-diagnosis gate:** if the message states or strongly implies an exact root cause or required technical solution that the source does not establish, it fails. Reframe around the supported problem or outcome.
- **Repetition/compression gate:** if two sentences communicate substantially the same fact, consequence, or proposed value, or if several source details can be accurately synthesized into one, it fails. Combine, remove, or synthesize the redundant material.
- **Buried-value gate:** if substantial source explanation can be removed before the Cartertek proposition without losing necessary context, it fails. Shorten the setup so Cartertek's relevance appears promptly.
- **Internal-field leakage gate:** if message wording or structure comes directly or through light paraphrase from `signal_summary`, `offer`, thesis, qualification explanation, positioning fields, or another Prospect draft, it fails. Compose the message independently from the underlying meaning.
- **Proposal-tone gate:** if the body reads like a proposal, statement of work, technical assessment, delivery plan, or procurement response rather than an initial conversation, it fails. Simplify it to the reason for contact and broad relevant help.
- **Indirect-relevance gate:** if the message explains Cartertek's fit, relevance, usefulness, opportunity, or contribution instead of directly stating what Cartertek could do, it fails. Rewrite the sentence with a concrete Cartertek action.
- **Passive-voice gate:** if a prospect-facing sentence uses passive voice where an active construction can express the same supported claim accurately, it fails. Rewrite it in active voice.
- **Hedging-without-scope-change gate:** if tentative or abstract wording weakens a bounded claim without actually narrowing scope, certainty, or outcome, it fails. Keep the bounded claim and state it directly.
- **Over-completion gate:** if the message continues after the reason for contact, Cartertek's relevant contribution, and next step are already clear, and the remaining material is not necessary for comprehension, it fails. Remove the extra reasoning chain.
- **List-necessity gate:** if a list can be expressed naturally and clearly as prose without material loss of clarity, it fails. Rewrite the list as prose.

A failed gate is blocking. Rewrite the message, then rerun the complete final quality-control checklist from the beginning. Do not save the draft until all applicable gates and checklist items pass.

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
- the message states directly what Cartertek could do, and that action follows from the evidence
- continued hiring or the existing company plan represented correctly
- no implication that Cartertek replaces a permanent role

#### Writing

- natural outsider perspective
- first source reference naturally establishes how it came to Cartertek's attention
- dense evidence split into readable sentences
- no list unless prose would materially reduce clarity
- no direct quotation or pseudo-quotation
- no unnecessary source jargon
- technical terms used only where natural and necessary
- no generic category label where operational language is available
- no vague reference to `this work`
- outcome emphasized over implementation method
- Cartertek's role stated with direct action language rather than fit/relevance meta-language
- active voice used throughout prospect-facing prose
- bounded claims stated directly without unnecessary hedging
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
