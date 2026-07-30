# Research, Draft, and Publish a Signal

Use a Draft Signal as the durable working record for each plausible research path. The draft may exist before an SEI Prospect. Create or identify the Prospect only after the path remains supported, then attach and publish the completed Signal.

Required pattern:

1. Create one Draft Signal as soon as a distinct research assertion becomes plausible. A Prospect and most Signal fields may remain blank.
2. Record discovery context and unverified propositions as draft notes or evidence gaps. Do not put search snippets, remembered propositions, or researcher-written summaries into Observed Facts.
3. Open each exact evidence URL and copy complete source sentences verbatim into Observed Facts. Populate `source_url`, `source_date`, `evidence_basis`, and `evidence_specificity` independently on every row.
4. Read the surrounding passage and find the newest relevant evidence. Record whether the condition is ongoing, temporary, resolved, contradicted, or narrowed.
5. Only after verified facts exist, derive the Signal Claim, managed Signal Type, and strength. A tentative type may guide further searching, but it must not determine how evidence is worded or which contradictory facts are discarded.
6. Check every material claim clause against specific fact rows. Remove unsupported claims about recurrence, scope, causation, teams, severity, duration, current status, human work, cost, or business impact.
7. Attempt to disprove the signal. If a material premise fails, reevaluate the whole path from zero rather than substituting adjacent rationales. Delete the draft when the path is disproven.
8. For a supported path, create or identify the Prospect, link the draft, add a descriptive name, complete structured analysis, and check all managed disqualifiers and guardrails.
9. Publish through the normal Publish action. Do not bypass validation or set status directly.
10. After save, read every stored fact, reopen every exact URL, and confirm character-for-character that the complete sentence appears there and belongs to the expected source. Also verify all row metadata, latest state, claim-clause support, type, and strength.
11. Only after that audit may the Published Signal feed qualification, lifecycle, playbook derivation, contact research, or message drafting.
12. Do not create CRM records unless the user explicitly instructs a manager action.

Do not use this workflow to send outreach or bypass protected statuses.


Each Observed Facts row stores its own `source_url`, `source_date`, `evidence_basis`, and `evidence_specificity`. At least one fact must supply any value required for the signal; multiple facts may use different sources and evidence classifications.

## Fact-level evidence metadata

`evidence_basis`, `evidence_specificity`, `source_url`, and `source_date` belong to each Observed Facts row, not to the Signal. Classify and cite each fact independently. When a rule requires one of these values, the signal satisfies the rule when at least one fact row supplies the required value. Do not copy a source classification across unrelated facts merely to satisfy validation.
