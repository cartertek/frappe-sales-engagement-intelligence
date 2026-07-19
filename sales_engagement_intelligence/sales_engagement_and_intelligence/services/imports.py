from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime
from frappe.utils.file_manager import get_file_path

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import (
    resolve_signal_type,
)

PROSPECT_FIELDS = {
    "prospect_name",
    "website",
    "prospect_type",
    "source_arena",
    "source_url",
    "source_notes",
    "first_seen_date",
    "last_researched_date",
    "offer",
    "signal_summary",
    "contact_target_notes",
    "primary_contact_name",
    "primary_contact_role",
    "primary_contact_email",
    "primary_contact_url",
    "primary_contact_notes",
    "next_action",
    "next_action_date",
    "assigned_to",
    "notes",
}
DATE_FIELDS = {
    "first_seen_date",
    "last_researched_date",
    "next_action_date",
    "source_date",
    "review_date",
    "manual_override_date",
}
BOOLEAN_FIELDS = {
    "exclude_from_qualification",
    "initial_exclude_from_qualification",
    "counts_toward_qualification",
    "initial_counts_toward_qualification",
}
PROTECTED_IMPORT_FIELDS = {
    "manual_qualification_override",
    "manual_qualification_reason",
    "do_not_contact",
    "rejected_reason",
    "crm_conversion_notes",
}
CREATE_ONLY = "Create Only"
UPDATE_EXISTING = "Update Existing"
CREATE_OR_UPDATE = "Create or Update"
DRY_RUN = "Dry Run"
SIGNAL_ONLY = "Signal Only"
PROSPECT_ONLY = "Prospect Only"
COMBINED = "Combined Prospect + Initial Signal"
TERMINAL_STATUSES = ("Rejected", "Do Not Contact", "Converted to CRM Lead", "Converted to CRM Deal")


def _normalize_import_mode(import_mode: str | None) -> str:
    if not import_mode or import_mode == "Dry Run":
        return CREATE_OR_UPDATE
    return import_mode


def _clean(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value if value != "" else None
    return value


def _parse_bool(value: Any) -> int:
    if value is None or value == "":
        return 0
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, (int, float)):
        return 1 if value else 0
    return 1 if str(value).strip().lower() in {"1", "true", "yes", "y", "on"} else 0


def _exclude_from_qualification_value(row: dict, initial: bool = False) -> int:
    """Resolve the new exclusion flag, accepting legacy count-toward columns during transition."""
    new_field = "initial_exclude_from_qualification" if initial else "exclude_from_qualification"
    legacy_field = "initial_counts_toward_qualification" if initial else "counts_toward_qualification"

    if row.get(new_field) is not None:
        return row.get(new_field) or 0
    if row.get(legacy_field) is not None:
        return 0 if row.get(legacy_field) else 1
    return 0


def normalize_domain(value: Optional[str]) -> Optional[str]:
    value = _clean(value)
    if not value:
        return None
    parsed = urlparse(value if "://" in value else f"https://{value}")
    hostname = (parsed.hostname or "").lower().strip(".")
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname or None


def normalize_import_row(row: dict) -> dict:
    normalized = {str(k or "").strip(): _clean(v) for k, v in row.items() if str(k or "").strip()}
    for field in list(normalized):
        if field in BOOLEAN_FIELDS:
            normalized[field] = _parse_bool(normalized[field])
        elif field in DATE_FIELDS or field == "initial_source_date":
            if normalized[field]:
                normalized[field] = str(getdate(normalized[field]))
    website = normalized.get("website") or normalized.get("prospect_website")
    normalized["normalized_domain"] = normalized.get("prospect_normalized_domain") or normalize_domain(
        website
    )
    if normalized.get("initial_signal_source_url") and not normalized.get("source_url_for_signal"):
        normalized["source_url_for_signal"] = normalized.get("initial_signal_source_url")
    elif normalized.get("source_url") and not normalized.get("source_url_for_signal"):
        normalized["source_url_for_signal"] = normalized.get("source_url")
    return normalized


def _result(
    is_duplicate: bool, doctype: str = "", name: str = "", reason: str = "", confidence: str = ""
) -> Optional[dict]:
    if not is_duplicate:
        return None
    return {
        "is_duplicate": True,
        "matched_doctype": doctype,
        "matched_name": name,
        "match_reason": reason,
        "confidence": confidence,
    }


