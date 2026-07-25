# Qualification

Qualification is driven by prospect context plus SEI Signal evidence. Signals include type, strength, evidence basis, confidence, source URL, source date, notes, and whether the signal counts toward qualification.

Observed evidence is directly visible in a source such as a job post, issue tracker, launch page, directory profile, or public request. Inferred evidence is a researched conclusion based on indirect evidence. Inferred qualifying evidence requires extra review and should be used carefully.

Each playbook can define a Signals Qualification Script. Eligible observed signals are grouped by their Signal Type's playbook, and each group is evaluated by that playbook script. A truthy result qualifies every eligible signal in that group; a prospect is qualified when at least one signal passes. Assigning a playbook does not itself qualify a prospect, change lifecycle status, or create CRM records.

Manual qualification overrides require a reason. Rejected and Do Not Contact remain protected lifecycle states.

## Lifecycle disposition for unqualified prospects

Unqualified means the evidence threshold was not met. It does not by itself mean more research is needed.

- Keep the prospect in Needs Research when more investigation is still required before a disposition decision.
- Move the prospect to Rejected when research is complete and no qualifying outreach evidence exists.
- Use Research Complete for Needs Review prospects that have enough evidence for a human review decision, not for researched prospects that are already known to be unqualified.
