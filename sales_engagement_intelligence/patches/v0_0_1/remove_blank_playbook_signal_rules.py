from __future__ import annotations

import frappe


def execute() -> None:
    frappe.db.sql(
        """
        DELETE FROM `tabSEI Playbook Signal Rule`
        WHERE TRIM(COALESCE(signal_type, '')) = ''
          AND TRIM(COALESCE(minimum_strength, '')) = ''
          AND TRIM(COALESCE(evidence_basis_required, '')) = ''
          AND COALESCE(exclude_from_qualification, 0) = 0
          AND TRIM(COALESCE(notes, '')) = ''
        """
    )
