# Cartertek Outreach Strategy and Execution Guide

This guide describes Cartertek's current outreach-marketing process.

## Follow the guide as written

This guide is an executable operating procedure, not reference material to summarize or approximate. When performing Cartertek outreach work, follow the applicable procedures as written and in the order they specify. Do not replace them with a summary, remembered approximation, simplified workflow, or a shorter set of principles. If a procedure requires a checklist, audit, gate, or ordered sequence, actually perform that procedure before proceeding.

### Operator documentation source of truth

Whenever this guide requires following, reading, checking, or referring to the SEI operator documentation, use **only the most recent operator docs from the GitHub repository**. Fetch or otherwise verify the current repository revision before reading them. The operator-doc files bundled into a deployed Frappe app, container, image, working copy, cached checkout, local mirror, prior conversation, or remembered workflow are not authoritative unless they have first been verified to match the latest repository version.

Do not claim to have read the current or latest operator docs merely because a copy exists at the expected `docs/operator_workflow/` path. Confirm that the copy being used is the latest GitHub-repository version first. If the latest repository docs cannot be obtained or verified, treat the operator instructions as unavailable rather than substituting an older copy.

## Purpose

Cartertek outreach is a small-volume, high-context client-acquisition process.

The goal is not to build large lead lists or send generic consulting pitches. The goal is to find organizations with **specific public evidence that makes a Cartertek engagement timely and relevant**, identify the people closest to that evidence, and contact them with a concise message grounded in what was actually observed.

The current process is:

```
Choose a validated playbook
→ research candidate prospects
→ develop evidence-first draft signals
→ publish only defensible signals
→ let SEI determine qualification from signal strength
→ research the prospect's identity and primary contact roles
→ find and verify named contacts and contact paths
→ draft the initial message inside the assigned template
→ review and send manually
→ follow up or reactivate when appropriate
→ record responses and commercial outcomes
→ hand real opportunities into CRM
```

The core question is:

```
Why is this organization worth contacting now, who is the right person to contact, and what specific Cartertek help is relevant to the evidence?
```

## Strategic Foundation

Most outreach fails because it begins with a list of companies and a generic reason to pitch them.

Cartertek's outreach should begin with evidence.

A good outreach prospect is not merely a company that fits a broad demographic. A good prospect has a visible reason Cartertek might be relevant now.

The system should preserve this distinction:

```
Observed signal ≠ inferred pattern
```

A company that "seems like the type that might need help" is not enough. There should be a defensible entry point: something visible, documented, timely, or specific enough to justify outreach.

The core strategy is:

```
Find observable signals of software risk, stalled development, operational friction, or technical overload.

Map that signal to a clear thesis.

Use the thesis to choose the contact role, message angle, and bounded offer direction.

Track what happens so future outreach can improve when the evidence justifies a change.
```

## Current outreach model

### Evidence-first cold outreach

The validated outreach motion is **signal-driven cold outbound**.

A campaign begins with a prospecting thesis about a kind of public evidence that may reveal timely software work. Research then tests that thesis against real prospects.

The public source is not enough by itself. A prospect advances only when the evidence survives the current signal definition, latest-state review, disqualifiers, and qualification rules.

A good prospect therefore has all three:

1. **Observable evidence** — a public source establishes the material facts.
2. **A current reason to care** — the evidence is still relevant now, not merely historical.
3. **A Cartertek-relevant work thesis** — the evidence points to software-engineering work Cartertek could plausibly perform.

Do not substitute broad company fit, industry fit, or speculation for a qualifying signal.

### Campaign playbooks are research strategies, not separate outreach channels

The current playbooks differ mainly in **what evidence we research and how that evidence is interpreted**. Once a prospect qualifies, they feed into the same downstream process:

```
qualification
→ contact selection and research
→ message drafting
→ manual outreach
→ follow-through
```

The validated campaign playbooks are:

- Failed Recruitment
- Launch Aftermath
- Technical Distress
- Ecosystem Adjacency

These playbooks are described later in this guide.

### Keep strategy distinct from execution variations

Email, LinkedIn, contact forms, phone, alternate contacts, later follow-ups, and reactivation are execution choices or lifecycle actions. They are not separate prospecting strategies.

Likewise, a source type does not become a new outreach strategy merely because it contains stronger buyer intent or appears in a different community. The important distinction is the **basis on which Cartertek selects and qualifies the prospect**.

## Evidence and qualification principles

Detailed signal-development and publication rules belong in the operator documentation. This guide preserves only the strategic rules that apply across campaigns.

### Evidence precedes classification

Research the facts before deciding that a prospect fits a signal type or strength.

Do not start from a desired qualification result and search backward for supporting language.

### Observed evidence is not inferred opportunity

A prospect may look promising without being qualified.

The source must support the material claim being made. Cartertek fit, company size, technical sophistication, or a plausible need for consulting are useful context, but they are not substitutes for evidence.

### Verify the latest state

A historical problem does not automatically establish a current opportunity.

Before retaining a Moderate or Strong signal, check whether later evidence shows the issue was fixed, the project completed, the role closed, the workaround accepted, or the relevant condition otherwise ended.

When later evidence contradicts the original thesis, reevaluate the entire signal instead of preserving the classification with a nearby interpretation.

### Qualification is a result, not a research target

Operators evaluate the evidence and signal strength accurately. SEI applies the resulting prospect qualification state.

Do not strengthen a signal because a prospect would otherwise fail to qualify.

Do not weaken a signal because contact discovery looks difficult.

## Prospect research workflow

### 1. Start with a validated playbook

Before researching candidates, load the current playbook and its managed signal definitions.

Understand:

- what evidence qualifies;
- what evidence disqualifies;
- the current-state and recency requirements;
- what would make the signal Weak, Moderate, or Strong;
- which source arenas are appropriate for that playbook.

### 2. Research candidate evidence before creating a prospect thesis

Search the playbook's source arenas for candidate evidence.

Prefer sources that expose the underlying facts directly: first-party posts, issue threads, job listings, official product or engineering material, public implementation discussions, and other primary sources where possible.

Do not accept a candidate because it resembles a good prospect. Develop the evidence first.

### 3. Develop draft signals using the operator workflow

Draft Signals are the research workspace. Follow the current research, evidence, source-review, and signal-evaluation procedures in `docs/operator_workflow/`.

A candidate does not become a published qualifying signal until the evidence and classification pass the required review.

### 4. Review the resulting prospect state

After signal publication, review the prospect as a whole.

Confirm that:

- the qualifying signal still represents the current evidence;
- contradictory or newer evidence has been considered;
- the prospect identity is correct;
- the qualification state is the natural result of the published signals.

Only then move into identity and contact research.

## Validated campaign playbooks

### Failed Recruitment / Failed Hiring

The campaign was executed as **Failed Recruitment**; the live SEI playbook is named **Failed Hiring**.

#### What the campaign looks for

Failed Recruitment / Failed Hiring identifies teams where public evidence suggests an unresolved engineering-capacity or implementation gap. Hiring friction is one important pattern, but the playbook also includes bounded consultancy-compatible technical work and current capacity gaps that can be addressed without waiting for a permanent hire.

The useful evidence is a **current technical-capacity or delivery gap**, not merely the existence or age of a job listing.

The current signal patterns include:

- a genuinely unresolved long-open technical role;
- an overloaded hybrid role that combines substantive software engineering with a separate business or operational function;
- a current technical-capacity gap constraining operations, delivery, or revenue;
- a current contract, fractional, temporary, subcontracted, or project opportunity for a bounded technical outcome.

#### Important lessons from execution

A job page that remains online is not evidence that a role is still open. The source must affirmatively support current application status where current vacancy matters.

