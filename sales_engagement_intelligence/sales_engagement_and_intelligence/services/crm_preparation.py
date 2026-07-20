from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
    get_primary_signal,
)
from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import (
    get_prospect_arenas_display,
    get_prospect_playbooks,
    get_prospect_playbooks_display,
)

CRM_LINK_FIELD_BY_DOCTYPE = {
    "CRM Lead": "crm_lead",
    "CRM Deal": "crm_deal",
    "CRM Organization": "crm_organization",
    "Contact": "crm_contact",
}

PROTECTED_LIFECYCLES = ("Rejected", "Do Not Contact")
CONVERTIBLE_QUALIFICATIONS = ("Qualified", "Manually Approved")
COMMERCIAL_RESPONSE_CATEGORIES = ("Positive", "Interested", "Meeting Booked", "Converted to Deal")


def _primary(prospect):
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
        effective_primary_contact,
    )

    return effective_primary_contact(prospect)


def _primary_name(prospect):
    row = _primary(prospect)
    return row.contact_name if row else None


def _primary_email(prospect):
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import emails

    row = _primary(prospect)
    values = emails(row) if row else []
    return values[0] if values else None


def _primary_url(prospect):
    return None


def _doctype_exists(doctype: str) -> bool:
    return bool(frappe.db.exists("DocType", doctype))


def _has_field(doctype: str, fieldname: str) -> bool:
    return _doctype_exists(doctype) and frappe.get_meta(doctype).has_field(fieldname)


def _set_if_exists(payload: dict, doctype: str, fieldname: str, value):
    if value is not None and value != "" and _has_field(doctype, fieldname):
        payload[fieldname] = value


def _first_existing_field(doctype: str, fieldnames: tuple[str, ...]) -> Optional[str]:
    for fieldname in fieldnames:
        if _has_field(doctype, fieldname):
            return fieldname
    return None


