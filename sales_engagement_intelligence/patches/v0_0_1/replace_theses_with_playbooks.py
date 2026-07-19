from __future__ import annotations

import re

import frappe


def execute():
    if not frappe.db.table_exists("SEI Playbook"):
        return
    mapping = _merge_theses_into_playbooks()
    _migrate_signal_types(mapping)
    _migrate_related_links(mapping)
    _migrate_primary_contacts()
    _seed_contact_roles()
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
        prospect_signal_type_sync,
    )

    prospect_signal_type_sync.sync_all_prospect_signal_types()


def _split_roles(value):
    return [x.strip() for x in re.split(r"[\n,;]+", value or "") if x.strip()]


def _ensure_role(role):
    if role and not frappe.db.exists("SEI Contact Role", role):
        frappe.get_doc({"doctype": "SEI Contact Role", "role_name": role, "active": 1}).insert(
            ignore_permissions=True
        )


def _merge_theses_into_playbooks():
    mapping = {}
    if not frappe.db.table_exists("SEI Thesis"):
        return mapping
    for thesis_name in frappe.get_all("SEI Thesis", pluck="name"):
        thesis = frappe.get_doc("SEI Thesis", thesis_name)
        candidates = []
        if frappe.db.has_column("SEI Playbook", "default_thesis"):
            candidates = frappe.get_all(
                "SEI Playbook", filters={"default_thesis": thesis_name}, pluck="name", order_by="name"
            )
        if not candidates and frappe.db.exists("SEI Playbook", thesis_name):
            candidates = [thesis_name]
        if not candidates:
            doc = frappe.get_doc(
                {
                    "doctype": "SEI Playbook",
                    "playbook_name": thesis_name,
                    "active": thesis.active,
                    "description": thesis.description,
                    "thesis": thesis.description,
                    "default_offer": thesis.default_offer,
                    "default_asset": thesis.default_asset,
                    "typical_prospect_types": thesis.typical_prospect_types,
                    "notes": thesis.notes,
                }
            )
            doc.insert(ignore_permissions=True)
            candidates = [doc.name]
        mapping[thesis_name] = candidates[0]
        for name in candidates:
            pb = frappe.get_doc("SEI Playbook", name)
            pb.thesis = pb.thesis or thesis.description
            pb.default_offer = pb.default_offer or thesis.default_offer
            pb.default_asset = pb.default_asset or thesis.default_asset
            pb.typical_prospect_types = pb.typical_prospect_types or thesis.typical_prospect_types
            existing_arenas = {r.research_arena for r in (pb.get("research_arenas") or [])}
            for row in thesis.get("research_arenas") or []:
                if row.research_arena not in existing_arenas:
                    pb.append("research_arenas", {"research_arena": row.research_arena})
            existing_roles = {r.contact_role for r in (pb.get("contact_roles") or [])}
            roles = _split_roles(getattr(thesis, "typical_contact_roles", None))
            if frappe.db.has_column("SEI Playbook", "likely_contact_roles"):
                roles += _split_roles(frappe.db.get_value("SEI Playbook", name, "likely_contact_roles"))
            for role in roles:
                _ensure_role(role)
                if role not in existing_roles:
                    pb.append("contact_roles", {"contact_role": role})
                    existing_roles.add(role)
            pb.save(ignore_permissions=True)
    return mapping


def _migrate_signal_types(mapping):
    if not frappe.db.table_exists("SEI Signal Type"):
        return
    old_col = frappe.db.has_column("SEI Signal Type", "thesis")
    for name in frappe.get_all("SEI Signal Type", pluck="name"):
        old = frappe.db.get_value("SEI Signal Type", name, "thesis") if old_col else None
        playbook = mapping.get(old) or (old if old and frappe.db.exists("SEI Playbook", old) else None)
        if playbook:
            frappe.db.set_value("SEI Signal Type", name, "playbook", playbook, update_modified=False)


def _migrate_related_links(mapping):
    for doctype, old, new in [
        ("SEI Asset", "related_thesis", "related_playbook"),
        ("SEI Interaction Attribution", "thesis", "playbook"),
        ("SEI Message Template", "thesis", "playbook"),
    ]:
        if (
            not frappe.db.table_exists(doctype)
            or not frappe.db.has_column(doctype, old)
            or not frappe.db.has_column(doctype, new)
        ):
            continue
        for row in frappe.get_all(doctype, fields=["name", old]):
            value = row.get(old)
            if value and not frappe.db.get_value(doctype, row.name, new):
                frappe.db.set_value(doctype, row.name, new, mapping.get(value, value), update_modified=False)


def _migrate_primary_contacts():
    if not frappe.db.table_exists("SEI Prospect") or not frappe.db.has_column(
        "SEI Prospect", "primary_contact_name"
    ):
        return
    for name in frappe.get_all("SEI Prospect", pluck="name"):
        row = frappe.db.get_value(
            "SEI Prospect",
            name,
            [
                "primary_contact_name",
                "primary_contact_role",
                "primary_contact_email",
                "primary_contact_notes",
            ],
            as_dict=True,
        )
        if not any(row.values()):
            continue
        role = row.primary_contact_role or "Primary Contact"
        _ensure_role(role)
        if not frappe.db.exists(
            "SEI Prospect Contact",
            {
                "parent": name,
                "parenttype": "SEI Prospect",
                "contact_role": role,
                "contact_name": row.primary_contact_name or "",
            },
        ):
            prospect = frappe.get_doc("SEI Prospect", name)
            prospect.append(
                "contacts",
                {
                    "contact_role": role,
                    "contact_name": row.primary_contact_name,
                    "emails": row.primary_contact_email,
                    "notes": row.primary_contact_notes,
                    "is_primary": 1,
                },
            )
            prospect.save(ignore_permissions=True)


def _seed_contact_roles():
    for role in (
        "Founder",
        "Founder / Operator",
        "CTO",
        "VP Engineering",
        "Engineering Manager",
        "Product Lead",
        "Operations Lead",
        "Delivery Lead",
        "Account Lead",
        "Technical Lead",
        "Innovation / AI Lead",
        "Agency Owner",
        "MSP Owner",
        "Consultant",
        "Advisor",
        "Primary Contact",
    ):
        _ensure_role(role)
