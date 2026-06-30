"""Desktop launcher setup for Sales Engagement and Intelligence."""

import json

import frappe
from frappe.model.document import Document

APP_NAME = "sales_engagement_intelligence"
PARENT_LABEL = "Sales Engagement and Intelligence"
COLOR = "gray"

CHILDREN = [
    {
        "label": "SEI Prospecting",
        "workspace": "SEI Prospecting",
        "icon": "search",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_prospecting.svg",
        "idx": 1,
    },
    {
        "label": "SEI Signals",
        "workspace": "SEI Signals",
        "icon": "chart",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_signals.svg",
        "idx": 2,
    },
    {
        "label": "SEI Touchpoints",
        "workspace": "SEI Touchpoints",
        "icon": "mail",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_touchpoints.svg",
        "idx": 3,
    },
    {
        "label": "SEI Assets",
        "workspace": "SEI Assets",
        "icon": "folder",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_assets.svg",
        "idx": 4,
    },
    {
        "label": "SEI CRM Conversion",
        "workspace": "SEI CRM Conversion",
        "icon": "arrow-right",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_crm_conversion.svg",
        "idx": 5,
    },
    {
        "label": "SEI Reports",
        "workspace": "SEI Reports",
        "icon": "bar-chart",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_reports.svg",
        "idx": 6,
    },
    {
        "label": "SEI Settings",
        "workspace": "SEI Settings",
        "icon": "setting",
        "logo": "/assets/sales_engagement_intelligence/desktop_icons/sei_settings.svg",
        "idx": 7,
    },
]


def after_migrate() -> None:
    """Create/update SEI desktop launcher records after Frappe orphan cleanup."""

    ensure_desktop_icons()


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
            "logo_url": "/assets/sales_engagement_intelligence/desktop_icons/sei_app.svg",
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
        child["label"],
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
        child["label"],
        {
            "label": child["label"],
            "icon_type": "Link",
            "link_type": "Workspace Sidebar",
            "link_to": child["label"],
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
            if item.get("label") not in labels and item.get("name") not in labels
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
