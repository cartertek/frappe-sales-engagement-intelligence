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


def _recalculate_prospects() -> None:
    if not frappe.db.table_exists("SEI Prospect"):
        return

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
        is_terminal_status,
    )
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    prospects = frappe.get_all("SEI Prospect", pluck="name")
    for prospect in prospects:
        apply_qualification_result(prospect)
        status = frappe.db.get_value("SEI Prospect", prospect, "lifecycle_status")
        if not is_terminal_status(status):
            apply_lifecycle_status(prospect)


def execute() -> None:
    _migrate_table("SEI Signal")
    _migrate_table("SEI Playbook Signal Rule")
    _recalculate_prospects()
