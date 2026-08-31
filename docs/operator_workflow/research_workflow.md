# Research Workflow

Research moves from source discovery to candidate signal evaluation. The goal is not to find companies that seem like Cartertek could help. The goal is to find source-backed evidence that supports a managed SEI Signal Type.

## Workflow

1. Select a Research Arena.
2. When a plausible research path appears, create a Draft Signal immediately. The Prospect does not need to exist yet and the draft may begin with only the information currently known.
3. Use that Draft Signal as the working record for the path. Add candidate sources, Observed Facts, analysis, possible Signal Type, disqualifier checks, and uncertainty as the research develops.
4. Open every exact source URL that may ultimately be stored on an Observed Facts row.
5. Confirm that each opened page contains the expected entity, document or role, and every complete quotation recorded from it.
6. Identify the author or speaker of the evidence, verify their relationship to the Prospect, and determine whether the source is first-party, second-party, or third-party. Do not infer organizational authorship from where the content is hosted.
7. Continually revise the draft as evidence strengthens, changes the interpretation, or rules out the path.
8. If the path is disproven, delete the Draft Signal. Do not create a Prospect merely to preserve a failed research path.
9. If the path remains supported, create or identify the Prospect, link the Draft Signal to it, finish every field required by the managed Signal Type and evidence rules, and publish the Signal.
10. Only Published Signals participate in qualification, lifecycle progression, derived Playbooks or Research Arenas, and message-drafting context.


## Draft Signals are the research workspace

Create a separate Draft Signal for each plausible research path rather than keeping candidate evidence only in chat, scratch notes, or an unstructured prospect record. A draft can exist before its Prospect and all fields are optional while the path is being investigated.

Update the same draft throughout the research path:

- add each candidate fact and its source metadata as soon as it is found;
- record tentative Signal Type and strength only when useful, and revise them freely;
- capture disqualifiers, contradictions, missing evidence, and uncertainty as they emerge;
- keep separate paths in separate Draft Signals so a disproven theory can be deleted without losing valid work.

A Draft Signal is not evidence that a Prospect qualifies. It must not be treated as a completed research result, used for outreach positioning, or allowed to advance lifecycle state.

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

When the path is disproven, delete the draft. When the path is supported, create or locate the Prospect, attach the draft, complete the publication requirements, and publish it. Publication is the point at which the research path becomes validated SEI evidence.

## Discovery source vs evidence source

A discovery source is how you found something.
An evidence source is the exact page, post, listing, issue, or artifact that proves the signal.

The signal source URL should normally be the evidence source, not the discovery source.

A search page may help discover a candidate, but the signal should link to the specific source item. Opening a discovery result, API record, cached copy, or search snippet does not count as opening the evidence source. Every exact URL intended for a fact row's `source_url` must itself be opened and reviewed during the current research run.

A thread or directory may help discover a candidate, but the signal should link to the specific post, listing, profile, or artifact that supports the claim.

An aggregator may be useful context, but the evaluator should prefer the original source when available.

## Authorship and provenance verification

The evidence source must be understood as a piece of communication by a specific author or speaker, not merely as content found under a Prospect's name or infrastructure. Verify who created the relevant statement and what relationship that person, account, organization, or automated system has to the Prospect.

Do not assume that content is first-party because it appears:

- in a company-owned GitHub repository or issue tracker;
- on a company community forum or support board;
- under a company subreddit, social tag, marketplace listing, or discussion thread;
- on a company-owned domain that permits user-generated content;
- in a repository where an external contributor has detailed technical knowledge.

If the author is an employee, maintainer, contractor, customer, external contributor, anonymous user, reporter, vendor, automated agent, or other third party, preserve that distinction. If affiliation is unknown, say so and narrow the claim accordingly. The venue tells you where the statement appears; it does not by itself tell you who is speaking for the organization.

## Source review checklist

Before creating or strengthening a signal, check:

- Did I open the exact URL that will be stored?
- Does that exact page contain the expected company or entity?
- Who authored or spoke the relevant statement?
- What is the author's or speaker's relationship to the Prospect, and can that relationship be verified?
- Is the evidence first-party, second-party, or third-party?
- Am I attributing a statement to the company only because of the domain, repository, issue tracker, forum, or other hosting venue?
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
- author or speaker identity and verified relationship to the Prospect
- provenance classification / attribution limits
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
