import frappe


def execute():
    frappe.reload_doc(
        "sales_engagement_and_intelligence",
        "workspace",
        "prospecting",
        force=True,
    )
