import frappe


def execute() -> None:
    if not (
        frappe.db.table_exists("SEI Playbook Signal Type")
        and frappe.db.table_exists("SEI Signal Type")
        and frappe.db.has_column("SEI Playbook Signal Type", "category")
    ):
        return

    frappe.db.sql(
        """
        UPDATE `tabSEI Playbook Signal Type` child
        INNER JOIN `tabSEI Signal Type` signal_type
            ON signal_type.name = child.signal_type
        SET
            child.category = signal_type.category,
            child.research_arena = signal_type.research_arena,
            child.active = signal_type.active
        """
    )