def _first_value(doctype: str, filters: dict, fields: list[str]) -> Optional[dict]:
    found = frappe.get_all(doctype, filters=filters, fields=fields, limit=1)
    return found[0] if found else None


def find_existing_sei_prospect(row: dict) -> Optional[dict]:
    row = normalize_import_row(row)
    fields = ["name", "prospect_name", "normalized_domain", "website", "source_url"]
    checks = [
        ("normalized_domain", row.get("normalized_domain"), "Matched by normalized_domain", "High"),
        ("website", row.get("website") or row.get("prospect_website"), "Matched by exact website", "High"),
        ("prospect_name", row.get("prospect_name"), "Matched by exact prospect_name", "Medium"),
        ("source_url", row.get("source_url"), "Matched by source_url", "Medium"),
    ]
    for fieldname, value, reason, confidence in checks:
        if not value:
            continue
        match = _first_value("SEI Prospect", {fieldname: value}, fields)
        if match:
            return _result(True, "SEI Prospect", match.name, reason, confidence)
    return None


def _find_signal_by_hash(prospect: str, evidence_notes: Optional[str]) -> Optional[dict]:
    if not prospect or not evidence_notes:
        return None
    target = hashlib.sha256(evidence_notes.strip().encode()).hexdigest()
    candidates = frappe.get_all(
        "SEI Signal",
        filters={"prospect": prospect},
        fields=["name", "evidence_notes"],
        limit=250,
    )
    for candidate in candidates:
        if hashlib.sha256((candidate.evidence_notes or "").strip().encode()).hexdigest() == target:
            return candidate
    return None


def find_existing_sei_signal(prospect_name: str, row: dict) -> Optional[dict]:
    row = normalize_import_row(row)
    prospect = prospect_name
    if not prospect:
        return None
    source_url = row.get("source_url_for_signal") or row.get("source_url")
    if source_url:
        match = _first_value("SEI Signal", {"prospect": prospect, "source_url": source_url}, ["name"])
        if match:
            return _result(True, "SEI Signal", match.name, "Matched by prospect + source_url", "High")
    signal_type = row.get("initial_signal_type") or row.get("signal_type")
    source_date = row.get("initial_source_date") or row.get("source_date")
    if signal_type and source_date:
        match = _first_value(
            "SEI Signal",
            {"prospect": prospect, "signal_type": signal_type, "source_date": source_date},
            ["name"],
        )
        if match:
            return _result(
                True, "SEI Signal", match.name, "Matched by prospect + signal_type + source_date", "Medium"
            )
    evidence_notes = row.get("initial_evidence_notes") or row.get("evidence_notes")
    match = _find_signal_by_hash(prospect, evidence_notes)
    if match:
        return _result(True, "SEI Signal", match.name, "Matched by prospect + evidence_notes hash", "Low")
    return None


def _resolve_playbook(row: dict) -> Optional[str]:
    value = row.get("sei_playbook") or row.get("playbook") or row.get("sei_thesis") or row.get("thesis")
    if not value:
        return None
    if frappe.db.exists("SEI Playbook", value):
        return value
    frappe.throw(f"SEI Playbook not found: {value}")


def _validate_prospect(row: dict, require_create_context: bool = True) -> None:
    if not row.get("prospect_name"):
        frappe.throw("prospect_name is required for Prospect import.")
    if require_create_context and not any(
        row.get(f) for f in ("website", "source_url", "source_arena", "primary_contact_email")
    ):
        frappe.throw(
            "At least one context field is required: website, source_url, "
            "source_arena, or primary_contact_email."
        )


def _has_initial_signal(row: dict) -> bool:
    return any(
        row.get(f)
        for f in (
            "initial_signal_type",
            "initial_signal_strength",
            "initial_evidence_basis",
            "initial_evidence_notes",
        )
    )


def _signal_value(row: dict, base: str, prefix: str = ""):
    return row.get(f"{prefix}{base}" if prefix else base)


