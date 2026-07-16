# Signal API

Methods:

- `add_signal(prospect, payload)`
- `update_signal(signal, payload)`
- `get_signals(prospect)`
- `find_duplicate_signal(prospect, payload)`

Adding or updating a signal recalculates Prospect qualification and lifecycle.

## Evidence-first validation

Moderate or Strong signals must include structured source-backed evidence:

- `observed_fact`
- `signal_claim`
- `why_this_signal_type`
- `why_not_weak`
- `disqualifiers_checked`

Observed signals require `observed_fact`. For Moderate or Strong signals, it must be a verbatim quotation copied from the source, contain at least one complete sentence, and directly support the selected Signal Type. Do not paraphrase or combine separate passages in this field.

Use `signal_claim` for paraphrase, interpretation, or explanation of what the quoted observation supports.

Weak signals require either `observed_fact` or `evidence_gap_reason` so review can learn from weak or rejected evidence.

Inferred signals are automatically excluded from qualification. Inferred signals cannot be Strong unless `manual_override_reason` is documented.

Signals with an applied disqualifier check are capped at Weak unless `manual_override_reason` is documented.

## Payload fields

Supported signal payload fields include:

```text
signal_type
signal_strength
evidence_basis
evidence_specificity
confidence
source_url
source_date
observed_fact
signal_claim
why_this_signal_type
why_not_weak
disqualifiers_checked
evidence_gap_reason
evidence_notes
disqualifier_checks
exclude_from_qualification
manual_override_reason
reviewed_by
review_date
attachment
```

## Qualification counting

Qualification counts only evidence-valid observed signals:

- one Strong observed signal, or
- two Moderate observed signals, or
- manual prospect approval with documented reasoning

Qualification excludes Weak signals, inferred signals, signals marked `exclude_from_qualification`, signals capped by a disqualifier without override, and signals missing required structured evidence fields.
