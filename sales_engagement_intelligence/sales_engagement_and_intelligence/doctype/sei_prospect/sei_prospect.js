frappe.ui.form.on('SEI Prospect', {
    refresh(frm) {
        if (frm.is_new()) return;

        reload_if_cached_document_is_stale(frm);

        configure_prospect_actions(frm);
        configure_primary_prospect_action(frm);

        configure_contact_grid(frm);
        configure_message_draft_grid(frm);
        render_crm_links(frm);
        render_signals_embedded_list(frm);
    }
});


const PROSPECT_ACTIONS_MENU = __('Prospect Actions');

function add_prospect_action(frm, label, handler) {
    frm.add_custom_button(__(label), handler, PROSPECT_ACTIONS_MENU);
}

function add_crm_action(frm, label, handler) {
    add_prospect_action(frm, `CRM — ${label}`, handler);
}

function reopen_prospect(frm) {
    frappe.confirm(__('Reopen this protected prospect and recalculate qualification?'), () => {
        call_and_reload(frm, 'reopen_prospect', { prospect: frm.doc.name });
    });
}

function mark_do_not_contact(frm) {
    frappe.confirm(__('Mark this prospect Do Not Contact? This blocks CRM preparation.'), () => {
        prompt_reason(__('Reason'), (reason) => {
            call_and_reload(frm, 'mark_do_not_contact', { prospect: frm.doc.name, reason });
        });
    });
}

function mark_rejected(frm) {
    prompt_reason(__('Rejected Reason'), (reason) => {
        call_and_reload(frm, 'mark_rejected', { prospect: frm.doc.name, reason });
    });
}

function convert_to_crm_lead(frm) {
    show_conversion_preview(frm, { allow_convert: true });
}

function configure_prospect_actions(frm) {
    add_prospect_action(frm, 'Recalculate Qualification', () => {
        call_and_reload(frm, 'recalculate_qualification', { prospect: frm.doc.name });
    });

    if (!is_terminal(frm)) {
        add_prospect_action(frm, 'Apply Lifecycle Suggestion', () => {
            call_and_reload(frm, 'apply_lifecycle_suggestion', { prospect: frm.doc.name });
        });
    }

    add_prospect_action(frm, 'Preview Message Draft', () => prompt_message_template(frm));

    if (['Find Contact', 'Ready for CRM Conversion'].includes(frm.doc.lifecycle_status)) {
        add_crm_action(frm, 'Mark as Not Ready for CRM', () => mark_not_ready_for_crm_conversion(frm));
    } else if (!is_terminal(frm)) {
        add_crm_action(frm, 'Mark as Ready for CRM Conversion', () => mark_ready_for_crm_conversion(frm));
    }

    if (can_prepare_crm(frm)) {
        add_crm_action(frm, 'Find Duplicates', () => show_conversion_preview(frm));
        add_crm_action(frm, 'Preview Conversion', () => show_conversion_preview(frm));

        if (is_manager_or_admin()) {
            if (!frm.doc.crm_lead) {
                add_crm_action(frm, 'Create Lead', () => {
                    confirm_create(frm, 'CRM Lead', 'create_crm_lead');
                });
            }
            add_crm_action(frm, 'Create Organization', () => {
                confirm_create(frm, 'CRM Organization', 'create_or_link_crm_organization');
            });
            if (has_contact_path(frm)) {
                add_crm_action(frm, 'Create Contact', () => {
                    confirm_create(frm, 'CRM Contact', 'create_or_link_crm_contact');
                });
            }
            add_crm_action(frm, 'Create Deal', () => prompt_deal_options(frm));
            add_link_button(frm, 'CRM Lead', 'crm_lead', 'CRM — Link Existing Lead');
            add_link_button(frm, 'CRM Organization', 'crm_organization', 'CRM — Link Existing Organization');
            add_link_button(frm, 'Contact', 'crm_contact', 'CRM — Link Existing Contact');
            add_link_button(frm, 'CRM Deal', 'crm_deal', 'CRM — Link Existing Deal');
        }
    }

    if (is_manager_or_admin()) {
        add_crm_action(frm, 'Convert to CRM Lead', () => convert_to_crm_lead(frm));
    }

    if ((frm.doc.crm_lead || frm.doc.crm_deal || frm.doc.crm_organization || frm.doc.crm_contact)
        && is_manager_or_admin()) {
        add_crm_action(frm, 'Sync SEI Context', () => {
            call_and_reload(frm, 'sync_sei_context_to_crm', { prospect: frm.doc.name });
        });
    }

    if (!['Converted to CRM Lead', 'Converted to CRM Deal', 'Do Not Contact'].includes(frm.doc.lifecycle_status)) {
        add_prospect_action(frm, 'Mark Rejected', () => mark_rejected(frm));
    }

    if (frm.doc.lifecycle_status !== 'Do Not Contact') {
        add_prospect_action(frm, 'Mark Do Not Contact', () => mark_do_not_contact(frm));
    }

    if (['Rejected', 'Do Not Contact'].includes(frm.doc.lifecycle_status) && is_manager_or_admin()) {
        add_prospect_action(
            frm,
            frm.doc.lifecycle_status === 'Do Not Contact' ? 'Remove Do Not Contact' : 'Reopen Prospect',
            () => reopen_prospect(frm)
        );
    }
}

