# ruff: noqa: E501
from __future__ import annotations

import frappe

PLAYBOOKS = [
    {
        "playbook_name": "Agency Overflow",
        "description": "Agencies or adjacent delivery teams that appear to need technical reinforcement, implementation depth, or overflow support.",
        "thesis": "Agency Technical Reinforcement",
        "default_offer": "White-label engineering support / technical rescue call",
        "typical_prospect_types": "Agency, Ecosystem Partner, Referral Partner",
        "legacy_source_arenas": "Agency directories, partner ecosystems, referral networks, service-provider communities",
        "legacy_contact_roles": "Founder, Operations Lead, Delivery Lead, Account Lead",
        "qualifying_signal_guidance": "Agency overflow, AI/custom software positioning, odd technical hiring, backend/integration claims without visible depth.",
        "disqualifying_guidance": "Disqualify agencies that clearly have deep internal engineering capacity, only sell media/creative services, or appear to need low-cost staffing rather than senior implementation support.",
        "recommended_first_action": "Review service positioning and identify the likely delivery gap before drafting.",
        "follow_up_guidance": "Follow up around a specific client-delivery bottleneck or technical backup use case; do not imply the agency is failing.",
        "rules": [
            ("Agency Overflow", "Moderate", "Observed"),
            ("Ecosystem Adjacency", "Moderate", "Observed"),
        ],
    },
    {
        "playbook_name": "Failed Hiring",
        "description": "Teams whose hiring pattern suggests an unresolved engineering capacity or implementation gap.",
        "thesis": "Hiring-Gap Substitution",
        "default_offer": "Scoped diagnostic / focused implementation sprint",
        "typical_prospect_types": "Startup, SMB, Enterprise",
        "legacy_source_arenas": "Job boards, company career pages, community hiring posts, role reposts",
        "legacy_contact_roles": "CTO, VP Engineering, Engineering Manager, Founder, Operator, Product Lead",
        "qualifying_signal_guidance": "Long-open role, repeated reposts, urgent contractor role, impossible hybrid role, modernization/AI/integration hiring.",
        "disqualifying_guidance": "Disqualify normal healthy hiring, broad evergreen roles, staffing-agency posts, and prospects where the role does not map to Cartertek delivery work.",
        "recommended_first_action": "Compare the role requirements to visible product or workflow needs.",
        "follow_up_guidance": "Position the offer as progress while hiring continues, not as replacement recruiting or staff augmentation.",
        "rules": [("Failed Recruitment", "Moderate", "Observed")],
    },
    {
        "playbook_name": "Launch Aftermath",
        "description": "Recently launched products or initiatives that show stabilization, integration, reliability, or cleanup needs.",
        "thesis": "Post-Launch Stabilization",
        "default_offer": "Production-readiness review / bug and integration cleanup",
        "typical_prospect_types": "Startup, SMB, Enterprise",
        "legacy_source_arenas": "Launch posts, Product Hunt, release notes, support forums, social announcements",
        "legacy_contact_roles": "Founder, CTO, Product Lead, Technical Lead",
        "qualifying_signal_guidance": "Recent launch, visible bugs, support complaints, performance issues, integration requests.",
        "disqualifying_guidance": "Disqualify launches with no visible technical friction, purely marketing launches, or issues unrelated to software delivery.",
        "recommended_first_action": "Capture the launch context and one concrete stabilization angle.",
        "follow_up_guidance": "Follow up with a pragmatic cleanup/readiness framing tied to the launch date or issue pattern.",
        "rules": [("Launch Aftermath", "Moderate", "Observed")],
    },
    {
        "playbook_name": "Technical Distress",
        "description": "Prospects showing public or research-backed evidence of stalled, fragile, abandoned, or broken technical work.",
        "thesis": "Project Rescue",
        "default_offer": "Technical diagnostic / stabilization sprint",
        "typical_prospect_types": "Startup, SMB, Enterprise, Community Lead, Directory Lead",
        "legacy_source_arenas": "GitHub, public forums, issue trackers, communities, product feedback surfaces",
        "legacy_contact_roles": "CTO, Technical Lead, Founder, Operations Lead, Product Owner",
        "qualifying_signal_guidance": "GitHub issues, public complaints, integration failures, abandoned tooling, migration problems, AI prototype failure.",
        "disqualifying_guidance": "Disqualify unsupported open-source hobby projects, stale issues with no commercial owner, and problems outside Cartertek's delivery scope.",
        "recommended_first_action": "Summarize the technical distress evidence and the likely business impact.",
        "follow_up_guidance": "Offer a diagnostic or stabilization sprint; avoid exaggerating or shaming the current implementation.",
        "rules": [("Technical Distress", "Moderate", "Observed")],
    },
    {
        "playbook_name": "Partner / Referral",
        "description": "Adjacent providers who can refer or partner on implementation-heavy software, AI, workflow, or integration work.",
        "thesis": "Agency Technical Reinforcement",
        "default_offer": "Referral partnership / technical backup / implementation partner relationship",
        "typical_prospect_types": "Agency, Ecosystem Partner, Referral Partner",
        "legacy_source_arenas": "Partner directories, consultant networks, local business networks, adjacent service ecosystems",
        "legacy_contact_roles": "Agency Owner, Designer, MSP Owner, Fractional CTO, Consultant, Advisor",
        "qualifying_signal_guidance": "Adjacent service provider, lacks custom software capability, clients asking for AI/automation/workflows/integrations.",
        "disqualifying_guidance": "Disqualify direct competitors with overlapping delivery capability, referral partners serving unrelated buyers, and purely transactional lead sellers.",
        "recommended_first_action": "Identify the partner's client base and where Cartertek complements their offer.",
        "follow_up_guidance": "Follow up around mutual-fit referral mechanics and technical backup, not a generic vendor pitch.",
        "rules": [("Credibility/Referral Signal", "Moderate", "Observed"), ("Ecosystem Adjacency", "Moderate", "Observed")],
    },
    {
        "playbook_name": "Reactivation",
        "description": "Previously reviewed or contacted prospects where a new signal or expired not-now window creates a reason to revisit.",
        "thesis": "Technical Diagnostic / Second Set of Eyes",
        "default_offer": "Depends on current signal",
        "typical_prospect_types": "Agency, Startup, SMB, Enterprise, Ecosystem Partner, Directory Lead, Community Lead, Procurement Lead, Referral Partner, Other",
        "legacy_source_arenas": "Prior SEI records, CRM history, renewed public signals, follow-up windows",
        "legacy_contact_roles": "Primary Contact, Owner, Founder, CTO, Operations Lead",
        "qualifying_signal_guidance": "New launch, role remains open, second signal appears, prior not-now window expires, new initiative, prospect changes role/company.",
        "disqualifying_guidance": "Do not reactivate Do Not Contact prospects. Avoid reactivation without a fresh signal, new owner, or elapsed not-now window.",
        "recommended_first_action": "Review prior notes and verify the new signal before drafting.",
        "follow_up_guidance": "Reference the current signal or timing change; do not pretend the prior context does not exist.",
        "rules": [("Reactivation Signal", "Moderate", "Observed")],
    },
]

