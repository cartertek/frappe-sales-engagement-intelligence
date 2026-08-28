from __future__ import annotations

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute() -> None:
    custom_fields = {}
    for doctype in ("CRM Lead", "CRM Deal"):
        if not frappe.db.exists("DocType", doctype):
            continue
        custom_fields[doctype] = [
            {
                "fieldname": "sei_research_arena",
                "label": "Research Arena",
                "fieldtype": "Data",
                "insert_after": "sei_prospect",
                "is_system_generated": 1,
            }
        ]
    if custom_fields:
        create_custom_fields(custom_fields, update=True)

    for doctype in ("CRM Lead", "CRM Deal"):
        if not frappe.db.exists("DocType", doctype):
            continue
        old = "sei_" + "source_arena"
        new = "sei_research_arena"
        if frappe.db.has_column(doctype, old) and frappe.db.has_column(doctype, new):
            frappe.db.sql(
                f"UPDATE `tab{doctype}` SET `{new}` = `{old}` "
                f"WHERE COALESCE(`{new}`, '') = '' AND COALESCE(`{old}`, '') != ''"
            )
        old_custom_field = f"{doctype}-{old}"
        if frappe.db.exists("Custom Field", old_custom_field):
            frappe.delete_doc("Custom Field", old_custom_field, force=True, ignore_permissions=True)

    old_report = "Prospects by " + "Source Arena"
    if frappe.db.exists("Report", old_report):
        frappe.db.delete("Report", {"name": old_report})

    frappe.clear_cache()