function configure_primary_prospect_action(frm) {
    const lifecycle = frm.doc.lifecycle_status;
    let label;
    let handler;

    if (lifecycle === 'Qualified') {
        label = __('Mark as Ready for CRM Conversion');
        handler = () => mark_ready_for_crm_conversion(frm);
    } else if (lifecycle === 'Ready for CRM Conversion' && is_manager_or_admin()) {
        label = __('Convert to CRM Lead');
        handler = () => convert_to_crm_lead(frm);
    } else if (lifecycle === 'Rejected' && is_manager_or_admin()) {
        label = __('Reopen Prospect');
        handler = () => reopen_prospect(frm);
    } else if (lifecycle === 'Do Not Contact' && is_manager_or_admin()) {
        label = __('Remove Do Not Contact');
        handler = () => reopen_prospect(frm);
    }

    if (label && handler) {
        frm.page.set_primary_action(label, handler);
    } else {
        frm.page.clear_primary_action();
    }
}


function reload_if_cached_document_is_stale(frm) {
    if (frm.__sei_freshness_check_in_progress || frm.__sei_reloading_stale_cache) return;
    if (!frm.doc?.name || !frm.doc?.modified) return;

    frm.__sei_freshness_check_in_progress = true;
    frm.disable_save();

    frappe.db.get_value('SEI Prospect', frm.doc.name, 'modified')
        .then((r) => {
            const server_modified = r && r.message && r.message.modified;
            if (!server_modified || !frm.doc || !frm.doc.modified) return;

            const local_time = frappe.datetime.str_to_obj(frm.doc.modified);
            const server_time = frappe.datetime.str_to_obj(server_modified);

            if (server_time > local_time) {
                frm.__sei_reloading_stale_cache = true;
                frappe.show_alert({
                    message: __('Reloading latest prospect version.'),
                    indicator: 'orange'
                });
                return frm.reload_doc();
            }
        })
        .always(() => {
            frm.__sei_freshness_check_in_progress = false;
            frm.__sei_reloading_stale_cache = false;
            frm.enable_save();
        });
}

function can_prepare_crm(frm) {
    return ['Qualified', 'Manually Approved'].includes(frm.doc.qualification_status)
        && !frm.doc.do_not_contact
        && !['Rejected', 'Do Not Contact'].includes(frm.doc.lifecycle_status);
}

function has_contact_path(frm) {
    return (frm.doc.contacts || []).some(row => row.is_primary && (row.contact_name || row.emails || row.notes));
}

function is_terminal(frm) {
    return ['Rejected', 'Do Not Contact', 'Converted to CRM Lead', 'Converted to CRM Deal'].includes(frm.doc.lifecycle_status);
}

function call_and_reload(frm, action, args) {
    frappe.call({
        method: `sales_engagement_intelligence.sales_engagement_and_intelligence.api.${action}`,
        args,
        freeze: true,
        callback(r) {
            const message = unwrap_api_message(r);
            if (message) {
                frappe.show_alert({
                    message: message.ok === false ? __('SEI action failed.') : __('SEI action complete.'),
                    indicator: message.ok === false ? 'red' : 'green'
                }, message.ok === false ? 7 : 4);
            }
            frm.reload_doc();
        }
    });
}

