frappe.ui.form.on('SEI Signal', {
    setup(frm) {
        frm.set_query('signal_type', () => ({ filters: { active: 1 } }));
    },

    onload_post_render(frm) {
        collapse_default_sections(frm);
        shorten_signal_textareas(frm);
    },

    refresh(frm) {
        add_publish_action(frm);
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


function add_publish_action(frm) {
    if (frm.is_new() || frm.doc.status !== 'Draft') {
        return;
    }
    frm.add_custom_button(__('Publish'), () => {
        frappe.confirm(
            __('Publish this Signal? All required fields and evidence rules will be validated.'),
            () => frappe.call({
                method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.publish_signal',
                args: { signal: frm.doc.name },
                freeze: true,
                callback() {
                    frm.reload_doc();
                }
            })
        );
    }, __('Signal Actions'));
}


function style_observed_facts_grid(frm) {
    const field = frm.get_field('observed_facts');
    if (!field || !field.grid || !field.grid.wrapper) {
        return;
    }

    const apply = () => {
        const $grid = field.grid.wrapper;
        $grid.addClass('sei-observed-facts-grid');

        const $container = $grid.find('.form-grid-container').first();
        const $reference_row = $grid.find('.grid-heading-row .data-row').first();
        if (!$container.length || !$reference_row.length) {
            return;
        }

        const visible_width = $container[0].clientWidth;
        const wide_column_width = Math.max(320, Math.floor(visible_width * 0.35));
        const content_columns = ['source_date', 'evidence_basis', 'evidence_specificity'];
        const measured_widths = {};

        content_columns.forEach((fieldname) => {
            let width = 0;
            $grid.find(`.grid-static-col[data-fieldname="${fieldname}"]`).each((_, cell) => {
                const area = cell.querySelector('.static-area') || cell;
                width = Math.max(width, area.scrollWidth + 24);
            });
            measured_widths[fieldname] = Math.max(width, 110);
        });

        const widths = {
            fact: wide_column_width,
            source_url: wide_column_width,
            source_date: measured_widths.source_date,
            evidence_basis: measured_widths.evidence_basis,
            evidence_specificity: measured_widths.evidence_specificity,
        };

        Object.entries(widths).forEach(([fieldname, width]) => {
            $grid.find(`.grid-static-col[data-fieldname="${fieldname}"]`)
                .removeClass('grid-data-last')
                .css({
                    flex: `0 0 ${width}px`,
                    'max-width': `${width}px`,
                    'min-width': `${width}px`,
                    width: `${width}px`,
                });
        });

        let fixed_width = 0;
        $reference_row.children().each((_, element) => {
            if (!$(element).is('.grid-static-col[data-fieldname]')) {
                fixed_width += element.getBoundingClientRect().width;
            }
        });
        const total_width = fixed_width + Object.values(widths).reduce((sum, width) => sum + width, 0);
        $grid.find('.grid-heading-row .data-row, .grid-body .grid-row .data-row').css({
            width: `${total_width}px`,
            'min-width': `${total_width}px`,
            'max-width': `${total_width}px`,
        });

        const $wrapping_areas = $grid.find(
            '.grid-body .grid-static-col[data-fieldname="fact"] .static-area, ' +
            '.grid-body .grid-static-col[data-fieldname="source_url"] .static-area'
        );
        $wrapping_areas.removeClass('ellipsis').css({
            display: 'block',
            height: 'auto',
            'max-height': 'none',
            'max-width': '100%',
            overflow: 'visible',
            'overflow-wrap': 'anywhere',
            'text-overflow': 'clip',
            'white-space': 'pre-wrap',
            width: '100%',
        });
        $grid.find('.grid-body .grid-static-col[data-fieldname="fact"] .static-area').css({
            'font-weight': '600',
        });

        content_columns.forEach((fieldname) => {
            $grid.find(`.grid-static-col[data-fieldname="${fieldname}"] .static-area`)
                .removeClass('ellipsis')
                .css({
                    overflow: 'visible',
                    'text-overflow': 'clip',
                    'white-space': 'nowrap',
                });
        });

        $grid.find('.grid-body .grid-row .data-row').each((_, row) => {
            const $row = $(row);
            let content_height = 0;
            ['fact', 'source_url'].forEach((fieldname) => {
                const area = $row.find(`.grid-static-col[data-fieldname="${fieldname}"] .static-area`)[0];
                if (!area) {
                    return;
                }
                const $cell = $(area).closest('.grid-static-col');
                const padding = parseFloat($cell.css('padding-top') || 0)
                    + parseFloat($cell.css('padding-bottom') || 0);
                content_height = Math.max(content_height, area.scrollHeight + padding);
            });
            const row_height = Math.max(
                parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--input-height')) || 38,
                Math.ceil(content_height)
            );

            $row.css({
                height: `${row_height}px`,
                'min-height': `${row_height}px`,
                'align-items': 'stretch',
                'flex-wrap': 'nowrap',
            });
            $row.children().css({
                height: `${row_height}px`,
                'min-height': `${row_height}px`,
            });
        });
    };

    apply();
    requestAnimationFrame(apply);
    setTimeout(apply, 100);

    if (!field.grid._sei_fact_grid_bound) {
        field.grid._sei_fact_grid_bound = true;

        // Frappe opens a child-table row from handlers attached below the grid
        // wrapper, so a delegated bubbling handler runs too late. Intercept the
        // Source URL interaction during capture, before the row handler sees it,
        // while leaving the browser's default link navigation intact.
        const grid_element = field.grid.wrapper.get(0);
        const isolate_source_url_link = (event) => {
            if (event.target.closest(
                '.grid-static-col[data-fieldname="source_url"] a[href]'
            )) {
                event.stopPropagation();
            }
        };
        grid_element.addEventListener('mousedown', isolate_source_url_link, true);
        grid_element.addEventListener('click', isolate_source_url_link, true);

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
