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
    ensure_milestone_8_seed_data()
    ensure_milestone_8_workspace_items()
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
    "Terminal Status Review",
    "Signals by Type and Strength",
    "Qualification by Signal Type",
    "Inferred Signal Review",
    "Missing Evidence Report",
    "Prospects by Source Arena",
    "Outcomes by Thesis",
    "Asset Usage and Outcomes",
    "Offer Performance",
    "CRM Conversion Summary",
    "CRM Lead Conversion Detail",
    "CRM Deal Conversion Detail",
    "CRM Context Missing",
    "Possible Duplicate CRM Conversion Review",
    "Import Batch Summary",
    "Import Batch Row Errors",
    "Import Source Quality",
    "Data Hygiene Dashboard",
    "Interaction Attribution Summary",
    "Response Category by Thesis",
    "Channel Outcome Report",
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
            "reports_shortcuts_header",
            {
                "id": "reports_shortcuts_header",
                "type": "header",
                "data": {"text": '<span class="h4"><b>SEI Reports</b></span>', "col": 12},
            },
        )
        or changed
    )
    for index, report_name in enumerate(MILESTONE_6_REPORTS, 1):
        changed = (
            _ensure_workspace_content_item(
                content,
                f"reports_shortcut_{index}",
                {
                    "id": f"reports_shortcut_{index}",
                    "type": "shortcut",
                    "data": {"shortcut_name": report_name, "col": 3},
                },
            )
            or changed
        )
    if changed:
        workspace.content = json.dumps(content)
        frappe.db.set_value(
            "Workspace",
            "Engagement Reports",
            "content",
            workspace.content,
            update_modified=False,
        )
        changed = False

    for report_name in MILESTONE_6_REPORTS:
        changed = (
            _ensure_workspace_link(
                workspace,
                {
                    "type": "Link",
                    "label": report_name,
                    "link_type": "Report",
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
                    "doc_view": "",
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
    content = _load_workspace_content(workspace.content)
    content_shortcuts = {
        item.get("data", {}).get("shortcut_name")
        for item in content
        if isinstance(item, dict) and item.get("type") == "shortcut"
    }
    missing_content = [
        report_name for report_name in MILESTONE_6_REPORTS if report_name not in content_shortcuts
    ]
    return {
        "ok": not missing and not missing_content,
        "missing_workspace": False,
        "missing_shortcuts": missing,
        "missing_content_shortcuts": missing_content,
    }

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
    # Workspace Link rows use a Dynamic Link field where ``link_type`` must be
    # populated before ``link_to``. Keep this helper defensive because existing
    # live rows may have been created by older migrations with an invalid
    # ``type=Report`` / missing ``link_type`` combination.
    if values.get("link_to") and not values.get("link_type"):
        values = {**values, "link_type": values.get("type")}
    if values.get("link_type") and values.get("type") not in {"Link", "Card Break"}:
        values = {**values, "type": "Link"}

    for link in workspace.links:
        if link.label == values["label"]:
            changed = False
            if link.get("link_to") and not link.get("link_type"):
                inferred_link_type = values.get("link_type") or link.get("type")
                if inferred_link_type:
                    link.set("link_type", inferred_link_type)
                    changed = True
            for key, value in values.items():
                if link.get(key) != value:
                    link.set(key, value)
                    changed = True
            return changed
    workspace.append("links", values)
    return True


def _normalize_workspace_shortcuts(workspace) -> bool:
    changed = False
    for shortcut in workspace.shortcuts:
        if shortcut.get("type") == "Report" and shortcut.get("doc_view") == "Report":
            shortcut.set("doc_view", "")
            changed = True
    return changed


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

MILESTONE_8_OPERATIONAL_DOCTYPES = (
    ("SEI Prospect", "SEI Prospects", "Blue"),
    ("SEI Import Batch", "SEI Import Batches", "Blue"),
    ("SEI Playbook", "SEI Playbooks", "Green"),
    ("SEI Message Template", "SEI Message Templates", "Green"),
    ("SEI Thesis", "SEI Theses", "Purple"),
    ("SEI Asset", "SEI Assets", "Purple"),
    ("SEI Interaction Attribution", "Interaction Attribution", "Orange"),
)


def ensure_milestone_8_seed_data() -> None:
    """Keep final playbook/template seed records present after migration."""

    if not frappe.db.exists("DocType", "SEI Playbook") or not frappe.db.exists(
        "DocType", "SEI Message Template"
    ):
        return
    from sales_engagement_intelligence.patches.v0_0_1.seed_playbooks_and_templates import (
        execute as seed_playbooks_and_templates,
    )

    seed_playbooks_and_templates()


def ensure_milestone_8_workspace_items() -> None:
    """Keep final SEI operating-system entry points visible in Prospecting."""

    if not frappe.db.exists("Workspace", "Prospecting"):
        return

    workspace = frappe.get_doc("Workspace", "Prospecting")
    changed = False
    content = _load_workspace_content(workspace.content)

    for item_id, item in (
        (
            "m8_outreach_header",
            {
                "id": "m8_outreach_header",
                "type": "header",
                "data": {"text": '<span class="h4"><b>Outreach Execution</b></span>', "col": 12},
            },
        ),
        (
            "m8_outreach_intro",
            {
                "id": "m8_outreach_intro",
                "type": "paragraph",
                "data": {
                    "text": "Playbooks, message templates, imports, queues, and attribution for manual outreach execution.",
                    "col": 12,
                },
            },
        ),
    ):
        changed = _ensure_workspace_content_item(content, item_id, item) or changed

    for index, (_, label, _) in enumerate(MILESTONE_8_OPERATIONAL_DOCTYPES, 1):
        changed = (
            _ensure_workspace_content_item(
                content,
                f"m8_outreach_shortcut_{index}",
                {
                    "id": f"m8_outreach_shortcut_{index}",
                    "type": "shortcut",
                    "data": {"shortcut_name": label, "col": 3},
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
                "label": "Outreach Execution",
                "link_type": "DocType",
                "link_to": None,
                "link_count": len(MILESTONE_8_OPERATIONAL_DOCTYPES),
                "onboard": 0,
                "dependencies": None,
                "hidden": 0,
            },
        )
        or changed
    )

    for doctype, label, color in MILESTONE_8_OPERATIONAL_DOCTYPES:
        changed = (
            _ensure_workspace_link(
                workspace,
                {
                    "type": "Link",
                    "label": doctype,
                    "link_type": "DocType",
                    "link_to": doctype,
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
                    "link_to": doctype,
                    "label": label,
                    "doc_view": "List",
                    "color": color,
                },
            )
            or changed
        )

    if changed:
        workspace.save(ignore_permissions=True)


@frappe.whitelist()
def validate_milestone_8_workspace_items() -> dict:
    """Production-safe validation for final Milestone 8 navigation."""

    if not frappe.db.exists("Workspace", "Prospecting"):
        return {"ok": False, "missing_workspace": True}

    workspace = frappe.get_doc("Workspace", "Prospecting")
    shortcut_labels = {shortcut.label for shortcut in workspace.shortcuts}
    expected_labels = {label for _, label, _ in MILESTONE_8_OPERATIONAL_DOCTYPES}
    missing_shortcuts = sorted(expected_labels - shortcut_labels)

    link_targets = {link.link_to for link in workspace.links if link.link_type == "DocType"}
    expected_doctypes = {doctype for doctype, _, _ in MILESTONE_8_OPERATIONAL_DOCTYPES}
    missing_links = sorted(expected_doctypes - link_targets)

    content = _load_workspace_content(workspace.content)
    content_shortcuts = {
        item.get("data", {}).get("shortcut_name")
        for item in content
        if isinstance(item, dict) and item.get("type") == "shortcut"
    }
    missing_content_shortcuts = sorted(expected_labels - content_shortcuts)

    return {
        "ok": not missing_shortcuts and not missing_links and not missing_content_shortcuts,
        "missing_workspace": False,
        "missing_shortcuts": missing_shortcuts,
        "missing_links": missing_links,
        "missing_content_shortcuts": missing_content_shortcuts,
    }
