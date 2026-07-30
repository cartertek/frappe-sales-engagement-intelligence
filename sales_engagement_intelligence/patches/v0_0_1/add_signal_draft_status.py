import frappe


def execute():
    if not frappe.db.has_column("SEI Signal", "status"):
        return
    frappe.db.sql("UPDATE `tabSEI Signal` SET status = 'Published'")
