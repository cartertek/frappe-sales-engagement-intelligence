from __future__ import annotations

import frappe


def execute() -> None:
    """Rebuild the native Playbook Signal Types child table from Signal Type assignments."""
    frappe.db.delete("SEI Playbook Signal Type")
    rows = frappe.get_all(
        "SEI Signal Type",
        filters={"playbook": ["is", "set"]},
        fields=["name", "playbook", "category", "research_arena", "active"],
        order_by="playbook asc, signal_type_name asc",
    )
    for row in rows:
        frappe.get_doc(
            {
                "doctype": "SEI Playbook Signal Type",
                "parent": row.playbook,
                "parenttype": "SEI Playbook",
                "parentfield": "signal_types",
                "signal_type": row.name,
                "category": row.category,
                "research_arena": row.research_arena,
                "active": row.active,
            }
        ).insert(ignore_permissions=True)
