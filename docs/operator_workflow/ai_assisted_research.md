# AI-Assisted Research

AI can help find and organize evidence, but it must not over-promote weak evidence.

AI-assisted research follows the same evidence-first rule as manual research:

A signal is not what the source reminds us of.
A signal is what the source directly supports.


## Agent draft discipline

The agent must create a Draft Signal when it begins pursuing a plausible signal path, not only after the path has been proven. The draft may be created before a Prospect exists and may contain only partial information.

The agent must then use that draft as its durable research workspace:

- append candidate Observed Facts and exact source metadata as they are verified;
- revise or remove facts when later context changes their meaning;
- fill analysis, candidate Signal Type, strength rationale, disqualifiers, and evidence gaps incrementally;
- preserve separate competing paths as separate drafts;
- delete a draft when its path is disproven.

When a path survives research, the agent must create or identify the Prospect, link the draft to that Prospect, complete every publication requirement, and publish the Signal. The agent must not treat a Draft Signal as completed evidence or use it to justify outreach.

The agent must keep three kinds of draft content distinct:

- **candidate notes:** summaries, snippets, hypotheses, and leads that still require verification;
- **verified Observed Facts:** complete verbatim sentences copied from exact opened sources, with row-level metadata;
- **analysis:** interpretation, candidate classification, disqualifiers, contradictions, latest-state assessment, and uncertainty.

Candidate notes must never be promoted into Observed Facts merely by rewriting them into clean prose. The agent's default summarization behavior is inappropriate for quotation fields.

## Agent research order

The agent must not start from a desired Signal Type, strength, prospect count, or Prospect outcome. It must proceed in this order:

1. capture candidate paths as drafts;
2. verify exact source text and metadata;
3. search for contradictory and newer evidence;
4. determine what the verified passages mean in context;
5. derive the claim, type, and strength from that evidence;
6. attempt to disprove the proposed signal;
7. publish only after a source-by-source audit.

Batch targets such as finding a requested number of Strong prospects are search objectives, not permission to relax evidence rules. A batch can legitimately produce few or no publishable signals.

## AI research protocol

For each proposed signal, AI must separate:

- verbatim source quotation of at least one complete sentence
- interpretation or paraphrase
- candidate Signal Type
- disqualifiers checked
- strength rationale
- uncertainty

## Exact-source verification gate

Before proposing or creating a Moderate or Strong signal, the assistant must open each exact URL that will be stored on the relevant Observed Facts row during the current research run. The opened page must contain the expected entity or company, the expected document or role, and each complete verbatim quotation and its matching fact-level source metadata. The assistant must also identify who actually authored or spoke the relevant statement and verify any relationship needed to attribute that statement to the Prospect; repository, domain, forum, or issue-tracker placement alone is not sufficient.

Search snippets, cached text, ATS APIs, job feeds, aggregators, and discovery results may identify candidates, but they do not prove that the proposed evidence URL is valid. The assistant must not construct or infer a public source URL from an ATS board slug, job ID, API response, or search result.

An HTTP success response is not sufficient. Generic ATS shells, board homepages, login pages, error pages, and pages that do not contain the expected entity, document, and quotation fail verification.

If exact-source verification fails, do not create or strengthen the signal from that URL. Continue researching for a valid evidence source or discard the candidate.

## Required AI output before creating signals

Before AI publishes a Signal or proposes that a draft is ready to publish, it should provide:

```text
Prospect:
Exact evidence source:
Exact URL opened:
Final URL after redirects:
Expected entity found:
Expected document or role found:
Observed Facts found verbatim (one row per fact):
Generic shell, login, or error page:
Observed fact (verbatim quotation; at least one complete sentence):
Signal claim (paraphrase/interpretation):
Candidate Signal Type:
Disqualifiers checked:
Proposed strength:
Why not Weak:
Uncertainty:
```

This applies whenever AI proposes new signals or signal updates. It is not limited to import preflight.

Before publication, the agent must additionally produce or internally complete this audit:

```text
Problem evidence:
Latest-state evidence:
Residual condition still present:
Material claim clauses and supporting fact rows:
Contradictory evidence considered:
Each stored quotation found verbatim at its exact URL:
Each fact's evidence basis and specificity checked independently:
```

If the latest evidence only reports a fix, restoration, completed remediation, or stable state, the agent must not publish a Moderate or Strong current-aftermath signal without separate evidence of recurrence, failed remediation, continuing affected users, residual backlog, or another active consequence.

## Conservative scoring rule

If AI cannot copy at least one complete source sentence verbatim into Observed Facts, or if the collected facts do not directly support the selected Signal Type and all signal claims, it must propose Weak. Multiple facts are encouraged when one fact does not support the complete analysis.

If AI cannot explain why the signal is not Weak, it must propose Weak.

If a source is useful for discovery but not direct evidence, AI must find the exact evidence source or propose Weak/context only.

## Contextual interpretation rule

AI must interpret quotations using the complete sentence and surrounding source context. Identical or similar wording in a source and a Signal Type definition is not proof that their meanings match.

Before classifying a fact, AI must identify what the relevant term refers to, who is speaking and in what relationship to the Prospect, who or what performs the action or bears the burden, whether the condition is ongoing or resolved, and what consequence the passage actually establishes. Technical processing is not human processing work. A temporary throughput loss is not an ongoing operating burden. A plan to improve reliability is not proof that the improvement work is excessive operational toil.

If a proposed signal depends on a lexical match rather than a contextual match, AI must reject that interpretation or keep the evidence Weak.

## No-overreach rule

AI must not upgrade a signal because:

- Cartertek could perform the work
- the company resembles a good prospect
- the role contains familiar keywords
- the source uses a word that appears in the Signal Type name
- the source describes technical work generally
- the source is from a promising arena

## Source of truth

Signal Type-specific criteria live in the managed SEI Signal Type definition. AI should refer to the managed definition rather than duplicating rules in prompts or docs.