def _validate_signal(row: dict, prefix: str = "") -> None:
    required = ["signal_type", "signal_strength", "evidence_basis"]
    missing = []
    for base in required:
        fieldname = f"{prefix}{base}" if prefix else base
        if not row.get(fieldname):
            missing.append(fieldname)
    if missing:
        frappe.throw("Missing required signal fields: " + ", ".join(missing))

    strength = _signal_value(row, "signal_strength", prefix)
    evidence_basis = _signal_value(row, "evidence_basis", prefix)
    if evidence_basis == "Observed" and not _signal_value(row, "observed_fact", prefix):
        frappe.throw("Observed signals require observed_fact.")

    if strength in {"Moderate", "Strong"}:
        proof_fields = [
            "observed_fact",
            "signal_claim",
            "why_this_signal_type",
            "why_not_weak",
            "disqualifiers_checked",
        ]
        missing_proof = [
            f"{prefix}{field}" if prefix else field
            for field in proof_fields
            if not _signal_value(row, field, prefix)
        ]
        if missing_proof:
            frappe.throw(
                "Moderate or Strong signals require structured evidence fields: " + ", ".join(missing_proof)
            )

    if strength == "Weak" and not (
        _signal_value(row, "observed_fact", prefix) or _signal_value(row, "evidence_gap_reason", prefix)
    ):
        frappe.throw("Weak signals require observed_fact or evidence_gap_reason.")

    if (
        evidence_basis == "Inferred"
        and strength == "Strong"
        and not _signal_value(row, "manual_override_reason", prefix)
    ):
        frappe.throw("Inferred signals cannot be Strong without manual_override_reason.")


def _prospect_values(row: dict) -> dict:
    return {field: row.get(field) for field in PROSPECT_FIELDS if row.get(field) is not None}


def _signal_values(prospect: str, row: dict, initial: bool = False) -> dict:
    if initial:
        values = {
            "prospect": prospect,
            "signal_type": resolve_signal_type(row.get("initial_signal_type")),
            "signal_strength": row.get("initial_signal_strength"),
            "evidence_basis": row.get("initial_evidence_basis"),
            "evidence_specificity": row.get("initial_evidence_specificity")
            or row.get("evidence_specificity"),
            "confidence": row.get("initial_confidence"),
            "source_url": row.get("initial_signal_source_url") or row.get("source_url"),
            "source_date": row.get("initial_source_date"),
            "observed_fact": row.get("initial_observed_fact"),
            "signal_claim": row.get("initial_signal_claim"),
            "why_this_signal_type": row.get("initial_why_this_signal_type"),
            "why_not_weak": row.get("initial_why_not_weak"),
            "disqualifiers_checked": row.get("initial_disqualifiers_checked"),
            "evidence_gap_reason": row.get("initial_evidence_gap_reason"),
            "evidence_notes": row.get("initial_evidence_notes"),
            "exclude_from_qualification": _exclude_from_qualification_value(row, initial=True),
            "manual_override_reason": row.get("initial_manual_override_reason"),
        }
    else:
        values = {
            "prospect": prospect,
            "signal_type": resolve_signal_type(row.get("signal_type")),
            "signal_strength": row.get("signal_strength"),
            "evidence_basis": row.get("evidence_basis"),
            "evidence_specificity": row.get("evidence_specificity"),
            "confidence": row.get("confidence"),
            "source_url": row.get("source_url"),
            "source_date": row.get("source_date"),
            "observed_fact": row.get("observed_fact"),
            "signal_claim": row.get("signal_claim"),
            "why_this_signal_type": row.get("why_this_signal_type"),
            "why_not_weak": row.get("why_not_weak"),
            "disqualifiers_checked": row.get("disqualifiers_checked"),
            "evidence_gap_reason": row.get("evidence_gap_reason"),
            "evidence_notes": row.get("evidence_notes"),
            "exclude_from_qualification": _exclude_from_qualification_value(row),
            "manual_override_reason": row.get("manual_override_reason"),
            "reviewed_by": row.get("reviewed_by"),
            "review_date": row.get("review_date"),
        }
    return {k: v for k, v in values.items() if v is not None}


