from __future__ import annotations

import frappe


def sync_prospect_signal_types(prospect: str | None) -> None:
    """Store the prospect's unique linked Signal Types as a filterable snapshot."""

    if not prospect or not _can_sync():
        return

    signal_types = frappe.get_all(
        "SEI Signal",
        filters={"prospect": prospect, "signal_type": ["is", "set"]},
        pluck="signal_type",
        order_by="signal_type asc",
    )
    value = ", ".join(dict.fromkeys(signal_types))
    playbooks = frappe.db.sql("""
        SELECT DISTINCT st.playbook
        FROM `tabSEI Signal` s
        JOIN `tabSEI Signal Type` st ON st.name=s.signal_type
        WHERE s.prospect=%s AND COALESCE(st.playbook, '') != ''
        ORDER BY st.playbook
    """, prospect, as_list=True)
    frappe.db.set_value(
        "SEI Prospect", prospect,
        {"signals": value, "playbooks": ", ".join(row[0] for row in playbooks)},
        update_modified=False,
    )


def sync_all_prospect_signal_types() -> None:
    """Backfill every prospect's Signal Type snapshot after schema migration."""

    if not _can_sync():
        return

    for prospect in frappe.get_all("SEI Prospect", pluck="name"):
        sync_prospect_signal_types(prospect)


def _can_sync() -> bool:
    return (
        frappe.db.table_exists("SEI Prospect")
        and frappe.db.table_exists("SEI Signal")
        and frappe.db.has_column("SEI Prospect", "signals")
        and frappe.db.has_column("SEI Prospect", "playbooks")
        and frappe.db.has_column("SEI Signal", "signal_type")
    )
