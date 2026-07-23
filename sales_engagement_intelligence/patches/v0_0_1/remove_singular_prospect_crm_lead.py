from __future__ import annotations

import frappe


def execute() -> None:
    if not frappe.db.table_exists("SEI Prospect") or not frappe.db.has_column(
        "SEI Prospect", "crm_lead"
    ):
        return

    if frappe.db.table_exists("CRM Lead") and frappe.db.has_column("CRM Lead", "sei_prospect"):
        legacy_links = frappe.db.sql(
            """
            SELECT name, crm_lead
            FROM `tabSEI Prospect`
            WHERE COALESCE(crm_lead, '') != ''
            """,
            as_dict=True,
        )
        for row in legacy_links:
            if not frappe.db.exists("CRM Lead", row.crm_lead):
                continue
            current = frappe.db.get_value("CRM Lead", row.crm_lead, "sei_prospect")
            if current and current != row.name:
                frappe.throw(
                    f"CRM Lead {row.crm_lead} is linked to {current}, but legacy Prospect "
                    f"{row.name} also references it. Resolve this conflict before migration."
                )
            frappe.db.set_value(
                "CRM Lead",
                row.crm_lead,
                "sei_prospect",
                row.name,
                update_modified=False,
            )

    frappe.db.sql_ddl("ALTER TABLE `tabSEI Prospect` DROP COLUMN `crm_lead`")
