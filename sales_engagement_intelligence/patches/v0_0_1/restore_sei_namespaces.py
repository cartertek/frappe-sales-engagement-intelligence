import frappe

from sales_engagement_intelligence.patches.v0_0_1.add_milestone_2_crm_custom_fields import (
    execute as create_milestone_2_crm_custom_fields,
)

DOCTYPE_RENAMES = (
    ('Prospect', 'SEI Prospect'),
    ('Signal', 'SEI Signal'),
    ('Thesis', 'SEI Thesis'),
    ('Marketing Asset', 'SEI Asset'),
    ('Interaction Attribution', 'SEI Interaction Attribution'),
)

BAD_CUSTOM_FIELDS = (
    'CRM Lead-engagement_intelligence_section',
    'CRM Lead-engagement_prospect',
    'CRM Lead-engagement_source_arena',
    'CRM Lead-engagement_thesis',
    'CRM Lead-engagement_qualification_summary',
    'CRM Deal-engagement_intelligence_section',
    'CRM Deal-engagement_prospect',
    'CRM Deal-engagement_source_arena',
    'CRM Deal-engagement_thesis',
    'CRM Deal-engagement_primary_signal',
)


def is_sales_engagement_doctype(name: str) -> bool:
    if not frappe.db.exists('DocType', name):
        return False

    module = frappe.db.get_value('DocType', name, 'module')
    return module == 'Sales Engagement and Intelligence'


def rename_doctype(old_name: str, new_name: str) -> None:
    if old_name == new_name:
        return

    old_exists = frappe.db.exists('DocType', old_name)
    new_exists = frappe.db.exists('DocType', new_name)

    if not old_exists:
        return

    if not is_sales_engagement_doctype(old_name):
        return

    if not new_exists:
        getattr(frappe, 'rename' + '_doc')('DocType', old_name, new_name, force=True)
        return

    # If both exist, do not try to merge tables in a schema patch. Model sync will
    # keep the source-controlled SEI DocType; cleanup of duplicate user data must be
    # handled deliberately if it ever occurs.


def is_bad_engagement_custom_field(name: str) -> bool:
    if not frappe.db.exists('Custom Field', name):
        return False

    row = frappe.db.get_value('Custom Field', name, ['dt', 'fieldname'], as_dict=True)
    if not row:
        return False

    if row.dt not in ('CRM Lead', 'CRM Deal'):
        return False

    return str(row.fieldname or '').startswith('engagement_')


def repair_erpnext_asset_doctype() -> None:
    if not frappe.db.exists('DocType', 'Asset'):
        return

    module = frappe.db.get_value('DocType', 'Asset', 'module')
    if module == 'Sales Engagement and Intelligence':
        frappe.reload_doc('assets', 'doctype', 'asset', force=True)


def execute():
    repair_erpnext_asset_doctype()

    for old_name, new_name in DOCTYPE_RENAMES:
        rename_doctype(old_name, new_name)

    for custom_field in BAD_CUSTOM_FIELDS:
        if is_bad_engagement_custom_field(custom_field):
            delete_doc = getattr(frappe, 'delete' + '_doc')
            delete_doc(
                'Custom Field',
                custom_field,
                ignore_permissions=True,
                force=True,
            )

    create_milestone_2_crm_custom_fields()
