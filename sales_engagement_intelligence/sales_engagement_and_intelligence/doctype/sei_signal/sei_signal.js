frappe.ui.form.on('SEI Signal', {
    setup(frm) {
        frm.set_query('signal_type', () => ({ filters: { active: 1 } }));

frappe.ui.form.on('SEI Signal Disqualifier Check', {
    applies(frm) {
        frm.set_value('is_strength_capped', has_applied_disqualifier(frm));
        show_evidence_guardrail_warning(frm);
    },

    disqualifier_checks_remove(frm) {
        frm.set_value('is_strength_capped', has_applied_disqualifier(frm));
        show_evidence_guardrail_warning(frm);
    },
});


function set_research_arena_query(frm) {
    if (!frm.doc.signal_type) {
    });
}

function show_evidence_guardrail_warning(frm) {
    const messages = [];

    if (frm.doc.evidence_basis === 'Inferred' && !frm.doc.exclude_from_qualification) {
        messages.push(__('Inferred signals are retained as context but do not count toward automatic qualification.'));
    }

    if (['Moderate', 'Strong'].includes(frm.doc.signal_strength) && !frm.doc.why_not_weak) {
        messages.push(__('Moderate/Strong signals must explain why the source-backed evidence is not Weak.'));
    }

    if (has_applied_disqualifier(frm)) {
        messages.push(__('This signal is capped at Weak unless a Manual Override Reason is documented.'));
    }

    if (['Search Result', 'Generic List or Directory', 'Aggregator', 'Unknown'].includes(frm.doc.evidence_specificity || '')) {
        messages.push(__('Evidence specificity is weak. Confirm the managed Signal Type allows this source type.'));
    }

    if (!messages.length) {
        frm.dashboard.clear_headline();
        return;
    }

    frm.dashboard.set_headline_alert(messages.join('<br>'), 'orange');
}

function add_disqualifier_actions(frm) {
    if (!frm.doc.signal_type) {
        return;
    }

    frm.add_custom_button(__('Load Disqualifier Checks'), () => {
        load_disqualifier_checks(frm, { only_if_empty: false });
    });
}

function has_applied_disqualifier(frm) {
    return (frm.doc.disqualifier_checks || []).some((row) => row.applies);
}

function render_signal_type_criteria(frm) {
    if (!frm.doc.signal_type) {
        frm.set_df_property('criteria_html', 'options', '');
        return;
    }

    frappe.db.get_doc('SEI Signal Type', frm.doc.signal_type).then((doc) => {
        const sections = [
            ['Summary', doc.evidence_summary || doc.description],
            ['Qualifying evidence', doc.qualifying_evidence],
            ['Insufficient evidence', doc.insufficient_evidence],
            ['Automatic Weak conditions', doc.automatic_weak_conditions],
            ['Disqualifying conditions', doc.disqualifying_conditions],
            ['Weak guidance', doc.weak_guidance],
            ['Moderate guidance', doc.moderate_guidance],
            ['Strong guidance', doc.strong_guidance],
            ['Evidence notes requirements', doc.evidence_notes_requirements],
        ].filter(([, value]) => value);

        const html = sections.map(([label, value]) => `
            <div class="mb-3">
                <div class="text-muted small">${frappe.utils.escape_html(__(label))}</div>
                <div style="white-space: pre-wrap;">${frappe.utils.escape_html(value)}</div>
            </div>
        `).join('');

        frm.set_df_property('criteria_html', 'options', html || __('No structured criteria are defined for this Signal Type yet.'));
    });
}

function load_disqualifier_checks(frm, { only_if_empty } = { only_if_empty: true }) {
    if (!frm.doc.signal_type) {
        return;
    }
    if (only_if_empty && (frm.doc.disqualifier_checks || []).length) {
        return;
    }

    frappe.db.get_doc('SEI Signal Type', frm.doc.signal_type).then((doc) => {
        const lines = (doc.disqualifying_conditions || '')
            .split('\n')
            .map((line) => line.trim().replace(/^[-*]\s*/, ''))
            .filter(Boolean);

        if (!lines.length) {
            return;
        }

        if (!only_if_empty) {
            frm.clear_table('disqualifier_checks');
        }

        const existing = new Set((frm.doc.disqualifier_checks || []).map((row) => row.disqualifier));
        lines.forEach((line) => {
            if (existing.has(line)) {
                return;
            }
            const row = frm.add_child('disqualifier_checks');
            row.signal_type = frm.doc.signal_type;
            row.disqualifier = line;
            row.applies = 0;
        });
        frm.refresh_field('disqualifier_checks');
    });
}


const COMPACT_SIGNAL_TEXT_FIELDS = [
    'observed_fact',
    'signal_claim',
    'why_this_signal_type',
    'why_not_weak',
    'disqualifiers_checked',
    'evidence_gap_reason',
    'evidence_notes',
    'manual_override_reason',
];

const DEFAULT_COLLAPSED_SIGNAL_SECTIONS = [
    'signal_type_definition_section',
    'qualification_section',
    'review_section',
];

function collapse_default_sections(frm) {
    DEFAULT_COLLAPSED_SIGNAL_SECTIONS.forEach((fieldname) => {
        const field = frm.get_field(fieldname);
        if (field && field.section) {
            field.section.collapse(true);
        }
    });
}

function shorten_signal_textareas(frm) {
    COMPACT_SIGNAL_TEXT_FIELDS.forEach((fieldname) => {
        const field = frm.get_field(fieldname);
        if (field && field.$input) {
            field.$input.css({ height: '88px', 'min-height': '88px' });
        }
    });
}
