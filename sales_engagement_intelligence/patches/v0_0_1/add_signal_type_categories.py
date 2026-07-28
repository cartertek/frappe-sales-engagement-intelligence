import frappe

DEFAULT_CATEGORY = "Uncategorized"


def execute() -> None:
    if not frappe.db.exists("DocType", "SEI Signal Type Category"):
        return

    if not frappe.db.exists("SEI Signal Type Category", DEFAULT_CATEGORY):
        frappe.get_doc(
            {
                "doctype": "SEI Signal Type Category",
                "category_name": DEFAULT_CATEGORY,
                "description": "Default category for Signal Types not yet classified.",
                "active": 1,
            }
        ).insert(ignore_permissions=True)

    if not frappe.db.table_exists("SEI Signal Type") or not frappe.db.has_column(
        "SEI Signal Type", "category"
    ):
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Signal Type`
        SET category = %s
        WHERE COALESCE(category, '') = ''
        """,
        (DEFAULT_CATEGORY,),
    )
