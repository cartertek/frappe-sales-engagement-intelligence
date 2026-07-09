from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import frappe


def has_doctype(doctype: str) -> bool:
    """Return true when the DocType exists in the current site."""
    if not doctype:
        return False
    try:
        if hasattr(frappe.db, "table_exists") and frappe.db.table_exists(doctype):
            return True
        return bool(frappe.db.exists("DocType", doctype))
    except Exception:
        return False


@lru_cache(maxsize=512)
def has_field(doctype: str, fieldname: str) -> bool:
    """Return true when a DocType has a field in the installed schema."""
    if not doctype or not fieldname or not has_doctype(doctype):
        return False
    try:
        return bool(frappe.get_meta(doctype).has_field(fieldname))
    except Exception:
        return False


def get_safe_link_field(doctype: str, candidates: Iterable[str]) -> str | None:
    """Return the first installed candidate field for schema-aware reports."""
    for candidate in candidates:
        if has_field(doctype, candidate):
            return candidate
    return None


def table(doctype: str) -> str:
    return f"`tab{doctype.replace('`', '')}`"


def column(doctype: str, fieldname: str, fallback: str = "NULL") -> str:
    return f"{table(doctype)}.`{fieldname}`" if has_field(doctype, fieldname) else fallback


def doctypes_available(*doctypes: str) -> bool:
    return all(has_doctype(doctype) for doctype in doctypes)


def empty_result(message: str):
    return [
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 240},
        {"label": "Message", "fieldname": "message", "fieldtype": "Data", "width": 640},
    ], [{"status": "Not Available", "message": message}]


def pct_expr(numerator: str, denominator: str) -> str:
    return f"ROUND(100 * ({numerator}) / NULLIF(({denominator}), 0), 2)"


def make_conditions(filters: dict | None, doctype: str, mapping: dict[str, str]) -> tuple[str, dict]:
    filters = filters or {}
    clauses: list[str] = []
    params: dict = {}
    for key, fieldname in mapping.items():
        value = filters.get(key)
        if value in (None, "", []):
            continue
        if not has_field(doctype, fieldname):
            continue
        param = f"filter_{key}"
        if isinstance(value, (list, tuple, set)):
            clauses.append(f"{table(doctype)}.`{fieldname}` IN %({param})s")
            params[param] = tuple(value)
        else:
            clauses.append(f"{table(doctype)}.`{fieldname}` = %({param})s")
            params[param] = value
    if filters.get("next_action_date") and has_field(doctype, "next_action_date"):
        clauses.append(f"{table(doctype)}.`next_action_date` <= %(filter_next_action_date)s")
        params["filter_next_action_date"] = filters["next_action_date"]
    return (" WHERE " + " AND ".join(clauses)) if clauses else "", params
