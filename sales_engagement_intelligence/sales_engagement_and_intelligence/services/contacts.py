from __future__ import annotations

import re

import frappe


def emails(contact) -> list[str]:
    return list(
        dict.fromkeys(x.strip() for x in re.split(r"[\n,;]+", contact.get("emails") or "") if x.strip())
    )


def populated_contacts(prospect) -> list:
    return [c for c in (prospect.get("contacts") or []) if c.get("contact_name") or emails(c)]


def primary_contacts(prospect) -> list:
    return sorted(
        [c for c in populated_contacts(prospect) if c.get("is_primary")],
        key=lambda c: ((c.get("contact_name") or "").casefold(), c.get("contact_role") or ""),
    )


def effective_primary_contact(prospect):
    rows = primary_contacts(prospect)
    return rows[0] if rows else None


def ensure_required_contact_roles(prospect) -> bool:
    if not prospect.get("name"):
        return False
    playbooks = (
        frappe.db.get_value("SEI Prospect", prospect.name, "playbooks") or prospect.get("playbooks") or ""
    )
    names = [x.strip() for x in playbooks.split(",") if x.strip()]
    required = []
    for name in names:
        required += [
            r.contact_role
            for r in frappe.get_all(
                "SEI Playbook Contact Role",
                filters={"parent": name, "parenttype": "SEI Playbook"},
                fields=["contact_role"],
                order_by="idx",
            )
        ]
    existing = {c.contact_role for c in prospect.get("contacts") or []}
    changed = False
    for role in sorted(set(required), key=str.casefold):
        if role not in existing:
            prospect.append("contacts", {"contact_role": role})
            changed = True
    return changed


def sync_required_contact_roles(prospect_name: str) -> bool:
    """Persist missing Playbook contact-role placeholders without running Prospect validation."""
    if not prospect_name or not frappe.db.exists("SEI Prospect", prospect_name):
        return False

    playbooks = frappe.db.get_value("SEI Prospect", prospect_name, "playbooks") or ""
    names = [value.strip() for value in playbooks.split(",") if value.strip()]
    required = {
        row.contact_role
        for name in names
        for row in frappe.get_all(
            "SEI Playbook Contact Role",
            filters={"parent": name, "parenttype": "SEI Playbook"},
            fields=["contact_role"],
            order_by="idx",
        )
        if row.contact_role
    }
    existing = set(
        frappe.get_all(
            "SEI Prospect Contact",
            filters={
                "parent": prospect_name,
                "parenttype": "SEI Prospect",
                "parentfield": "contacts",
            },
            pluck="contact_role",
        )
    )
    changed = False
    next_idx = (
        frappe.db.sql(
            """SELECT COALESCE(MAX(idx), 0) FROM `tabSEI Prospect Contact`
            WHERE parent=%s AND parenttype='SEI Prospect' AND parentfield='contacts'""",
            prospect_name,
        )[0][0]
        + 1
    )
    for role in sorted(required - existing, key=str.casefold):
        frappe.get_doc(
            {
                "doctype": "SEI Prospect Contact",
                "parent": prospect_name,
                "parenttype": "SEI Prospect",
                "parentfield": "contacts",
                "idx": next_idx,
                "contact_role": role,
            }
        ).db_insert()
        next_idx += 1
        changed = True
    return changed
