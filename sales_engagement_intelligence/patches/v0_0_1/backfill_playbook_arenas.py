import frappe


def execute():
    if not (
        frappe.db.exists("DocType", "SEI Playbook")
        and frappe.db.exists("DocType", "SEI Research Arena")
        and frappe.db.exists("DocType", "SEI Signal Type")
    ):
        return

    for row in frappe.get_all("SEI Signal Type", fields=["playbook", "research_arena"]):
        if not row.playbook or not row.research_arena:
            continue
        if frappe.db.exists(
            "SEI Playbook Research Arena",
            {
                "parent": row.playbook,
                "parenttype": "SEI Playbook",
                "parentfield": "research_arenas",
                "research_arena": row.research_arena,
            },
        ):
            continue
        playbook = frappe.get_doc("SEI Playbook", row.playbook)
        playbook.append("research_arenas", {"research_arena": row.research_arena})
        playbook.save(ignore_permissions=True)
