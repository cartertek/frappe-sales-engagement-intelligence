from __future__ import annotations

from typing import Optional

import frappe
from frappe.model.document import Document

QUALIFYING_STRENGTHS = ("Moderate", "Strong")
TERMINAL_STATUSES = ("Rejected", "Do Not Contact")


def _has_value(value) -> bool:
    return bool(str(value or "").strip())


def is_evidence_valid_for_qualification(signal: dict) -> bool:
    """Return whether a signal has enough structured evidence to count."""
    if signal.get("signal_strength") not in QUALIFYING_STRENGTHS:
        return False
    if signal.get("evidence_basis") != "Observed":
        return False
    if signal.get("exclude_from_qualification") or signal.get("is_strength_capped"):
        return False
    return all(
        _has_value(signal.get(fieldname))
        for fieldname in (
            "observed_fact",
            "signal_claim",
            "why_this_signal_type",
            "why_not_weak",
            "disqualifiers_checked",
        )
    )


def _signal_filters(prospect_name: str) -> dict:
    return {
        "prospect": prospect_name,
        "exclude_from_qualification": 0,
        "evidence_basis": "Observed",
        "signal_strength": ["in", QUALIFYING_STRENGTHS],
        "is_strength_capped": 0,
    }


def get_qualifying_signals(prospect_name: str) -> list[dict]:
    """Return observed Moderate/Strong signals that are not excluded from qualification."""
    if not prospect_name:
        return []

    rows = frappe.get_all(
        "SEI Signal",
        filters=_signal_filters(prospect_name),
        fields=[
            "name",
            "signal_strength",
            "evidence_basis",
            "exclude_from_qualification",
            "is_strength_capped",
            "observed_fact",
            "signal_claim",
            "why_this_signal_type",
            "why_not_weak",
            "disqualifiers_checked",
            "source_date",
            "creation",
        ],
        order_by="source_date desc, creation desc",
    )
    return [signal for signal in rows if is_evidence_valid_for_qualification(signal)]


def get_primary_signal(prospect_name: str) -> Optional[str]:
    """Select a deterministic primary signal for CRM context."""
    if not prospect_name:
        return None

    precedence = [
        {**_signal_filters(prospect_name), "signal_strength": "Strong"},
        {**_signal_filters(prospect_name), "signal_strength": "Moderate"},
        {"prospect": prospect_name, "evidence_basis": "Observed"},
        {"prospect": prospect_name},
    ]

    for filters in precedence:
        signal = frappe.get_all(
            "SEI Signal",
            filters=filters,
            fields=["name"],
            order_by="source_date desc, creation desc",
            limit=1,
        )
        if signal:
            return signal[0].name
    return None


def calculate_prospect_qualification_for_doc(prospect: Document) -> dict:
    strong_count = 0
    moderate_count = 0
    qualified_signals = []

    if prospect.name and not prospect.do_not_contact and prospect.lifecycle_status != "Rejected":
        qualified_signals = get_qualifying_signals(prospect.name)
        strong_count = sum(1 for signal in qualified_signals if signal.signal_strength == "Strong")
        moderate_count = sum(1 for signal in qualified_signals if signal.signal_strength == "Moderate")

    qualified_count = strong_count + moderate_count
    primary_signal = get_primary_signal(prospect.name) if prospect.name else None

    if prospect.do_not_contact:
        status = "Do Not Contact"
        explanation = "Prospect is marked Do Not Contact."
    elif prospect.lifecycle_status == "Rejected" or prospect.qualification_status == "Rejected":
        status = "Rejected"
        explanation = "Prospect is rejected and will not be automatically re-qualified."
    elif prospect.manual_qualification_override:
        if not prospect.manual_qualification_reason:
            frappe.throw(
                "Manual Qualification Reason is required when Manual Qualification Override is checked."
            )
        status = "Manually Approved"
        explanation = f"Manually approved: {prospect.manual_qualification_reason}"
    elif strong_count >= 1:
        status = "Qualified"
        explanation = "Qualified by 1 strong observed signal."
    elif moderate_count >= 2:
        status = "Qualified"
        explanation = f"Qualified by {moderate_count} moderate observed signals."
    elif qualified_count == 1:
        status = "Needs Review"
        explanation = "Needs review: only 1 moderate observed qualifying signal."
    else:
        status = "Unqualified"
        explanation = "No strong observed signal or 2 moderate observed qualifying signals found."

    return {
        "qualification_status": status,
        "strong_observed_signal_count": strong_count,
        "moderate_observed_signal_count": moderate_count,
        "qualified_signal_count": qualified_count,
        "primary_signal": primary_signal,
        "qualification_explanation": explanation,
    }


def calculate_prospect_qualification(prospect_name: str) -> dict:
    return calculate_prospect_qualification_for_doc(frappe.get_doc("SEI Prospect", prospect_name))


def apply_qualification_to_doc(prospect: Document) -> dict:
    result = calculate_prospect_qualification_for_doc(prospect)
    for field in (
        "qualification_status",
        "strong_observed_signal_count",
        "moderate_observed_signal_count",
        "qualified_signal_count",
        "qualification_explanation",
    ):
        prospect.set(field, result[field])
    return result


def apply_qualification_result(prospect_name: str) -> dict:
    result = calculate_prospect_qualification(prospect_name)
    frappe.db.set_value(
        "SEI Prospect",
        prospect_name,
        {
            "qualification_status": result["qualification_status"],
            "strong_observed_signal_count": result["strong_observed_signal_count"],
            "moderate_observed_signal_count": result["moderate_observed_signal_count"],
            "qualified_signal_count": result["qualified_signal_count"],
            "qualification_explanation": result["qualification_explanation"],
        },
        update_modified=True,
    )
    frappe.get_doc("SEI Prospect", prospect_name).notify_update()
    return result
