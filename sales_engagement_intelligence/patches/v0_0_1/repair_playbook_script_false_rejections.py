from __future__ import annotations

import frappe

BAD_EXPLANATION = "No eligible signal passed its playbook qualification script."
BAD_MIGRATION_START = "2026-07-24 20:38:28"
BAD_MIGRATION_END = "2026-07-24 20:38:31"

# Exact pre-migration business state from backup
# /backup/20260724_131258-frappe_localhost-database.sql.gz.
BACKUP_STATE = {
    "SEI-PROS-2026-00068": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00069": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00070": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00071": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00073": (
        "Research Complete",
        "Needs Review",
        1,
        0,
        1,
        "Needs review: only 1 moderate observed qualifying signal.",
    ),
    "SEI-PROS-2026-00074": (
        "Research Complete",
        "Needs Review",
        1,
        0,
        1,
        "Needs review: only 1 moderate observed qualifying signal.",
    ),
    "SEI-PROS-2026-00075": (
        "Research Complete",
        "Needs Review",
        1,
        0,
        1,
        "Needs review: only 1 moderate observed qualifying signal.",
    ),
    "SEI-PROS-2026-00076": (
        "Research Complete",
        "Needs Review",
        1,
        0,
        1,
        "Needs review: only 1 moderate observed qualifying signal.",
    ),
    "SEI-PROS-2026-00103": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00107": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00122": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00136": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00144": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00148": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00149": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00156": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00168": (
        "Find Contact",
        "Qualified",
        2,
        0,
        2,
        "Qualified by 2 moderate observed signals.",
    ),
    "SEI-PROS-2026-00169": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00170": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00171": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00177": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00178": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00179": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00180": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00181": ("Qualified", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00186": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00189": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00192": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
    "SEI-PROS-2026-00193": ("Find Contact", "Qualified", 1, 1, 0, "Qualified by 1 strong observed signal."),
}


def execute() -> None:
    if not frappe.db.table_exists("SEI Prospect"):
        return

    for prospect, state in BACKUP_STATE.items():
        current = frappe.db.get_value(
            "SEI Prospect",
            prospect,
            ["lifecycle_status", "qualification_status", "qualification_explanation", "modified"],
            as_dict=True,
        )
        if not _still_has_bad_migration_state(current):
            continue

        lifecycle, qualification, qualified_count, strong_count, moderate_count, explanation = state
        frappe.db.set_value(
            "SEI Prospect",
            prospect,
            {
                "lifecycle_status": lifecycle,
                "qualification_status": qualification,
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
