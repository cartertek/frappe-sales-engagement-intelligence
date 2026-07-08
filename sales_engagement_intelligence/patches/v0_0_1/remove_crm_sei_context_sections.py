import frappe

SECTION_CUSTOM_FIELDS = (
    "CRM Lead-sei_section",
    "CRM Deal-sei_section",
)


def execute():
    """Remove redundant SEI Context sections now that SEI fields live on tabs."""

    for custom_field in SECTION_CUSTOM_FIELDS:
        if frappe.db.exists("Custom Field", custom_field):
            frappe.delete_doc("Custom Field", custom_field, ignore_permissions=True, force=True)

    frappe.clear_cache()
