"""Desktop launcher setup for Sales Engagement and Intelligence."""

import json

import frappe
from frappe.model.document import Document

APP_NAME = "sales_engagement_intelligence"
PARENT_LABEL = "Sales Engagement and Intelligence"
COLOR = "#700da8"

CHILDREN = [
    {
        "name": "Prospecting - Sales Engagement",
        "label": "Prospecting",
        "workspace": "Prospecting",
        "icon": "search",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/prospecting.svg",
        "idx": 1,
    },
    {
        "name": "Signals - Sales Engagement",
        "label": "Signals",
        "workspace": "Signals",
        "icon": "chart",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/signals.svg",
        "idx": 2,
    },
    {
        "name": "Touchpoints - Sales Engagement",
        "label": "Touchpoints",
        "workspace": "Touchpoints",
        "icon": "mail",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/touchpoints.svg",
        "idx": 3,
    },
    {
        "name": "Assets - Sales Engagement",
        "label": "Assets",
        "workspace": "Assets",
        "icon": "folder",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/assets.svg",
        "idx": 4,
    },
    {
        "name": "CRM Conversion - Sales Engagement",
        "label": "CRM Conversion",
        "workspace": "CRM Conversion",
        "icon": "arrow-right",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/crm_conversion.svg",
        "idx": 5,
    },
    {
        "name": "Reports - Sales Engagement",
        "label": "Reports",
        "workspace": "Reports",
        "icon": "bar-chart",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/reports.svg",
        "idx": 6,
    },
    {
        "name": "Settings - Sales Engagement",
        "label": "Settings",
        "workspace": "Settings",
        "icon": "setting",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/settings.svg",
        "idx": 7,
    },
]


# Legacy exported standard records from the broken implementation.  These must
# be removed before the maintained non-standard records are recreated.
LEGACY_RECORD_NAMES = (
    PARENT_LABEL,
    "Prospecting",
    "Signals",
    "Touchpoints",
    "Assets",
    "CRM Conversion",
    "Reports",
    "Settings",
)


def after_migrate() -> None:
    """Create/update desktop launcher records after Frappe orphan cleanup."""

    remove_legacy_standard_records()
    ensure_desktop_icons()


def remove_legacy_standard_records() -> None:
    """Remove app-owned standard records that Frappe cleanup can treat as orphans."""

    for doctype in ("Desktop Icon", "Workspace Sidebar"):
        if not frappe.db.exists("DocType", doctype):
            continue

        for name in LEGACY_RECORD_NAMES:
            if not frappe.db.exists(doctype, name):
                continue

            doc_app = frappe.db.get_value(doctype, name, "app")
            if doc_app == APP_NAME:
                frappe.delete_doc(doctype, name, ignore_permissions=True, force=True)


def ensure_desktop_icons() -> None:
    parent = upsert_doc(
        "Desktop Icon",
        PARENT_LABEL,
        {
            "label": PARENT_LABEL,
            "icon_type": "App",
            "link_type": "External",
            "link": "/app/sales-engagement-and-intelligence",
            "link_to": None,
            "parent_icon": None,
            "app": APP_NAME,
            "icon": "broadcast",
            "logo_url": "/assets/sales_engagement_intelligence/desktop_icons/app.svg",
            "bg_color": COLOR,
            "hidden": 0,
            "standard": 0,
            "restrict_removal": 0,
            "idx": 20,
        },
    )

    child_docs = []
    for child in CHILDREN:
        upsert_workspace_sidebar(child)
        child_docs.append(upsert_desktop_child(child))

    frappe.db.commit()
    update_desktop_layouts(parent, child_docs)
    frappe.db.commit()
    clear_desktop_cache()


def upsert_workspace_sidebar(child: dict) -> Document:
    doc = upsert_doc(
        "Workspace Sidebar",
        child["name"],
        {
            "title": child["label"],
            "app": APP_NAME,
            "header_icon": child["icon"],
            "standard": 0,
            "idx": child["idx"],
        },
    )
    doc.set("items", [])
    doc.append(
        "items",
        {
            "type": "Link",
            "label": "Home",
            "link_type": "Workspace",
            "link_to": child["workspace"],
            "icon": "home",
            "collapsible": 1,
            "show_arrow": 0,
            "indent": 0,
            "child": 0,
            "keep_closed": 0,
        },
    )
    doc.save(ignore_permissions=True)
    return doc


def upsert_desktop_child(child: dict) -> Document:
    return upsert_doc(
        "Desktop Icon",
        child["name"],
        {
            "label": child["label"],
            "icon_type": "Link",
            "link_type": "Workspace Sidebar",
            "link_to": child["name"],
            "link": None,
            "parent_icon": PARENT_LABEL,
            "app": APP_NAME,
            "icon": child["icon"],
            "logo_url": child["logo"],
            "bg_color": COLOR,
            "hidden": 0,
            "standard": 0,
            "restrict_removal": 0,
            "idx": child["idx"],
        },
    )


def upsert_doc(doctype: str, name: str, values: dict) -> Document:
    if frappe.db.exists(doctype, name):
        doc = frappe.get_doc(doctype, name)
    else:
        doc = frappe.new_doc(doctype)
        doc.name = name

    for field, value in values.items():
        setattr(doc, field, value)

    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)

    return doc


def update_desktop_layouts(parent, children: list) -> None:
    labels = {PARENT_LABEL, *(child["label"] for child in CHILDREN)}
    names = {PARENT_LABEL, *(child["name"] for child in CHILDREN)}
    parent_item = layout_item(parent)
    parent_item["hidden"] = 0
    parent_item["child_icons"] = [layout_item(child) for child in children]

    for layout_name in frappe.get_all("Desktop Layout", pluck="name"):
        layout_doc = frappe.get_doc("Desktop Layout", layout_name)
        try:
            layout = json.loads(layout_doc.layout or "[]")
        except Exception:
            layout = []
        if not isinstance(layout, list):
            layout = []

        filtered = [
            item
            for item in layout
            if item.get("label") not in labels and item.get("name") not in names
        ]
        filtered.append(parent_item)
        filtered.extend(parent_item["child_icons"])
        layout_doc.layout = json.dumps(filtered)
        layout_doc.save(ignore_permissions=True)


def layout_item(doc) -> dict:
    fields = [
        "name",
        "label",
        "bg_color",
        "link",
        "link_type",
        "app",
        "icon_type",
        "parent_icon",
        "icon",
        "link_to",
        "idx",
        "standard",
        "logo_url",
        "hidden",
        "restrict_removal",
        "icon_image",
    ]
    item = {field: getattr(doc, field, None) for field in fields}
    item["child_icons"] = []
    item["in_folder"] = bool(item.get("parent_icon"))
    return item


def clear_desktop_cache() -> None:
    for user in frappe.get_all("Desktop Layout", pluck="name"):
        frappe.clear_cache(user=user)
    frappe.clear_cache()
