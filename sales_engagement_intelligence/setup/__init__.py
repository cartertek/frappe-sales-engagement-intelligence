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
    ensure_milestone_6_workspace_reports()
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
                "link_count": 1,
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


MILESTONE_6_REPORTS = (
    "Prospect Lifecycle Summary",
    "Active Prospect Queue",
    "Ready for CRM Conversion",
    "Signals by Type and Strength",
    "Qualification by Signal Type",
    "Prospects by Source Arena",
    "Outcomes by Thesis",
    "CRM Conversion Summary",
    "CRM Context Missing",
    "Import Batch Summary",
    "Import Batch Row Errors",
    "Data Hygiene Dashboard",
    "Interaction Attribution Summary",
)


def ensure_milestone_6_workspace_reports() -> None:
    """Keep Milestone 6 report shortcuts visible after fixture sync.

    Workspace fixtures are not sufficient once a live Workspace has been synced or
    customized. This repair is idempotent, scoped to Engagement Reports, and only
    creates/repairs report navigation metadata. It does not execute reports or mutate
    SEI/CRM business records.
    """

    if not frappe.db.exists("Workspace", "Engagement Reports"):
        return

    workspace = frappe.get_doc("Workspace", "Engagement Reports")
    changed = False

    content = _load_workspace_content(workspace.content)
    changed = (
        _ensure_workspace_content_item(
            content,
            "reports_header",
            {
                "id": "reports_header",
                "type": "header",
                "data": {"text": "Reports and Feedback", "col": 12},
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_content_item(
            content,
            "reports_intro",
            {
                "id": "reports_intro",
                "type": "paragraph",
                "data": {
                    "text": (
                        "Operational reporting for prospect queues, signals, imports, "
                        "CRM conversion, data hygiene, and interaction attribution."
                    ),
                    "col": 12,
                },
            },
        )
        or changed
    )
    changed = (
        _ensure_workspace_content_item(
            content,
            "reports_card",
            {
                "id": "reports_card",
                "type": "card",
                "data": {"card_name": "SEI Reports", "col": 4},
            },
        )
        or changed
    )
    if changed:
        workspace.content = json.dumps(content)

    for report_name in MILESTONE_6_REPORTS:
        changed = (
            _ensure_workspace_link(
                workspace,
                {
                    "type": "Report",
                    "label": report_name,
                    "link_to": report_name,
                    "link_count": 0,
                    "onboard": 0,
                    "hidden": 0,
                    "is_query_report": 0,
                },
            )
            or changed
        )
        changed = (
            _ensure_workspace_shortcut(
                workspace,
                {
                    "type": "Report",
                    "link_to": report_name,
                    "label": report_name,
                    "doc_view": "Report",
                    "color": "Purple",
                    "stats_filter": "[]",
                },
            )
            or changed
        )

    if changed:
        workspace.save(ignore_permissions=True)


@frappe.whitelist()
def validate_milestone_6_workspace_reports() -> dict:
    """Production-safe validation for the live Engagement Reports workspace."""

    if not frappe.db.exists("Workspace", "Engagement Reports"):
        return {"ok": False, "missing_workspace": True, "missing_shortcuts": list(MILESTONE_6_REPORTS)}

    workspace = frappe.get_doc("Workspace", "Engagement Reports")
    labels = {shortcut.label for shortcut in workspace.shortcuts}
    missing = [report_name for report_name in MILESTONE_6_REPORTS if report_name not in labels]
    return {"ok": not missing, "missing_workspace": False, "missing_shortcuts": missing}

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