function mark_ready_for_crm_conversion(frm) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.mark_ready_for_crm_conversion',
        args: { prospect: frm.doc.name },
        freeze: true,
        callback(r) {
            const message = unwrap_api_message(r) || {};
            if (message.ok === false) {
                const code = message.error && message.error.code;
                if (code === 'CRM_READINESS_REQUIREMENTS_NOT_MET' || code === 'CRM_CONVERSION_BLOCKED') {
                    show_crm_readiness_checklist(message);
                } else {
                    frappe.msgprint({
                        title: __('CRM Conversion Failed'),
                        indicator: 'red',
                        message: frappe.utils.escape_html(
                            (message.error && message.error.message) || __('Unexpected CRM conversion error.')
                        )
                    });
                }
                return;
            }
            frappe.show_alert({
                message: message.data && message.data.lifecycle_status === 'Find Contact'
                    ? __('CRM handoff approved. Add a usable primary contact to become Ready for CRM Conversion.')
                    : __('Prospect marked Ready for CRM Conversion.'),
                indicator: 'green'
            }, 6);
            frm.reload_doc();
        }
    });
}

function mark_not_ready_for_crm_conversion(frm) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.mark_not_ready_for_crm_conversion',
        args: { prospect: frm.doc.name },
        freeze: true,
        callback(r) {
            const message = unwrap_api_message(r) || {};
            if (message.ok === false) {
                frappe.show_alert({
                    message: (message.error && message.error.message) || __('Unable to undo CRM readiness.'),
                    indicator: 'red'
                }, 7);
                return;
            }
            frappe.show_alert({message: __('Prospect removed from CRM handoff.'), indicator: 'green'});
            frm.reload_doc();
        }
    });
}

function show_crm_readiness_checklist(message) {
    const details = message.error && message.error.details ? message.error.details : {};
    const requirements = details.requirements || [];
    const rows = requirements.map((requirement) => {
        const met = Boolean(requirement.met);
        return `<li><span class="indicator-pill ${met ? 'green' : 'red'}">${met ? '✓' : '✕'}</span> ${frappe.utils.escape_html(requirement.label || '')}</li>`;
    }).join('');
    frappe.msgprint({
        title: __('CRM Readiness Requirements'),
        message: `<p>${frappe.utils.escape_html((message.error && message.error.message) || __('Requirements not met.'))}</p><ul style="list-style:none;padding-left:0">${rows}</ul>`,
        indicator: 'red'
    });
}

function show_conversion_preview(frm, options = {}) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_crm_conversion',
        args: { prospect: frm.doc.name },
        freeze: true,
        callback(r) {
            const data = unwrap_api_data(r);
            const fields = [{ fieldtype: 'HTML', fieldname: 'preview_html' }];
            const dialog_options = {
                title: options.allow_convert ? __('Convert to CRM Lead') : __('CRM Conversion Preview'),
                size: 'extra-large',
                fields
            };
            if (options.allow_convert) {
                dialog_options.primary_action_label = __('Convert to CRM Lead');
                dialog_options.primary_action = () => convert_from_preview(frm, dialog);
            }
            const dialog = new frappe.ui.Dialog(dialog_options);
            dialog.fields_dict.preview_html.$wrapper.html(render_preview_html(data));
            dialog.show();
        }
    });
}


function convert_from_preview(frm, dialog) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.convert_to_crm_lead',
        args: { prospect: frm.doc.name },
        freeze: true,
        callback(r) {
            const message = unwrap_api_message(r) || {};
            if (message.ok === false) {
                show_crm_readiness_checklist(message);
                return;
            }
            dialog.hide();
            frappe.show_alert({ message: __('Prospect converted to CRM Lead.'), indicator: 'green' });
            frm.reload_doc();
        }
    });
}


function unwrap_api_message(r) {
    return (r && r.message) || null;
}

function unwrap_api_data(r) {
    const message = unwrap_api_message(r) || {};
    return message.ok === true ? (message.data || {}) : message;
}

