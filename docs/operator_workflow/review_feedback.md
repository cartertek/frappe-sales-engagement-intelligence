# Review Feedback

Reviewer comments on downgraded or rejected signals are evaluation feedback, not merely data cleanup instructions.

## Diagnose the evaluation mistake

When a reviewer downgrades a signal, identify why:

- source did not prove the claim
- source contradicted the claim
- wrong Signal Type
- strength too high
- inferred pattern treated as observed evidence
- Cartertek fit mistaken for signal evidence
- source was a discovery source rather than evidence source
- disqualifier was missed

## Feedback loop

If the same feedback pattern appears repeatedly, update the managed Signal Type definition or SEI validation logic.

Do not solve recurring signal-quality problems only by cleaning individual records.

## Assignment handling

Assignments with comments should be handled by:

1. reading the reviewer comment
2. identifying the evaluation mistake
3. correcting the signal record if needed
4. updating the relevant managed Signal Type definition if the mistake reflects unclear criteria
5. closing the assignment only after the underlying issue is addressed

## Signal Type feedback records

When review feedback reveals a reusable false-positive pattern or unclear criterion, create a Signal Type Feedback record with:

- signal type
- source signal
- feedback summary
- false-positive pattern
- recommended definition change
- reviewer and review date
- status

Use these records to improve the managed Signal Type definitions over time.
