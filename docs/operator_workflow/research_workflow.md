# Research Workflow

Research moves from source discovery to candidate signal evaluation. The goal is not to find companies that seem like Cartertek could help. The goal is to find source-backed evidence that supports a managed SEI Signal Type.

## Workflow

1. Select a source arena.
2. When a plausible research path appears, create a Draft Signal immediately. The Prospect does not need to exist yet and the draft may begin with only the information currently known.
3. Use that Draft Signal as the working record for the path. Add candidate sources, Observed Facts, analysis, possible Signal Type, disqualifier checks, and uncertainty as the research develops.
4. Open every exact source URL that may ultimately be stored on an Observed Facts row.
5. Confirm that each opened page contains the expected entity, document or role, and every complete quotation recorded from it.
6. Continually revise the draft as evidence strengthens, changes the interpretation, or rules out the path.
7. If the path is disproven, delete the Draft Signal. Do not create a Prospect merely to preserve a failed research path.
8. If the path remains supported, create or identify the Prospect, link the Draft Signal to it, finish every field required by the managed Signal Type and evidence rules, and publish the Signal.
9. Only Published Signals participate in qualification, lifecycle progression, derived Playbooks or Research Arenas, and message-drafting context.


## Draft Signals are the research workspace

Create a separate Draft Signal for each plausible research path rather than keeping candidate evidence only in chat, scratch notes, or an unstructured prospect record. A draft can exist before its Prospect and all fields are optional while the path is being investigated.

Update the same draft throughout the research path:

- add each candidate fact and its source metadata as soon as it is found;
- record tentative Signal Type and strength only when useful, and revise them freely;
- capture disqualifiers, contradictions, missing evidence, and uncertainty as they emerge;
- keep separate paths in separate Draft Signals so a disproven theory can be deleted without losing valid work.

A Draft Signal is not evidence that a Prospect qualifies. It must not be treated as a completed research result, used for outreach positioning, or allowed to advance lifecycle state.

When the path is disproven, delete the draft. When the path is supported, create or locate the Prospect, attach the draft, complete the publication requirements, and publish it. Publication is the point at which the research path becomes validated SEI evidence.

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
- Does it contain the expected role, post, RFP, issue, or document?
- Does it contain every complete quotation proposed for the Observed Facts rows?
- Is it a real content page rather than a generic ATS shell, board homepage, login page, or error page?
- Does this source point to one specific piece of evidence?
- Does the source directly support the signal claim?
- Is the source current enough for the claim being made?
- Is the source primary, or merely an aggregator?
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