Likewise, an old role is not automatically a failed-recruitment signal. Persistence alone does not prove difficulty hiring.

For overloaded or hybrid roles, the role must actually perform substantive software-engineering work. A technical background, automation, configuration, architecture advice, demos, or technical fluency are not enough by themselves.

#### Outreach thesis

The outreach thesis is that Cartertek may be able to take on a defined body of engineering work that the organization is having difficulty staffing or concentrating into the current role structure.

Do not frame Cartertek as a generic replacement for an employee. Tie the message to the actual work implied by the qualifying evidence.

### Launch Aftermath

#### What the campaign looks for

Launch Aftermath identifies recently launched products, systems, or capabilities where public evidence shows a material technical consequence after launch and meaningful work remains.

A recent launch can be a timing trigger, but it is not enough by itself to justify outreach. The actionable thesis comes from **current post-launch aftermath or implementation demand**.

Examples may include continuing reliability problems, production-readiness gaps, integration failures, material defects, or other consequences that create a plausible body of engineering work.

#### Important lessons from execution

Current-state verification is mandatory. A launch-related issue that was subsequently fixed, stabilized, or completed is not a current Strong signal without separate evidence of continuing aftermath.

Do not preserve a prospect merely because the original launch was recent or technically ambitious.

#### Outreach thesis

The outreach thesis is targeted stabilization or completion work around the specific post-launch consequence that remains current.

### Technical Distress

#### What the campaign looks for

Technical Distress is not simply "a company has a technical problem."

The campaign targets **loss of technical agency**: evidence that an organization cannot safely or efficiently understand, change, maintain, or operate an important software system without disproportionate burden, uncertainty, repeated failure, or dependency.

Typical source arenas include public issue trackers, technical communities, engineering posts, migration discussions, and company-owned support or project surfaces.

#### Important lessons from execution

A difficult bug or isolated defect is not automatically Technical Distress. The evidence must support the broader loss-of-agency thesis required by the managed signal definition.

If a specific remediation is already in progress, the historical distress condition does not automatically remain current. A Moderate or Strong in-progress-remediation signal requires separate current evidence that:

1. material impairment still exists; and
2. substantial remediation work still remains.

Evidence that only minor cleanup, rollout, monitoring, validation, or closeout remains does not support the commercial thesis. Follow the current operator rules for the special recency gate that applies to remaining-work evidence during active remediation.

#### Outreach thesis

The outreach thesis is project rescue, technical diagnosis, stabilization, or implementation help that restores the organization's ability to safely move the system forward.

### Ecosystem Adjacency

#### What the campaign looks for

Ecosystem Adjacency identifies organizations using a technology Cartertek can directly modify, extend, integrate, or customize when those organizations publicly describe implementation gaps or implementation blockage.

The important adjacency is **technical capability**: Cartertek can work directly on the relevant ecosystem rather than merely advise around it.

Frappe and ERPNext were the first ecosystem used to validate this process.

#### Current signal patterns

Two useful patterns emerged from execution:

- **Product implementation gap** — the organization has a real workflow requirement that the current product does not satisfy, with evidence that the gap matters enough to create plausible implementation work.
- **Ecosystem implementation blockage** — the organization is materially blocked while trying to implement, extend, migrate, or operate within the ecosystem, and meaningful technical work remains.

A feature request or complaint is not automatically a strong prospect. The evidence must establish real workflow impact and the current implementation need required by the managed signal definition.

#### Important lessons from execution

Public implementation discussions often begin with a username or issue author rather than a clean company identity. Identity resolution may therefore be a substantial part of prospect research.

Do not assume the issue author is the best outreach contact. After the organization is identified, perform the normal role-selection and contact-research process.

When a selected role requires signal-specific relevance, job title alone is insufficient. The research must affirmatively establish why that person is connected to the qualifying implementation problem.

#### Outreach thesis

The outreach thesis is that Cartertek can directly implement, extend, or unblock the relevant system because the work falls inside an ecosystem Cartertek can modify.

