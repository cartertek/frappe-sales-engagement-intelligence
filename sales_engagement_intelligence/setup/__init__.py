import json

import frappe

PARENT_ICON = "Sales Engagement and Intelligence"
SEI_REMOVED_DESKTOP_ICONS = {"Signals"}
SEI_CANONICAL_RESEARCH_DOCTYPES = {"SEI Prospect", "SEI Signal"}
SEI_CANONICAL_TOUCHPOINT_DOCTYPES = {"SEI Interaction Attribution"}

SEI_DESKTOP_ICON_RENAMES = {
    "Assets": "Theses and Assets",
    "Reports": "Engagement Reports",
    "Settings": "Engagement Settings",
}


def after_migrate() -> None:
    """Refresh Desk state after app metadata and standard records sync."""

    repair_sei_desktop_layout()
    consolidate_prospecting_navigation()
    ensure_milestone_5_workspace_items()
    ensure_milestone_6_workspace_reports()
    ensure_signal_type_seed_data()
    ensure_milestone_8_seed_data()
    ensure_milestone_8_workspace_items()
    ensure_signal_prospect_tag_sync()
    ensure_prospect_signal_type_sync()
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
        original_length = len(node)
        node[:] = [
            child
            for child in node
            if not (
                isinstance(child, dict)
                and child.get("parent_icon") == PARENT_ICON
                and child.get("name") in SEI_REMOVED_DESKTOP_ICONS
            )
        ]
        changed = len(node) != original_length
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


def consolidate_prospecting_navigation() -> None:
    """Keep operational DocTypes associated with their canonical sidebars."""

    for doctype, name in (
        ("Desktop Icon", "Signals"),
        ("Workspace Sidebar", "Signals"),
        ("Workspace", "Signals"),
    ):
        if frappe.db.exists(doctype, name):
            frappe.delete_doc(doctype, name, force=True, ignore_permissions=True)

    if not frappe.db.table_exists("Workspace Sidebar"):
        return

    canonical_sidebar_by_doctype = {
        **{doctype: "Prospecting" for doctype in SEI_CANONICAL_RESEARCH_DOCTYPES},
        **{doctype: "Touchpoints" for doctype in SEI_CANONICAL_TOUCHPOINT_DOCTYPES},
    }
    for sidebar_name in frappe.get_all("Workspace Sidebar", pluck="name"):
        sidebar = frappe.get_doc("Workspace Sidebar", sidebar_name)
        retained_items = [
            item.as_dict()
            for item in sidebar.items
            if not (
                item.type == "Link"
                and item.link_to in canonical_sidebar_by_doctype
                and canonical_sidebar_by_doctype[item.link_to] != sidebar_name
            )
        ]
        if len(retained_items) != len(sidebar.items):
            sidebar.set("items", retained_items)
            sidebar.save(ignore_permissions=True)


def ensure_signal_type_seed_data() -> None:
    """Keep managed signal type taxonomy seeded after migrations."""

    try:
        from sales_engagement_intelligence.patches.v0_0_1.seed_signal_types import (
            execute as seed_signal_types,
        )

        seed_signal_types()
    except Exception:
        frappe.log_error(title="SEI signal type seed repair failed", message=frappe.get_traceback())


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
    changed = _remove_invalid_workspace_url_links(workspace)

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


def _remove_invalid_workspace_url_links(workspace) -> bool:
    """Drop legacy Workspace Link rows whose Dynamic Link target is URL.

    Workspace Link.link_to is a Dynamic Link keyed by link_type. Frappe does not
    ship a DocType named URL, so rows with link_type=URL fail validation when the
    Workspace is saved during migrate. Those navigation entries are already
    represented by workspace content/shortcuts or reports; keeping the invalid
    link rows is worse than omitting them because it blocks deploys.
    """

    original_len = len(workspace.links)
    workspace.set(
        "links",
        [link for link in workspace.links if link.get("link_type") != "URL"],
    )
    return len(workspace.links) != original_len


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

MILESTONE_8_QUEUE_SHORTCUTS = (
    "Needs Research",
    "Research Complete",
    "Qualified",
    "Find Contact",
    "Ready for CRM Conversion",
    "Rejected",
    "Do Not Contact",
)

MILESTONE_8_DAILY_WORKFLOW_SHORTCUTS = (
    ("SEI Prospect", "Prospects", "List", "Blue"),
    ("SEI Import Batch", "Import Batches", "List", "Blue"),
    ("SEI Import Batch", "New Import Batch", "New", "Green"),
)

MILESTONE_8_OUTREACH_SETUP_SHORTCUTS = (
    ("SEI Playbook", "Playbooks", "List", "Green"),
    ("SEI Message Template", "Message Templates", "List", "Green"),
    ("SEI Thesis", "Theses", "List", "Purple"),
    ("SEI Asset", "Assets", "List", "Purple"),
)

