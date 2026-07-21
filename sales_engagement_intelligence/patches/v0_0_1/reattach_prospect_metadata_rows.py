import frappe


def execute():
    frappe.db.sql(
        """
        UPDATE `tabSEI Prospect Metadata`
        SET parentfield = 'prospect_metadata'
        WHERE parenttype = 'SEI Prospect'
          AND parentfield = 'metadata'
        """
    )