## Prospect identity and contact research

Contact research begins **after** the prospect and qualifying evidence are understood.

Follow `docs/operator_workflow/identity-contact-research.md` rather than inventing contact logic from titles alone.

The practical sequence is:

1. establish the organization's canonical identity;
2. select the primary roles required by the playbook for this specific prospect;
3. research each selected role separately;
4. verify that a named person actually occupies the claimed role;
5. establish signal-specific relevance where the role requires it;
6. search for a directly attributable contact path;
7. preserve unresolved primary roles rather than forcing a weak match.

### Role proximity matters more than seniority

The best contact is usually the person closest to the qualifying work, not automatically the most senior executive.

Research should distinguish among the economic buyer, pain owner, technical owner, product or operations owner, and other roles defined by the playbook.

### Do not guess contact information

Never reconstruct or infer a personal email address from a company pattern and store it as verified.

Prefer directly published, person-attributable email addresses. A public personal email may be usable when identity is firmly established, but record it accurately as personal rather than presenting it as a company mailbox.

Generic company inboxes should remain generic contacts and should not be attached to a named person.

### Deep contact research is allowed when justified

For high-quality prospects, contact discovery may require multiple passes and creative identity research across official pages, public profiles, conference material, code history, archived professional material, industry documents, or other public records.

The standard is evidence, not convenience. Stop short of guessing.

## Prospect positioning before drafting

Before drafting the initial message, make the outreach position explicit.

Confirm:

- what qualifying signal is being used;
- what work the evidence suggests;
- why Cartertek is relevant to that work;
- which contact is being addressed and why;
- what scope of help can be stated accurately without overcommitting.

This is the bridge between research and writing. Do not make the writer rediscover the prospect thesis from raw evidence.

## Initial message drafting

Follow the current `docs/operator_workflow/message-drafting.md` and `docs/operator_workflow/initial-outreach.md` procedures.

The most important process rules established during execution are summarized below.

### The assigned template is immutable during drafting

The playbook's message template is the outer structure. Message drafting means filling the content the template allows.

Do not rewrite template-supplied greeting, wrapper, CTA, spacing, signature, or other fixed text while drafting a prospect message.

If the template itself needs improvement, change it as a separate template-maintenance task.

### Introduce the source accurately

The opening should identify the actual source item conversationally and from the recipient's perspective.

Do not pretend Cartertek has inside knowledge. Do not describe a public issue, post, launch, job listing, or implementation discussion as something more direct than it is.

### Use the evidence selectively

The message is not a research summary.

Use only enough evidence to establish why Cartertek is reaching out and what work appears relevant. Do not retell the signal record, dump implementation details, or diagnose the prospect from the outside.

### State relevance directly

The message should make clear what Cartertek could actually do in relation to the observed work.

Do not write a sentence that sounds like an answer to an unasked question such as "where Cartertek could help is..." or "this looks like a good fit."

State the relevant work naturally as part of the message.

### Use active voice and calibrated claims

Prefer active voice throughout.

Do not use vague language merely to avoid overcommitting. Be direct about the work while keeping the claimed scope accurate to what the public evidence supports.

### Avoid formulaic substitution

The template may be shared across prospects, but the authored body should not read like the same sentence with nouns replaced.

Use the actual source, work, recipient role, and Cartertek relevance to determine the wording.

## Sending and interaction recording

Initial outreach remains manual and reviewed.

Before sending:

1. read the rendered message as the recipient will receive it;
2. confirm the recipient is the intended primary contact;
3. confirm the sender field and delivery address;
4. confirm the message still matches the current evidence;
5. send through the appropriate channel;
6. record the touchpoint and sent content in SEI.

Do not use bulk blasting or unreviewed AI auto-send.

## Follow-up and reactivation

Follow-up is part of the lifecycle of an existing prospect. It is not a separate prospecting strategy.

