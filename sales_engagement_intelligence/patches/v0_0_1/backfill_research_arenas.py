import frappe

LEGACY_ARENA = "Legacy / Unclassified"


def execute():
    if not frappe.db.exists("DocType", "SEI Research Arena"):
        return

    if not frappe.db.exists("SEI Research Arena", LEGACY_ARENA):
        frappe.get_doc(
            {
                "doctype": "SEI Research Arena",
                "arena_name": LEGACY_ARENA,
                "description": "Migration-only arena for signals created before Research Arenas existed.",
                "active": 1,
            }
        ).insert(ignore_permissions=True)

    for thesis_name in frappe.get_all("SEI Thesis", pluck="name"):
        if not frappe.db.exists(
            "SEI Thesis Research Arena",
            {
                "parent": thesis_name,
                "parenttype": "SEI Thesis",
                "parentfield": "research_arenas",
                "research_arena": LEGACY_ARENA,
            },
        ):
            thesis = frappe.get_doc("SEI Thesis", thesis_name)
            thesis.append("research_arenas", {"research_arena": LEGACY_ARENA})
            thesis.save(ignore_permissions=True)

    frappe.db.sql(
        """
        UPDATE `tabSEI Signal`
        SET research_arena = %s
        WHERE COALESCE(research_arena, '') = ''
        """,
        LEGACY_ARENA,
    )
