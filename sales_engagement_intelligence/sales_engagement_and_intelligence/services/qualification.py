from __future__ import annotations

from collections import defaultdict
from typing import Optional

import frappe
from frappe.model.document import Document

from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
    signal_qualification_script,
)

TERMINAL_STATUSES = ("Rejected", "Do Not Contact")
STRUCTURED_EVIDENCE_FIELDS = (
    "signal_claim",
    "why_this_signal_type",
    "why_not_weak",
    "disqualifiers_checked",
)
SCRIPT_SIGNAL_FIELDS = (
    "name",
    "signal_type",
    "signal_strength",
    "confidence",
    "signal_claim",
    "why_this_signal_type",
    "why_not_weak",
    "disqualifiers_checked",
    "evidence_gap_reason",
    "evidence_notes",
    "review_date",
    "creation",
)


def _has_value(value) -> bool:
    return bool(str(value or "").strip())


def is_evidence_valid_for_qualification(signal: dict) -> bool:
    """Return whether a signal may be presented to its playbook qualification script."""
    if signal.get("exclude_from_qualification"):
        return False
    observed_facts = signal.get("observed_facts") or []
    has_observed_fact = any(
        _has_value(item.get("fact")) and item.get("evidence_basis") == "Observed"
        for item in observed_facts
    )
    if signal.get("signal_strength") in ("Moderate", "Strong"):
        return has_observed_fact and all(
            _has_value(signal.get(fieldname)) for fieldname in STRUCTURED_EVIDENCE_FIELDS
        )
    return has_observed_fact or _has_value(signal.get("evidence_gap_reason"))


def _signal_filters(prospect_name: str) -> dict:
    return {
        "prospect": prospect_name,
        "exclude_from_qualification": 0,
    }


def get_eligible_signals(prospect_name: str) -> list[dict]:
    """Return observed, non-excluded signals eligible for playbook qualification."""
    if not prospect_name:
        return []

    rows = frappe.get_all(
        "SEI Signal",
        filters=_signal_filters(prospect_name),
        fields=[*SCRIPT_SIGNAL_FIELDS, "exclude_from_qualification"],
        order_by="creation desc",
    )
    names = [row.name for row in rows]
    facts_by_signal = {name: [] for name in names}
    if names:
        facts = frappe.get_all(
            "SEI Signal Observed Fact",
            filters={"parent": ["in", names], "parenttype": "SEI Signal"},
            fields=[
                "parent",
                "fact",
                "evidence_basis",
                "evidence_specificity",
                "source_url",
                "source_date",
                "idx",
            ],
            order_by="parent asc, idx asc",
        )
        for fact in facts:
            facts_by_signal.setdefault(fact.parent, []).append(
                {
                    "fact": fact.fact,
                    "evidence_basis": fact.evidence_basis,
                    "evidence_specificity": fact.evidence_specificity,
                    "source_url": fact.source_url,
                    "source_date": fact.source_date,
                }
            )
    for row in rows:
        row["observed_facts"] = facts_by_signal.get(row.name, [])
    return [signal for signal in rows if is_evidence_valid_for_qualification(signal)]


def _signal_for_script(signal: dict) -> dict:
    data = {field: signal.get(field) for field in SCRIPT_SIGNAL_FIELDS}
    # `strength` is the concise public name used by qualification scripts; keep the stored field too.
    data["observed_facts"] = signal.get("observed_facts") or []
    data["strength"] = signal.get("signal_strength")
    return data


def evaluate_signal_groups(prospect_name: str) -> tuple[list[dict], str, list[str]]:
    """Evaluate each playbook group and aggregate its qualification status."""
    eligible = get_eligible_signals(prospect_name)
    if not eligible:
        return [], "Unqualified", []

    signal_types = sorted({row.signal_type for row in eligible if row.signal_type})
    type_rows = frappe.get_all(
        "SEI Signal Type",
        filters={"name": ["in", signal_types]},
        fields=["name", "playbook"],
    )
    playbook_by_type = {row.name: row.playbook for row in type_rows if row.playbook}

    grouped: dict[str, list[dict]] = defaultdict(list)
    for signal in eligible:
        playbook = playbook_by_type.get(signal.signal_type)
        if playbook:
            grouped[playbook].append(signal)

    precedence = {
        "Unqualified": 0,
        "Needs Review": 1,
        "Qualified": 2,
        "Manually Approved": 3,
        "Rejected": 4,
        "Do Not Contact": 5,
    }
    aggregate_status = "Unqualified"
    counted_signals: list[dict] = []
    errors: list[str] = []
    for playbook, signals in grouped.items():
        script = frappe.db.get_value("SEI Playbook", playbook, "signal_qualification_script") or ""
        try:
            group_status = signal_qualification_script.evaluate_signal_qualification_script(
                script,
                [_signal_for_script(signal) for signal in signals],
            )
        except signal_qualification_script.SignalQualificationScriptError as exc:
            errors.append(f"{playbook}: {exc}")
            frappe.log_error(
                title=f"SEI qualification script failed: {playbook}",
                message=str(exc),
            )
            group_status = "Unqualified"

        if precedence[group_status] > precedence[aggregate_status]:
            aggregate_status = group_status
        if group_status in ("Qualified", "Needs Review", "Manually Approved"):
            counted_signals.extend(signals)

    return counted_signals, aggregate_status, errors


