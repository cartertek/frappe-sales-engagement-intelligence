from __future__ import annotations

import json
from functools import wraps
from typing import Any, Callable, Optional

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import (
    get_prospect_arenas,
    get_prospect_arenas_display,
    get_prospect_playbooks,
    get_prospect_playbooks_display,
)

SEI_USER_ROLES = {"Sales Engagement User", "Sales Engagement Manager"}
SEI_MANAGER_ROLES = {"Sales Engagement Manager"}

ERROR_CODES = {
    "validation": "VALIDATION_ERROR",
    "permission": "PERMISSION_DENIED",
    "not_found": "NOT_FOUND",
    "duplicate": "DUPLICATE_FOUND",
    "protected": "PROTECTED_STATE",
    "invalid_payload": "INVALID_PAYLOAD",
    "unsupported": "UNSUPPORTED_OPERATION",
    "schema": "SCHEMA_ERROR",
    "import": "IMPORT_ERROR",
    "crm_blocked": "CRM_CONVERSION_BLOCKED",
}

PROSPECT_CREATE_FIELDS = {
    "prospect_name",
    "website",
    "prospect_type",
    "source_url",
    "source_notes",
    "offer",
    "signal_summary",
    "contact_target_notes",
    "next_action",
    "next_action_date",
    "assigned_to",
    "notes",
    "suggested_message_template",
}
PROSPECT_UPDATE_FIELDS = PROSPECT_CREATE_FIELDS | {"first_seen_date", "last_researched_date"}
PROSPECT_RESTRICTED_FIELDS = {
    "qualification_status",
    "lifecycle_status",
    "crm_lead",
    "crm_organization",
    "crm_contact",
    "crm_deal",
    "do_not_contact",
    "rejected_reason",
    "manual_qualification_override",
    "manual_qualification_reason",
    "crm_conversion_notes",
}
WORKFLOW_RELEVANT_PROSPECT_FIELDS = {
    "website",
    "source_url",
    "signal_summary",
    "contact_target_notes",
    "last_researched_date",
    "offer",
    "suggested_message_template",
}
SIGNAL_FIELDS = {
    "signal_type",
    "signal_strength",
    "evidence_basis",
    "evidence_specificity",
    "confidence",
    "source_url",
    "source_date",
    "observed_fact",
    "signal_claim",
    "why_this_signal_type",
    "why_not_weak",
    "disqualifiers_checked",
    "evidence_gap_reason",
    "evidence_notes",
    "disqualifier_checks",
    "exclude_from_qualification",
    "manual_override_reason",
    "reviewed_by",
    "review_date",
    "attachment",
}
IMPORT_BATCH_CREATE_FIELDS = {
    "batch_label",
    "source_type",
    "source_arena",
    "source_url",
    "import_file",
    "import_kind",
    "import_mode",
    "notes",
}
ATTRIBUTION_FIELDS = {
    "prospect",
    "signal",
    "thesis",
    "marketing_asset",
    "offer",
    "source_arena",
    "crm_lead",
    "crm_deal",
    "fcrm_note",
    "crm_task",
    "crm_call_log",
    "interaction_type",
    "channel",
    "interaction_date",
    "response_category",
    "notes",
}
QUEUE_FIELDS = [
    "name",
    "prospect_name",
    "website",
    "arenas_display",
    "source_url",
    "playbooks_display",
    "offer",
    "qualification_status",
    "lifecycle_status",
    "qualification_explanation",
    "next_action",
    "next_action_date",
    "assigned_to",
    "crm_lead",
    "crm_organization",
    "crm_contact",
    "crm_deal",
    "do_not_contact",
    "rejected_reason",
    "suggested_message_template",
    "modified",
]
PROTECTED_LIFECYCLES = {"Rejected", "Do Not Contact"}


def success(data: Any = None, warnings: Optional[list] = None, messages: Optional[list] = None) -> dict:
    return {"ok": True, "data": data or {}, "warnings": warnings or [], "messages": messages or []}


def failure(code: str, message: str, details: Optional[dict] = None, warnings: Optional[list] = None) -> dict:
    return {
        "ok": False,
        "error": {"code": code, "message": message, "details": details or {}},
        "warnings": warnings or [],
    }


def _classify_exception(exc: Exception) -> str:
    name = exc.__class__.__name__.lower()
    message = str(exc).lower()
    if "permission" in name or "not permitted" in message or "required for this action" in message:
        return ERROR_CODES["permission"]
    if "does not exist" in message or "not found" in message:
        return ERROR_CODES["not_found"]
    if "duplicate" in message:
        return ERROR_CODES["duplicate"]
    if "do not contact" in message or "rejected" in message or "protected" in message:
        return ERROR_CODES["protected"]
    if "crm" in message and (
        "cannot be created" in message or "conversion" in message or "deal creation" in message
    ):
        return ERROR_CODES["crm_blocked"]
    if "import" in message or "row" in message:
        return ERROR_CODES["import"]
    if "json" in message or "payload" in message:
        return ERROR_CODES["invalid_payload"]
    return ERROR_CODES["validation"]


