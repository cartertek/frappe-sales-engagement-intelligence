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
                'fieldname': 'sei_section',
                'label': 'Sales Engagement Intelligence',
                'fieldtype': 'Section Break',
                'insert_after': _insert_after('CRM Lead', 'status'),
                'collapsible': 1,
            },
            {
                'fieldname': 'sei_prospect',
                'label': 'SEI Prospect',
                'fieldtype': 'Link',
                'options': 'SEI Prospect',
                'insert_after': 'sei_section',
            },
            {
                'fieldname': 'sei_source_arena',
                'label': 'SEI Source Arena',
                'fieldtype': 'Data',
                'insert_after': 'sei_prospect',
            },
            {
                'fieldname': 'sei_thesis',
                'label': 'SEI Thesis',
                'fieldtype': 'Link',
                'options': 'SEI Thesis',
                'insert_after': 'sei_source_arena',
            },
            {
                'fieldname': 'sei_qualification_summary',
                'label': 'SEI Qualification Summary',
                'fieldtype': 'Small Text',
                'insert_after': 'sei_thesis',
            },
        ]

    if frappe.db.exists('DocType', 'CRM Deal'):
        custom_fields['CRM Deal'] = [
            {
                'fieldname': 'sei_section',
                'label': 'Sales Engagement Intelligence',
                'fieldtype': 'Section Break',
                'insert_after': _insert_after('CRM Deal', 'status'),
                'collapsible': 1,
            },
            {
                'fieldname': 'sei_prospect',
                'label': 'SEI Prospect',
                'fieldtype': 'Link',
                'options': 'SEI Prospect',
                'insert_after': 'sei_section',
            },
            {
                'fieldname': 'sei_source_arena',
                'label': 'SEI Source Arena',
                'fieldtype': 'Data',
                'insert_after': 'sei_prospect',
            },
            {
                'fieldname': 'sei_thesis',
                'label': 'SEI Thesis',
                'fieldtype': 'Link',
                'options': 'SEI Thesis',
                'insert_after': 'sei_source_arena',
            },
            {
                'fieldname': 'sei_primary_signal',
                'label': 'SEI Primary Signal',
                'fieldtype': 'Link',
                'options': 'SEI Signal',
                'insert_after': 'sei_thesis',
            },
        ]

    if custom_fields:
        create_custom_fields(custom_fields, update=True)
