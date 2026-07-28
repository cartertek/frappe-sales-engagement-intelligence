import frappe


def execute() -> None:
    if not frappe.db.table_exists("SEI Playbook"):
        return

    rows = frappe.get_all(
        "SEI Playbook",
        filters={"signal_qualification_script": ["like", "%it.category%"]},
        fields=["name", "signal_qualification_script"],
    )
    updated_playbooks = []
    for row in rows:
        script = (row.signal_qualification_script or "").replace("it.category", "it.type.category")
        frappe.db.set_value(
            "SEI Playbook",
            row.name,
            "signal_qualification_script",
            script,
            update_modified=False,
        )
        updated_playbooks.append(row.name)

    if updated_playbooks:
        from sales_engagement_intelligence.sales_engagement_and_intelligence.services.qualification import (
            recalculate_prospects_for_playbook,
        )

        for playbook in updated_playbooks:
            recalculate_prospects_for_playbook(playbook)
