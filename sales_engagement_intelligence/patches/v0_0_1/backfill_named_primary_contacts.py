import frappe


def execute():
    if not frappe.db.has_column("SEI Prospect", "named_primary_contacts"):
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Prospect` prospect
        SET named_primary_contacts = (
            SELECT COUNT(*)
            FROM `tabSEI Prospect Contact` contact
            WHERE contact.parent = prospect.name
              AND contact.parenttype = 'SEI Prospect'
              AND contact.parentfield = 'contacts'
              AND contact.is_primary = 1
              AND COALESCE(TRIM(contact.contact_name), '') != ''
        )
        """
    )
