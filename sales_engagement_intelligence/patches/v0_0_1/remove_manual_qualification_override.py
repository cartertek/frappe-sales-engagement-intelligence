import frappe


def execute():
    if not frappe.db.has_column("SEI Prospect", "manual_qualification_override"):
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Prospect`
        SET qualification_status = 'Manually Approved'
        WHERE COALESCE(manual_qualification_override, 0) = 1
          AND COALESCE(manual_qualification_reason, '') != ''
          AND qualification_status NOT IN ('Rejected', 'Do Not Contact')
        """
    )
