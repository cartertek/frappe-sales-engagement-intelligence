from __future__ import annotations

from typing import Optional

import frappe
from frappe.model.document import Document

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
    contact_role_requirements,
    emails,
    primary_contacts,
)

TERMINAL_STATUSES = (
    "Rejected",
    "Do Not Contact",
    "Converted to CRM Lead",
    "Converted to CRM Deal",
)


def is_terminal_status(status: str) -> bool:
    return status in TERMINAL_STATUSES


def has_contact_path(prospect: Document) -> bool:
    role_requirements = {
        role.casefold(): signal_specific
        for role, signal_specific in contact_role_requirements(prospect).items()
    }
    return any(
        emails(contact)
        and (contact.get("contact_role") or "").casefold() in role_requirements
        and (
            not role_requirements[(contact.get("contact_role") or "").casefold()]
            or bool((contact.get("signal_relevance") or "").strip())
        )
        for contact in primary_contacts(prospect)
    )


def has_company_identity(prospect: Document) -> bool:
    return bool(prospect.get("prospect_name") or prospect.get("website") or prospect.get("source_url"))


def has_crm_link(prospect: Document) -> bool:
    return bool(prospect.get("crm_lead") or prospect.get("crm_deal"))


def has_signals(prospect: Document) -> bool:
    prospect_name = prospect.get("name")
    return bool(prospect_name and frappe.db.exists("SEI Signal", {"prospect": prospect_name}))


def has_research_evidence(prospect: Document) -> bool:
    return bool(
        prospect.get("last_researched_date") or prospect.get("signal_summary") or has_signals(prospect)
    )


def suggest_lifecycle_status(prospect_name: str) -> str:
    return suggest_lifecycle_status_for_doc(frappe.get_doc("SEI Prospect", prospect_name))


def suggest_lifecycle_status_for_doc(prospect: Document) -> str:
    if prospect.do_not_contact:
        return "Do Not Contact"
    if prospect.crm_deal:
        return "Converted to CRM Deal"
    if prospect.crm_lead:
        return "Converted to CRM Lead"
    if is_terminal_status(prospect.lifecycle_status):
        return prospect.lifecycle_status

    if prospect.qualification_status == "Rejected":
        return "Rejected"

    if prospect.qualification_status in ("Qualified", "Manually Approved"):
        if prospect.lifecycle_status == "Find Contact":
            if has_contact_path(prospect):
                return "Ready for CRM Conversion"
            return "Find Contact"
        if prospect.lifecycle_status == "Ready for CRM Conversion":
            return "Ready for CRM Conversion" if has_contact_path(prospect) else "Find Contact"
        return "Qualified"

    if prospect.qualification_status == "Needs Review":
        return "Research Complete"

    if prospect.qualification_status in ("Unqualified", None, ""):
        if prospect.lifecycle_status == "Research Complete":
            return "Rejected"
        if prospect.lifecycle_status in ("New", "Needs Research"):
            return prospect.lifecycle_status or "Needs Research"
        if has_research_evidence(prospect):
            return "Rejected"
        return "Needs Research"

    if has_research_evidence(prospect):
        return "Research Complete"

    return prospect.lifecycle_status or "Needs Research"


def apply_lifecycle_to_doc(prospect: Document) -> dict:
    old_status = prospect.lifecycle_status
    new_status = suggest_lifecycle_status_for_doc(prospect)
    if old_status != new_status:
        prospect.lifecycle_status = new_status
    if new_status == "Rejected":
        prospect.qualification_status = "Rejected"
    return {"old_lifecycle_status": old_status, "lifecycle_status": new_status}


