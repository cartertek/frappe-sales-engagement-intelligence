"""Clean up legacy SEI Desk records after moving to an HRMS-style model."""

import frappe

APP = "sales_engagement_intelligence"
PARENT_ICON = "Sales Engagement and Intelligence"
RENAMES = {
    "Assets": "Theses and Assets",
    "Reports": "Engagement Reports",
    "Settings": "Engagement Settings",
}


def execute() -> None:
    """Rename or remove old app-owned generic Desk records once."""

    for old_name, new_name in RENAMES.items():
        _rename_or_remove_app_record("Workspace", old_name, new_name)
        _rename_or_remove_app_record("Workspace Sidebar", old_name, new_name)
        _rename_or_remove_app_record("Desktop Icon", old_name, new_name)

    _delete_app_owned_record("Workspace Sidebar", PARENT_ICON)
    _delete_app_owned_record("Workspace", PARENT_ICON)
    frappe.clear_cache()


def _delete_app_owned_record(doctype: str, name: str) -> None:
    if frappe.db.exists(doctype, name) and _is_app_owned_record(doctype, name):
        frappe.delete_doc(doctype, name, force=True, ignore_permissions=True)


def _rename_or_remove_app_record(doctype: str, old_name: str, new_name: str) -> None:
    if not frappe.db.exists(doctype, old_name):
        return

    if not _is_app_owned_record(doctype, old_name):
        return

    if frappe.db.exists(doctype, new_name):
        frappe.delete_doc(doctype, old_name, force=True, ignore_permissions=True)
        return

    frappe.rename_doc(
        doctype,
        old_name,
        new_name,
        force=True,
        ignore_permissions=True,
        show_alert=False,
    )


def _is_app_owned_record(doctype: str, name: str) -> bool:
    app = frappe.db.get_value(doctype, name, "app")
    if app == APP:
        return True

    if doctype == "Desktop Icon":
        parent_icon = frappe.db.get_value(doctype, name, "parent_icon")
        return parent_icon == PARENT_ICON

    if doctype == "Workspace":
        parent_page = frappe.db.get_value(doctype, name, "parent_page")
        module = frappe.db.get_value(doctype, name, "module")
        return parent_page == PARENT_ICON or module == "Sales Engagement and Intelligence"

    return False
