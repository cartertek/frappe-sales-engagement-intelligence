from __future__ import annotations

import frappe


def count_sent_message_drafts(prospect) -> int:
    """Count sent draft child rows from a Prospect document or name."""
    if hasattr(prospect, "get"):
        return sum(1 for row in prospect.get("message_drafts") or [] if row.get("sent"))
    if not prospect or not _can_sync():
        return 0
    return frappe.db.count(
        "SEI Prospect Message Draft",
        {"parent": prospect, "parenttype": "SEI Prospect", "parentfield": "message_drafts", "sent": 1},
    )


def sync_prospect_emails_sent(prospect: str | None) -> None:
    if not prospect or not _can_sync() or not frappe.db.exists("SEI Prospect", prospect):
        return
    emails_sent = count_sent_message_drafts(prospect)
    current = frappe.db.get_value("SEI Prospect", prospect, "emails_sent") or 0
    if int(current) == emails_sent:
        return

    frappe.db.set_value(
        "SEI Prospect",
        prospect,
        "emails_sent",
        emails_sent,
        update_modified=True,
    )
    frappe.get_doc("SEI Prospect", prospect).notify_update()


def sync_all_prospect_emails_sent() -> None:
    if _can_sync():
        for prospect in frappe.get_all("SEI Prospect", pluck="name"):
            sync_prospect_emails_sent(prospect)


def _can_sync() -> bool:
    return all((
        frappe.db.table_exists("SEI Prospect"),
        frappe.db.table_exists("SEI Prospect Message Draft"),
        frappe.db.has_column("SEI Prospect", "emails_sent"),
        frappe.db.has_column("SEI Prospect Message Draft", "sent"),
    ))
