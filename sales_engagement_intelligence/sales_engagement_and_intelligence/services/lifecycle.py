from __future__ import annotations

from typing import Optional

import frappe
from frappe.model.document import Document

TERMINAL_STATUSES = (
    "Rejected",
    "Do Not Contact",
    "Converted to CRM Lead",
    "Converted to CRM Deal",
)


def is_terminal_status(status: str) -> bool:
    return status in TERMINAL_STATUSES


def has_contact_path(prospect: Document) -> bool:
    return bool(
        prospect.get("primary_contact_email")
        or prospect.get("primary_contact_url")
        or prospect.get("primary_contact_name")
    )


def has_company_identity(prospect: Document) -> bool:
    return bool(prospect.get("prospect_name") or prospect.get("website") or prospect.get("source_url"))


def has_crm_link(prospect: Document) -> bool:
    return bool(prospect.get("crm_lead") or prospect.get("crm_deal"))


def suggest_lifecycle_status(prospect_name: str) -> str:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)

    if prospect.do_not_contact:
        return "Do Not Contact"
    if prospect.crm_deal:
        return "Converted to CRM Deal"
    if prospect.crm_lead:
        return "Converted to CRM Lead"
    if is_terminal_status(prospect.lifecycle_status):
        return prospect.lifecycle_status

    if prospect.qualification_status in ("Qualified", "Manually Approved"):
        if has_contact_path(prospect) or has_company_identity(prospect):
            return "Ready for CRM Conversion"
        return "Find Contact"

    if prospect.qualification_status == "Needs Review":
        return "Research Complete"

    if prospect.get("last_researched_date") or prospect.get("signal_summary"):
        return "Research Complete"

    return prospect.lifecycle_status or "New"


def apply_lifecycle_status(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    old_status = prospect.lifecycle_status
    new_status = suggest_lifecycle_status(prospect_name)

    if old_status != new_status:
        frappe.db.set_value(
            "SEI Prospect",
            prospect_name,
            "lifecycle_status",
            new_status,
            update_modified=True,
        )

    return {"old_lifecycle_status": old_status, "lifecycle_status": new_status}


def mark_rejected(prospect_name: str, reason: Optional[str] = None) -> dict:
    values = {
        "lifecycle_status": "Rejected",
        "qualification_status": "Rejected",
        "ready_for_crm_conversion": 0,
    }
    if reason:
        values["rejected_reason"] = reason
    frappe.db.set_value("SEI Prospect", prospect_name, values, update_modified=True)
    return {"lifecycle_status": "Rejected", "qualification_status": "Rejected"}


def mark_do_not_contact(prospect_name: str, reason: Optional[str] = None) -> dict:
    values = {
        "do_not_contact": 1,
        "lifecycle_status": "Do Not Contact",
        "qualification_status": "Do Not Contact",
        "ready_for_crm_conversion": 0,
    }
    if reason:
        values["rejected_reason"] = reason
    frappe.db.set_value("SEI Prospect", prospect_name, values, update_modified=True)
    return {
        "do_not_contact": 1,
        "lifecycle_status": "Do Not Contact",
        "qualification_status": "Do Not Contact",
    }


def reopen_prospect(prospect_name: str) -> dict:
    roles = frappe.get_roles()
    has_manager_access = (
        frappe.session.user == "Administrator"
        or "Administrator" in roles
        or "Sales Engagement Manager" in roles
    )
    if not has_manager_access:
        frappe.throw(
            "Only an Administrator or Sales Engagement Manager can reopen a protected prospect."
        )

    frappe.db.set_value(
        "SEI Prospect",
        prospect_name,
        {
            "do_not_contact": 0,
            "lifecycle_status": "New",
            "qualification_status": "Unqualified",
            "ready_for_crm_conversion": 0,
        },
        update_modified=True,
    )

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    qualification = apply_qualification_result(prospect_name)
    lifecycle = apply_lifecycle_status(prospect_name)
    return {**qualification, **lifecycle}


def mark_ready_for_crm_conversion(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    if prospect.do_not_contact or prospect.lifecycle_status in ("Rejected", "Do Not Contact"):
        frappe.throw("Do Not Contact or Rejected prospects cannot be marked ready for CRM conversion.")
    if prospect.qualification_status not in ("Qualified", "Manually Approved"):
        frappe.throw("Only Qualified or Manually Approved prospects can be marked ready for CRM conversion.")

    frappe.db.set_value(
        "SEI Prospect",
        prospect_name,
        {
            "ready_for_crm_conversion": 1,
            "lifecycle_status": "Ready for CRM Conversion",
        },
        update_modified=True,
    )
    return {"ready_for_crm_conversion": 1, "lifecycle_status": "Ready for CRM Conversion"}
