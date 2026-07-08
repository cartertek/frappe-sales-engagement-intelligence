from __future__ import annotations

from typing import Optional

import frappe


def _check_prospect_permission(prospect: str, ptype: str = 'write'):
    doc = frappe.get_doc('SEI Prospect', prospect)
    if not doc.has_permission(ptype):
        frappe.throw(f'Not permitted to {ptype} SEI Prospect {prospect}.')
    return doc


def _require_manager():
    if 'Sales Engagement Manager' not in frappe.get_roles():
        frappe.throw('Sales Engagement Manager role is required for this action.')


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
    _check_prospect_permission(prospect, 'read')
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        build_crm_lead_payload,
        validate_crm_conversion_eligibility,
    )
    return {
        'eligibility': validate_crm_conversion_eligibility(prospect),
        'payload': build_crm_lead_payload(prospect),
    }


@frappe.whitelist()
def sync_sei_context_to_crm(prospect: str) -> dict:
    _check_prospect_permission(prospect)
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
def create_crm_lead(prospect: str) -> dict:
    _check_prospect_permission(prospect)
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_crm_lead_from_prospect,
    )
    return create_crm_lead_from_prospect(prospect)
