# Research Workflow

Research moves from source discovery to candidate signal evaluation. The goal is not to find companies that seem like Cartertek could help. The goal is to find source-backed evidence that supports a managed SEI Signal Type.

## Workflow

1. Select a Research Arena.
2. When a plausible research path appears, create a Draft Signal immediately. The Prospect does not need to exist yet and the draft may begin with only the information currently known.
3. Use that Draft Signal as the working record for the path. Add candidate sources, Observed Facts, analysis, possible Signal Type, disqualifier checks, and uncertainty as the research develops.
4. Open every exact source URL that may ultimately be stored on an Observed Facts row.
5. Confirm that each opened page contains the expected entity, document or role, and every complete quotation recorded from it. Identify who actually authored or spoke the relevant statement and what relationship, if any, that speaker has to the Prospect.
6. Continually revise the draft as evidence strengthens, changes the interpretation, or rules out the path.
7. If the path is disproven, delete the Draft Signal. Do not create a Prospect merely to preserve a failed research path.
8. If the signal path remains supported, perform the **Prospect eligibility review** below before creating or linking a Prospect. A supported signal is not by itself permission to create a Prospect.
9. Create or identify a Prospect only when the candidate organization passes the Prospect eligibility review. If it does not pass, do not create a Prospect, do not promote the Draft Signal, and do not continue treating the candidate as an outreach prospect. Preserve useful discovery context outside the Prospect workflow as appropriate.
10. For an eligible prospect, search for an existing organization-level Prospect first. Create one only when no appropriate record exists, link the Draft Signal, finish every field required by the managed Signal Type and evidence rules, and publish the Signal.
11. Only Published Signals participate in qualification, lifecycle progression, derived Playbooks or Research Arenas, and message-drafting context. After publication, complete the post-publication Prospect review below and let Frappe apply qualification and lifecycle state.


## Draft Signals are the research workspace

Create a separate Draft Signal for each plausible research path rather than keeping candidate evidence only in chat, scratch notes, or an unstructured prospect record. A draft can exist before its Prospect and all fields are optional while the path is being investigated.

Update the same draft throughout the research path:

- add each candidate fact and its source metadata as soon as it is found;
- record tentative Signal Type and strength only when useful, and revise them freely;
- capture disqualifiers, contradictions, missing evidence, and uncertainty as they emerge;
- keep separate paths in separate Draft Signals so a disproven theory can be deleted without losing valid work.

A Draft Signal is not evidence that a Prospect qualifies. It must not be treated as a completed research result, used for outreach positioning, or allowed to advance lifecycle state.

## Prospect eligibility review

A signal path can be valid even when the organization or entity behind it is not an acceptable Cartertek outreach prospect. **Prospect eligibility is a mandatory gate before a Draft Signal may create or link to a new Prospect.** Do not equate a Strong or otherwise supported Signal with an eligible Prospect.

Before creating a Prospect from a Draft Signal, verify all of the following:

- **Identifiable organization:** the Prospect can represent a specific organization or genuinely separate operating entity, using its canonical public identity. Do not create a Prospect for a product, platform, repository, open-source project, technical system, initiative, migration, location, or research path merely because the Signal concerns it.
- **Correct prospect identity:** determine which organization actually experiences the condition and would be the subject of outreach. Repository, project, ecosystem, or community context does not by itself establish that the hosted project or venue is the prospect.
- **Commercial actionability:** Cartertek can realistically pursue the organization as an outreach opportunity. Keep this decision separate from Signal strength: commercial actionability must not raise or lower the Signal's strength, but a candidate that is not realistically pursuable must not become or remain an outreach Prospect.
- **Plausible outreach organization:** there is an organizational structure or responsible party to whom Cartertek could plausibly direct outreach about the observed condition. The exact named contact does not need to be known yet; contact research comes later.
- **No protected duplicate or prohibited path:** search by canonical name, website, and normalized domain before creation. Reuse an existing organization-level Prospect where appropriate, and never create a duplicate to bypass Rejected or Do Not Contact state.
- **Evidence belongs to this Prospect:** the verified Signal evidence and organizational attribution support the candidate organization being the party experiencing the condition. Do not transfer a project-, contributor-, customer-, ecosystem-, or third-party problem onto an organization without evidence establishing that relationship.

If any required eligibility point fails, **do not create the Prospect and do not promote the Draft Signal**. The research path may still describe a real condition, but it is not an acceptable prospect for this outreach workflow. Delete the Draft Signal when the path is no longer useful as an actionable research path; do not create a Prospect merely to preserve it.

Only prospects that pass this eligibility review may be created from a Draft Signal or considered further for qualification, contact research, positioning, or outreach.

## Post-publication Prospect review

After an eligible Prospect has been created or identified and its Signal has been published, review the resulting Prospect before considering the research batch complete. Prospect review confirms that the record belongs in the correct operational queue; it is not a substitute for the pre-creation eligibility gate above.

Review the SEI Prospect form for identity, Research Arena, source URL, offer, signal summary, notes, contact path, qualification status, lifecycle status, and CRM links. Review related Published Signals and their managed Signal Types to confirm the derived thesis list, evidence, and timing are current and specific.

