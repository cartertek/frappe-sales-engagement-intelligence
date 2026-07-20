from __future__ import annotations

import re

import frappe
from frappe.utils import validate_email_address


def normalize_email_list(value: str | None, *, label: str = "Email addresses") -> str | None:
    raw = (value or "").strip()
    if not raw:
        return None

    addresses = [item.strip() for item in re.split(r"[,;\n]+", raw) if item.strip()]
    for address in addresses:
        try:
            validate_email_address(address, throw=True)
        except Exception:
            frappe.throw(f"{label} must contain only valid email addresses. Invalid value: {address}")
    return ", ".join(dict.fromkeys(addresses))
