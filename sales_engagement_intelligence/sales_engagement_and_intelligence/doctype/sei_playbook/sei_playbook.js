const COMPACT_PLAYBOOK_TEXT_FIELDS = [
    'description',
    'thesis',
    'typical_prospect_types',
    'qualifying_signal_guidance',
    'disqualifying_guidance',
    'follow_up_guidance',
    'notes',
];

frappe.ui.form.on('SEI Playbook', {
    refresh(frm) {
        COMPACT_PLAYBOOK_TEXT_FIELDS.forEach((fieldname) => {
            const field = frm.get_field(fieldname);
            if (field && field.$input) {
                field.$input.css({ height: '88px', 'min-height': '88px' });
            }
        });
    },
});
