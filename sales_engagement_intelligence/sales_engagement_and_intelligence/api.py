from __future__ import annotations

import json
from typing import Optional

import frappe


def _check_prospect_permission(prospect: str, ptype: str = "write"):
    doc = frappe.get_doc("SEI Prospect", prospect)
    if not doc.has_permission(ptype):
        frappe.throw(f"Not permitted to {ptype} SEI Prospect {prospect}.")
    return doc


def _has_manager_access():
    roles = frappe.get_roles()
    return (
        frappe.session.user == "Administrator"
        or "Administrator" in roles
        or "Sales Engagement Manager" in roles
    )


def _require_manager():
    if not _has_manager_access():
        frappe.throw("Administrator or Sales Engagement Manager role is required for this action.")


def _parse_options(options: Optional[str | dict]) -> dict:
    if not options:
        return {}
    if isinstance(options, dict):
        return options
    return json.loads(options)


@frappe.whitelist()
def recalculate_qualification(prospect: str) -> dict:
    _check_prospect_permission(prospect)
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    return apply_qualification_result(prospect)


@frappe.whitelist()
def apply_lifecycle_suggestion(prospect: str) -> dict:
    _check_prospect_permission(prospect)
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
    )

    return apply_lifecycle_status(prospect)


@frappe.whitelist()
def mark_ready_for_crm_conversion(prospect: str) -> dict:
    _check_prospect_permission(prospect)
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        mark_ready_for_crm_conversion,
    )

    return mark_ready_for_crm_conversion(prospect)


@frappe.whitelist()
def preview_crm_lead(prospect: str) -> dict:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        build_crm_lead_payload,
        find_possible_crm_duplicates,
        validate_crm_conversion_eligibility,
    )

    return {
        "eligibility": validate_crm_conversion_eligibility(prospect),
        "duplicates": find_possible_crm_duplicates(prospect),
        "payload": build_crm_lead_payload(prospect),
    }


@frappe.whitelist()
def preview_crm_conversion(prospect: str) -> dict:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        build_crm_contact_payload,
        build_crm_deal_payload,
        build_crm_lead_payload,
        build_crm_organization_payload,
        find_possible_crm_duplicates,
        validate_crm_conversion_eligibility,
    )

    return {
        "eligibility": validate_crm_conversion_eligibility(prospect),
        "duplicates": find_possible_crm_duplicates(prospect),
        "payloads": {
            "crm_lead": build_crm_lead_payload(prospect),
            "crm_organization": build_crm_organization_payload(prospect),
            "crm_contact": build_crm_contact_payload(prospect),
            "crm_deal": build_crm_deal_payload(prospect),
        },
    }


@frappe.whitelist()
def find_crm_duplicates(prospect: str) -> dict:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        find_possible_crm_duplicates,
    )

    return find_possible_crm_duplicates(prospect)


@frappe.whitelist()
def sync_sei_context_to_crm(prospect: str) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        sync_sei_context_to_crm,
    )

    return sync_sei_context_to_crm(prospect)


@frappe.whitelist()
def mark_rejected(prospect: str, reason: Optional[str] = None) -> dict:
    _check_prospect_permission(prospect)
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        mark_rejected,
    )

    return mark_rejected(prospect, reason)


@frappe.whitelist()
def mark_do_not_contact(prospect: str, reason: Optional[str] = None) -> dict:
    _check_prospect_permission(prospect)
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        mark_do_not_contact,
    )

    return mark_do_not_contact(prospect, reason)


@frappe.whitelist()
def reopen_prospect(prospect: str) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        reopen_prospect,
    )

    return reopen_prospect(prospect)


@frappe.whitelist()
def create_crm_lead(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_crm_lead_from_prospect,
    )

    return create_crm_lead_from_prospect(prospect, _parse_options(options))


@frappe.whitelist()
def create_or_link_crm_organization(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_or_link_crm_organization,
    )

    return create_or_link_crm_organization(prospect, _parse_options(options))


@frappe.whitelist()
def create_or_link_crm_contact(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_or_link_crm_contact,
    )

    return create_or_link_crm_contact(prospect, _parse_options(options))


@frappe.whitelist()
def create_crm_deal(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_crm_deal_from_prospect,
    )

    return create_crm_deal_from_prospect(prospect, _parse_options(options))


@frappe.whitelist()
def link_existing_crm_record(prospect: str, doctype: str, record_name: str) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        link_existing_crm_record,
    )

    return link_existing_crm_record(prospect, doctype, record_name)
