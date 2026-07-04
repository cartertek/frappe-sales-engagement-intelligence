import frappe

from sales_engagement_intelligence.patches.v0_0_1.add_milestone_2_crm_custom_fields import (
    execute as create_milestone_2_crm_custom_fields,
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


def execute():
    for custom_field in BAD_CUSTOM_FIELDS:
        if frappe.db.exists('Custom Field', custom_field):
            frappe.delete_doc('Custom Field', custom_field, ignore_permissions=True, force=True)

    create_milestone_2_crm_custom_fields()