def _match_signal_import_prospect(row: dict) -> Optional[str]:
    if row.get("prospect_normalized_domain"):
        name = frappe.db.get_value(
            "SEI Prospect", {"normalized_domain": row.get("prospect_normalized_domain")}, "name"
        )
        if name:
            return name
    if row.get("prospect_website"):
        domain = normalize_domain(row.get("prospect_website"))
        name = frappe.db.get_value(
            "SEI Prospect", {"normalized_domain": domain}, "name"
        ) or frappe.db.get_value("SEI Prospect", {"website": row.get("prospect_website")}, "name")
        if name:
            return name
    if row.get("prospect_name"):
        return frappe.db.get_value("SEI Prospect", {"prospect_name": row.get("prospect_name")}, "name")
    return None


def classify_import_row(row: dict, import_kind: str = COMBINED, import_mode: str = CREATE_OR_UPDATE) -> dict:
    row = normalize_import_row(row)
    duplicate = None
    intended_action = "Create Prospect"
    errors = []
    try:
        if import_kind == SIGNAL_ONLY:
            prospect = _match_signal_import_prospect(row)
            if not prospect:
                frappe.throw("No existing SEI Prospect matched for signal-only import.")
            _validate_signal(row)
            duplicate = find_existing_sei_signal(prospect, row)
            intended_action = (
                "Update Signal"
                if duplicate and import_mode in (UPDATE_EXISTING, CREATE_OR_UPDATE)
                else "Create Signal"
            )
            if duplicate and import_mode == CREATE_ONLY:
                intended_action = "Skip"
        else:
            _validate_prospect(row, require_create_context=True)
            _resolve_playbook(row)
            duplicate = find_existing_sei_prospect(row)
            if duplicate:
                if import_mode in (UPDATE_EXISTING, CREATE_OR_UPDATE):
                    intended_action = "Update Prospect"
                else:
                    intended_action = "Skip"
            elif import_mode == UPDATE_EXISTING:
                intended_action = "Failed"
                errors.append("No existing SEI Prospect matched for update.")
            else:
                intended_action = "Create Prospect"
            if import_kind == COMBINED and _has_initial_signal(row):
                _validate_signal(row, prefix="initial_")
    except Exception as exc:
        intended_action = "Failed"
        errors.append(frappe.get_traceback() if frappe.conf.developer_mode else str(exc))
    return {
        "row": row,
        "duplicate": duplicate,
        "intended_action": intended_action,
        "errors": errors,
    }


def _read_csv(batch_doc: Document) -> list[dict]:
    if not batch_doc.import_file:
        frappe.throw("Attach an import_file before running import.")
    path = Path(get_file_path(batch_doc.import_file))
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _clear_rows(batch_doc: Document) -> None:
    batch_doc.set("rows", [])


def _append_row(
    batch_doc: Document,
    row_number: int,
    row: dict,
    status: str,
    action: str,
    error: str = "",
    prospect: str = "",
    signal: str = "",
    matched: str = "",
) -> None:
    batch_doc.append(
        "rows",
        {
            "row_number": row_number,
            "row_status": status,
            "action_taken": action,
            "prospect": prospect,
            "signal": signal,
            "matched_existing_prospect": matched,
            "error_message": (error or "")[:140],
            "raw_row_json": json.dumps(row, indent=2, default=str),
        },
    )


def _recalculate(prospect: str) -> None:
    if not prospect:
        return
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
        is_terminal_status,
    )
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    try:
        frappe.flags.sei_m3_recalculating = True
        apply_qualification_result(prospect)
        status = frappe.db.get_value("SEI Prospect", prospect, "lifecycle_status")
        if not is_terminal_status(status):
            apply_lifecycle_status(prospect)
    finally:
        frappe.flags.sei_m3_recalculating = False


def _create_prospect(row: dict) -> str:
    doc = frappe.get_doc({"doctype": "SEI Prospect", **_prospect_values(row)})
    doc.insert()
    return doc.name


def _update_prospect(name: str, row: dict) -> str:
    doc = frappe.get_doc("SEI Prospect", name)
    before_status = doc.lifecycle_status
    for key, value in _prospect_values(row).items():
        if key not in PROTECTED_IMPORT_FIELDS and value is not None:
            doc.set(key, value)
    doc.save()
    if before_status in TERMINAL_STATUSES:
        # Preserve terminal lifecycle protections if validation logic recalculated anything around the update.
        frappe.db.set_value("SEI Prospect", name, "lifecycle_status", before_status, update_modified=False)
    return doc.name


