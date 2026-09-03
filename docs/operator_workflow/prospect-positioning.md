# Prospect Positioning

Prospect positioning is **Stage 1** of the ordered [Initial Outreach](initial-outreach.md) process. Complete it and satisfy its completion gate before beginning message drafting.

Prospect positioning converts completed research into a usable outreach direction. Complete positioning before drafting a message. Positioning explains why the prospect is worth contacting, why Cartertek may be relevant now, what work or operational problem outreach should address, how Cartertek should be presented, and which claims or language should be avoided.

Positioning is not a draft email. It is interpreted context that lets the drafting process produce a message that is specific, accurate, and commercially useful.

## Required deliverable

The deliverable of Prospect Positioning is a **high-quality, prospect-specific `offer` stored on the Prospect**. That offer is the positioning result that the next [Message Drafting](message-drafting.md) procedure will consume when composing the initial outreach message.

The offer must identify the bounded work or outcome Cartertek can credibly help with based on the evidence, Playbook, and Signal Type guidance. A generic Playbook default, filler value, broad service category, or merely plausible consulting idea is not a completed positioning deliverable. Internal reasoning, notes, or an ability to draft a message are not substitutes for writing the completed offer to the Prospect.

Offer construction has a blocking prerequisite: the Prospect's `signal_summary` must first be accurate and complete. The signal summary is the evidence synthesis on which the positioning procedure builds. **Do not develop, revise, approve, or store the offer until the signal-summary hard gate in Step 2 passes.**

## Required inputs

Before developing positioning, load and review:

- the Prospect record
- Research Arena and source context
- all linked Published Signals
- Signal Type, strength, evidence basis, and managed Signal Type guidance
- source URLs and Observed Facts
- the assigned Playbook and its message guidance
- lifecycle and qualification status
- prospect type
- known contact roles and intended contact path
- current thesis, offer, asset, and prior positioning when present
- prior touchpoints or outcomes when relevant

Do not develop positioning from the company name, industry, role title, signal label, or a short extracted summary alone.

## Positioning procedure

### 1. Read the underlying evidence

Read the actual material that produced the signal. Depending on the arena, this may be a job posting, founder post, product announcement, GitHub issue, support thread, company page, public complaint, directory profile, technical discussion, or another observable artifact.

Identify what was directly observed and distinguish it from interpretation. Preserve the evidence-first rule:

```text
Observed fact != inferred pattern
```

Do not turn an inference into a claim of fact.

### 2. Establish and hard-gate an accurate, complete signal summary

Use the underlying evidence from Step 1 to verify the Prospect's `signal_summary`. The summary must accurately and completely synthesize the signal evidence that matters to outreach, including the observed condition, the material consequence or operational meaning established by the evidence, and the current context needed to understand why the signal is relevant now. It must preserve the boundary between observed fact and inference and must not overstate what the evidence proves.

A stale summary, filler such as `Technical Distress evidence collected during research batch`, a generic Signal Type label, a summary that omits material evidence or current context, or a summary that conflicts with the Published Signals or Observed Facts fails this step. When the existing `signal_summary` fails, rewrite it and store the corrected summary on the Prospect before continuing.

Then determine what the signal establishes. Explain why the evidence makes outreach timely. The signal may establish persistent hiring friction, a technical capacity gap, visible production problems, a manual or fragmented process, post-launch pressure, a capability mismatch, project-delivery risk, or demand for integration, automation, stabilization, or technical reinforcement.

State what the signal does and does not prove. For example, an open role may establish that the company wants additional capacity. It does not prove that the company is poorly managed, technically weak, or unable to complete the work.

#### Signal-summary hard gate

Do not proceed to Step 3 or begin constructing the offer unless all of the following are true:

- the actual underlying evidence has been read
- the stored `signal_summary` accurately reflects the relevant Published Signal evidence
- the stored `signal_summary` is complete enough to preserve the material condition, consequence, and current context needed for positioning
- observed facts and inference remain distinct
- no filler, stale, contradictory, or materially incomplete summary remains

If any check fails, correct `signal_summary`, reread it against the underlying evidence, and rerun this gate from the beginning. **Offer construction is blocked until this gate passes.**

### 3. Identify the actual work or problem

Look beneath broad labels such as `infrastructure`, `platform`, `systems`, `operations`, `tooling`, or `product engineering`. Use the concrete details beneath those labels to identify what the company is actually trying to accomplish or improve.

Examples include:

- improving a deployment process
- reducing manual handoffs
- connecting fragmented internal systems
- making AI development processes more reliable
- simplifying knowledge transfer
- automating internal workflows
- stabilizing production systems
- moving a delayed product initiative forward

Interpret the operational meaning of the evidence rather than repeating the source's vocabulary.

### 4. Separate timing from offer substance

Answer these questions independently:

1. Why is outreach timely?
2. What can Cartertek credibly help with?

The signal often answers the first question while the source details answer the second. For a Failed Hiring prospect, the open or long-running search may explain the timing, while the role responsibilities identify the work Cartertek could help advance.

