# Initial Outreach

Initial outreach is the ordered operator process for turning a qualified, contactable Prospect into a reviewed, unsent outreach draft. It consists of two required stages that must be completed in order:

1. [Prospect positioning](prospect-positioning.md)
2. [Message drafting](message-drafting.md)

These are not independent optional workflows. Positioning produces the interpreted outreach direction required by message drafting. Message drafting consumes that completed positioning and turns it into a saved draft. Do not begin message drafting before prospect positioning is complete.

Initial outreach remains a preparation workflow. Completing either stage does not send a message, mark a Prospect contacted, change lifecycle status, or create CRM records.

## Entry requirements

Begin the initial outreach process only when:

- the Prospect is not Rejected or Do Not Contact
- enough Published Signal evidence exists to justify outreach
- the applicable Playbook and managed Signal Types are available
- the source evidence can be reviewed
- the intended contact path is known or a usable contact has been selected
- the Prospect is in an outreach-ready working state, normally Find Contact after contact research is complete or Ready for CRM Conversion when the operator is also preparing CRM handoff

If evidence, positioning inputs, or contact context are incomplete, return to the relevant research (including Prospect eligibility/review), signal-evaluation, or contact-research workflow before proceeding.

## Stage 1: Prospect positioning

Complete [Prospect positioning](prospect-positioning.md) first.

This stage interprets the Prospect's evidence into an outreach direction. It must establish:

- why outreach is timely
- what the signal actually supports
- what work or operational problem the message should address
- how the Playbook applies
- how each applicable Signal Type refines the positioning
- why Cartertek is relevant
- what bounded offer direction is defensible
- which claims, terms, or framings should be avoided

### Positioning completion gate

Do not advance to message drafting until the positioning:

- is based on reviewed source evidence rather than labels or summaries alone
- distinguishes observed facts from inference
- identifies the actual work or problem beneath broad source terminology
- separates the timing signal from the substance of Cartertek's offer
- applies both Playbook and Signal Type guidance
- explains Cartertek's relevance in prospect-specific terms
- defines a bounded, evidence-supported offer direction
- records important language and claim restrictions
- is complete enough that drafting does not need to rediscover the meaning of the evidence

## Stage 2: Message drafting

After the positioning completion gate is satisfied, complete [Message drafting](message-drafting.md).

This stage combines:

- completed prospect positioning
- current operator drafting guidance
- Playbook message guidance
- applicable Signal Type message guidance
- Prospect and contact data
- source evidence
- the selected message and subject templates

It then produces a complete outreach message, renders it through the template, saves it to the Prospect's Message Drafts table, and verifies the stored result.

### Drafting completion gate

The initial outreach process is complete only when the draft:

- accurately reflects the completed positioning
- is specific to the Prospect and grounded in observable evidence
- follows the current Playbook and Signal Type guidance
- uses the selected template without duplicated greetings, signatures, or calls to action
- has a correctly rendered subject and HTML body
- preserves intentional template whitespace
- identifies the intended contact, platform, sender, and template
- remains unsent with `sent` unchecked and `sent_on` empty
- has been read back from SEI and passed the final drafting quality-control checklist

## Ordered process summary

```text
Qualified and contactable Prospect
-> Complete Prospect Positioning
-> Pass Positioning Completion Gate
-> Complete Message Drafting
-> Save and Read Back Unsent Draft
-> Pass Drafting Completion Gate
-> Initial Outreach Preparation Complete
-> Manual Operator Review and Send
```

Do not skip positioning, draft from incomplete evidence, or treat a successfully executed save command as completion. Each stage must satisfy its completion gate before the next action begins.
