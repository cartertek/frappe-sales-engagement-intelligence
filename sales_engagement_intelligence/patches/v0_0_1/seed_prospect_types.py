import frappe

PROSPECT_TYPES = (
    "Agency",
    "Startup",
    "SMB",
    "Enterprise",
    "Nonprofit",
    "NGO",
    "Government",
)


def execute():
    if not frappe.db.table_exists("SEI Prospect Type"):
        return

    for prospect_type in PROSPECT_TYPES:
        if frappe.db.exists("SEI Prospect Type", prospect_type):
            continue
        frappe.get_doc(
            {
                "doctype": "SEI Prospect Type",
                "prospect_type_name": prospect_type,
                "active": 1,
            }
        ).insert(ignore_permissions=True)