def api_endpoint(fn: Callable) -> Callable:
    @frappe.whitelist()
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            if isinstance(result, dict) and result.get("ok") in (True, False):
                return result
            return success(result)
        except Exception as exc:
            code = _classify_exception(exc)
            expected_codes = {
                ERROR_CODES["validation"],
                ERROR_CODES["permission"],
                ERROR_CODES["not_found"],
                ERROR_CODES["duplicate"],
                ERROR_CODES["protected"],
                ERROR_CODES["invalid_payload"],
                ERROR_CODES["unsupported"],
                ERROR_CODES["schema"],
                ERROR_CODES["import"],
                ERROR_CODES["crm_blocked"],
            }
            if code not in expected_codes:
                # Keep unexpected stack traces in server logs, not in script-facing API responses.
                frappe.log_error(title=f"SEI API error: {fn.__name__}", message=frappe.get_traceback())
            return failure(code, str(exc))

    return wrapper


def _parse_payload(payload: dict | str | None, *, required: bool = True) -> dict:
    if payload is None or payload == "":
        if required:
            frappe.throw("Payload is required.")
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError as exc:
            frappe.throw(f"Invalid JSON payload: {exc}")
        if not isinstance(parsed, dict):
            frappe.throw("Payload must decode to a JSON object.")
        return parsed
    frappe.throw("Payload must be an object or JSON string.")


def _parse_list(value: list[str] | str | None) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return value
    parsed = json.loads(value)
    if not isinstance(parsed, list):
        frappe.throw("Expected a JSON list.")
    return parsed


def _parse_bool(value: int | str | bool | None) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _limit(value: int | str | None, default: int = 50, maximum: int = 250) -> int:
    try:
        limit = int(value or default)
    except Exception:
        limit = default
    return max(1, min(limit, maximum))


def _roles() -> set[str]:
    return set(frappe.get_roles() or [])


def _has_manager_access() -> bool:
    roles = _roles()
    return (
        frappe.session.user == "Administrator" or "Administrator" in roles or bool(SEI_MANAGER_ROLES & roles)
    )


def _has_sei_access() -> bool:
    roles = _roles()
    return _has_manager_access() or bool(SEI_USER_ROLES & roles)


def _require_sei_user():
    if not _has_sei_access():
        frappe.throw("Sales Engagement User or Sales Engagement Manager role is required for this action.")


def _require_manager():
    if not _has_manager_access():
        frappe.throw("Administrator or Sales Engagement Manager role is required for this action.")


def _check_doc_permission(doctype: str, name: str, ptype: str = "read"):
    doc = frappe.get_doc(doctype, name)
    if not doc.has_permission(ptype):
        frappe.throw(f"Not permitted to {ptype} {doctype} {name}.")
    return doc


def _check_prospect_permission(prospect: str, ptype: str = "write"):
    _require_sei_user()
    return _check_doc_permission("SEI Prospect", prospect, ptype)


def _check_batch_permission(batch: str, ptype: str = "read"):
    _require_sei_user()
    return _check_doc_permission("SEI Import Batch", batch, ptype)


def _meta_fields(doctype: str) -> set[str]:
    return {field.fieldname for field in frappe.get_meta(doctype).fields if field.fieldname}


def _select_fields(doctype: str, fields: list[str]) -> list[str]:
    known = _meta_fields(doctype)
    return [field for field in fields if field == "name" or field in known]


def _filter_known_fields(doctype: str, values: dict) -> tuple[dict, list[str]]:
    known = _meta_fields(doctype)
    kept = {key: value for key, value in values.items() if key in known}
    dropped = sorted(key for key in values if key not in known)
    return kept, dropped


def _sanitize_values(payload: dict, allowed: set[str], doctype: str) -> tuple[dict, list[dict]]:
    warnings = []
    restricted = sorted(set(payload) & PROSPECT_RESTRICTED_FIELDS)
    if restricted:
        warnings.append({"code": "RESTRICTED_FIELDS_IGNORED", "fields": restricted})
    values = {field: payload[field] for field in allowed if field in payload}
    values, dropped = _filter_known_fields(doctype, values)
    if dropped:
        warnings.append({"code": "UNKNOWN_FIELDS_IGNORED", "fields": dropped})
    ignored = sorted(set(payload) - set(values) - set(PROSPECT_RESTRICTED_FIELDS) - {"sei_playbook"})
    ignored = [field for field in ignored if field not in allowed]
    if ignored:
        warnings.append({"code": "UNSUPPORTED_FIELDS_IGNORED", "fields": ignored})
    return values, warnings


def _is_protected(prospect_doc) -> bool:
    return bool(
        prospect_doc.get("do_not_contact") or prospect_doc.get("lifecycle_status") in PROTECTED_LIFECYCLES
    )


def _recalculate_and_apply_lifecycle(prospect: str) -> dict:
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
        is_terminal_status,
    )
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    qualification = apply_qualification_result(prospect)
    lifecycle = {}
    status = frappe.db.get_value("SEI Prospect", prospect, "lifecycle_status")
    if not is_terminal_status(status):
        lifecycle = apply_lifecycle_status(prospect)
    return {"qualification": qualification, "lifecycle": lifecycle}


