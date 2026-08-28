from __future__ import annotations

import frappe


def execute() -> None:
    if frappe.db.table_exists("SEI Playbook Signal Type"):
        frappe.db.delete("SEI Playbook Signal Type")
