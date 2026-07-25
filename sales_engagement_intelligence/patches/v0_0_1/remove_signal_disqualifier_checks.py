from __future__ import annotations

import frappe

LEGACY_DOCTYPE = "SEI Signal Disqualifier Check"


def execute() -> None:
    if frappe.db.exists("DocType", LEGACY_DOCTYPE):
        frappe.delete_doc("DocType", LEGACY_DOCTYPE, ignore_permissions=True, force=True)

    if frappe.db.table_exists("SEI Signal") and frappe.db.has_column("SEI Signal", "is_strength_capped"):
        frappe.db.sql_ddl("ALTER TABLE `tabSEI Signal` DROP COLUMN `is_strength_capped`")