def _prospect_row(row) -> dict:
    data = dict(row)
    data["prospect"] = data.pop("name", None)
    data["arenas"] = get_prospect_arenas(data["prospect"])
    data["arenas_display"] = ", ".join(data["arenas"])
    data["playbooks"] = get_prospect_playbooks(data["prospect"])
    data["playbooks_display"] = ", ".join(data["playbooks"])
    return data


def _prospect_summary(prospect: str) -> dict:
    doc = frappe.get_doc("SEI Prospect", prospect)
    signals = frappe.get_all(
        "SEI Signal",
        filters={"prospect": prospect},
        fields=["name", "signal_type", "signal_strength", "evidence_basis", "source_url", "source_date"],
        order_by="source_date desc, creation desc",
        limit=5,
    )
    primary_signal = None
    try:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
            get_primary_signal,
        )

        primary_signal = get_primary_signal(prospect)
    except Exception:
        primary_signal = signals[0].name if signals else None
    return {
        "prospect": doc.name,
        "prospect_name": doc.prospect_name,
        "website": doc.website,
        "normalized_domain": doc.normalized_domain,
        "arenas": get_prospect_arenas(doc.name),
        "arenas_display": get_prospect_arenas_display(doc.name),
        "source_url": doc.source_url,
        "playbooks": get_prospect_playbooks(doc.name),
        "playbooks_display": get_prospect_playbooks_display(doc.name),
        "offer": doc.offer,
        "qualification_status": doc.qualification_status,
        "lifecycle_status": doc.lifecycle_status,
        "qualification_explanation": doc.qualification_explanation,
        "signal_count": frappe.db.count("SEI Signal", {"prospect": prospect}),
        "primary_signal": primary_signal,
        "recent_signals": signals,
        "crm_links": {
            "crm_lead": doc.crm_lead,
            "crm_organization": doc.crm_organization,
            "crm_contact": doc.crm_contact,
            "crm_deal": doc.crm_deal,
        },
        "contact_path": {},
        "do_not_contact": doc.do_not_contact,
        "rejected_reason": doc.rejected_reason,
        "next_action": doc.next_action,
        "next_action_date": doc.next_action_date,
    }


def _queue(
    filters: dict | str | None, base_filters: dict, limit: int = 50, manager_only: bool = False
) -> dict:
    if manager_only:
        _require_manager()
    else:
        _require_sei_user()
    supplied = _parse_payload(filters, required=False)
    clean_filters = dict(base_filters)
    allowed_filters = {
        "offer",
        "qualification_status",
        "lifecycle_status",
        "assigned_to",
        "next_action_date",
    }
    for key, value in supplied.items():
        if key in allowed_filters and value not in (None, ""):
            clean_filters[key] = value
    rows = frappe.get_all(
        "SEI Prospect",
        filters=clean_filters,
        fields=_select_fields("SEI Prospect", QUEUE_FIELDS),
        order_by="next_action_date asc, modified desc",
        limit=_limit(limit),
    )
    arena_filter = supplied.get("arena") or supplied.get("source_arena") or supplied.get("research_arena")
    thesis_filter = supplied.get("playbook") or supplied.get("sei_playbook")
    result_rows = [_prospect_row(row) for row in rows]
    if arena_filter:
        result_rows = [row for row in result_rows if arena_filter in row.get("arenas", [])]
    if thesis_filter:
        result_rows = [row for row in result_rows if thesis_filter in row.get("playbooks", [])]
    return {"rows": result_rows, "count": len(result_rows)}


# Prospect endpoints


@api_endpoint
def create_prospect(payload: dict | str) -> dict:
    _require_sei_user()
    values, warnings = _sanitize_values(_parse_payload(payload), PROSPECT_CREATE_FIELDS, "SEI Prospect")
    if not values.get("prospect_name"):
        frappe.throw("prospect_name is required.")
    doc = frappe.get_doc({"doctype": "SEI Prospect", **values})
    doc.insert()
    recalculation = _recalculate_and_apply_lifecycle(doc.name)
    return success(
        {"prospect": doc.name, "summary": _prospect_summary(doc.name), **recalculation}, warnings=warnings
    )


@api_endpoint
def update_prospect(prospect: str, payload: dict | str) -> dict:
    doc = _check_prospect_permission(prospect, "write")
    if _is_protected(doc) and not _has_manager_access():
        frappe.throw("Protected prospects require manager access for API updates.")
    raw = _parse_payload(payload)
    values, warnings = _sanitize_values(raw, PROSPECT_UPDATE_FIELDS, "SEI Prospect")
    changed = set(values)
    for key, value in values.items():
        doc.set(key, value)
    doc.save()
    recalculation = {}
    if changed & WORKFLOW_RELEVANT_PROSPECT_FIELDS:
        recalculation = _recalculate_and_apply_lifecycle(doc.name)
    return success(
        {"prospect": doc.name, "summary": _prospect_summary(doc.name), **recalculation}, warnings=warnings
    )


