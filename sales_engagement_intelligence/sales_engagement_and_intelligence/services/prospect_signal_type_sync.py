from __future__ import annotations

import frappe


def sync_prospect_signal_types(prospect: str | None) -> None:
    """Store queryable taxonomy snapshots derived from a prospect's Signals."""
    if not prospect or not _can_sync():
        return
    rows = frappe.db.sql(
        """SELECT DISTINCT s.signal_type, st.playbook, st.research_arena
        FROM `tabSEI Signal` s
        LEFT JOIN `tabSEI Signal Type` st ON st.name = s.signal_type
        WHERE s.prospect = %s AND COALESCE(s.signal_type, '') != ''
        ORDER BY s.signal_type, st.playbook, st.research_arena""",
        prospect,
        as_dict=True,
    )
    values = {
        "signals": ", ".join(dict.fromkeys(r.signal_type for r in rows if r.signal_type)),
        "playbooks": ", ".join(dict.fromkeys(r.playbook for r in rows if r.playbook)),
        "arenas": ", ".join(dict.fromkeys(r.research_arena for r in rows if r.research_arena)),
    }
    current = frappe.db.get_value(
        "SEI Prospect", prospect, tuple(values), as_dict=True
    ) or {}
    if all((current.get(field) or "") == value for field, value in values.items()):
        return

    frappe.db.set_value("SEI Prospect", prospect, values, update_modified=True)
    frappe.get_doc("SEI Prospect", prospect).notify_update()


def sync_all_prospect_signal_types() -> None:
    if _can_sync():
        for prospect in frappe.get_all("SEI Prospect", pluck="name"):
            sync_prospect_signal_types(prospect)


def _can_sync() -> bool:
    return all(
        (
            frappe.db.table_exists("SEI Prospect"),
            frappe.db.table_exists("SEI Signal"),
            frappe.db.table_exists("SEI Signal Type"),
            frappe.db.has_column("SEI Prospect", "signals"),
            frappe.db.has_column("SEI Prospect", "playbooks"),
            frappe.db.has_column("SEI Prospect", "arenas"),
            frappe.db.has_column("SEI Signal", "signal_type"),
            frappe.db.has_column("SEI Signal Type", "playbook"),
            frappe.db.has_column("SEI Signal Type", "research_arena"),
        )
    )
