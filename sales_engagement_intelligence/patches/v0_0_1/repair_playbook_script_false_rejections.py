from __future__ import annotations

import frappe

BAD_EXPLANATION = "No eligible signal passed its playbook qualification script."
BAD_MIGRATION_START = "2026-07-24 20:38:28"
BAD_MIGRATION_END = "2026-07-24 20:38:31"

QUALIFIED_STRONG = {
    "SEI-PROS-2026-00068",
    "SEI-PROS-2026-00069",
    "SEI-PROS-2026-00070",
    "SEI-PROS-2026-00071",
    "SEI-PROS-2026-00169",
    "SEI-PROS-2026-00170",
    "SEI-PROS-2026-00171",
    "SEI-PROS-2026-00177",
    "SEI-PROS-2026-00178",
    "SEI-PROS-2026-00179",
    "SEI-PROS-2026-00180",
    "SEI-PROS-2026-00181",
}

FIND_CONTACT_STRONG = {
    "SEI-PROS-2026-00103",
    "SEI-PROS-2026-00107",
    "SEI-PROS-2026-00122",
    "SEI-PROS-2026-00136",
    "SEI-PROS-2026-00144",
    "SEI-PROS-2026-00148",
    "SEI-PROS-2026-00149",
    "SEI-PROS-2026-00156",
    "SEI-PROS-2026-00186",
    "SEI-PROS-2026-00189",
    "SEI-PROS-2026-00192",
    "SEI-PROS-2026-00193",
}

FIND_CONTACT_MODERATE = {"SEI-PROS-2026-00168"}
VICTIMS = QUALIFIED_STRONG | FIND_CONTACT_STRONG | FIND_CONTACT_MODERATE


def execute() -> None:
    if not frappe.db.table_exists("SEI Prospect"):
        return

    for prospect in sorted(VICTIMS):
        current = frappe.db.get_value(
            "SEI Prospect",
            prospect,
            [
                "lifecycle_status",
                "qualification_status",
                "qualification_explanation",
                "modified",
            ],
            as_dict=True,
        )
        if not _still_has_bad_migration_state(current):
            continue

        lifecycle = "Qualified" if prospect in QUALIFIED_STRONG else "Find Contact"
        strong_count = 0 if prospect in FIND_CONTACT_MODERATE else 1
        moderate_count = 2 if prospect in FIND_CONTACT_MODERATE else 0
        qualified_count = strong_count + moderate_count
        explanation = (
            "Qualified by 2 moderate observed signals."
            if prospect in FIND_CONTACT_MODERATE
            else "Qualified by 1 strong observed signal."
        )

        frappe.db.set_value(
            "SEI Prospect",
            prospect,
            {
                "lifecycle_status": lifecycle,
                "qualification_status": "Qualified",
                "qualified_signal_count": qualified_count,
                "strong_observed_signal_count": strong_count,
                "moderate_observed_signal_count": moderate_count,
                "qualification_explanation": explanation,
            },
            update_modified=True,
        )


def _still_has_bad_migration_state(current) -> bool:
    if not current:
        return False
    modified = str(current.modified or "")
    return (
        current.lifecycle_status == "Rejected"
        and current.qualification_status == "Rejected"
        and current.qualification_explanation == BAD_EXPLANATION
        and BAD_MIGRATION_START <= modified <= BAD_MIGRATION_END
    )
