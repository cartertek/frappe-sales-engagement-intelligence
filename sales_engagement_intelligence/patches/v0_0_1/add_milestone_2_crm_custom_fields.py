import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def _insert_after(doctype, preferred):
    meta = frappe.get_meta(doctype)
    if preferred and meta.has_field(preferred):
        return preferred

    visible_fields = [
        field.fieldname
        for field in meta.fields
        if field.fieldtype not in ('Section Break', 'Column Break', 'Tab Break')
    ]
    return visible_fields[-1] if visible_fields else None


def execute():
    custom_fields = {}

    if frappe.db.exists('DocType', 'CRM Lead'):
        custom_fields['CRM Lead'] = [
            {
                'fieldname': 'engagement_intelligence_section',
                'label': 'Engagement Intelligence',
                'fieldtype': 'Section Break',
                'insert_after': _insert_after('CRM Lead', 'status'),
                'collapsible': 1,
            },
            {
                'fieldname': 'engagement_prospect',
                'label': 'Prospect',
                'fieldtype': 'Link',
                'options': 'Prospect',
                'insert_after': 'engagement_intelligence_section',
            },
            {
                'fieldname': 'engagement_source_arena',
                'label': 'Source Arena',
                'fieldtype': 'Data',
                'insert_after': 'engagement_prospect',
            },
            {
                'fieldname': 'engagement_thesis',
                'label': 'Thesis',
                'fieldtype': 'Link',
                'options': 'Thesis',
                'insert_after': 'engagement_source_arena',
            },
            {
                'fieldname': 'engagement_qualification_summary',
                'label': 'Qualification Summary',
                'fieldtype': 'Small Text',
                'insert_after': 'engagement_thesis',
            },
        ]

    if frappe.db.exists('DocType', 'CRM Deal'):
        custom_fields['CRM Deal'] = [
            {
                'fieldname': 'engagement_intelligence_section',
                'label': 'Engagement Intelligence',
                'fieldtype': 'Section Break',
                'insert_after': _insert_after('CRM Deal', 'status'),
                'collapsible': 1,
            },
            {
                'fieldname': 'engagement_prospect',
                'label': 'Prospect',
                'fieldtype': 'Link',
                'options': 'Prospect',
                'insert_after': 'engagement_intelligence_section',
            },
            {
                'fieldname': 'engagement_source_arena',
                'label': 'Source Arena',
                'fieldtype': 'Data',
                'insert_after': 'engagement_prospect',
            },
            {
                'fieldname': 'engagement_thesis',
                'label': 'Thesis',
                'fieldtype': 'Link',
                'options': 'Thesis',
                'insert_after': 'engagement_source_arena',
            },
            {
                'fieldname': 'engagement_primary_signal',
                'label': 'Primary Signal',
                'fieldtype': 'Link',
                'options': 'Signal',
                'insert_after': 'engagement_thesis',
            },
        ]

    if custom_fields:
        create_custom_fields(custom_fields, update=True)
