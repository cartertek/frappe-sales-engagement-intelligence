from __future__ import annotations

import frappe

from sales_engagement_intelligence.patches.v0_0_1.seed_signal_types import SIGNAL_TYPES

EVIDENCE_FIELDS = (
    "evidence_summary",
    "qualifying_evidence",
    "insufficient_evidence",
    "automatic_weak_conditions",
    "disqualifying_conditions",
    "weak_guidance",
    "moderate_guidance",
    "strong_guidance",
    "evidence_notes_requirements",
    "false_positive_examples",
    "positive_examples",
)


def execute() -> None:
    for row in SIGNAL_TYPES:
        signal_type = row.get("signal_type_name")
        if not signal_type or not frappe.db.exists("SEI Signal Type", signal_type):
            continue
        doc = frappe.get_doc("SEI Signal Type", signal_type)
        changed = False
        for fieldname in EVIDENCE_FIELDS:
            if row.get(fieldname) and not doc.get(fieldname):
                doc.set(fieldname, row[fieldname])
                changed = True
        if changed:
            doc.save(ignore_permissions=True)
