from __future__ import annotations

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.services import (
    signal_qualification_script,
)

LEGACY_DOCTYPE = "SEI Playbook Signal Rule"


def execute() -> None:
    _migrate_default_rules()
    _remove_legacy_doctype()
    _recalculate_prospects()


def _migrate_default_rules() -> None:
    if not frappe.db.exists("DocType", LEGACY_DOCTYPE):
        return

    for playbook in frappe.get_all("SEI Playbook", pluck="name"):
        if frappe.db.get_value("SEI Playbook", playbook, "signal_qualification_script"):
            continue

        rows = frappe.get_all(
            LEGACY_DOCTYPE,
            filters={"parent": playbook, "parenttype": "SEI Playbook"},
            fields=[
                "signal_type",
                "minimum_strength",
                "evidence_basis_required",
                "exclude_from_qualification",
                "notes",
            ],
        )
        # Frappe child grids can create/remove a single empty placeholder row. Treat no persisted
        # row or one completely blank row as that default state; meaningful legacy rules are not
        # translated because their semantics are not equivalent to executable scripts.
        if not rows or (len(rows) == 1 and _is_blank_rule(rows[0])):
            frappe.db.set_value(
                "SEI Playbook",
                playbook,
                "signal_qualification_script",
                signal_qualification_script.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT,
                update_modified=False,
            )


def _is_blank_rule(row: dict) -> bool:
    return not any(
        (
            str(row.get("signal_type") or "").strip(),
            str(row.get("minimum_strength") or "").strip(),
            str(row.get("evidence_basis_required") or "").strip(),
            bool(row.get("exclude_from_qualification")),
            str(row.get("notes") or "").strip(),
        )
    )


def _remove_legacy_doctype() -> None:
    if frappe.db.exists("DocType", LEGACY_DOCTYPE):
        frappe.delete_doc("DocType", LEGACY_DOCTYPE, ignore_permissions=True, force=True)


def _recalculate_prospects() -> None:
    if not frappe.db.table_exists("SEI Prospect"):
        return

    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.lifecycle import (
        apply_lifecycle_status,
        is_terminal_status,
    )
    from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
        apply_qualification_result,
    )

    for prospect in frappe.get_all("SEI Prospect", pluck="name"):
        apply_qualification_result(prospect)
        status = frappe.db.get_value("SEI Prospect", prospect, "lifecycle_status")
        if not is_terminal_status(status):
            apply_lifecycle_status(prospect)
