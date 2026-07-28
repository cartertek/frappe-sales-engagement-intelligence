import frappe


def execute():
    frappe.db.set_value(
        "SEI Prospect",
        {"lifecycle_status": "Qualified"},
        "lifecycle_status",
        "Research Complete",
        update_modified=False,
    )

    if frappe.db.exists("Workspace", "Prospecting"):
        from sales_engagement_intelligence.setup import ensure_milestone_8_workspace_items

        ensure_milestone_8_workspace_items()