def _create_signal(prospect: str, row: dict, initial: bool = False) -> str:
    doc = frappe.get_doc({"doctype": "SEI Signal", **_signal_values(prospect, row, initial=initial)})
    doc.insert()
    return doc.name


def _update_signal(signal: str, prospect: str, row: dict, initial: bool = False) -> str:
    doc = frappe.get_doc("SEI Signal", signal)
    for key, value in _signal_values(prospect, row, initial=initial).items():
        if key != "prospect" and value is not None:
            doc.set(key, value)
    doc.save()
    return doc.name


def _run_signal_only_row(row: dict, mode: str) -> dict:
    prospect = _match_signal_import_prospect(row)
    if not prospect:
        frappe.throw("No existing SEI Prospect matched for signal-only import.")
    _validate_signal(row)
    duplicate = find_existing_sei_signal(prospect, row)
    if duplicate:
        if mode in (UPDATE_EXISTING, CREATE_OR_UPDATE):
            signal = _update_signal(duplicate["matched_name"], prospect, row)
            _recalculate(prospect)
            return {
                "status": "Updated",
                "action": "Update Signal",
                "prospect": prospect,
                "signal": signal,
                "matched": prospect,
            }
        return {
            "status": "Skipped",
            "action": "Skip",
            "prospect": prospect,
            "matched": prospect,
            "error": duplicate["match_reason"],
        }
    if mode == UPDATE_EXISTING:
        frappe.throw("No existing SEI Signal matched for update.")
    signal = _create_signal(prospect, row)
    _recalculate(prospect)
    return {"status": "Created", "action": "Create Signal", "prospect": prospect, "signal": signal}


def _run_prospect_row(row: dict, mode: str, combined: bool) -> dict:
    _validate_prospect(row, require_create_context=True)
    duplicate = find_existing_sei_prospect(row)
    prospect = duplicate["matched_name"] if duplicate else None
    action = "Create Prospect"
    status = "Created"
    signal = ""
    error = ""

    if duplicate:
        if mode in (UPDATE_EXISTING, CREATE_OR_UPDATE):
            prospect = _update_prospect(prospect, row)
            action = "Update Prospect"
            status = "Updated"
        else:
            return {
                "status": "Skipped",
                "action": "Skip",
                "matched": prospect,
                "prospect": prospect,
                "error": duplicate["match_reason"],
            }
    else:
        if mode == UPDATE_EXISTING:
            frappe.throw("No existing SEI Prospect matched for update.")
        prospect = _create_prospect(row)

    if combined and _has_initial_signal(row):
        _validate_signal(row, prefix="initial_")
        signal_duplicate = find_existing_sei_signal(prospect, row)
        if signal_duplicate:
            if mode in (UPDATE_EXISTING, CREATE_OR_UPDATE):
                signal = _update_signal(signal_duplicate["matched_name"], prospect, row, initial=True)
                action = "Update Signal" if action == "Create Prospect" else action
                status = "Updated" if status != "Created" else status
            else:
                error = signal_duplicate["match_reason"]
        else:
            if mode != UPDATE_EXISTING:
                signal = _create_signal(prospect, row, initial=True)
            else:
                error = "No existing SEI Signal matched for update."
    _recalculate(prospect)
    return {
        "status": status,
        "action": action,
        "prospect": prospect,
        "signal": signal,
        "matched": duplicate["matched_name"] if duplicate else "",
        "error": error,
    }


