from __future__ import annotations

import re
from dataclasses import dataclass

import frappe
from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import (
    get_prospect_theses,
    get_signal_type_thesis,
)

VARIABLES = (
    "prospect_name",
    "website",
    "source_arena",
    "signal_summary",
    "qualification_explanation",
    "thesis",
    "offer",
    "asset_url",
    "primary_contact_name",
    "primary_contact_role",
)
VARIABLE_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")


@dataclass
class RenderedDraft:
    subject: str
    body: str
    missing_variables: list[str]
    variables: dict[str, str]


def preview_message_draft(prospect: str, template: str) -> dict:
    """Render a manual-review message draft without sending or mutating workflow state."""

    prospect_doc = frappe.get_doc("SEI Prospect", prospect)
    template_doc = frappe.get_doc("SEI Message Template", template)
    if not template_doc.active:
        frappe.throw("Message template is inactive.")

    context = build_context(prospect_doc, template_doc)
    subject, subject_missing = render_template(template_doc.subject_template or "", context)
    body, body_missing = render_template(template_doc.body_template or "", context)
    missing = sorted(set(subject_missing + body_missing))

    return {
        "prospect": prospect_doc.name,
        "template": template_doc.name,
        "channel": template_doc.channel,
        "subject": subject,
        "body": body,
        "missing_variables": missing,
        "variables": context,
        "safety": {
            "sent": False,
            "communication_created": False,
            "lifecycle_changed": False,
            "crm_record_created": False,
        },
    }


def build_context(prospect_doc, template_doc) -> dict[str, str]:
    derived_theses = get_prospect_theses(prospect_doc.name)
    thesis_name = (derived_theses[0] if derived_theses else None) or template_doc.thesis or ""
    thesis_label = ", ".join(derived_theses) if derived_theses else thesis_name
    offer = prospect_doc.offer or ""
    asset = template_doc.asset or ""

    if thesis_name and frappe.db.exists("SEI Thesis", thesis_name):
        thesis = frappe.get_doc("SEI Thesis", thesis_name)
        thesis_label = thesis.thesis_name or thesis.name
        offer = offer or thesis.default_offer or ""
        asset = asset or thesis.default_asset or ""

    if not asset and getattr(prospect_doc, "sei_playbook", None):
        default_asset = frappe.db.get_value("SEI Playbook", prospect_doc.sei_playbook, "default_asset")
        asset = default_asset or ""

    asset_url = ""
    if asset and frappe.db.exists("SEI Asset", asset):
        asset_url = frappe.db.get_value("SEI Asset", asset, "url") or ""

    signal_summary = prospect_doc.signal_summary or ""
    if not signal_summary:
        signal_summary = _primary_signal_summary(prospect_doc.name)

    return {
        "prospect_name": prospect_doc.prospect_name or "",
        "website": prospect_doc.website or "",
        "source_arena": prospect_doc.source_arena or "",
        "signal_summary": signal_summary,
        "qualification_explanation": prospect_doc.qualification_explanation or "",
        "thesis": thesis_label or "",
        "offer": offer or template_doc.get("default_offer") or "",
        "asset_url": asset_url,
        "primary_contact_name": prospect_doc.primary_contact_name or "",
        "primary_contact_role": prospect_doc.primary_contact_role or "",
    }


def _primary_signal_summary(prospect: str) -> str:
    rows = frappe.get_all(
        "SEI Signal",
        filters={"prospect": prospect},
        fields=["signal_type", "signal_strength", "evidence_basis", "evidence_notes"],
        order_by="source_date desc, creation desc",
        limit=1,
    )
    if not rows:
        return ""
    row = rows[0]
    signal_label = frappe.db.get_value("SEI Signal Type", row.signal_type, "signal_type_name") or row.signal_type
    parts = [row.signal_strength, row.evidence_basis, signal_label]
    summary = " ".join([part for part in parts if part])
    if row.evidence_notes:
        summary = f"{summary}: {row.evidence_notes}" if summary else row.evidence_notes
    return summary


def render_template(template: str, context: dict[str, str]) -> tuple[str, list[str]]:
    missing: list[str] = []

    def replace(match):
        key = match.group(1)
        value = context.get(key, "")
        if value in (None, ""):
            missing.append(key)
            return ""
        return str(value)

    return VARIABLE_RE.sub(replace, template or ""), missing