@api_endpoint
def get_prospect(prospect: str) -> dict:
    doc = _check_prospect_permission(prospect, "read")
    data = doc.as_dict()
    data["arenas"] = get_prospect_arenas(doc.name)
    data["arenas_display"] = get_prospect_arenas_display(doc.name)
    data["playbooks"] = get_prospect_playbooks(doc.name)
    data["playbooks_display"] = get_prospect_playbooks_display(doc.name)
    return data


@api_endpoint
def get_prospect_summary(prospect: str) -> dict:
    _check_prospect_permission(prospect, "read")
    return _prospect_summary(prospect)


@api_endpoint
def find_prospects(filters: dict | str | None = None, limit: int = 50) -> dict:
    _require_sei_user()
    supplied = _parse_payload(filters, required=False)
    allowed = {
        "prospect_name",
        "website",
        "normalized_domain",
        "qualification_status",
        "lifecycle_status",
        "assigned_to",
        "do_not_contact",
    }
    clean_filters = {
        key: value for key, value in supplied.items() if key in allowed and value not in (None, "")
    }
    rows = frappe.get_all(
        "SEI Prospect",
        filters=clean_filters,
        fields=_select_fields("SEI Prospect", QUEUE_FIELDS),
        order_by="modified desc",
        limit=_limit(limit),
    )
    arena_filter = supplied.get("arena") or supplied.get("source_arena") or supplied.get("research_arena")
    thesis_filter = supplied.get("playbook") or supplied.get("sei_playbook")
    result_rows = [_prospect_row(row) for row in rows]
    if arena_filter:
        result_rows = [row for row in result_rows if arena_filter in row.get("arenas", [])]
    if thesis_filter:
        result_rows = [row for row in result_rows if thesis_filter in row.get("playbooks", [])]
    return {"rows": result_rows, "count": len(result_rows)}


# Signal endpoints


@api_endpoint
def add_signal(prospect: str, payload: dict | str) -> dict:
    _check_prospect_permission(prospect, "write")
    values = {field: value for field, value in _parse_payload(payload).items() if field in SIGNAL_FIELDS}
    values, dropped = _filter_known_fields("SEI Signal", values)
    warnings = [{"code": "UNKNOWN_FIELDS_IGNORED", "fields": dropped}] if dropped else []
    doc = frappe.get_doc({"doctype": "SEI Signal", "prospect": prospect, **values})
    doc.insert()
    recalculation = _recalculate_and_apply_lifecycle(prospect)
    return success(
        {"signal": doc.name, "prospect": prospect, "summary": _prospect_summary(prospect), **recalculation},
        warnings=warnings,
    )


@api_endpoint
def update_signal(signal: str, payload: dict | str) -> dict:
    _require_sei_user()
    doc = _check_doc_permission("SEI Signal", signal, "write")
    prospect = doc.prospect
    _check_prospect_permission(prospect, "write")
    values = {field: value for field, value in _parse_payload(payload).items() if field in SIGNAL_FIELDS}
    values.pop("prospect", None)
    values, dropped = _filter_known_fields("SEI Signal", values)
    for key, value in values.items():
        doc.set(key, value)
    doc.save()
    recalculation = _recalculate_and_apply_lifecycle(prospect)
    warnings = [{"code": "UNKNOWN_FIELDS_IGNORED", "fields": dropped}] if dropped else []
    return success(
        {"signal": doc.name, "prospect": prospect, "summary": _prospect_summary(prospect), **recalculation},
        warnings=warnings,
    )


@api_endpoint
def get_signals(prospect: str) -> dict:
    _check_prospect_permission(prospect, "read")
    rows = frappe.get_all(
        "SEI Signal",
        filters={"prospect": prospect},
        fields=[
            "name",
            *[field for field in SIGNAL_FIELDS if field not in {"attachment", "disqualifier_checks"}],
        ],
        order_by="source_date desc, creation desc",
    )
    return {"signals": rows, "count": len(rows)}


@api_endpoint
def find_duplicate_signal(prospect: str, payload: dict | str) -> dict:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        find_existing_sei_signal,
    )

    duplicate = find_existing_sei_signal(prospect, _parse_payload(payload))
    return {"duplicate": duplicate, "is_duplicate": bool(duplicate)}


# Workflow endpoints


@api_endpoint
def recalculate_qualification(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    return apply_qualification_result(prospect)


@api_endpoint
def apply_lifecycle(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
    )

    return apply_lifecycle_status(prospect)


@api_endpoint
def apply_lifecycle_suggestion(prospect: str) -> dict:
    return apply_lifecycle(prospect)


@api_endpoint
def mark_ready_for_crm_conversion(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        mark_ready_for_crm_conversion,
    )

    return mark_ready_for_crm_conversion(prospect)


@api_endpoint
def mark_not_ready_for_crm_conversion(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        mark_not_ready_for_crm_conversion,
    )

    return mark_not_ready_for_crm_conversion(prospect)


@api_endpoint
def mark_rejected(prospect: str, reason: Optional[str] = None) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        mark_rejected,
    )

    return mark_rejected(prospect, reason)


@api_endpoint
def mark_do_not_contact(prospect: str, reason: Optional[str] = None) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        mark_do_not_contact,
    )

    return mark_do_not_contact(prospect, reason)