function render_preview_html(data) {
    const eligibility = data.eligibility || {};
    const reasons = (eligibility.reasons || [])
        .map(reason => `<li>${frappe.utils.escape_html(reason)}</li>`)
        .join('');
    const duplicates = data.duplicates || {};
    const payloads = data.payloads || {};

    return `
        <p><b>${__('Lead Creation Eligible')}:</b> ${eligibility.eligible ? __('Yes') : __('No')}</p>
        ${reasons ? `<p><b>${__('Blocking / Warning Reasons')}</b></p><ul>${reasons}</ul>` : ''}
        <h4>${__('Possible CRM Duplicates')}</h4>
        ${render_duplicate_group(__('CRM Leads'), duplicates.crm_leads || [], 'CRM Lead')}
        ${render_duplicate_group(__('CRM Organizations'), duplicates.crm_organizations || [], 'CRM Organization')}
        ${render_duplicate_group(__('CRM Contacts'), duplicates.crm_contacts || [], 'Contact')}
        ${render_duplicate_group(__('CRM Deals'), duplicates.crm_deals || [], 'CRM Deal')}
        <h4>${__('Payload Preview')}</h4>
        <pre style="white-space: pre-wrap; max-height: 420px; overflow: auto;">${frappe.utils.escape_html(JSON.stringify(payloads, null, 2))}</pre>
    `;
}

function render_duplicate_group(label, rows, doctype) {
    if (!rows.length) {
        return `<p><b>${label}:</b> ${__('None found')}</p>`;
    }

    const items = rows.map(row => {
        const title = row.title || row.name;
        const reason = row.reason || '';
        const route = crm_frontend_route(doctype, row.name);
        return `<li><a href="${route}">${frappe.utils.escape_html(title)}</a> — ${frappe.utils.escape_html(reason)}</li>`;
    }).join('');
    return `<p><b>${label}</b></p><ul>${items}</ul>`;
}


function crm_frontend_route(doctype, record_name) {
    const collections = {
        'CRM Lead': 'leads',
        'CRM Deal': 'deals',
        'CRM Organization': 'organizations',
        'Contact': 'contacts'
    };
    return `/crm/${collections[doctype]}/${encodeURIComponent(record_name)}`;
}

function render_crm_links(frm) {
    const field = frm.fields_dict.crm_links_html;
    if (!field) return;
    field.$wrapper.html(`<p class="text-muted">${__('Loading CRM records…')}</p>`);
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.get_linked_crm_records',
        args: { prospect: frm.doc.name },
        callback(r) {
            const data = unwrap_api_data(r) || {};
            const groups = [
                [__('CRM Leads'), 'CRM Lead', data.crm_leads || []],
                [__('CRM Organizations'), 'CRM Organization', data.crm_organizations || []],
                [__('CRM Contacts'), 'Contact', data.crm_contacts || []],
                [__('CRM Deals'), 'CRM Deal', data.crm_deals || []]
            ];
            const html = groups.map(([label, doctype, rows]) => {
                const links = rows.length
                    ? rows.map(row => `<a class="btn btn-default btn-sm mr-2 mb-2" href="${crm_frontend_route(doctype, row.name)}">${frappe.utils.escape_html(row.title || row.name)}</a>`).join('')
                    : `<span class="text-muted">${__('None')}</span>`;
                return `<div class="mb-3"><div class="text-muted small mb-1">${label}</div><div>${links}</div></div>`;
            }).join('');
            field.$wrapper.html(`<div class="sei-crm-links">${html}</div>`);
        }
    });
}

function confirm_create(frm, label, action, options = {}) {
    frappe.confirm(
        __(`Create ${label} from this SEI Prospect? Review CRM duplicates/preview first if you have not already done so.`),
        () => call_and_reload(frm, action, { prospect: frm.doc.name, options })
    );
}

function prompt_deal_options(frm) {
    frappe.prompt(
        [
            {
                fieldtype: 'Check',
                fieldname: 'manager_override',
                label: __('Manager override: commercial basis confirmed outside SEI attribution')
            },
            {
                fieldtype: 'Check',
                fieldname: 'allow_direct_deal',
                label: __('Allow direct Deal creation without linked CRM Lead'),
                default: frm.doc.crm_lead ? 0 : 1
            }
        ],
        (values) => {
            confirm_create(frm, 'CRM Deal', 'create_crm_deal', {
                manager_override: Boolean(values.manager_override),
                allow_direct_deal: Boolean(values.allow_direct_deal)
            });
        },
        __('CRM Deal Options')
    );
}

function add_link_button(frm, doctype, fieldname, action_label = null) {
    if (frm.doc[fieldname]) return;
    const label = __(action_label || `Link Existing ${doctype}`);
    frm.add_custom_button(label, () => {
        frappe.prompt(
            [{ fieldtype: 'Link', fieldname: 'record_name', label: doctype, options: doctype, reqd: 1 }],
            (values) => {
                call_and_reload(frm, 'link_existing_crm_record', {
                    prospect: frm.doc.name,
                    doctype,
                    record_name: values.record_name
                });
            },
            label
        );
    }, PROSPECT_ACTIONS_MENU);
}