TEMPLATES = [
    {
        "template_name": "Agency Overflow - Email - Technical Backup",
        "playbook": "Agency Overflow",
        "channel": "Email",
        "prospect_type": "Agency",
        "contact_role": "Founder",
        "subject_template": "Technical backup for {{ prospect_name }}",
        "body_template": "Hi {{ primary_contact_name }},\n\nI noticed {{ signal_summary }}. Cartertek helps agencies add senior engineering support for custom software, integrations, AI workflows, and rescue work without forcing a staffing model.\n\nIf useful, I can take a quick look at where {{ prospect_name }} might need technical backup and suggest a scoped way to de-risk delivery.\n\nBest,\nJoshua",
        "notes": "Manual review required. Replace any blank or awkward variables before sending.",
    },
    {
        "template_name": "Failed Hiring - Email - Implementation Sprint",
        "playbook": "Failed Hiring",
        "channel": "Email",
        "contact_role": "CTO",
        "subject_template": "Progress while {{ prospect_name }} is hiring",
        "body_template": "Hi {{ primary_contact_name }},\n\nI saw {{ signal_summary }}. When teams have a role open for a while, the urgent work often keeps piling up before the hire is in place.\n\nCartertek can help with a scoped diagnostic or implementation sprint around {{ offer }} so the project keeps moving while hiring continues.\n\nBest,\nJoshua",
        "notes": "Use only when the hiring signal is specific and current.",
    },
    {
        "template_name": "Launch Aftermath - Email - Stabilization Review",
        "playbook": "Launch Aftermath",
        "channel": "Email",
        "contact_role": "Founder",
        "subject_template": "Post-launch cleanup for {{ prospect_name }}",
        "body_template": "Hi {{ primary_contact_name }},\n\nCongrats on the recent launch. I noticed {{ signal_summary }}, which is the kind of post-launch friction Cartertek helps clean up.\n\nWe can review reliability, integrations, and workflow gaps, then turn that into a focused stabilization sprint.\n\nBest,\nJoshua",
        "notes": "Keep the tone respectful; do not overstate observed issues.",
    },
    {
        "template_name": "Technical Distress - Email - Diagnostic",
        "playbook": "Technical Distress",
        "channel": "Email",
        "contact_role": "Founder",
        "subject_template": "A second set of eyes on {{ prospect_name }}",
        "body_template": "Hi {{ primary_contact_name }},\n\nI came across {{ signal_summary }}. Cartertek helps teams stabilize stalled or fragile software projects and turn the next step into something concrete.\n\nA small diagnostic could clarify what is broken, what is worth preserving, and what a focused stabilization sprint would look like.\n\nBest,\nJoshua",
        "notes": "Use evidence carefully; avoid accusatory language.",
    },
    {
        "template_name": "Partner Referral - Email - Technical Partner",
        "playbook": "Partner / Referral",
        "channel": "Email",
        "contact_role": "Agency Owner",
        "subject_template": "Technical implementation partner for {{ prospect_name }}",
        "body_template": "Hi {{ primary_contact_name }},\n\nI noticed {{ signal_summary }}. Cartertek partners with adjacent service providers when their clients need custom software, workflow automation, integrations, AI implementation, or project rescue support.\n\nIf that comes up for your clients, I would be glad to compare notes and see whether there is a useful referral fit.\n\nBest,\nJoshua",
        "notes": "Partner/referral framing only; not a direct prospect pain pitch.",
    },
    {
        "template_name": "Reactivation - Email - Current Signal",
        "playbook": "Reactivation",
        "channel": "Email",
        "contact_role": "Primary Contact",
        "subject_template": "Following up on {{ prospect_name }}",
        "body_template": "Hi {{ primary_contact_name }},\n\nI wanted to follow up because {{ signal_summary }}. Based on that current context, {{ offer }} may be a useful next step.\n\nCartertek can help evaluate the project or workflow and turn the next step into a scoped implementation plan.\n\nBest,\nJoshua",
        "notes": "Verify prior outreach history and Do Not Contact status before use.",
    },
]