@api_endpoint
def reopen_prospect(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        reopen_prospect,
    )

    return reopen_prospect(prospect)


# Playbook and drafting endpoints


@api_endpoint
def apply_playbook_defaults(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.playbooks import (
        apply_playbook_defaults as _apply_playbook_defaults,
    )

    return _apply_playbook_defaults(prospect)


@api_endpoint
def preview_message_draft(prospect: str, template: str) -> dict:
    _check_prospect_permission(prospect, "read")
    _check_doc_permission("SEI Message Template", template, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.drafting import (
        preview_message_draft as _preview_message_draft,
    )

    return _preview_message_draft(prospect, template)


# CRM conversion/linking endpoints


@api_endpoint
def preview_crm_lead(prospect: str) -> dict:
    result = preview_crm_conversion(prospect)
    if result.get("ok") is False:
        return result
    return result["data"]


@api_endpoint
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


@api_endpoint
def find_crm_duplicates(prospect: str) -> dict:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        find_possible_crm_duplicates,
    )

    return find_possible_crm_duplicates(prospect)


@api_endpoint
def create_crm_lead(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_crm_lead_from_prospect,
    )

    return create_crm_lead_from_prospect(prospect, _parse_payload(options, required=False))


@api_endpoint
def create_or_link_crm_organization(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_or_link_crm_organization,
    )

    return create_or_link_crm_organization(prospect, _parse_payload(options, required=False))


@api_endpoint
def create_or_link_contact(prospect: str, options: Optional[str | dict] = None) -> dict:
    result = create_or_link_crm_contact(prospect, options)
    if result.get("ok") is False:
        return result
    return result["data"]


@api_endpoint
def create_or_link_crm_contact(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_or_link_crm_contact,
    )

    return create_or_link_crm_contact(prospect, _parse_payload(options, required=False))


@api_endpoint
def create_crm_deal(prospect: str, options: Optional[str | dict] = None) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        create_crm_deal_from_prospect,
    )

    return create_crm_deal_from_prospect(prospect, _parse_payload(options, required=False))


@api_endpoint
def link_existing_crm_record(prospect: str, doctype: str, record_name: str) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        link_existing_crm_record,
    )

    return link_existing_crm_record(prospect, doctype, record_name)


@api_endpoint
def sync_sei_context_to_crm(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        sync_sei_context_to_crm,
    )

    return sync_sei_context_to_crm(prospect)


# Import and data hygiene endpoints


@api_endpoint
def create_import_batch(payload: dict | str) -> dict:
    _require_sei_user()
    raw = _parse_payload(payload)
    values = {field: raw[field] for field in IMPORT_BATCH_CREATE_FIELDS if field in raw}
    values, dropped = _filter_known_fields("SEI Import Batch", values)
    if not values.get("batch_label"):
        frappe.throw("batch_label is required.")
    doc = frappe.get_doc({"doctype": "SEI Import Batch", **values})
    doc.insert()
    warnings = [{"code": "UNKNOWN_FIELDS_IGNORED", "fields": dropped}] if dropped else []
    return success({"batch": doc.name, "status": doc.status}, warnings=warnings)


@api_endpoint
def dry_run_import(batch: str) -> dict:
    _check_batch_permission(batch, "write")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        run_import_batch as _run_import_batch,
    )

    return _run_import_batch(batch, True)


@api_endpoint
def run_import(batch: str) -> dict:
    _check_batch_permission(batch, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        run_import_batch as _run_import_batch,
    )

    return _run_import_batch(batch, False)


@api_endpoint
def run_import_batch(batch: str, dry_run: int | str | bool = 1) -> dict:
    result = dry_run_import(batch) if _parse_bool(dry_run) else run_import(batch)
    if result.get("ok") is False:
        return result
    return result["data"]


@api_endpoint
def cancel_import_batch(batch: str) -> dict:
    _check_batch_permission(batch, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        cancel_import_batch,
    )

    return cancel_import_batch(batch)


@api_endpoint
def reset_import_batch_to_draft(batch: str) -> dict:
    _check_batch_permission(batch, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        reset_import_batch_to_draft as _reset_import_batch_to_draft,
    )

    return _reset_import_batch_to_draft(batch)


@api_endpoint
def get_import_batch_status(batch: str) -> dict:
    doc = _check_batch_permission(batch, "read")
    return {
        "batch": doc.name,
        "batch_label": doc.batch_label,
        "status": doc.status,
        "dry_run": doc.dry_run,
        "rows_total": doc.rows_total,
        "rows_created": doc.rows_created,
        "rows_updated": doc.rows_updated,
        "rows_skipped": doc.rows_skipped,
        "rows_failed": doc.rows_failed,
        "started_at": doc.started_at,
        "completed_at": doc.completed_at,
        "error_summary": doc.error_summary,
    }


@api_endpoint
def get_import_batch_rows(batch: str, filters: dict | str | None = None) -> dict:
    doc = _check_batch_permission(batch, "read")
    supplied = _parse_payload(filters, required=False)
    rows = []
    for row in doc.rows:
        item = row.as_dict()
        if supplied.get("row_status") and item.get("row_status") != supplied["row_status"]:
            continue
        if supplied.get("action_taken") and item.get("action_taken") != supplied["action_taken"]:
            continue
        rows.append(item)
    return {"batch": batch, "rows": rows, "count": len(rows)}


