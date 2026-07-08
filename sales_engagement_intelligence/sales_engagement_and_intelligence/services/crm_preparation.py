from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
    get_primary_signal,
)


def _has_field(doctype: str, fieldname: str) -> bool:
    return frappe.get_meta(doctype).has_field(fieldname)


def _set_if_exists(payload: dict, doctype: str, fieldname: str, value):
    if value and _has_field(doctype, fieldname):
        payload[fieldname] = value


def _domain(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = (parsed.hostname or "").lower().strip(".")
    return host[4:] if host.startswith("www.") else host or None


def validate_crm_conversion_eligibility(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    reasons = []

    if prospect.qualification_status not in ("Qualified", "Manually Approved"):
        reasons.append("Prospect is not Qualified or Manually Approved.")
    if prospect.do_not_contact:
        reasons.append("Prospect is marked Do Not Contact.")
    if prospect.lifecycle_status in ("Rejected", "Do Not Contact"):
        reasons.append(f"Prospect lifecycle is {prospect.lifecycle_status}.")
    if prospect.crm_lead:
        reasons.append("Prospect is already linked to a CRM Lead; use Sync SEI Context instead.")
    has_identity = prospect.prospect_name and (
        prospect.website or prospect.primary_contact_email or prospect.source_url
    )
    if not has_identity:
        reasons.append("Prospect is missing enough identity information for CRM preparation.")

    duplicates = find_possible_crm_lead_duplicates(prospect)
    if duplicates:
        reasons.append(
            "Possible existing CRM Lead duplicate found; link it manually or resolve before creation."
        )

    return {"eligible": not reasons, "reasons": reasons, "duplicates": duplicates}


def find_possible_crm_lead_duplicates(prospect) -> list[dict]:
    if not frappe.db.exists("DocType", "CRM Lead"):
        return []

    matches = []
    fields = ["name"]
    for field in ("lead_name", "organization", "email", "website", "sei_prospect"):
        if _has_field("CRM Lead", field):
            fields.append(field)

    if _has_field("CRM Lead", "sei_prospect"):
        for row in frappe.get_all(
            "CRM Lead",
            filters={"sei_prospect": prospect.name},
            fields=fields,
            limit=5,
        ):
            matches.append(row)

    if prospect.primary_contact_email and _has_field("CRM Lead", "email"):
        for row in frappe.get_all(
            "CRM Lead",
            filters={"email": prospect.primary_contact_email},
            fields=fields,
            limit=5,
        ):
            if row.name not in [m.name for m in matches]:
                matches.append(row)

    if prospect.website and _has_field("CRM Lead", "website"):
        for row in frappe.get_all("CRM Lead", filters={"website": prospect.website}, fields=fields, limit=5):
            if row.name not in [m.name for m in matches]:
                matches.append(row)

    return matches


def build_crm_lead_payload(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    lead = {"doctype": "CRM Lead"}

    title = prospect.primary_contact_name or prospect.prospect_name or prospect.name
    for field in ("lead_name", "first_name", "organization", "company_name", "title"):
        _set_if_exists(lead, "CRM Lead", field, title)

    _set_if_exists(lead, "CRM Lead", "email", prospect.primary_contact_email)
    _set_if_exists(lead, "CRM Lead", "website", prospect.website)
    # Native CRM Lead Source is a Link field; keep source_arena in SEI-owned fields
    # unless explicitly mapped later.
    _set_if_exists(lead, "CRM Lead", "status", "New")

    _set_if_exists(lead, "CRM Lead", "sei_prospect", prospect.name)
    _set_if_exists(lead, "CRM Lead", "sei_source_arena", prospect.source_arena)
    _set_if_exists(lead, "CRM Lead", "sei_thesis", prospect.thesis)
    _set_if_exists(
        lead,
        "CRM Lead",
        "sei_qualification_summary",
        prospect.qualification_explanation or prospect.signal_summary,
    )

    return lead


def build_crm_organization_payload(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    payload = {"doctype": "CRM Organization"}
    _set_if_exists(payload, "CRM Organization", "organization_name", prospect.prospect_name)
    _set_if_exists(payload, "CRM Organization", "website", prospect.website)
    return payload


def build_crm_contact_payload(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    payload = {"doctype": "CRM Contacts"}
    _set_if_exists(payload, "CRM Contacts", "full_name", prospect.primary_contact_name)
    _set_if_exists(payload, "CRM Contacts", "email", prospect.primary_contact_email)
    # CRM Contacts has no native URL field in the inspected Frappe CRM schema.
    return payload


def build_crm_deal_payload(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    payload = {"doctype": "CRM Deal"}
    _set_if_exists(payload, "CRM Deal", "lead_name", prospect.prospect_name)
    _set_if_exists(payload, "CRM Deal", "organization_name", prospect.prospect_name)
    _set_if_exists(payload, "CRM Deal", "sei_prospect", prospect.name)
    _set_if_exists(payload, "CRM Deal", "sei_source_arena", prospect.source_arena)
    _set_if_exists(payload, "CRM Deal", "sei_thesis", prospect.thesis)
    _set_if_exists(payload, "CRM Deal", "sei_primary_signal", get_primary_signal(prospect.name))
    return payload


def sync_sei_context_to_crm(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    result = {"crm_lead_synced": False, "crm_deal_synced": False}

    if prospect.crm_lead:
        values = {}
        for field, value in {
            "sei_prospect": prospect.name,
            "sei_source_arena": prospect.source_arena,
            "sei_thesis": prospect.thesis,
            "sei_qualification_summary": prospect.qualification_explanation or prospect.signal_summary,
        }.items():
            if _has_field("CRM Lead", field):
                values[field] = value
        if values:
            frappe.db.set_value("CRM Lead", prospect.crm_lead, values, update_modified=True)
            result["crm_lead_synced"] = True

    if prospect.crm_deal:
        values = {}
        for field, value in {
            "sei_prospect": prospect.name,
            "sei_source_arena": prospect.source_arena,
            "sei_thesis": prospect.thesis,
            "sei_primary_signal": get_primary_signal(prospect.name),
        }.items():
            if _has_field("CRM Deal", field):
                values[field] = value
        if values:
            frappe.db.set_value("CRM Deal", prospect.crm_deal, values, update_modified=True)
            result["crm_deal_synced"] = True

    return result


def create_crm_lead_from_prospect(prospect_name: str) -> dict:
    eligibility = validate_crm_conversion_eligibility(prospect_name)
    if not eligibility["eligible"]:
        frappe.throw("CRM Lead cannot be created: " + "; ".join(eligibility["reasons"]))

    payload = build_crm_lead_payload(prospect_name)
    lead = frappe.get_doc(payload)
    lead.insert()

    frappe.db.set_value(
        "SEI Prospect",
        prospect_name,
        {
            "crm_lead": lead.name,
            "lifecycle_status": "Converted to CRM Lead",
            "ready_for_crm_conversion": 0,
        },
        update_modified=True,
    )
    return {"crm_lead": lead.name, "lifecycle_status": "Converted to CRM Lead"}
