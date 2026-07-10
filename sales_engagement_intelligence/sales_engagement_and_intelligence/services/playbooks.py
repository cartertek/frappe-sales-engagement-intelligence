from __future__ import annotations

import frappe


def apply_playbook_defaults(prospect: str) -> dict:
    """Fill blank prospect guidance fields from the assigned playbook.

    This is intentionally user-triggered and conservative: it never overwrites
    populated fields, never recalculates qualification, never changes lifecycle,
    and never creates CRM/outreach records.
    """

    doc = frappe.get_doc("SEI Prospect", prospect)
    if not doc.sei_playbook:
        frappe.throw("Select a SEI Playbook before applying playbook defaults.")

    playbook = frappe.get_doc("SEI Playbook", doc.sei_playbook)
    changed: list[str] = []
    skipped: list[str] = []

    def fill_if_blank(fieldname: str, value):
        if value in (None, ""):
            return
        if doc.get(fieldname):
            skipped.append(fieldname)
            return
        doc.set(fieldname, value)
        changed.append(fieldname)

    fill_if_blank("thesis", playbook.default_thesis)
    fill_if_blank("offer", playbook.default_offer)

    guidance_parts = []
    if playbook.recommended_first_action:
        guidance_parts.append(f"First action: {playbook.recommended_first_action}")
    if playbook.likely_contact_roles:
        guidance_parts.append(f"Likely contacts: {playbook.likely_contact_roles}")
    if playbook.qualifying_signal_guidance:
        guidance_parts.append(f"Signals: {playbook.qualifying_signal_guidance}")
    fill_if_blank("playbook_guidance", "\n".join(guidance_parts))

    if playbook.likely_contact_roles:
        fill_if_blank("contact_target_notes", playbook.likely_contact_roles)

    if not doc.suggested_message_template:
        template = _find_default_template(playbook.name, playbook.default_thesis, doc.prospect_type)
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
        "message": (
            "Playbook defaults applied to blank fields only."
            if changed
            else "No blank fields needed updates."
        ),
    }


def _find_default_template(playbook: str, thesis: str | None, prospect_type: str | None) -> str | None:
    filters = {"active": 1, "playbook": playbook}
    if prospect_type:
        exact = frappe.get_all(
            "SEI Message Template",
            filters={**filters, "prospect_type": prospect_type},
            pluck="name",
            order_by="modified desc",
            limit=1,
        )
        if exact:
            return exact[0]
    rows = frappe.get_all(
        "SEI Message Template",
        filters=filters,
        pluck="name",
        order_by="modified desc",
        limit=1,
    )
    if rows:
        return rows[0]
    if thesis:
        rows = frappe.get_all(
            "SEI Message Template",
            filters={"active": 1, "thesis": thesis},
            pluck="name",
            order_by="modified desc",
            limit=1,
        )
        if rows:
            return rows[0]
    return None