def get_qualifying_signals(prospect_name: str) -> list[dict]:
    """Return signals from groups that qualify, need review, or are manually approved."""
    signals, _status, _errors = evaluate_signal_groups(prospect_name)
    return signals


def get_primary_signal(prospect_name: str) -> Optional[str]:
    """Select a deterministic primary signal for CRM context."""
    if not prospect_name:
        return None

    qualified = get_qualifying_signals(prospect_name)
    if qualified:
        strength_order = {"Strong": 0, "Moderate": 1, "Weak": 2}
        qualified.sort(
            key=lambda signal: (
                strength_order.get(signal.signal_strength, 3),
                max(
                    (str(fact.get("source_date") or "") for fact in signal.observed_facts),
                    default="",
                ),
                str(signal.creation or ""),
            ),
            reverse=False,
        )
        return qualified[0].name

    observed_parent = frappe.get_all(
        "SEI Signal Observed Fact",
        filters={
            "parenttype": "SEI Signal",
            "evidence_basis": "Observed",
            "parent": [
                "in",
                frappe.get_all(
                    "SEI Signal",
                    filters={"prospect": prospect_name},
                    pluck="name",
                ),
            ],
        },
        fields=["parent"],
        order_by="source_date desc, creation desc",
        limit=1,
    )
    if observed_parent:
        return observed_parent[0].parent

    signal = frappe.get_all(
        "SEI Signal",
        filters={"prospect": prospect_name},
        fields=["name"],
        order_by="creation desc",
        limit=1,
    )
    if signal:
        return signal[0].name
    return None


def calculate_prospect_qualification_for_doc(prospect: Document) -> dict:
    counted_signals: list[dict] = []
    script_status = "Unqualified"
    script_errors: list[str] = []

    if prospect.name and not prospect.do_not_contact and prospect.lifecycle_status != "Rejected":
        counted_signals, script_status, script_errors = evaluate_signal_groups(prospect.name)

    qualified_count = len(counted_signals)
    strong_count = sum(1 for signal in counted_signals if signal.signal_strength == "Strong")
    moderate_count = sum(1 for signal in counted_signals if signal.signal_strength == "Moderate")
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
    elif script_errors and script_status == "Unqualified":
        status = "Unqualified"
        explanation = (
            "No signal passed qualification; one or more playbook qualification scripts failed to execute."
        )
    else:
        status = script_status
        if status == "Qualified":
            explanation = f"Qualified by {qualified_count} signal(s) under playbook qualification scripts."
        elif status == "Needs Review":
            explanation = (
                f"Needs review based on {qualified_count} signal(s) under playbook qualification scripts."
            )
        elif status == "Manually Approved":
            explanation = "Manually approved by a playbook qualification script."
        elif status == "Rejected":
            explanation = "Rejected by a playbook qualification script."
        elif status == "Do Not Contact":
            explanation = "Marked Do Not Contact by a playbook qualification script."
        else:
            explanation = "No eligible signal qualified under its playbook qualification script."

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


def recalculate_prospects_for_playbook(playbook: str) -> None:
    """Recalculate prospects with at least one Signal Type assigned to this playbook."""
    signal_types = frappe.get_all("SEI Signal Type", filters={"playbook": playbook}, pluck="name")
    if not signal_types:
        return
    prospects = frappe.get_all(
        "SEI Signal",
        filters={"signal_type": ["in", signal_types]},
        pluck="prospect",
        distinct=True,
    )
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
        is_terminal_status,
    )

    for prospect in {name for name in prospects if name}:
        apply_qualification_result(prospect)
        status = frappe.db.get_value("SEI Prospect", prospect, "lifecycle_status")
        if not is_terminal_status(status):
            apply_lifecycle_status(prospect)