def _domain(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = (parsed.hostname or "").lower().strip(".")
    return host[4:] if host.startswith("www.") else host or None


def _same_domain(left: Optional[str], right: Optional[str]) -> bool:
    return bool(_domain(left) and _domain(left) == _domain(right))


def _append_unique_match(matches: list[dict], row, reason: str):
    if not row:
        return
    item = dict(row)
    record_name = item.get("name")
    if not record_name or record_name in {match["name"] for match in matches}:
        return
    item["reason"] = reason
    item.setdefault(
        "title",
        item.get("lead_name")
        or item.get("organization_name")
        or item.get("company_name")
        or item.get("full_name")
        or record_name,
    )
    matches.append(item)


def _get_fields(doctype: str, candidates: tuple[str, ...]) -> list[str]:
    fields = ["name"]
    for field in candidates:
        if field != "name" and _has_field(doctype, field):
            fields.append(field)
    return fields


def _get_all_if_exists(doctype: str, *args, **kwargs):
    if not _doctype_exists(doctype):
        return []
    return frappe.get_all(doctype, *args, **kwargs)


def _set_prospect_values(prospect_name: str, values: dict):
    values = {field: value for field, value in values.items() if _has_field("SEI Prospect", field)}
    if values:
        frappe.db.set_value("SEI Prospect", prospect_name, values, update_modified=True)


def _copy_prospect_metadata(prospect_name: str, target_doctype: str, target_name: str) -> dict:
    """Copy Frappe collaboration metadata from a prospect to a CRM record, idempotently."""
    source_doctype = "SEI Prospect"
    copied = {"assignments": 0, "attachments": 0, "tags": 0, "shares": 0}

    assignments = frappe.get_all(
        "ToDo",
        filters={"reference_type": source_doctype, "reference_name": prospect_name},
        fields=[
            "status",
            "priority",
            "color",
            "date",
            "allocated_to",
            "description",
            "role",
            "assigned_by",
            "sender",
            "assignment_rule",
        ],
    )
    for assignment in assignments:
        duplicate_filters = {
            "reference_type": target_doctype,
            "reference_name": target_name,
            "allocated_to": assignment.get("allocated_to"),
            "role": assignment.get("role"),
            "assignment_rule": assignment.get("assignment_rule"),
        }
        if frappe.db.exists("ToDo", duplicate_filters):
            continue
        frappe.get_doc({
            "doctype": "ToDo",
            "reference_type": target_doctype,
            "reference_name": target_name,
            **{key: value for key, value in assignment.items() if value is not None},
        }).insert(ignore_permissions=True)
        copied["assignments"] += 1

    attachments = frappe.get_all(
        "File",
        filters={"attached_to_doctype": source_doctype, "attached_to_name": prospect_name},
        fields=[
            "file_name",
            "file_url",
            "is_private",
            "file_size",
            "file_type",
            "thumbnail_url",
            "folder",
            "content_hash",
            "attached_to_field",
        ],
    )
    for attachment in attachments:
        duplicate_filters = {
            "attached_to_doctype": target_doctype,
            "attached_to_name": target_name,
            "file_url": attachment.get("file_url"),
            "attached_to_field": attachment.get("attached_to_field"),
        }
        if frappe.db.exists("File", duplicate_filters):
            continue
        frappe.get_doc({
            "doctype": "File",
            "attached_to_doctype": target_doctype,
            "attached_to_name": target_name,
            **{key: value for key, value in attachment.items() if value is not None},
        }).insert(ignore_permissions=True)
        copied["attachments"] += 1

    tags = frappe.get_all(
        "Tag Link",
        filters={"document_type": source_doctype, "document_name": prospect_name},
        fields=["tag", "title"],
    )
    for tag in tags:
        duplicate_filters = {
            "document_type": target_doctype,
            "document_name": target_name,
            "tag": tag.get("tag"),
        }
        if frappe.db.exists("Tag Link", duplicate_filters):
            continue
        frappe.get_doc({
            "doctype": "Tag Link",
            "document_type": target_doctype,
            "document_name": target_name,
            **{key: value for key, value in tag.items() if value is not None},
        }).insert(ignore_permissions=True)
        copied["tags"] += 1

    shares = frappe.get_all(
        "DocShare",
        filters={"share_doctype": source_doctype, "share_name": prospect_name},
        fields=["user", "read", "write", "share", "submit", "everyone"],
    )
    for share in shares:
        duplicate_filters = {
            "share_doctype": target_doctype,
            "share_name": target_name,
            "user": share.get("user"),
            "everyone": share.get("everyone") or 0,
        }
        existing = frappe.db.get_value("DocShare", duplicate_filters, "name")
        values = {key: share.get(key) or 0 for key in ("read", "write", "share", "submit")}
        if existing:
            frappe.db.set_value("DocShare", existing, values, update_modified=False)
            continue
        frappe.get_doc({
            "doctype": "DocShare",
            "share_doctype": target_doctype,
            "share_name": target_name,
            "user": share.get("user"),
            "everyone": share.get("everyone") or 0,
            **values,
        }).insert(ignore_permissions=True)
        copied["shares"] += 1

    return copied


def _assert_not_protected(prospect) -> None:
    if prospect.do_not_contact or prospect.lifecycle_status in PROTECTED_LIFECYCLES:
        frappe.throw("Rejected or Do Not Contact prospects cannot be converted or linked to CRM records.")


def _assert_base_conversion_eligible(prospect) -> None:
    _assert_not_protected(prospect)
    if prospect.qualification_status not in CONVERTIBLE_QUALIFICATIONS:
        frappe.throw("Only Qualified or Manually Approved prospects can be converted to CRM.")


def _has_identity(prospect) -> bool:
    return bool(
        prospect.prospect_name
        and (
            prospect.website
            or _primary_email(prospect)
            or prospect.source_url
            or (prospect.prospect_name and get_prospect_arenas_display(prospect.name))
        )
    )


def _safe_set_link_on_related_doc(
    doctype: str, record_name: str, linked_doctype: str, linked_name: str
) -> bool:
    """Best-effort relationship linking using installed Frappe CRM schema only."""
    if not record_name or not _doctype_exists(doctype) or not frappe.db.exists(doctype, record_name):
        return False

    field_options = frappe.get_meta(doctype).fields
    for field in field_options:
        if field.fieldtype == "Link" and field.options == linked_doctype:
            frappe.db.set_value(doctype, record_name, field.fieldname, linked_name, update_modified=True)
            return True
    return False


def _has_commercial_basis(prospect_name: str) -> bool:
    if not _doctype_exists("SEI Interaction Attribution"):
        return False
    return bool(
        frappe.db.exists(
            "SEI Interaction Attribution",
            {
                "prospect": prospect_name,
                "response_category": ["in", COMMERCIAL_RESPONSE_CATEGORIES],
            },
        )
    )


def _record_conversion_attribution(
    prospect_name: str,
    action: str,
    crm_lead: Optional[str] = None,
    crm_deal: Optional[str] = None,
    notes: Optional[str] = None,
) -> Optional[str]:
    if not _doctype_exists("SEI Interaction Attribution"):
        return None

    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    doc = frappe.new_doc("SEI Interaction Attribution")
    doc.prospect = prospect.name
    if _has_field("SEI Interaction Attribution", "signal"):
        doc.signal = get_primary_signal(prospect.name)
    if _has_field("SEI Interaction Attribution", "thesis"):
        theses = get_prospect_playbooks(prospect.name)
        doc.thesis = theses[0] if theses else None
    if _has_field("SEI Interaction Attribution", "offer"):
        doc.offer = prospect.offer
    if _has_field("SEI Interaction Attribution", "source_arena"):
        doc.source_arena = get_prospect_arenas_display(prospect.name)
    if crm_lead and _has_field("SEI Interaction Attribution", "crm_lead"):
        doc.crm_lead = crm_lead
    if crm_deal and _has_field("SEI Interaction Attribution", "crm_deal"):
        doc.crm_deal = crm_deal
    if _has_field("SEI Interaction Attribution", "interaction_type"):
        doc.interaction_type = "Other"
    if _has_field("SEI Interaction Attribution", "channel"):
        doc.channel = "Other"
    if _has_field("SEI Interaction Attribution", "interaction_date"):
        doc.interaction_date = frappe.utils.now_datetime()
    if _has_field("SEI Interaction Attribution", "response_category"):
        doc.response_category = "Converted to Deal" if action == "Created CRM Deal" else "Other"
    if _has_field("SEI Interaction Attribution", "notes"):
        actor = frappe.session.user or "Unknown user"
        doc.notes = f"{action} by {actor}. {notes or ''}".strip()
    doc.insert(ignore_permissions=True)
    return doc.name


def validate_crm_conversion_eligibility(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    reasons = []

    if prospect.qualification_status not in CONVERTIBLE_QUALIFICATIONS:
        reasons.append("Prospect is not Qualified or Manually Approved.")
    if prospect.do_not_contact:
        reasons.append("Prospect is marked Do Not Contact.")
    if prospect.lifecycle_status in PROTECTED_LIFECYCLES:
        reasons.append(f"Prospect lifecycle is {prospect.lifecycle_status}.")
    if prospect.crm_lead:
        reasons.append("Prospect is already linked to a CRM Lead; use Sync SEI Context instead.")
    if prospect.lifecycle_status != "Ready for CRM Conversion":
        reasons.append("Prospect lifecycle is not Ready for CRM Conversion.")
    if not _has_identity(prospect):
        reasons.append("Prospect is missing enough identity information for CRM preparation.")

    duplicates = find_possible_crm_duplicates(prospect.name)
    if duplicates["has_duplicates"]:
        reasons.append("Possible CRM duplicate found; link it or resolve before creating new CRM records.")

    return {"eligible": not reasons, "reasons": reasons, "duplicates": duplicates}


def _find_crm_lead_duplicates(prospect) -> list[dict]:
    doctype = "CRM Lead"
    fields = _get_fields(
        doctype,
        (
            "lead_name",
            "organization",
            "organization_name",
            "company_name",
            "email",
            "website",
            "sei_prospect",
        ),
    )
    matches: list[dict] = []

    if _has_field(doctype, "sei_prospect"):
        for row in _get_all_if_exists(
            doctype, filters={"sei_prospect": prospect.name}, fields=fields, limit=10
        ):
            _append_unique_match(matches, row, "Matched by SEI Prospect link")

    if _primary_email(prospect):
        for email_field in ("email", "email_id"):
            if _has_field(doctype, email_field):
                for row in _get_all_if_exists(
                    doctype,
                    filters={email_field: _primary_email(prospect)},
                    fields=fields,
                    limit=10,
                ):
                    _append_unique_match(matches, row, "Matched by primary contact email")

    if prospect.website and _has_field(doctype, "website"):
        for row in _get_all_if_exists(
            doctype, filters={"website": prospect.website}, fields=fields, limit=10
        ):
            _append_unique_match(matches, row, "Matched by website")
        for row in _get_all_if_exists(
            doctype, filters={"website": ["like", f"%{_domain(prospect.website)}%"]}, fields=fields, limit=20
        ):
            if _same_domain(prospect.website, row.get("website")):
                _append_unique_match(matches, row, "Matched by normalized domain")

    for name_field in ("lead_name", "organization", "organization_name", "company_name"):
        if prospect.prospect_name and _has_field(doctype, name_field):
            for row in _get_all_if_exists(
                doctype, filters={name_field: prospect.prospect_name}, fields=fields, limit=10
            ):
                _append_unique_match(matches, row, f"Matched by {name_field.replace('_', ' ')}")

    return matches


def _find_crm_organization_duplicates(prospect) -> list[dict]:
    doctype = "CRM Organization"
    fields = _get_fields(doctype, ("organization_name", "website", "domain", "sei_prospect"))
    matches: list[dict] = []

    if prospect.crm_organization and frappe.db.exists(doctype, prospect.crm_organization):
        row = frappe.get_value(doctype, prospect.crm_organization, fields, as_dict=True)
        _append_unique_match(matches, row, "Already linked from SEI Prospect")

    if prospect.prospect_name and _has_field(doctype, "organization_name"):
        for row in _get_all_if_exists(
            doctype, filters={"organization_name": prospect.prospect_name}, fields=fields, limit=10
        ):
            _append_unique_match(matches, row, "Matched by organization name")

    if prospect.website:
        if _has_field(doctype, "website"):
            for row in _get_all_if_exists(
                doctype, filters={"website": prospect.website}, fields=fields, limit=10
            ):
                _append_unique_match(matches, row, "Matched by website")
            for row in _get_all_if_exists(
                doctype,
                filters={"website": ["like", f"%{_domain(prospect.website)}%"]},
                fields=fields,
                limit=20,
            ):
                if _same_domain(prospect.website, row.get("website")):
                    _append_unique_match(matches, row, "Matched by normalized domain")
        if _has_field(doctype, "domain"):
            for row in _get_all_if_exists(
                doctype, filters={"domain": _domain(prospect.website)}, fields=fields, limit=10
            ):
                _append_unique_match(matches, row, "Matched by normalized domain")

    return matches


def _find_crm_contact_duplicates(prospect) -> list[dict]:
    doctype = "Contact"
    fields = _get_fields(
        doctype,
        ("full_name", "first_name", "last_name", "email_id", "company_name"),
    )
    matches: list[dict] = []

    if prospect.crm_contact and frappe.db.exists(doctype, prospect.crm_contact):
        row = frappe.get_value(doctype, prospect.crm_contact, fields, as_dict=True)
        _append_unique_match(matches, row, "Already linked from SEI Prospect")

    if _primary_email(prospect):
        if _has_field(doctype, "email_id"):
            for row in _get_all_if_exists(
                doctype,
                filters={"email_id": _primary_email(prospect)},
                fields=fields,
                limit=10,
            ):
                _append_unique_match(matches, row, "Matched by contact email")
        if _doctype_exists("Contact Email"):
            for email_row in frappe.get_all(
                "Contact Email",
                filters={"email_id": _primary_email(prospect), "parenttype": "Contact"},
                fields=["parent"],
                limit=10,
            ):
                row = frappe.get_value(doctype, email_row.parent, fields, as_dict=True)
                _append_unique_match(matches, row, "Matched by contact email")

    if _primary_name(prospect):
        name_field = _first_existing_field(doctype, ("full_name", "first_name"))
        if name_field:
            filters = {name_field: _primary_name(prospect)}
            if _has_field(doctype, "company_name") and prospect.prospect_name:
                filters["company_name"] = prospect.prospect_name
            for row in _get_all_if_exists(doctype, filters=filters, fields=fields, limit=10):
                _append_unique_match(matches, row, "Matched by contact name and company")

    return matches


def _find_crm_deal_duplicates(prospect) -> list[dict]:
    doctype = "CRM Deal"
    fields = _get_fields(
        doctype,
        ("deal_name", "lead", "lead_name", "organization", "organization_name", "status", "sei_prospect"),
    )
    matches: list[dict] = []

    if _has_field(doctype, "sei_prospect"):
        for row in _get_all_if_exists(
            doctype, filters={"sei_prospect": prospect.name}, fields=fields, limit=10
        ):
            _append_unique_match(matches, row, "Matched by SEI Prospect link")

    for field, value in (
        ("lead", prospect.crm_lead),
        ("organization", prospect.crm_organization),
        ("organization_name", prospect.prospect_name),
    ):
        if value and _has_field(doctype, field):
            filters = {field: value}
            if _has_field(doctype, "status"):
                filters["status"] = ["not in", ("Won", "Lost", "Closed")]
            for row in _get_all_if_exists(doctype, filters=filters, fields=fields, limit=10):
                _append_unique_match(matches, row, f"Matched by open {field.replace('_', ' ')} deal")

    title_field = _first_existing_field(doctype, ("deal_name", "lead_name", "organization_name"))
    if title_field and prospect.prospect_name:
        for row in _get_all_if_exists(
            doctype, filters={title_field: prospect.prospect_name}, fields=fields, limit=10
        ):
            _append_unique_match(matches, row, f"Matched by {title_field.replace('_', ' ')}")

    return matches


def find_possible_crm_duplicates(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    result = {
        "has_duplicates": False,
        "crm_leads": _find_crm_lead_duplicates(prospect),
        "crm_organizations": _find_crm_organization_duplicates(prospect),
        "crm_contacts": _find_crm_contact_duplicates(prospect),
        "crm_deals": _find_crm_deal_duplicates(prospect),
    }
    result["has_duplicates"] = any(result[key] for key in result if key != "has_duplicates")
    return result


def find_possible_crm_lead_duplicates(prospect) -> list[dict]:
    return _find_crm_lead_duplicates(prospect)


def build_crm_lead_payload(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    lead = {"doctype": "CRM Lead"}

    title = _primary_name(prospect) or prospect.prospect_name or prospect.name
    for field in ("lead_name", "first_name", "organization", "organization_name", "company_name", "title"):
        _set_if_exists(lead, "CRM Lead", field, title)

    _set_if_exists(lead, "CRM Lead", "email", _primary_email(prospect))
    _set_if_exists(lead, "CRM Lead", "email_id", _primary_email(prospect))
    _set_if_exists(lead, "CRM Lead", "website", prospect.website)
    _set_if_exists(lead, "CRM Lead", "status", "New")
    _set_if_exists(lead, "CRM Lead", "organization", prospect.crm_organization)

    _set_if_exists(lead, "CRM Lead", "sei_prospect", prospect.name)
    _set_if_exists(lead, "CRM Lead", "sei_source_arena", get_prospect_arenas_display(prospect.name))
    _set_if_exists(lead, "CRM Lead", "sei_playbook", get_prospect_playbooks_display(prospect.name))
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
    _set_if_exists(
        payload, "CRM Organization", "domain", prospect.normalized_domain or _domain(prospect.website)
    )
    return payload


def build_crm_contact_payload(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    payload = {"doctype": "Contact"}
    _set_if_exists(payload, "Contact", "first_name", _primary_name(prospect) or prospect.prospect_name)
    _set_if_exists(payload, "Contact", "full_name", _primary_name(prospect))
    _set_if_exists(payload, "Contact", "email_id", _primary_email(prospect))
    _set_if_exists(payload, "Contact", "company_name", prospect.prospect_name)
    if _primary_email(prospect) and _has_field("Contact", "email_ids"):
        payload["email_ids"] = [{"email_id": _primary_email(prospect), "is_primary": 1}]
    return payload


def build_crm_deal_payload(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    payload = {"doctype": "CRM Deal"}
    title = prospect.prospect_name or _primary_name(prospect) or prospect.name
    _set_if_exists(payload, "CRM Deal", "deal_name", title)
    _set_if_exists(payload, "CRM Deal", "lead_name", title)
    _set_if_exists(payload, "CRM Deal", "organization_name", prospect.prospect_name)
    _set_if_exists(payload, "CRM Deal", "lead", prospect.crm_lead)
    _set_if_exists(payload, "CRM Deal", "organization", prospect.crm_organization)
    _set_if_exists(payload, "CRM Deal", "status", "Qualification")
    _set_if_exists(payload, "CRM Deal", "sei_prospect", prospect.name)
    _set_if_exists(payload, "CRM Deal", "sei_source_arena", get_prospect_arenas_display(prospect.name))
    _set_if_exists(payload, "CRM Deal", "sei_playbook", get_prospect_playbooks_display(prospect.name))
    _set_if_exists(payload, "CRM Deal", "sei_primary_signal", get_primary_signal(prospect.name))
    return payload


def sync_sei_context_to_crm(prospect_name: str) -> dict:
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    result = {
        "crm_lead_synced": False,
        "crm_deal_synced": False,
        "crm_organization_synced": False,
        "crm_contact_synced": False,
    }

    if prospect.crm_lead and frappe.db.exists("CRM Lead", prospect.crm_lead):
        values = {}
        for field, value in {
            "sei_prospect": prospect.name,
            "sei_source_arena": get_prospect_arenas_display(prospect.name),
            "sei_playbook": get_prospect_playbooks_display(prospect.name),
            "sei_qualification_summary": prospect.qualification_explanation or prospect.signal_summary,
            "organization": prospect.crm_organization,
        }.items():
            if _has_field("CRM Lead", field):
                values[field] = value
        if values:
            frappe.db.set_value("CRM Lead", prospect.crm_lead, values, update_modified=True)
            result["crm_lead_synced"] = True

    if prospect.crm_deal and frappe.db.exists("CRM Deal", prospect.crm_deal):
        values = {}
        for field, value in {
            "sei_prospect": prospect.name,
            "sei_source_arena": get_prospect_arenas_display(prospect.name),
            "sei_playbook": get_prospect_playbooks_display(prospect.name),
            "sei_primary_signal": get_primary_signal(prospect.name),
            "lead": prospect.crm_lead,
            "organization": prospect.crm_organization,
        }.items():
            if _has_field("CRM Deal", field):
                values[field] = value
        if values:
            frappe.db.set_value("CRM Deal", prospect.crm_deal, values, update_modified=True)
            result["crm_deal_synced"] = True

    if prospect.crm_organization and prospect.crm_lead:
        result["crm_organization_synced"] = _safe_set_link_on_related_doc(
            "CRM Lead", prospect.crm_lead, "CRM Organization", prospect.crm_organization
        )

    if prospect.crm_contact:
        lead_linked = bool(
            prospect.crm_lead
            and _safe_set_link_on_related_doc(
                "CRM Contacts", prospect.crm_contact, "CRM Lead", prospect.crm_lead
            )
        )
        org_linked = bool(
            prospect.crm_organization
            and _safe_set_link_on_related_doc(
                "Contact", prospect.crm_contact, "CRM Organization", prospect.crm_organization
            )
        )
        result["crm_contact_synced"] = lead_linked or org_linked

    return result


def create_crm_lead_from_prospect(prospect_name: str, options: Optional[dict] = None) -> dict:
    options = options or {}
    eligibility = validate_crm_conversion_eligibility(prospect_name)
    duplicate_override = bool(options.get("allow_duplicate"))
    if not eligibility["eligible"]:
        blocking_reasons = eligibility["reasons"][:]
        if duplicate_override:
            blocking_reasons = [reason for reason in blocking_reasons if "duplicate" not in reason.lower()]
        if blocking_reasons:
            frappe.throw("CRM Lead cannot be created: " + "; ".join(blocking_reasons))

    payload = build_crm_lead_payload(prospect_name)
    lead = frappe.get_doc(payload)
    lead.insert()
    metadata = _copy_prospect_metadata(prospect_name, "CRM Lead", lead.name)

    _set_prospect_values(prospect_name, {"crm_lead": lead.name})
    sync = sync_sei_context_to_crm(prospect_name)

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
    )

    lifecycle = apply_lifecycle_status(prospect_name)
    audit = _record_conversion_attribution(
        prospect_name,
        "Created CRM Lead",
        crm_lead=lead.name,
        notes="Duplicate override used." if duplicate_override else None,
    )
    return {"crm_lead": lead.name, **lifecycle, "sync": sync, "metadata": metadata, "audit": audit}


def create_or_link_crm_organization(prospect_name: str, options: Optional[dict] = None) -> dict:
    options = options or {}
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    _assert_base_conversion_eligible(prospect)

    existing = options.get("existing_record")
    if existing:
        return link_existing_crm_record(prospect_name, "CRM Organization", existing)

    if not (
        prospect.prospect_name and (prospect.website or prospect.normalized_domain or prospect.source_url)
    ):
        frappe.throw("CRM Organization creation requires a clear company identity.")

    duplicates = _find_crm_organization_duplicates(prospect)
    if duplicates and not options.get("allow_duplicate"):
        frappe.throw(
            "Possible CRM Organization duplicate found; link the existing organization or use an override."
        )

    payload = build_crm_organization_payload(prospect_name)
    organization = frappe.get_doc(payload)
    organization.insert()
    metadata = _copy_prospect_metadata(prospect_name, "CRM Organization", organization.name)
    _set_prospect_values(prospect_name, {"crm_organization": organization.name})
    sync = sync_sei_context_to_crm(prospect_name)
    audit = _record_conversion_attribution(
        prospect_name, "Created CRM Organization", notes=f"CRM Organization: {organization.name}"
    )
    return {"crm_organization": organization.name, "sync": sync, "metadata": metadata, "audit": audit}


def create_or_link_crm_contact(prospect_name: str, options: Optional[dict] = None) -> dict:
    options = options or {}
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    _assert_base_conversion_eligible(prospect)

    existing = options.get("existing_record")
    if existing:
        return link_existing_crm_record(prospect_name, "Contact", existing)

    if not (_primary_name(prospect) or _primary_email(prospect) or _primary_url(prospect)):
        frappe.throw("CRM Contact creation requires a verified contact name, email, or URL.")

    duplicates = _find_crm_contact_duplicates(prospect)
    if duplicates and not options.get("allow_duplicate"):
        frappe.throw(
            "Possible CRM Contact duplicate found; link the existing contact or use a manager override."
        )

    payload = build_crm_contact_payload(prospect_name)
    contact = frappe.get_doc(payload)
    contact.insert()
    metadata = _copy_prospect_metadata(prospect_name, "Contact", contact.name)
    if prospect.crm_deal and _has_field("CRM Deal", "contact"):
        frappe.db.set_value("CRM Deal", prospect.crm_deal, "contact", contact.name, update_modified=True)
    _set_prospect_values(prospect_name, {"crm_contact": contact.name})
    sync = sync_sei_context_to_crm(prospect_name)
    audit = _record_conversion_attribution(
        prospect_name, "Created CRM Contact", notes=f"CRM Contact: {contact.name}"
    )
    return {"crm_contact": contact.name, "sync": sync, "metadata": metadata, "audit": audit}


def create_crm_deal_from_prospect(prospect_name: str, options: Optional[dict] = None) -> dict:
    options = options or {}
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    _assert_base_conversion_eligible(prospect)

    if not prospect.crm_lead and not options.get("allow_direct_deal"):
        frappe.throw("CRM Deal creation requires a linked CRM Lead unless direct Deal creation is confirmed.")
    if not (_has_commercial_basis(prospect.name) or options.get("manager_override")):
        frappe.throw(
            "CRM Deal creation requires positive interest, meeting booked, commercial basis, or override."
        )

    duplicates = _find_crm_deal_duplicates(prospect)
    if duplicates and not options.get("allow_duplicate"):
        frappe.throw("Possible CRM Deal duplicate found; link the existing deal or use a manager override.")

    payload = build_crm_deal_payload(prospect_name)
    deal = frappe.get_doc(payload)
    deal.insert()
    _set_prospect_values(prospect_name, {"crm_deal": deal.name})
    sync = sync_sei_context_to_crm(prospect_name)

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
    )

    lifecycle = apply_lifecycle_status(prospect_name)
    audit = _record_conversion_attribution(
        prospect_name,
        "Created CRM Deal",
        crm_lead=prospect.crm_lead,
        crm_deal=deal.name,
        notes="Manager override used." if options.get("manager_override") else None,
    )
    return {"crm_deal": deal.name, **lifecycle, "sync": sync, "audit": audit}


def link_existing_crm_record(prospect_name: str, doctype: str, record_name: str) -> dict:
    if doctype not in CRM_LINK_FIELD_BY_DOCTYPE:
        frappe.throw(f"Unsupported CRM record type: {doctype}")
    if not frappe.db.exists(doctype, record_name):
        frappe.throw(f"{doctype} {record_name} does not exist.")

    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    _assert_not_protected(prospect)

    fieldname = CRM_LINK_FIELD_BY_DOCTYPE[doctype]
    current = prospect.get(fieldname)
    if current and current != record_name:
        frappe.throw(
            f"SEI Prospect is already linked to {doctype} {current}; unlink or override manually first."
        )

    _set_prospect_values(prospect_name, {fieldname: record_name})

    if _has_field(doctype, "sei_prospect"):
        frappe.db.set_value(doctype, record_name, "sei_prospect", prospect_name, update_modified=True)

    metadata = (
        _copy_prospect_metadata(prospect_name, doctype, record_name)
        if doctype in ("CRM Lead", "CRM Organization", "Contact")
        else {}
    )
    sync = sync_sei_context_to_crm(prospect_name)

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
    )

    lifecycle = apply_lifecycle_status(prospect_name) if doctype in ("CRM Lead", "CRM Deal") else {}
    audit = _record_conversion_attribution(
        prospect_name,
        f"Linked Existing {doctype}",
        crm_lead=record_name if doctype == "CRM Lead" else prospect.crm_lead,
        crm_deal=record_name if doctype == "CRM Deal" else prospect.crm_deal,
        notes=f"Linked {doctype} {record_name}.",
    )
    return {fieldname: record_name, **lifecycle, "sync": sync, "metadata": metadata, "audit": audit}


def _contact_payload_for_row(prospect, row) -> dict:
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import emails

    payload = {"doctype": "Contact"}
    _set_if_exists(
        payload, "Contact", "first_name", row.contact_name or row.contact_role or prospect.prospect_name
    )
    _set_if_exists(payload, "Contact", "full_name", row.contact_name)
    _set_if_exists(payload, "Contact", "email_id", (emails(row) or [None])[0])
    _set_if_exists(payload, "Contact", "company_name", prospect.prospect_name)
    if emails(row) and _has_field("Contact", "email_ids"):
        payload["email_ids"] = [
            {"email_id": email, "is_primary": 1 if i == 0 else 0} for i, email in enumerate(emails(row))
        ]
    return payload


def _find_contact_by_row(prospect, row):
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import emails

    for email in emails(row):
        if _has_field("Contact", "email_id"):
            found = frappe.db.get_value("Contact", {"email_id": email}, "name")
            if found:
                return found
        if _doctype_exists("Contact Email"):
            found = frappe.db.get_value(
                "Contact Email", {"email_id": email, "parenttype": "Contact"}, "parent"
            )
            if found:
                return found
    return None


def _upsert_contact_row(prospect, row):
    name = (
        row.crm_contact
        if row.crm_contact and frappe.db.exists("Contact", row.crm_contact)
        else _find_contact_by_row(prospect, row)
    )
    payload = _contact_payload_for_row(prospect, row)
    if name:
        doc = frappe.get_doc("Contact", name)
        for key, value in payload.items():
            if key == "doctype" or value in (None, "") or not hasattr(doc, key):
                continue
            field = frappe.get_meta("Contact").get_field(key)
            if field and field.fieldtype in ("Table", "Table MultiSelect"):
                doc.set(key, value)
            else:
                setattr(doc, key, value)
        doc.save()
    else:
        doc = frappe.get_doc(payload)
        doc.insert()
    _copy_prospect_metadata(prospect.name, "Contact", doc.name)
    row.db_set("crm_contact", doc.name, update_modified=False)
    if prospect.crm_organization:
        _safe_set_link_on_related_doc("Contact", doc.name, "CRM Organization", prospect.crm_organization)
    return doc


def _lead_payload_for_contact(prospect, row):
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import emails

    payload = {"doctype": "CRM Lead"}
    title = row.contact_name or prospect.prospect_name
    for field in ("lead_name", "first_name", "title"):
        _set_if_exists(payload, "CRM Lead", field, title)
    _set_if_exists(payload, "CRM Lead", "email", (emails(row) or [None])[0])
    _set_if_exists(payload, "CRM Lead", "email_id", (emails(row) or [None])[0])
    _set_if_exists(payload, "CRM Lead", "organization", prospect.crm_organization)
    _set_if_exists(payload, "CRM Lead", "website", prospect.website)
    _set_if_exists(payload, "CRM Lead", "status", "New")
    _set_if_exists(payload, "CRM Lead", "sei_prospect", prospect.name)
    _set_if_exists(payload, "CRM Lead", "sei_playbook", get_prospect_playbooks_display(prospect.name))
    return payload


def convert_prospect_to_crm_leads(prospect_name: str) -> dict:
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.contacts import (
        emails,
        populated_contacts,
        primary_contacts,
    )

    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    _assert_base_conversion_eligible(prospect)
    if prospect.lifecycle_status != "Ready for CRM Conversion":
        frappe.throw("Prospect must be in Ready for CRM Conversion status.")
    primaries = primary_contacts(prospect)
    if not primaries:
        frappe.throw("At least one populated primary contact is required.")
    # organization upsert
    org_dupes = _find_crm_organization_duplicates(prospect)
    if prospect.crm_organization and frappe.db.exists("CRM Organization", prospect.crm_organization):
        org = frappe.get_doc("CRM Organization", prospect.crm_organization)
    elif org_dupes:
        org = frappe.get_doc("CRM Organization", org_dupes[0]["name"])
    else:
        org = frappe.get_doc(build_crm_organization_payload(prospect_name))
        org.insert()
    _copy_prospect_metadata(prospect_name, "CRM Organization", org.name)
    _set_prospect_values(prospect_name, {"crm_organization": org.name})
    prospect = frappe.get_doc("SEI Prospect", prospect_name)
    contacts = [_upsert_contact_row(prospect, row) for row in populated_contacts(prospect)]
    leads = []
    for row in primary_contacts(prospect):
        existing = None
        for email in emails(row):
            for field in ("email", "email_id"):
                if _has_field("CRM Lead", field):
                    existing = frappe.db.get_value("CRM Lead", {field: email}, "name")
                    if existing:
                        break
            if existing:
                break
        if existing:
            lead = frappe.get_doc("CRM Lead", existing)
        else:
            lead = frappe.get_doc(_lead_payload_for_contact(prospect, row))
            lead.insert()
        _copy_prospect_metadata(prospect_name, "CRM Lead", lead.name)
        leads.append(lead.name)
    _set_prospect_values(
        prospect_name,
        {
            "crm_lead": sorted(leads)[0],
            "crm_contact": sorted(c.name for c in contacts)[0] if contacts else None,
        },
    )
    frappe.db.set_value(
        "SEI Prospect", prospect_name, "lifecycle_status", "Converted to CRM Lead", update_modified=True
    )
    return {
        "crm_organization": org.name,
        "crm_contacts": [c.name for c in contacts],
        "crm_leads": leads,
        "lifecycle_status": "Converted to CRM Lead",
    }
