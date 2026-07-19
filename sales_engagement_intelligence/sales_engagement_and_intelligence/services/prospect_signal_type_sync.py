from __future__ import annotations

import frappe


def sync_prospect_signal_types(prospect: str | None) -> None:
    """Store queryable taxonomy snapshots derived from a prospect's Signals."""

    if not prospect or not _can_sync():
        return

    rows = frappe.db.sql(
        """
        SELECT DISTINCT s.signal_type, st.research_arena
        FROM `tabSEI Signal` s
        LEFT JOIN `tabSEI Signal Type` st ON st.name = s.signal_type
        WHERE s.prospect = %s AND COALESCE(s.signal_type, '') != ''
        ORDER BY s.signal_type, st.research_arena
        """,
        prospect,
        as_dict=True,
    )
    signal_types = list(dict.fromkeys(row.signal_type for row in rows if row.signal_type))
    arenas = list(dict.fromkeys(row.research_arena for row in rows if row.research_arena))
    frappe.db.set_value(
        "SEI Prospect",
        prospect,
        {"signals": ", ".join(signal_types), "arenas": ", ".join(arenas)},
        update_modified=False,
    )


def sync_all_prospect_signal_types() -> None:
    """Backfill every prospect's queryable taxonomy snapshots."""

    if not _can_sync():
        return

    for prospect in frappe.get_all("SEI Prospect", pluck="name"):
        sync_prospect_signal_types(prospect)


def _can_sync() -> bool:
    return (
        frappe.db.table_exists("SEI Prospect")
        and frappe.db.table_exists("SEI Signal")
        and frappe.db.table_exists("SEI Signal Type")
        and frappe.db.has_column("SEI Prospect", "signals")
        and frappe.db.has_column("SEI Prospect", "arenas")
        and frappe.db.has_column("SEI Signal", "signal_type")
        and frappe.db.has_column("SEI Signal Type", "research_arena")
    )
