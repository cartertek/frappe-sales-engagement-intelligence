# AI-Assisted Research

AI can help find and organize evidence, but it must not over-promote weak evidence.

AI-assisted research follows the same evidence-first rule as manual research:

A signal is not what the source reminds us of.
A signal is what the source directly supports.

## AI research protocol

For each proposed signal, AI must separate:

- verbatim source quotation of at least one complete sentence
- interpretation or paraphrase
- candidate Signal Type
- disqualifiers checked
- strength rationale
- uncertainty

## Required AI output before creating signals

Before AI proposes a new signal or signal update, it should provide:

```text
Prospect:
Exact evidence source:
Observed fact (verbatim quotation; at least one complete sentence):
Signal claim (paraphrase/interpretation):
Candidate Signal Type:
Disqualifiers checked:
Proposed strength:
Why not Weak:
Uncertainty:
```

This applies whenever AI proposes new signals or signal updates. It is not limited to import preflight.

## Conservative scoring rule

If AI cannot copy at least one complete source sentence verbatim into Observed Fact, or if the quotation does not directly support the selected Signal Type, it must propose Weak.

If AI cannot explain why the signal is not Weak, it must propose Weak.

If a source is useful for discovery but not direct evidence, AI must find the exact evidence source or propose Weak/context only.

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