@api_endpoint
def find_duplicate_sei_prospects(filters: dict | str | None = None) -> dict:
    _require_sei_user()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        find_duplicate_sei_prospects as _find_duplicate_sei_prospects,
    )

    return _find_duplicate_sei_prospects()


@api_endpoint
def find_duplicate_sei_signals(filters: dict | str | None = None) -> dict:
    _require_sei_user()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        find_duplicate_sei_signals as _find_duplicate_sei_signals,
    )

    return _find_duplicate_sei_signals()


@api_endpoint
def backfill_normalized_domains(limit: int | None = None, dry_run: bool = True) -> dict:
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        normalize_domain,
    )

    rows = frappe.get_all(
        "SEI Prospect",
        fields=["name", "website", "normalized_domain"],
        limit=_limit(limit, default=500, maximum=5000) if limit else 0,
    )
    changes = []
    for prospect in rows:
        domain = normalize_domain(prospect.website)
        if domain and domain != prospect.normalized_domain:
            changes.append({"prospect": prospect.name, "old": prospect.normalized_domain, "new": domain})
            if not _parse_bool(dry_run):
                frappe.db.set_value(
                    "SEI Prospect", prospect.name, "normalized_domain", domain, update_modified=True
                )
    return {
        "dry_run": _parse_bool(dry_run),
        "updated": 0 if _parse_bool(dry_run) else len(changes),
        "changes": changes,
    }


@api_endpoint
def backfill_sei_normalized_domains() -> dict:
    result = backfill_normalized_domains(dry_run=False)
    if result.get("ok") is False:
        return result
    return result["data"]


@api_endpoint
def recalculate_selected_prospects(prospects: list[str] | str) -> dict:
    _require_manager()
    rows = []
    for prospect in _parse_list(prospects):
        if frappe.db.exists("SEI Prospect", prospect):
            rows.append({"prospect": prospect, **_recalculate_and_apply_lifecycle(prospect)})
    return {"updated": rows, "count": len(rows)}


@api_endpoint
def recalculate_all_sei_prospect_qualifications() -> dict:
    _require_manager()
    prospects = frappe.get_all("SEI Prospect", pluck="name")
    result = recalculate_selected_prospects(prospects)
    if result.get("ok") is False:
        return result
    return result["data"]


@api_endpoint
def apply_lifecycle_to_selected_prospects(prospects: str | list[str]) -> dict:
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        apply_lifecycle_to_selected_prospects as _apply_lifecycle_to_selected_prospects,
    )

    return _apply_lifecycle_to_selected_prospects(_parse_list(prospects))


@api_endpoint
def find_sei_prospects_missing_source_arena() -> dict:
    _require_sei_user()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        find_prospects_missing_source_arena,
    )

    return find_prospects_missing_source_arena()


@api_endpoint
def find_sei_prospects_missing_signal_evidence() -> dict:
    _require_sei_user()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        find_prospects_missing_signal_evidence,
    )

    return find_prospects_missing_signal_evidence()


@api_endpoint
def find_sei_signals_missing_source_url() -> dict:
    _require_sei_user()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        find_signals_missing_source_url,
    )

    return find_signals_missing_source_url()


@api_endpoint
def find_inferred_qualifying_signal_issues() -> dict:
    _require_sei_user()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.imports import (
        find_inferred_qualifying_signal_issues,
    )

    return find_inferred_qualifying_signal_issues()


# Queue endpoints: direct DocType queries, not report wrappers.


@api_endpoint
def get_needs_research_queue(filters: dict | str | None = None, limit: int = 50) -> dict:
    return _queue(
        filters, {"lifecycle_status": ["in", ["New", "Needs Research"]], "do_not_contact": 0}, limit
    )


@api_endpoint
def get_ready_for_crm_conversion_queue(filters: dict | str | None = None, limit: int = 50) -> dict:
    return _queue(
        filters,
        {
            "lifecycle_status": "Ready for CRM Conversion",
            "do_not_contact": 0,
            "qualification_status": ["in", ["Qualified", "Manually Approved"]],
        },
        limit,
    )


@api_endpoint
def get_find_contact_queue(filters: dict | str | None = None, limit: int = 50) -> dict:
    return _queue(filters, {"lifecycle_status": "Find Contact", "do_not_contact": 0}, limit)


@api_endpoint
def get_protected_status_queue(filters: dict | str | None = None, limit: int = 50) -> dict:
    return _queue(
        filters,
        {"lifecycle_status": ["in", ["Rejected", "Do Not Contact"]]},
        limit,
        manager_only=True,
    )


