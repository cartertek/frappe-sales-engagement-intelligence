# Research Workflow

Research moves from source discovery to candidate signal evaluation. The goal is not to find companies that seem like Cartertek could help. The goal is to find source-backed evidence that supports a managed SEI Signal Type.

## Workflow

1. Select a source arena.
2. Search for candidate evidence.
3. Open the exact source URL that would be stored on the signal.
4. Confirm that the opened page contains the expected entity, the expected document or role, and the complete proposed `observed_fact` quotation.
5. Identify what the source directly says or shows.
6. Decide whether the source supports any managed Signal Type.
7. If yes, create or update a signal.
8. If no, reject the candidate or keep it as non-counting context.

## Discovery source vs evidence source

A discovery source is how you found something.
An evidence source is the exact page, post, listing, issue, or artifact that proves the signal.

The signal source URL should normally be the evidence source, not the discovery source.

A search page may help discover a candidate, but the signal should link to the specific source item. Opening a discovery result, API record, cached copy, or search snippet does not count as opening the evidence source. The exact URL intended for `source_url` must itself be opened and reviewed during the current research run.

A thread or directory may help discover a candidate, but the signal should link to the specific post, listing, profile, or artifact that supports the claim.

An aggregator may be useful context, but the evaluator should prefer the original source when available.

## Source review checklist

Before creating or strengthening a signal, check:

- Did I open the exact URL that will be stored?
- Does that exact page contain the expected company or entity?
- Does it contain the expected role, post, RFP, issue, or document?
- Does it contain the complete `observed_fact` quotation?
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
- observed fact
- candidate Signal Type
- evidence specificity
- disqualifiers checked
- proposed strength
- uncertainty

If the exact evidence source is missing, or the exact URL does not contain the expected entity, document, and complete quotation, keep the item as discovery context or reject it. Do not create a Moderate or Strong signal from that URL.
