import frappe


def execute() -> None:
    if not frappe.db.table_exists("SEI Playbook"):
        return

    rows = frappe.get_all(
        "SEI Playbook",
        filters={"signal_qualification_script": ["like", "%it.category%"]},
        fields=["name", "signal_qualification_script"],
    )
    for row in rows:
        script = (row.signal_qualification_script or "").replace("it.category", "it.type.category")
        frappe.db.set_value(
            "SEI Playbook",
            row.name,
            "signal_qualification_script",
            script,
            update_modified=False,
        )
