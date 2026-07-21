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


def is_real_contact(contact) -> bool:
    return bool(
        contact.get("contact_name")
        or emails(contact)
        or contact.get("notes")
        or contact.get("crm_contact")
    )


def contact_role_requirements(prospect) -> dict[str, bool]:
    prospect_name = prospect.get("name") if hasattr(prospect, "get") else str(prospect or "")
    playbooks = (prospect.get("playbooks") or "") if hasattr(prospect, "get") else ""
    if prospect_name:
        playbooks = frappe.db.get_value("SEI Prospect", prospect_name, "playbooks") or playbooks
    names = [value.strip() for value in playbooks.split(",") if value.strip()]
    requirements: dict[str, bool] = {}
    for name in names:
        for row in frappe.get_all(
            "SEI Playbook Contact Role",
            filters={"parent": name, "parenttype": "SEI Playbook"},
            fields=["contact_role", "signal_specific_relevance"],
            order_by="idx",
        ):
            role = (row.contact_role or "").strip()
            if role:
                requirements[role] = requirements.get(role, False) or bool(
                    row.signal_specific_relevance
                )
    return dict(sorted(requirements.items(), key=lambda item: item[0].casefold()))


def contact_role_requires_signal_relevance(prospect, role: str) -> bool:
    normalized = (role or "").strip().casefold()
    return any(
        name.casefold() == normalized and signal_specific
        for name, signal_specific in contact_role_requirements(prospect).items()
    )


def required_contact_roles(prospect) -> list[str]:
    return list(contact_role_requirements(prospect))


def missing_required_contact_roles(prospect) -> list[str]:
    existing = {
        (row.get("contact_role") or "").strip().casefold()
        for row in prospect.get("contacts") or []
        if is_real_contact(row) and row.get("contact_role")
    }
    return [role for role in required_contact_roles(prospect) if role.casefold() not in existing]


def remove_empty_contact_role_placeholders(prospect) -> bool:
    contacts = list(prospect.get("contacts") or [])
    retained = [row for row in contacts if is_real_contact(row)]
    if len(retained) == len(contacts):
        return False
    prospect.set("contacts", retained)
    return True