function prompt_reason(label, callback) {
    frappe.prompt(
        [{ fieldtype: 'Small Text', fieldname: 'reason', label, reqd: 0 }],
        (values) => callback(values.reason),
        label
    );
}

function is_manager_or_admin() {
    return frappe.session.user === 'Administrator'
        || frappe.user_roles.includes('Administrator')
        || frappe.user_roles.includes('Sales Engagement Manager');
}



function prompt_message_template(frm) {
    const fields = [
        {
            fieldname: 'template',
            label: __('Message Template'),
            fieldtype: 'Link',
            options: 'SEI Message Template',
            reqd: 1,
            get_query() {
                const filters = { active: 1 };
                return { filters };
            }
        }
    ];

    const default_template = frm.doc.suggested_message_template || null;
    frappe.prompt(fields, (values) => {
        show_message_draft_preview(frm, values.template);
    }, __('Preview Message Draft'), __('Render Preview'));

    // frappe.prompt does not expose a stable direct default hook across Frappe
    // versions. Keep the suggested template visible on the form instead of
    // relying on undocumented dialog internals.
    if (default_template) {
        frappe.show_alert({
            message: __('Suggested template: {0}', [default_template]),
            indicator: 'blue'
        });
    }
}

function show_message_draft_preview(frm, template) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_message_draft',
        args: { prospect: frm.doc.name, template },
        freeze: true,
        callback(r) {
            const message = unwrap_api_message(r) || {};
            if (message.ok === false) {
                frappe.show_alert({
                    message: __('Draft preview failed.'),
                    indicator: 'red'
                }, 7);
                return;
            }
            const data = message.data || {};
            const dialog = new frappe.ui.Dialog({
                title: __('Message Draft Preview'),
                size: 'extra-large',
                fields: [{ fieldtype: 'HTML', fieldname: 'draft_html' }]
            });
            dialog.fields_dict.draft_html.$wrapper.html(render_message_draft_html(data));
            dialog.show();
        }
    });
}

function render_message_draft_html(data) {
    const missing = data.missing_variables || [];
    const missing_html = missing.length
        ? `<p><b>${__('Missing Variables')}:</b> ${missing.map(value => frappe.utils.escape_html(value)).join(', ')}</p>`
        : `<p><b>${__('Missing Variables')}:</b> ${__('None')}</p>`;
    const safety = data.safety || {};
    return `
        <p><b>${__('Channel')}:</b> ${frappe.utils.escape_html(data.channel || '')}</p>
        ${missing_html}
        <h4>${__('Subject')}</h4>
        <pre style="white-space: pre-wrap;">${frappe.utils.escape_html(data.subject || '')}</pre>
        <h4>${__('Body')}</h4>
        <pre style="white-space: pre-wrap; max-height: 420px; overflow: auto;">${frappe.utils.escape_html(data.body || '')}</pre>
        <h4>${__('Safety')}</h4>
        <pre style="white-space: pre-wrap;">${frappe.utils.escape_html(JSON.stringify(safety, null, 2))}</pre>
        <p class="text-muted">${__('This preview does not send outreach, create a Communication, create CRM records, or change lifecycle status.')}</p>
    `;
}


function render_signals_embedded_list(frm) {
    const field = frm.fields_dict.signals_embedded_list;
    if (!field || !field.$wrapper) return;

    const wrapper = field.$wrapper;

    if (frm.is_new()) {
        wrapper.html(`<p class="text-muted">${__('Save this prospect before adding signals.')}</p>`);
        return;
    }

    wrapper.html(`<p class="text-muted">${__('Loading signals...')}</p>`);

    frappe.db.get_list('SEI Signal', {
        fields: [
            'name',
            'signal_type',
            'signal_strength',
            'evidence_basis',
            'exclude_from_qualification',
            'confidence',
            'source_date',
            'modified'
        ],
        filters: { prospect: frm.doc.name },
        order_by: 'source_date desc, modified desc',
        limit: 100
    }).then((signals) => {
        wrapper.html(render_signals_table(frm, signals || []));
        wrapper.find('[data-sei-action="new-signal"]').on('click', () => {
            frappe.new_doc('SEI Signal', {
                prospect: frm.doc.name,
                prospect_name: frm.doc.prospect_name
            });
        });
    }).catch(() => {
        wrapper.html(`<p class="text-muted">${__('Unable to load signals.')}</p>`);
    });
}

