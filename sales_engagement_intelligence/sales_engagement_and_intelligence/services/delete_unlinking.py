from __future__ import annotations

from collections.abc import Iterable

import frappe

REFERENCE_FIELDS: dict[str, tuple[tuple[str, str], ...]] = {
    "SEI Prospect": (
        ("CRM Lead", "sei_prospect"),
        ("CRM Deal", "sei_prospect"),
        ("SEI Signal", "prospect"),
        ("SEI Interaction Attribution", "prospect"),
        ("SEI Import Batch Row", "prospect"),
        ("SEI Import Batch Row", "matched_existing_prospect"),
    ),
    "SEI Signal": (
        ("CRM Deal", "sei_primary_signal"),
        ("SEI Interaction Attribution", "signal"),
        ("SEI Import Batch Row", "signal"),
        ("SEI Signal Disqualifier Check", "signal"),
        ("SEI Signal Type Feedback", "source_signal"),
    ),
    "CRM Deal": (
        ("SEI Prospect", "crm_deal"),
        ("SEI Interaction Attribution", "crm_deal"),
    ),
}


def unlink_references_before_delete(doc, method: str | None = None) -> None:
    """Clear SEI-owned links to a record before Frappe validates deletion links."""

    del method
    if doc.doctype == "CRM Deal":
        doc.flags.sei_affected_prospects = _linked_prospects_for_deal(doc)

    for reference_doctype, fieldname in REFERENCE_FIELDS.get(doc.doctype, ()):
        _clear_link_values(reference_doctype, fieldname, doc.name)


def restore_prospect_lifecycle_after_deal_delete(doc, method: str | None = None) -> None:
    """Remove stale Converted-to-Deal lifecycle states after a CRM Deal is deleted."""

    del method
    prospects: Iterable[str] = getattr(doc.flags, "sei_affected_prospects", ()) or ()
    for prospect_name in prospects:
        if not frappe.db.exists("SEI Prospect", prospect_name):
            continue
        prospect = frappe.get_doc("SEI Prospect", prospect_name)
        if prospect.lifecycle_status != "Converted to CRM Deal":
            continue

        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
            suggest_pre_crm_handoff_status,
        )

        lifecycle_status = (
            "Converted to CRM Lead"
            if prospect.crm_lead
            else suggest_pre_crm_handoff_status(prospect)
        )
        frappe.db.set_value(
            "SEI Prospect",
            prospect_name,
            {
                "lifecycle_status": lifecycle_status,
                "ready_for_crm_conversion": 0,
            },
            update_modified=True,
        )
        frappe.get_doc("SEI Prospect", prospect_name).notify_update()


def _linked_prospects_for_deal(doc) -> tuple[str, ...]:
    prospects = set()
    if getattr(doc, "sei_prospect", None):
        prospects.add(doc.sei_prospect)

    if _field_available("SEI Prospect", "crm_deal"):
        prospects.update(
            frappe.get_all(
                "SEI Prospect",
                filters={"crm_deal": doc.name},
                pluck="name",
            )
        )
    return tuple(sorted(prospects))


def _clear_link_values(doctype: str, fieldname: str, target_name: str) -> None:
    if not _field_available(doctype, fieldname):
        return

    for name in frappe.get_all(doctype, filters={fieldname: target_name}, pluck="name"):
        frappe.db.set_value(
            doctype,
            name,
            fieldname,
            None,
            update_modified=False,
        )


def _field_available(doctype: str, fieldname: str) -> bool:
    return frappe.db.table_exists(doctype) and frappe.db.has_column(doctype, fieldname)
