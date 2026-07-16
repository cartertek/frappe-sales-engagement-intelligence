from __future__ import annotations

import frappe

SIGNAL_TYPES = (
    "early-technical-capacity-gap",
    "overloaded-hybrid-scope",
    "consultancy-compatible-contract",
    "long-open-role",
)

REVIEW_STANDARD = """Hiring-gap review tests for Moderate or Strong signals:

1. Current-condition test
The source must identify a specific company process, vacancy, buying path, or role scope that is currently manual, blocked, brittle, delayed, failing, unresolved, or unscalable. A role responsibility, team mission, desired future state, candidate qualification, or general category of work is not enough.

2. Role-centrality test
The qualifying condition must be a central reason for the hire or engagement, not merely one responsibility, success metric, or improvement opportunity inside a broad role. When the evidence is real but peripheral, the signal is normally Moderate at most.

3. Role-type test
Non-engineering roles are presumptively Weak across all hiring-gap signal types. A non-engineering role may be Moderate or Strong only as an exceptional case where the source directly documents concrete missing or inadequate systems, substantial technical construction or integration ownership, and a material current business burden. Owner's Accounting Manager signal is the reference example: no inventory subledger, no ERP roadmap, manual integrations consuming every close cycle, and a mandate to build the missing systems.

For Moderate or Strong signals, Disqualifiers Checked must explicitly include:
Current-condition test: [pass/fail and source-backed explanation]
Role-centrality test: [pass/fail and source-backed explanation]
Role-type test: [engineering / non-engineering exception / fail, with explanation]"""


def append_once(existing: str | None) -> str:
    existing = (existing or "").strip()
    if "Hiring-gap review tests for Moderate or Strong signals:" in existing:
        return existing
    return f"{existing}\n\n{REVIEW_STANDARD}".strip()


def execute() -> None:
    for name in SIGNAL_TYPES:
        if not frappe.db.exists("SEI Signal Type", name):
            continue
        doc = frappe.get_doc("SEI Signal Type", name)
        doc.evidence_notes_requirements = append_once(doc.evidence_notes_requirements)
        doc.automatic_weak_conditions = append_once(doc.automatic_weak_conditions)
        doc.save(ignore_permissions=True)