For an unanswered prospect, the next action may be another message, another relevant contact, another appropriate channel, or stopping active follow-up. The exact cadence should be defined by the applicable playbook or current operating procedure rather than improvised independently for every prospect.

Reactivation means revisiting a known prospect when **new evidence makes the account timely again**. Examples include a new qualifying signal, a materially changed implementation state, a new launch, renewed hiring friction, or another current development relevant to the original thesis.

Do not treat the mere passage of time as a new signal.

## Response handling and CRM handoff

When a prospect replies, record the outcome and make the next action explicit.

Typical actions include:

- reply or answer a question;
- route to the correct person;
- schedule a call;
- mark for later follow-up;
- stop outreach;
- update CRM handoff or sales records when appropriate.

SEI is the pre-CRM research and outreach layer. CRM handoff is explicit and user-controlled. A Qualified or Manually Approved prospect may be approved for CRM handoff once the identity and contact requirements are satisfied; a prospect does not need to have replied before a CRM Lead can be created.

Deal creation is different. Do not create a Deal merely because a prospect was researched, qualified, or converted to a CRM Lead. A Deal requires a commercial basis such as positive interest, a meeting, a scoped discussion, proposal or diagnostic interest, or an explicit manager override.

Follow `docs/operator_workflow/crm-conversion.md` for the current handoff procedure.

## Learning from outcomes

Cartertek should preserve outreach outcomes so the process can improve, but the outreach program does **not** depend on high-volume experimentation.

Record enough information to answer practical questions over time:

- Which campaign sources produce defensible prospects?
- Which qualifying patterns repeatedly produce weak or misleading leads?
- Which kinds of contacts are reachable and relevant?
- Which messages or approaches produce useful responses?
- Where does the workflow repeatedly stall?

Use obvious patterns and accumulated evidence to revise playbooks, signal definitions, contact rules, and drafting guidance when justified.

Do not create artificial A/B tests, complex attribution schemes, or optimization work that is disproportionate to the small outreach volume.

## Operating rhythm

The working rhythm is simple:

1. choose one validated playbook and research batch;
2. develop and review evidence-first signals;
3. allow qualification to follow from published evidence;
4. complete identity and primary-contact research for qualified prospects;
5. position the prospect for outreach;
6. draft and review the initial message using the assigned template;
7. send manually;
8. work follow-up, responses, and reactivation as they become due;
9. hand real commercial opportunities into CRM;
10. feed concrete lessons back into the playbook or operator docs.

Keep batches small enough that research quality and source verification remain high.

## Scope boundaries

This guide covers Cartertek's current validated signal-driven cold-outreach process.

It does not treat every possible lead source, buyer-intent surface, referral path, partnership concept, directory, community, or channel as a separate outreach strategy.

New prospecting strategies should be added here only after they have been deliberately developed and validated. Do not mix exploratory strategy ideas into the current operating process prematurely.

## Non-Goals and Safety Boundaries

The outreach system is deliberately not a mass outbound machine.

Do not use it for:

```
mass scraping
automatic cold email blasting
AI auto-send
automatic LinkedIn messaging
automatic contact-form submission
unreviewed autonomous prospecting
automatic CRM conversion
generic lead scoring detached from evidence
```

The system should support disciplined, context-specific outreach.

Automation may assist with intake, organization, drafting, reporting, and workflow visibility, but the operator remains responsible for judgment and sending.

## Frappe SEI implementation

Sales Engagement and Intelligence (SEI) supports this process as the pre-CRM operating layer. It stores prospects, evidence-backed signals, playbook context, selected contacts, message drafts, interactions, and lifecycle state, then supports explicit handoff into Frappe CRM when a prospect becomes commercially real.

Do not infer the outreach process from the database schema. The strategy guide defines the operating model; the current operator docs define execution details; the live playbooks and managed signal definitions define campaign-specific rules.

Start with:

`docs/operator_workflow/README.md`
