# Signal Evaluation

Signal evaluation starts after a candidate evidence source has been found.

A signal is not what the source reminds us of.
A signal is what the source directly supports.

## Core evaluation questions

Ask these questions in order:

1. What does the source directly say or show?
2. What am I inferring?
3. Which managed Signal Type does this evidence appear to support?
4. Does the Signal Type definition say this evidence is sufficient?
5. Do any disqualifiers apply?
6. Why is this not Weak?

## Evidence note format

Use this structure when recording signal evidence:

```text
Observed fact:
[What the source directly says or shows]

Signal claim:
[What this fact is being used to support]

Why this Signal Type:
[Why the observed fact matches the selected managed Signal Type]

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

Observed means the source directly says or shows the fact.

Inferred means the evaluator believes something may be true based on pattern, context, analogy, or experience.

Inferred evidence may be useful context, but it should not be treated as equivalent to observed evidence.

## Signal Type criteria

Signal Type-specific criteria, disqualifiers, automatic Weak conditions, and strength guidance live in the managed SEI Signal Type definition. Do not duplicate those rules into separate operator docs.