def apply_lifecycle_status(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    old_status = prospect.lifecycle_status
    new_status = suggest_lifecycle_status_for_doc(prospect)

    if old_status != new_status:
        values = {"lifecycle_status": new_status}
        if new_status == "Rejected":
            values.update({"qualification_status": "Rejected"})
        frappe.db.set_value(
            "SEI Prospect",
            prospect_name,
            values,
            update_modified=True,
        )
        frappe.get_doc("SEI Prospect", prospect_name).notify_update()

    return {"old_lifecycle_status": old_status, "lifecycle_status": new_status}


def mark_rejected(prospect_name: str, reason: Optional[str] = None) -> dict:
    values = {
        "lifecycle_status": "Rejected",
        "qualification_status": "Rejected",
    }
    if reason:
        values["rejected_reason"] = reason
    frappe.db.set_value("SEI Prospect", prospect_name, values, update_modified=True)
    frappe.get_doc("SEI Prospect", prospect_name).notify_update()
    return {"lifecycle_status": "Rejected", "qualification_status": "Rejected"}


def mark_do_not_contact(prospect_name: str, reason: Optional[str] = None) -> dict:
    values = {
        "do_not_contact": 1,
        "lifecycle_status": "Do Not Contact",
        "qualification_status": "Do Not Contact",
    }
    if reason:
        values["rejected_reason"] = reason
    frappe.db.set_value("SEI Prospect", prospect_name, values, update_modified=True)
    frappe.get_doc("SEI Prospect", prospect_name).notify_update()
    return {
        "do_not_contact": 1,
        "lifecycle_status": "Do Not Contact",
        "qualification_status": "Do Not Contact",
    }


def _has_manager_access() -> bool:
    roles = frappe.get_roles()
    return (
        frappe.session.user == "Administrator"
        or "Administrator" in roles
        or "Sales Engagement Manager" in roles
    )


def reopen_prospect(prospect_name: str) -> dict:
    if not _has_manager_access():
        frappe.throw("Only an Administrator or Sales Engagement Manager can reopen a protected prospect.")

    frappe.db.set_value(
        "SEI Prospect",
        prospect_name,
        {
            "do_not_contact": 0,
            "lifecycle_status": "New",
            "qualification_status": "Unqualified",
        },
        update_modified=True,
    )
    frappe.get_doc("SEI Prospect", prospect_name).notify_update()

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    qualification = apply_qualification_result(prospect_name)
    lifecycle = apply_lifecycle_status(prospect_name)
    return {**qualification, **lifecycle}


def get_crm_readiness_requirements(prospect: Document) -> list[dict]:
    return [
        {
            "key": "qualified",
            "label": "Qualification status is Qualified or Manually Approved",
            "met": prospect.qualification_status in ("Qualified", "Manually Approved"),
        },
        {
            "key": "not_do_not_contact",
            "label": "Prospect is not marked Do Not Contact",
            "met": not bool(prospect.do_not_contact),
        },
        {
            "key": "not_protected_lifecycle",
            "label": "Lifecycle status is not Rejected or Do Not Contact",
            "met": prospect.lifecycle_status not in ("Rejected", "Do Not Contact"),
        },
        {
            "key": "no_crm_lead",
            "label": "No CRM Lead has already been created",
            "met": not bool(prospect.get("crm_lead")),
        },
    ]


def suggest_pre_crm_handoff_status(prospect: Document) -> str:
    if prospect.qualification_status in ("Qualified", "Manually Approved"):
        return "Qualified"
    if prospect.qualification_status == "Needs Review":
        return "Research Complete"
    if prospect.qualification_status in ("Unqualified", None, ""):
        return "Needs Research" if has_research_evidence(prospect) else "New"
    return "New"


def mark_ready_for_crm_conversion(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    requirements = get_crm_readiness_requirements(prospect)
    unmet = [requirement for requirement in requirements if not requirement["met"]]
    if unmet:
        return {
            "ok": False,
            "error": {
                "code": "CRM_READINESS_REQUIREMENTS_NOT_MET",
                "message": "This prospect is not ready to enter the CRM handoff workflow.",
                "details": {"requirements": requirements},
            },
            "warnings": [],
        }

    lifecycle_status = "Ready for CRM Conversion" if has_contact_path(prospect) else "Find Contact"
    frappe.db.set_value(
        "SEI Prospect", prospect_name, "lifecycle_status", lifecycle_status, update_modified=True
    )
    frappe.get_doc("SEI Prospect", prospect_name).notify_update()
    return {"lifecycle_status": lifecycle_status}


def mark_not_ready_for_crm_conversion(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    if prospect.lifecycle_status not in ("Find Contact", "Ready for CRM Conversion"):
        return {
            "ok": False,
            "error": {
                "code": "CRM_HANDOFF_NOT_ACTIVE",
                "message": "This prospect is not currently in the CRM handoff workflow.",
                "details": {},
            },
            "warnings": [],
        }

    lifecycle_status = suggest_pre_crm_handoff_status(prospect)
    frappe.db.set_value(
        "SEI Prospect", prospect_name, "lifecycle_status", lifecycle_status, update_modified=True
    )
    frappe.get_doc("SEI Prospect", prospect_name).notify_update()
    return {"lifecycle_status": lifecycle_status}