Do not make the offer only “help while you hire.” Identify the actual work that could move during that period.

### 5. Apply the assigned Playbook

Use the Playbook to determine the commercial framing, intended contact role, appropriate offer, relationship to the prospect's existing plan, and claims the outreach must avoid.

For Failed Hiring positioning:

- do not describe recruitment as a failure
- do not sound like a recruiter
- do not suggest abandoning the permanent search
- do not present Cartertek as a replacement employee
- position Cartertek as a consultancy that can help move relevant work forward while permanent hiring continues

### 6. Apply Signal Type guidance separately

Signal Type guidance refines the Playbook; it does not replace it. Determine which evidence should lead, which consequences matter, which interpretations are justified, and which overstatements must be avoided.

For a technical-capacity signal, positioning may emphasize the bounded technical area, the operational consequence, the work delayed or made unreliable, and the outcome Cartertek could help restore. Do not generalize a specific constraint into a claim about the entire company.

### 7. Determine Cartertek's relevance

Connect the evidence to Cartertek through a clear chain:

```text
Observed evidence
-> operational meaning
-> Cartertek capability
-> useful outcome
```

The relevance must be specific enough to refer back to the evidence.

Weak:

> Cartertek can help with technical challenges.

Stronger:

> Cartertek can help simplify and automate the internal workflows described in the posting so the company is less dependent on manual coordination.

Do not turn positioning into a delivery plan. Identify the work and result, not an implementation sprint, architecture, or task list.

### 8. Write the high-quality offer

Using only positioning that follows from the signal summary that passed the Step 2 hard gate, identify the kind of help Cartertek could offer without inventing a project. Appropriate directions may include:

- moving a defined piece of product work forward
- stabilizing a production process
- improving an internal workflow
- reducing manual operational work
- connecting fragmented tools or systems
- making an AI development process more reliable
- supporting a delayed modernization initiative
- providing technical reinforcement while hiring continues

The offer must be plausible, evidence-supported, commercially meaningful, narrow enough to avoid speculation, and broad enough not to fabricate scope. It must be prospect-specific enough to guide the next Message Drafting procedure toward the actual work or outcome Cartertek can help with.

Write the completed offer to the Prospect's `offer` field. Do not leave a generic Playbook default, filler value, stale offer, or temporary working language in place. The stored `offer` is the required Stage 1 deliverable.

### 9. Identify language and claims to avoid

Record prospect-specific risks, including:

- source jargon that would sound unnatural in outreach
- marketing language that should not be repeated
- technical shorthand that needs translation
- conclusions the evidence does not support
- accusatory or opportunistic language
- wording that could imply Cartertek replaces a permanent role
- terminology likely to confuse the intended contact
- distinctive phrases that would reveal mechanical paraphrasing

Preserve technical terms only when they are necessary and natural, such as the name of a specific technology the prospect actually uses.

### 10. Validate the completed positioning deliverable

Use the following questions to verify that the stored `offer` is supported by complete positioning rather than by a generic service idea or an unexamined default. The completed positioning must answer:

- What source should the message mention?
- What did the source reveal?
- What is the underlying operational problem?
- Why does that matter now?
- What work could Cartertek credibly address?
- What result should Cartertek emphasize?
- How should continued hiring or the prospect's existing plan be acknowledged?
- What should the message avoid saying?
- Which language should be translated or softened?
- Which contact is most appropriate and why?

## Positioning quality checks

Before completing positioning, confirm:

- the Step 2 signal-summary hard gate passed before any offer was developed or approved
- the stored `signal_summary` remains accurate and complete against the underlying evidence
- the source evidence was actually read
- observed facts and inference remain distinct
- the positioning identifies the real work, not only a broad source label
- the signal's timing function is separated from the offer
- Playbook guidance and Signal Type guidance are both applied
- Cartertek's relevance clearly follows from the evidence
- the offer is bounded and not invented
- the stored `offer` is high-quality, prospect-specific, and derived from the validated signal summary plus the underlying evidence, Playbook, and Signal Type guidance
- the stored `offer` is suitable as the positioning input for the next Message Drafting procedure
- no filler, generic Playbook default, stale offer, or temporary working value remains in `offer`
- source jargon is not repeated mechanically
- the positioning does not imply facts the source does not establish
- the guidance is specific enough to support a prospect-specific draft without rediscovering the evidence's meaning

## Completion gate

Prospect Positioning is complete only when both of its persisted outputs are valid:

1. `signal_summary` has passed the Step 2 accuracy-and-completeness hard gate.
2. `offer` contains the high-quality, prospect-specific positioning deliverable produced from that validated summary and the remainder of this procedure.

If either field is missing, stale, filler, generic, materially incomplete, unsupported by the evidence, or otherwise fails the checks above, Stage 1 is incomplete. Do not begin Message Drafting. Correct the affected field, rerun the applicable positioning checks, and pass this completion gate before proceeding.
