# ruff: noqa: E501, I001
from __future__ import annotations

import frappe

COMMON_EVIDENCE_NOTES_REQUIREMENTS = """Evidence notes must identify:
- the exact observed fact
- why that fact supports this Signal Type
- which false positives were ruled out
- why the signal is not Weak when strength is Moderate or Strong"""

COMMON_WEAK_GUIDANCE = "Evidence is relevant context, but the source does not directly prove this Signal Type."
COMMON_MODERATE_GUIDANCE = (
    "Source directly supports this Signal Type, but timing, severity, buyer path, or completeness "
    "still needs review."
)
COMMON_STRONG_GUIDANCE = (
    "Source directly, specifically, and timely supports this Signal Type with clear business relevance."
)

DEFAULT_AUTOMATIC_WEAK_CONDITIONS = """Source is a search result rather than a specific evidence item.
Evidence relies on inferred fit rather than an observed fact.
Evidence is stale or timing cannot be determined.
Evidence source is an aggregator when a primary source should be available."""

SIGNAL_TYPES = [
    {
        "signal_type_name": "Failed Recruitment",
        "description": "Visible hiring gap, long-open role, urgent contractor need, or repeated reposting.",
        "evidence_summary": 'A visible hiring-friction signal where a technical role appears unresolved, repeatedly promoted, unusually urgent, or positioned as a gap Cartertek could cover with a scoped alternative.',
        "qualifying_evidence": 'The source directly shows a relevant technical role or contractor need that is unresolved over time, urgent, repeatedly reposted, or unusually broad for one hire.',
        "insufficient_evidence": 'A single normal job post, undated search result, ordinary engineering hiring, or specialized role is not enough to prove hiring friction.',
        "disqualifying_conditions": 'Role is clearly new and ordinary\nRole is unrelated to Cartertek services\nNo evidence of persistence, urgency, or unusual scope\nRecruiter-only listing without buyer context',
        "false_positive_examples": 'A normal senior engineer job post with no evidence of urgency, repeated posting, or hybrid overload.',
        "positive_examples": 'The same integration-heavy engineering role is still open after repeated reposting and the company is also asking for contractor help.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Failed Hiring",
    },
    {
        "signal_type_name": "Technical Distress",
        "description": "Observable broken, fragile, stalled, or unsupported technical work.",
        "evidence_summary": 'Observable broken, fragile, stalled, or unsupported technical work that suggests a real technical problem rather than broad fit.',
        "qualifying_evidence": 'The source directly shows a failure, bug, outage, abandoned implementation, unresolved issue, integration problem, migration blockage, or explicit request for troubleshooting help.',
        "insufficient_evidence": 'General technical work, technology keywords, normal product development, or a company using software does not prove distress.',
        "disqualifying_conditions": 'No actual technical problem identified\nOnly mentions normal feature work\nOnly inferred from stack or industry\nSource contradicts existence of a problem',
        "false_positive_examples": 'A GitHub repository with open issues that are normal enhancement requests, not visible distress.',
        "positive_examples": 'A public issue or customer post says a key integration is broken and blocking operations.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Technical Distress",
    },
    {
        "signal_type_name": "Launch Aftermath",
        "description": (
            "Recent launch followed by visible stabilization, reliability, bug, "
            "or integration pressure."
        ),
        "evidence_summary": 'A recent launch followed by visible stabilization, reliability, bug, integration, support, or scale pressure.',
        "qualifying_evidence": 'The source directly ties a recent launch to post-launch complaints, bug reports, reliability problems, integration requests, support backlog, or scale pressure.',
        "insufficient_evidence": 'A launch announcement alone is not enough. Generic excitement, product-market fit language, or normal launch marketing does not prove aftermath pressure.',
        "disqualifying_conditions": 'Launch is not recent\nNo post-launch issue or pressure is visible\nOnly marketing announcement\nProblem is unrelated to software delivery',
        "false_positive_examples": 'A polished product-launch post with no evidence of instability, support pressure, or follow-up work.',
        "positive_examples": 'A launch announcement is followed by support complaints about performance and missing integrations.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Launch Aftermath",
    },
    {
        "signal_type_name": "Agency Overflow",
        "description": (
            "Agency or delivery team appears to need senior implementation backup "
            "or overflow support."
        ),
        "evidence_summary": 'An agency or delivery team shows visible evidence that it may need senior implementation backup, subcontracting, or technical reinforcement.',
        "qualifying_evidence": 'The source directly shows the agency selling or requesting technical delivery beyond visible capacity, seeking subcontractors, posting overloaded hybrid roles, or publicly asking for implementation backup.',
        "insufficient_evidence": 'An agency offering technical services is not enough. Broad service claims, AI buzzwords, or agency size alone do not prove overflow.',
        "disqualifying_conditions": 'Only normal agency positioning\nNo delivery pressure or capacity gap\nEvidence points to hiring employees only\nNo vendor/subcontractor openness',
        "false_positive_examples": 'A design agency lists web development as a service but shows no capacity pressure or partner need.',
        "positive_examples": 'An agency asks for a subcontracted engineering partner to rescue or deliver a client integration project.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Agency Overflow",
    },
    {
        "signal_type_name": "Ecosystem Adjacency",
        "description": (
            "Adjacent provider, partner, or intermediary likely to encounter clients "
            "needing engineering support."
        ),
        "evidence_summary": 'A partner, intermediary, or adjacent provider visibly encounters clients with software, workflow, AI, integration, or implementation needs.',
        "qualifying_evidence": 'The source directly shows the organization serves clients adjacent to Cartertek problems and has a plausible referral, partner, or implementation path.',
        "insufficient_evidence": 'Being in a vaguely related market or serving businesses is not enough without visible adjacency to relevant client problems.',
        "disqualifying_conditions": 'No client problem adjacency\nOnly broad business services\nNo plausible referral or implementation path\nConsumer-only audience',
        "false_positive_examples": 'A generic consultant profile with no evidence of client implementation, workflow, software, or technical delivery needs.',
        "positive_examples": 'A fractional CTO advisor publicly helps nontechnical founders scope AI workflow projects but does not provide implementation.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Agency Overflow",
    },
    {
        "signal_type_name": "Vendor/Directory Presence",
        "description": (
            "Directory or marketplace visibility creates an explainable source "
            "context for outreach."
        ),
        "evidence_summary": 'Directory, marketplace, or vendor visibility that creates explainable outreach context and may support a diagnostic or second-set-of-eyes thesis.',
        "qualifying_evidence": 'The source directly places the prospect in a relevant vendor, implementation, agency, or technology-services context with enough specificity to justify outreach context.',
        "insufficient_evidence": 'A generic listing, scraped directory row, or broad category membership is usually weak unless the Signal Type criteria explain why it matters.',
        "disqualifying_conditions": 'Listing is stale or unverifiable\nCategory is too broad\nNo service/context relevance\nDirectory only duplicates company homepage with no useful evidence',
        "false_positive_examples": 'A search result snippet from a directory that does not open to a specific relevant profile.',
        "positive_examples": 'A current marketplace profile states the company provides implementation services adjacent to Cartertek support offers.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Technical Distress",
    },
    {
        "signal_type_name": "Community Request",
        "description": (
            "Public request for help, advice, rescue, implementation, automation, "
            "or technical troubleshooting."
        ),
        "evidence_summary": 'A public request for help, advice, rescue, implementation, automation, or technical troubleshooting.',
        "qualifying_evidence": 'The source directly shows a person or company asking for help with a relevant software, workflow, AI, integration, rescue, or troubleshooting problem.',
        "insufficient_evidence": 'General discussion, educational questions, or technology curiosity is not enough without an actionable request or problem.',
        "disqualifying_conditions": 'Question is purely educational\nNo buyer/prospect identity\nProblem is solved in thread\nRequest is for free advice only with no outreach path',
        "false_positive_examples": 'A Reddit comment asking what tool to learn, with no business problem or buyer path.',
        "positive_examples": 'A founder asks for help finding someone to fix a failed automation or integration project.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Technical Distress",
    },
    {
        "signal_type_name": "Procurement Visibility",
        "description": (
            "Public buying, RFP, vendor research, or procurement evidence around "
            "software/workflow needs."
        ),
        "evidence_summary": 'Public buying, RFP, vendor research, or procurement evidence around software, workflow, automation, AI, or integration needs.',
        "qualifying_evidence": 'The source directly shows the prospect researching, requesting, purchasing, or evaluating outside help for relevant technical or workflow work.',
        "insufficient_evidence": 'Generic vendor pages, broad procurement portals, or old RFPs are not enough without a current relevant buying signal.',
        "disqualifying_conditions": 'RFP is expired\nNeed is outside Cartertek scope\nOnly general vendor registration\nNo current buying or evaluation activity',
        "false_positive_examples": 'An old procurement archive that mentions software but has no current opportunity or buyer need.',
        "positive_examples": 'A current RFP requests an implementation partner for workflow automation and system integration.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Technical Distress",
    },
    {
        "signal_type_name": "Credibility/Referral Signal",
        "description": (
            "Referral, partner, reputation, or credibility evidence that supports "
            "warmer outreach."
        ),
        "evidence_summary": 'Referral, partner, reputation, or credibility evidence that supports warmer outreach or a trusted path to contact.',
        "qualifying_evidence": 'The source directly shows a shared relationship, referral context, partner mention, prior collaboration, public endorsement, or credible warm-path reason.',
        "insufficient_evidence": 'A mutual industry, vague social proximity, or similar audience is not enough without a concrete credibility or referral path.',
        "disqualifying_conditions": 'No actual warm-path evidence\nOnly same industry or geography\nRelationship is too stale\nSource indicates no-contact or bad fit',
        "false_positive_examples": 'Both companies appear in the same directory category, but there is no relationship or referral context.',
        "positive_examples": 'A partner publicly recommends the prospect or is visibly connected to Cartertek through a relevant project context.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Agency Overflow",
    },
    {
        "signal_type_name": "Reactivation Signal",
        "description": "Fresh timing signal that makes a prior prospect worth revisiting.",
        "evidence_summary": 'Fresh timing evidence that makes a prior prospect worth revisiting.',
        "qualifying_evidence": 'The source directly shows a new or changed circumstance since prior evaluation, such as a new launch, persistent role, new technical initiative, second relevant signal, or contact change.',
        "insufficient_evidence": 'Simply being a prior prospect or old fit is not enough. The source must show new timing evidence.',
        "disqualifying_conditions": 'No new evidence since prior review\nPrior Do Not Contact status\nOld signal repeated without change\nNew event is unrelated to original thesis or Cartertek scope',
        "false_positive_examples": 'Revisiting a company only because it was in an old list, with no fresh source-backed reason.',
        "positive_examples": 'A prior not-now prospect launches a new AI workflow initiative six months later.',
        "automatic_weak_conditions": DEFAULT_AUTOMATIC_WEAK_CONDITIONS,
        "weak_guidance": COMMON_WEAK_GUIDANCE,
        "moderate_guidance": COMMON_MODERATE_GUIDANCE,
        "strong_guidance": COMMON_STRONG_GUIDANCE,
        "evidence_notes_requirements": COMMON_EVIDENCE_NOTES_REQUIREMENTS,
        "playbook": "Technical Distress",
    },
]


def execute() -> None:
    for row in SIGNAL_TYPES:
        playbook = row.get("playbook")
        if playbook and not frappe.db.exists("SEI Playbook", playbook):
            continue
        if frappe.db.exists("SEI Signal Type", row["signal_type_name"]):
            doc = frappe.get_doc("SEI Signal Type", row["signal_type_name"])
            doc.update(row)
            doc.save(ignore_permissions=True)
        else:
            frappe.get_doc({"doctype": "SEI Signal Type", **row}).insert(ignore_permissions=True)

    remove_deprecated_signal_type("Other")


def remove_deprecated_signal_type(signal_type: str) -> None:
    if not frappe.db.exists("SEI Signal Type", signal_type):
        return

    linked_signal = frappe.db.exists("SEI Signal", {"signal_type": signal_type})
    linked_rule = frappe.db.exists("SEI Playbook Signal Rule", {"signal_type": signal_type})
    if linked_signal or linked_rule:
        return

    frappe.delete_doc("SEI Signal Type", signal_type, ignore_permissions=True, force=True)
