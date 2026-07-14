frappe.ui.form.on('SEI Signal', {
    refresh(frm) {
        show_inferred_qualification_warning(frm);
    },

    evidence_basis(frm) {
        show_inferred_qualification_warning(frm);
    },

    exclude_from_qualification(frm) {
        show_inferred_qualification_warning(frm);
    },

    signal_strength(frm) {
        show_inferred_qualification_warning(frm);
    },
});

function show_inferred_qualification_warning(frm) {
    const inferred_not_excluded_signal = frm.doc.evidence_basis === 'Inferred'
        && !frm.doc.exclude_from_qualification;

    if (!inferred_not_excluded_signal) {
        frm.dashboard.clear_headline();
        return;
    }

    frm.dashboard.set_headline_alert(
        __('Inferred signals are retained as evidence, but they do not count toward automatic qualification.'),
        'orange'
    );
}
