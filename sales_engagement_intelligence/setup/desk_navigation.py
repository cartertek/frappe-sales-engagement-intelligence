"""Migration-safe Desk navigation bridge for Sales Engagement and Intelligence."""

from __future__ import annotations

import frappe

APP_NAME = "sales_engagement_intelligence"
APP_TITLE = "Sales Engagement and Intelligence"
APP_LOGO = "/assets/sales_engagement_intelligence/desktop_icons/app.svg"
APP_ROUTE = "/app/sales-engagement-and-intelligence"

WORKSPACES = (
    "Sales Engagement and Intelligence",
    "Prospecting",
    "Signals",
    "Touchpoints",
    "Theses and Assets",
    "CRM Attribution",
    "Engagement Reports",
    "Engagement Settings",
)

LAYOUT_RENAMES = {
    "Assets": "Theses and Assets",
    "CRM Conversion": "CRM Attribution",
    "Reports": "Engagement Reports",
    "Settings": "Engagement Settings",
}

WORKSPACE_LOGOS = {
    "Prospecting": "/assets/sales_engagement_intelligence/desktop_icons/prospecting.svg",
    "Signals": "/assets/sales_engagement_intelligence/desktop_icons/signals.svg",
    "Touchpoints": "/assets/sales_engagement_intelligence/desktop_icons/touchpoints.svg",
    "Theses and Assets": "/assets/sales_engagement_intelligence/desktop_icons/assets.svg",
    "CRM Attribution": "/assets/sales_engagement_intelligence/desktop_icons/crm_conversion.svg",
    "Engagement Reports": "/assets/sales_engagement_intelligence/desktop_icons/reports.svg",
    "Engagement Settings": "/assets/sales_engagement_intelligence/desktop_icons/settings.svg",
}


def after_migrate() -> None:
    """Ensure generated Desk navigation rows exist for this installed app."""

    ensure_app_icon()
    ensure_workspace_sidebars()
    ensure_workspace_icons()
    repair_saved_layouts()
    clear_navigation_cache()


def ensure_app_icon() -> None:
    icon = get_or_new_doc("Desktop Icon", APP_TITLE)
    icon.update(
        {
            "label": APP_TITLE,
            "icon_type": "App",
            "link_type": "External",
            "link": APP_ROUTE,
            "logo_url": APP_LOGO,
            "app": APP_NAME,
            "standard": 0,
            "hidden": 0,
            "restrict_removal": 0,
        }
    )
    save_doc(icon)


def ensure_workspace_sidebars() -> None:
    for workspace_name in WORKSPACES:
        if not frappe.db.exists("Workspace", workspace_name):
            continue

        workspace = frappe.get_doc("Workspace", workspace_name)
        sidebar = get_or_new_doc("Workspace Sidebar", workspace_name)
        sidebar.update(
            {
                "title": workspace_name,
                "header_icon": workspace.get("icon"),
                "app": APP_NAME,
                "standard": 0,
                "for_user": None,
            }
        )
        ensure_sidebar_items(sidebar, workspace)
        save_doc(sidebar)


def ensure_sidebar_items(sidebar, workspace) -> None:
    existing = {(item.link_type, item.link_to) for item in sidebar.get("items", [])}

    if ("Workspace", workspace.name) not in existing:
        sidebar.append(
            "items",
            {
                "label": "Home",
                "link_to": workspace.name,
                "link_type": "Workspace",
                "type": "Link",
                "idx": 0,
            },
        )

    next_idx = len(sidebar.get("items", []))
    for shortcut in workspace.get("shortcuts", []):
        link_to = shortcut.get("link_to")
        link_type = shortcut.get("type")
        if not link_to or not link_type or (link_type, link_to) in existing:
            continue

        sidebar.append(
            "items",
            {
                "label": shortcut.get("label") or link_to,
                "link_to": link_to,
                "link_type": link_type,
                "type": "Link",
                "idx": next_idx,
            },
        )
        next_idx += 1
        existing.add((link_type, link_to))


def ensure_workspace_icons() -> None:
    for workspace_name in WORKSPACES:
        if workspace_name == APP_TITLE:
            continue
        if not frappe.db.exists("Workspace", workspace_name):
            continue
        if not frappe.db.exists("Workspace Sidebar", workspace_name):
            continue

        workspace = frappe.get_doc("Workspace", workspace_name)
        icon = get_or_new_doc("Desktop Icon", workspace_name)
        icon.update(
            {
                "label": workspace_name,
                "icon_type": "Link",
                "link_type": "Workspace Sidebar",
                "link_to": workspace_name,
                "parent_icon": APP_TITLE,
                "icon": workspace.get("icon"),
                "logo_url": WORKSPACE_LOGOS.get(workspace_name),
                "app": APP_NAME,
                "standard": 0,
                "hidden": 0,
                "restrict_removal": 0,
            }
        )
        save_doc(icon)


def repair_saved_layouts() -> None:
    for layout_name in frappe.get_all("Desktop Layout", pluck="name"):
        layout = frappe.db.get_value("Desktop Layout", layout_name, "layout")
        if not layout:
            continue

        rows = parse_layout(layout)
        if not isinstance(rows, list):
            continue

        changed = False
        for row in rows:
            if isinstance(row, dict):
                changed = update_layout_row(row) or changed

        if changed:
            frappe.db.set_value("Desktop Layout", layout_name, "layout", frappe.as_json(rows))


def parse_layout(layout: str):
    try:
        return frappe.parse_json(layout)
    except Exception:
        return None


def update_layout_row(row: dict, in_sei_app: bool = False) -> bool:
    changed = False
    row_is_sei = in_sei_app or row.get("app") == APP_NAME or row.get("parent_icon") == APP_TITLE
    old_name = row.get("name") or row.get("label")
    new_name = LAYOUT_RENAMES.get(old_name)

    if row_is_sei and new_name:
        for key in ("name", "label", "link_to", "parent_icon", "sidebar"):
            if row.get(key) == old_name:
                row[key] = new_name
                changed = True

    children = row.get("child_icons")
    child_in_sei_app = row_is_sei or row.get("name") == APP_TITLE or row.get("label") == APP_TITLE
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                changed = update_layout_row(child, in_sei_app=child_in_sei_app) or changed

    return changed


def get_or_new_doc(doctype: str, name: str):
    if frappe.db.exists(doctype, name):
        return frappe.get_doc(doctype, name)
    doc = frappe.new_doc(doctype)
    if doctype == "Desktop Icon":
        doc.label = name
    elif doctype == "Workspace Sidebar":
        doc.title = name
    return doc


def save_doc(doc) -> None:
    doc.flags.ignore_permissions = True
    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)


def clear_navigation_cache() -> None:
    frappe.cache.delete_key("desktop_icons")
    frappe.cache.delete_key("bootinfo")
    frappe.clear_cache()
