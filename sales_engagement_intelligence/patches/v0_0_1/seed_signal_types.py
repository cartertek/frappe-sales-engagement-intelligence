from __future__ import annotations

import frappe

SIGNAL_TYPES = [
    {
        "signal_type_name": "Failed Recruitment",
        "description": "Visible hiring gap, long-open role, urgent contractor need, or repeated reposting.",
        "thesis": "Hiring-Gap Substitution",
    },
    {
        "signal_type_name": "Technical Distress",
        "description": "Observable broken, fragile, stalled, or unsupported technical work.",
        "thesis": "Project Rescue",
    },
    {
        "signal_type_name": "Launch Aftermath",
        "description": "Recent launch followed by visible stabilization, reliability, bug, or integration pressure.",
        "thesis": "Post-Launch Stabilization",
    },
    {
        "signal_type_name": "Agency Overflow",
        "description": "Agency or delivery team appears to need senior implementation backup or overflow support.",
        "thesis": "Agency Technical Reinforcement",
    },
    {
        "signal_type_name": "Ecosystem Adjacency",
        "description": "Adjacent provider, partner, or intermediary likely to encounter clients needing engineering support.",
        "thesis": "Agency Technical Reinforcement",
    },
    {
        "signal_type_name": "Vendor/Directory Presence",
        "description": "Directory or marketplace visibility creates an explainable source context for outreach.",
        "thesis": "Technical Diagnostic / Second Set of Eyes",
    },
    {
        "signal_type_name": "Community Request",
        "description": "Public request for help, advice, rescue, implementation, automation, or technical troubleshooting.",
        "thesis": "Project Rescue",
    },
    {
        "signal_type_name": "Procurement Visibility",
        "description": "Public buying, RFP, vendor research, or procurement evidence around software/workflow needs.",
        "thesis": "Workflow Integration",
    },
    {
        "signal_type_name": "Credibility/Referral Signal",
        "description": "Referral, partner, reputation, or credibility evidence that supports warmer outreach.",
        "thesis": "Agency Technical Reinforcement",
    },
    {
        "signal_type_name": "Reactivation Signal",
        "description": "Fresh timing signal that makes a prior prospect worth revisiting.",
        "thesis": "Technical Diagnostic / Second Set of Eyes",
    },
    {
        "signal_type_name": "Other",
        "description": "Fallback signal type for reviewed evidence that does not fit the default taxonomy.",
        "thesis": "Technical Diagnostic / Second Set of Eyes",
    },
]


def execute() -> None:
    for row in SIGNAL_TYPES:
        thesis = row.get("thesis")
        if thesis and not frappe.db.exists("SEI Thesis", thesis):
            continue
        if frappe.db.exists("SEI Signal Type", row["signal_type_name"]):
            doc = frappe.get_doc("SEI Signal Type", row["signal_type_name"])
            doc.update(row)
            doc.save(ignore_permissions=True)
        else:
            frappe.get_doc({"doctype": "SEI Signal Type", **row}).insert(ignore_permissions=True)
