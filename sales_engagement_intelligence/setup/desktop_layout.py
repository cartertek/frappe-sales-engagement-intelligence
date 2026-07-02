"""Desktop layout maintenance for Sales Engagement and Intelligence."""

import frappe

APP_NAME = "sales_engagement_intelligence"

LEGACY_ASSET_RENAMES = {
    "sei_app.svg": "app.svg",
    "sei_prospecting.svg": "prospecting.svg",
    "sei_signals.svg": "signals.svg",
    "sei_touchpoints.svg": "touchpoints.svg",
    "sei_assets.svg": "assets.svg",
    "sei_crm_conversion.svg": "crm_conversion.svg",
    "sei_reports.svg": "reports.svg",
    "sei_settings.svg": "settings.svg",
}

# These were exported by the app with globally common document names.  The visible
# labels are fine; the document names are not.  New records use app-specific names.
LEGACY_GLOBAL_RECORDS = (
    "Prospecting",
    "Signals",
    "Touchpoints",
    "Assets",
    "CRM Conversion",
    "Reports",
    "Settings",
)


def after_migrate() -> None:
    """Repair desktop state touched by older standard desktop exports."""

    rename_desktop_icon_assets()
    remove_legacy_global_records()
    restore_missing_desktop_icons()


def rename_desktop_icon_assets() -> None:
    updated_users = []
    for name in frappe.get_all("Desktop Layout", pluck="name"):
        layout = frappe.db.get_value("Desktop Layout", name, "layout") or ""
        updated_layout = layout
        for old, new in LEGACY_ASSET_RENAMES.items():
            updated_layout = updated_layout.replace(old, new)

        if updated_layout != layout:
            frappe.db.set_value("Desktop Layout", name, "layout", updated_layout)
            updated_users.append(name)

    if updated_users:
        frappe.db.commit()
        for user in updated_users:
            frappe.clear_cache(user=user)
        frappe.clear_cache()


def remove_legacy_global_records() -> None:
    """Remove only app-owned legacy records with globally common names.

    Earlier versions exported standard ``Desktop Icon`` / ``Workspace Sidebar`` /
    ``Workspace`` rows named ``Assets``, ``Reports``, ``Settings``, etc.  Those
    names are global document names and can collide with core or other app Desk
    records.  The replacement records keep the same visible labels but use
    app-specific document names such as ``Sales Engagement Assets``.
    """

    for doctype in ("Desktop Icon", "Workspace Sidebar", "Workspace"):
        if not frappe.db.exists("DocType", doctype):
            continue

        for name in LEGACY_GLOBAL_RECORDS:
            if frappe.db.get_value(doctype, name, "app") == APP_NAME:
                frappe.delete_doc(doctype, name, ignore_permissions=True, force=True)


def restore_missing_desktop_icons() -> None:
    """Restore desktop icons removed during legacy sidebar cleanup.

    The v17 upgrade path can remove ``Desktop Icon`` rows while converting old
    ``Workspace Sidebar`` rows.  Once the app-owned naming collisions are gone,
    recreate missing public icons from the surviving public Workspace Sidebar or
    Workspace records without overwriting any existing icon.
    """

    if not frappe.db.exists("DocType", "Desktop Icon"):
        return

    restored = restore_icons_from_workspace_sidebars()
    restored += restore_icons_from_workspaces()

    if restored:
        frappe.clear_cache()


def restore_icons_from_workspace_sidebars() -> int:
    if not frappe.db.exists("DocType", "Workspace Sidebar"):
        return 0

    restored = 0
    sidebars = frappe.get_all(
        "Workspace Sidebar",
        filters={"for_user": ("in", ("", None))},
        fields=["name", "title", "header_icon", "idx", "app"],
    )
    for sidebar in sidebars:
        if frappe.db.exists("Desktop Icon", sidebar.name):
            continue

        doc = frappe.new_doc("Desktop Icon")
        doc.name = sidebar.name
        doc.label = sidebar.title or sidebar.name
        doc.app = sidebar.app or "frappe"
        doc.hidden = 0
        doc.standard = 1
        doc.icon_type = "Link"
        doc.link_type = "Workspace Sidebar"
        doc.link_to = sidebar.name
        doc.icon = sidebar.header_icon or "folder-normal"
        doc.idx = sidebar.idx or 0
        doc.insert(ignore_permissions=True)
        restored += 1

    return restored


def restore_icons_from_workspaces() -> int:
    if not frappe.db.exists("DocType", "Workspace"):
        return 0
    if not desktop_icon_supports_workspace_links():
        return 0

    restored = 0
    workspaces = frappe.get_all(
        "Workspace",
        filters={"for_user": ("in", ("", None))},
        fields=["name", "title", "label", "icon", "idx", "app", "public"],
    )
    for workspace in workspaces:
        if workspace.public == 0:
            continue
        if frappe.db.exists("Desktop Icon", workspace.name):
            continue

        doc = frappe.new_doc("Desktop Icon")
        doc.name = workspace.name
        doc.label = workspace.title or workspace.label or workspace.name
        doc.app = workspace.app or "frappe"
        doc.hidden = 0
        doc.standard = 1
        doc.icon_type = "Link"
        doc.link_type = "Workspace"
        doc.link_to = workspace.name
        doc.icon = workspace.icon or "folder-normal"
        doc.idx = workspace.idx or 0
        doc.insert(ignore_permissions=True)
        restored += 1

    return restored


def desktop_icon_supports_workspace_links() -> bool:
    meta = frappe.get_meta("Desktop Icon")
    field = meta.get_field("link_type")
    options = (field.options or "") if field else ""
    return "Workspace" in {option.strip() for option in options.split("\n")}
