from __future__ import annotations

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.services.taxonomy import (
    get_prospect_playbooks,
)


def apply_playbook_defaults(prospect: str) -> dict:
    """Apply defaults from the first alphabetically derived prospect playbook."""
    doc = frappe.get_doc("SEI Prospect", prospect)
    names = get_prospect_playbooks(prospect)
    if not names:
        frappe.throw("This prospect has no Playbook derived from its Signals.")
    playbook = frappe.get_doc("SEI Playbook", names[0])
    changed = []
    skipped = []

    def fill(field, value):
        if value in (None, ""):
            return
        if doc.get(field):
            skipped.append(field)
            return
        doc.set(field, value)
        changed.append(field)

    fill("offer", playbook.default_offer)
    roles = ", ".join(r.contact_role for r in (playbook.get("contact_roles") or []))
    fill("contact_target_notes", roles)
    if not doc.suggested_message_template:
        template = _find_default_template(playbook.name, doc.prospect_type)
        if template:
            doc.suggested_message_template = template
            changed.append("suggested_message_template")
    if changed:
        doc.save()
    return {
        "prospect": doc.name,
        "playbook": playbook.name,
        "changed_fields": changed,
        "skipped_populated_fields": skipped,
        "message": "Playbook defaults applied to blank fields only."
        if changed
        else "No blank fields needed updates.",
    }


def _find_default_template(playbook: str, prospect_type: str | None) -> str | None:
    filters = {"active": 1, "playbook": playbook}
    if prospect_type:
        rows = frappe.get_all(
            "SEI Message Template",
            filters={**filters, "prospect_type": prospect_type},
            pluck="name",
            order_by="modified desc",
            limit=1,
        )
        if rows:
            return rows[0]
    rows = frappe.get_all(
        "SEI Message Template", filters=filters, pluck="name", order_by="modified desc", limit=1
    )
    return rows[0] if rows else None
