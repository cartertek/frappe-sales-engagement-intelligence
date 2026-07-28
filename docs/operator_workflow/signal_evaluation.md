# Signal Evaluation

Signal evaluation starts after a candidate evidence source has been found.

A signal is not what the source reminds us of.
A signal is what the source directly supports.

## Core evaluation questions

Ask these questions in order:

1. What complete source sentence can be quoted verbatim?
2. What am I inferring?
3. Which managed Signal Type does this evidence appear to support?
4. Does the Signal Type definition say this evidence is sufficient?
5. Do any disqualifiers apply?
6. Why is this not Weak?

## Qualification independence from contact strategy and actionability

Signal qualification must be based on the evidence and the managed Signal Type / Playbook criteria. Contact strategy, ease of reaching a buyer, procurement friction, budget assumptions, vendor accessibility, and general commercial actionability must not increase or decrease signal strength.

Do not downgrade a real signal because the best contact is unclear, the organization is large, procurement may be complex, or outside-vendor engagement is uncertain. Those are later outreach and contact-research questions. Likewise, do not upgrade a weak signal because the organization appears well funded or commercially attractive.

The operator must keep these decisions separate:

1. Signal qualification: what does the evidence prove, and how strong is the observed need under the managed rules?
2. Contact strategy: who is organizationally closest to the problem and senior enough to act?
3. Commercial actionability: whether Cartertek can realistically pursue the opportunity.

Only the first belongs in signal strength.

## Signal name

When creating a signal, give it a short descriptive name that identifies the specific observed event, condition, or evidence. The name should distinguish the signal from other signals on the same prospect without repeating only the Signal Type. Prefer a concise phrase such as `Backend role reposted for four months` or `Post-launch checkout failures reported`.

Do not use the generated SEI record ID, the prospect name alone, or the Signal Type alone as the descriptive name.

## Assistant-created signal default

Assistant-created signals default to Weak and excluded from qualification unless `observed_facts` contains at least one direct quotation copied verbatim from the source. Each fact must contain at least one complete sentence and directly support the selected managed Signal Type. One fact is the minimum; add multiple facts whenever the signal has multiple claims or one quotation does not support the complete analysis.

Each Observed Facts row should contain one coherent verbatim fact. Do not paraphrase, synthesize, interpret, or splice separate source passages into one row. Preserve original wording and sentence boundaries. Add additional rows for additional supporting facts. Multiple facts are encouraged when needed to support every claim. Any paraphrase or explanation of what the quotation means belongs in `signal_claim`, `why_this_signal_type`, `why_not_weak`, or `evidence_notes`.

Do not create a Moderate or Strong assistant-created signal from company context, a job title, technical work area, company scale, hiring activity, Cartertek fit, or a plausible interpretation. The analysis fields may explain the quotation, but they must not supply a signal assertion missing from the quoted source text.

Use this test before creating or strengthening a signal:

> If the selected Signal Type were hidden, would the Observed Facts still plainly describe that exact kind of signal and support every claim?

If the answer is no, create only a Weak, excluded signal or reject the candidate.

## Signal Type assertion examples

These examples do not replace the managed Signal Type definitions. They define the minimum assertion that must appear across the verbatim quotations stored in `observed_facts` before an assistant-created signal can count.

| Signal Type | Observed Facts must assert | Invalid Observed Facts pattern |
|---|---|---|
| `early-technical-capacity-gap` | A concrete technical capacity gap: the operational/business process and the actual constraint on that process. | Company scale, automation hiring, integration work, AI/workflow/internal-tools work, or desire to improve onboarding/customer experience. |
| `consultancy-compatible-contract` | Buyer openness to a firm, vendor, consultancy, agency, implementation partner, subcontractor, or company-to-company delivery path. | Contract role, bounded project, implementation task, contractor request, or work that merely seems suitable for Cartertek. |
| `long-open-role` | The same or substantially similar role has persisted over time through dated reposts, repeated promotion, explicit still-hiring language, or history/archive evidence. | Single job post, stale-looking listing, specialized role, search result, or job-board listing alone. |
| `overloaded-hybrid-scope` | One role owns engineering work plus a separate non-engineering function. | Customer-facing engineering, cross-functional collaboration, requirements gathering, implementation engineering, FDE, solutions engineering, or broad technical scope. |

## Evidence note format

Use this structure when recording signal evidence:

```text
Observed fact:
[Verbatim quotation from the source; at least one complete sentence; no paraphrasing]

Signal claim:
[Paraphrase or interpretation of what the quotation supports]

Why this Signal Type:
[Why the observed facts match the selected managed Signal Type and support all claims]

Disqualifiers checked:
[Relevant disqualifiers from the managed Signal Type definition]

Strength rationale:
[Why this is Weak, Moderate, or Strong]
```

SEI also stores these as structured fields on the signal. For Moderate or Strong signals, do not leave the logic only in legacy Evidence Notes.

## Strength standard

Weak means the source may be relevant context, but it does not directly prove the selected Signal Type.

Moderate means the source directly supports the selected Signal Type, but severity, timing, buyer path, or completeness needs review.

Strong means the source directly and specifically proves the selected Signal Type and shows a timely reason the prospect may care.

When in doubt, mark Weak.

## Why Not Weak rule

Any Moderate or Strong signal must be able to answer: why is this not Weak?

The answer must come from the source and the managed Signal Type definition, not from Cartertek fit or evaluator intuition.

## Cartertek fit is not evidence

A source can describe work Cartertek could do without proving a signal.

Signal evaluation asks: what does this source prove?

It does not ask: could Cartertek help with this?

## Observed vs inferred

Observed means `observed_facts` contains one or more rows with the source's exact wording as verbatim quotations of at least one complete sentence each. Interpretation remains separate in `signal_claim` and the other analysis fields.

Inferred means the evaluator believes something may be true based on pattern, context, analogy, or experience.

Inferred evidence may be useful context, but it should not be treated as equivalent to observed evidence.

## Signal Type criteria

Signal Type-specific criteria, disqualifiers, automatic Weak conditions, and strength guidance live in the managed SEI Signal Type definition. Do not duplicate those rules into separate operator docs.