MILESTONE_8_SUPPORTING_RECORD_SHORTCUTS = (
    ("SEI Signal", "Signals", "List", "Grey"),
    ("SEI Interaction Attribution", "Interaction Attribution", "List", "Orange"),
)

MILESTONE_8_OPERATIONAL_SHORTCUTS = (
    *MILESTONE_8_DAILY_WORKFLOW_SHORTCUTS,
    *MILESTONE_8_OUTREACH_SETUP_SHORTCUTS,
    *MILESTONE_8_SUPPORTING_RECORD_SHORTCUTS,
)

MILESTONE_8_OPERATIONAL_DOCTYPES = tuple(
    (doctype, label, color)
    for doctype, label, _doc_view, color in MILESTONE_8_OPERATIONAL_SHORTCUTS
    if label != "New Import Batch"
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


def _queue_shortcut_values(label: str) -> dict:
    return {
        "type": "DocType",
        "link_to": "SEI Prospect",
        "label": label,
        "doc_view": "List",
        "stats_filter": json.dumps([["SEI Prospect", "lifecycle_status", "=", label]]),
        "color": "Grey",
    }


def _shortcut_values(doctype: str, label: str, doc_view: str, color: str) -> dict:
    return {
        "type": "DocType",
        "link_to": doctype,
        "label": label,
        "doc_view": doc_view,
        "color": color,
    }


def _prospecting_workspace_content() -> list:
    content = [
        {
            "id": "prospecting_header",
            "type": "header",
            "data": {"text": "Prospecting", "col": 12},
        },
        {
            "id": "prospecting_intro",
            "type": "paragraph",
            "data": {"text": "Pre-CRM research and qualification workflows.", "col": 12},
        },
        {
            "id": "prospecting_queue_header",
            "type": "header",
            "data": {"text": '<span class="h4"><b>Prospect Queues</b></span>', "col": 12},
        },
    ]

    for index, label in enumerate(MILESTONE_8_QUEUE_SHORTCUTS, 1):
        content.append(
            {
                "id": f"prospecting_queue_shortcut_{index}",
                "type": "shortcut",
                "data": {"shortcut_name": label, "col": 3},
            }
        )

    content.append(
        {
            "id": "prospecting_queue_guidance",
            "type": "paragraph",
            "data": {
                "text": (
                    "Research Complete is for Needs Review prospects. "
                    "Unqualified prospects should remain in Needs Research until a decision is possible, "
                    "or move to Rejected when research is complete and no qualifying evidence exists."
                ),
                "col": 12,
            },
        }
    )

    for section_id, title, intro, shortcuts in (
        (
            "daily_workflow",
            "Daily Workflow",
            "Open active prospects, review imports, or start a new import batch.",
            MILESTONE_8_DAILY_WORKFLOW_SHORTCUTS,
        ),
        (
            "outreach_setup",
            "Outreach Setup",
            "Configure playbooks, message templates, theses, and supporting assets.",
            MILESTONE_8_OUTREACH_SETUP_SHORTCUTS,
        ),
        (
            "supporting_records",
            "Supporting Records",
            "Review signal evidence and outcome attribution records.",
            MILESTONE_8_SUPPORTING_RECORD_SHORTCUTS,
        ),
    ):
        content.extend(
            [
                {
                    "id": f"{section_id}_header",
                    "type": "header",
                    "data": {"text": f'<span class="h4"><b>{title}</b></span>', "col": 12},
                },
                {
                    "id": f"{section_id}_intro",
                    "type": "paragraph",
                    "data": {"text": intro, "col": 12},
                },
            ]
        )
        for index, (_doctype, label, _doc_view, _color) in enumerate(shortcuts, 1):
            content.append(
                {
                    "id": f"{section_id}_shortcut_{index}",
                    "type": "shortcut",
                    "data": {"shortcut_name": label, "col": 3},
                }
            )

    return content


def _prospecting_workspace_links() -> list:
    links = []
    for section_label, shortcuts in (
        ("Daily Workflow", MILESTONE_8_DAILY_WORKFLOW_SHORTCUTS),
        ("Outreach Setup", MILESTONE_8_OUTREACH_SETUP_SHORTCUTS),
        ("Supporting Records", MILESTONE_8_SUPPORTING_RECORD_SHORTCUTS),
    ):
        links.append(
            {
                "type": "Card Break",
                "label": section_label,
                "link_type": "DocType",
                "link_to": None,
                "link_count": len(shortcuts),
                "onboard": 0,
                "dependencies": None,
                "hidden": 0,
            }
        )
        for doctype, label, _doc_view, _color in shortcuts:
            links.append(
                {
                    "type": "Link",
                    "label": label,
                    "link_type": "DocType",
                    "link_to": doctype,
                    "link_count": 0,
                    "onboard": 0,
                    "dependencies": None,
                    "hidden": 0,
                }
            )
    return links


def ensure_milestone_8_workspace_items() -> None:
    """Keep final Prospecting workspace navigation visible and de-duplicated."""

    if not frappe.db.exists("Workspace", "Prospecting"):
        return

    workspace = frappe.get_doc("Workspace", "Prospecting")
    changed = _remove_invalid_workspace_url_links(workspace)

    desired_content = _prospecting_workspace_content()
    if _load_workspace_content(workspace.content) != desired_content:
        workspace.content = json.dumps(desired_content)
        changed = True

    desired_links = _prospecting_workspace_links()
    existing_links = [
        {
            "type": link.get("type"),
            "label": link.get("label"),
            "link_type": link.get("link_type"),
            "link_to": link.get("link_to"),
            "link_count": link.get("link_count"),
            "onboard": link.get("onboard"),
            "dependencies": link.get("dependencies"),
            "hidden": link.get("hidden"),
        }
        for link in workspace.links
    ]
    if existing_links != desired_links:
        workspace.set("links", desired_links)
        changed = True

    desired_shortcuts = [
        *[_queue_shortcut_values(label) for label in MILESTONE_8_QUEUE_SHORTCUTS],
        *[
            _shortcut_values(doctype, label, doc_view, color)
            for doctype, label, doc_view, color in MILESTONE_8_OPERATIONAL_SHORTCUTS
        ],
    ]
    existing_shortcuts = [
        {
            "type": shortcut.get("type"),
            "link_to": shortcut.get("link_to"),
            "label": shortcut.get("label"),
            "doc_view": shortcut.get("doc_view"),
            "stats_filter": shortcut.get("stats_filter"),
            "color": shortcut.get("color"),
        }
        for shortcut in workspace.shortcuts
    ]
    if existing_shortcuts != desired_shortcuts:
        workspace.set("shortcuts", desired_shortcuts)
        changed = True

    if changed:
        workspace.save(ignore_permissions=True)


@frappe.whitelist()
def validate_milestone_8_workspace_items() -> dict:
    """Production-safe validation for final Milestone 8 navigation."""

    if not frappe.db.exists("Workspace", "Prospecting"):
        return {"ok": False, "missing_workspace": True}

    workspace = frappe.get_doc("Workspace", "Prospecting")
    shortcut_labels = {shortcut.label for shortcut in workspace.shortcuts}
    expected_labels = set(MILESTONE_8_QUEUE_SHORTCUTS) | {
        label for _doctype, label, _doc_view, _color in MILESTONE_8_OPERATIONAL_SHORTCUTS
    }
    missing_shortcuts = sorted(expected_labels - shortcut_labels)

    link_targets = {link.link_to for link in workspace.links if link.link_type == "DocType"}
    expected_doctypes = {
        doctype for doctype, _label, _doc_view, _color in MILESTONE_8_OPERATIONAL_SHORTCUTS
    }
    missing_links = sorted(expected_doctypes - link_targets)

    content = _load_workspace_content(workspace.content)
    content_shortcuts = {
        item.get("data", {}).get("shortcut_name")
        for item in content
        if isinstance(item, dict) and item.get("type") == "shortcut"
    }
    missing_content_shortcuts = sorted(expected_labels - content_shortcuts)

    content_headers = {
        item.get("data", {}).get("text")
        for item in content
        if isinstance(item, dict) and item.get("type") == "header"
    }
    expected_headers = {
        '<span class="h4"><b>Prospect Queues</b></span>',
        '<span class="h4"><b>Daily Workflow</b></span>',
        '<span class="h4"><b>Outreach Setup</b></span>',
        '<span class="h4"><b>Supporting Records</b></span>',
    }
    missing_headers = sorted(expected_headers - content_headers)

    duplicate_content_shortcuts = sorted(
        label
        for label in content_shortcuts
        if label and sum(
            1
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "shortcut"
            and item.get("data", {}).get("shortcut_name") == label
        )
        > 1
    )

    return {
        "ok": not missing_shortcuts
        and not missing_links
        and not missing_content_shortcuts
        and not missing_headers
        and not duplicate_content_shortcuts,
        "missing_workspace": False,
        "missing_shortcuts": missing_shortcuts,
        "missing_links": missing_links,
        "missing_content_shortcuts": missing_content_shortcuts,
        "missing_headers": missing_headers,
        "duplicate_content_shortcuts": duplicate_content_shortcuts,
    }


def ensure_prospect_signal_type_sync() -> None:
    """Backfill Prospect.signals from linked Signal Types after migrations."""

    try:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            prospect_signal_type_sync,
        )

        prospect_signal_type_sync.sync_all_prospect_signal_types()
    except Exception:
        frappe.log_error(
            title="SEI prospect signal type sync failed",
            message=frappe.get_traceback(),
        )


def ensure_signal_prospect_tag_sync() -> None:
    """Keep the DB-level prospect-tag sync trigger installed after migrations."""

    try:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
            prospect_tag_sync,
        )

        prospect_tag_sync.sync_all_signal_prospect_tags()
        prospect_tag_sync.ensure_signal_prospect_tag_trigger()
    except Exception:
        frappe.log_error(title="SEI prospect tag sync repair failed", message=frappe.get_traceback())
