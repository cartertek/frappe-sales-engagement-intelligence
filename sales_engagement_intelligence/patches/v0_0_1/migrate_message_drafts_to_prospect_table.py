from __future__ import annotations

import frappe


def execute() -> None:
    if not (
        frappe.db.table_exists("SEI Message Draft")
        and frappe.db.table_exists("SEI Prospect Message Draft")
    ):
        return
    drafts = frappe.get_all(
        "SEI Message Draft",
        fields=[
            "name",
            "prospect",
            "platform",
            "from_user",
            "to_contact",
            "cc",
            "subject",
            "body",
            "sent",
            "sent_on",
            "crm_email",
        ],
        order_by="creation, name",
    )
    by_prospect: dict[str, list[dict]] = {}
    for draft in drafts:
        if draft.prospect:
            by_prospect.setdefault(draft.prospect, []).append(draft)
    for prospect, rows in by_prospect.items():
        if not frappe.db.exists("SEI Prospect", prospect):
            continue
        doc = frappe.get_doc("SEI Prospect", prospect)
        existing = {
            row.legacy_message_draft
            for row in (doc.get("message_drafts") or [])
            if row.legacy_message_draft
        }
        changed = False
        for row in rows:
            if row.name in existing:
                continue
            doc.append(
                "message_drafts",
                {
                    "platform": row.platform,
                    "from_user": row.from_user,
                    "to_contact": row.to_contact,
                    "cc": row.cc,
                    "subject": row.subject,
                    "body": row.body,
                    "sent": row.sent,
                    "sent_on": row.sent_on,
                    "crm_email": row.crm_email,
                    "legacy_message_draft": row.name,
                },
            )
            changed = True
        if changed:
            doc.save(ignore_permissions=True)
