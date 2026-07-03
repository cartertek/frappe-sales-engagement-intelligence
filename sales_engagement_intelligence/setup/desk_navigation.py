"""Migration-safe Desk navigation bridge for Sales Engagement and Intelligence.

Frappe v17 generates Desktop Icon and Workspace Sidebar rows from installed app
and public Workspace metadata when an app is installed. This app is already
installed on production, so normal bench migrate will not rerun the install hook.

This bridge recreates only this app's Desk navigation rows after Frappe's orphan
cleanup has removed old standard file-backed rows. It intentionally does not
mutate Desktop Layout, User Workspaces, or unrelated apps' navigation records.
"""

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


def after_migrate() -> None:
    """Ensure generated Desk navigation rows exist for this installed app."""

    ensure_app_icon()
    ensure_workspace_sidebars()
    ensure_workspace_icons()
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
                "parent_icon": None if workspace_name == APP_TITLE else APP_TITLE,
                "icon": workspace.get("icon"),
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