@api_endpoint
def get_recent_import_batches(filters: dict | str | None = None, limit: int = 50) -> dict:
    _require_sei_user()
    supplied = _parse_payload(filters, required=False)
    clean_filters = {}
    for key in ("status", "source_type", "source_arena", "import_kind"):
        if supplied.get(key):
            clean_filters[key] = supplied[key]
    rows = frappe.get_all(
        "SEI Import Batch",
        filters=clean_filters,
        fields=[
            "name",
            "batch_label",
            "source_type",
            "source_arena",
            "status",
            "dry_run",
            "rows_total",
            "rows_created",
            "rows_updated",
            "rows_skipped",
            "rows_failed",
            "modified",
        ],
        order_by="modified desc",
        limit=_limit(limit),
    )
    return {"rows": [{"batch": row.pop("name"), **dict(row)} for row in rows], "count": len(rows)}


# Interaction attribution endpoints


@api_endpoint
def create_interaction_attribution(payload: dict | str) -> dict:
    _require_sei_user()
    raw = _parse_payload(payload)
    values = {field: raw[field] for field in ATTRIBUTION_FIELDS if field in raw}
    values, dropped = _filter_known_fields("SEI Interaction Attribution", values)
    if not values.get("prospect"):
        frappe.throw("prospect is required.")
    _check_prospect_permission(values["prospect"], "read")
    doc = frappe.get_doc({"doctype": "SEI Interaction Attribution", **values})
    doc.insert()
    warnings = [{"code": "UNKNOWN_FIELDS_IGNORED", "fields": dropped}] if dropped else []
    return success({"interaction_attribution": doc.name}, warnings=warnings)


@api_endpoint
def get_interaction_attributions(
    prospect: str | None = None, crm_lead: str | None = None, crm_deal: str | None = None
) -> dict:
    _require_sei_user()
    filters = {}
    if prospect:
        _check_prospect_permission(prospect, "read")
        filters["prospect"] = prospect
    if crm_lead:
        filters["crm_lead"] = crm_lead
    if crm_deal:
        filters["crm_deal"] = crm_deal
    if not filters:
        frappe.throw("Provide prospect, crm_lead, or crm_deal.")
    fields = [
        "name",
        *[field for field in ATTRIBUTION_FIELDS if field in _meta_fields("SEI Interaction Attribution")],
    ]
    rows = frappe.get_all(
        "SEI Interaction Attribution",
        filters=filters,
        fields=fields,
        order_by="interaction_date desc, creation desc",
        limit=250,
    )
    return {
        "rows": [{"interaction_attribution": row.pop("name"), **dict(row)} for row in rows],
        "count": len(rows),
    }


@api_endpoint
def get_linked_crm_records(prospect: str) -> dict:
    _check_prospect_permission(prospect, "read")
    doc = frappe.get_doc("SEI Prospect", prospect)
    groups = {
        "crm_leads": [],
        "crm_organizations": [],
        "crm_contacts": [],
        "crm_deals": [],
    }
    seen = {key: set() for key in groups}

    def add(group: str, doctype: str, name: str | None):
        if not name or name in seen[group] or not frappe.db.exists(doctype, name):
            return
        seen[group].add(name)
        title_fields = {
            "CRM Lead": ("lead_name", "first_name", "organization"),
            "CRM Organization": ("organization_name",),
            "Contact": ("full_name", "first_name"),
            "CRM Deal": ("deal_name", "lead_name", "organization_name"),
        }[doctype]
        title = None
        for fieldname in title_fields:
            if fieldname in _meta_fields(doctype):
                title = frappe.db.get_value(doctype, name, fieldname)
                if title:
                    break
        groups[group].append({"name": name, "title": title or name})

    add("crm_leads", "CRM Lead", doc.get("crm_lead"))
    add("crm_organizations", "CRM Organization", doc.get("crm_organization"))
    add("crm_contacts", "Contact", doc.get("crm_contact"))
    add("crm_deals", "CRM Deal", doc.get("crm_deal"))
    for row in doc.get("contacts") or []:
        add("crm_contacts", "Contact", row.get("crm_contact"))

    for group, doctype in (
        ("crm_leads", "CRM Lead"),
        ("crm_organizations", "CRM Organization"),
        ("crm_contacts", "Contact"),
        ("crm_deals", "CRM Deal"),
    ):
        if "sei_prospect" in _meta_fields(doctype):
            for name in frappe.get_all(doctype, filters={"sei_prospect": prospect}, pluck="name"):
                add(group, doctype, name)

    return groups


@api_endpoint
def convert_to_crm_lead(prospect: str) -> dict:
    _check_prospect_permission(prospect, "write")
    _require_manager()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.crm_preparation import (
        convert_prospect_to_crm_leads,
    )

    return convert_prospect_to_crm_leads(prospect)


@api_endpoint
def get_missing_prospect_contact_roles(prospect: str) -> list[str]:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
        missing_required_contact_roles,
    )

    return missing_required_contact_roles(frappe.get_doc("SEI Prospect", prospect))


@api_endpoint
def get_prospect_contact_role_requirements(prospect: str) -> dict[str, bool]:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
        contact_role_requirements,
    )

    return contact_role_requirements(frappe.get_doc("SEI Prospect", prospect))


@api_endpoint
def prospect_contact_role_requires_signal_relevance(prospect: str, contact_role: str) -> bool:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
        contact_role_requires_signal_relevance,
    )

    return contact_role_requires_signal_relevance(
        frappe.get_doc("SEI Prospect", prospect), contact_role
    )


