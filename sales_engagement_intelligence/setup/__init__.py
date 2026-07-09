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
    ensure_milestone_5_workspace_items()
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


def ensure_milestone_5_workspace_items() -> None:
    """Ensure Milestone 5 import shortcuts are visible in the Prospecting workspace.

    Workspace fixtures and one-time patches do not reliably overwrite a live Workspace
    after it has already been synced or customized. This repair is intentionally
    idempotent and narrowly scoped to the Prospecting workspace so future deploys keep
    the SEI import entry points visible without disturbing the existing queue cards.
    """

    if not frappe.db.exists("Workspace", "Prospecting"):
        return

    workspace = frappe.get_doc("Workspace", "Prospecting")
    changed = False

    content = _load_workspace_content(workspace.content)
    changed = (
        _ensure_workspace_content_item(
            content,
            "sei_imports_header",
            {
                "id": "sei_imports_header",
                "type": "header",
                "data": {
                    "text": '<span class="h4"><b>SEI Imports</b></span>',
                    "col": 12,
                },
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_content_item(
            content,
            "sei_imports_shortcut_1",
            {
                "id": "sei_imports_shortcut_1",
                "type": "shortcut",
                "data": {"shortcut_name": "SEI Import Batches", "col": 3},
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_content_item(
            content,
            "sei_imports_shortcut_2",
            {
                "id": "sei_imports_shortcut_2",
                "type": "shortcut",
                "data": {"shortcut_name": "New Import Batch", "col": 3},
            },
        )
        or changed
    )

    if changed:
        workspace.content = json.dumps(content)

    changed = (
        _ensure_workspace_link(
            workspace,
            {
                "type": "Card Break",
                "label": "SEI Imports",
                "link_type": "DocType",
                "link_to": None,
                "link_count": 3,
                "onboard": 0,
                "dependencies": None,
                "hidden": 0,
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_link(
            workspace,
            {
                "type": "Link",
                "label": "SEI Import Batch",
                "link_type": "DocType",
                "link_to": "SEI Import Batch",
                "link_count": 0,
                "onboard": 0,
                "dependencies": None,
                "hidden": 0,
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_link(
            workspace,
            {
                "type": "Link",
                "label": "Import Templates Documentation",
                "link_type": "URL",
                "link_to": "/app/file?file_url=%25docs/import_templates%25",
                "link_count": 0,
                "onboard": 0,
                "dependencies": None,
                "hidden": 0,
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_link(
            workspace,
            {
                "type": "Link",
                "label": "Data Hygiene",
                "link_type": "URL",
                "link_to": "/app/query-report",
                "link_count": 0,
                "onboard": 0,
                "dependencies": None,
                "hidden": 0,
            },
        )
        or changed
    )

    changed = (
        _ensure_workspace_shortcut(
            workspace,
            {
                "type": "DocType",
                "link_to": "SEI Import Batch",
                "label": "SEI Import Batches",
                "doc_view": "List",
                "color": "Blue",
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_shortcut(
            workspace,
            {
                "type": "DocType",
                "link_to": "SEI Import Batch",
                "label": "New Import Batch",
                "doc_view": "New",
                "color": "Green",
            },
        )
        or changed
    )

    if changed:
        workspace.save(ignore_permissions=True)


def _load_workspace_content(content: str | None) -> list:
    if not content:
        return []
    try:
        parsed = json.loads(content)
    except (TypeError, ValueError):
        return []
    return parsed if isinstance(parsed, list) else []


def _ensure_workspace_content_item(content: list, item_id: str, item: dict) -> bool:
    for index, existing in enumerate(content):
        if isinstance(existing, dict) and existing.get("id") == item_id:
            if existing != item:
                content[index] = item
                return True
            return False
    content.append(item)
    return True


def _ensure_workspace_link(workspace, values: dict) -> bool:
    for link in workspace.links:
        if link.label == values["label"]:
            changed = False
            for key, value in values.items():
                if link.get(key) != value:
                    link.set(key, value)
                    changed = True
            return changed
    workspace.append("links", values)
    return True


def _ensure_workspace_shortcut(workspace, values: dict) -> bool:
    for shortcut in workspace.shortcuts:
        if shortcut.label == values["label"]:
            changed = False
            for key, value in values.items():
                if shortcut.get(key) != value:
                    shortcut.set(key, value)
                    changed = True
            return changed
    workspace.append("shortcuts", values)
    return True
