from __future__ import annotations

from typing import Iterable

import frappe


def _as_list(value) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


def resolve_signal_type(value: str | None) -> str | None:
    """Resolve a signal type by document name or display name."""
    if not value:
        return None
    by_title = frappe.db.get_value("SEI Signal Type", {"signal_type_name": value}, "name")
    if by_title:
        return by_title
    if frappe.db.exists("SEI Signal Type", value):
        return value
    frappe.throw(f"SEI Signal Type not found: {value}")


def get_signal_type_thesis(signal_type: str | None) -> str | None:
    if not signal_type:
        return None
    return frappe.db.get_value("SEI Signal Type", signal_type, "thesis")


def get_signal_type_arena(signal_type: str | None) -> str | None:
    if not signal_type:
        return None
    return frappe.db.get_value("SEI Signal Type", signal_type, "research_arena")


def _get_prospect_signal_type_values(prospect: str | None, fieldname: str) -> list[str]:
    if not prospect:
        return []
    rows = frappe.db.sql(
        f"""
        SELECT DISTINCT st.`{fieldname}` value
        FROM `tabSEI Signal` s
        INNER JOIN `tabSEI Signal Type` st ON st.name = s.signal_type
        WHERE s.prospect = %s AND COALESCE(st.`{fieldname}`, '') != ''
        ORDER BY st.`{fieldname}`
        """,
        prospect,
        as_dict=True,
    )
    return [row.value for row in rows if row.value]


def get_prospect_theses(prospect: str | None) -> list[str]:
    """Return the ordered unique thesis list derived from prospect signals."""
    return _get_prospect_signal_type_values(prospect, "thesis")


def get_prospect_theses_display(prospect: str | None) -> str:
    return ", ".join(get_prospect_theses(prospect))


def get_prospect_arenas(prospect: str | None) -> list[str]:
    """Return the ordered unique arena list derived from prospect signals."""
    return _get_prospect_signal_type_values(prospect, "research_arena")


def get_prospect_arenas_display(prospect: str | None) -> str:
    return ", ".join(get_prospect_arenas(prospect))


def add_derived_theses(row: dict, prospect_field: str = "name") -> dict:
    prospect = row.get(prospect_field) or row.get("prospect")
    theses = get_prospect_theses(prospect)
    row["theses"] = theses
    row["theses_display"] = ", ".join(theses)
    return row


def add_derived_arenas(row: dict, prospect_field: str = "name") -> dict:
    prospect = row.get(prospect_field) or row.get("prospect")
    arenas = get_prospect_arenas(prospect)
    row["arenas"] = arenas
    row["arenas_display"] = ", ".join(arenas)
    return row


def prospect_matches_any_thesis(prospect: str | None, theses: str | Iterable[str] | None) -> bool:
    wanted = set(_as_list(theses))
    if not wanted:
        return True
    return bool(set(get_prospect_theses(prospect)) & wanted)
