from __future__ import annotations

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
    signal_qualification_script,
)

OLD_DEFAULT_SCRIPTS = (
    'return signals.some(it => it.strength == "Strong") || '
    'signals.filter(it => it.strength == "Moderate").length > 1;',
    'return signals.some(it => it.strength == "Strong") ||\n'
    '    signals.filter(it => it.strength == "Moderate").length > 1;',
)


def execute() -> None:
    if not frappe.db.table_exists("SEI Playbook"):
        return

    for old_script in OLD_DEFAULT_SCRIPTS:
        frappe.db.sql(
            """
            UPDATE `tabSEI Playbook`
            SET signal_qualification_script = %s
            WHERE signal_qualification_script = %s
            """,
            (signal_qualification_script.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT, old_script),
        )
