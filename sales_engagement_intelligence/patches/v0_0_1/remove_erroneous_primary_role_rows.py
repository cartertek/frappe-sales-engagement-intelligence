from __future__ import annotations

import frappe


def execute() -> None:
    if not frappe.db.table_exists("SEI Prospect Contact"):
        return
    frappe.db.sql(
        """DELETE FROM `tabSEI Prospect Contact`
        WHERE parenttype = 'SEI Prospect'
          AND parentfield = 'contacts'
          AND COALESCE(contact_name, '') = ''
          AND COALESCE(emails, '') = ''
          AND COALESCE(notes, '') = ''
          AND COALESCE(crm_contact, '') = ''"""
    )
