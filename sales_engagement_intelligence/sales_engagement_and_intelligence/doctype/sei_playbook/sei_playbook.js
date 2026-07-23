const COMPACT_PLAYBOOK_TEXT_FIELDS = [
    'description',
    'thesis',
    'typical_prospect_types',
    'qualifying_signal_guidance',
    'disqualifying_guidance',
    'message_guidance',
    'follow_up_guidance',
    'notes',
];

frappe.ui.form.on('SEI Playbook', {
    refresh(frm) {
        remove_blank_signal_rule_rows(frm);
        COMPACT_PLAYBOOK_TEXT_FIELDS.forEach((fieldname) => {
            const field = frm.get_field(fieldname);
            if (field && field.$input) {
                field.$input.css({ height: '88px', 'min-height': '88px' });
            }
        });
    },

    before_save(frm) {
        remove_blank_signal_rule_rows(frm);
    },
});

function remove_blank_signal_rule_rows(frm) {
    const rows = frm.doc.signal_rules || [];
    const retained = rows.filter((row) => !is_blank_signal_rule(row));

    if (retained.length === rows.length) {
        return;
    }

    rows
        .filter((row) => is_blank_signal_rule(row))
        .forEach((row) => {
            if (row.doctype && row.name && locals[row.doctype]) {
                delete locals[row.doctype][row.name];
            }
        });

    frm.doc.signal_rules = retained;
    frm.refresh_field('signal_rules');
}

function is_blank_signal_rule(row) {
    return ![
        row.signal_type,
        row.minimum_strength,
        row.evidence_basis_required,
        row.exclude_from_qualification,
        row.notes,
    ].some((value) => (typeof value === 'string' ? value.trim() : Boolean(value)));
}