def run_import_batch(batch: str, dry_run: bool = True) -> dict:
    batch_doc = frappe.get_doc("SEI Import Batch", batch)
    if batch_doc.status == "Cancelled":
        frappe.throw("Cancelled import batches cannot be run.")
    rows = _read_csv(batch_doc)
    import_kind = batch_doc.import_kind or COMBINED
    import_mode = CREATE_OR_UPDATE if dry_run else _normalize_import_mode(batch_doc.import_mode)

    _clear_rows(batch_doc)
    batch_doc.started_at = now_datetime()
    batch_doc.completed_at = None
    batch_doc.imported_by = frappe.session.user
    batch_doc.dry_run = 1 if dry_run else 0
    batch_doc.rows_total = len(rows)
    counters = {"created": 0, "updated": 0, "skipped": 0, "failed": 0}
    errors = []

    for idx, raw in enumerate(rows, start=2):
        row = normalize_import_row(raw)
        savepoint = f"sei_import_row_{idx}"
        frappe.db.savepoint(savepoint)
        try:
            if dry_run:
                classified = classify_import_row(row, import_kind=import_kind, import_mode=import_mode)
                duplicate = classified.get("duplicate")
                action = classified["intended_action"]
                if classified["errors"]:
                    status = "Failed"
                    counters["failed"] += 1
                    error = "; ".join(classified["errors"])
                    errors.append(f"Row {idx}: {error}")
                elif action == "Skip":
                    status = "Duplicate Warning"
                    counters["skipped"] += 1
                    error = duplicate["match_reason"] if duplicate else "Skipped"
                elif action.startswith("Update"):
                    status = "Duplicate Warning" if duplicate else "Updated"
                    counters["updated"] += 1
                    error = duplicate["match_reason"] if duplicate else ""
                else:
                    status = "Pending"
                    counters["created"] += 1
                    error = ""
                _append_row(
                    batch_doc,
                    idx,
                    row,
                    status,
                    action,
                    error=error,
                    matched=duplicate["matched_name"]
                    if duplicate and duplicate.get("matched_doctype") == "SEI Prospect"
                    else "",
                )
            else:
                if import_kind == SIGNAL_ONLY:
                    result = _run_signal_only_row(row, import_mode)
                else:
                    result = _run_prospect_row(row, import_mode, combined=(import_kind == COMBINED))
                status = result.get("status") or "Failed"
                if status == "Created":
                    counters["created"] += 1
                elif status == "Updated":
                    counters["updated"] += 1
                elif status in ("Skipped", "Duplicate Warning"):
                    counters["skipped"] += 1
                _append_row(
                    batch_doc,
                    idx,
                    row,
                    status,
                    result.get("action", ""),
                    error=result.get("error", ""),
                    prospect=result.get("prospect", ""),
                    signal=result.get("signal", ""),
                    matched=result.get("matched", ""),
                )
        except Exception as exc:
            frappe.db.rollback(save_point=savepoint)
            counters["failed"] += 1
            message = str(exc)
            errors.append(f"Row {idx}: {message}")
            _append_row(batch_doc, idx, row, "Failed", "Failed", error=message)

    batch_doc.rows_created = counters["created"]
    batch_doc.rows_updated = counters["updated"]
    batch_doc.rows_skipped = counters["skipped"]
    batch_doc.rows_failed = counters["failed"]
    batch_doc.completed_at = now_datetime()
    batch_doc.error_summary = "\n".join(errors)[:60000]
    if dry_run:
        batch_doc.status = "Dry Run Complete"
    elif counters["failed"]:
        batch_doc.status = (
            "Import Complete with Errors"
            if counters["created"] or counters["updated"] or counters["skipped"]
            else "Failed"
        )
    else:
        batch_doc.status = "Import Complete"
    batch_doc.save()
    frappe.db.commit()
    return {
        "batch": batch_doc.name,
        "status": batch_doc.status,
        "rows_total": batch_doc.rows_total,
        "rows_created": batch_doc.rows_created,
        "rows_updated": batch_doc.rows_updated,
        "rows_skipped": batch_doc.rows_skipped,
        "rows_failed": batch_doc.rows_failed,
    }


def cancel_import_batch(batch: str) -> dict:
    doc = frappe.get_doc("SEI Import Batch", batch)
    if doc.status not in ("Draft", "Failed"):
        frappe.throw("Only Draft or Failed import batches can be cancelled.")
    doc.status = "Cancelled"
    doc.save()
    return {"batch": batch, "status": "Cancelled"}


def backfill_normalized_domains() -> dict:
    updated = 0
    for prospect in frappe.get_all("SEI Prospect", fields=["name", "website", "normalized_domain"]):
        domain = normalize_domain(prospect.website)
        if domain and domain != prospect.normalized_domain:
            frappe.db.set_value(
                "SEI Prospect", prospect.name, "normalized_domain", domain, update_modified=True
            )
            updated += 1
    return {"updated": updated}


