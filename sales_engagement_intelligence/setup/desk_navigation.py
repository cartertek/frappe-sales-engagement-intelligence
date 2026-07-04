"""Migration-safe Desk navigation bridge for Sales Engagement and Intelligence."""

from __future__ import annotations

import frappe

APP_NAME = "sales_engagement_intelligence"
APP_TITLE = "Sales Engagement and Intelligence"
APP_LOGO = "/assets/sales_engagement_intelligence/desktop_icons/app.svg"
APP_ROUTE = "/app/sales-engagement-and-intelligence"
ICON_COLOR = "#700da8"

APP_ICON = {
    "label": APP_TITLE,
    "workspace": "Sales Engagement and Intelligence",
    "icon": "broadcast",
    "logo_url": APP_LOGO,
    "idx": 20,
}

NAV_ITEMS = (
    ("Prospecting", "Prospecting", "search", "prospecting.svg", 1),
    ("Signals", "Signals", "chart", "signals.svg", 2),
    ("Touchpoints", "Touchpoints", "mail", "touchpoints.svg", 3),
    ("Assets", "Theses and Assets", "folder", "assets.svg", 4),
    ("CRM Conversion", "CRM Attribution", "arrow-right", "crm_conversion.svg", 5),
    ("Reports", "Engagement Reports", "bar-chart", "reports.svg", 6),
    ("Settings", "Engagement Settings", "setting", "settings.svg", 7),
)


def logo_url(filename: str) -> str:
    return f"/assets/sales_engagement_intelligence/desktop_icons/{filename}"


def after_migrate() -> None:
    """Ensure generated Desk navigation rows preserve production desktop display."""

    ensure_app_icon()
    ensure_workspace_sidebars()
    ensure_workspace_icons()
    clear_navigation_cache()


def ensure_app_icon() -> None:
    icon = get_or_new_doc("Desktop Icon", APP_TITLE)
    icon.update(
        {
            "label": APP_TITLE,
            "bg_color": ICON_COLOR,
            "icon_type": "App",
            "link_type": "External",
            "link": APP_ROUTE,
            "logo_url": APP_ICON["logo_url"],
            "idx": APP_ICON["idx"],
            "app": APP_NAME,
            "standard": 0,
            "hidden": 0,
            "restrict_removal": 0,
        }
    )
    save_doc(icon)


def ensure_workspace_sidebars() -> None:
    ensure_parent_sidebar()
    for label, workspace_name, icon_name, _logo, _idx in NAV_ITEMS:
        if not frappe.db.exists("Workspace", workspace_name):
            continue
        sidebar = get_or_new_doc("Workspace Sidebar", label)
        sidebar.update(
            {
                "title": label,
                "header_icon": icon_name,
                "app": APP_NAME,
                "standard": 0,
                "for_user": None,
            }
        )
        set_sidebar_items(sidebar, frappe.get_doc("Workspace", workspace_name))
        save_doc(sidebar)


def ensure_parent_sidebar() -> None:
    workspace_name = APP_ICON["workspace"]
    if not frappe.db.exists("Workspace", workspace_name):
        return
    sidebar = get_or_new_doc("Workspace Sidebar", APP_TITLE)
    sidebar.update(
        {
            "title": APP_TITLE,
            "header_icon": APP_ICON["icon"],
            "app": APP_NAME,
            "standard": 0,
            "for_user": None,
        }
    )
    set_sidebar_items(sidebar, frappe.get_doc("Workspace", workspace_name))
    save_doc(sidebar)


def set_sidebar_items(sidebar, workspace) -> None:
    sidebar.set("items", [])
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
    idx = 1
    for shortcut in workspace.get("shortcuts", []):
        link_to = shortcut.get("link_to")
        link_type = shortcut.get("type")
        if not link_to or not link_type:
            continue
        sidebar.append(
            "items",
            {
                "label": shortcut.get("label") or link_to,
                "link_to": link_to,
                "link_type": link_type,
                "type": "Link",
                "idx": idx,
            },
        )
        idx += 1


def ensure_workspace_icons() -> None:
    for label, workspace_name, icon_name, logo_file, idx in NAV_ITEMS:
        if not frappe.db.exists("Workspace", workspace_name):
            continue
        if not frappe.db.exists("Workspace Sidebar", label):
            continue
        icon = get_or_new_doc("Desktop Icon", label)
        icon.update(
            {
                "label": label,
                "bg_color": ICON_COLOR,
                "icon_type": "Link",
                "link_type": "Workspace Sidebar",
                "link_to": label,
                "parent_icon": APP_TITLE,
                "icon": icon_name,
                "logo_url": logo_url(logo_file),
                "idx": idx,
                "app": APP_NAME,
                "standard": 0,
                "hidden": 0,
                "restrict_removal": 0,
            }
        )
        save_doc(icon)


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
