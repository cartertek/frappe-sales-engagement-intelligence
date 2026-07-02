import frappe

from sales_engagement_intelligence.patches.v0_0_1.add_milestone_2_crm_custom_fields import (
    execute as create_milestone_2_crm_custom_fields,
)

OLD_CUSTOM_FIELDS = (
    'CRM Lead-sei_section',
    'CRM Lead-sei_prospect',
    'CRM Lead-sei_source_arena',
    'CRM Lead-sei_thesis',
    'CRM Lead-sei_qualification_summary',
    'CRM Deal-sei_section',
    'CRM Deal-sei_prospect',
    'CRM Deal-sei_source_arena',
    'CRM Deal-sei_thesis',
    'CRM Deal-sei_primary_signal',
)


def execute():
    for custom_field in OLD_CUSTOM_FIELDS:
        if frappe.db.exists('Custom Field', custom_field):
            frappe.delete_doc('Custom Field', custom_field, ignore_permissions=True, force=True)

    create_milestone_2_crm_custom_fields()