function render_signals_table(frm, signals) {
    const new_button = `
        <button class="btn btn-xs btn-default" data-sei-action="new-signal">
            ${__('New Signal')}
        </button>
    `;

    if (!signals.length) {
        return `
            <div class="sei-signals-embedded-list">
                <div class="flex justify-between align-center" style="margin-bottom: var(--margin-sm);">
                    <p class="text-muted" style="margin: 0;">${__('No signals recorded for this prospect yet.')}</p>
                    ${new_button}
                </div>
            </div>
        `;
    }

    const rows = signals.map((signal) => {
        const route = `/app/sei-signal/${encodeURIComponent(signal.name)}`;
        const excluded = signal.exclude_from_qualification ? __('Yes') : __('No');
        const confidence = signal.confidence === null || signal.confidence === undefined
            ? ''
            : `${flt(signal.confidence, 2)}%`;

        return `
            <tr>
                <td><a href="${route}">${frappe.utils.escape_html(signal.signal_type || signal.name)}</a></td>
                <td>${render_signal_badge(signal.signal_strength)}</td>
                <td>${frappe.utils.escape_html(signal.evidence_basis || '')}</td>
                <td>${excluded}</td>
                <td>${confidence}</td>
                <td>${frappe.utils.escape_html(signal.source_date || '')}</td>
            </tr>
        `;
    }).join('');

    return `
        <div class="sei-signals-embedded-list">
            <div class="flex justify-between align-center" style="margin-bottom: var(--margin-sm);">
                <p class="text-muted" style="margin: 0;">${__('Signals linked to this prospect')}</p>
                ${new_button}
            </div>
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead>
                        <tr>
                            <th>${__('Signal Type')}</th>
                            <th>${__('Strength')}</th>
                            <th>${__('Evidence')}</th>
                            <th>${__('Excluded')}</th>
                            <th>${__('Confidence')}</th>
                            <th>${__('Source Date')}</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>
        </div>
    `;
}

function render_signal_badge(strength) {
    if (!strength) return '';
    const color = {
        Strong: 'green',
        Moderate: 'orange',
        Weak: 'gray'
    }[strength] || 'gray';
    return `<span class="indicator-pill ${color}">${frappe.utils.escape_html(strength)}</span>`;
}



function configure_message_draft_grid(frm) {
    const field = frm.fields_dict.message_drafts;
    if (!field || !field.grid || !frm.doc.name) return;
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.get_prospect_contact_options',
        args: { prospect: frm.doc.name },
        callback(r) {
            const available = (r.message && r.message.data) || [];
            const saved = (frm.doc.message_drafts || [])
                .map(row => row.to_contact)
                .filter(Boolean);
            const options = [...new Set([...available, ...saved])];
            field.grid.update_docfield_property('to_contact', 'options', options.join('\n'));
            refresh_open_message_draft_editor(field);
        }
    });
    normalize_managed_grid_editor(field, 'message-draft');
    isolate_message_draft_sent_checkbox(field);
}


function refresh_open_message_draft_editor(field) {
    const openRow = field.grid && field.grid.open_grid_row;
    if (!openRow || !openRow.doc || !openRow.grid_form) return;
    const fields = openRow.grid_form.fields_dict || {};
    const recipient = fields.to_contact;
    if (recipient) {
        recipient.df.options = field.grid.get_field('to_contact').options;
    }
    ['platform', 'from_user', 'to_contact', 'cc', 'subject', 'body'].forEach(fieldname => {
        const control = fields[fieldname];
        if (!control) return;
        control.refresh();
        control.set_value(openRow.doc[fieldname] ?? '');
    });
}


function isolate_message_draft_sent_checkbox(field) {
    if (!field || !field.$wrapper) return;

    const bind = () => {
        field.$wrapper.find('[data-fieldname="sent"] input').each(function () {
            const $checkbox = $(this);
            if ($checkbox.attr('data-sei-sent-bound')) return;
            $checkbox
                .attr('data-sei-sent-bound', '1')
                .on('mousedown.sei-sent click.sei-sent', function (event) {
                    event.stopPropagation();
                });
        });
    };

    bind();
    if (!field.__sei_sent_checkbox_observer) {
        field.__sei_sent_checkbox_observer = new MutationObserver(bind);
        field.__sei_sent_checkbox_observer.observe(field.$wrapper.get(0), {
            childList: true,
            subtree: true
        });
    }
}


