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
                'fieldname': 'sei_tab',
                'label': 'SEI',
                'fieldtype': 'Tab Break',
                'insert_after': _insert_after('CRM Lead', 'converted'),
            },
            {
                'fieldname': 'sei_prospect',
                'label': 'Prospect',
                'fieldtype': 'Link',
                'options': 'SEI Prospect',
                'insert_after': 'sei_tab',
            },
            {
                'fieldname': 'sei_source_arena',
                'label': 'Source Arena',
                'fieldtype': 'Data',
                'insert_after': 'sei_prospect',
            },
            {
                'fieldname': 'sei_thesis',
                'label': 'Thesis',
                'fieldtype': 'Link',
                'options': 'SEI Thesis',
                'insert_after': 'sei_source_arena',
            },
            {
                'fieldname': 'sei_qualification_summary',
                'label': 'Qualification Summary',
                'fieldtype': 'Small Text',
                'insert_after': 'sei_thesis',
            },
        ]

    if frappe.db.exists('DocType', 'CRM Deal'):
        custom_fields['CRM Deal'] = [
            {
                'fieldname': 'sei_tab',
                'label': 'SEI',
                'fieldtype': 'Tab Break',
                'insert_after': _insert_after('CRM Deal', 'gender'),
            },
            {
                'fieldname': 'sei_prospect',
                'label': 'Prospect',
                'fieldtype': 'Link',
                'options': 'SEI Prospect',
                'insert_after': 'sei_tab',
            },
            {
                'fieldname': 'sei_source_arena',
                'label': 'Source Arena',
                'fieldtype': 'Data',
                'insert_after': 'sei_prospect',
            },
            {
                'fieldname': 'sei_thesis',
                'label': 'Thesis',
                'fieldtype': 'Link',
                'options': 'SEI Thesis',
                'insert_after': 'sei_source_arena',
            },
            {
                'fieldname': 'sei_primary_signal',
                'label': 'Primary Signal',
                'fieldtype': 'Link',
                'options': 'SEI Signal',
                'insert_after': 'sei_thesis',
            },
        ]

    if custom_fields:
        create_custom_fields(custom_fields, update=True)
