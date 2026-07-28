# Signal API

Methods:

- `add_signal(prospect, payload)`
- `update_signal(signal, payload)`
- `get_signals(prospect)`
- `find_duplicate_signal(prospect, payload)`

Adding or updating a signal recalculates Prospect qualification and lifecycle.

## Evidence-first validation

Moderate or Strong signals must include structured source-backed evidence:

- `observed_facts`
- `signal_claim`
- `why_this_signal_type`
- `why_not_weak`
- `disqualifiers_checked`

Observed signals require at least one `observed_facts` row. Each row contains a `fact` value with a verbatim source quotation of at least one complete sentence. One fact is the minimum; multiple facts are encouraged whenever needed to support every claim. Do not paraphrase or splice separate passages into one fact.

Use `signal_claim` for paraphrase, interpretation, or explanation of what the quoted observation supports.

Weak signals require either `observed_facts` or `evidence_gap_reason` so review can learn from weak or rejected evidence.

Inferred signals are automatically excluded from qualification. Inferred signals cannot be Strong unless `manual_override_reason` is documented.

## Payload fields

Supported signal payload fields include. `observed_facts` is a child-row list:

```text
signal_type
signal_strength
evidence_basis
evidence_specificity
confidence
source_url
source_date
observed_facts: [{"fact": "Complete verbatim source sentence."}]
signal_claim
why_this_signal_type
why_not_weak
disqualifiers_checked
evidence_gap_reason
evidence_notes
exclude_from_qualification
manual_override_reason
reviewed_by
review_date
attachment
```

## Qualification by Playbook script

Qualification first excludes inferred signals, signals marked `exclude_from_qualification`, and signals that do not satisfy their strength-specific evidence guardrails. Remaining observed signals, including Weak signals, are grouped by the Playbook assigned to their Signal Type.

Each Playbook's `signal_qualification_script` receives its group through the JavaScript global `signals`. A truthy script result means every eligible signal in that group passes the qualification test. The Prospect is qualified when at least one signal passes. Manual Prospect approval with documented reasoning remains available as an override.