function normalize_managed_grid_editor(field, key) {
    if (!field || !field.$wrapper) return;

    const meaningfulFields = key === 'contact'
        ? ['contact_role', 'contact_name', 'emails', 'notes', 'is_primary']
        : ['platform', 'to_contact', 'cc', 'subject', 'body'];

    const removeEmptyLocalRow = $form => {
        const cdn = $form.closest('.grid-row').attr('data-name');
        const row = cdn && locals[field.grid.doctype] && locals[field.grid.doctype][cdn];
        if (!row || !row.__islocal) return false;
        const hasMeaningfulValue = meaningfulFields.some(name => {
            const value = row[name];
            return typeof value === 'string' ? value.trim() : Boolean(value);
        });
        if (hasMeaningfulValue) return false;
        field.grid.grid_rows_by_docname[cdn]?.remove();
        return true;
    };

    const normalize = () => {
        field.$wrapper.find('.form-in-grid').each(function () {
            const $form = $(this);
            $form.find('.grid-insert-row-below, .grid-append-row').remove();

            const $close = $form.find('.grid-collapse-row');
            if ($close.length && !$close.attr('data-sei-close-icon')) {
                $close
                    .attr('data-sei-close-icon', '1')
                    .attr('aria-label', __('Close'))
                    .attr('title', __('Close'))
                    .empty()
                    .html('&times;')
                    .on('click.sei-empty-row', function (event) {
                        if (removeEmptyLocalRow($form)) {
                            event.preventDefault();
                            event.stopImmediatePropagation();
                        }
                    });
            }

            const $body = $form.children('.grid-form-body');
            const $footer = $body.children('.grid-footer-toolbar');
            if ($footer.length && !$footer.attr('data-sei-fixed-footer')) {
                $footer
                    .attr('data-sei-fixed-footer', '1')
                    .removeClass('hidden-xs')
                    .insertAfter($body);
            }

            const $footerActions = $form.children('.grid-footer-toolbar').find('.row-actions');
            if ($footerActions.length && !$footerActions.find('.sei-grid-done').length) {
                $('<button type="button" class="btn btn-primary btn-sm sei-grid-done"></button>')
                    .text(__('Done'))
                    .on('click', function (event) {
                        event.preventDefault();
                        event.stopImmediatePropagation();
                        $close.trigger('click');
                    })
                    .appendTo($footerActions);
            }
        });
    };

    normalize();
    const observerKey = `__sei_${key.replace('-', '_')}_grid_observer`;
    if (!field[observerKey]) {
        field[observerKey] = new MutationObserver(normalize);
        field[observerKey].observe(field.$wrapper.get(0), {
            childList: true,
            subtree: true
        });
    }
}


function configure_contact_grid(frm) {
    const field = frm.fields_dict.contacts;
    if (!field || !field.$wrapper) return;

    if (field.grid) {
        const email_field = field.grid.get_field('emails');
        if (email_field) {
            email_field.formatter = value => {
                const display = String(value || '')
                    .split(/[\n,;]+/)
                    .map(email => email.trim())
                    .filter(Boolean)
                    .join(', ');
                const escaped = frappe.utils.escape_html(display);
                return `<span class="ellipsis" title="${escaped}">${escaped}</span>`;
            };
        }
    }

    normalize_managed_grid_editor(field, 'contact');
}


frappe.ui.form.on('SEI Prospect Message Draft', {
    sent(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (!row.sent) {
            if (!row.sent_on && !row.crm_email) return;
            frappe.call({
                method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.mark_message_draft_unsent',
                args: { draft: row.name },
                freeze: true,
                callback() {
                    frm.reload_doc();
                },
                error() {
                    frappe.model.set_value(cdt, cdn, 'sent', 1);
                }
            });
            return;
        }
        if (row.__islocal) {
            frappe.model.set_value(cdt, cdn, 'sent', 0);
            frappe.msgprint(__('Save the message draft before marking it as sent.'));
            return;
        }
        frappe.call({
            method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.mark_message_draft_sent',
            args: { draft: row.name },
            freeze: true,
            callback() {
                frm.reload_doc();
            },
            error() {
                frappe.model.set_value(cdt, cdn, 'sent', 0);
            }
        });
    }
});