Use the queue state as follows:

- **Needs Research:** insufficient evidence or context; continue research before dispositioning.
- **Research Complete:** evidence is complete enough for human review, normally because qualification is Needs Review.
- **Rejected:** research is complete and the prospect should not continue because no qualifying outreach evidence exists.
- **Find Contact:** prospect looks relevant but no usable contact path exists. Use [Prospect identity and contact research](identity-contact-research.md) to complete identity context, select primary contact roles, and research validated contacts.
- **Qualified:** enough evidence exists, but CRM conversion has not been prepared.
- **Ready for CRM Conversion:** explicit operator action marked the prospect ready.
- **Do Not Contact:** protected suppression state.

Do Not Contact and Rejected states are protected. Do not bypass them through API updates, duplicate Prospect creation, import fixes, or CRM conversion actions.

## Develop the draft in evidence-first stages

Do not fill a draft as though every field has the same evidentiary status. Research should move through these stages:

1. **Candidate path:** record why the path appears plausible, the discovery source, and what still needs verification. Do not present candidate notes as Observed Facts.
2. **Verified evidence:** open the exact source and copy complete verbatim sentences into Observed Facts, with fact-level source metadata. Candidate summaries, search snippets, and researcher notes must remain outside Observed Facts.
3. **Context and latest state:** read enough surrounding material to determine what the quotation means, whether the condition is current or resolved, and whether later evidence contradicts or narrows it.
4. **Classification:** only after verified facts exist, select a candidate Signal Type and strength. Build the claim from the evidence; do not search for wording that supports a classification chosen in advance.
5. **Publication audit:** compare each stored fact against its exact source, check every material claim clause, and publish only when the completed record passes all managed rules.

The draft may contain tentative analysis and competing interpretations, but `observed_facts` is reserved for source text that has already passed exact-source verification. If a useful proposition has not yet been captured as a complete verbatim sentence, record it as a research note or evidence gap rather than manufacturing a polished fact row.

## One draft per research assertion

A research path is one specific assertion that could become one Signal. Create separate drafts when evidence may support different Signal Types, different triggering events, or materially different claims. Do not combine unrelated facts merely because they concern the same Prospect or launch.

Several individually insufficient facts do not become a valid signal through accumulation. Together they must establish the defining assertion of the selected Signal Type. If every fact omits the required consequence, the collection still omits it.

When the path is disproven, delete the draft. When the Signal path is supported, perform the Prospect eligibility review before creating or locating a Prospect. Only an eligible candidate may proceed to Prospect creation/linking, publication, and further consideration. Publication is the point at which the research path becomes validated SEI evidence.

## Discovery source vs evidence source

A discovery source is how you found something.
An evidence source is the exact page, post, listing, issue, or artifact that proves the signal.

The signal source URL should normally be the evidence source, not the discovery source.

A search page may help discover a candidate, but the signal should link to the specific source item. Opening a discovery result, API record, cached copy, or search snippet does not count as opening the evidence source. Every exact URL intended for a fact row's `source_url` must itself be opened and reviewed during the current research run.

A thread or directory may help discover a candidate, but the signal should link to the specific post, listing, profile, or artifact that supports the claim.

An aggregator may be useful context, but the evaluator should prefer the original source when available.

## Source review checklist

Before creating or strengthening a signal, check:

- Did I open the exact URL that will be stored?
- Does that exact page contain the expected company or entity?
- Who actually authored or spoke the relevant statement, and what is their relationship to the Prospect?
- Am I treating content as first-party only because it appears in the Prospect's repository, domain, forum, issue tracker, or other hosted venue?
- Does it contain the expected role, post, RFP, issue, or document?
- Does it contain every complete quotation proposed for the Observed Facts rows?
- Is it a real content page rather than a generic ATS shell, board homepage, login page, or error page?
- Does this source point to one specific piece of evidence?
- Does the source directly support the signal claim?
- Is the source current enough for the claim being made?
- Is the source primary, or merely an aggregator? If it is user-generated or third-party content on a Prospect-controlled venue, am I preserving that provenance rather than attributing it to the Prospect?
- If this is a collection, list, or search page, have I found the specific item?

## Research output

A useful research result identifies:

- prospect
- exact evidence source
- observed facts
- candidate Signal Type
- evidence specificity
- disqualifiers checked
- proposed strength
- uncertainty

If the exact evidence source is missing, or the exact URL does not contain the expected entity, document, and complete quotation, keep the item as discovery context or reject it. Do not create a Moderate or Strong signal from that URL.


Each Observed Facts row stores its own `source_url`, `source_date`, `evidence_basis`, and `evidence_specificity`. At least one fact must supply any value required for the signal; multiple facts may use different sources and evidence classifications.

## Fact-level evidence metadata

`evidence_basis`, `evidence_specificity`, `source_url`, and `source_date` belong to each Observed Facts row, not to the Signal. Classify and cite each fact independently. When a rule requires one of these values, the signal satisfies the rule when at least one fact row supplies the required value. Do not copy a source classification across unrelated facts merely to satisfy validation.
