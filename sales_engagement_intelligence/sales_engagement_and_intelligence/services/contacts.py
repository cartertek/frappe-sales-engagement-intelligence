from __future__ import annotations

import re

import frappe


def emails(contact) -> list[str]:
    return list(
        dict.fromkeys(x.strip() for x in re.split(r"[\n,;]+", contact.get("emails") or "") if x.strip())
    )


def populated_contacts(prospect) -> list:
    return [
        c for c in (prospect.get("contacts") or []) if c.get("contact_name") or emails(c) or c.get("notes")
    ]


def primary_contacts(prospect) -> list:
    return sorted(
        [c for c in populated_contacts(prospect) if c.get("is_primary")],
        key=lambda c: ((c.get("contact_name") or "").casefold(), c.get("contact_role") or ""),
    )


def effective_primary_contact(prospect):
    rows = primary_contacts(prospect)
    return rows[0] if rows else None


def ensure_required_contact_roles(prospect) -> None:
    if not prospect.get("name"):
        return
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
    for role in sorted(set(required), key=str.casefold):
        if role not in existing:
            prospect.append("contacts", {"contact_role": role})
