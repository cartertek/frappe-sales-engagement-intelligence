# Qualification

Qualification is driven by prospect context plus SEI Signal evidence. Signals include type, strength, confidence, notes, and whether the signal counts toward qualification. Each Observed Facts row carries its own evidence basis, evidence specificity, source URL, and source date.

An Observed fact is directly visible in its cited source, such as a job post, issue tracker, launch page, directory profile, or public request. An Inferred fact is a researched conclusion based on indirect evidence. A signal is eligible for automatic qualification when at least one fact is Observed and the signal is not excluded. A signal supported only by Inferred facts requires review and is excluded automatically unless manually handled.

Each playbook can define a Signals Qualification Script. Eligible observed signals are grouped by their Signal Type's playbook, and each group is evaluated by that playbook script. A truthy result qualifies every eligible signal in that group; a prospect is qualified when at least one signal passes. Assigning a playbook does not itself qualify a prospect, change lifecycle status, or create CRM records.

Manual qualification overrides require a reason. Rejected and Do Not Contact remain protected lifecycle states.

## Lifecycle disposition for unqualified prospects

Unqualified means the evidence threshold was not met. It does not by itself mean more research is needed.

- Keep the prospect in Needs Research when more investigation is still required before a disposition decision.
- Move the prospect to Rejected when research is complete and no qualifying outreach evidence exists.
- Use Research Complete when research is finished. Qualification Status distinguishes Needs Review, Qualified, and Manually Approved outcomes; completed unqualified research should move to Rejected.
