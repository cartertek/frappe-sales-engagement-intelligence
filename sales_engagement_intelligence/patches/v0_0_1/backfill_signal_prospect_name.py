import frappe


def execute():
    if not frappe.db.has_column('SEI Signal', 'prospect_name'):
        return

    signals = frappe.get_all(
        'SEI Signal',
        filters={'prospect': ['is', 'set']},
        fields=['name', 'prospect'],
    )
    for signal in signals:
        prospect_name = frappe.db.get_value(
            'SEI Prospect',
            signal.prospect,
            'prospect_name',
        )
        if prospect_name:
            frappe.db.set_value(
                'SEI Signal',
                signal.name,
                'prospect_name',
                prospect_name,
                update_modified=False,
            )
