from __future__ import annotations

import frappe


def _migrate_table(doctype: str) -> None:
    table = f"tab{doctype}"
    if not frappe.db.table_exists(doctype):
        return
    if not frappe.db.has_column(doctype, "exclude_from_qualification"):
        return
    if not frappe.db.has_column(doctype, "counts_toward_qualification"):
        return

    frappe.db.sql(
        f"""
        UPDATE `{table}`
        SET exclude_from_qualification = CASE
            WHEN COALESCE(counts_toward_qualification, 0) = 1 THEN 0
            ELSE 1
        END
        """
    )



def execute() -> None:
    _migrate_table("SEI Signal")
