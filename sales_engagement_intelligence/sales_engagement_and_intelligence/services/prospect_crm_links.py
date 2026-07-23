from __future__ import annotations

import frappe


def get_prospect_crm_leads(prospect_name: str) -> list[str]:
    """Return every CRM Lead linked to an SEI Prospect in stable order."""
    if not prospect_name or not frappe.db.exists("DocType", "CRM Lead"):
        return []
    if not frappe.get_meta("CRM Lead").has_field("sei_prospect"):
        return []
    return frappe.get_all(
        "CRM Lead",
        filters={"sei_prospect": prospect_name},
        pluck="name",
        order_by="creation asc, name asc",
    )


def has_prospect_crm_leads(prospect_name: str) -> bool:
    if not prospect_name or not frappe.db.exists("DocType", "CRM Lead"):
        return False
    if not frappe.get_meta("CRM Lead").has_field("sei_prospect"):
        return False
    return bool(frappe.db.exists("CRM Lead", {"sei_prospect": prospect_name}))


def get_prospect_crm_lead_rows(prospect_name: str, fields: list[str] | None = None) -> list[dict]:
    if not prospect_name or not frappe.db.exists("DocType", "CRM Lead"):
        return []
    if not frappe.get_meta("CRM Lead").has_field("sei_prospect"):
        return []
    requested = fields or ["name", "lead_name", "email", "organization"]
    if "name" not in requested:
        requested = ["name", *requested]
    return frappe.get_all(
        "CRM Lead",
        filters={"sei_prospect": prospect_name},
        fields=requested,
        order_by="creation asc, name asc",
    )
