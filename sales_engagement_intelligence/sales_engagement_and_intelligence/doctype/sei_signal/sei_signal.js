frappe.ui.form.on('SEI Signal', {
    setup(frm) {
        frm.set_query('signal_type', () => ({ filters: { active: 1 } }));
    },

    onload_post_render(frm) {
        collapse_default_sections(frm);
        shorten_signal_textareas(frm);
    },

    refresh(frm) {
        shorten_signal_textareas(frm);
        style_observed_facts_grid(frm);
        render_signal_type_criteria(frm);
        show_evidence_guardrail_warning(frm);
    },

    signal_type(frm) {
        render_signal_type_criteria(frm);
    },


    exclude_from_qualification(frm) {
        show_evidence_guardrail_warning(frm);
    },

    signal_strength(frm) {
        show_evidence_guardrail_warning(frm);
    },

});


function style_observed_facts_grid(frm) {
    const field = frm.get_field('observed_facts');
    if (!field || !field.grid || !field.grid.wrapper) {
        return;
    }

    const column_weights = {
        fact: 5,
        evidence_basis: 1,
        evidence_specificity: 2,
        source_url: 1,
        source_date: 1,
    };
    const total_weight = Object.values(column_weights).reduce((total, weight) => total + weight, 0);

    const apply = () => {
        const $grid = field.grid.wrapper;
        $grid.addClass('sei-observed-facts-grid');

        const $reference_row = $grid.find('.grid-heading-row .data-row').first();
        if (!$reference_row.length) {
            return;
        }

        const row_width = $reference_row[0].getBoundingClientRect().width;
        let fixed_width = 0;
        $reference_row.children().each((_, element) => {
            const $element = $(element);
            if (!$element.is('.grid-static-col[data-fieldname]')) {
                fixed_width += element.getBoundingClientRect().width;
            }
        });
        const data_width = Math.max(0, row_width - fixed_width);

        Object.entries(column_weights).forEach(([fieldname, weight], index, entries) => {
            const allocated = index === entries.length - 1
                ? data_width - entries.slice(0, -1).reduce(
                    (used, [, prior_weight]) => used + Math.floor(data_width * prior_weight / total_weight),
                    0
                )
                : Math.floor(data_width * weight / total_weight);
            $grid.find(`.grid-static-col[data-fieldname="${fieldname}"]`)
                .removeClass('grid-data-last')
                .css({
                    flex: `0 0 ${allocated}px`,
                    'max-width': `${allocated}px`,
                    'min-width': `${allocated}px`,
                    width: `${allocated}px`,
                });
        });

        $grid.find('.grid-static-col[data-fieldname="fact"] .static-area').css({
            display: 'block',
            height: 'auto',
            'max-width': '100%',
            overflow: 'hidden',
            'overflow-wrap': 'anywhere',
            'text-overflow': 'clip',
            'white-space': 'pre-wrap',
            width: '100%',
        });
        $grid.find('.grid-row .data-row').css({
            height: 'auto',
            'align-items': 'stretch',
            'flex-wrap': 'nowrap',
        });
    };

    apply();
    requestAnimationFrame(apply);
    setTimeout(apply, 100);

    if (!field.grid._sei_fact_grid_bound) {
        field.grid._sei_fact_grid_bound = true;
        $(frm.wrapper).on('grid-row-render.sei-observed-facts', (_, grid_row) => {
            if (grid_row.grid === field.grid) {
                requestAnimationFrame(apply);
            }
        });
        $(window).on('resize.sei-observed-facts', frappe.utils.debounce(apply, 100));
    }
}

function show_evidence_guardrail_warning(frm) {
    const messages = [];

    const facts = frm.doc.observed_facts || [];
    const has_observed = facts.some((fact) => fact.evidence_basis === 'Observed');
    const has_inferred = facts.some((fact) => fact.evidence_basis === 'Inferred');
    if (has_inferred && !has_observed && !frm.doc.exclude_from_qualification) {
        messages.push(__('Signals supported only by inferred facts do not count toward automatic qualification.'));
    }

    if (['Moderate', 'Strong'].includes(frm.doc.signal_strength) && !frm.doc.why_not_weak) {
        messages.push(__('Moderate/Strong signals must explain why the source-backed evidence is not Weak.'));
    }

    const weak_specificity = facts.some((fact) =>
        ['Search Result', 'Generic List or Directory', 'Aggregator', 'Unknown'].includes(fact.evidence_specificity || '')
    );
    if (weak_specificity) {
        messages.push(__('One or more facts have weak evidence specificity. Confirm the managed Signal Type allows those source types.'));
    }

    if (!messages.length) {
        frm.dashboard.clear_headline();
        return;
    }

    frm.dashboard.set_headline_alert(messages.join('<br>'), 'orange');
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


const COMPACT_SIGNAL_TEXT_FIELDS = [
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
