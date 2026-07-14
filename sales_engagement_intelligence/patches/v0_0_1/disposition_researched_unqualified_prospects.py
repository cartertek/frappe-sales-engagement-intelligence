import frappe


def execute():
    """Disposition researched but unqualified prospects after lifecycle rule cleanup."""
    prospects = frappe.get_all(
        "SEI Prospect",
        filters={
            "lifecycle_status": "Research Complete",
            "qualification_status": "Unqualified",
        },
        pluck="name",
    )

    for prospect in prospects:
        frappe.db.set_value(
            "SEI Prospect",
            prospect,
            {
                "lifecycle_status": "Rejected",
                "qualification_status": "Rejected",
                "ready_for_crm_conversion": 0,
            },
            update_modified=True,
        )