@api_endpoint
def get_prospect_contact_options(prospect: str) -> list[str]:
    _check_prospect_permission(prospect, "read")
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
        emails,
        populated_contacts,
    )

    doc = frappe.get_doc("SEI Prospect", prospect)
    return [
        f"{row.contact_name or row.contact_role} <{(emails(row) or [''])[0]}>".strip()
        for row in populated_contacts(doc)
    ]


def _message_draft_recipient(prospect, value: str | None) -> str:
    from email.utils import parseaddr

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import emails

    raw = (value or "").strip()
    parsed = parseaddr(raw)[1]
    if parsed and "@" in parsed:
        return parsed
    for row in prospect.get("contacts") or []:
        if raw in {
            (row.get("contact_name") or "").strip(),
            (row.get("crm_contact") or "").strip(),
        }:
            addresses = emails(row)
            if addresses:
                return addresses[0]
    frappe.throw(f"No email address is available for message recipient {raw or '(blank)'}.")


def _message_draft_sender(value: str | None) -> tuple[str, str | None]:
    from email.utils import parseaddr

    raw = (value or "").strip()
    display_name, parsed = parseaddr(raw)
    if parsed and "@" in parsed:
        user = frappe.db.get_value("User", {"email": parsed}, ["email", "full_name"], as_dict=True)
        return parsed, (user.full_name if user else display_name or None)

    user = frappe.db.get_value("User", raw, ["email", "full_name"], as_dict=True)
    if user and user.email and "@" in user.email:
        return user.email, user.full_name or None

    frappe.throw(f"No email address is available for message sender {raw or '(blank)'}.")


def _optional_email_list(value: str | None) -> str | None:
    from email.utils import getaddresses

    addresses = [address for _, address in getaddresses([value or ""]) if "@" in address]
    return ", ".join(dict.fromkeys(addresses)) or None


@api_endpoint
def mark_message_draft_sent(draft: str) -> dict:
    if frappe.db.exists("SEI Prospect Message Draft", draft):
        doc = frappe.get_doc("SEI Prospect Message Draft", draft)
        _check_doc_permission("SEI Prospect", doc.parent, "write")
        prospect = frappe.get_doc("SEI Prospect", doc.parent)
    else:
        _check_doc_permission("SEI Message Draft", draft, "write")
        doc = frappe.get_doc("SEI Message Draft", draft)
        prospect = frappe.get_doc("SEI Prospect", doc.prospect)
    if (
        prospect.lifecycle_status not in ("Converted to CRM Lead", "Converted to CRM Deal")
        or not prospect.crm_lead
    ):
        frappe.throw("The prospect must be converted to a CRM Lead before a draft can be marked sent.")
    sender, sender_full_name = _message_draft_sender(doc.from_user)
    payload = {
        "doctype": "Communication",
        "communication_type": "Communication",
        "communication_medium": "Email",
        "sent_or_received": "Sent",
        "status": "Linked",
        "delivery_status": "Sent",
        "sender": sender,
        "sender_full_name": sender_full_name,
        "recipients": _message_draft_recipient(prospect, doc.to_contact),
        "cc": _optional_email_list(doc.cc),
        "subject": doc.subject or f"Message to {doc.to_contact}",
        "content": doc.body or "",
        "reference_doctype": "CRM Lead",
        "reference_name": prospect.crm_lead,
    }
    communication = frappe.get_doc(payload)
    communication.insert(ignore_permissions=True)
    doc.db_set(
        {
            "sent": 1,
            "sent_on": frappe.utils.now_datetime(),
            "crm_email": communication.name,
        }
    )
    return {"crm_email": communication.name, "sent": True}


@api_endpoint
def mark_message_draft_unsent(draft: str) -> dict:
    if frappe.db.exists("SEI Prospect Message Draft", draft):
        doc = frappe.get_doc("SEI Prospect Message Draft", draft)
        _check_doc_permission("SEI Prospect", doc.parent, "write")
    else:
        _check_doc_permission("SEI Message Draft", draft, "write")
        doc = frappe.get_doc("SEI Message Draft", draft)

    communication_name = doc.get("crm_email")
    if communication_name and frappe.db.exists("Communication", communication_name):
        communication = frappe.get_doc("Communication", communication_name)
        if communication.sent_or_received != "Sent":
            frappe.throw("The linked CRM Communication is not an outgoing sent message.")
        communication.delete(ignore_permissions=True)

    doc.db_set({"sent": 0, "sent_on": None, "crm_email": None})
    return {"crm_email": None, "sent": False}


@frappe.whitelist()
def log_contact_placeholder_debug(payload: str | dict | None = None) -> dict:
    """Temporary browser-to-server diagnostics for Prospect contact placeholder debugging."""
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {"raw": payload}
    entry = {
        "timestamp": frappe.utils.now_datetime().isoformat(),
        "user": frappe.session.user,
        "payload": payload or {},
    }
    frappe.logger("sei_contact_placeholder_debug", allow_site=True, file_count=5).info(
        json.dumps(entry, default=str, sort_keys=True)
    )
    return {"logged": True}
