from __future__ import annotations

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
    signal_qualification_script,
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
        signal_qualification_script.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT,
    )