def execute() -> None:
    seed_playbooks()
    seed_message_templates()


def _ensure_role(role: str) -> None:
    if role and not frappe.db.exists("SEI Contact Role", role):
        frappe.get_doc({"doctype":"SEI Contact Role","role_name":role,"active":1}).insert(ignore_permissions=True)


def seed_playbooks() -> None:
    for row in PLAYBOOKS:
        rules = row["rules"]
        roles = [value.strip() for value in row.get("legacy_contact_roles", "").split(",") if value.strip()]
        values = {key: value for key, value in row.items() if key not in ("rules", "legacy_contact_roles", "legacy_source_arenas")}
        values["active"] = 1
        doc = frappe.get_doc("SEI Playbook", values["playbook_name"]) if frappe.db.exists("SEI Playbook", values["playbook_name"]) else frappe.get_doc({"doctype":"SEI Playbook"})
        doc.update(values)
        doc.set("signal_rules", [])
        for signal_type, minimum_strength, evidence_basis_required in rules:
            doc.append("signal_rules", {"signal_type":signal_type,"minimum_strength":minimum_strength,"evidence_basis_required":evidence_basis_required,"exclude_from_qualification":0})
        doc.set("contact_roles", [])
        for role in roles:
            _ensure_role(role)
            doc.append("contact_roles", {"contact_role":role})
        doc.save(ignore_permissions=True) if doc.name else doc.insert(ignore_permissions=True)


def seed_message_templates() -> None:
    for row in TEMPLATES:
        values = {**row, "active": 1}
        if values.get("playbook") and not frappe.db.exists("SEI Playbook", values["playbook"]):
            continue
        _ensure_role(values.get("contact_role"))
        if frappe.db.exists("SEI Message Template", values["template_name"]):
            doc = frappe.get_doc("SEI Message Template", values["template_name"])
            doc.update(values)
            doc.save(ignore_permissions=True)
        else:
            frappe.get_doc({"doctype": "SEI Message Template", **values}).insert(ignore_permissions=True)
