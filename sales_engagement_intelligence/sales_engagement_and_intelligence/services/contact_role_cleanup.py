from __future__ import annotations

import frappe

CANONICAL_NAMES = {
    "account lead": "Account Lead",
    "advisor": "Advisor",
    "Agency owner": "Agency Owner",
    "consultant": "Consultant",
    "delivery lead": "Delivery Lead",
    "department head": "Department Head",
    "designer": "Designer",
    "engineering lead": "Engineering Lead",
    "engineering manager": "Engineering Manager",
    "fractional CTO": "Fractional CTO",
    "hiring manager": "Hiring Manager",
    "MSP owner": "MSP Owner",
    "operations lead": "Operations Lead",
    "operations owner": "Operations Owner",
    "owner": "Owner",
    "product lead": "Product Lead",
    "product owner": "Product Owner",
    "technical lead": "Technical Lead",
}


def _ensure_role(name: str) -> None:
    if not frappe.db.exists("SEI Contact Role", name):
        frappe.get_doc({"doctype": "SEI Contact Role", "role_name": name, "active": 1}).insert(
            ignore_permissions=True
        )


def execute() -> dict:
    for name in ("Founder", "Operator", "Innovation Lead", "AI Lead"):
        _ensure_role(name)

    frappe.db.set_value(
        "SEI Prospect Contact",
        {"contact_role": "Founder / Operator"},
        "contact_role",
        "Founder",
        update_modified=False,
    )
    frappe.db.set_value(
        "SEI Playbook Contact Role",
        {"contact_role": "Founder / Operator"},
        "contact_role",
        "Founder",
        update_modified=False,
    )

    for parent in frappe.get_all(
        "SEI Playbook Contact Role", filters={"contact_role": "Founder"}, pluck="parent"
    ):
        if not frappe.db.exists(
            "SEI Playbook Contact Role", {"parent": parent, "contact_role": "Operator"}
        ):
            playbook = frappe.get_doc("SEI Playbook", parent)
            playbook.append("contact_roles", {"contact_role": "Operator"})
            playbook.save(ignore_permissions=True)

    for composite in ("Founder / Operator", "Innovation / AI Lead"):
        if frappe.db.exists("SEI Contact Role", composite):
            frappe.delete_doc("SEI Contact Role", composite, ignore_permissions=True, force=True)

    renamed = []
    for old, new in CANONICAL_NAMES.items():
        if frappe.db.exists("SEI Contact Role", old):
            frappe.rename_doc("SEI Contact Role", old, new, force=True)
            renamed.append((old, new))

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
        prospect_signal_type_sync,
    )

    prospect_signal_type_sync.sync_all_prospect_signal_types()
    frappe.db.commit()
    return {"renamed": renamed}
