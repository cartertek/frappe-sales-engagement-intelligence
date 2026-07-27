from __future__ import annotations

import frappe

DEFAULT_SCRIPT = (
    'return signals.some(it => it.strength == "Strong") || '
    'signals.filter(it => it.strength == "Moderate").length > 1;'
)


def execute() -> None:
    if not frappe.db.table_exists("SEI Playbook"):
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Playbook`
        SET signal_qualification_script = %s
        WHERE signal_qualification_script IS NULL
           OR TRIM(signal_qualification_script) = ''
        """,
        DEFAULT_SCRIPT,
    )
