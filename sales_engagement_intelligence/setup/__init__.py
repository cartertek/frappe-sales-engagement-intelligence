import json

import frappe

PARENT_ICON = "Sales Engagement and Intelligence"
SEI_DESKTOP_ICON_RENAMES = {
    "Assets": "Theses and Assets",
    "Reports": "Engagement Reports",
    "Settings": "Engagement Settings",
}


def after_migrate() -> None:
    """Refresh Desk state after app metadata and standard records sync."""

    repair_sei_desktop_layout()
    frappe.clear_cache()


def after_app_install(app_name: str) -> None:
    """Refresh Desk state when dependent apps are installed after SEI."""

    if app_name not in {"crm", "erpnext"}:
        return
    frappe.clear_cache()


def before_app_uninstall(app_name: str) -> None:
    """Refresh Desk state when dependent apps are removed."""

    if app_name not in {"crm", "erpnext"}:
        return
    frappe.clear_cache()


def repair_sei_desktop_layout() -> None:
    """Rewrite old SEI child icon names inside saved Desktop Layout rows.

    Frappe stores per-user Desktop Layout snapshots separately from Desktop Icon
    records. Only entries under the SEI parent icon are rewritten so ERPNext/core
    icons with the same generic labels are left alone.
    """

    if not frappe.db.table_exists("Desktop Layout"):
        return

    for name, layout_json in frappe.db.get_values("Desktop Layout", {}, ["name", "layout"]):
        if not layout_json:
            continue

        try:
            layout = json.loads(layout_json)
        except (TypeError, ValueError):
            continue

        if _repair_layout_node(layout):
            frappe.db.set_value(
                "Desktop Layout",
                name,
                "layout",
                json.dumps(layout, separators=(",", ":")),
                update_modified=False,
            )


def _repair_layout_node(node) -> bool:
    changed = False

    if isinstance(node, list):
        for child in node:
            changed = _repair_layout_node(child) or changed
        return changed

    if not isinstance(node, dict):
        return False

    if node.get("parent_icon") == PARENT_ICON:
        for old_name, new_name in SEI_DESKTOP_ICON_RENAMES.items():
            for key in ("name", "label", "link_to", "workspace", "title"):
                if node.get(key) == old_name:
                    node[key] = new_name
                    changed = True

    for value in node.values():
        changed = _repair_layout_node(value) or changed

    return changed
