from __future__ import annotations

import frappe

PLAYBOOK_FIELD_ORDER = (
    "overview_tab",
    "playbook_name",
    "active",
    "description",
    "thesis",
    "typical_prospect_types",
    "notes",
    "research_arenas_section",
    "research_arenas",
    "qualification_tab",
    "signal_types_section",
    "signal_types",
    "signal_qualification_script",
    "qualification_guidance_section",
    "qualifying_signal_guidance",
    "disqualifying_guidance",
    "outreach_tab",
    "default_offer",
    "default_asset",
    "default_template",
    "recommended_first_action",
    "message_guidance",
    "follow_up_guidance",
    "contact_roles_section",
    "contact_roles",
)


def execute() -> None:
    if not frappe.db.exists("DocType", "SEI Playbook"):
        return

    fields = frappe.get_all(
        "DocField",
        filters={"parent": "SEI Playbook"},
        fields=["name", "fieldname", "idx"],
    )
    by_fieldname = {row.fieldname: row for row in fields}

    for idx, fieldname in enumerate(PLAYBOOK_FIELD_ORDER, start=1):
        field = by_fieldname.get(fieldname)
        if field and field.idx != idx:
            frappe.db.set_value("DocField", field.name, "idx", idx, update_modified=False)

    frappe.clear_cache(doctype="SEI Playbook")
