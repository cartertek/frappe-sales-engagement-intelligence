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
                "description": "Migration-only arena for Signal Types that predate Research Arenas.",
                "active": 1,
            }
        ).insert(ignore_permissions=True)

    # A Signal Type now owns exactly one arena. Existing types are preserved under
    # the legacy arena until an operator classifies them explicitly.
    frappe.db.sql(
        """
        UPDATE `tabSEI Signal Type`
        SET research_arena = %s
        WHERE COALESCE(research_arena, '') = ''
        """,
        LEGACY_ARENA,
    )