def find_duplicate_sei_prospects() -> dict:
    groups = []
    for field in ("normalized_domain", "website", "primary_contact_email", "prospect_name", "source_url"):
        rows = frappe.db.sql(
            f"""
            select `{field}` as value, count(*) as count, group_concat(name order by creation) as names
            from `tabSEI Prospect`
            where ifnull(`{field}`, '') != ''
            group by `{field}` having count(*) > 1
            """,
            as_dict=True,
        )
        for row in rows:
            groups.append(
                {"field": field, "value": row.value, "count": row.count, "names": row.names.split(",")}
            )
    return {"duplicates": groups, "count": len(groups)}


def find_duplicate_sei_signals() -> dict:
    groups = []
    rows = frappe.db.sql(
        """
        select prospect, source_url, count(*) as count, group_concat(name order by creation) as names
        from `tabSEI Signal`
        where ifnull(prospect, '') != '' and ifnull(source_url, '') != ''
        group by prospect, source_url having count(*) > 1
        """,
        as_dict=True,
    )
    for row in rows:
        groups.append(
            {
                "key": "prospect+source_url",
                "prospect": row.prospect,
                "source_url": row.source_url,
                "count": row.count,
                "names": row.names.split(","),
            }
        )
    rows = frappe.db.sql(
        """
        select prospect, signal_type, source_date, count(*) as count,
            group_concat(name order by creation) as names
        from `tabSEI Signal`
        where ifnull(prospect, '') != '' and ifnull(signal_type, '') != '' and source_date is not null
        group by prospect, signal_type, source_date having count(*) > 1
        """,
        as_dict=True,
    )
    for row in rows:
        groups.append(
            {
                "key": "prospect+signal_type+source_date",
                "prospect": row.prospect,
                "signal_type": row.signal_type,
                "source_date": row.source_date,
                "count": row.count,
                "names": row.names.split(","),
            }
        )
    return {"duplicates": groups, "count": len(groups)}


def recalculate_all_prospect_qualifications() -> dict:
    prospects = frappe.get_all("SEI Prospect", pluck="name")
    updated = 0
    for prospect in prospects:
        _recalculate(prospect)
        updated += 1
    return {"updated": updated}


def apply_lifecycle_to_selected_prospects(prospects: list[str]) -> dict:
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
    )

    updated = []
    for prospect in prospects or []:
        if frappe.db.exists("SEI Prospect", prospect):
            updated.append({"prospect": prospect, **apply_lifecycle_status(prospect)})
    return {"updated": updated, "count": len(updated)}


def find_prospects_missing_source_arena() -> dict:
    """Backward-compatible audit: prospects without any signal-derived arena."""
    names = frappe.db.sql(
        """
        SELECT p.name
        FROM `tabSEI Prospect` p
        WHERE NOT EXISTS (
            SELECT 1
            FROM `tabSEI Signal` s
            INNER JOIN `tabSEI Signal Type` st ON st.name = s.signal_type
            WHERE s.prospect = p.name AND COALESCE(st.research_arena, '') != ''
        )
        ORDER BY p.creation DESC
        """,
        pluck=True,
    )
    return {"prospects": names, "count": len(names)}


def find_prospects_missing_signal_evidence() -> dict:
    names = frappe.db.sql(
        """
        select p.name
        from `tabSEI Prospect` p
        left join `tabSEI Signal` s on s.prospect = p.name
        where s.name is null
        order by p.creation desc
        """,
        as_dict=False,
    )
    prospects = [row[0] for row in names]
    return {"prospects": prospects, "count": len(prospects)}


def find_signals_missing_source_url() -> dict:
    names = frappe.get_all("SEI Signal", filters={"source_url": ["in", ["", None]]}, pluck="name")
    return {"signals": names, "count": len(names)}


def find_inferred_qualifying_signal_issues() -> dict:
    names = frappe.get_all(
        "SEI Signal",
        filters={"exclude_from_qualification": 0, "evidence_basis": "Inferred"},
        fields=["name", "prospect", "signal_type", "signal_strength"],
    )
    return {"signals": names, "count": len(names)}


def reset_import_batch_to_draft(batch: str) -> dict:
    doc = frappe.get_doc("SEI Import Batch", batch)
    if doc.status == "Cancelled":
        frappe.throw("Cancelled import batches cannot be reset to Draft.")
    doc.status = "Draft"
    doc.dry_run = 1
    doc.completed_at = None
    doc.error_summary = None
    doc.save()
    return {"batch": batch, "status": "Draft"}
