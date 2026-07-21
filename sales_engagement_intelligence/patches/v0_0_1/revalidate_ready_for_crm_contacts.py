from __future__ import annotations

import frappe


def execute() -> None:
    if not frappe.db.table_exists("SEI Prospect"):
        return

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
    )

    prospects = frappe.get_all(
        "SEI Prospect",
        filters={"lifecycle_status": "Ready for CRM Conversion"},
        pluck="name",
    )
    for prospect in prospects:
        apply_lifecycle_status(prospect)
